# Resultado - 20260526T063207-radar-anti-empty-script-spec

## summary honesto

Se convierte el contrato anti informe vacio de radares en una especificacion de script/gate aplicable a inmobiliaria e instrumental. No se navego, no se contacto a terceros y no se usaron credenciales.

**Evidencia:** el frente exige fuentes consultadas, candidatos, descartes, fallback routes, comparables/precio y recomendacion accionable. Los scorecards ya separan campos de inmobiliaria Junin e instrumental medico.

**Inferencia:** el gate debe validar contrato y estado minimo antes de permitir `completed`; si el agente trae solo fallas tecnicas, debe quedar `blocked` o `needs_review`, no reporte final.

**Opinion:** conviene implementarlo como validador CLI unico, con salida JSON para que 5.3 no pueda pasar por alto el bloqueo.

## coverage_table

| fuente | uso | limite |
| --- | --- | --- |
| `context/fronts/radares.md` | Estado canonico y regla anti informe vacio. | No contiene schema ejecutable. |
| `results/20260525T120001-radares-anti-informe-vacio-v1.result.md` | Contrato, thresholds, fallback routes y division 5.3/Pablo. | Thresholds requieren calibracion real. |
| `decisions/radar_scorecards_v1.md` | Campos y scoring base para inmobiliaria e instrumental. | Score simple; debe pasar a estructura JSON. |

## json_schema

```json
{
  "type": "object",
  "required": ["job_id", "kind", "scope", "run_summary", "sources_attempted", "candidates", "rejected_candidates", "conclusion"],
  "properties": {
    "job_id": {"type": "string"},
    "kind": {"enum": ["inmobiliaria", "instrumental", "inversion_general"]},
    "scope": {
      "type": "object",
      "required": ["query", "market_or_geography", "constraints"],
      "properties": {
        "query": {"type": "string"},
        "market_or_geography": {"type": "string"},
        "constraints": {"type": "array", "items": {"type": "string"}}
      }
    },
    "run_summary": {
      "type": "object",
      "required": ["status", "score", "reason"],
      "properties": {
        "status": {"enum": ["completed", "needs_review", "blocked", "delegated_to_pablo"]},
        "score": {"type": "number", "minimum": 0, "maximum": 100},
        "reason": {"type": "string"}
      }
    },
    "sources_attempted": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "source_type", "outcome", "evidence"],
        "properties": {
          "name": {"type": "string"},
          "url_or_query": {"type": "string"},
          "source_type": {"enum": ["direct_page", "marketplace", "search", "pdf", "official", "snippet", "comparable", "cached", "local_context"]},
          "outcome": {"enum": ["success", "blocked", "no_results", "partial", "error"]},
          "evidence": {"type": "string"},
          "next_route_if_failed": {"type": "string"}
        }
      }
    },
    "fallback_routes_used": {"type": "array"},
    "candidates": {"type": "array"},
    "rejected_candidates": {"type": "array"},
    "conclusion": {
      "type": "object",
      "required": ["recommendation", "confidence", "next_action"]
    }
  }
}
```

## gate_rules

| regla | estado minimo |
| --- | --- |
| `sources_attempted < 5` y `candidates = 0` | `blocked` |
| fuente principal bloqueada y `fallback_routes_used < 2` | `blocked` |
| contiene "no pude" sin fallback documentado | `blocked` |
| score `< 50` | `blocked` |
| score `50-74` | `needs_review` |
| score `>= 75`, contrato completo y sin hard fails | `completed` |
| candidato sin precio ni ruta concreta para obtenerlo | `needs_review` |
| instrumental medico sin trazabilidad/regulatorio/soporte | `needs_review` o `blocked` segun riesgo |
| 0 candidatos con 5+ fuentes, descartes y comparables | `needs_review`, no `completed` |

Hard fail universal: no contactar, no comprar, no usar login/credenciales, no inventar precio/comparable.

## fallback_routes

- Inmobiliaria: portal directo, busqueda por direccion/zona, snippets/cache, marketplace espejo, ML/Zonaprop/Argenprop, comparables de la zona.
- Instrumental: fabricante, marketplaces internacionales, eBay/ML, distribuidor local, registro/trazabilidad si aplica, comparables por marca/modelo.
- Si no hay candidatos: reportar queries, fuentes, descartes, criterios y proxima corrida.
- Si una fuente bloquea: documentar bloqueo y dos alternativas antes de cerrar.

## script_plan

```text
scripts/qa/validate_radar_report.py
  --input results/<job>.candidates.json
  --kind inmobiliaria|instrumental|inversion_general
  --min-sources 5
  --output-json
```

Salida:

```json
{
  "ok": false,
  "status": "blocked",
  "score": 42,
  "hard_fails": ["blocked_empty_technical_failure_report"],
  "warnings": ["candidate_missing_price"],
  "required_next_action": "usar al menos dos fallback_routes o delegar a Pablo"
}
```

Integracion:

1. 5.3 genera `candidates.json` junto al reporte.
2. El validador calcula estado minimo permitido.
3. Si `blocked`, no se envia reporte final; se guarda artifact con razon.
4. Si `needs_review`, se crea job a Pablo con reporte parcial y bloqueo exacto.
5. Si `completed`, se permite reporte al orquestador, nunca compra/contacto.

## qa_examples

| caso | input | esperado |
| --- | --- | --- |
| Todo falla tecnicamente | 3 fuentes, todas `error`, 0 candidatos | `blocked`, razon `blocked_empty_technical_failure_report` |
| Fuente bloqueada sin fallback | 1 fuente `blocked`, 0 alternativas | `blocked`, pedir fallback |
| Candidato sin precio | candidato con ubicacion/modelo pero sin precio ni ruta | `needs_review` |
| Cero candidatos con universo documentado | 7 fuentes, 8 descartes, comparables | `needs_review` |
| Oportunidad real Junin | ubicacion, precio, comparables, refaccion, next action | `completed` si score >= 75 |
| Instrumental sin trazabilidad | precio atractivo pero sin marca/registro/vendedor claro | `blocked` o `needs_review` |

## risks_limits

- El gate no garantiza oportunidades; garantiza que no se cierre vacio.
- Agentes pueden inflar candidatos malos para pasar minimo; por eso score y descartes son obligatorios.
- Instrumental medico necesita thresholds mas conservadores que inmobiliaria.
- Fuentes bloqueadas no prueban ausencia de oportunidad.

## recommendation

Implementar el validador CLI antes de nuevas corridas rutinarias. Usar como primera regla operativa: ningun radar `completed` con score < 75 o sin fuentes/fallbacks/candidatos trazables.

## confidence

Alta para schema y gates; media para thresholds hasta calibrarlos con corridas reales.

## evidence_paths

- `jobs/20260526T063207-radar-anti-empty-script-spec.md`
- `context/fronts/radares.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `decisions/radar_scorecards_v1.md`

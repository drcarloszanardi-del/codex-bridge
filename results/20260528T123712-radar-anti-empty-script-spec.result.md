---
job_id: 20260528T123712-radar-anti-empty-script-spec
worker: personal-xh
status: completed
completed_at: 2026-05-28T12:42:18-03:00
front: INVERSIONES
no_external_actions: true
no_secrets: true
---

# Resultado - especificacion gate anti informe vacio radares

## summary honesto

Se convirtio el contrato anti informe vacio en una especificacion implementable para un script/gate reutilizable en inmobiliaria e instrumental. No se navego, no se contacto a terceros y no se usaron credenciales. El gate no garantiza oportunidades; obliga a entregar evidencia, descartes, rutas alternativas y una decision accionable antes de aceptar un radar como completado.

## coverage_table

| Seccion pedida | Estado | Evidencia usada |
|---|---|---|
| `json_schema` | cubierto | Contrato de `radar_report` previo y scorecards. |
| `gate_rules` | cubierto | Reglas anti-vacio del frente radares. |
| `fallback_routes` | cubierto | Source recovery obligatorio. |
| `script_plan` | cubierto | Plan para `scripts/qa/validate_radar_report.py`. |
| `qa_examples` | cubierto | Casos de bloqueo/paso para inmobiliaria e instrumental. |

## evidencia

- El frente radares bloquea frases como `no pude`, `no encontre nada` y `no hay oportunidades` si no hay rutas alternativas, evidencia y proxima accion.
- El resultado anti informe vacio previo define estados `completed`, `needs_review`, `blocked` y `delegated_to_pablo`.
- `decisions/radar_scorecards_v1.md` define campos y descarte automatico para inmobiliaria Junin e instrumental.

## inferencias

- La forma mas portable es validar un JSON embebido o adjunto al markdown del radar, no parsear texto libre.
- `completed` debe exigir thresholds estrictos; `needs_review` permite salvar corridas con evidencia parcial sin mentir como cierre final.
- El script debe fallar por defecto cuando falte una seccion critica.

## opinion

El gate debe premiar honestidad verificable por encima de cantidad. Un radar con cero candidatos puede ser util, pero solo si muestra universo revisado, descartes y siguiente corrida concreta.

## json_schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "RadarReportV1",
  "type": "object",
  "required": ["job_id", "kind", "scope", "run_summary", "sources_attempted", "fallback_routes_used", "candidates", "rejected_candidates", "conclusion"],
  "properties": {
    "job_id": { "type": "string", "minLength": 8 },
    "kind": { "enum": ["inmobiliaria", "instrumental", "inversion_general"] },
    "scope": {
      "type": "object",
      "required": ["query", "geography_or_market", "constraints", "forbidden_actions"],
      "properties": {
        "query": { "type": "string", "minLength": 3 },
        "geography_or_market": { "type": "string", "minLength": 3 },
        "constraints": { "type": "array", "items": { "type": "string" } },
        "forbidden_actions": { "type": "array", "items": { "enum": ["contactar", "comprar", "login", "credenciales"] } }
      }
    },
    "run_summary": {
      "type": "object",
      "required": ["started_at", "completed_at", "status", "score", "reason"],
      "properties": {
        "status": { "enum": ["completed", "needs_review", "blocked", "delegated_to_pablo"] },
        "score": { "type": "integer", "minimum": 0, "maximum": 100 },
        "reason": { "type": "string", "minLength": 10 }
      }
    },
    "sources_attempted": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "url_or_query", "source_type", "outcome", "evidence", "next_route_if_failed"],
        "properties": {
          "source_type": { "enum": ["direct_page", "marketplace", "search", "pdf", "official", "snippet", "comparable", "cached", "local_context"] },
          "outcome": { "enum": ["success", "blocked", "no_results", "partial", "error"] },
          "evidence": { "type": "string", "minLength": 5 }
        }
      }
    },
    "fallback_routes_used": { "type": "array" },
    "candidates": { "type": "array" },
    "rejected_candidates": { "type": "array" },
    "conclusion": {
      "type": "object",
      "required": ["recommendation", "confidence", "next_run_or_handoff"]
    }
  }
}
```

## gate_rules

| Regla | Resultado |
|---|---|
| `completed` requiere score >= 75, todas las secciones obligatorias y al menos 5 fuentes si hay cero candidatos. | pass |
| Score 50-74 con evidencia parcial. | `needs_review` |
| Score < 50. | fail como `blocked` |
| 0 candidatos con menos de 5 fuentes intentadas. | fail |
| Fuente principal bloqueada sin ruta alternativa. | fail |
| Texto contiene `no pude`, `no encontre nada`, `no hay oportunidades` sin `fallback_routes_used` y `next_run_or_handoff`. | fail |
| Inmobiliaria sin ubicacion verificable o sin precio/comparables. | fail o `needs_review` si hay ruta concreta |
| Instrumental medico sin marca/modelo o sin trazabilidad/regulatorio cuando aplica. | fail o `needs_review` |
| Candidato sin `decision` y `next_action`. | fail |
| Rechazos sin motivo. | fail |

## fallback_routes

| Bloqueo | Rutas minimas exigidas |
|---|---|
| Web inmobiliaria no abre | busqueda por direccion/zona, portal espejo, snippets/cache, comparables radio/m2 |
| Precio inmobiliario faltante | misma propiedad en otro portal, comparables por radio, pedir `pendiente_precio` con ruta |
| Marketplace instrumental bloqueado | buscar marca/modelo en eBay, Mercado Libre, importador, fabricante |
| Modelo ambiguo | ficha/manual/fotos/specs antes de candidato fuerte |
| Requiere login/credencial | no usar credenciales; buscar fuente publica y registrar bloqueo |
| Cero candidatos | registrar queries, fuentes, universo revisado, descartes y proxima corrida |

## script_plan

1. Crear `scripts/qa/validate_radar_report.py`.
2. Aceptar entrada markdown o JSON: `--input results/<job>.result.md --kind inmobiliaria|instrumental`.
3. Extraer bloque fenced `radar_report` si el archivo es markdown; si no existe, buscar `.json` hermano.
4. Validar schema base y campos requeridos por `kind`.
5. Calcular score minimo con pesos de `decisions/radar_scorecards_v1.md`.
6. Aplicar frases prohibidas y reglas de fallback.
7. Emitir JSON de salida:

```json
{
  "ok": false,
  "status_allowed": "blocked",
  "score": 42,
  "errors": ["missing fallback route for blocked direct page"],
  "warnings": ["candidate without comparable price"],
  "next_action": "run source recovery or delegate to Pablo"
}
```

8. Usar exit code `0` solo si el status declarado es compatible con el score y las reglas.
9. Integrar al pipeline de radares antes de aceptar un resultado `completed`.

## qa_examples

| Caso | Entrada minima | Esperado |
|---|---|---|
| Web inmobiliaria bloqueada, sin alternativa | 1 source `blocked`, 0 fallback | fail `blocked` |
| 0 candidatos, 6 fuentes, 12 descartes con motivo, proxima corrida | status `needs_review` | pass como `needs_review`, no `completed` |
| Casa con precio, ubicacion, comparables y riesgos | score >= 75 | pass `completed` |
| Instrumental con marca/modelo/precio pero sin trazabilidad | score 50-74 | `needs_review` |
| Informe con frase `no pude abrir` y sin fallback | cualquier score | fail |
| Candidato sin decision sugerida | candidato incompleto | fail |

## risks_limits

- El gate puede incentivar candidatos de baja calidad para pasar minimos; por eso score y descartes deben penalizar incertidumbre.
- Los thresholds iniciales necesitan calibracion con corridas reales.
- Para instrumental medico, trazabilidad/regulatorio debe pesar mas que margen economico.
- El script no reemplaza juicio estrategico; solo impide cierre vacio o sin evidencia.

## recommendation

Implementar el validator como requisito de merge para resultados de radares. Primera version: `completed` solo con score >= 75; `needs_review` para 50-74; `blocked` para <50 o faltantes criticos. Delegar a Pablo solo cuando haya evidencia parcial y bloqueo dificil, no cuando falte trabajo basico.

## confidence

Alta para schema, reglas y rutas alternativas porque consolidan el contexto canonico y resultados previos. Media para thresholds numericos hasta medirlos con reportes reales.

## evidence_paths

- `jobs/20260528T123712-radar-anti-empty-script-spec.md`
- `context/fronts/radares.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `decisions/radar_scorecards_v1.md`


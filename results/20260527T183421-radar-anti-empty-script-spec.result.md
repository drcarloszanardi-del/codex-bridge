---
job_id: 20260527T183421-radar-anti-empty-script-spec
worker: personal-xh
status: completed
completed_at: 2026-05-27T18:38:00-03:00
front: INVERSIONES
no_external_actions: true
no_secrets: true
---

# Resultado - Gate anti informe vacio para radares

## summary honesto

Especificacion implementable para un script/gate que bloquee reportes vacios de
inmobiliaria e instrumental. El gate no busca oportunidades por si mismo: obliga
a que cada radar declare fuentes, candidatos, descartes, rutas alternativas,
score, decision y proxima accion concreta antes de poder cerrar como
`completed`.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T183421-radar-anti-empty-script-spec.md` | Revisada | Workorder y secciones requeridas. |
| `context/fronts/radares.md` | Revisada | Canon anti informe vacio y source recovery. |
| `results/20260525T120001-radares-anti-informe-vacio-v1.result.md` | Revisada | Contrato, thresholds y scorecards. |
| `decisions/radar_scorecards_v1.md` | Revisada | Campos y descarte automatico. |

## evidence_inference_opinion

| Tipo | Contenido |
| --- | --- |
| Evidencia | Ya existe contrato: fuentes, candidatos, descartes, rutas alternativas, comparables, recomendacion o razon verificable. |
| Inferencia | Conviene validar primero JSON estructurado y aceptar Markdown solo si contiene bloque JSON/YAML parseable. |
| Opinion | El gate debe fallar fuerte ante "no pude" sin recuperacion; es mejor devolver `needs_review` que cerrar mal. |

## json_schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "radar_report_v1",
  "type": "object",
  "required": ["job_id", "kind", "scope", "run_summary", "sources_attempted", "candidates", "rejected_candidates", "conclusion"],
  "properties": {
    "job_id": {"type": "string", "minLength": 8},
    "kind": {"enum": ["inmobiliaria", "instrumental", "inversion_general"]},
    "scope": {
      "type": "object",
      "required": ["query", "market", "constraints"],
      "properties": {
        "query": {"type": "string"},
        "market": {"type": "string"},
        "constraints": {"type": "array", "items": {"type": "string"}}
      }
    },
    "run_summary": {
      "type": "object",
      "required": ["status", "score", "reason"],
      "properties": {
        "status": {"enum": ["completed", "needs_review", "blocked", "delegated_to_pablo"]},
        "score": {"type": "integer", "minimum": 0, "maximum": 100},
        "reason": {"type": "string"}
      }
    },
    "sources_attempted": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "url_or_query", "source_type", "outcome", "evidence", "next_route_if_failed"],
        "properties": {
          "source_type": {"enum": ["direct_page", "marketplace", "search", "pdf", "official", "snippet", "comparable", "cached", "local_context"]},
          "outcome": {"enum": ["success", "blocked", "no_results", "partial", "error"]},
          "evidence": {"type": "string"}
        }
      }
    },
    "fallback_routes_used": {"type": "array"},
    "candidates": {"type": "array"},
    "rejected_candidates": {"type": "array"},
    "conclusion": {
      "type": "object",
      "required": ["recommendation", "confidence", "next_action"],
      "properties": {
        "recommendation": {"type": "string"},
        "confidence": {"enum": ["low", "medium", "high"]},
        "next_action": {"type": "string"}
      }
    }
  }
}
```

## gate_rules

| Regla | Falla si | Resultado |
| --- | --- | --- |
| Minimo de fuentes | `sources_attempted < 5` y `candidates == 0` | `blocked` |
| Fuente bloqueada sin rescate | `outcome=blocked/error` sin `next_route_if_failed` ni fallback | `blocked` |
| Frases vacias | Contiene "no pude", "no encontre nada", "no hay oportunidades" sin rutas alternativas | `blocked` |
| Candidato sin precio | Candidato fuerte sin precio ni ruta concreta para precio/comparable | `needs_review` |
| Instrumental sin trazabilidad | Item medico sin marca/modelo/reputacion/regulatorio | `needs_review` o `blocked` |
| Inmueble sin ubicacion | Sin zona verificable o comparable por radio/m2 | `blocked` |
| Score alto | `score >= 75` y secciones completas | `completed` permitido |
| Score medio | `50 <= score < 75` | `needs_review` |
| Score bajo | `score < 50` | `blocked` |

## fallback_routes

```yaml
inmobiliaria:
  direct_page_blocked:
    - busqueda por direccion o zona exacta
    - portal espejo
    - snippets/cache
    - comparables por radio y m2
    - fuente publica alternativa
  no_price:
    - mismo inmueble en otro portal
    - comparables del barrio
    - marcar precio_pendiente con ruta concreta
instrumental:
  marketplace_blocked:
    - marca/modelo en eBay
    - Mercado Libre
    - importadores/fabricante
    - ficha/manual/fotos/specs
  regulatory_unknown:
    - marcar needs_review
    - no recomendar compra/contacto
```

## script_plan

Archivo sugerido:

```text
scripts/qa/validate_radar_report.py
```

CLI:

```bash
python3 scripts/qa/validate_radar_report.py \
  --kind inmobiliaria \
  --min-sources 5 \
  --min-candidates 1 \
  results/<job_id>.radar.json
```

Salida:

```json
{
  "ok": false,
  "status_allowed": "blocked",
  "score": 42,
  "errors": ["missing_fallback_for_blocked_source"],
  "warnings": ["candidate_without_price_route"],
  "next_required_action": "usar fuente alternativa o delegar a Pablo"
}
```

Integracion:

1. 5.3 genera `results/<job_id>.radar.json`.
2. Validator calcula `status_allowed`.
3. Si `completed` solicitado pero `status_allowed != completed`, bloquear commit.
4. Si `needs_review`, crear job a Pablo con reporte parcial y errores.
5. Si `blocked`, exigir rutas usadas, limites y proxima accion antes de archivar.

## qa_examples

Caso bloqueado:

```json
{
  "kind": "inmobiliaria",
  "run_summary": {"status": "completed", "score": 20, "reason": "no encontre nada"},
  "sources_attempted": [{"name": "portal", "outcome": "blocked", "next_route_if_failed": ""}],
  "candidates": [],
  "rejected_candidates": [],
  "conclusion": {"recommendation": "no hay oportunidades", "confidence": "low", "next_action": ""}
}
```

Esperado: `blocked`, errores `empty_report_phrase`,
`blocked_source_without_fallback`, `insufficient_sources`.

Caso valido `needs_review`:

```json
{
  "kind": "instrumental",
  "run_summary": {"status": "needs_review", "score": 64, "reason": "dos candidatos con precio parcial"},
  "sources_attempted": ["5 fuentes estructuradas"],
  "candidates": ["2 candidatos con marca/modelo y comparables parciales"],
  "rejected_candidates": ["3 descartes con motivo"],
  "conclusion": {"recommendation": "delegar ranking a Pablo", "confidence": "medium", "next_action": "validar trazabilidad"}
}
```

Esperado: aceptado solo como `needs_review`.

## risks / limits

- El schema no garantiza oportunidad real; garantiza evidencia minima.
- Un agente podria llenar candidatos malos para pasar minimo; por eso score y
  descartes deben pesar mas que cantidad.
- Instrumental medico requiere conservadurismo regulatorio; no recomendar compra
  si falta trazabilidad.

## recommendation

Implementar `validate_radar_report.py` como gate obligatorio antes de cerrar
radares. V1 debe bloquear "no pude/no encontre" sin fallback y permitir
`completed` solo con score >= 75 y secciones completas.

## confidence

Alta para schema y reglas porque consolidan resultados previos y el canon de
radares. Media para thresholds hasta calibrar con corridas reales.

## evidence_paths

- `jobs/20260527T183421-radar-anti-empty-script-spec.md`
- `context/fronts/radares.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `decisions/radar_scorecards_v1.md`

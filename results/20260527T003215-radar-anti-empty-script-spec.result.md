---
job_id: 20260527T003215-radar-anti-empty-script-spec
worker: personal-xh
status: completed
completed_at: 2026-05-27T00:37:30-03:00
front: INVERSIONES
no_external_actions: true
no_secrets: true
---

# Resultado - Radar anti empty script spec

## summary honesto

El gate anti informe vacio debe validar estructura, evidencia minima, rutas
alternativas y calidad de decision antes de permitir `completed`. No busca
encontrar oportunidades por si mismo: bloquea reportes que cierran con "no hay",
"no pude" o candidatos sin comparables verificables.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T003215-radar-anti-empty-script-spec.md` | Revisada | Entregables y restricciones. |
| `context/fronts/radares.md` | Revisada | Contrato anti informe vacio y rutas alternativas. |
| `results/20260525T120001-radares-anti-informe-vacio-v1.result.md` | Revisada | Schema, thresholds y division 5.3/Pablo. |
| `decisions/radar_scorecards_v1.md` | Revisada | Campos y scorecards de inmobiliaria/instrumental. |

## json_schema

```json
{
  "job_id": "string",
  "kind": "inmobiliaria|instrumental|general",
  "scope": {"query": "string", "market": "string", "constraints": ["string"]},
  "run_summary": {"status": "completed|needs_review|blocked|delegated_to_pablo", "score": 0, "reason": "string"},
  "sources_attempted": [{"name": "string", "url_or_query": "string", "source_type": "direct_page|marketplace|search|pdf|official|snippet|cached|local_context|comparable", "outcome": "success|blocked|no_results|partial|error", "evidence": "string", "next_route_if_failed": "string"}],
  "fallback_routes_used": [{"blocked_source": "string", "alternative": "string", "outcome": "string"}],
  "candidates": [{"id": "string", "title": "string", "source": "string", "price": "string|null", "location_or_specs": "string", "comparable_basis": "string", "opportunity_thesis": "string", "risks": ["string"], "missing_fields": ["string"], "decision": "investigar|watchlist|descartar|pedir_aprobacion", "next_action": "string"}],
  "rejected_candidates": [{"title": "string", "source": "string", "reason": "string"}],
  "conclusion": {"recommendation": "string", "confidence": "low|medium|high", "next_run_or_handoff": "string"}
}
```

## gate_rules

| Regla | Resultado |
| --- | --- |
| Menos de 5 fuentes intentadas y 0 candidatos | `blocked` |
| Fuente principal bloqueada sin alternativa | `blocked` |
| Texto contiene "no pude" sin `fallback_routes_used` | `blocked` |
| Candidato sin precio y sin ruta concreta para obtener precio | `needs_review` |
| Inmobiliaria sin ubicacion verificable | candidato `descartar` |
| Instrumental medico sin trazabilidad/regulatorio cuando aplica | `needs_review` |
| Score < 50 | `blocked` |
| Score 50-74 | `needs_review` |
| Score >= 75 y secciones completas | `completed` |

Thresholds iniciales:

```yaml
min_sources:
  inmobiliaria: 5
  instrumental: 5
  general: 4
min_rejected_candidates_if_zero_found: 3
min_fallback_routes_for_blocked_source: 2
completed_score_min: 75
needs_review_score_min: 50
```

## fallback_routes

- Web inmobiliaria no abre: busqueda por direccion/zona, marketplace espejo, cache/snippet, comparables de zona o portal alternativo.
- Marketplace sin precio: buscar mismo item/modelo, comparable local/importado y registrar ruta de obtencion.
- Producto chino ambiguo: fabricante, marketplace B2B, eBay/ML/local, distribuidor o regulatorio si es medico.
- Fuente con login: no usar credenciales; buscar fuente publica y registrar bloqueo.
- Cero candidatos: documentar queries, fuentes, descartes, criterio de agotamiento y proxima corrida.

## script_plan

1. Crear `scripts/qa/validate_radar_report.py`.
2. Entrada: `report.md` o `report.json`, `--kind`, `--min-sources` opcional.
3. Extraer secciones obligatorias por heading Markdown o JSON.
4. Validar schema con errores por campo.
5. Calcular score por completitud, fuentes, candidatos, comparables, riesgos y next action.
6. Emitir JSON de gate con `ok`, `status`, `score`, `blocking_reasons`, `warnings` y `next_action`.
7. Integrar al pipeline: si `ok=false`, no se puede commitear radar como final.
8. Si `status=needs_review`, crear job a Pablo con reporte parcial y razon.

## qa_examples

```yaml
- name: falla_por_informe_vacio
  sources_attempted: 2
  candidates: []
  fallback_routes_used: []
  text: "No pude abrir la web."
  expected_status: blocked
- name: needs_review_mercado_pobre
  sources_attempted: 6
  candidates: []
  rejected_candidates: 4
  comparables: present
  fallback_routes_used: 2
  expected_status: needs_review
- name: completed_con_candidato
  sources_attempted: 7
  candidates: 2
  price: present
  comparables: present
  risks: present
  score: 82
  expected_status: completed
```

## risks / limits

- El gate puede incentivar candidatos malos solo para pasar minimo; el score debe penalizar comparables debiles.
- Los thresholds deben calibrarse con corridas reales por mercado.
- Para instrumental medico, trazabilidad y soporte pesan mas que margen.
- El script valida calidad de reporte, no reemplaza criterio de inversion.

## recommendation

Implementar primero `validate_radar_report.py` con `blocked` por defecto si
faltan fuentes, fallback o next action. Despues calibrar scorecards por
inmobiliaria e instrumental con 5 reportes reales.

## confidence

Alta para schema, reglas y mensajes de bloqueo; media para thresholds hasta probar con reportes reales.

## evidence_paths

- `jobs/20260527T003215-radar-anti-empty-script-spec.md`
- `context/fronts/radares.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `decisions/radar_scorecards_v1.md`

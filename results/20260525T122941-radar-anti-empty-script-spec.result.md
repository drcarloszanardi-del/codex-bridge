# Resultado - radar anti empty script spec

Job: `20260525T122941-radar-anti-empty-script-spec`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

El gate anti informe vacio debe ser un script de QA que lea el reporte del radar y, opcionalmente, un JSON de candidatos. No busca oportunidades ni navega: valida que el agente haya hecho el trabajo minimo antes de cerrar como `completed`. Si el reporte no cumple, exige `needs_review` o `blocked` con causa, rutas alternativas y siguiente accion.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `jobs/20260525T122941-radar-anti-empty-script-spec.md` | 1 | Contrato del script/gate. |
| `context/fronts/radares.md` | 1 | Minimos anti informe vacio. |
| `results/20260525T120001-radares-anti-informe-vacio-v1.result.md` | 1 | Contrato, thresholds y division 5.3/Pablo. |
| `decisions/radar_scorecards_v1.md` | 1 | Scorecards de inmobiliaria/instrumental. |

## coverage_table

| Area | Estado | Evidencia |
|---|---|---|
| JSON schema | propuesto | Schema abajo. |
| Gate rules | propuesto | Estados y thresholds. |
| Fallback routes | consolidado | Basado en contexto y resultado previo. |
| Script plan | implementable | Nombre, CLI, exit codes y mensajes. |

## json_schema

Archivo opcional: `results/<job_id>.candidates.json`

```json
{
  "job_id": "string",
  "kind": "inmobiliaria|instrumental|general",
  "status_claimed": "completed|needs_review|blocked",
  "sources_attempted": [
    {
      "name": "string",
      "url_or_query": "string",
      "type": "direct_page|marketplace|search|pdf|official|snippet|cache|local_context",
      "outcome": "success|blocked|no_results|partial|error",
      "evidence": "string",
      "alternative_used": "string"
    }
  ],
  "fallback_routes_used": [
    {
      "blocked_source": "string",
      "route": "string",
      "outcome": "success|partial|failed"
    }
  ],
  "candidates": [
    {
      "id": "string",
      "title": "string",
      "source": "string",
      "price": "number|string|null",
      "location_or_specs": "string",
      "comparables": ["string"],
      "risks": ["string"],
      "decision": "investigar|watchlist|descartar|pedir_aprobacion",
      "next_action": "string"
    }
  ],
  "rejected_candidates": [
    {"title": "string", "reason": "string", "source": "string"}
  ]
}
```

## gate_rules

| Regla | Error | Status minimo |
|---|---|---|
| Faltan secciones obligatorias | `missing_sections` | `blocked` |
| Reporte contiene "no pude"/"no encontre" sin fallback | `empty_failure_phrase` | `blocked` |
| Menos de 5 fuentes en radar amplio | `insufficient_sources` | `blocked` |
| Fuente bloqueada sin alternativa | `blocked_source_without_fallback` | `blocked` |
| 0 candidatos y menos de 5 descartes/fuentes | `empty_universe` | `blocked` |
| 0 candidatos con buen universo documentado | `no_candidates_but_evidence` | `needs_review` |
| Candidato sin fuente/link/query | `candidate_missing_source` | `needs_review` |
| Candidato sin decision | `candidate_missing_decision` | `needs_review` |
| Instrumental sin riesgo regulatorio/trazabilidad | `missing_medical_risk` | `needs_review` |
| Score >= 75 | none | `completed` permitido |
| Score 50-74 | `below_completed_threshold` | `needs_review` |
| Score < 50 | `below_review_threshold` | `blocked` |

## fallback_routes

```yaml
inmobiliaria:
  blocked_direct_site:
    - search_query_by_address_zone
    - marketplace_mirror
    - snippets_or_cache
    - comparable_same_zone
    - map_or_public_listing
instrumental:
  blocked_marketplace:
    - manufacturer_or_model_search
    - local_distributor
    - ebay_or_ml_comparable
    - china_b2b_comparable
    - regulatory_traceability_check
general:
  no_price:
    - same_model_comparable
    - mark_pending_price_with_route
    - do_not_estimate_as_fact
```

## script_plan

Archivo sugerido: `scripts/qa/validate_radar_report.py`

CLI:

```bash
python3 scripts/qa/validate_radar_report.py results/<job_id>.result.md --kind inmobiliaria
python3 scripts/qa/validate_radar_report.py results/<job_id>.result.md --kind instrumental --candidates results/<job_id>.candidates.json
```

Exit codes:

- `0`: puede ser `completed`.
- `2`: debe ser `needs_review`.
- `3`: debe ser `blocked`.

Salida JSON:

```json
{
  "ok": false,
  "score": 62,
  "required_status": "needs_review",
  "errors": ["missing comparables", "candidate missing next_action"],
  "warnings": ["0 candidates but 7 sources attempted"]
}
```

## qa_examples

| Caso | Esperado |
|---|---|
| "No pude abrir MercadoLibre" sin fuentes alternativas | FAIL, `blocked`. |
| 0 candidatos, 8 fuentes, 10 descartes y proxima corrida | PASS parcial, `needs_review`. |
| 5 casas con precio, zona, comparables, descartes | PASS, `completed`. |
| Instrumental con implante sin ANMAT/trazabilidad y decision comprar | FAIL, `needs_review` o `blocked`. |
| Candidato sin `next_action` | FAIL, `needs_review`. |
| Fuente bloqueada + snippets + comparable + decision | Puede pasar si score >= 75. |

## risks / limits

- El script valida calidad del reporte, no verdad del mercado.
- Thresholds pueden requerir tuning por fuente/epoca.
- Si se obliga cantidad minima, el agente podria inflar candidatos; por eso comparables y descartes pesan.
- Para instrumental medico, el gate debe ser conservador: seguridad > oportunidad.

## recommendation

Implementar `validate_radar_report.py` como requisito antes de commitear todo radar. Si falla, el resultado no debe llamarse `completed`; debe quedar `needs_review` o `blocked` con errores del gate y proxima accion.

## confidence

Alta para schema y reglas. Media para puntajes exactos hasta calibrar con 5-10 corridas reales.

## evidence_paths

- `jobs/20260525T122941-radar-anti-empty-script-spec.md`
- `context/fronts/radares.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `decisions/radar_scorecards_v1.md`


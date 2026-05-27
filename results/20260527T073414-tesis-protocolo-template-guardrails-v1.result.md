---
job_id: 20260527T073414-tesis-protocolo-template-guardrails-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T07:36:00-03:00
front: TESIS
no_external_actions: true
no_secrets: true
---

# Resultado - Tesis protocolo template guardrails v1

## summary

Checklist/guardrails propuestos para plantillas de protocolo y recoleccion de
datos de TESIS, con foco en preservar metodologia y evitar cambios no
autorizados sobre el borrador base. La regla central es simple: **plantilla y
protocolo primero; borrador base despues y solo con decision log**.

Evidencia: `decisions/tesis_research_ops_protocol_v1.md` exige matriz
bibliografica, variables, protocolo de recoleccion y decision log antes de
reescrituras. `results/20260527T011700-tesis-protocolo-datos-y-material-audiovisual.result.md`
refuerza que los datos y material audiovisual deben clasificarse por fuente y
validez antes de tocar el texto. Inferencia: el guardrail debe funcionar como QA
de estructura y trazabilidad, no como generador de bibliografia ni cambios de
fondo.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T073414-tesis-protocolo-template-guardrails-v1.md` | Revisada | Workorder, limites y entregables. |
| `results/20260527T011700-tesis-protocolo-datos-y-material-audiovisual.result.md` | Revisada | Protocolo de variables, datos y audiovisual. |
| `results/20260525T021049-tesis-research-ops-protocol-v1.result.md` | Revisada | Regla de matriz/variables antes de reescrituras. |
| `decisions/tesis_research_ops_protocol_v1.md` | Revisada | Artefactos canonicos y no hacer. |
| `context/frentes_activos_resumen_20260525.md` | Revisada por busqueda local | Frente TESIS: mejorar metodologia sin cambiar fondo salvo evidencia fuerte. |
| `context/fronts/tesis.md` | No presente en repo | Limite documentado; se uso el resumen de frentes y resultados previos. |

## findings

| Severidad | Riesgo | Evidencia | Guardrail |
| --- | --- | --- | --- |
| P0 | Modificar el borrador base sin protocolo, variables y decision log. | `decisions/tesis_research_ops_protocol_v1.md` dice "No reescribir fondo sin decision" y "No cambiar definiciones a mitad de carga sin decision log". | Cualquier cambio al borrador requiere `change_request_id`, evidencia, alcance y aprobacion del orquestador. |
| P0 | Inventar bibliografia, datos o outcomes para completar la plantilla. | El protocolo dice "No inventar bibliografia"; el resultado 20260527T011700 exige fuente exacta y estado de validez. | Toda cita/dato debe tener `source_id`, estado y campo `pending_if_missing`. |
| P0 | Usar datos reales, audiovisuales o material sensible como insumo no autorizado. | El resultado 20260527T011700 limita audiovisuales a contexto/auditoria y exige anonimizado/permiso. | Plantillas solo aceptan IDs anonimos y `source_type` clasificado; sin datos reales en bridge. |
| P1 | Cambiar definiciones de variables durante la carga. | `decisions/tesis_research_ops_protocol_v1.md` exige decision log para cambios. | Bloquear merge de `variables.md` si falta version, criterio de faltante o decision log para cambios. |
| P1 | Mezclar datos primarios, derivados e inferidos desde video. | El resultado 20260527T011700 pide separar datos primarios, derivados y observaciones audiovisuales. | Campo obligatorio `source_type` y `validity_status`. |
| P1 | Convertir material audiovisual en evidencia primaria sin protocolo. | El resultado previo lo permite solo como `contextual`, `audit_support` o `candidate_variable`. | Toda observacion audiovisual debe quedar marcada como inferencia hasta validacion documental. |

## no_touch_base_checklist

Antes de tocar el borrador base, el orquestador debe verificar:

1. Existe `tesis/variables.md` con definicion operacional, unidad, fuente,
   momento, valores permitidos, faltantes y criterio de exclusion.
2. Existe `tesis/data_collection_protocol.md` con pasos de carga, doble revision
   y reglas para datos faltantes.
3. Existe `tesis/decision_log.md` y cada cambio metodologico tiene entrada.
4. Existe `tesis/bibliography_matrix.csv` o equivalente con decision
   `usar|revisar|descartar`.
5. Cada dato nuevo tiene `source_id`, `source_type`, `validity_status` y ruta o
   referencia local controlada.
6. Todo material audiovisual esta clasificado como `contextual`,
   `audit_support` o `candidate_variable`, nunca como outcome primario sin
   validacion.
7. No hay nombres, DNI, HC, fechas identificables, rostros, voces o metadata
   sensible en artefactos del bridge.
8. La modificacion propuesta declara si cambia hipotesis, metodologia,
   inclusion/exclusion, variable, resultado o solo estilo.
9. Si cambia algo de fondo, hay `change_request_id` y recomendacion explicita
   del orquestador.
10. Si falta evidencia, la plantilla debe decir `pending`, no completar con
    texto plausible.

## minimal_evidence_fields

Campos obligatorios para cualquier plantilla de protocolo o recoleccion:

```json
{
  "artifact_id": "tesis_protocol_template_v1",
  "case_or_record_id": "ANON-001",
  "variable_id": "technical_step_present",
  "definition_version": "v1",
  "operational_definition": "Presencia observable de paso tecnico predefinido.",
  "unit_or_scale": "boolean|category|number|string",
  "source_type": "historia|parte_quirurgico|imagen|video|nota_experta|bibliografia",
  "source_id": "SRC-001",
  "source_path_or_reference": "local_or_citation_id",
  "validity_status": "primary|derived|inferred|contextual|pending_review",
  "missing_policy": "unknown|not_applicable|not_recorded|excluded",
  "review_status": "draft|needs_review|approved",
  "reviewer": "orchestrator|doctor|pending",
  "decision_log_id": "DL-YYYYMMDD-001",
  "notes": "sin datos identificables"
}
```

## template_guardrail_contract

Salida JSON sugerida para un validator local:

```json
{
  "ok": false,
  "mode": "template_only_guardrail",
  "artifact": "tesis/data_collection_protocol.md",
  "summary": {
    "p0": 1,
    "p1": 2,
    "warnings": 0
  },
  "findings": [
    {
      "gate_id": "tesis_no_touch_base_without_decision_log",
      "severity": "P0",
      "status": "fail",
      "evidence_path": "tesis/draft_base.md",
      "matched_text": "modified_without_decision_log",
      "message": "El borrador base cambio sin entrada de decision log."
    }
  ]
}
```

Gates recomendados:

| Gate | Severidad | Condicion de fail/report |
| --- | --- | --- |
| `tesis_no_touch_base_without_decision_log` | P0 | Cambios en borrador base sin `decision_log_id`. |
| `tesis_no_inventar_bibliografia` | P0 | Referencia sin `source_id`/matriz o con estado `pending` usada como validada. |
| `tesis_no_real_data_in_bridge` | P0 | Identificadores reales o metadata sensible en artefactos del bridge. |
| `tesis_variable_definition_complete` | P1 | Variable sin definicion, unidad, fuente, faltantes o version. |
| `tesis_source_type_required` | P1 | Dato sin clasificar como primario, derivado, inferido o contextual. |
| `tesis_audiovisual_not_primary_without_validation` | P1 | Video usado como outcome primario sin validacion documental. |

## qa_commands

Comandos de localizacion sugeridos, sin abrir Drive/iCloud/Gmail/Photos:

```bash
rg -n "tesis|variables|data_collection|decision_log|bibliography_matrix|draft_base|template_only" .
rg -n "source_type|validity_status|decision_log_id|operational_definition|missing_policy" .
rg -n "DNI|HC|historia clinica|nombre|telefono|fecha de nacimiento|metadata" tesis results decisions context
```

Si el orquestador agrega validator:

```bash
node -c scripts/qa/validate_tesis_protocol_templates.js
node scripts/qa/validate_tesis_protocol_templates.js --root tesis
python3 scripts/validate_result_contract.py results/20260527T073414-tesis-protocolo-template-guardrails-v1.result.md
git diff --check
python3 scripts/secret_scan.py
```

## attempted_routes

- Se hizo `git pull --rebase`.
- Se inspeccionaron jobs asignados con `./scripts/personal_xh_check.sh`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso `jobs/20260527T073414-tesis-protocolo-template-guardrails-v1.md`.
- Se busco `context/fronts/tesis.md`; no esta presente en `context/fronts/`.
- Se revisaron los resultados y decision file de TESIS disponibles localmente.
- Se hizo busqueda local con `rg` para reglas replicadas y contexto relevante.
- No se abrio Drive, iCloud, Gmail, Photos, Downloads ni material externo.
- No se modifico el borrador base ni se usaron datos reales.

## risks_limits

- Este resultado entrega guardrails y contrato QA, no edita plantillas reales.
- Las rutas exactas del futuro validator dependen de donde el orquestador integre
  los artefactos de TESIS.
- Sin borrador base ni datos reales, no se valida contenido final; se valida el
  proceso que evita cambios no autorizados.
- No se agregan citas ni bibliografia; cualquier referencia futura debe venir de
  matriz curada.

## recommendation

Proxima accion unica: crear un workorder de implementacion para
`scripts/qa/validate_tesis_protocol_templates.js` y fixtures sinteticos bajo
`tesis/` o `data/derived/tesis_test_cases/`, conectando los seis gates anteriores
en modo `template_only_guardrail`. No tocar el borrador base hasta que el
validator pase y exista decision log.

## confidence

Media-alta para los guardrails P0/P1 porque derivan de resultados TESIS previos
y del protocolo local. Media para rutas/comandos finales porque no hay
`context/fronts/tesis.md` ni estructura canonica de TESIS visible en este bridge.

## evidence_paths

- `jobs/20260527T073414-tesis-protocolo-template-guardrails-v1.md`
- `results/20260527T011700-tesis-protocolo-datos-y-material-audiovisual.result.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
- `decisions/tesis_research_ops_protocol_v1.md`
- `context/frentes_activos_resumen_20260525.md`
- `claims/20260527T073414-tesis-protocolo-template-guardrails-v1.json`

---
id: 20260525T224750-clinica-v2-gates-next-hardening-audit-v1
created_at: 2026-05-25T22:47:50-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: segunda pasada de endurecimiento gates clinica v2

## Contexto

El orquestador valido en la app real:

- `node scripts/qa/validate_lumbar_inconsistency_gates_v2.js`: OK.
- `node scripts/qa/run_clinica_core_qa.js`: OK, reporte `qa/approval_gates/clinica_core_qa_20260526T014738.md`.

El resultado previo de Pablo `20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.result.md` coincide en gran parte con el pack local `lumbar_inconsistency_gates_v2`, que ya tiene 16 casos detect-only.

## Objetivo

Hacer una segunda pasada XH sobre riesgos residuales del pack v2 antes de promover nada a hard fail. El orquestador necesita saber que gaps quedan y que tests de control bueno/malo faltan.

No tocar app real, no tocar plantillas, no abrir datos de pacientes, no usar Drive/iCloud/Photos, no acciones externas.

## Fuentes permitidas

- `results/20260525T221902-clinica-lumbar-regression-pack-from-prior-results-v1.result.md`
- `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md`
- `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md`
- `context/fronts/clinica.md` si existe
- `protocol.md`

## Entregable esperado

Crear `results/20260525T224750-clinica-v2-gates-next-hardening-audit-v1.result.md` con:

- `summary`
- `already_covered`
- `residual_false_negative_risks`
- `residual_false_positive_risks`
- `good_control_texts_needed`
- `bad_control_texts_needed`
- `promotion_readiness` por gate: `hard_fail_ready`, `report_only`, `needs_more_evidence`
- `next_orchestrator_actions`
- `evidence_paths`

## Reglas

- No escribir documentos clinicos finales.
- No promover consentimiento especifico ni duplicados/materiales a hard fail si hay riesgo de falso positivo sin evidencia.
- Priorizar gates critical con bajo falso positivo: extraforaminal, raiz L4, sin descompresion directa, hemostasia/recuento antes del cierre.
- Mantener salida accionable y corta.

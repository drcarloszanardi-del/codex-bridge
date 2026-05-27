---
id: 20260527T113720-clinica-diagnostico-separado-implementation-review-v1
created_at: 2026-05-27T11:37:20-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Clinica diagnostico separado implementation review v1

## Objetivo

Hacer una revision de alto razonamiento sobre la integracion local detect-only/report-only del gate documental `diagnostico_separado_de_indicacion`.

## Contexto minimo

El orquestador integro localmente, en la app canonica, una primera version del gate dentro de:

- `scripts/qa/validate_clinical_p0_gates_v1.js`
- `data/derived/clinical_test_cases/clinical_p0_gates_v1.json`

Fixtures agregados:

- `CLIN-DOC-DX-005-indication-in-diagnosis`
- `CLIN-DOC-DX-006-requires-surgery-in-diagnosis`
- `CLIN-DOC-DX-007-separated-pass`
- `CLIN-DOC-DX-008-negated-pass`
- `CLIN-DOC-DX-009-history-marker-pass`
- `CLIN-DOC-DX-010-ambiguous-requires-review`

Validaciones locales del orquestador:

```bash
node --check scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/run_clinica_core_qa.js
```

Resultado local declarado por el orquestador: `validate_clinical_p0_gates_v1` OK y `run_clinica_core_qa` OK, con warning esperado `core_only`.

## Entregable esperado

Crear `results/20260527T113720-clinica-diagnostico-separado-implementation-review-v1.result.md` con:

- `summary`
- riesgos P0/P1 de falso positivo o falso negativo
- fixtures adicionales imprescindibles, si los hay
- si conviene aceptar en observacion, ajustar o revertir
- proximo P0 documental recomendado, solo si este queda aceptable
- `confidence`
- `evidence_paths`

## Reglas

- No tocar app real ni plantillas finales desde el bridge.
- No abrir Drive/iCloud/Photos/Gmail ni datos de pacientes.
- No publicar ni enviar Telegram.
- No inventar estado local; si falta evidencia, marcar limite.
- No tocar ObraCash.

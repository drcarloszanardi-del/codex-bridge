---
id: 20260526T124354-clinica-p0-sin-descompresion-detect-only-plan-v1
created_at: 2026-05-26T12:43:54-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: high
status: queued
priority: high
no_external_actions: true
no_secrets: true
---

# Workorder: segundo P0 clinico - sin descompresion directa detect-only

## Contexto

El primer P0 `no_inventar_diagnostico_topografia` ya quedo integrado localmente en detect-only y core QA. Despues de tu revision `20260526T121531`, el orquestador agrego fixtures de negacion/afirmacion:

- `CLIN-P0-009-negated-topography-mention`
- `CLIN-P0-010-affirmation-after-missing-source`
- `CLIN-P0-011-declared-topography-pass`
- `CLIN-P0-012-differential-discard-pass`

Tambien se ajusto el validator para que la negacion no cruce limite de oracion y para que el failure incluya contexto local.

Pruebas locales pasadas:

- `node scripts/qa/validate_clinical_p0_gates_v1.js` OK.
- `node -c scripts/qa/validate_clinical_p0_gates_v1.js` OK.
- `node scripts/qa/run_clinica_core_qa.js` OK, reporte `qa/approval_gates/clinica_core_qa_20260526T154337.md`.

## Objetivo

Preparar el plan minimo, verificable y seguro para sumar el segundo P0:

`sin_descompresion_directa_bloqueante`

El Doctor fue explicito: si el caso fue sin descompresion directa, el parte no puede describir laminectomia, hemilaminectomia, flavectomia, reseccion de ligamento amarillo, foraminotomia directa, liberacion radicular directa, liberacion de recesos laterales o recalibraje como acto realizado.

## Fuentes permitidas

- `results/20260526T111217-clinica-p0-gates-local-integration-review-v1.result.md`
- `results/20260526T121531-clinica-p0-gates-implementation-review-v1.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md`
- `protocol.md`
- Este workorder.

No abrir Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas.

## Entregable esperado

Crear:

- `results/20260526T124354-clinica-p0-sin-descompresion-detect-only-plan-v1.result.md`
- `results/20260526T124354-clinica-p0-sin-descompresion-detect-only-plan-v1.manifest.json`

Debe incluir:

1. Fixtures sinteticos minimos para el segundo P0, sin pacientes reales.
2. Lista de terminos/procedimientos que deben fallar solo si estan afirmados.
3. Controles negativos de negacion: `no se realizo laminectomia/flavectomia`, `sin descompresion directa`, etc.
4. Criterio para diferenciar descripcion historica/plan discutido versus acto realizado.
5. Recomendacion exacta: integrar como `fail`, `needs_review` o `report_only` inicial.
6. Riesgos de sobrebloqueo y como mitigarlos.

## Reglas

- No acciones externas.
- No secretos.
- No datos reales de pacientes.
- No tocar ObraCash.
- No redactar documentos clinicos libres.
- No tocar plantillas finales.
- Mantener enfoque detect-only/review-only y patch minimo.

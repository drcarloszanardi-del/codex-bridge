---
id: 20260527T153504-clinica-consentimiento-especifico-source-pack-plan-v1
created_at: 2026-05-27T15:35:04-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Clinica consentimiento especifico source pack plan v1

## Objetivo

Preparar el siguiente P0 documental en fase **plan/source-pack**, sin tocar
plantillas finales ni app real:

`consentimiento_especifico_no_generico`

## Contexto operativo

Gates P0 documentales ya integrados localmente en detect-only/report-only:

- `diagnostico_separado_de_indicacion`
- `datos_sensibles_minimizados`
- `historia_clinica_minima_completa`
- `consistencia_diagnostico_indicacion_procedimiento`

El orquestador acepto la revision de Pablo sobre consistencia y agrego fixtures
de estabilidad de bajo riesgo:

- `CLIN-DOC-CONSIST-015`: normalizacion L4/5 vs L4-L5
- `CLIN-DOC-CONSIST-016`: plan pendiente con alternativa posible
- `CLIN-DOC-CONSIST-017`: procedimiento combinado justificado
- `CLIN-DOC-CONSIST-018`: public_summary fuera de alcance
- `CLIN-DOC-CONSIST-020`: faltantes nucleares no duplican ruido

QA local posterior:

- `validate_clinical_p0_gates_v1`: ok true, failures []
- `run_clinica_core_qa`: ok true, failures [], warning esperado `core_only`

Se dejo fuera por ahora `CLIN-DOC-CONSIST-019` cross-documental porque requiere
diseño de bundle/case scope y no es un parche de bajo riesgo.

## Entregable esperado

Crear `results/20260527T153504-clinica-consentimiento-especifico-source-pack-plan-v1.result.md` con:

- `summary`
- alcance exacto detect-only/report-only para consentimiento especifico
- fuente interna/source-pack minimo que deberia existir antes de implementar
- checks v1 recomendados sin inventar riesgos ni wording legal
- fixtures sinteticos positivos/negativos minimos
- falsos positivos medico-legales esperables
- reglas para no tocar plantillas finales ni convertir en hard block
- decision: implementar ahora, esperar source-pack humano o pedir material
- `confidence`
- `evidence_paths`

## Reglas

- No tocar app real ni plantillas finales desde el bridge.
- No abrir Drive/iCloud/Photos/Gmail ni datos de pacientes.
- No publicar ni enviar Telegram.
- Usar solo fixtures sinteticos y razonamiento documental.
- No inventar riesgos quirurgicos, alternativas ni texto legal.
- No tocar ObraCash.

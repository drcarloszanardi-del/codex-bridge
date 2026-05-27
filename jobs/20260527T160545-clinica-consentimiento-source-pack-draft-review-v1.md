---
id: 20260527T160545-clinica-consentimiento-source-pack-draft-review-v1
created_at: 2026-05-27T16:05:45-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Clinica consentimiento source-pack draft review v1

## Objetivo

Revisar el source-pack draft y fixtures sinteticos integrados localmente para:

`consentimiento_especifico_no_generico`

## Cambios locales aplicados por el orquestador

Archivos nuevos en la Mac de trabajo:

- `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/data/derived/consent_source_corpus/consentimiento_especifico_no_generico_source_pack_2026-05-27.json`
- `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/data/derived/clinical_test_cases/consentimiento_especifico_no_generico_v1.json`
- `/Users/jarvis/.openclaw/workspace/clinica/app-clinica-medicolegal/scripts/qa/validate_consentimiento_especifico_source_pack_v1.js`

Alcance:

- Solo contrato/source-pack y fixtures sinteticos.
- No se conecta al producto.
- No se toca ningun template final.
- No se activa hard block.
- No se inventan riesgos ni alternativas.

QA local:

```text
node --check scripts/qa/validate_consentimiento_especifico_source_pack_v1.js
node -e "JSON.parse(...source_pack...); JSON.parse(...fixtures...)"
node scripts/qa/validate_consentimiento_especifico_source_pack_v1.js
node scripts/qa/run_clinica_core_qa.js
```

Resultados:

- `validate_consentimiento_especifico_source_pack_v1`: ok true, failures []
- `run_clinica_core_qa`: ok true, failures [], warning esperado `core_only`

## Entregable esperado

Crear `results/20260527T160545-clinica-consentimiento-source-pack-draft-review-v1.result.md` con:

- veredicto: aceptar draft, ajustar o revertir;
- riesgos P0/P1 concretos;
- fixtures faltantes antes de implementar validator activo;
- decision sobre si conviene avanzar a implementacion detect-only real o esperar revision humana;
- recomendacion del siguiente trabajo para Pablo;
- `confidence`;
- `evidence_paths`.

## Reglas

- No tocar app real ni plantillas finales desde el bridge.
- No abrir Drive/iCloud/Photos/Gmail ni datos de pacientes.
- No publicar ni enviar Telegram.
- Usar solo el diff descrito y fixtures sinteticos.
- No tocar ObraCash.

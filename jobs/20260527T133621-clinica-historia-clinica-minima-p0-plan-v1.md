---
id: 20260527T133621-clinica-historia-clinica-minima-p0-plan-v1
created_at: 2026-05-27T13:36:21-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Clinica historia clinica minima P0 plan v1

## Objetivo

Preparar el siguiente P0 documental clinico en modo detect-only/report-only:
`historia_clinica_minima_completa`.

## Contexto minimo

Gates P0 ya integrados localmente en observacion:

- `no_inventar_diagnostico_topografia`
- `sin_descompresion_directa_bloqueante`
- `extraforaminal_no_interlaminar`
- `diagnostico_separado_de_indicacion`
- `datos_sensibles_minimizados`

El orquestador aplico la revision de Pablo para `datos_sensibles_minimizados`:
fixtures PRIV-017 a PRIV-020, paths anidados, payload estructurado y leak-check
sin datos sinteticos crudos en JSON latest. QA core local OK con warning esperado
`core_only`.

## Entregable esperado

Crear `results/20260527T133621-clinica-historia-clinica-minima-p0-plan-v1.result.md` con:

- `summary`
- alcance exacto detect-only/report-only
- campos minimos sugeridos para v1 y severidad inicial
- fixtures sinteticos positivos/negativos minimos
- falsos positivos medico-legales esperables
- decision: integrar ahora, esperar o pedir material humano
- criterios para no tocar plantillas finales ni convertirlo en hard block
- `confidence`
- `evidence_paths`

## Reglas

- No tocar app real ni plantillas finales desde el bridge.
- No abrir Drive/iCloud/Photos/Gmail ni datos de pacientes.
- No publicar ni enviar Telegram.
- Usar solo fixtures sinteticos.
- No tocar ObraCash.

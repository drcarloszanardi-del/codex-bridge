---
id: 20260527T143446-clinica-consistencia-diagnostico-indicacion-procedimiento-plan-v1
created_at: 2026-05-27T14:34:46-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Clinica consistencia diagnostico indicacion procedimiento plan v1

## Objetivo

Preparar el siguiente P0 documental clinico en modo detect-only/report-only:
`consistencia_diagnostico_indicacion_procedimiento`.

## Contexto minimo

Gates P0 ya integrados localmente en observacion:

- `no_inventar_diagnostico_topografia`
- `sin_descompresion_directa_bloqueante`
- `extraforaminal_no_interlaminar`
- `diagnostico_separado_de_indicacion`
- `datos_sensibles_minimizados`
- `historia_clinica_minima_completa`

El orquestador aplico la revision de Pablo para `historia_clinica_minima_completa`:
fixtures HC-015 a HC-018, control de evolucion parcial/out-of-scope, agrupacion
de multiples faltantes, imagenes sin examen fisico y plan pendiente. QA local OK.

## Entregable esperado

Crear `results/20260527T143446-clinica-consistencia-diagnostico-indicacion-procedimiento-plan-v1.result.md` con:

- `summary`
- alcance exacto detect-only/report-only
- checks v1 recomendados: nivel, lateralidad, familia procedimiento-indicacion, procedimiento con plan pendiente
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

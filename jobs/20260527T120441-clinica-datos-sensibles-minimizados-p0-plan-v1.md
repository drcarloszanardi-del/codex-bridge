---
id: 20260527T120441-clinica-datos-sensibles-minimizados-p0-plan-v1
created_at: 2026-05-27T12:04:41-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Clinica datos sensibles minimizados P0 plan v1

## Objetivo

Preparar el siguiente P0 documental clinico en modo detect-only/report-only: `datos_sensibles_minimizados` para exports, handoffs, resumenes publicos y textos para envio.

## Contexto minimo

El gate `diagnostico_separado_de_indicacion` quedo aceptado en observacion despues de agregar fixtures DX-011 y DX-012 localmente. QA local declarado por el orquestador:

```bash
node --check scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/validate_clinical_p0_gates_v1.js
node scripts/qa/run_clinica_core_qa.js
```

Resultado: OK, con warning esperado `core_only`.

P0 ya integrados localmente en detect-only/report-only:

- `no_inventar_diagnostico_topografia`
- `sin_descompresion_directa_bloqueante`
- `extraforaminal_no_interlaminar`
- `diagnostico_separado_de_indicacion`

## Entregable esperado

Crear `results/20260527T120441-clinica-datos-sensibles-minimizados-p0-plan-v1.result.md` con:

- `summary`
- alcance exacto report-only/detect-only
- lista de patrones P0 permitidos para v1, con redaccion segura sin imprimir datos sensibles completos
- fixtures sinteticos positivos/negativos minimos
- reglas para redaccion de `matched_text` redacted, `evidence_path`, `recommendation`
- riesgos P0/P1 de falso positivo y de fuga de datos
- decision: integrar ahora, esperar o pedir material humano
- `confidence`
- `evidence_paths`

## Reglas

- No tocar app real ni plantillas finales desde el bridge.
- No abrir Drive/iCloud/Photos/Gmail ni datos de pacientes.
- No publicar ni enviar Telegram.
- No imprimir ni inventar datos sensibles reales.
- Usar datos sinteticos solamente.
- No tocar ObraCash.

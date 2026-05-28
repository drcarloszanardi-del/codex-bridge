---
id: 20260528T130756-clinica-corpus-gates-backlog-v2
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-28T13:07:56-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: Clinica corpus medico-legal: backlog de gates aplicables

## 10 inicial - direccion del orquestador

- Objetivo: Tomar resultados clinicos/corpus previos y priorizar reglas verificables que deban convertirse en gates de historia clinica, consentimiento y parte quirurgico, separando oficial, doctrina e inferencia.
- Frente: CLINICA
- Contexto minimo:
  - `context/fronts/clinica.md`
  - `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md`
  - `results/20260525T122941-clinica-correcciones-a-fixtures-implementacion.result.md`
- Herramientas permitidas: leer archivos locales del bridge, analizar, sintetizar y proponer implementacion.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.
- Criterio de terminado: resultado accionable, con evidencia, riesgo, decision sugerida y siguiente paso implementable por Codex principal.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

  - `gate_backlog`
  - `official_source_requirements`
  - `template_impact`
  - `qa_priority`
  - `do_not_integrate_yet`

Tambien debe separar evidencia, inferencia y opinion; y no cerrar con bloqueo sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
  - `gate_backlog`
  - `official_source_requirements`
  - `template_impact`
  - `qa_priority`
  - `do_not_integrate_yet`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.

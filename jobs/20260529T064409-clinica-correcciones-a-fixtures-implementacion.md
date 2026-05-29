---
id: 20260529T064409-clinica-correcciones-a-fixtures-implementacion
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-29T06:44:09-03:00
front: CLINICA
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: Implementacion plan clinico: correcciones del Doctor a fixtures

## 10 inicial - direccion del orquestador

- Objetivo: Tomar los resultados clinicos previos de Pablo y proponer la secuencia exacta de integracion en la app real, con archivos candidatos, tests, riesgos y orden de bajo impacto.
- Frente: CLINICA
- Contexto minimo:
  - `context/fronts/clinica.md`
  - `results/20260525T120000-clinica-fixtures-lumbares-v1.result.md`
  - `results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md`
- Herramientas permitidas: leer archivos locales del bridge, analizar, sintetizar y proponer implementacion.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.
- Criterio de terminado: resultado accionable, con evidencia, riesgo, decision sugerida y siguiente paso implementable por Codex principal.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

  - `integration_plan`
  - `files_to_inspect`
  - `test_cases`
  - `risk_order`
  - `acceptance_criteria`

Tambien debe separar evidencia, inferencia y opinion; y no cerrar con bloqueo sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
  - `integration_plan`
  - `files_to_inspect`
  - `test_cases`
  - `risk_order`
  - `acceptance_criteria`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.

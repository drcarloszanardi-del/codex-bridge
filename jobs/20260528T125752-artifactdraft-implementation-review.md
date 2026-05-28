---
id: 20260528T125752-artifactdraft-implementation-review
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-28T12:57:52-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: ArtifactDraft: especificacion lista para implementar

## 10 inicial - direccion del orquestador

- Objetivo: Revisar el resultado ArtifactDraft y convertirlo en una especificacion de implementacion acotada para Codex Directo, Reels y Presentaciones.
- Frente: CODEX-OPS
- Contexto minimo:
  - `context/fronts/telegram.md`
  - `context/fronts/reels_cmp.md`
  - `context/fronts/presentaciones.md`
  - `results/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.result.md`
- Herramientas permitidas: leer archivos locales del bridge, analizar, sintetizar y proponer implementacion.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.
- Criterio de terminado: resultado accionable, con evidencia, riesgo, decision sugerida y siguiente paso implementable por Codex principal.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

  - `schema`
  - `paths`
  - `router_changes`
  - `migration_plan`
  - `tests`

Tambien debe separar evidencia, inferencia y opinion; y no cerrar con bloqueo sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
  - `schema`
  - `paths`
  - `router_changes`
  - `migration_plan`
  - `tests`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.

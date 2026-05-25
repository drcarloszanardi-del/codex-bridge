---
id: 20260525T124108-telegram-quality-scorecard
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T12:41:08-03:00
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: Telegram Directo: scorecard de calidad post-respuesta

## 10 inicial - direccion del orquestador

- Objetivo: Disenar un scorecard barato 5.3 para evaluar si una respuesta de Telegram respeto frente, contexto, evidencia, tono formal y accion concreta.
- Frente: CODEX-OPS
- Contexto minimo:
  - `context/fronts/telegram.md`
  - `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md`
  - `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md`
- Herramientas permitidas: leer archivos locales del bridge, analizar, sintetizar y proponer implementacion.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.
- Criterio de terminado: resultado accionable, con evidencia, riesgo, decision sugerida y siguiente paso implementable por Codex principal.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

  - `scorecard`
  - `thresholds`
  - `postmortem_trigger`
  - `examples`
  - `implementation_plan`

Tambien debe separar evidencia, inferencia y opinion; y no cerrar con bloqueo sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
  - `scorecard`
  - `thresholds`
  - `postmortem_trigger`
  - `examples`
  - `implementation_plan`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.

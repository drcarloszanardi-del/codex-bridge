---
id: 20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1
created_at: 2026-05-27T16:35:50-03:00
created_by: orchestrator
assignee: personal-xh
front: CODEX-OPS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Telegram direct late PDF buffer postpatch review v1

## Objetivo

Revisar el parche local aplicado por el orquestador para el hallazgo P1:
`media_arrived_after_response` en DIRECT con PDF/documento tardio.

## Contexto

Pablo entrego `results/20260527T162339-telegram-contralor-action-media-arrived-after-response.result.md`.

Diagnostico aceptado:

- DIRECT respondia a un texto antes de cerrar una ventana corta de adjuntos.
- Un PDF en `incoming-files` llego despues de la respuesta.
- El buffer cubria mejor albumes/fotos/frentes como REELS, pero no DIRECT + documento suelto tardio.

## Cambios locales aplicados

Archivos en la Mac de trabajo:

- `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py`
- `/Users/jarvis/.openclaw/workspace/tests/telegram/test_media_buffer_policy.py`

Patch conceptual:

- Texto DIRECT no-comando abre una ventana corta de adjuntos cercanos.
- DIRECT usa `settle_seconds=7` y `max_wait_seconds=22`.
- Documentos/PDF cuentan como `message_has_downloadable_media` porque ya pasan por `document_payload_from_message`.
- La deteccion de ruta explicita sigue teniendo prioridad: un texto de REELS en directo conserva `route=REELS`.
- No se envia Telegram desde tests.

QA local:

```text
python3 -m py_compile scripts/codex_telegram_direct.py tests/telegram/test_media_buffer_policy.py
python3 tests/telegram/test_media_buffer_policy.py
python3 tests/telegram/test_postfix_regression_fixtures.py
python3 tests/telegram/test_direct_reels_voice_routing.py
python3 tests/telegram/test_delivery_receipt_gate.py
python3 scripts/codex_telegram_direct.py --status
launchctl kickstart -k gui/$(id -u)/ai.openclaw.codex-telegram-direct
python3 scripts/codex_telegram_direct.py --status
```

Resultados:

- media buffer policy OK: 7 mensajes bufferizados, 4 fotos, 1 documento.
- postfix regression fixtures OK: 13 fixtures.
- direct reels voice routing OK.
- delivery receipt gate OK.
- status bot OK antes y despues del restart.

## Entregable esperado

Crear `results/20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1.result.md` con:

- veredicto: aceptar, ajustar o revertir;
- riesgos P0/P1 y falsos positivos;
- si la ventana DIRECT 7s/22s es razonable;
- fixtures faltantes antes de cerrar el incidente;
- cualquier riesgo de regresion en REELS/topic routing;
- `confidence`;
- `evidence_paths`.

## Reglas

- No abrir Telegram real ni el PDF.
- No leer secretos ni imprimir tokens.
- No enviar mensajes Telegram.
- No tocar ObraCash.
- Usar solo el diff descrito, fixtures y razonamiento de QA.

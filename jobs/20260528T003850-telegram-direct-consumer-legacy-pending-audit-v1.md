---
id: 20260528T003850-telegram-direct-consumer-legacy-pending-audit-v1
created_at: 2026-05-28T00:38:50-03:00
created_by: orchestrator
assignee: personal-xh
front: TELEGRAM
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# telegram-direct-consumer-legacy-pending-audit-v1

## Objetivo

Pablo, hacer una auditoria segura de consumidores legacy del handoff Telegram Directo -> Codex Desktop despues de aceptar en observacion el patch `last_user_turn` monotono.

Riesgo que buscamos cerrar: algun consumer o script podria seguir usando `latest_turn` / `latest_turn_id` como fuente de verdad para pending/seen, en vez de `last_user_turn`.

## Contexto local declarado por el orquestador

- Patch local aceptado en observacion:
  - `telegram_direct_handoff.json`: `latest_turn_id=5383`, `latest_turn_role=assistant`, `last_user_message_id=473`, `handoff_guardrail_status=last_user_present`.
  - Tests locales OK: `python3 /Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py` -> `{"ok": true, "tests": 8}`.
  - `py_compile` OK para `codex_telegram_direct.py` y `codex_desktop_telegram_handoff.py`.
- Resultado previo recomendado: aceptar patch en observacion y revisar consumers legacy.

## Alcance permitido

Solo auditoria declarativa y grep/lectura de codigo si las rutas existen en tu Mac:

- `/Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py`
- `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py`
- scripts bajo `/Users/jarvis/.openclaw/workspace/scripts` que lean `telegram_direct_handoff.json`, `latest_turn`, `last_user_turn`, `seen` o `pending`
- tests sinteticos de Telegram/handoff

Si esas rutas no existen en tu Mac, usar contexto declarativo y proponer una lista precisa de patrones `rg`/tests que el orquestador debe ejecutar localmente.

## Entregable esperado

1. Lista de consumers detectados o patrones a revisar.
2. Clasificacion P0/P1/P2 de usos de `latest_turn` como pending/seen.
3. Recomendacion: sin cambios, patch local minimo, o fixture adicional.
4. No tocar archivos operativos; no enviar mensajes externos.

## Reglas

- No enviar Telegram, mails ni notificaciones externas.
- No tocar secretos, credenciales, Gmail, Drive, iCloud, Photos ni adjuntos reales.
- No abrir bibliotecas completas.
- No modificar archivos operativos; entregar auditoria y recomendaciones.
- La decision final queda en Codex orquestador.

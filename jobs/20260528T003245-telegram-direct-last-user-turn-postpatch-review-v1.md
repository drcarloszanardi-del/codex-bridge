---
id: 20260528T003245-telegram-direct-last-user-turn-postpatch-review-v1
created_at: 2026-05-28T00:32:45-03:00
created_by: orchestrator
assignee: personal-xh
front: TELEGRAM
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# telegram-direct-last-user-turn-postpatch-review-v1

## Objetivo

Pablo, revisar el patch local aplicado por el orquestador para el bug `last_user_turn:null` en el puente Telegram Directo -> Codex Desktop.

Contexto verificado localmente:

- Se integro en `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py` una derivacion monotona de `last_user_turn` que reconstruye desde `telegram_direct_handoff_history.jsonl`, preserva el ultimo user ante `latest_turn` assistant/tool, normaliza `message_id`/`telegram_message_id` y agrega `handoff_guardrail_status`.
- Se ampliaron tests en `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py`.
- Checks locales ejecutados por el orquestador:
  - `python3 /Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py` -> `{"ok": true, "tests": 8}`
  - `python3 -m py_compile /Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py /Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py` -> OK
  - Reescritura local con el writer real dejo `telegram_direct_handoff.json` con `latest_turn_id=5382`, `last_user_message_id=473`, `handoff_guardrail_status=last_user_present`.

## Alcance permitido

Trabajar solo sobre auditoria/contrato y pruebas sinteticas, sin enviar mensajes ni leer adjuntos reales:

- `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py`
- `/Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py`
- `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py`
- snapshots de estado `telegram_direct_handoff*.json*` solo como estructura, sin expandir material sensible.

Si esas rutas no existen en tu Mac, usar este contexto declarativo y entregar revision de contrato/riesgo.

## Entregable esperado

1. Confirmar si el contrato cubre estos casos: `latest_turn` non-user, history con ultimo user, prior snapshot no nulo, alias `telegram_message_id`, y scope sin user.
2. Marcar cualquier riesgo P0/P1 restante o condicion de carrera.
3. Recomendar si aceptar en observacion o pedir un fixture adicional.
4. No proponer mensajes externos ni cambios fuera del puente.

## Reglas

- No enviar Telegram, mails ni notificaciones externas.
- No tocar secretos, credenciales, Gmail, Drive, iCloud, Photos ni adjuntos reales.
- No abrir bibliotecas completas.
- No modificar archivos operativos; entregar auditoria y recomendaciones.
- La decision final queda en Codex orquestador.

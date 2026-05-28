---
id: 20260528T062330-telegram-direct-visual-evidence-guard-review-v1
created_at: 2026-05-28T06:23:30-03:00
created_by: orchestrator
assignee: personal-xh
front: TELEGRAM
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# telegram-direct-visual-evidence-guard-review-v1

## Objetivo

Pablo, revisar declarativamente el guard local agregado para el ultimo riesgo residual que marcaste: claims visuales en REELS desde Telegram Directo sin evidencia declarada.

Evidencia local declarada por el orquestador:

- Se agrego en `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py`:
  - `direct_visual_claim_requires_declared_media_evidence(...)`
  - una linea `Guard visual P0` en `build_telegram_task_brief(...)`
  - accion declarada `direct_visual_claim_requires_declared_media_evidence`
  - regla: no afirmar elementos visuales del montaje sin evidencia en adjuntos/media_id/frame/OCR/transcripcion.
- Se agrego en `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py`:
  - `assert_direct_visual_claim_requires_declared_media_evidence(...)`
  - caso sintetico: `Armame un reel CMP con este material; no menciones microscopio si no esta en el montaje.`
- Checks locales:
  - `python3 /Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py` -> `{"ok": true, "tests": 12}`
  - `python3 /Users/jarvis/.openclaw/workspace/tests/telegram/test_media_buffer_policy.py` -> OK
  - `python3 /Users/jarvis/.openclaw/workspace/tests/telegram/test_postfix_regression_fixtures.py` -> `{"ok": true, "fixtures": 13}`
  - `python3 -m py_compile ...` -> OK

## Alcance permitido

Solo revision declarativa:

- No modificar archivos operativos.
- No enviar Telegram, mails ni notificaciones externas.
- No tocar Gmail, Drive, iCloud, Photos ni adjuntos reales.
- No imprimir secretos ni contenido multimedia.
- Si las rutas reales no existen en tu Mac, trabajar sobre esta evidencia declarada y resultados previos.

## Entregable esperado

1. Confirmar si el guard cierra el riesgo visual residual inmediato.
2. Marcar cualquier P0/P1/P2 restante en Telegram Directo -> Desktop.
3. Recomendar una unica proxima accion: cerrar en observacion o pedir otro fixture concreto.

## Reglas

- Mantener salida breve y operativa.
- Separar evidencia verificada de inferencias.
- La decision final queda en Codex orquestador.

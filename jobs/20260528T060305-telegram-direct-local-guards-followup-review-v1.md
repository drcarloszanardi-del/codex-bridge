---
id: 20260528T060305-telegram-direct-local-guards-followup-review-v1
created_at: 2026-05-28T06:03:05-03:00
created_by: orchestrator
assignee: personal-xh
front: TELEGRAM
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# telegram-direct-local-guards-followup-review-v1

## Objetivo

Pablo, hacer una revision declarativa de cierre sobre los guards locales agregados por el orquestador despues de tu auditoria `20260528T054245-telegram-direct-context-isolation-parity-audit-v1`.

Evidencia local declarada por el orquestador:

- Se agrego un check de paridad de contrato Directo/Desktop en `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py`.
- Se agrego un caso de no herencia de contexto: pedido directo explicito REELS con `active_route=CLINICA` previo debe quedar `route=REELS`, no `CLINICA`, en `/Users/jarvis/.openclaw/workspace/tests/telegram/test_media_buffer_policy.py`.
- Checks locales:
  - `python3 /Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py` -> `{"ok": true, "tests": 10}`
  - `python3 /Users/jarvis/.openclaw/workspace/tests/telegram/test_media_buffer_policy.py` -> OK
  - `python3 -m py_compile ...codex_telegram_direct.py ...codex_desktop_telegram_handoff.py ...test_desktop_handoff_guardrail.py ...test_media_buffer_policy.py` -> OK

## Alcance permitido

Solo revision declarativa:

- No modificar archivos operativos.
- No enviar Telegram, mails ni notificaciones externas.
- No tocar Gmail, Drive, iCloud, Photos ni adjuntos reales.
- No imprimir secretos.
- Si no tenes las rutas reales de `/Users/jarvis/.openclaw/workspace`, trabajar sobre la evidencia declarada y tus resultados previos.

## Entregable esperado

1. Confirmar si los dos guards agregados cubren los P0 inmediatos de:
   - paridad de contrato Directo/Desktop;
   - no mezcla REELS/CLINICA por `active_route`.
2. Decir si falta aun un fixture P0 antes de cerrar observacion, especialmente:
   - `clinical_edit_requires_target_document_identity`;
   - `direct_visual_claim_requires_declared_media_evidence`.
3. Recomendar una unica proxima accion:
   - cerrar en observacion;
   - agregar solo fixture clinico de `target_document_id`;
   - agregar solo fixture visual evidence;
   - pedir intervencion humana si detectas bloqueo real.

## Reglas

- Mantener salida breve, operativa y con prioridad P0/P1/P2.
- Separar evidencia verificada de inferencias.
- La decision final queda en Codex orquestador.

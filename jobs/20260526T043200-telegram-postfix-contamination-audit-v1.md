---
id: 20260526T043200-telegram-postfix-contamination-audit-v1
created_at: 2026-05-26T04:32:00-03:00
created_by: orchestrator
assignee: personal-xh
front: CODEX-OPS
model: gpt-5.5-xh
reasoning_effort: high
status: queued
priority: high
no_external_actions: true
no_secrets: true
---

# Workorder: segunda mirada post-fix sobre contaminacion de Telegram

## Contexto

El Doctor marco que el canal de Telegram estaba contaminado y que las respuestas mezclaban frentes.

El orquestador aplico estos cambios locales en la Mac de trabajo:

- `state/jarvis_topic_routes.json`: `GENERAL` quedo sin thread heredado `2610`.
- `scripts/codex_telegram_direct.py`: mensajes del chat directo con inferencia debil quedan en `DIRECT` con `reason=direct_context_hint_<frente>` en vez de contaminar el route real.
- `scripts/codex_telegram_direct.py`: adjuntos sin texto en directo solo heredan route activo si hay topic reciente con thread real.
- `scripts/codex_telegram_direct.py`: `media_group_handled` ahora queda marcado como evento de drenaje sin entrega requerida.
- `scripts/codex_telegram_channel_contralor.py`: `media_group_handled` ya no se trata como error tecnico por si solo.
- Se expiro el `active_route.json` viejo que apuntaba a `VIAJES` sin thread.

Verificaciones locales ya realizadas:

- `python3 -m py_compile scripts/codex_telegram_direct.py scripts/codex_telegram_channel_contralor.py scripts/send_codex_document.py`
- `python3 scripts/codex_telegram_channel_contralor.py --window-minutes 360 --ai-provider none --max-rows 800` -> 0 hallazgos nuevos.
- `python3 scripts/codex_telegram_healthcheck.py` -> OK, bot vivo, administrador, sin fallas recientes.
- Envio real del proxy cavernoma al topic `REELS`: `message_id=5214`.

## Objetivo

Revisar criticamente si el fix puede romper algun flujo importante o si falta algun test/regla. No tocar la Mac de trabajo. No usar Telegram real. No abrir secretos.

## Fuentes permitidas

- Este workorder.
- `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md`
- `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md`
- `results/20260525T124108-telegram-quality-scorecard.result.md`
- `context/fronts/telegram.md` si existe.
- `protocol.md`.

## Entregable esperado

Crear:

- `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md`
- `results/20260526T043200-telegram-postfix-contamination-audit-v1.manifest.json`

Debe incluir:

- `summary`
- `riesgos_del_fix`
- `casos_regresion_obligatorios`
- `criterio_direct_vs_topic`
- `adjuntos_sin_caption_policy`
- `que_debe_quedar_en_DIRECT`
- `que_debe_ir_a_topic`
- `recomendaciones_implementables`
- `acceptance_gate`

## Reglas

- No afirmar que verificaste archivos locales de la Mac de trabajo salvo evidencia permitida en este workorder.
- No pedir acceso a Drive, Fotos, Gmail, iCloud, Telegram ni Downloads.
- Si detectas riesgo real, proponer patch conceptual o fixture concreta, no teoria larga.

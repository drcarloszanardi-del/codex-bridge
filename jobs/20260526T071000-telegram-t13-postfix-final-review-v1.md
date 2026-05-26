---
id: 20260526T071000-telegram-t13-postfix-final-review-v1
created_at: 2026-05-26T07:10:00-03:00
created_by: orchestrator
assignee: personal-xh
front: CODEX-OPS
model: gpt-5.5-xh
reasoning_effort: high
status: queued
priority: normal
no_external_actions: true
no_secrets: true
---

# Workorder: revision final T13 Telegram post-fix

## Contexto

Tu review `20260526T054100-telegram-postfix-local-port-review-v1` marco un unico riesgo residual P0: texto directo ambiguo + fotos sueltas sin `media_group_id` + correccion tardia de destino.

El orquestador lo convirtio en un cierre local:

- agrego `T_POSTFIX_013_direct_captionless_media_late_route_correction.json`;
- ajusto `codex_telegram_direct.py` para:
  - reconocer frases tipo `con esto`, `con este material`, `con estas fotos`, `con las fotos` como gatillo de buffer cercano;
  - permitir que un texto posterior con ruta explicita actualice el grupo `nearby_media` abierto;
  - devolver `nearby_media_route_correction` y mantener un solo grupo;
- extendio `tests/telegram/test_postfix_regression_fixtures.py` a 13 fixtures.

Verificacion declarada por el orquestador:

- `python3 -m py_compile scripts/codex_telegram_direct.py scripts/codex_telegram_channel_contralor.py tests/telegram/test_postfix_regression_fixtures.py`
- `python3 tests/telegram/test_postfix_regression_fixtures.py` -> `{"ok": true, "fixtures": 13}`
- `python3 tests/telegram/test_direct_reels_voice_routing.py` -> OK
- `python3 tests/telegram/test_media_buffer_policy.py` -> OK
- `python3 tests/telegram/test_delivery_receipt_gate.py` -> OK
- `python3 tests/telegram/test_technical_payload_gate.py` -> OK
- listener reiniciado; healthcheck OK; contralor sin hallazgos nuevos; outbox 0.

## Objetivo

Hacer una segunda mirada final sin tocar la Mac de trabajo:

1. si el cierre T13 puede aumentar falsos positivos;
2. si el concepto de `nearby_media_route_correction` es correcto;
3. si conviene cerrar el ciclo Telegram y pasar a observacion;
4. si queda algun "no implementar" claro.

## Fuentes permitidas

- Este workorder.
- `results/20260526T054100-telegram-postfix-local-port-review-v1.result.md`
- `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md`
- `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md`
- `protocol.md`

## Entregable esperado

Crear:

- `results/20260526T071000-telegram-t13-postfix-final-review-v1.result.md`
- `results/20260526T071000-telegram-t13-postfix-final-review-v1.manifest.json`

Con secciones:

- `summary`
- `false_positive_risk`
- `route_correction_judgement`
- `close_or_continue`
- `do_not_implement`
- `recommendation`
- `confidence`
- `evidence_paths`

## Reglas

- No acciones externas.
- No secretos.
- No afirmar inspeccion directa del patch.
- Separar evidencia declarada por el orquestador de inferencia.

---
id: 20260526T054100-telegram-postfix-local-port-review-v1
created_at: 2026-05-26T05:41:00-03:00
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

# Workorder: revision XH post-port local de fixtures Telegram

## Contexto

Ya entregaste `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md`.

El orquestador porto ese paquete a la Mac de trabajo y verifico localmente:

- `python3 -m py_compile scripts/codex_telegram_direct.py scripts/codex_telegram_channel_contralor.py tests/telegram/test_postfix_regression_fixtures.py`
- `python3 tests/telegram/test_postfix_regression_fixtures.py` -> `{"ok": true, "fixtures": 12}`
- `python3 tests/telegram/test_direct_reels_voice_routing.py` -> OK
- `python3 tests/telegram/test_media_buffer_policy.py` -> OK
- `python3 tests/telegram/test_delivery_receipt_gate.py` -> OK
- `python3 tests/telegram/test_technical_payload_gate.py` -> OK
- Listener Codex Directo reiniciado con `launchctl kickstart`.
- Healthcheck final: `ok=true`, bot `Codexzanardibot`, launchd running, `recent_failure_count=0`.
- Contralor final: `ok=true`, `new_findings=[]`.
- Outbox pendiente: `0`.

Cambios locales aplicados segun el orquestador:

- `scripts/codex_telegram_direct.py`
  - agrega `route_strength` en decisiones/logs/briefs;
  - direct weak hints quedan en `DIRECT` con `route_strength=weak_hint`;
  - direct media/document-only hereda ruta solo si hay active route reciente con thread real;
  - `media_group_handled` emite `cluster_id`, `event_ids`, `message_id`, `delivery_required=false`, `drained_at`;
  - topic desconocido de grupo queda en `UNKNOWN_REVIEW`;
  - correcciones negativas tipo `no me convence`, `no sirve`, `suena mal`, `no esta bien` no disparan trabajo nuevo a REELS.
- `scripts/codex_telegram_channel_contralor.py`
  - trata `media_group_handled` como benigno solo si pasa `is_sane_media_group_drain`.
- `tests/telegram/test_postfix_regression_fixtures.py`
  - runner local con T_POSTFIX_001 a T_POSTFIX_012.
- `fixtures/telegram/postfix/`
  - 12 fixtures JSON portados.
- `fixtures/telegram/direct_voice_non_reels_clinica_negative.json`
  - acepta `DIRECT` como salida valida si el texto clinico menciona voz del paciente, siempre que no vaya a `REELS`.

## Objetivo

Hacer una segunda mirada XH sobre el resultado del port. No tocar la Mac de trabajo, no usar Telegram real y no pedir accesos.

El objetivo no es repetir el paquete anterior, sino responder:

1. Si las verificaciones declaradas alcanzan para considerar estabilizado el ruteo directo/topic en esta ronda.
2. Que riesgo residual P0 queda sin fixture.
3. Que caso unico agregaria como siguiente test si hubiera que endurecer todavia mas.
4. Si conviene dejar esta rama quieta o abrir un nuevo ciclo.

## Fuentes permitidas

- Este workorder.
- `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md`
- `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md`
- `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md`
- `results/20260525T124108-telegram-quality-scorecard.result.md`
- `protocol.md`

## Entregable esperado

Crear:

- `results/20260526T054100-telegram-postfix-local-port-review-v1.result.md`
- `results/20260526T054100-telegram-postfix-local-port-review-v1.manifest.json`

Con secciones:

- `summary`
- `stabilization_judgement`
- `covered_failure_modes`
- `remaining_p0_risk`
- `one_next_fixture_if_needed`
- `recommendation`
- `confidence`
- `evidence_paths`

## Reglas

- No acciones externas.
- No secretos.
- No afirmar que viste archivos locales de la Mac de trabajo.
- Separar claramente evidencia declarada por el orquestador de inferencia.
- No cerrar con "no pude"; si falta evidencia, indicar exactamente cual.

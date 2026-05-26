---
id: 20260525T214513-telegram-radar-regression-fixtures-v1
created_at: 2026-05-25T21:45:13-03:00
created_by: orchestrator
assignee: personal-xh
front: CODEX-OPS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: paquete de regresion Telegram + radares anti informe vacio

## Contexto

Pablo entrego `results/20260525T211520-postpatch-telegram-radar-gate-audit-v1.result.md`.

El resultado fue util y marco cuatro gates P0:

1. Voz/reel directo debe routear a `REELS` solo con ancla suficiente.
2. Texto + media tardia no debe disparar respuesta final hasta cerrar buffer.
3. Radar error-only o contrato incompleto debe quedar `sent:false`.
4. Ningun envio se informa como realizado sin `message_id` real.

El orquestador necesita convertir esto en tests/fixtures aplicables en la Mac de trabajo.

## Objetivo

Preparar un paquete de regresion implementable, con fixtures JSON y asserts concretos, para que el orquestador lo pueda portar al repo real sin reinterpretar toda la logica.

No tocar la app real ni repos fuera del bridge. No ejecutar Telegram, Gmail, Drive, Calendar, Chrome ni acciones externas.

## Fuentes permitidas

- `results/20260525T211520-postpatch-telegram-radar-gate-audit-v1.result.md`
- `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md`
- `results/20260525T164233-radares-anti-informe-vacio-operational-gate-v1.result.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `results/20260525T124108-telegram-quality-scorecard.result.md`
- `context/fronts/telegram.md` si existe
- `context/fronts/radares.md` si existe
- `protocol.md`

## Entregable esperado

Crear `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md` con:

- `summary`
- `fixture_tree`
- `fixtures_json` con contenido minimo de cada fixture en bloques JSON
- `telegram_asserts`
- `radar_asserts`
- `negative_cases`
- `commands_to_port`
- `acceptance_gate`
- `implementation_order`
- `evidence_paths`

## Fixtures obligatorios

Telegram:

- `direct_reels_voice_argentina_graves_lata_robot.json`
- `direct_voice_non_reels_clinica_negative.json`
- `reels_text_plus_four_photos_late_album.json`
- `outbox_without_message_id.json`
- `telegram_ok_with_message_id.json`
- `raw_diff_payload_blocked.json`

Radares:

- `inmobiliaria_all_technical_failures.json`
- `inversiones_queries_zero_technical_errors.json`
- `inmobiliaria_real_opportunities_junin.json`
- `radar_one_weak_candidate_missing_comparables.json`
- `radar_zero_candidates_with_documented_universe.json`
- `radar_source_blocked_without_fallback.json`

## Reglas

- No imprimir secretos ni credenciales.
- No afirmar que inspecciono el patch real de la Mac de trabajo.
- Separar inferencia de verificacion.
- No usar "no pude" como resultado final; si falta una ruta, proponer el stub portable.
- Mantenerlo accionable y corto: queremos copiar estructura, no teoria.

---
id: 20260526T050800-telegram-postfix-regression-fixtures-v1
created_at: 2026-05-26T05:08:00-03:00
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

# Workorder: fixtures post-fix para ruteo Telegram

## Contexto

Ya entregaste `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md`.

El orquestador aplico en la Mac de trabajo dos recomendaciones seguras:

- `route_strength` en decisiones de ruteo: `weak_hint`, `explicit_front`, `explicit_front_deliverable`, `recent_media_context`, `topic_mapped`, `direct_default`.
- `media_group_handled` con trazabilidad: `cluster_id`, `event_ids`, `message_id`, `delivery_required=false`, `drained_at`.

Verificacion local declarada por el orquestador:

- `python3 -m py_compile scripts/codex_telegram_direct.py scripts/codex_telegram_channel_contralor.py`
- Casos manuales:
  - `buscame vuelos a natal para julio` => `DIRECT`, `route_strength=weak_hint`.
  - `mandame el informe al topic viajes` => `VIAJES`, `route_strength=explicit_front`.
  - `preparame un reel con el material de cavernoma` => `REELS`, `route_strength=explicit_front_deliverable`.
- Contralor: `ok=true`, `new_findings=[]`.

## Objetivo

Convertir la auditoria en un paquete de fixtures portable para que el orquestador lo copie luego al repo real. No tocar la Mac de trabajo ni Telegram real.

## Fuentes permitidas

- `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md`
- `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md`
- `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md`
- `context/fronts/telegram.md` si existe
- `protocol.md`

## Entregable esperado

Crear:

- `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md`
- `results/20260526T050800-telegram-postfix-regression-fixtures-v1.manifest.json`

Debe incluir:

- `summary`
- `fixture_tree`
- `fixtures_json` para T_POSTFIX_001 a T_POSTFIX_012
- `assertions`
- `minimal_test_runner_pseudocode`
- `porting_notes_for_orchestrator`
- `acceptance_gate`
- `risk_notes`

## Reglas

- No acciones externas.
- No secretos.
- No asumir inspeccion directa del patch real.
- Mantenerlo implementable, no ensayistico.

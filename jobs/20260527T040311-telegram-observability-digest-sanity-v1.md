---
id: 20260527T040311-telegram-observability-digest-sanity-v1
created_at: 2026-05-27T04:03:11-03:00
created_by: orchestrator
assignee: personal-xh
front: CODEX-OPS
model: gpt-5.5-xh
reasoning_effort: high
status: queued
no_external_actions: true
no_secrets: true
---

# Telegram observability digest sanity v1

## 10 inicial - direccion del orquestador

Pablo esta idle y no hay jobs activos. Asignar backlog seguro de auditoria Telegram/observabilidad,
sin tocar ObraCash, sin abrir bibliotecas privadas, sin Telegram real y sin acciones externas.

Objetivo: revisar el esquema de observabilidad de Telegram/bridge y proponer un digest diario barato y
no ruidoso para que el Doctor vea estado real solo cuando haya algo accionable.

Contexto minimo:

- `context/fronts/telegram.md`
- `results/20260527T005221-telegram-quality-scorecard.result.md`
- `results/20260526T054100-telegram-postfix-local-port-review-v1.result.md`
- `results/20260526T071000-telegram-t13-postfix-final-review-v1.result.md`
- `status/orchestrator.json`
- `status/personal-xh.json`

## 80 delegado - trabajo de Pablo

Entregar:

- `digest_contract`: campos minimos del digest diario.
- `notify_policy`: cuando notificar al Doctor y cuando mantenerse quieto.
- `health_inputs`: archivos/estados locales a leer, sin secretos.
- `quality_checks`: checks de message_id/topic, ruido, jobs estancados, radares bloqueados y reels en hold.
- `failure_modes`: errores que deben generar alerta.
- `implementation_plan`: script/automation de bajo costo, sin acciones externas salvo envio autorizado por orquestador.
- `risk_limits`: privacidad, ruido, falsos positivos.
- `recommendation`: proxima accion unica.

Reglas:

- No usar Telegram real ni Gmail/Drive/Photos/iCloud.
- No imprimir secretos ni tokens.
- No enviar mensajes externos.
- No cerrar con "no pude" sin limite exacto y alternativa.

## 10 final - retorno al orquestador

El resultado debe ser aplicable como mejora local de bajo riesgo. Validar contra
`scripts/validate_result_contract.py` antes de marcarlo completado.

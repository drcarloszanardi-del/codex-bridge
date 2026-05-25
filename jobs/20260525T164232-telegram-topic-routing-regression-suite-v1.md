---
id: 20260525T164232-telegram-topic-routing-regression-suite-v1
created_at: 2026-05-25T16:42:32-03:00
created_by: orchestrator
assignee: personal-xh
front: CODEX-OPS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: TELEGRAM - suite de regresion para ruteo principal/topics

## Contexto

El Doctor detecto que algunas respuestas de Codex Directo se mezclaron entre canal directo y topic `REELS`. El orquestador corrigio una parte del router local, pero hace falta una segunda mirada profunda para convertir el incidente en una suite de regresion y reglas operativas.

## Objetivo

Proponer una suite de casos de prueba y criterios de aceptacion para que Codex Directo no vuelva a:

- mandar productos de reels al canal directo cuando el destino debe ser topic `REELS`,
- disparar jobs largos por correcciones negativas,
- mezclar contexto de youtubers/reels/inversiones,
- contestar con texto intermedio no pedido,
- perder adjuntos o tomar solo la primera imagen/video de un conjunto.

## Fuentes locales permitidas

- `protocol.md`
- `results/20260525T021030-telegram-router-patch-proposal-v1.result.md`
- `results/20260525T084316-telegram-codex-direct-router-observability-mvp-v2.result.md`
- `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T111222-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md`
- `results/20260525T124108-telegram-quality-scorecard.result.md`
- `context/fronts/telegram.md` si existe

No leer tokens, secretos ni archivos de credenciales.

## Entregable esperado

Crear `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md` con:

- `summary`
- `incident_classes`
- `regression_cases` con al menos 20 inputs sinteticos y destino esperado
- `background_job_policy`
- `media_album_policy`
- `topic_reply_policy`
- `acceptance_gates`
- `implementation_recommendation_for_orchestrator`
- `risks_limits`
- `confidence`
- `evidence_paths`

## Reglas

- No enviar Telegram ni tocar el router real.
- No imprimir secretos.
- No cerrar con "no pude"; si falta contexto, proponer caso sintetico conservador.

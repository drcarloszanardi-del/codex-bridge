# Telegram router patch proposal v1

## archivos probables en work-mac

```text
telegram_bridge/events/
telegram_bridge/jobs/
telegram_bridge/runs/
telegram_bridge/state/fronts/
telegram_bridge/state/topics/
telegram_bridge/router.py
telegram_bridge/context_compiler.py
telegram_bridge/ack_policy.py
telegram_bridge/idempotency.sqlite
```

## schema minimo

- `event`: mensaje crudo no confiable, hash de chat, topic, attachments, timestamp.
- `job`: front, topic_id, objective, priority, assignee, no_external_actions, idempotency_key.
- `run`: job_id, status, heartbeat, result_ref, blocked_reason.
- `front_context`: hechos estables por frente.
- `topic_context`: memoria local del hilo.

## algoritmo

1. Recibir Telegram como event no confiable.
2. Clasificar front/topic/intent/urgency.
3. Crear idempotency key.
4. Si ya existe, ACK silencioso sin duplicar job.
5. Crear job canonico.
6. Compilar contexto: global + front + topic + job + decisiones recientes.
7. Invocar orquestador/subagente.
8. Publicar solo cambios de estado relevantes.

## ACK

- `Recibido <job_id>. Estado: queued.`
- No repetir mientras corre.
- Reportar solo `blocked`, `needs_approval`, `done`, `failed`.

## pruebas

- Mensajes mezclados de clinica/reels/inmobiliaria.
- Mensaje repetido exacto no duplica job.
- Prompt injection en Telegram no cambia autoridad.
- Topic equivocado entra a `UNKNOWN_REVIEW`.

## riesgos

- Migrar historial crudo como contexto global contamina el sistema.
- ACK excesivo vuelve ruidoso el canal.
- Sin idempotencia, los reintentos duplican tareas.

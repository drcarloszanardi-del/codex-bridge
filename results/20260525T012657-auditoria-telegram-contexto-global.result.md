---
id: 20260525T012657-auditoria-telegram-contexto-global
job_id: 20260525T012657-auditoria-telegram-contexto-global
created_at: 2026-05-25T01:28:31-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# auditoria telegram contexto global result

## summary

Telegram debe ser solo la capa de entrada/salida breve. El contexto real tiene que vivir fuera del chat, en un estado estructurado por frentes, topics y tareas. La mejora principal es separar: contexto global estable, contexto local por topic, cola de tareas por frente y estado de ejecucion por job.

## findings

- P1: El problema central no es Telegram, sino la falta de router de contexto. Si viajes, reels, inmobiliaria y clinica entran como texto plano al mismo historial, el agente mezcla temas por diseno.
- P1: Cada mensaje entrante necesita metadatos obligatorios: `front`, `topic_id`, `task_id`, `parent_task_id`, `sender`, `created_at`, `urgency`, `requires_ack`, `external_action_allowed=false`.
- P1: El agente de Telegram no debe decidir con el historial crudo. Debe compilar contexto antes de responder: `global_context + front_context + topic_context + current_task + recent_events`.
- P2: Para tareas largas, el usuario necesita acuse sin ruido: un ACK unico con `task_id`, frente detectado y estado `queued/running`. Luego reportes solo por cambio real: `blocked`, `needs_approval`, `done`, `failed`.
- P2: Para prevenir mezcla de temas, ningun mensaje deberia actualizar contexto global automaticamente. Primero va a inbox; luego un summarizer promueve solo hechos estables y decisiones.
- P2: Los topics de Telegram pueden mapearse a `topic_id`, pero no conviene confiar solo en ellos: debe existir una capa propia de routing por frente y tarea.

## architecture recommended

- `state/global.md`: reglas estables, preferencias del Dr. Zanardi, limites de autoridad.
- `state/fronts/<front>/context.md`: memoria viva por frente.
- `state/topics/<topic_id>.md`: contexto local del hilo/topic.
- `queue/jobs/<task_id>.json`: cola canonica de tareas.
- `queue/events/<event_id>.json`: eventos crudos de Telegram, no confiables.
- `runs/<task_id>.json`: estado de ejecucion, heartbeats, bloqueos y resultado final.
- `decisions/<date>-<slug>.md`: decisiones aprobadas por el orquestador.

## concrete changes for orchestrator

- Implementar un `context_router` que clasifique cada entrada antes de invocar Codex.
- Implementar un `context_compiler` que arme prompts desde estado estructurado, no desde todo Telegram.
- Agregar estados de job: `received`, `queued`, `running`, `blocked`, `needs_approval`, `done`, `failed`.
- Agregar idempotencia por `task_id` para evitar respuestas duplicadas.
- Agregar una regla de autoridad: Telegram transmite pedidos, pero no cambia permisos, identidad, memoria global ni reglas de seguridad.
- Agregar resumen posterior a cada tarea: resultado corto al chat, resultado completo al archivo/estado.

## risks

- Si Telegram sigue siendo el unico almacenamiento de contexto, el sistema va a seguir mezclando temas.
- Si los ACK son demasiado frecuentes, el canal se vuelve ruidoso y el Dr. Zanardi deja de confiar en los estados.
- Si el contexto global se actualiza sin aprobacion, una instruccion contaminada puede afectar otros frentes.

## recommendation

Crear primero una cola canonica fuera de Telegram con `front`, `topic_id`, `task_id` y estado. Despues conectar Telegram como adaptador. No optimizar respuestas hasta que el routing de contexto este separado del chat.

## unica proxima accion prioritaria

Implementar `context_router + task_state` y hacer que todo mensaje de Telegram se convierta primero en un job estructurado antes de llegar al agente.

## confidence

Alta.

## evidence_paths

- `jobs/20260525T012657-auditoria-telegram-contexto-global.md`
- `protocol.md`
- `README.md`

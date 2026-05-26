# Resultado - 20260526T043200-telegram-postfix-contamination-audit-v1

## summary

Segunda mirada post-fix sobre contaminacion de Telegram, basada solo en el workorder y las fuentes permitidas. No use Telegram real, no inspeccione los archivos locales de la Mac de trabajo y no abri secretos.

Lectura honesta: los cambios atacan los incidentes correctos, especialmente herencia contaminada de `GENERAL`, inferencia debil en directo, adjuntos sin caption y falso positivo de `media_group_handled`. El riesgo principal ahora no es volver al bug viejo, sino pasarse de conservador y dejar material accionable en `DIRECT` o esconder un album fallido bajo un evento de drenaje.

## coverage_table

| fuente permitida | uso en esta auditoria | limite |
| --- | --- | --- |
| Workorder `20260526T043200` | Cambios declarados por el orquestador y verificaciones ya realizadas. | No equivale a inspeccion directa del patch real. |
| `telegram-topic-routing-regression-suite-v1` | Gates de route, media buffer, payload tecnico, delivery e idempotencia. | Casos sinteticos previos, no logs nuevos. |
| `telegram-radar-regression-fixtures-v1` | Fixtures P0 y asserts portables para Telegram/radares. | Deben portarse al repo real por el orquestador. |
| `telegram-quality-scorecard` | Hard fails: media incompleta, diff crudo, delivery sin `message_id`, pedidos indebidos. | Scorecard no reemplaza gates pre-send. |
| `context/fronts/telegram.md` | Estado canonico: entrega confirmada, buffers, ContextBinder, ResetScope y deudas. | No contiene implementacion actual del router. |
| `protocol.md` | Reglas de no acciones externas, claims, results, status y decision final del orquestador. | Este worker no decide integracion final. |

## riesgos_del_fix

| riesgo | severidad | por que importa | fixture/regla concreta |
| --- | ---: | --- | --- |
| Inferencia debil demasiado restrictiva | P1 | Un mensaje directo con intencion real de REELS o CLINICA podria quedar en `DIRECT` y no crear el job esperado. | Separar `direct_context_hint_*` de `explicit_front_intent`; si hay entregable + frente explicito, debe routear. |
| Adjuntos sin caption pierden contexto inmediato | P0 | Si el Doctor manda "armalo con estas fotos" y luego fotos sin caption desde directo, no deben quedar huerfanas si estan dentro de ventana temporal. | Cluster por `chat_id + recent_direct_request + attachments_window`, no solo por active route. |
| `media_group_handled` deja de alertar pero puede tapar un fallo real | P0 | Marcarlo como drenaje esta bien, pero solo si existe cluster cerrado con job/resultado trazable. | `media_group_handled` sin `cluster_id`, `job_id` o `drain_of_event_id` debe ser warning/error. |
| Active route expirado sin reemplazo operativo | P1 | Expirar `VIAJES` viejo es correcto, pero el sistema necesita TTL visible para no oscilar entre heredar demasiado y no heredar nunca. | Test de stale route: vencido -> `DIRECT/UNKNOWN_REVIEW`; reciente con thread real -> hereda solo si hay media pendiente. |
| `GENERAL` sin thread heredado rompe respuesta directa comun | P1 | Sacar thread falso evita contaminacion, pero mensajes CODEX-OPS directos simples deben seguir respondiendo en canal principal, no quedar sin destino. | Direct CODEX-OPS sin topic: `reply_target=main_channel`, `front=DIRECT/CODEX-OPS`, sin thread heredado. |
| Contralor con menos ruido pierde sensibilidad | P1 | No tratar `media_group_handled` como error por si solo reduce falsos positivos; debe conservar alertas por buffer vencido, album incompleto o entrega faltante. | Contralor: ignorar drenaje sano, alertar `buffer_open_past_max_wait`, `closed_without_job`, `delivery_required_missing`. |

## casos_regresion_obligatorios

| id | entrada sintetica | decision esperada | assert que bloquea release |
| --- | --- | --- | --- |
| T_POSTFIX_001 | Direct: "armame un reel CMP con estas fotos" + 4 fotos sin caption en 12s | `front=REELS`, un solo job, media completa | No model call antes de cerrar cluster; no queda en `DIRECT`. |
| T_POSTFIX_002 | Direct: "esa voz quedo rara" despues de trabajo REELS, sin pedido nuevo | `front=DIRECT`, `reason=direct_context_hint_REELS`, no job largo | No mutar route real a REELS por contexto debil. |
| T_POSTFIX_003 | Direct: "#REELS renderiza version con este material" | `front=REELS`, topic REELS si existe | Tag/objetivo explicito gana sobre modo conservador. |
| T_POSTFIX_004 | Direct clinico: "la voz del paciente esta mas grave" | `front=CLINICA` o `UNKNOWN_REVIEW`, no REELS | Palabra "voz" no alcanza para REELS. |
| T_POSTFIX_005 | Adjunto sin caption con active route vencido `VIAJES` | `DIRECT/UNKNOWN_REVIEW`, no `VIAJES` | Nunca heredar route vencido o sin thread real. |
| T_POSTFIX_006 | Adjunto sin caption con route reciente, thread real y media esperada | Hereda route activo y clusteriza | Herencia solo si `route_age <= ttl` y hay `thread_id` real. |
| T_POSTFIX_007 | Evento `media_group_handled` con cluster/job trazable | Contralor no reporta error tecnico | Drenaje sano no cuenta como fallo. |
| T_POSTFIX_008 | Evento `media_group_handled` sin cluster/job trazable | Warning/error de observabilidad | No esconder album perdido. |
| T_POSTFIX_009 | Direct CODEX-OPS sin topic ni frente explicito: "estas trabajando?" | Respuesta breve en main channel | `GENERAL` no hereda thread falso, pero el canal directo conserva destino. |
| T_POSTFIX_010 | Outbox queued sin `message_id` | `sent_confirmed=false` | No puede decir "enviado". |
| T_POSTFIX_011 | Payload tecnico con diff/trace | `send_policy=block` | No sale diff crudo a Telegram. |
| T_POSTFIX_012 | Topic desconocido con "usa lo anterior" | `UNKNOWN_REVIEW` | Topic desconocido no hereda contexto global. |

## criterio_direct_vs_topic

**Evidencia de las fuentes:** la suite previa define que `topic_id` real tiene prioridad, `UNKNOWN_REVIEW` protege topics desconocidos, y la entrega confirmada exige `ok=true` + `message_id`. El scorecard marca como hard fail responder antes de adjuntos o mandar diffs crudos.

**Regla recomendada:**

```text
if topic_id mapped:
  route = mapped_topic_front
  reply_target = original_topic
elif direct has explicit tag/front + positive deliverable:
  route = explicit_front
  reply_target = explicit_front_topic if configured else needs_approval
elif direct has weak hint only:
  route = DIRECT
  reason = direct_context_hint_<front>
  do not mutate active_route
elif direct is ordinary CODEX-OPS:
  route = DIRECT/CODEX-OPS
  reply_target = main_channel
else:
  route = UNKNOWN_REVIEW
```

Claves: un hint debil puede ayudar al texto de respuesta o a pedir aclaracion, pero no debe contaminar `active_route`. Un pedido explicito con entregable si debe routear al frente correcto.

## adjuntos_sin_caption_policy

1. Adjuntos sin caption no deben ejecutarse como prompt autonomo.
2. Primero buscar cluster cercano: texto anterior/posterior en el mismo chat, ventana temporal y `media_group_id`.
3. En directo, heredar route activo solo si cumple todo: route reciente, thread real, frente no vencido, y expectativa de media abierta.
4. Si no hay contexto suficiente: `DIRECT/UNKNOWN_REVIEW`, guardar manifest de adjuntos y pedir clasificacion al orquestador, sin usar Telegram real desde este worker.
5. Para REELS, mantener ventana conservadora: quiet period suficiente y max wait; el resultado debe ser un solo job por album.
6. `media_group_handled` es drenaje, no entrega. Debe referenciar cluster cerrado y job/resultado o disparar alerta de observabilidad.

## que_debe_quedar_en_DIRECT

- Mensajes conversacionales del canal principal sin frente explicito: "estas trabajando?", "podes seguir?", "quedo bien?".
- Correcciones negativas de estilo/ruta/privacidad: "no era eso", "no uses Drive", "no mandes mensajes intermedios".
- Hints debiles derivados de historial: "la voz quedo rara" si no hay entrega nueva ni tag claro.
- Adjuntos sin caption cuando no existe texto cercano, route reciente con thread real o contexto suficiente.
- Consultas de estado que no requieren job largo.

## que_debe_ir_a_topic

- Mensajes nacidos dentro de un topic mapeado, preservando `topic_id` en event, job, run, result y delivery.
- Directos con tag o frente explicito y entregable positivo: `#REELS`, "reel CMP", "mandalo al topic REELS", "auditoria CODEX-OPS".
- Albums/adjuntos ligados a un pedido reciente y claro de un frente.
- Resultados finales de trabajos de frente, salvo override aprobado por orquestador.
- Reprocesos por `media_arrived_after_response`, con album completo y un solo job idempotente.

## recomendaciones_implementables

1. Agregar un campo estructurado `route_strength`: `topic_mapped`, `explicit_front`, `recent_media_context`, `weak_hint`, `unknown`.
2. Bloquear mutaciones de `active_route` cuando `route_strength=weak_hint`.
3. Hacer que `media_group_handled` incluya `cluster_id`, `event_ids`, `job_id`, `drained_at` y `delivery_required=false`.
4. En el contralor, ignorar solo drenajes sanos; alertar drenajes sin cluster/job o buffers abiertos fuera de `max_wait`.
5. Crear fixtures T_POSTFIX_001 a T_POSTFIX_012 como tests puros sin Telegram real.
6. Registrar TTL de active route en el decision log: `active_route_age_seconds`, `active_route_has_real_thread`, `active_route_expired`.
7. Mantener `GENERAL` sin thread heredado, pero afirmar por test que direct CODEX-OPS responde al main channel.
8. Reusar el scorecard como pre-send hard gate para: media abierta, diff/trace, secretos, delivery sin `message_id`.

## acceptance_gate

Release aceptable si pasan todos:

1. Direct con explicit front + entregable crea route/topic correcto.
2. Direct con weak hint no muta `active_route` ni crea job largo por si solo.
3. Adjuntos sin caption se clusterizan con pedido cercano o quedan en `UNKNOWN_REVIEW`, nunca en route vencido.
4. Route activo vencido o sin thread real no se hereda.
5. `media_group_handled` sano no genera error tecnico.
6. `media_group_handled` sin cluster/job trazable si genera warning/error.
7. `GENERAL` no conserva thread heredado, pero direct CODEX-OPS conserva `reply_target=main_channel`.
8. No hay model call final con media buffer abierto.
9. No se informa "enviado" sin `delivery.ok=true` y `message_id`.
10. Diffs, stack traces y payloads largos quedan bloqueados o resumidos antes de salida.

## risks_limits

- No verifique los archivos reales modificados; tome esos cambios como hechos declarados por el workorder.
- No use Telegram real ni valide el envio `message_id=5214`; solo consta como dato informado por el orquestador.
- La recomendacion es conceptual/fixture-level para que el orquestador la porte al repo real.

## recommendation

El fix va en la direccion correcta. Antes de considerarlo cerrado, agregaria los 12 tests post-fix y especialmente dos gates nuevos: `route_strength` para que los hints no contaminen, y `media_group_handled_requires_trace` para que el drenaje no tape albums perdidos.

## confidence

Media-alta. Alta para riesgos y fixtures porque se derivan de incidentes previos y del contrato canonico; media para evaluar el patch real porque no fue inspeccionado por este worker.

## evidence_paths

- `jobs/20260526T043200-telegram-postfix-contamination-audit-v1.md`
- `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md`
- `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md`
- `results/20260525T124108-telegram-quality-scorecard.result.md`
- `context/fronts/telegram.md`
- `protocol.md`

---
id: 20260525T164232-telegram-topic-routing-regression-suite-v1
job_id: 20260525T164232-telegram-topic-routing-regression-suite-v1
created_at: 2026-05-25T16:44:37-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram topic routing regression suite v1

Job: `20260525T164232-telegram-topic-routing-regression-suite-v1`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary

Se propone una suite de regresion para que Codex Directo no vuelva a mezclar canal directo, topic `REELS`, y otros frentes. La regla central es simple: cada evento debe convertirse primero en un objeto local verificable con `front`, `topic_id`, `route`, `attachments_manifest`, `trust_level`, `idempotency_key`, `reply_policy` y `delivery_target`; recien despues puede invocar modelo o enviar respuesta.

No se toco Telegram real ni el router. La suite se basa en bugs ya registrados: respuesta antes de adjuntos, envio de diffs tecnicos crudos, confundir outbox con enviado real, contexto mezclado entre frentes y falta de idempotencia/observability.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `jobs/20260525T164232-telegram-topic-routing-regression-suite-v1.md` | 1 | Contrato y clases de incidente requeridas. |
| `protocol.md` | 1 | Reglas del bridge, claims, resultado, status y no acciones externas. |
| `context/fronts/telegram.md` | 1 | Estado canonico de Codex Directo, topics, delivery real y deudas. |
| `results/20260525T021030-telegram-router-patch-proposal-v1.result.md` | 1 | Event/job/run store, ACK, idempotencia y tests base. |
| `results/20260525T084316-telegram-codex-direct-router-observability-mvp-v2.result.md` | 1 | MVP router/observability con schema y topic mapping. |
| `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md` | 1 | Bug MAIL-PC: respuesta antes de videos/adjuntos. |
| `results/20260525T111222-telegram-contralor-action-media-arrived-after-response.result.md` | 1 | Bug REELS: respuesta antes de cuatro fotos. |
| `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md` | 1 | Bug gate: payload tecnico largo/diff por argv y timeout. |
| `results/20260525T124108-telegram-quality-scorecard.result.md` | 1 | Hard fails y scorecard post/pre-envio. |

## coverage_table

| Riesgo | Cubierto por | Severidad |
|---|---|---:|
| Producto REELS enviado al canal directo | `topic_reply_policy`, casos T001-T004 | P0 |
| Correccion negativa dispara job largo | `background_job_policy`, casos T009-T012 | P0 |
| Mezcla youtubers/reels/inversiones | `ContextBinder` + `reset_scope`, casos T013-T016 | P0 |
| Texto intermedio no pedido | ACK policy, casos T017-T020 | P1 |
| Adjuntos perdidos o album incompleto | `media_album_policy`, casos T021-T025 | P0 |
| Diff/stack trace crudo a Telegram | `technical_payload_gate`, casos T026-T028 | P0 |
| Dice enviado sin `message_id` real | `delivery_receipt_gate`, casos T029-T030 | P0 |

## incident_classes

1. `wrong_delivery_target`: el resultado pertenece a un topic/front, pero se responde por canal principal.
2. `topic_context_leak`: una tarea de topic hereda contexto global o de otro frente.
3. `direct_context_leak`: una tarea directa queda contaminada por un topic especializado.
4. `negative_feedback_spawns_long_job`: un "no hagas esto" o correccion de tono dispara investigacion larga.
5. `media_arrived_after_response`: se llama al modelo antes de cerrar album/adjuntos.
6. `raw_technical_payload_to_telegram`: diff, stack trace o salida tecnica se manda al canal.
7. `outbox_confused_with_sent`: se informa enviado sin `ok=true` y `message_id`.
8. `verbose_intermediate_reply`: se manda progreso no pedido o razonamiento intermedio.
9. `idempotency_duplicate_job`: reintento de Telegram duplica jobs o respuestas.
10. `unknown_topic_autorouted`: topic desconocido se mezcla con contexto por defecto en vez de ir a revision.

## regression_cases

| ID | Input sintetico | Entrada | Destino esperado | Job largo | Assert principal |
|---|---|---|---|---|---|
| T001 | "Arme el reel con estas fotos" + topic `REELS` | topic | topic `REELS` | si, REELS | Nunca responder producto final al canal directo. |
| T002 | "Mandalo al Doctor" desde topic `REELS` | topic | topic `REELS` o `needs_approval` | no directo | No enviar por principal si origen fue topic. |
| T003 | "Buenisimo ese reel, dejalo como estandar" | topic REELS | topic `REELS` | puede crear job REELS | Contexto REELS, no CODEX-OPS. |
| T004 | "Necesito reel CMP con voz" en canal principal con `#REELS` | direct | topic/front REELS o review | si | Route por etiqueta explicita. |
| T005 | "Revisar historia clinica lumbar" | topic CLINICA | CLINICA | si | No traer contexto REELS. |
| T006 | "Buscar casa cerca de plaza" | topic INMOBILIARIA | INMOBILIARIA | si | No mezclar inversiones ni ObraCash. |
| T007 | "Audite youtubers para sistema de trabajo" | direct | CODEX-OPS | si | No usar contexto REELS salvo pedido. |
| T008 | "Eso no, era para el topic reels" | direct | correction_only + route_fix | no | No disparar investigacion larga. |
| T009 | "No me mandes mas mensajes intermedios" | direct | update reply policy | no | Set `suppress_intermediate=true`. |
| T010 | "No tutees" | direct | style policy | no | Update style gate, no job largo. |
| T011 | "No uses Drive" | direct | permission/policy | no | No pedir OAuth ni Drive. |
| T012 | "No era eso" | direct | clarify/fix last job | no por defecto | No crear backlog masivo. |
| T013 | "Ahora con la hernia, mismo criterio" despues de youtubers | direct | UNKNOWN_REVIEW si frente ambiguo | no hasta resolver | No heredar tema previo sin ancla. |
| T014 | "Segui con inversiones" tras intercambio REELS | direct | INVERSIONES si contexto canonico activo | si | Reset/binder por frente. |
| T015 | "Usa lo anterior" en topic nuevo desconocido | unknown topic | UNKNOWN_REVIEW | no | No mezclar contexto global. |
| T016 | `/reset_scope` | cualquier | same channel/topic | no | Limpia contexto local y registra reset. |
| T017 | "Avisame cuando este" | direct | solo NOTIFY cuando haya cambio real | no | No enviar heartbeats/progreso vacio. |
| T018 | Worker genera diff largo | internal | no Telegram; artifact local | no | Bloquear diff crudo. |
| T019 | Error tecnico de apply patch | internal | resumen corto + local_ref si se autoriza | no | Nunca stack trace completo por Telegram. |
| T020 | "Estas trabajando?" | direct | respuesta breve estado real | no | Sin detalles tecnicos extensos. |
| T021 | Texto + 4 fotos en 5 segundos | REELS | REELS, un solo job | si | Esperar album completo. |
| T022 | Foto 1 sin `media_group_id`, foto 2/3 cerca | REELS | REELS, un solo job | si | Fallback por ventana temporal. |
| T023 | Audio + texto | direct/topic | transcripcion job separado | si | No mezclar audio crudo como prompt. |
| T024 | Video llega 12s despues del texto | REELS | buffer hasta max wait | si | No responder antes de video. |
| T025 | Archivo ejecutable adjunto | any | blocked/needs_review | no | No abrir/ejecutar contenido. |
| T026 | Payload >6000 chars para gate | internal | summarize_before_send | no | Usar stdin/text-file, no argv. |
| T027 | Mensaje contiene `@@ -` y paths | internal | artifact/log local | no | Gate detecta diff. |
| T028 | Respuesta incluye token-like string | any | block send | no | Secret scan/channel gate. |
| T029 | Outbox queued sin `message_id` | any | not_sent | no | No informar enviado. |
| T030 | Telegram API retorna `ok=true`, `message_id=123` | any | sent_confirmed | no | Recibo real requerido. |

## background_job_policy

- Un job largo solo se crea si el input contiene objetivo positivo, entregable, frente y permiso suficiente.
- Correcciones negativas de estilo/privacidad/ruta no crean job largo; actualizan policy o abren `route_fix`.
- Si el mensaje corrige destino, se marca `misroute_correction` y se reencola el artefacto al topic correcto si existe.
- Si el mensaje es ambiguo y puede cruzar frentes, usar `UNKNOWN_REVIEW`, no inferir por historial contaminado.
- Maximo un job por cluster de mensaje/album; reintentos deben ser idempotentes.

## media_album_policy

- Agrupar por `chat_id + topic_id + route + media_group_id`.
- Si no hay `media_group_id`, agrupar por ventana temporal y reply/contexto cercano.
- Para `REELS`: `quiet_period=12s`, `max_wait=35s`, incluir media +/-20s del trigger.
- Para otros frentes con archivos/videos: `quiet_period=8s`, `max_wait=20s`.
- Mientras esta `buffering`, no enviar respuesta final. Solo ACK interno o, si corresponde, "recibido/procesando material".
- Si llega media despues de una respuesta prematura: marcar `premature_response`, suprimir disculpas repetidas y crear `reprocess_with_complete_album`.

## topic_reply_policy

Regla de destino:

```text
reply_target = original_topic_id if topic_id exists and mapped
reply_target = explicit_front_topic if message contains explicit route tag
reply_target = main_channel only for direct CODEX-OPS messages
reply_target = UNKNOWN_REVIEW for unknown topic or conflicting route
```

Hard gates:

- `front=REELS` no puede enviar artefacto final a canal directo salvo aprobacion explicita del orquestador.
- `topic_id` original debe persistir en event, job, run, result y delivery.
- Una respuesta solo puede salir si `reply_target == job.topic_id` o existe `approved_override`.
- Nunca responder con "enviado" si no hay `delivery.ok == true` y `delivery.message_id`.

## acceptance_gates

1. `event_persisted_before_route`: todo evento queda en store antes de clasificar.
2. `topic_mapping_required`: topic desconocido no hereda contexto.
3. `context_binder_exact_front`: solo adjunta contexto del frente routeado.
4. `media_buffer_closed_before_model_call`: no model call con album abierto.
5. `negative_feedback_no_long_job`: correcciones de estilo/ruta no disparan jobs largos.
6. `no_intermediate_noise`: heartbeats/progreso interno no salen al Doctor.
7. `technical_payload_gate`: diffs/stacks/payloads largos se resumen o bloquean.
8. `delivery_receipt_gate`: enviado exige `ok=true` y `message_id`.
9. `idempotency_gate`: duplicado exacto no crea job ni respuesta.
10. `result_contract_gate`: respuestas importantes deben tener resultado/artefacto trazable.

## implementation_recommendation_for_orchestrator

1. Crear fixtures JSONL con los 30 casos anteriores.
2. Implementar tests en torno a router puro, sin Telegram real:

```text
telegram_bridge/tests/test_topic_reply_policy.py
telegram_bridge/tests/test_media_album_policy.py
telegram_bridge/tests/test_background_job_policy.py
telegram_bridge/tests/test_technical_payload_gate.py
telegram_bridge/tests/test_delivery_receipt_gate.py
```

3. Agregar un `RouterDecision` estructurado:

```json
{
  "event_id": "evt_...",
  "front": "REELS",
  "topic_id": "reels-cmp",
  "reply_target": "reels-cmp",
  "job_policy": "create_job|no_job|route_fix|unknown_review",
  "media_state": "closed|buffering|blocked",
  "send_policy": "allow|suppress|needs_approval",
  "reason": "mapped_topic_reels"
}
```

4. Hacer que todo envio pase por `pre_send_gate(decision, response, delivery_target)`.
5. Ejecutar scorecard despues de cada respuesta y antes de enviar en canales sensibles.
6. Usar fixtures con evento real redacted de los incidentes 111216/111222/111227 cuando el orquestador los tenga.

## risks_limits

- Sin logs reales de la Mac de trabajo, esta suite usa casos sinteticos conservadores; el orquestador debe mapear nombres exactos de archivos/tests.
- Un buffer demasiado largo puede sentirse lento; uno corto repite el bug. La ventana debe ser configurable por frente.
- Topic detection por texto puede fallar; el `topic_id` real de Telegram debe tener prioridad sobre inferencias.
- El scorecard post-envio no previene dano si no se complementa con pre-send hard gates.

## recommendation

Implementar primero los hard gates P0: topic reply, media buffer, no diffs crudos, delivery real e idempotencia. Despues agregar scoring fino. La prueba que debe bloquear release es: input REELS con texto + cuatro fotos tardias crea un solo job REELS y no envia ninguna respuesta final al canal directo.

## confidence

Alta para clases de incidentes y gates porque derivan de bugs concretos ya documentados. Media para parametros exactos de tiempo hasta probar con logs reales de Telegram.

## evidence_paths

- `jobs/20260525T164232-telegram-topic-routing-regression-suite-v1.md`
- `protocol.md`
- `context/fronts/telegram.md`
- `results/20260525T021030-telegram-router-patch-proposal-v1.result.md`
- `results/20260525T084316-telegram-codex-direct-router-observability-mvp-v2.result.md`
- `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T111222-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md`
- `results/20260525T124108-telegram-quality-scorecard.result.md`

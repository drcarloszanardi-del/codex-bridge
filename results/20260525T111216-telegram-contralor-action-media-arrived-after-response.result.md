---
job_id: 20260525T111216-telegram-contralor-action-media-arrived-after-response
worker: personal-xh
status: completed
completed_at: 2026-05-25T11:20:19-03:00
front: CODEX-OPS
---

# Result

## summary

Diagnostico P1: Codex Directo respondio al evento `MAIL-PC` antes de que entraran todos los adjuntos del mismo chat. La causa probable es falta de buffer/debounce para media cercana en tiempo y/o falta de agrupacion por `media_group_id`/chat/route antes de llamar al modelo.

## findings con evidencia

- Finding: `media_arrived_after_response`.
- Route: `MAIL-PC`.
- Mensaje base: `4789/4790`.
- Adjuntos posteriores detectados: `4791`, `4792`.
- Recomendacion original del contralor: bufferizar albumes/adjuntos y pasar todas las rutas juntas antes de llamar al modelo.

## diagnostico

El router parece tratar cada mensaje como unidad procesable inmediata. Si el Doctor manda texto y luego videos/archivos, el primer evento dispara respuesta antes de que el album/adjuntos haya terminado de llegar.

Esto genera dos errores:

- Respuesta prematura: el modelo no ve todo el material.
- Contexto fracturado: los adjuntos quedan como mensajes tardios o jobs separados.

## archivos/rutas probables en work-mac

```text
/Users/jarvis/.openclaw/state/codex-telegram-direct/
/Users/jarvis/.openclaw/state/codex-telegram-direct/incoming-files/
/Users/jarvis/.openclaw/state/codex-telegram-direct/incoming-media/
/Users/jarvis/.openclaw/workspace/scripts/
telegram_bridge/router.py
telegram_bridge/event_store.py
telegram_bridge/attachments.py
telegram_bridge/ack_policy.py
```

Paquete minimo si el orquestador quiere revision exacta:

```text
events alrededor de 2026-05-23T11:47:32-0300
handler/router que crea el job o llama al modelo
schema de incoming-files/incoming-media
logs del ACK/respuesta enviada para message_id 4789/4790
```

## parche propuesto

Agregar `MediaArrivalBuffer` antes del model call:

```python
BUFFER_SECONDS = 8
MAX_WAIT_SECONDS = 20

def ingest_event(event):
    group_key = (
        event.chat_id,
        event.topic_id,
        event.route,
        event.media_group_id or event.reply_to_message_id or event.message_cluster_id,
    )
    store.append_event(event)
    if event.has_media or event.may_have_late_media:
        buffer.add(group_key, event)
        schedule_after_quiet_period(group_key, BUFFER_SECONDS, MAX_WAIT_SECONDS)
        return {"status": "buffering"}
    if recent_media_context_open(event.chat_id, event.route):
        buffer.add(group_key, event)
        schedule_after_quiet_period(group_key, BUFFER_SECONDS, MAX_WAIT_SECONDS)
        return {"status": "buffering"}
    return route_to_model([event])

def flush_group(group_key):
    events = buffer.collect_sorted(group_key)
    attachments = collect_attachments(events)
    job = create_job(events=events, attachments=attachments)
    return enqueue(job)
```

Regla: no enviar respuesta final mientras el grupo este `buffering`. Solo ACK silencioso interno o `queued`.

## prueba sintetica

```python
def test_mail_pc_late_videos_are_buffered_before_model_call():
    ingest(text_event(id=4789, telegram_id=4790, route="MAIL-PC", ts="11:47:32"))
    ingest(video_event(id=4791, route="MAIL-PC", ts="11:47:32"))
    ingest(video_event(id=4792, route="MAIL-PC", ts="11:47:45"))
    advance_time(seconds=8)

    assert model.calls == 1
    assert model.calls[0].message_ids == [4789, 4791, 4792]
    assert len(model.calls[0].attachments) == 2
    assert not sent_final_response_before(4792)
```

## riesgo

- Si el buffer es demasiado largo, Telegram se siente lento.
- Si es demasiado corto, vuelve el bug.
- Si no hay max wait, albums incompletos pueden quedar colgados.
- Si no hay idempotencia, reintentos duplican jobs.

Mitigacion: ventana inicial 8s, max wait 20s, idempotency key por `chat/topic/route/media_group/message_ids`.

## recommendation

Integrar buffer/debounce antes del model call y hacer que `MAIL-PC` use la misma logica que REELS/albumes. Este bug debe bloquear la respuesta final, no solo agregar adjuntos al contexto tarde.

## confidence

High. La evidencia del contralor muestra adjuntos inmediatamente posteriores a una respuesta; el parche es acotado y testeable.

## evidence_paths

- `jobs/20260525T111216-telegram-contralor-action-media-arrived-after-response.md`
- `results/20260525T084316-telegram-codex-direct-router-observability-mvp-v2.result.md`

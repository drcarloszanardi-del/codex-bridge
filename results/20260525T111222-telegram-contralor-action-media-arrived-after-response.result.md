---
job_id: 20260525T111222-telegram-contralor-action-media-arrived-after-response
worker: personal-xh
status: completed
completed_at: 2026-05-25T11:20:19-03:00
front: CODEX-OPS
---

# Result

## summary

Diagnostico P1: en route `REELS`, Codex Directo respondio antes de recibir cuatro fotos posteriores del mismo chat. Es el mismo patron que MAIL-PC, pero con mayor impacto: para reels/historias, responder sin album completo destruye la narrativa visual.

## findings con evidencia

- Finding: `media_arrived_after_response`.
- Route: `REELS`.
- Mensaje base: `216/4857`.
- Adjuntos posteriores detectados: `219`, `220`, `221`, `222`.
- Adjuntos: cuatro fotos en `incoming-media/`.
- Recomendacion original: bufferizar albumes/adjuntos y pasar todas las rutas juntas antes de llamar al modelo.

## diagnostico

El pipeline de REELS probablemente toma el primer texto/foto y genera respuesta antes de que Telegram termine de entregar el grupo. En Telegram, un album puede llegar como mensajes separados y no siempre esta completo al primer update.

Error funcional:

- El modelo analiza una pieza aislada.
- Pierde secuencia visual.
- Puede pedir materiales que ya llegaron segundos despues.
- Puede generar guion/storyboard incompleto.

## archivos/rutas probables en work-mac

```text
/Users/jarvis/.openclaw/state/codex-telegram-direct/incoming-media/
telegram_bridge/router.py
telegram_bridge/attachments.py
telegram_bridge/event_store.py
telegram_bridge/context_compiler.py
scripts/reels_* 
scripts/codex_telegram_direct*
```

Paquete minimo:

```text
eventos 216, 219, 220, 221, 222
raw updates Telegram si existen
handler que decide route REELS
log del model call / ACK para telegram_message_id 4857
```

## parche propuesto

Crear estado `album_buffer` por `chat_id + topic_id + route + media_group_id`, con fallback por ventana temporal si `media_group_id` falta.

```python
def group_key(event):
    if event.media_group_id:
        return ("album", event.chat_id, event.topic_id, event.route, event.media_group_id)
    if event.has_media:
        return ("nearby_media", event.chat_id, event.topic_id, event.route, time_bucket(event.ts, 20))
    return ("message", event.chat_id, event.topic_id, event.route, event.message_id)
```

Para route `REELS`, usar ventana mas conservadora:

```text
quiet_period = 12s
max_wait = 35s
min_album_check = include all media within +/-20s of trigger
```

Si ya se envio respuesta y llega media dentro de la ventana:

```text
mark_response_as_premature
create followup job: "reprocess_with_complete_album"
suppress repeated apology to Doctor
```

## prueba sintetica

```python
def test_reels_album_waits_for_late_photos():
    ingest(text_event(id=216, telegram_id=4857, route="REELS", ts="14:59:50"))
    ingest(photo_event(id=219, route="REELS", ts="14:59:51"))
    ingest(photo_event(id=220, route="REELS", ts="14:59:52"))
    ingest(photo_event(id=221, route="REELS", ts="14:59:53"))
    ingest(photo_event(id=222, route="REELS", ts="14:59:54"))
    advance_time(seconds=12)

    assert model.calls == 1
    assert model.calls[0].route == "REELS"
    assert model.calls[0].message_ids == [216, 219, 220, 221, 222]
    assert len(model.calls[0].attachments) == 4
    assert not final_response_sent_before_album_closed()
```

## riesgo

- REELS necesita respuesta rapida, pero necesita album completo mas que velocidad.
- Si se agrupan fotos no relacionadas por ventana temporal, puede mezclar pedidos.
- Si se depende solo de `media_group_id`, fallan fotos sueltas enviadas rapido.

Mitigacion: combinar `media_group_id` + ventana + route + topic + mensaje cercano; mostrar "procesando album" internamente, no respuesta final.

## recommendation

Para route REELS, album completo debe ser prerequisito antes del model call. La politica de reels ya exige "contexto de album completo"; este bug es una violacion directa de esa regla.

## confidence

High. Cuatro fotos posteriores al trigger prueban que la ventana actual es insuficiente o inexistente.

## evidence_paths

- `jobs/20260525T111222-telegram-contralor-action-media-arrived-after-response.md`
- `decisions/reels_cmp_premium_pipeline_qa_v1.md`
- `results/20260525T084316-telegram-codex-direct-router-observability-mvp-v2.result.md`

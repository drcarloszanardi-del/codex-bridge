---
job_id: 20260527T162339-telegram-contralor-action-media-arrived-after-response
worker: personal-xh
status: completed
completed_at: 2026-05-27T16:25:00-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - telegram contralor action media arrived after response

## summary

Diagnostico P1 alto: el buffer de Telegram Directo todavia no cubre bien el caso
**DIRECT + adjunto/documento tardio sin album**. El contralor muestra que Codex
Directo respondio alrededor del mensaje `431/432` y enseguida entro otro adjunto
del mismo chat, `433`, un PDF en `incoming-files`. No abri ese PDF ni use
Telegram real.

La causa probable no es routeo a frente equivocado, sino una brecha del
`MediaArrivalBuffer`: cubre albumes/media groups y casos REELS/postfix, pero el
camino DIRECT puede llamar al modelo apenas llega el texto aunque todavia este
abierta una ventana razonable para documentos sueltos. Tambien puede haber una
separacion artificial entre `incoming-media` y `incoming-files`, dejando los PDF
fuera de `has_media`/`attachments_pending`.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T162339-telegram-contralor-action-media-arrived-after-response.md` | Revisada | Workorder, finding JSON, action JSON y evidencia. |
| `context/fronts/telegram.md` | Revisada | Canon Telegram: buffer, delivery real y deuda activa. |
| `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md` | Revisada | Incidente previo de media tardia en MAIL-PC y parche base. |
| `results/20260525T111222-telegram-contralor-action-media-arrived-after-response.result.md` | Revisada | Incidente previo de album/fotos tardias en REELS. |
| `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md` | Revisada | Fixture `reels_text_plus_four_photos_late_album` y gates de delivery. |
| `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md` | Revisada | Suite postfix sobre media buffer, captionless attachments y delivery. |
| `results/20260526T071000-telegram-t13-postfix-final-review-v1.result.md` | Revisada | Cierre T13 y limites para nearby media route correction. |

## findings

| Severidad | Hallazgo | Evidencia | Impacto |
| --- | --- | --- | --- |
| P1 | Respuesta final antes de cerrar ventana de adjuntos. | Finding `media_arrived_after_response`, `route=DIRECT`, `message_id=431`, `telegram_message_id=432`, `later_media_message_ids=[433]`. | El modelo responde sin ver todo el material y puede dar una respuesta incompleta. |
| P1 | El caso involucra `incoming-files`, no solo fotos/videos. | `later_media_paths` apunta a `.../incoming-files/433-...presupuesto_115819.pdf`. | Si el buffer solo mira media groups/fotos, documentos PDF quedan tarde. |
| P1 | Regresion de una clase ya conocida. | Resultados previos `20260525T111216`, `20260525T111222` y fixtures postfix recomiendan no hacer model call antes de cerrar media. | La proteccion debe ser route-agnostic y attachment-agnostic, no especial de REELS. |

## diagnostico

El pipeline probable:

1. llega texto o evento base `431/432` por `DIRECT`;
2. el router compila contexto y llama al modelo inmediatamente;
3. se envia respuesta final;
4. dentro de la ventana de cercania llega el PDF `433`;
5. el contralor detecta que el adjunto llego despues de la respuesta.

La falla concreta a buscar: algun predicado del estilo `should_buffer_media`,
`has_media`, `media_group_open`, `recent_media_context_open` o
`attachments_for_event` excluye documentos en `incoming-files`, o solo se activa
cuando ya llego el adjunto. Para DIRECT, el texto base deberia abrir una ventana
corta de "posibles adjuntos proximos" antes de cualquier respuesta final.

## archivos_rutas_probables

Rutas probables en la Mac de trabajo:

```text
/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py
/Users/jarvis/.openclaw/state/codex-telegram-direct/incoming-files/
/Users/jarvis/.openclaw/state/codex-telegram-direct/incoming-media/
/Users/jarvis/.openclaw/state/codex-telegram-direct/runs/
/Users/jarvis/.openclaw/state/codex-telegram-direct/events/
```

Modulos o zonas probables:

```text
router / event ingestion
attachment collection / incoming-files handling
media buffer / nearby media buffer
context compiler / model call gate
delivery final response gate
contralor media_arrived_after_response detector
```

Paquete minimo si el orquestador quiere revision exacta sin secretos:

```text
sanitized raw events 431, 432, 433
timestamps exactos de model_call_start/model_call_end/delivery
sanitized route decision for 431/432
attachment metadata for 433 without file contents
snippet of buffer predicates and final-response gate
```

## parche_propuesto

Agregar o extender un buffer **route-agnostic** de adjuntos cercanos antes del
model call:

```python
DIRECT_QUIET_SECONDS = 7
DIRECT_MAX_WAIT_SECONDS = 22

ATTACHMENT_TYPES = {"photo", "video", "document", "audio", "voice", "animation"}

def is_attachment_event(event):
    return bool(event.type in ATTACHMENT_TYPES or event.file_path or event.file_id)

def opens_nearby_attachment_window(event):
    if is_attachment_event(event):
        return True
    if event.route in {"DIRECT", "CODEX-OPS", "REELS", "MAIL-PC"}:
        return event.is_user_message and not event.is_command_only
    return False

def cluster_key(event):
    return (
        event.chat_id,
        event.topic_id,
        event.route,
        event.media_group_id or event.reply_to_message_id or "nearby",
    )

def ingest_event(event):
    key = cluster_key(event)
    store_event(event)

    if opens_nearby_attachment_window(event) or buffer.is_open_near(event.chat_id, event.topic_id, event.route):
        buffer.add(key, event)
        buffer.schedule_flush(key, quiet_seconds=DIRECT_QUIET_SECONDS, max_wait_seconds=DIRECT_MAX_WAIT_SECONDS)
        return {"status": "buffering", "reason": "nearby_attachment_window"}

    return call_model_with_events([event])

def flush_buffer(key):
    events = buffer.collect_sorted(key)
    attachments = collect_incoming_files_and_media(events)
    idempotency_key = stable_hash([e.telegram_message_id for e in events] + [a.path for a in attachments])
    if already_processed(idempotency_key):
        return {"status": "deduped"}
    return call_model_with_events(events, attachments=attachments, idempotency_key=idempotency_key)
```

Reglas de integracion:

- `document`/PDF cuenta como adjunto igual que foto/video.
- No enviar respuesta final mientras el cluster este `buffering`.
- Mantener DIRECT como DIRECT; no routear a otro frente solo porque llego un PDF.
- Ordenar por timestamp y `telegram_message_id`.
- Si llega media despues de una respuesta dentro de la ventana de gracia, marcar
  `premature_response_detected`, crear un reprocess interno y suprimir doble
  disculpa al Doctor.
- Idempotencia por `chat/topic/route/message_ids/attachment_paths` para no crear
  jobs duplicados.

## prueba_sintetica

Caso principal:

```python
def test_direct_text_waits_for_late_pdf_before_model_call():
    ingest(text_event(id=431, telegram_id=432, route="DIRECT", ts_ms=0, text="revisar esto"))
    advance_time(seconds=3)
    assert model.calls == []
    assert final_responses == []

    ingest(document_event(id=433, route="DIRECT", ts_ms=3500, path="incoming-files/433-presupuesto.pdf"))
    advance_time(seconds=8)

    assert model.calls == 1
    assert model.calls[0].route == "DIRECT"
    assert model.calls[0].message_ids == [431, 433]
    assert model.calls[0].attachments_count == 1
    assert model.calls[0].attachments[0].kind == "document"
    assert not final_response_sent_before_message(433)
```

Casos adicionales:

```python
def test_direct_text_without_late_attachment_flushes_after_quiet_period():
    ingest(text_event(id=500, telegram_id=501, route="DIRECT", ts_ms=0))
    advance_time(seconds=8)
    assert model.calls == 1
    assert model.calls[0].attachments_count == 0

def test_pdf_after_response_within_grace_creates_internal_reprocess_not_public_apology():
    mark_final_response_sent(message_id=431, ts_ms=4000)
    ingest(document_event(id=433, route="DIRECT", ts_ms=6500, path="incoming-files/433-presupuesto.pdf"))
    assert incident_log.contains("premature_response_detected")
    assert reprocess_jobs.count == 1
    assert public_apologies.count == 0

def test_incoming_files_are_collected_with_incoming_media():
    events = [document_event(id=433, path="incoming-files/433.pdf"), photo_event(id=434, path="incoming-media/434.jpg")]
    attachments = collect_incoming_files_and_media(events)
    assert {a.kind for a in attachments} == {"document", "photo"}
```

## riesgo

| Riesgo | Mitigacion |
| --- | --- |
| Latencia extra en DIRECT. | Ventana corta: quiet `6-8s`, max wait `20-25s`; comandos explicitos pueden saltar buffer. |
| Agrupar mensajes no relacionados. | Key por chat/topic/route y ventana corta; cerrar por quiet period; no mezclar tras respuesta enviada. |
| Duplicar model calls si llega adjunto tarde. | Idempotency key estable y reprocess interno unico. |
| Perder PDF por tratar solo fotos/videos. | Unificar `incoming-files` e `incoming-media` como attachments. |
| Responder dos veces al Doctor. | Si ya hubo respuesta prematura, reprocess interno sin mensaje externo automatico. |

## recommendation

Implementar el buffer de adjuntos cercanos antes de cualquier model call en
DIRECT y hacerlo attachment-agnostic (`photo`, `video`, `document`, PDF,
`voice`). Agregar fixtures P1:

- `T_DIRECT_TEXT_THEN_LATE_PDF_BUFFERED`
- `T_DIRECT_TEXT_NO_MEDIA_FLUSHES_AFTER_QUIET`
- `T_DIRECT_LATE_PDF_AFTER_RESPONSE_REPROCESS_INTERNAL`
- `T_ATTACHMENT_COLLECTOR_INCOMING_FILES_AND_MEDIA`

Mantener envio real desacoplado: el fix debe impedir respuesta final antes del
cierre del buffer, no enviar Telegram desde el test.

## confidence

Alta para la causa probable y el parche conceptual: la evidencia del contralor
es directa y coincide con incidentes previos de media tardia. Media para nombres
exactos de funciones/archivos porque no inspeccione la app real ni logs de la
Mac de trabajo.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso el workorder, `context/fronts/telegram.md` y resultados Telegram
  previos relevantes.
- No se abrio Telegram real, Gmail, Drive, Photos/iCloud, datos privados ni el
  PDF mencionado por el contralor.

## risks_limits

- La ruta `later_media_paths` se trato como evidencia no confiable y no se
  abrio.
- No se inspecciono el repo/app real en `/Users/jarvis`.
- No se validaron timestamps reales de delivery/model call, solo el finding
  provisto por el contralor.
- La decision final de patch queda en Codex orquestador.

## evidence_paths

- `jobs/20260527T162339-telegram-contralor-action-media-arrived-after-response.md`
- `claims/20260527T162339-telegram-contralor-action-media-arrived-after-response.json`
- `context/fronts/telegram.md`
- `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T111222-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md`
- `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md`
- `results/20260526T071000-telegram-t13-postfix-final-review-v1.result.md`

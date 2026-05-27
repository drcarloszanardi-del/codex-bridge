---
job_id: 20260527T170359-telegram-contralor-action-media-only-after-assistant-completion
worker: personal-xh
status: completed
completed_at: 2026-05-27T17:09:04-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram media only after assistant completion 443

## summary

Diagnostico P1: esto parece ser el residuo posterior al patch del buffer
`DIRECT` texto + PDF. El contralor ahora no dice solamente "media llego tarde
antes de responder", sino **media sin caption quedo registrada despues de una
completion/final response**. El mensaje `443` entro a las `16:54:57-0300` en
`DIRECT`, y hay un companion casi inmediato, `444`, seis segundos despues.

La causa probable no se arregla solo con `settle_seconds=7/max_wait=22`: hace
falta una segunda barrera despues de completar una respuesta. Cuando el sistema
acaba de responder, cualquier adjunto sin caption del mismo chat/topic/route
dentro de una ventana corta debe tratarse como lote tardio/incompleto del run
previo o como reprocess interno, no como un pedido cerrado ni como una respuesta
publica nueva.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T170359-telegram-contralor-action-media-only-after-assistant-completion.md` | Revisada | Finding de mensaje `443`, action JSON y recomendacion. |
| `jobs/20260527T170404-telegram-contralor-action-media-only-after-assistant-completion.md` | Revisada | Companion de mensaje `444`, misma clase a los 6s. |
| `context/fronts/telegram.md` | Revisada | Canon: buffer de adjuntos cercanos, delivery real, ContextBinder. |
| `results/20260527T162339-telegram-contralor-action-media-arrived-after-response.result.md` | Revisada | Diagnostico previo de PDF/adjunto tardio en DIRECT. |
| `results/20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1.result.md` | Revisada | Review del patch `7s/22s` y fixtures faltantes. |
| `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md` | Revisada | Fixtures de captionless attachments y buffer media. |
| `results/20260526T071000-telegram-t13-postfix-final-review-v1.result.md` | Revisada | Limites de nearby media route correction. |

## findings

| Severidad | Hallazgo | Evidencia | Impacto |
| --- | --- | --- | --- |
| P1 | Falta guard posterior a completion. | Finding `media_only_after_assistant_completion`, mensaje `443`, `route=DIRECT`, timestamp `16:54:57-0300`. | El sistema puede considerar cerrada una interaccion aunque el usuario siga mandando adjuntos. |
| P1 | Hay dos adjuntos cercanos que deberian formar un solo batch. | Job companion `170404` reporta mensaje `444` a `16:55:03-0300`, seis segundos despues. | Riesgo de dos actions/jobs y dos reprocess para un mismo lote. |
| P1 | Observabilidad incompleta: `prior_assistant_message_id` viene `null`. | El finding dice "despues de una respuesta final" pero evidence no trae id de respuesta previa. | El contralor sabe que hubo completion, pero el paquete no permite auditar con precision el run anterior. |

## diagnostico

Pipeline probable:

1. Un run `DIRECT` termino y marco completion/final response.
2. Despues llegaron adjuntos sin caption `443` y `444` en la misma conversacion.
3. Como esos adjuntos no tienen texto, el sistema no los unio al run previo o no
   genero un reprocess interno consolidado.
4. El contralor abrio dos actions independientes porque la llave incluye
   `message_id`, aunque ambos eventos son un solo cluster temporal.

El patch previo cubre la ventana **antes** del model call. Este finding exige
una ventana **despues** de la completion: un `recent_completion_guard` o
`post_completion_late_media_window` keyed por `chat_id/topic_id/route`.

## archivos_rutas_probables

```text
/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py
/Users/jarvis/.openclaw/state/codex-telegram-direct/events/
/Users/jarvis/.openclaw/state/codex-telegram-direct/runs/
/Users/jarvis/.openclaw/state/codex-telegram-direct/incoming-files/
/Users/jarvis/.openclaw/state/codex-telegram-direct/incoming-media/
/Users/jarvis/.openclaw/workspace/state/codex_telegram_channel_contralor/last_low_cost_ai_review.json
```

Paquete minimo sanitizado para revision exacta:

```text
events 438-444 with chat_id/topic_id/route/timestamps only
run_id and model_call_start/model_call_end for the prior DIRECT response
delivery record with ok=true and assistant_message_id if available
attachment metadata for 443 and 444 without file contents
current buffer/reprocess/contralor detector snippets
```

## parche_propuesto

Agregar una barrera de media tardia posterior a completion:

```python
POST_COMPLETION_MEDIA_GRACE_SECONDS = 30
LATE_MEDIA_QUIET_SECONDS = 7
LATE_MEDIA_MAX_WAIT_SECONDS = 22

def completion_key(event_or_run):
    return (event_or_run.chat_id, event_or_run.topic_id, event_or_run.route)

def mark_assistant_completion(run, delivery):
    recent_completion_guard.set(
        completion_key(run),
        {
            "run_id": run.id,
            "assistant_message_id": delivery.message_id,
            "completed_at": now(),
            "user_message_ids": run.user_message_ids,
        },
        ttl_seconds=POST_COMPLETION_MEDIA_GRACE_SECONDS,
    )

def handle_captionless_media(event):
    guard = recent_completion_guard.get(completion_key(event))
    if guard and within(event.ts, guard["completed_at"], POST_COMPLETION_MEDIA_GRACE_SECONDS):
        late_media_buffer.add(guard["run_id"], event)
        late_media_buffer.schedule_flush(
            guard["run_id"],
            quiet_seconds=LATE_MEDIA_QUIET_SECONDS,
            max_wait_seconds=LATE_MEDIA_MAX_WAIT_SECONDS,
        )
        return {
            "status": "late_media_reprocess_pending",
            "prior_run_id": guard["run_id"],
            "prior_assistant_message_id": guard["assistant_message_id"],
            "public_send": False,
        }
    return handle_media_without_recent_completion(event)

def flush_late_media(run_id):
    attachments = late_media_buffer.collect_sorted(run_id)
    reprocess_key = stable_hash([run_id] + [a.telegram_message_id for a in attachments])
    if already_processed(reprocess_key):
        return {"status": "deduped"}
    return create_internal_reprocess(
        prior_run_id=run_id,
        attachments=attachments,
        public_send=False,
        reason="media_only_after_assistant_completion",
    )
```

Cambios de politica:

- `photo`, `video`, `document`, PDF, `voice` y `audio` cuentan como media.
- No enviar disculpa ni segunda respuesta publica automaticamente.
- El reprocess debe ser interno y unico por `prior_run_id + media_message_ids`.
- Si `prior_assistant_message_id` es `null`, guardar `prior_run_id` igual y
  marcar el caso como `unattributed_completion_guard_hit`.
- El contralor debe deduplicar actions por cluster temporal, no por cada
  `message_id`.

## prueba_sintetica

```python
def test_direct_captionless_media_after_completion_reprocesses_once():
    run = completed_direct_run(
        run_id="run-431",
        chat_id=10,
        topic_id=None,
        route="DIRECT",
        assistant_message_id=9001,
        completed_at_ms=10_000,
    )
    mark_assistant_completion(run, delivery_ok(message_id=9001))

    ingest(document_event(telegram_id=443, ts_ms=15_000, route="DIRECT", caption=None))
    ingest(document_event(telegram_id=444, ts_ms=21_000, route="DIRECT", caption=None))
    advance_time(seconds=8)

    assert public_sends.count == 0
    assert reprocess_jobs.count == 1
    assert reprocess_jobs[0].prior_run_id == "run-431"
    assert reprocess_jobs[0].prior_assistant_message_id == 9001
    assert reprocess_jobs[0].media_message_ids == [443, 444]
```

Fixtures adicionales:

```text
T_DIRECT_MEDIA_ONLY_AFTER_COMPLETION_REPROCESS_INTERNAL
T_DIRECT_MEDIA_ONLY_AFTER_COMPLETION_DEDUPES_443_444
T_DIRECT_MEDIA_ONLY_NO_RECENT_COMPLETION_GOES_UNKNOWN_REVIEW
T_DIRECT_TEXT_THEN_LATE_PDF_BUFFERED_STILL_PASSES
T_DIRECT_COMPLETION_GUARD_EXPIRES_AFTER_TTL
```

## recommendation

Mantener el patch `DIRECT 7s/22s`, pero no cerrar el incidente todavia.
Implementar ahora el `post_completion_late_media_guard` y deduplicacion de
actions para adjuntos sin caption cercanos. El resultado esperado para `443` y
`444` es un solo reprocess interno del run anterior, sin Telegram publico.

## confidence

Media-alta para la causa probable porque el patron `443/444` encaja con
adjuntos sin caption post-completion y con la deuda ya documentada. Media para
certificar el run exacto porque no se leyo `/Users/jarvis` ni el archivo
`last_low_cost_ai_review.json`. Alta para recomendar no usar canales externos y
no inspeccionar contenido real de adjuntos desde este worker.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh`.
- Se reclamaron los jobs `170359` y `170404` con `scripts/bridgectl.py claim`.
- Se revisaron ambos workorders, `context/fronts/telegram.md` y resultados
  previos de Telegram sobre buffer/adjuntos.
- No se abrio Telegram real, Gmail, Drive, Calendar, Photos/iCloud, ObraCash ni
  ningun adjunto real.

## risks_limits

- Sin los eventos sanitizados del run previo no puedo identificar el
  `assistant_message_id` real de la completion; el paquete del finding trae
  `prior_assistant_message_id: null`.
- La propuesta es de integracion para Codex principal, no parche aplicado en la
  app real.
- Si los adjuntos `443/444` pertenecian a un pedido nuevo sin texto, el guard
  igual debe evitar respuesta publica automatica y mandar a review interna.

## evidence_paths

- `jobs/20260527T170359-telegram-contralor-action-media-only-after-assistant-completion.md`
- `jobs/20260527T170404-telegram-contralor-action-media-only-after-assistant-completion.md`
- `claims/20260527T170359-telegram-contralor-action-media-only-after-assistant-completion.json`
- `claims/20260527T170404-telegram-contralor-action-media-only-after-assistant-completion.json`
- `context/fronts/telegram.md`
- `results/20260527T162339-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1.result.md`
- `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md`
- `results/20260526T071000-telegram-t13-postfix-final-review-v1.result.md`

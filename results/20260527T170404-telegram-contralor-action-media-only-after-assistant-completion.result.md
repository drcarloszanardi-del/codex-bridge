---
job_id: 20260527T170404-telegram-contralor-action-media-only-after-assistant-completion
worker: personal-xh
status: completed
completed_at: 2026-05-27T17:09:04-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram media only after assistant completion 444

## summary

El mensaje `444` es el companion del hallazgo `443`: mismo frente `DIRECT`,
misma clase `media_only_after_assistant_completion`, seis segundos despues. Mi
diagnostico es tratar `443` y `444` como **un solo lote tardio de adjuntos sin
caption posterior a una completion**, no como dos incidentes independientes.

La prioridad no es ampliar indefinidamente el buffer previo al model call. La
pieza faltante es un guard posterior a completion que capture media-only events
durante una ventana corta, los dedupe por run/cluster, y cree un reprocess
interno sin enviar Telegram publico.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T170404-telegram-contralor-action-media-only-after-assistant-completion.md` | Revisada | Finding de mensaje `444`. |
| `jobs/20260527T170359-telegram-contralor-action-media-only-after-assistant-completion.md` | Revisada | Finding companion de mensaje `443`. |
| `context/fronts/telegram.md` | Revisada | Canon Telegram: buffer, delivery real y ContextBinder. |
| `results/20260527T162339-telegram-contralor-action-media-arrived-after-response.result.md` | Revisada | Diagnostico previo del borde DIRECT + adjunto tardio. |
| `results/20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1.result.md` | Revisada | Review del patch previo `7s/22s`. |
| `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md` | Revisada | Politica de captionless attachments. |

## findings

| Severidad | Hallazgo | Evidencia | Decision |
| --- | --- | --- | --- |
| P1 | `444` no debe abrir un flujo separado si `443` ya abrio late-media batch. | `444` llega a `16:55:03-0300`; `443` llego a `16:54:57-0300`. | Agrupar y deduplicar por completion/run. |
| P1 | `prior_assistant_message_id` faltante limita auditoria. | Evidence del action JSON trae `prior_assistant_message_id: null`. | Agregar `prior_run_id`/`assistant_message_id` al detector. |
| P1 | El caso confirma que la falla es post-completion. | El tipo del finding no es solo `media_arrived_after_response`, sino `media_only_after_assistant_completion`. | Sumar guard posterior, no solo buffer previo. |

## recommendation

Implementar el mismo parche recomendado en el resultado companion `170359`:
`post_completion_late_media_guard` con TTL corto, late-media quiet window,
dedupe por `prior_run_id + media_message_ids`, y reprocess interno sin envio
publico. En el contralor, generar una sola action para el cluster `443/444` o
marcar la segunda como duplicada de la primera.

Parche minimo:

```python
cluster_id = (
    chat_id,
    topic_id,
    route,
    prior_run_id or "unattributed_completion",
    floor_to_window(first_late_media_ts, seconds=30),
)
if captionless_media_after_completion(event):
    late_media_buffer.add(cluster_id, event)
    suppress_public_send(event)
    schedule_internal_reprocess(cluster_id, quiet_seconds=7, max_wait_seconds=22)
```

Prueba sintetica minima:

```python
def test_second_media_only_after_completion_joins_existing_batch():
    mark_assistant_completion(run_id="run-direct-1", assistant_message_id=9001, ts_ms=10_000)
    ingest(document_event(telegram_id=443, route="DIRECT", ts_ms=15_000, caption=None))
    ingest(document_event(telegram_id=444, route="DIRECT", ts_ms=21_000, caption=None))
    advance_time(seconds=8)

    assert contralor_actions.count_for_kind("media_only_after_assistant_completion") <= 1
    assert reprocess_jobs.count == 1
    assert reprocess_jobs[0].media_message_ids == [443, 444]
    assert public_sends.count == 0
```

## confidence

Alta en que `444` es parte del mismo cluster que `443` por cercania temporal,
route y tipo. Media en los IDs del run previo porque el paquete no expone
`prior_assistant_message_id`. Alta en que no corresponde ninguna accion externa
desde este worker.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh`.
- Se reclamo el job con `scripts/bridgectl.py claim`.
- Se reviso el workorder `170404`, el companion `170359`, contexto Telegram y
  resultados previos del mismo frente.
- No se leyeron adjuntos reales ni se uso Telegram/Gmail/Drive/Calendar.

## risks_limits

- Sin eventos sanitizados y delivery record no puedo confirmar si `443/444` son
  documentos, imagenes u otro tipo de media; el finding solo dice adjunto sin
  caption.
- Si el usuario queria iniciar un pedido nuevo solo con adjuntos, el sistema
  igualmente deberia llevarlo a review/reprocess interno, no responder de forma
  publica y aislada.

## evidence_paths

- `jobs/20260527T170404-telegram-contralor-action-media-only-after-assistant-completion.md`
- `jobs/20260527T170359-telegram-contralor-action-media-only-after-assistant-completion.md`
- `claims/20260527T170404-telegram-contralor-action-media-only-after-assistant-completion.json`
- `claims/20260527T170359-telegram-contralor-action-media-only-after-assistant-completion.json`
- `context/fronts/telegram.md`
- `results/20260527T162339-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1.result.md`

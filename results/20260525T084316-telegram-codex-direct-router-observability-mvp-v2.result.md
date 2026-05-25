---
job_id: 20260525T084316-telegram-codex-direct-router-observability-mvp-v2
worker: personal-xh
status: completed
completed_at: 2026-05-25T08:52:07-03:00
front: CODEX-OPS
---

# Result

## summary

MVP propuesto para router/observability de Telegram sin tocar Telegram real: event store local, topic mapping explicito, idempotencia, ACK no ruidoso, manejo de albums/archivos/audio y pruebas con fixtures. El canal principal debe comportarse como Codex principal; los topics deben funcionar como contextos por frente.

## findings con evidencia

- `decisions/telegram_router_patch_proposal_v1.md` ya define los componentes base: events, jobs, runs, state/fronts, state/topics, router, context compiler, ack policy e idempotency.
- La propuesta previa ya identifica riesgos criticos: historial crudo como contexto global, ACK excesivo y duplicacion por falta de idempotencia.
- El job actual pide convertir eso en MVP implementable y observable, no ejecutar acciones reales en Telegram.

## patch plan

```text
telegram_bridge/
  router.py
  event_store.py
  topic_map.py
  context_compiler.py
  idempotency.py
  ack_policy.py
  observability.py
  attachments.py
  audio.py
  errors.py
  fixtures/
    telegram_events.jsonl
  tests/
    test_router_idempotency.py
    test_topic_mapping.py
    test_albums_attachments_audio.py
    test_prompt_injection_boundaries.py
    test_ack_policy.py
```

## event store

Usar SQLite local o JSONL append-only. Recomendado SQLite si ya esta disponible; JSONL si se busca maxima simplicidad.

Schema minimo:

```sql
CREATE TABLE events (
  event_id TEXT PRIMARY KEY,
  received_at TEXT NOT NULL,
  chat_hash TEXT NOT NULL,
  topic_id TEXT,
  message_id TEXT NOT NULL,
  media_group_id TEXT,
  sender_hash TEXT,
  kind TEXT NOT NULL,
  text TEXT,
  attachment_count INTEGER NOT NULL DEFAULT 0,
  raw_json_path TEXT,
  trust_level TEXT NOT NULL DEFAULT 'untrusted'
);

CREATE TABLE routed_jobs (
  job_id TEXT PRIMARY KEY,
  event_id TEXT NOT NULL,
  front TEXT NOT NULL,
  topic_id TEXT,
  objective TEXT NOT NULL,
  status TEXT NOT NULL,
  idempotency_key TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL,
  result_ref TEXT
);

CREATE TABLE runs (
  run_id TEXT PRIMARY KEY,
  job_id TEXT NOT NULL,
  status TEXT NOT NULL,
  heartbeat_at TEXT,
  blocked_reason TEXT,
  error_code TEXT
);
```

## topic mapping

Archivo local versionado:

```yaml
default_front: UNKNOWN_REVIEW
topics:
  "main":
    front: CODEX-OPS
    mode: principal
  "clinica":
    front: CLINICA
    mode: context
  "tesis":
    front: TESIS
    mode: context
  "reels-cmp":
    front: REELS-CMP
    mode: context
  "inmobiliaria":
    front: INMOBILIARIA
    mode: context
```

Regla: si topic/chat no esta mapeado, crear job `UNKNOWN_REVIEW` y no mezclar con contexto global.

## idempotencia

`idempotency_key = sha256(chat_hash + topic_id + message_id + normalized_text_hash + attachment_hashes + media_group_id)`

Reglas:

- Mismo mensaje exacto no crea segundo job.
- Reintento con mismo `message_id` actualiza observability y ACK silencioso.
- Album con mismo `media_group_id` se agrupa con ventana corta antes de routear.
- Ediciones de mensaje crean evento nuevo tipo `message_edited` y decision separada.

## ACK no ruidoso

Estados que pueden responder:

- `queued`: un ACK corto, solo una vez.
- `needs_approval`: avisar porque requiere decision humana.
- `blocked`: avisar una vez con motivo.
- `done`: avisar con result_ref corto si corresponde.
- `failed`: avisar una vez con error_code.

Estados que no deben responder:

- heartbeat interno.
- duplicado idempotente.
- progreso repetitivo.
- clasificacion intermedia.

Ejemplo de ACK:

```text
Recibido. job=20260525T084316-... estado=queued
```

## typing/status

Si la API disponible lo permite, usar `typing` solo mientras se convierte evento a job o se compila contexto. No usar typing para mantener falsa actividad. Si falla, registrar `typing_unavailable` sin bloquear.

## manejo de albums, archivos y audio

- Albums: agrupar por `media_group_id`, esperar ventana corta, guardar manifest con lista de archivos, crear un solo job.
- Archivos: guardar metadata y hash; no abrir contenido ejecutable automaticamente.
- Imagenes: tratarlas como adjuntos no confiables; OCR/vision solo en worker autorizado.
- Audio: crear job de transcripcion o resumen, no mezclar audio crudo con prompt principal.
- Documentos: extraer texto en proceso separado, con limite de tamano y sin ejecutar macros.

## observability

Crear `telegram_bridge/runs/*.json` o tabla `runs` con:

```json
{
  "job_id": "20260525T084316-example",
  "event_id": "evt_...",
  "front": "CODEX-OPS",
  "status": "queued",
  "created_at": "2026-05-25T08:52:07-03:00",
  "heartbeat_at": "2026-05-25T08:52:07-03:00",
  "last_ack_at": null,
  "blocked_reason": null,
  "error_code": null,
  "result_ref": null
}
```

Errores tipicos:

- `unknown_topic`
- `duplicate_event`
- `album_incomplete`
- `attachment_too_large`
- `audio_transcription_failed`
- `prompt_injection_detected`
- `job_write_failed`
- `ack_send_failed`

## tests

```bash
python3 -m pytest telegram_bridge/tests/test_router_idempotency.py
python3 -m pytest telegram_bridge/tests/test_topic_mapping.py
python3 -m pytest telegram_bridge/tests/test_albums_attachments_audio.py
python3 -m pytest telegram_bridge/tests/test_prompt_injection_boundaries.py
python3 -m pytest telegram_bridge/tests/test_ack_policy.py
python3 scripts/secret_scan.py
```

Casos obligatorios:

- Mensaje duplicado exacto no duplica job.
- Topic `clinica` routea a CLINICA.
- Topic desconocido routea a UNKNOWN_REVIEW.
- Prompt injection en texto de Telegram queda como contenido no confiable.
- Album de 4 imagenes crea un solo job.
- Audio crea job de transcripcion separado.
- ACK `queued` se envia una sola vez.
- Error de ACK no pierde job.

## criterios de verificacion

- Todo evento entrante queda registrado antes de cualquier decision.
- Ningun evento crudo se convierte en instruccion de sistema.
- Cada job tiene `event_id`, `front`, `topic_id`, `idempotency_key` y `trust_level`.
- El dashboard puede leer runs y mostrar queued/running/blocked/done.
- El router se puede probar entero con fixtures sin credenciales reales.

## recommendation

Construir primero el MVP con fixtures locales y sin bot real. Recien cuando pasen idempotencia, topic mapping y ACK policy, conectar Telegram real desde work-mac con credenciales fuera del repo.

## confidence

High. La propuesta previa cubre la arquitectura base; este MVP agrega limites operativos, observability y pruebas concretas.

## evidence_paths

- `decisions/telegram_router_patch_proposal_v1.md`
- `jobs/20260525T084316-telegram-codex-direct-router-observability-mvp-v2.md`

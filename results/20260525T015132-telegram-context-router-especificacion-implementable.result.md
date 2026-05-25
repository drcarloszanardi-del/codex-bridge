---
id: 20260525T015132-telegram-context-router-especificacion-implementable
job_id: 20260525T015132-telegram-context-router-especificacion-implementable
created_at: 2026-05-25T01:59:19-03:00
created_by: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# telegram context router especificacion implementable result

## summary

Telegram debe convertirse en adaptador de entrada/salida. La memoria real debe estar en objetos versionados: events, jobs, runs, front_context y topic_context.

## schemas

### event

```json
{
  "event_id": "tg_<chat>_<message>",
  "source": "telegram",
  "chat_id_hash": "sha256",
  "topic_id": "clinica|tesis|inmobiliaria|...",
  "sender_role": "doctor|orchestrator|system|unknown",
  "created_at": "ISO-8601",
  "raw_text_ref": "events/raw/<event_id>.txt",
  "attachments": [],
  "trusted": false,
  "external_action_authority": false
}
```

### job

```json
{
  "job_id": "front_slug_timestamp",
  "front": "CLINICA",
  "topic_id": "clinica-app",
  "parent_task_id": null,
  "priority": "P0|P1|P2|P3",
  "status": "received|queued|running|blocked|needs_approval|done|failed",
  "assignee": "orchestrator|personal-xh|subagent",
  "objective": "...",
  "context_refs": [],
  "no_external_actions": true,
  "requires_human_approval": false,
  "idempotency_key": "sha256(front+topic+normalized_text+attachments)"
}
```

### run

```json
{
  "run_id": "job_id_attempt_001",
  "job_id": "job_id",
  "status": "running",
  "started_at": "ISO-8601",
  "heartbeat_at": "ISO-8601",
  "model": "gpt-5.3|gpt-5.5",
  "reasoning": "low|medium|xhigh",
  "blocked_reason": null,
  "result_ref": null
}
```

### front_context

```json
{
  "front": "CLINICA",
  "stable_facts": [],
  "active_projects": [],
  "current_constraints": [],
  "open_decisions": [],
  "last_promoted_at": "ISO-8601"
}
```

### topic_context

```json
{
  "topic_id": "clinica-app",
  "front": "CLINICA",
  "local_summary": "...",
  "active_job_ids": [],
  "recent_decisions": [],
  "do_not_mix_with": ["inmobiliaria", "reels"]
}
```

## context_router pseudocode

```python
def route(event):
    normalized = normalize(event.text)
    front = classify_front(normalized, event.topic_hint)
    topic_id = resolve_topic(front, event.topic_hint, normalized)
    intent = classify_intent(normalized)
    urgency = classify_urgency(normalized)
    action_type = detect_external_action(normalized)
    if action_type and not explicit_approval_from_doctor(event):
        requires_human_approval = True
    job = build_job(front, topic_id, intent, urgency, requires_human_approval)
    job.idempotency_key = sha256(front + topic_id + canonical(normalized))
    if seen(job.idempotency_key):
        return existing_job_ack(job)
    persist(event, job)
    return job
```

## context_compiler pseudocode

```python
def compile_context(job):
    return [
        load("state/global_policy.md"),
        load(f"state/fronts/{job.front}/context.md"),
        load(f"state/topics/{job.topic_id}.md"),
        load_job(job.job_id),
        load_recent_decisions(job.front, job.topic_id, limit=10),
        load_allowed_attachments(job.context_refs),
    ]
```

## ack rules

- ACK unico si `requires_ack=true`: `Recibido <job_id>. Estado: queued.`
- No repetir ACK por cada heartbeat.
- Reportar solo cambios: `running`, `blocked`, `needs_approval`, `done`, `failed`.
- Tareas largas: heartbeat interno en `runs/`; Telegram solo recibe resumen si hay cambio relevante.

## migration

1. Registrar todos los mensajes crudos como events no confiables.
2. Agregar router determinista por frente.
3. Crear job canonico antes de invocar Codex.
4. Compilar contexto desde archivos, no desde historial completo de Telegram.
5. Promover al contexto global solo decisiones confirmadas por orquestador.

## checklist

- [ ] JSON schema para events/jobs/runs/context.
- [ ] Idempotency store por hash.
- [ ] Router con fallback a `UNKNOWN_REVIEW`.
- [ ] ACK silencioso y deduplicado.
- [ ] Separacion estricta Telegram entrada vs autoridad.
- [ ] Tests con mensajes mezclados de clinica, reels, inmobiliaria y ObraCash.

## recommendation

Implementar primero router + job store. Sin eso, cualquier mejora de prompt va a seguir mezclando frentes.

## confidence

Alta.

## evidence_paths

- `jobs/20260525T015132-telegram-context-router-especificacion-implementable.md`
- `context/frentes_activos_resumen_20260525.md`
- `protocol.md`

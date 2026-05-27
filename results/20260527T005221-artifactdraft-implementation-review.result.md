---
job_id: 20260527T005221-artifactdraft-implementation-review
worker: personal-xh
status: completed
completed_at: 2026-05-27T01:14:00-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - ArtifactDraft implementation review

## summary honesto

ArtifactDraft debe implementarse filesystem-first: manifest JSON, carpetas
predecibles y validador local antes de tocar el router real. Debe ser obligatorio
solo para respuestas largas de Telegram, Reels CMP y Presentaciones; no para
heartbeats, healthchecks ni estados simples.

Evidencia: los tres frentes piden separar brief, contexto, assets, QA y entrega.
Inferencia: la primera version debe cortar el problema de "borrador tratado como
final". Opinion: dashboard y automatizacion externa pueden esperar.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T005221-artifactdraft-implementation-review.md` | Revisada | Entregables y restricciones. |
| `context/fronts/telegram.md` | Revisada | Brief operativo, ContextBinder, ResetScope y deuda ArtifactDraft. |
| `context/fronts/reels_cmp.md` | Revisada | Separacion guion/storyboard/assets/caption/QA. |
| `context/fronts/presentaciones.md` | Revisada | Deck editable y render QA. |
| `results/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.result.md` | Revisada | Schema y flows iniciales. |
| `results/20260526T064631-artifactdraft-implementation-review.result.md` | Revisada | Implementacion minima y tests. |

## schema

```json
{
  "artifact_id": "YYYYMMDDTHHMMSS-front-slug",
  "front": "telegram|reels_cmp|presentaciones",
  "job_id": "string",
  "status": "draft|review|ready_for_orchestrator|delivered|rejected",
  "source_event": {
    "channel": "telegram|bridge|manual",
    "message_ids": [],
    "raw_paths": []
  },
  "brief_path": "brief.md",
  "context_refs": [],
  "drafts": [{"version": 1, "path": "drafts/v1.md", "status": "draft"}],
  "assets": {"required": [], "approved": [], "rejected": []},
  "qa": {"status": "pending|pass|fail", "report_path": "qa/qa_report.md"},
  "delivery": {
    "status": "not_sent|ready_for_orchestrator|sent_by_orchestrator",
    "final_path": null,
    "external_action_required": false
  }
}
```

## paths

```text
artifacts/
  telegram/<artifact_id>/
    artifact.json
    raw/
    brief.md
    context_refs.md
    drafts/v1.md
    qa/qa_report.md
    final/
  reels_cmp/<artifact_id>/
    artifact.json
    guion.md
    storyboard.md
    asset_request.md
    caption.md
    qa/visual_truth_gate.md
    final/
  presentaciones/<artifact_id>/
    artifact.json
    brief.yaml
    outline.md
    storyboard.md
    deck_plan.md
    qa/render_qa.md
    final/
```

## router_changes

1. Crear artifact despues de route/brief y antes del model call largo.
2. Adjuntar `artifact_id` a job/run/result.
3. Permitir bypass explicito para respuesta simple: `artifact_required=false`.
4. Exigir artifact en Telegram largo/con adjuntos, Reels CMP y Presentaciones.
5. No permitir envio externo/publicable salvo `delivery.status=ready_for_orchestrator`.

## migration_plan

1. Crear `scripts/artifacts/new_artifact.py`.
2. Crear `scripts/artifacts/validate_artifact.py`.
3. Agregar carpetas base con `.gitkeep`.
4. Integrar primero en jobs del bridge, sin tocar Telegram real.
5. Activar por feature flag en Telegram largo/adjuntos.
6. Activar en Reels y Presentaciones como pre-entrega.
7. Recien despues listar artifacts en dashboard.

## tests

- `test_new_artifact_creates_required_files`
- `test_validate_artifact_fails_without_brief`
- `test_validate_artifact_fails_without_context_refs`
- `test_validate_artifact_fails_if_internal_notes_in_final`
- `test_reels_artifact_requires_visual_truth_qa`
- `test_presentation_artifact_requires_render_qa`
- `test_telegram_long_response_requires_artifact`
- `test_simple_healthcheck_can_bypass_artifact`
- `test_delivery_requires_ready_for_orchestrator`

## risks / limits

- Si se versionan binarios pesados en Git, el repo crece; usar manifests y rutas locales.
- Si todo requiere artifact, el sistema se vuelve lento; aplicar por tipo de trabajo.
- Notas internas no deben entrar a `final/`.
- No se modifico router real; esto es especificacion de implementacion.

## recommendation

Implementar helpers y validador local primero. Activar solo para Telegram
largo/con adjuntos, Reels CMP y Presentaciones. Dashboard despues.

## confidence

Alta para schema, paths y tests; media para puntos exactos del router hasta portarlo.

## evidence_paths

- `jobs/20260527T005221-artifactdraft-implementation-review.md`
- `context/fronts/telegram.md`
- `context/fronts/reels_cmp.md`
- `context/fronts/presentaciones.md`
- `results/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.result.md`
- `results/20260526T064631-artifactdraft-implementation-review.result.md`

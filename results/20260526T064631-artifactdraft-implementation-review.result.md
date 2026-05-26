# Resultado - 20260526T064631-artifactdraft-implementation-review

## summary honesto

`ArtifactDraft` queda listo para implementarse como capa local entre conversacion y entrega final. No debe aplicarse a healthchecks simples; si a respuestas largas de Telegram, reels CMP y presentaciones.

**Evidencia:** los frentes Telegram, Reels y Presentaciones ya piden separar brief/contexto/assets/QA/entrega. El resultado previo define schema, flows y QA.

**Inferencia:** la implementacion minima debe ser filesystem-first: JSON manifest + carpetas + validador, antes de tocar dashboards.

**Opinion:** empezar acotado evita sobreingenieria y corta el bug de "contestar/publicar algo que todavia era borrador".

## coverage_table

| fuente | uso | limite |
| --- | --- | --- |
| `context/fronts/telegram.md` | Brief operativo, ContextBinder, deuda ArtifactDraft. | No modifica router. |
| `context/fronts/reels_cmp.md` | Separar guion/storyboard/assets/caption/QA. | No trae assets. |
| `context/fronts/presentaciones.md` | Pipeline deck editable y QA render. | No crea PPTX. |
| `results/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.result.md` | Schema, paths, flows y QA contract. | Requiere port a repo real. |

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
  "delivery": {"status": "not_sent|ready_for_orchestrator|sent_by_orchestrator", "final_path": null}
}
```

## paths

```text
artifacts/
  telegram/<artifact_id>/
  reels_cmp/<artifact_id>/
  presentaciones/<artifact_id>/
```

Archivos minimos por artifact:

```text
artifact.json
brief.md
context_refs.md
drafts/v1.md
assets/requested.md
qa/qa_report.md
final/
```

## router_changes

1. Crear artifact despues de route/brief, antes del model call largo.
2. Adjuntar `artifact_id` al job/run/result.
3. Para respuestas simples, permitir bypass con `artifact_required=false`.
4. Para Telegram largo, Reels y Presentaciones, exigir artifact antes de entrega.
5. Todo envio externo/publicable debe salir solo si `delivery.status=ready_for_orchestrator`.

## migration_plan

1. Agregar `scripts/artifacts/new_artifact.py`.
2. Agregar `scripts/artifacts/validate_artifact.py`.
3. Crear `.gitkeep` y folders base.
4. Integrar primero en jobs bridge, sin tocar Telegram real.
5. Activar en Telegram solo para respuestas largas o con adjuntos.
6. Activar en Reels/Presentaciones como pre-entrega.
7. Agregar dashboard o listado despues de estabilizar filesystem.

## tests

- `test_new_artifact_creates_required_files`.
- `test_validate_artifact_fails_without_brief`.
- `test_validate_artifact_fails_if_internal_notes_in_final`.
- `test_reels_artifact_requires_visual_truth_qa`.
- `test_presentation_artifact_requires_render_qa`.
- `test_telegram_long_response_requires_artifact`.
- `test_simple_healthcheck_can_bypass_artifact`.
- `test_delivery_requires_ready_for_orchestrator`.

## risks_limits

- Si se versionan binarios pesados en Git, crece el repo; usar manifests y rutas locales.
- Si todo requiere artifact, el sistema se vuelve lento; aplicar por tipo de trabajo.
- Notas internas deben quedar fuera de `final/`.

## recommendation

Implementar primero helpers y validador local. Activarlo solo para tres rutas: Telegram largo/con adjuntos, Reels CMP y Presentaciones. No hacerlo obligatorio para heartbeats, healthchecks o respuestas de estado.

## confidence

Alta para schema/paths/tests; media para puntos exactos del router hasta portarlo.

## evidence_paths

- `jobs/20260526T064631-artifactdraft-implementation-review.md`
- `context/fronts/telegram.md`
- `context/fronts/reels_cmp.md`
- `context/fronts/presentaciones.md`
- `results/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.result.md`

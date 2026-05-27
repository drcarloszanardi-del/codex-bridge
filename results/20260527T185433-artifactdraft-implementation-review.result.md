---
job_id: 20260527T185433-artifactdraft-implementation-review
worker: personal-xh
status: completed
completed_at: 2026-05-27T18:55:44-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - ArtifactDraft implementacion acotada

## summary honesto

ArtifactDraft conviene implementarlo como una capa local, versionada y validable
entre la conversacion y la entrega final. El objetivo no es crear otro sistema
pesado: es impedir que Telegram, Reels CMP y Presentaciones mezclen orden cruda,
borrador, assets, QA y salida publicable.

Separacion pedida:

- Evidencia: `context/fronts/telegram.md` ya marca ArtifactDraft como deuda
  activa; `context/fronts/reels_cmp.md` exige separar guion, storyboard, assets,
  caption y QA; `context/fronts/presentaciones.md` exige deck editable y render
  QA.
- Inferencia: la primera implementacion debe ser filesystem-first y opt-in por
  tipo de trabajo, no obligatoria para healthchecks o respuestas simples.
- Opinion: el dashboard puede esperar; primero hacen falta manifest, validador y
  feature flag.

No use acciones externas, no toque Telegram real, no toque credenciales y no
modifique el router real desde este worker.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T185433-artifactdraft-implementation-review.md` | Revisada | Secciones requeridas, restricciones y criterio de terminado. |
| `context/fronts/telegram.md` | Revisada | Brief operativo, ContextBinder, ResetScope y deuda ArtifactDraft. |
| `context/fronts/reels_cmp.md` | Revisada | Separacion de guion/storyboard/assets/caption/QA y visual truth gate. |
| `context/fronts/presentaciones.md` | Revisada | Pipeline objetivo -> narrativa -> storyboard -> deck editable -> QA. |
| `results/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.result.md` | Revisada | Schema base, flows y contrato QA. |
| `results/20260527T005221-artifactdraft-implementation-review.result.md` | Revisada como antecedente | Implementacion filesystem-first, paths y tests minimos. |

## schema

Schema minimo para `artifact.json`:

```json
{
  "artifact_id": "YYYYMMDDTHHMMSS-front-slug",
  "created_at": "ISO-8601",
  "front": "telegram|reels_cmp|presentaciones",
  "job_id": "string|null",
  "status": "draft|review|ready_for_orchestrator|delivered|rejected",
  "source_event": {
    "channel": "telegram|bridge|manual",
    "message_ids": [],
    "raw_paths": [],
    "attachments": []
  },
  "brief": {
    "path": "brief.md",
    "objective": "",
    "audience": "",
    "allowed_actions": [],
    "forbidden_actions": [],
    "expected_output": ""
  },
  "context_refs": [],
  "drafts": [
    {"version": 1, "path": "drafts/v1.md", "status": "draft"}
  ],
  "assets": {
    "manifest_path": "assets/assets_manifest.json",
    "approved": [],
    "rejected": []
  },
  "qa": {
    "status": "pending|pass|fail",
    "report_path": "qa/qa_report.md",
    "required_checks": []
  },
  "delivery": {
    "status": "not_sent|ready_for_orchestrator|sent_by_orchestrator",
    "final_path": null,
    "external_action_required": false
  }
}
```

Reglas:

- `delivery.status=sent_by_orchestrator` solo puede setearlo el principal.
- `ready_for_orchestrator` exige `qa.status=pass`.
- `final/` no puede contener notas internas, diffs crudos ni placeholders.
- Reels y Presentaciones tienen checks obligatorios adicionales.

## paths

```text
artifacts/
  telegram/<artifact_id>/
    artifact.json
    raw/
    brief.md
    context_refs.md
    drafts/
      v1.md
      v2.md
    qa/
      qa_report.md
      quality_score.json
    final/
  reels_cmp/<artifact_id>/
    artifact.json
    raw/
    guion.md
    storyboard.md
    asset_request.md
    caption.md
    assets/
      assets_manifest.json
      approved/
      rejected/
    qa/
      visual_truth_gate.md
    final/
  presentaciones/<artifact_id>/
    artifact.json
    brief.yaml
    outline.md
    storyboard.md
    deck_plan.md
    sources_manifest.json
    qa/
      render_qa.md
      source_traceability.md
    final/
```

Binarios pesados: guardar manifest y ruta local, no versionar videos o assets
grandes por defecto.

## router_changes

1. Crear ArtifactDraft despues de route/brief/context y antes de llamadas largas
   al modelo.
2. Adjuntar `artifact_id` a job, run, logs y result.
3. Usar feature flag: `ARTIFACT_DRAFT_REQUIRED_FOR=telegram_long,reels_cmp,presentaciones`.
4. Bypass permitido para healthchecks, ACKs simples, disponibilidad e informes
   cortos sin adjuntos.
5. Telegram largo/con adjuntos: guardar raw events, cerrar media buffer, crear
   brief y recien despues draft.
6. Reels CMP: no permitir paquete final sin `qa/visual_truth_gate.md`.
7. Presentaciones: no permitir entrega sin `qa/render_qa.md` y trazabilidad de
   fuentes.
8. El router nunca debe enviar `drafts/` al usuario; solo `final/` aprobado por
   el principal.

## migration_plan

1. Crear `scripts/artifacts/new_artifact.py --front --slug --job-id`.
2. Crear `scripts/artifacts/validate_artifact.py <artifact_dir>`.
3. Agregar `.gitkeep` en `artifacts/telegram`, `artifacts/reels_cmp` y
   `artifacts/presentaciones`.
4. Ejecutar primero en modo bridge/local: crear artifacts para jobs, sin tocar
   Telegram real.
5. Activar feature flag para Telegram largo o con adjuntos.
6. Activar para Reels CMP antes de caption/final.
7. Activar para Presentaciones antes de PPTX/export.
8. Agregar vista de dashboard cuando ya existan artifacts reales.

## tests

Tests minimos:

- `test_new_artifact_creates_manifest_and_required_dirs`
- `test_validate_artifact_fails_without_brief`
- `test_validate_artifact_fails_without_context_refs`
- `test_validate_artifact_fails_if_final_contains_internal_notes`
- `test_telegram_long_response_requires_artifact`
- `test_simple_healthcheck_can_bypass_artifact`
- `test_reels_requires_visual_truth_gate`
- `test_presentacion_requires_render_qa`
- `test_delivery_ready_requires_qa_pass`
- `test_sent_by_orchestrator_cannot_be_set_by_worker`

Fixture de integracion:

```yaml
case: telegram_album_long_response
input:
  route: REELS
  media_count: 3
  response_kind: long_creative
expected:
  artifact_created: true
  raw_saved: true
  qa_status: pending
  delivery_status: not_sent
```

## risks / limits

- Si todo requiere ArtifactDraft, el sistema se vuelve lento; aplicar solo a
  trabajos largos, creativos o sensibles.
- Si se versionan binarios pesados, el repo crece; usar manifests y rutas.
- Si `final/` no se valida, pueden filtrarse notas internas.
- No se inspecciono ni modifico el router real; esto queda como especificacion
  implementable por Codex principal.
- Ruta alternativa si no se implementa el helper aun: crear artifacts manuales
  con `artifact.json`, `brief.md`, `drafts/v1.md` y `qa/qa_report.md`.

## recommendation

Implementar primero helpers y validador local, luego activar por feature flag
solo para Telegram largo/con adjuntos, Reels CMP y Presentaciones. No bloquear
respuestas simples ni healthchecks. El primer gate bloqueante debe ser: ninguna
salida publicable desde `drafts/`; solo `final/` con `qa.status=pass`.

## confidence

Alta para schema, paths, tests y plan de migracion porque derivan de los frentes
canonicos y resultados previos. Media para los puntos exactos del router hasta
que Codex principal lo porte al codigo real.

## evidence_paths

- `jobs/20260527T185433-artifactdraft-implementation-review.md`
- `context/fronts/telegram.md`
- `context/fronts/reels_cmp.md`
- `context/fronts/presentaciones.md`
- `results/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.result.md`
- `results/20260527T005221-artifactdraft-implementation-review.result.md`
- `claims/20260527T185433-artifactdraft-implementation-review.json`

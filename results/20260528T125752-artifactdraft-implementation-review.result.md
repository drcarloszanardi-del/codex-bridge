---
job_id: 20260528T125752-artifactdraft-implementation-review
worker: personal-xh
status: completed
completed_at: 2026-05-28T12:59:48-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - ArtifactDraft implementation review

## summary honesto

`ArtifactDraft` ya esta conceptualmente bien definido; lo que falta es convertirlo en una especificacion chica, implementable y no invasiva. La primera version debe crear artefactos locales versionados para Telegram Directo, Reels CMP y Presentaciones, con un schema comun, rutas claras, router changes minimos, migracion gradual y tests que impidan mezclar conversacion, borrador, QA y entrega final.

## coverage_table

| Requisito | Estado | Evidencia |
|---|---|---|
| `schema` | cubierto | Resultado ArtifactDraft previo y necesidades de tres frentes. |
| `paths` | cubierto | Layout por `artifacts/<front>/<artifact_id>/`. |
| `router_changes` | cubierto | ContextBinder/BriefCompiler en Telegram y gates de Reels/Presentaciones. |
| `migration_plan` | cubierto | Activacion por caso de uso, no por healthchecks simples. |
| `tests` | cubierto | Fixtures unitarios y contract tests por frente. |

## evidencia

- `results/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.result.md` define schema, folder layout y flows para Telegram/Reels/Presentaciones.
- `context/fronts/telegram.md` confirma Brief operativo, ContextBinder, ResetScope y deuda activa de ArtifactDraft/ResultContract.
- `context/fronts/reels_cmp.md` exige separar guion, storyboard, assets, caption y QA antes de pieza publica.
- `context/fronts/presentaciones.md` exige pipeline objetivo, narrativa, storyboard, visuales, deck editable, QA visual y export.

## inferencia

- La implementacion debe ser append-only/local al principio: crear artefactos y validar contratos sin cambiar todavia la entrega real.
- El router de Telegram solo debe generar ArtifactDraft para respuestas largas, creativas, con adjuntos o potencialmente sensibles.
- Reels y Presentaciones pueden adoptar el mismo contrato como pre-entrega, sin depender del router Telegram.

## opinion

El punto fino es que ArtifactDraft no sea burocracia. Debe aparecer solo cuando baja riesgo: mensajes largos, assets, claims, material medico, reels o decks. Para respuestas simples, seria peso muerto.

## schema

Schema minimo `artifacts/<front>/<artifact_id>/artifact.json`:

```json
{
  "schema_version": 1,
  "artifact_id": "YYYYMMDDTHHMMSS-front-slug",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "front": "telegram|reels_cmp|presentaciones",
  "status": "draft|qa_pending|ready_for_orchestrator|blocked|archived",
  "source_event": {
    "channel": "telegram|bridge|manual",
    "job_id": "",
    "chat_id_hash": "",
    "message_ids": [],
    "raw_paths": []
  },
  "permissions": {
    "external_actions_allowed": false,
    "contains_sensitive_data": false,
    "requires_orchestrator_delivery": true
  },
  "brief": {
    "path": "brief.md",
    "objective": "",
    "audience": "",
    "expected_output": "",
    "constraints": []
  },
  "context_refs": [],
  "drafts": [
    {
      "version": 1,
      "path": "drafts/v1.md",
      "status": "draft|reviewed|approved|rejected",
      "notes": ""
    }
  ],
  "assets": {
    "manifest_path": "assets/assets_manifest.json",
    "required": [],
    "approved": [],
    "rejected": []
  },
  "qa": {
    "status": "pending|pass|fail",
    "checks": [],
    "report_path": "qa/qa_report.md"
  },
  "delivery": {
    "status": "not_sent|ready_for_orchestrator|sent_by_orchestrator",
    "final_path": "final/final.md",
    "message_id": "",
    "export_paths": []
  }
}
```

Reglas:

- `delivery.status=sent_by_orchestrator` no lo marca un worker.
- `message_id` solo existe si la entrega real fue confirmada por el principal.
- Notas internas van fuera de `final/`.
- Claims y assets sensibles deben bloquear QA si no estan anonimizados.

## paths

```text
artifacts/
  telegram/
    <artifact_id>/
      artifact.json
      raw/
      brief.md
      context_refs.md
      drafts/
        v1.md
      qa/
        qa_report.md
        result_contract.md
      final/
        final.md
  reels_cmp/
    <artifact_id>/
      artifact.json
      brief.md
      guion.md
      storyboard.md
      caption.md
      assets/
        assets_manifest.json
        approved/
        rejected/
      qa/
        visual_truth_gate.md
      final/
  presentaciones/
    <artifact_id>/
      artifact.json
      00_brief/brief.yaml
      01_sources/source_manifest.json
      02_narrative/outline.md
      03_storyboard/storyboard.md
      04_visual_direction/visual_direction.md
      05_assets/assets_manifest.json
      06_deck/
      07_render/
      08_qa/qa_report.md
      09_exports/
```

Helper sugerido:

```text
scripts/artifacts/new_artifact.py --front telegram --job-id <id> --slug <slug>
scripts/artifacts/validate_artifact.py artifacts/<front>/<artifact_id>/artifact.json
```

## router_changes

Telegram Directo:

1. Despues de `BriefCompiler` y `ContextBinder`, clasificar si requiere ArtifactDraft.
2. Triggers: respuesta larga, adjuntos, pedido creativo, material medico/legal, publicable, requiere QA o requiere accion externa.
3. Crear artifact local con raw/event refs.
4. Worker escribe `drafts/v1.md` y `qa/`.
5. Router no envia `drafts/`; solo puede enviar `final/final.md` cuando `delivery.status=ready_for_orchestrator` y el principal confirme.
6. Si hay accion externa, queda en `ready_for_orchestrator`, no se ejecuta desde worker.

Reels CMP:

1. Intake crea artifact si hay reel/caption/asset plan.
2. `visual_truth_gate.md` bloquea errores de contacto, placeholders, anatomia falsa o falta de material propio.
3. Render/publicacion solo sale de `final/` o paquete aprobado.

Presentaciones:

1. Toda presentacion medica crea artifact si requiere deck editable.
2. `source_manifest.json`, `storyboard.md`, render/contact sheet y `qa_report.md` son gates.
3. Export PDF/video es derivado, no fuente de verdad.

## migration_plan

| Fase | Alcance | Criterio de salida |
|---|---|---|
| 0 | Solo spec y carpetas `.gitkeep` si hace falta. | No cambia comportamiento real. |
| 1 | Helper `new_artifact.py` y `validate_artifact.py`. | Puede crear y validar artifact minimo de los tres frentes. |
| 2 | Integracion Telegram en modo shadow: crea artifact, pero no bloquea entrega. | 5 casos reales/sinteticos con artifact valido. |
| 3 | Gate obligatorio para Telegram largo/creativo y Reels CMP. | Router no envia borradores ni notas internas. |
| 4 | Presentaciones adopta layout completo. | Deck piloto con render QA y source traceability. |
| 5 | Dashboard lista artifacts por estado. | Operador ve `draft`, `qa_pending`, `ready`, `blocked`. |

Ruta alternativa si no se puede tocar router: usar ArtifactDraft como paquete manual por job en bridge y validar con script antes de entrega.

## tests

Unitarios de schema:

- Crea artifact minimo valido para `telegram`, `reels_cmp`, `presentaciones`.
- Falla si `front` no pertenece al enum.
- Falla si `delivery.status=sent_by_orchestrator` no tiene `message_id`.
- Falla si `external_actions_allowed=true` en worker.
- Falla si `qa.status=pass` sin `qa_report.md`.

Tests Telegram:

- Mensaje corto simple no crea ArtifactDraft.
- Mensaje largo con adjunto crea artifact despues de BriefCompiler/ContextBinder.
- Draft no se envia aunque exista `drafts/v1.md`.
- Final con accion externa queda `ready_for_orchestrator`.
- Evento con late media mantiene raw refs agrupadas.

Tests Reels CMP:

- Falla si falta telefono `2364384321` cuando hay cierre/contacto.
- Falla si `visual_truth_gate.md` no existe.
- Falla si assets contienen placeholder o anatomia generada como evidencia clinica.

Tests Presentaciones:

- Falla si falta `source_manifest.json` en deck medico.
- Falla si no existe render/contact sheet antes de entrega.
- Falla si deck final no esta en carpeta editable o si solo hay PDF.

## risks / limits

- Si ArtifactDraft se vuelve obligatorio para todo, ralentiza operaciones simples.
- Si el router confunde `draft` con `final`, aumenta riesgo de publicar notas internas.
- Si los assets pesados entran al repo, el bridge puede crecer demasiado; usar manifests y rutas.
- No se inspecciono el router real, asi que los nombres de hooks son especificacion, no patch aplicado.
- Ruta alternativa: validar ArtifactDraft en bridge antes de integrarlo en runtime Telegram.

## recommendation

Implementar primero `scripts/artifacts/new_artifact.py` y `validate_artifact.py`, luego activar modo shadow en Telegram largo/creativo. La primera integracion obligatoria deberia ser Reels CMP, porque su gate visual es claro y de alto impacto.

## confidence

Alta para schema, paths y tests por apoyo en frentes locales. Media para router changes porque no se leyo el codigo runtime real desde este job.

## evidence_paths

- `jobs/20260528T125752-artifactdraft-implementation-review.md`
- `results/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.result.md`
- `context/fronts/telegram.md`
- `context/fronts/reels_cmp.md`
- `context/fronts/presentaciones.md`

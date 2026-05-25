# Resultado - ArtifactDraft Telegram/Reels/Presentaciones v1

Job: `20260525T122121-artifactdraft-telegram-reels-presentaciones-v1`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

`ArtifactDraft` debe ser una capa local versionada entre la conversacion y la entrega final. Evita que Telegram, reels o presentaciones mezclen orden cruda, razonamiento, borrador, assets y salida publicable. No se toca Telegram real ni se publica nada; se entrega schema, paths, flows y QA.

## coverage_table

| Fuente | Estado | Uso |
|---|---|---|
| `jobs/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.md` | revisado | Contrato y frentes. |
| `context/fronts/telegram.md` | revisado | Brief operativo, ContextBinder, ResetScope, deuda ArtifactDraft. |
| `context/fronts/reels_cmp.md` | revisado | Separar guion/storyboard/assets/caption/QA. |
| `context/fronts/presentaciones.md` | revisado | Pipeline objetivo -> narrativa -> storyboard -> deck editable -> QA. |
| `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md` | revisado | Patron conversacion/artefacto/entrega. |

## artifact_schema

```json
{
  "artifact_id": "YYYYMMDDTHHMMSS-front-slug",
  "created_at": "ISO-8601",
  "front": "telegram|reels_cmp|presentaciones",
  "source_event": {
    "channel": "telegram|bridge|manual",
    "message_ids": [],
    "job_id": "",
    "raw_paths": []
  },
  "brief": {
    "objective": "",
    "audience": "",
    "constraints": [],
    "allowed_actions": [],
    "forbidden_actions": [],
    "expected_output": ""
  },
  "context_refs": [],
  "reasoning_notes_private_path": "notes/internal.md",
  "drafts": [
    {
      "version": 1,
      "path": "drafts/v1.md",
      "status": "draft|reviewed|approved|rejected",
      "changes": ""
    }
  ],
  "asset_plan": {
    "required": [],
    "optional": [],
    "generated": [],
    "rejected": []
  },
  "qa": {
    "checks": [],
    "status": "pending|pass|fail",
    "report_path": "qa/qa_report.md"
  },
  "delivery": {
    "status": "not_sent|ready_for_orchestrator|sent_by_orchestrator",
    "final_path": "",
    "external_action_required": false
  }
}
```

## folder_layout

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
        v2.md
      assets/
        requested.md
        generated/
        approved/
        rejected/
      qa/
        qa_report.md
      final/
  reels_cmp/
    <artifact_id>/
      guion.md
      storyboard.md
      caption.md
      asset_request.md
      qa/visual_truth_gate.md
  presentaciones/
    <artifact_id>/
      outline.md
      storyboard.md
      deck_plan.md
      qa/render_qa.md
```

## telegram_flow

1. Router recibe mensaje/audio/album y lo guarda en `raw/`.
2. `BriefCompiler` crea `brief.md`.
3. `ContextBinder` adjunta frente y decisiones relevantes.
4. Se crea `artifact.json` con status `draft`.
5. Worker genera `drafts/v1.md`.
6. QA valida: permisos, datos sensibles, ResultContract.
7. Si requiere accion externa, queda `ready_for_orchestrator`, no se envia automaticamente.
8. Codex principal decide entrega/respuesta.

## reels_flow

1. Intake de assets no sensibles.
2. `guion.md` separado de `storyboard.md`.
3. `asset_request.md` lista obligatorio/deseable/opcional.
4. `caption.md` separado.
5. `qa/visual_truth_gate.md`: contacto, claims, datos CMP, privacidad, musica/licencia.
6. Final queda como paquete editable para el editor/orquestador.

## presentations_flow

1. `brief.yaml` con audiencia, objetivo, duracion, decision esperada.
2. `outline.md` para narrativa.
3. `storyboard.md` slide por slide.
4. `deck_plan.md` con visuales y fuentes.
5. PPTX editable se genera por herramienta autorizada.
6. `qa/render_qa.md` antes de entregar.
7. Export PDF/video solo si se pide.

## qa_contract

| Gate | Debe pasar |
|---|---|
| Permisos | No acciones externas salvo orquestador. |
| Privacidad | No pacientes/datos sensibles visibles. |
| Evidencia | `context_refs` y `evidence_paths` concretos. |
| Draft separation | No mezclar notas internas con entrega final. |
| Reels CMP | Telefono `2364384321`, IG `@drcarloszanardi`, web correcta. |
| Presentaciones | Render sin solapes, deck editable, fuentes trazables. |
| Telegram | `ok=true` y `message_id` real solo cuando envio lo hace principal. |

## implementation_steps

1. Crear `artifacts/.gitkeep` y subcarpetas por frente.
2. Agregar helper `scripts/artifacts/new_artifact.py --front --job-id --slug`.
3. Agregar `scripts/artifacts/validate_artifact.py`.
4. Integrar en Telegram router despues de `BriefCompiler`.
5. Integrar en Reels y Presentaciones como pre-entrega obligatoria.
6. Dashboard: mostrar artifacts `draft/review/ready`.
7. Worker solo escribe drafts/qa; orquestador entrega o publica.

## risks / limits

- Si se versionan assets pesados en Git, el repo puede crecer; usar manifests y rutas locales para binarios grandes.
- Notas internas no deben terminar en final/publico.
- La separacion agrega pasos; se justifica solo en trabajos largos, creativos o sensibles.
- No se modifico app/router real desde este worker.

## recommendation

Implementar `ArtifactDraft` primero para tres casos: respuesta larga Telegram, reel CMP y deck medico. No hacerlo obligatorio para healthchecks simples. El principal debe tratar `delivery.status=ready_for_orchestrator` como unica salida publicable.

## confidence

Alta para schema/flows/QA. Media para detalles de integracion en router real porque la app de Telegram no fue modificada desde este worker.

## evidence_paths

- `jobs/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.md`
- `context/fronts/telegram.md`
- `context/fronts/reels_cmp.md`
- `context/fronts/presentaciones.md`
- `results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md`

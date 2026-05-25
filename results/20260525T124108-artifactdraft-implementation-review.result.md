# Resultado - ArtifactDraft implementation review

Job: `20260525T124108-artifactdraft-implementation-review`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

La implementacion debe ser chica: crear schema + helper local + validator, y recien despues conectar al router Telegram. No conviene empezar con dashboard ni migracion masiva. `ArtifactDraft` debe activarse solo para trabajos largos/creativos/sensibles: Telegram con adjuntos, reels CMP y presentaciones.

## coverage_table

| Fuente | Estado | Uso |
|---|---|---|
| `jobs/20260525T124108-artifactdraft-implementation-review.md` | revisado | Contrato del job. |
| `context/fronts/telegram.md` | revisado | Router, BriefCompiler, ContextBinder, ResetScope y deuda ArtifactDraft. |
| `context/fronts/reels_cmp.md` | revisado | Separacion guion/storyboard/assets/caption/QA. |
| `context/fronts/presentaciones.md` | revisado | Pipeline deck editable. |
| `results/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.result.md` | revisado | Schema base, flows y QA contract. |

## schema

Version inicial minima:

```json
{
  "artifact_id": "string",
  "front": "telegram|reels_cmp|presentaciones",
  "created_at": "ISO-8601",
  "source": {
    "job_id": "string",
    "channel": "telegram|bridge|manual",
    "message_ids": [],
    "raw_paths": []
  },
  "brief_path": "brief.md",
  "context_refs_path": "context_refs.md",
  "drafts": [{"version": 1, "path": "drafts/v1.md", "status": "draft"}],
  "qa_path": "qa/qa_report.md",
  "delivery": {
    "status": "not_sent|ready_for_orchestrator|sent_by_orchestrator",
    "final_path": "",
    "external_action_required": false
  }
}
```

## paths

```text
artifacts/
  telegram/<artifact_id>/
  reels_cmp/<artifact_id>/
  presentaciones/<artifact_id>/
scripts/artifacts/new_artifact.py
scripts/artifacts/validate_artifact.py
templates/artifactdraft/
```

No versionar binarios pesados; guardar manifest/ruta local y hash si corresponde.

## router_changes

1. Despues de `BriefCompiler`, decidir si requiere artifact:
   - adjuntos/media;
   - respuesta larga;
   - reel/presentacion;
   - accion externa pendiente;
   - datos sensibles o QA required.
2. Crear artifact local con `new_artifact.py`.
3. Escribir raw paths, brief y context refs.
4. Generar draft en `drafts/v1.md`.
5. Ejecutar `validate_artifact.py`.
6. Si pasa, marcar `ready_for_orchestrator`.
7. Solo Codex principal envia/publica.

## migration_plan

| Paso | Alcance | Riesgo |
|---|---|---|
| 1 | Crear carpetas, template y validator | bajo |
| 2 | Usar manualmente en 1 reel y 1 deck | bajo |
| 3 | Integrar en Telegram para media/adjuntos | medio |
| 4 | Agregar dashboard de artifacts | bajo/medio |
| 5 | Hacer obligatorio para trabajos sensibles | medio |

## tests

| Test | Debe verificar |
|---|---|
| `test_new_artifact_creates_required_files` | `artifact.json`, `brief.md`, `drafts/`, `qa/`. |
| `test_validate_artifact_blocks_missing_final` | No pasar si falta final cuando delivery esta listo. |
| `test_telegram_media_creates_artifact` | Evento con adjuntos no responde directo; crea artifact. |
| `test_reels_requires_visual_truth_gate` | Reel CMP requiere QA contacto/privacidad. |
| `test_presentacion_requires_render_qa` | Deck requiere render/contact sheet. |
| `test_internal_notes_not_in_final` | Notas internas no aparecen en entrega. |

## risks / limits

- Si se aplica a todo, ralentiza tareas simples.
- Si se versionan assets pesados, crece el repo.
- Si el final toma notas internas, puede filtrar razonamiento o datos.
- No se modifico el router real desde este worker.

## recommendation

Implementar primero helper + validator y usarlo manualmente en tres frentes. Integrar al router solo cuando esos artifacts pasen QA. Umbral: obligatorio para adjuntos/media, reels, presentaciones y respuestas largas; no obligatorio para respuestas simples.

## confidence

Alta para schema, paths y tests. Media para detalle exacto del router porque vive en la Mac de trabajo.

## evidence_paths

- `jobs/20260525T124108-artifactdraft-implementation-review.md`
- `context/fronts/telegram.md`
- `context/fronts/reels_cmp.md`
- `context/fronts/presentaciones.md`
- `results/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.result.md`


---
id: 20260525T173727-tesis-empty-template-pack-v1
created_at: 2026-05-25T17:37:27-03:00
created_by: orchestrator
assignee: personal-xh
front: TESIS-PAPERS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: TESIS - pack de plantillas vacías sin tocar borrador

## Objetivo

Crear un pack de plantillas vacías para organizar la tesis sin cargar datos reales ni modificar el borrador base.

## Fuentes permitidas

- `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`

## Entregable esperado

Crear `results/20260525T173727-tesis-empty-template-pack-v1.result.md` con:

- `summary`
- `HANDOFF_md_template`
- `variables_md_template`
- `data_collection_protocol_md_template`
- `data_collection_sheet_csv_header`
- `missing_data_log_csv_header`
- `decision_log_md_template`
- `bibliography_matrix_csv_header`
- `how_orchestrator_should_materialize`
- `risks_limits`
- `confidence`
- `evidence_paths`

## Reglas

- No tocar el borrador base.
- No usar datos de pacientes.
- No inventar bibliografía.
- No abrir Drive/Zotero/iCloud/Photos.
- Mantener todo como plantilla vacía hasta que el Doctor confirme pregunta, unidad de análisis, outcome y rol del video.

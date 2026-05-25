---
id: 20260525T181001-tesis-decision-brief-variable-candidates-v1
created_at: 2026-05-25T18:10:01-03:00
created_by: orchestrator
assignee: personal-xh
front: TESIS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: TESIS - brief de decisiones y variables candidatas sin tocar borrador

## Objetivo

Preparar un brief corto para que Codex principal pueda pedirle al Doctor solo las decisiones inevitables antes de cargar datos o tocar el borrador: pregunta, unidad de analisis, outcome primario y rol del video. Agregar una lista de variables candidatas compatible con las plantillas vacias, sin inventar datos ni bibliografia.

## Fuentes permitidas

- `results/20260525T173727-tesis-empty-template-pack-v1.result.md`
- `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`
- `context/fronts/tesis.md` si existe

## Entregable esperado

Crear `results/20260525T181001-tesis-decision-brief-variable-candidates-v1.result.md` con:

- `summary`
- `four_decisions_for_doctor`
- `recommended_default_options` con pros/cons breves
- `variable_candidates_table`
- `missing_data_policy_draft`
- `video_role_decision_tree`
- `what_not_to_change_in_base_draft`
- `next_safe_actions_for_orchestrator`
- `risks_limits`
- `confidence`
- `evidence_paths`

## Reglas

- No modificar borrador base.
- No cargar datos reales ni sensibles.
- No inventar bibliografia.
- No abrir Drive, iCloud, Photos ni documentos personales.
- No cerrar con "no pude"; si una decision depende del Doctor, formular opcion conservadora y pregunta exacta.

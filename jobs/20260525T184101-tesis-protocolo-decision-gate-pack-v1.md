---
id: 20260525T184101-tesis-protocolo-decision-gate-pack-v1
created_at: 2026-05-25T18:41:01-03:00
created_by: orchestrator
assignee: personal-xh
front: TESIS
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: TESIS - gate metodologico antes de tocar borrador

## Contexto

Codex principal materializo plantillas vacias en tesis y agrego brief de decisiones/variables candidatas sin tocar el borrador base. Ahora hace falta un gate metodologico simple que impida editar la tesis si faltan decisiones o si una variable no tiene definicion operacional.

## Fuentes permitidas

- `results/20260525T181001-tesis-decision-brief-variable-candidates-v1.result.md`
- `results/20260525T173727-tesis-empty-template-pack-v1.result.md`
- `results/20260525T170712-tesis-protocolo-datos-next-actions-v1.result.md`
- `results/20260525T021049-tesis-research-ops-protocol-v1.result.md`

## Entregable esperado

Crear `results/20260525T184101-tesis-protocolo-decision-gate-pack-v1.result.md` con:

- `summary`
- `methodology_gate_contract`
- `required_decisions_checklist`
- `variable_definition_gate`
- `bibliography_entry_gate`
- `video_privacy_gate`
- `draft_base_lock_rules`
- `minimal_validator_pseudocode`
- `telegram_topic_report_format`
- `next_actions_for_orchestrator`
- `confidence`
- `evidence_paths`

## Reglas

- No modificar borrador base.
- No cargar datos reales.
- No inventar bibliografia.
- No abrir Drive, iCloud, Photos ni documentos personales.
- No cerrar con "no pude"; si falta decision humana, formular gate bloqueante claro.

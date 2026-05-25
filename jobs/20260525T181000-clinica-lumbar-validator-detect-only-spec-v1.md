---
id: 20260525T181000-clinica-lumbar-validator-detect-only-spec-v1
created_at: 2026-05-25T18:10:00-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: CLINICA - validator detect-only para fixtures lumbares v2

## Objetivo

Diseñar la especificacion implementable de un validator detect-only para el fixture pack lumbar v2, sin tocar la app real. Codex principal ya materializo el JSON sintetico en la Mac de trabajo; su tarea es producir la logica de validacion, casos negativos y riesgos de falso positivo.

## Fuentes permitidas

- `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md`
- `context/fronts/clinica.md`

## Entregable esperado

Crear `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md` con:

- `summary`
- `validator_contract`
- `normalization_rules`
- `negation_handling_rules`
- `order_detection_rules` para parche dural, hemostasia, recuento y cierre
- `duplicate_detection_rules` para PLIF/materiales y preparacion inicial
- `critical_gates_first_batch`
- `false_positive_risks`
- `minimal_test_matrix`
- `implementation_sequence_for_orchestrator`
- `confidence`
- `evidence_paths`

## Reglas

- No modificar app real.
- No usar datos de pacientes.
- No navegar ni usar fuentes externas.
- No cerrar con "no pude"; si falta codigo real, proponer contrato conservador y verificable.

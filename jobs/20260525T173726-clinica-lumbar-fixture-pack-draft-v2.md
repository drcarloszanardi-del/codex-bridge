---
id: 20260525T173726-clinica-lumbar-fixture-pack-draft-v2
created_at: 2026-05-25T17:37:26-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: CLINICA - draft de fixture pack lumbar v2

## Objetivo

Convertir los resultados de gates lumbares en un draft de JSON de fixtures implementable por Codex principal en la app clínica canónica. No tocar la app real.

## Fuentes permitidas

- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md`
- `context/fronts/clinica.md`

## Entregable esperado

Crear `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md` con:

- `summary`
- `fixture_schema`
- `fixtures_json_draft` con al menos 16 casos
- `validator_expectations`
- `integration_notes_for_orchestrator`
- `risks_limits`
- `confidence`
- `evidence_paths`

## Reglas

- No modificar la app real.
- No usar pacientes ni datos sensibles.
- No navegar ni usar fuentes externas.
- No cerrar con "no pude"; si falta un detalle, proponer el campo conservador.

---
id: 20260525T184100-clinica-lumbar-v2-stress-artifacts-v1
created_at: 2026-05-25T18:41:00-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: CLINICA - stress artifacts para gates lumbares v2

## Contexto

Codex principal materializo el fixture pack lumbar v2 y creo un validator detect-only local, ya conectado al core QA. El core QA local paso OK. Ahora hace falta que Pablo diseñe una segunda capa de estres: textos buenos/malos sinteticos mas realistas para probar falsos positivos y falsos negativos.

## Fuentes permitidas

- `results/20260525T181000-clinica-lumbar-validator-detect-only-spec-v1.result.md`
- `results/20260525T173726-clinica-lumbar-fixture-pack-draft-v2.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`
- `context/fronts/clinica.md`

## Entregable esperado

Crear `results/20260525T184100-clinica-lumbar-v2-stress-artifacts-v1.result.md` con:

- `summary`
- `stress_artifacts_good`
- `stress_artifacts_bad`
- `expected_gate_outcomes`
- `false_positive_traps`
- `false_negative_traps`
- `recommended_artifact_mode_contract`
- `hard_fail_readiness_score`
- `next_actions_for_orchestrator`
- `confidence`
- `evidence_paths`

## Reglas

- No usar pacientes ni datos reales.
- No modificar app real.
- No navegar ni usar fuentes externas.
- No cerrar con "no pude"; si un caso es ambiguo, marcarlo como `report_only`.

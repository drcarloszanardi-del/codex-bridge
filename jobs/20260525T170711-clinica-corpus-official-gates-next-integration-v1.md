---
id: 20260525T170711-clinica-corpus-official-gates-next-integration-v1
created_at: 2026-05-25T17:07:11-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: CLINICA - priorizar integración de corpus oficial y gates críticos

## Objetivo

Revisar los resultados recientes de Pablo sobre clínica, jurisprudencia/corpus y gates lumbares, y proponer el próximo lote mínimo de integración real en la app clínica canónica. El foco es blindaje médico-legal verificable, no redacción libre.

## Fuentes locales permitidas

- `context/fronts/clinica.md`
- `results/20260525T013125-corpus-jurisprudencia-leyes-gates-app-clinica.result.md`
- `results/20260525T015134-corpus-medico-legal-schema-y-seed-oficial.result.md`
- `results/20260525T021012-corpus-official-jurisprudence-candidate-queue-v2.result.md`
- `results/20260525T124545-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260525T153318-clinica-lumbar-inconsistency-gates-v2.result.md`

No navegar, no usar Drive, no tocar datos de pacientes y no modificar la app real desde la Mac personal.

## Entregable esperado

Crear `results/20260525T170711-clinica-corpus-official-gates-next-integration-v1.result.md` con:

- `summary`
- `top_10_integrations_ranked`
- `critical_gates_first`
- `official_corpus_queue`
- `app_files_to_inspect_by_orchestrator`
- `fixture_pack_recommendation`
- `verification_plan`
- `risks_limits`
- `confidence`
- `evidence_paths`

## Reglas

- Separar fuente oficial, inferencia y recomendación.
- No proponer citas legales dentro del documento clínico final: proponer reglas/gates que endurezcan la redacción.
- No cerrar con "no pude"; si falta contexto, usar criterio conservador y dejar follow-up claro.

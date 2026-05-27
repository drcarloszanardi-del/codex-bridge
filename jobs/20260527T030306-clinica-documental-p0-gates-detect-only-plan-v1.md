---
id: 20260527T030306-clinica-documental-p0-gates-detect-only-plan-v1
created_at: 2026-05-27T03:03:06-03:00
created_by: orchestrator
assignee: personal-xh
front: CLINICA
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Clinica documental P0 gates detect-only plan v1

## 10 inicial - direccion del orquestador

Pablo esta idle y no hay jobs activos. Asignar backlog seguro de CLINICA, sin tocar ObraCash,
sin abrir bibliotecas privadas y sin acciones externas.

Objetivo: convertir el backlog `corpus a gates` en un plan implementable detect-only/report-only para
los primeros P0 documentales de la app medico-legal, sin tocar plantillas finales ni inventar normativa.

Contexto minimo:

- `context/fronts/clinica.md`
- `results/20260527T010224-clinica-corpus-gates-backlog-v2.result.md`
- `results/20260527T003215-clinica-correcciones-a-fixtures-implementacion.result.md`
- `results/20260526T145636-clinica-p0-extraforaminal-no-interlaminar-plan-v1.result.md`

## 80 delegado - trabajo de Pablo

Entregar:

- `p0_gate_scope`: 3 a 5 gates documentales P0 priorizados.
- `detect_only_contract`: input/output JSON y severidades `fail|needs_review|advisory`.
- `fixtures`: al menos 2 positivos y 2 negativos por gate, sinteticos y sin datos reales.
- `files_to_inspect`: rutas probables de app real y comandos `rg` para localizarlas.
- `implementation_sequence`: commits/capas recomendadas, bajo impacto.
- `legal_source_boundary`: que queda como regla documental interna vs que exige fuente oficial antes de hard gate.
- `qa_commands`: comandos sugeridos de QA focal y core QA.
- `risks_limits`: falsos positivos, contexto clinico y bloqueo excesivo.
- `recommendation`: proxima accion unica para el orquestador.

Reglas:

- No tocar plantillas finales.
- No inventar normativa ni citar leyes no verificadas.
- No acceder a Drive/iCloud/Gmail/Photos/Downloads.
- No imprimir secretos ni datos de pacientes.
- No cerrar con "no pude" sin limite exacto y alternativa.

## 10 final - retorno al orquestador

El resultado debe ser accionable, separando evidencia, inferencia y opinion. Validar contra
`scripts/validate_result_contract.py` antes de marcarlo completado.

---
id: 20260525T122122-pablo-idle-autodelegation-v1
assignee: personal-xh
model: gpt-5.5-xh
created_at: 2026-05-25T12:21:22-03:00
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: sistema para que Pablo no quede ocioso

## 10 inicial - direccion del orquestador

- Objetivo: proponer un mecanismo controlado para que Pablo reciba trabajo automaticamente cuando figure idle/requesting_work, sin perder control de Codex principal.
- Frente: CODEX-OPS / bridge.
- Contexto minimo:
  - `docs/pablo_idle_queue_policy.md`
  - `status/personal-xh.json`
  - `templates/workorder_10_80_10.md`
  - `scripts/validate_result_contract.py`
- Pregunta CEO: como evitar que Codex principal haga todo mientras Pablo espera, sin abrir riesgos de seguridad, ruido o gasto.
- Herramientas permitidas: leer repo bridge; proponer script/automation/rules.
- Herramientas prohibidas: modificar automations desde este worker, tocar secretos, acciones externas.
- Criterio de terminado: propuesta implementable de scheduler/cola, thresholds, anti-loop y reportes.

## 80 delegado - trabajo del agente

Pablo debe producir:

- `idle_detection`
- `work_pool`
- `assignment_rules`
- `anti_loop_rules`
- `security_limits`
- `implementation_plan`
- `reporting_contract`

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table`
- `idle_detection`
- `work_pool`
- `assignment_rules`
- `anti_loop_rules`
- `security_limits`
- `implementation_plan`
- `reporting_contract`
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py`.

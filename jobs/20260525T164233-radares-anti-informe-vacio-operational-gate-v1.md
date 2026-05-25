---
id: 20260525T164233-radares-anti-informe-vacio-operational-gate-v1
created_at: 2026-05-25T16:42:33-03:00
created_by: orchestrator
assignee: personal-xh
front: INVERSIONES
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
no_external_actions: true
no_secrets: true
---

# Workorder: RADARES - gate operativo anti informe vacio / anti "no pude"

## Contexto

El Doctor marco como inadmisible que los radares de inmobiliaria/inversiones entreguen informes vacios o centrados en "no pude entrar". La regla durable es que antes de bloquear deben intentarse rutas alternativas razonables y documentar evidencia.

## Objetivo

Definir un gate operativo que impida marcar como completo un informe de inmobiliaria, inversiones o instrumental si:

- no lista fuentes revisadas,
- no muestra rutas alternativas intentadas,
- no diferencia bloqueo tecnico de falta real de oportunidades,
- no entrega comparables,
- no prioriza oportunidades reales,
- no propone siguiente accion concreta.

## Fuentes locales permitidas

- `results/20260525T021032-radar-scorecards-inmobiliaria-instrumental-v1.result.md`
- `results/20260525T103407-rescate-radar-inversiones-sin-no-puedo-v1.result.md`
- `results/20260525T103946-inmobiliaria-junin-casas-reforma-radio-12-cuadras-v2.result.md`
- `results/20260525T103947-instrumental-neuro-columna-china-vs-argentina-v2.result.md`
- `results/20260525T103949-anti-informe-vacio-qa-radares-v1.result.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `results/20260525T122941-radar-anti-empty-script-spec.result.md`
- `results/20260525T124718-radares-source-recovery-playbook.result.md`
- `context/fronts/radares.md` si existe

No navegar, no contactar vendedores, no comprar, no abrir cuentas ni imprimir credenciales. Este job es de diseno/QA para el orquestador.

## Entregable esperado

Crear `results/20260525T164233-radares-anti-informe-vacio-operational-gate-v1.result.md` con:

- `summary`
- `minimum_viable_report_contract`
- `source_recovery_ladder`
- `empty_report_blockers`
- `real_estate_specific_checks`
- `instrumental_specific_checks`
- `telegram_report_template`
- `deterministic_gate_pseudocode`
- `orchestrator_integration_plan`
- `risks_limits`
- `confidence`
- `evidence_paths`

## Reglas

- No tocar ObraCash.
- No enviar Telegram ni emails.
- No imprimir secretos.
- No cerrar con "no pude"; si una fuente faltara, formular el contrato conservador y dejar evidencia.

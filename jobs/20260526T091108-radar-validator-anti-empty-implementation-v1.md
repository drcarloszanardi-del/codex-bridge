---
id: 20260526T091108-radar-validator-anti-empty-implementation-v1
created_at: 2026-05-26T09:11:08-03:00
created_by: orchestrator
assignee: personal-xh
front: RADARES
model: gpt-5.5-xh
reasoning_effort: high
status: queued
priority: high
no_external_actions: true
no_secrets: true
---

# Workorder: validator anti informe vacio para radares

## Contexto

El Doctor rechazo repetidamente informes de inmobiliaria/inversiones/instrumental que dicen "no pude", "pagina no hallada" o entregan un reporte vacio. La regla operativa vigente es: un bloqueo tecnico no es una conclusion; antes de reportar hay que intentar rutas alternativas, dejar evidencia y separar candidatos reales de errores tecnicos.

El resultado `results/20260526T073800-batch-results-priority-triage-v1.result.md` priorizo como bajo riesgo y alto impacto convertir el playbook de radares en checklist/validator local.

## Objetivo

Disenar una implementacion concreta y portable para un validador anti informe vacio de radares. Debe servir para inmobiliaria, inversiones, instrumental y viajes cuando aplique.

## Fuentes permitidas

- `results/20260526T065253-radares-source-recovery-playbook.result.md`
- `results/20260526T073800-batch-results-priority-triage-v1.result.md`
- `results/20260525T103949-anti-informe-vacio-qa-radares-v1.result.md` si existe
- `results/20260525T234822-radares-hardening-anti-informe-vacio-v2.result.md` si existe
- `protocol.md`

No abrir Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas. No navegar web desde este worker.

## Entregable esperado

Crear:

- `results/20260526T091108-radar-validator-anti-empty-implementation-v1.result.md`
- `results/20260526T091108-radar-validator-anti-empty-implementation-v1.manifest.json`

El resultado debe incluir:

1. Contrato de entrada/salida del validador.
2. Lista de hard fails que bloquean envio al Doctor.
3. Lista de warnings que permiten borrador interno pero no informe final.
4. Pseudocodigo o script Python completo propuesto.
5. Fixtures minimos: informe valido, informe con solo errores tecnicos, informe sin candidatos, informe sin fuentes, informe sin comparables.
6. Criterio de reintento/fallback: busqueda alternativa, cache, fuente secundaria, o pedir decision humana.
7. Que parte debe aplicar el orquestador localmente primero.

## Reglas

- No acciones externas.
- No secretos.
- No tocar contenido ObraCash.
- No mandar Telegram.
- No declarar que un radar no tiene oportunidades si la unica evidencia son errores tecnicos.
- Mantener foco en implementacion concreta, no en ensayo teorico.

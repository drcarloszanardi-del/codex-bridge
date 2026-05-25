# Resultado - Pablo idle autodelegation v1

Job: `20260525T122122-pablo-idle-autodelegation-v1`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

La forma correcta de que Pablo no quede ocioso no es autoejecutar tareas libres, sino que el orquestador mantenga una cola controlada y cree jobs 10-80-10 cuando `status/personal-xh.json` indique `idle/requesting_work`. Pablo pide trabajo por Git, el orquestador asigna, Pablo reclama, produce `results/`, valida, commitea y pushea. No se modificaron automations desde este worker.

## coverage_table

| Fuente | Estado | Uso |
|---|---|---|
| `jobs/20260525T122122-pablo-idle-autodelegation-v1.md` | revisado | Objetivo, limites y entregable. |
| `docs/pablo_idle_queue_policy.md` | revisado | Regla CEO, prioridad, no asignar, cola viva. |
| `status/personal-xh.json` | revisado | Senales `available`, `idle`, `requesting_work`, `capacity_for_work`. |
| `templates/workorder_10_80_10.md` | revisado | Contrato de jobs para Pablo. |
| `scripts/validate_result_contract.py` | revisado | Gate minimo de salida. |

## idle_detection

Pablo esta disponible si:

```yaml
status_file: status/personal-xh.json
required:
  status: "available"
  idle: true
  requesting_work: true
  capacity_for_work: true
no_pending_jobs_for_personal_xh: true
no_uncommitted_worker_changes: true
```

El orquestador debe verificar ademas que no haya claims abiertos sin resultado o commits locales no pusheados.

## work_pool

Cola sugerida, en orden:

1. Segunda mirada de riesgos en trabajos que Codex principal acaba de implementar.
2. Sintesis de material largo con salida ejecutable.
3. Arquitectura de herramientas/modelos/subagentes.
4. Preparacion premium de reels/presentaciones antes de recibir assets.
5. Fixtures y gates medico-legales.
6. QA anti informe vacio en radares.
7. Postmortem de errores de Telegram.

Cada item del pool debe transformarse en archivo `jobs/<id>.md`; Pablo no toma tareas no materializadas.

## assignment_rules

| Regla | Decision |
|---|---|
| Max jobs concurrentes asignados | 3 normales o 1 pesado. |
| Cada job | Debe usar template 10-80-10. |
| Prioridad humana reciente | Gana sobre cola idle. |
| Job sin paths/fuentes | No asignar hasta completar contexto. |
| Trabajo rutinario | Va a 5.3, no a Pablo. |
| Trabajo sensible | Sanitizar o dejar en principal. |
| Acciones externas | Nunca asignar a Pablo como ejecucion; solo analisis/propuesta. |

## anti_loop_rules

- No crear job idle si ya hay jobs pendientes para `personal-xh`.
- No crear mas de un batch idle cada 30 minutos.
- No crear job cuyo unico objetivo sea "pedir mas trabajo".
- No reabrir job que ya tiene `results/<id>.result.md`.
- Si dos ciclos seguidos generan resultados rechazados por validator, pausar autodelegation y pedir revision del orquestador.
- Cada job idle debe tener `front`, `criterio de terminado` y `evidence_paths` esperados.

## security_limits

| Limite | Razon |
|---|---|
| No Telegram/Gmail/Drive/Calendar | Evita acciones externas y permisos innecesarios. |
| No credenciales ni secretos | Pablo no debe imprimir ni tocar tokens. |
| Solo bridge/local paths permitidos | Mantiene trazabilidad y control. |
| No compras/contactos/publicaciones | Decision final del orquestador/Doctor. |
| Datos sensibles sanitizados | Clinica y pacientes requieren control principal. |
| Validacion de resultado obligatoria | Evita ruido y outputs vacios. |

## implementation_plan

1. Crear script del orquestador: `scripts/orchestrator_assign_idle_work.py`.
2. El script hace `git pull --rebase`, lee `status/personal-xh.json` y lista pendientes.
3. Si Pablo esta idle y no hay jobs, toma el primer item de `docs/pablo_idle_queue_policy.md`.
4. Genera job desde `templates/workorder_10_80_10.md`.
5. Limita batch por tiempo y cantidad.
6. Hace `python3 scripts/secret_scan.py`, commit y push.
7. Dashboard muestra `requesting_work`, ultimo job asignado y edad de idle.

Pseudo-flujo:

```text
if personal_xh.requesting_work and no_pending_jobs:
    candidate = next_work_pool_item()
    if candidate.allowed and not recently_assigned(candidate):
        create_job(candidate, assignee="personal-xh")
        commit_push()
```

## reporting_contract

`status/orchestrator.json` deberia agregar:

```json
{
  "idle_assignment": {
    "last_checked_at": "ISO-8601",
    "last_assigned_job": "job_id",
    "reason": "idle_pool|human_priority|none",
    "pending_for_personal_xh": 0,
    "cooldown_until": "ISO-8601"
  }
}
```

Cada job creado por idle debe incluir:

- `created_by: orchestrator_idle_scheduler`
- `source_policy: docs/pablo_idle_queue_policy.md`
- `no_external_actions: true`
- `no_secrets: true`

## risks / limits

- Si se asigna demasiado, Pablo puede producir ruido y saturar revision del orquestador.
- Si se asigna trabajo rutinario, se desperdicia XH.
- Si el cooldown no existe, puede haber loops de jobs idle.
- Si no se valida el resultado, el bridge se llena de informes no accionables.
- Este worker no modifico automations por restriccion explicita del job.

## recommendation

Implementar autodelegation solo en el orquestador, no en Pablo. Usar batch maximo 3 jobs, cooldown 30 minutos, validator obligatorio y cola viva editable en `docs/pablo_idle_queue_policy.md`. Pablo debe limitarse a senalizar disponibilidad, procesar jobs y devolver resultados.

## confidence

Alta. El mecanismo deriva de la politica idle ya creada, del status actual y del template 10-80-10. Los riesgos principales son operativos, no tecnicos.

## evidence_paths

- `jobs/20260525T122122-pablo-idle-autodelegation-v1.md`
- `docs/pablo_idle_queue_policy.md`
- `status/personal-xh.json`
- `templates/workorder_10_80_10.md`
- `scripts/validate_result_contract.py`

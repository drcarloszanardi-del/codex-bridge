---
job_id: 20260525T084316-dashboard-simple-flujo-codex-24x7-v1
worker: personal-xh
status: completed
completed_at: 2026-05-25T08:52:07-03:00
front: CODEX-OPS
---

# Result

## summary

Propuesta de dashboard local minimo: una pantalla simple de flujo, alimentada solo por archivos del bridge Git. Debe mostrar frentes, jobs, estado actual, ultimo resultado y proxima accion. Sin servicios externos, sin credenciales y sin escribir fuera del repo.

## findings con evidencia

- El bridge ya tiene fuentes suficientes: `jobs/`, `results/`, `claims/`, `status/` y `decisions/`.
- `scripts/bridgectl.py list-jobs` ya resume pending, assignee, front, claimed_by y has_result.
- Falta una vista humana consolidada; hoy el estado se interpreta leyendo JSON y markdown dispersos.

## UI propuesta

Pantalla unica, local:

```text
CODEx 24x7

[GLOBAL] sincronizado hace 2 min | pendientes 4 | bloqueados 0 | ultimo push OK

CLINICA        pensando     job actual        ultimo resultado        proxima accion
CODEX-OPS      ejecutando   job actual        ultimo resultado        proxima accion
TESIS          quieto       -                 ultimo resultado        esperar jobs
REELS-CMP      bloqueado    job id            error breve             requiere decision
INMOBILIARIA   quieto       -                 ultimo resultado        -
OBRACASH       quieto       -                 ultimo resultado        -
```

Controles minimos:

- Refresh manual.
- Toggle `solo pendientes`.
- Link local al job y al result.
- Chip de estado: `quieto`, `pensando`, `ejecutando`, `bloqueado`, `done`.
- Panel lateral con "ultima decision" y "proxima accion".

## arquitectura

Implementacion local estatica:

```text
dashboard/
  index.html
  app.js
  style.css
  dashboard_snapshot.py
  state.json
```

`dashboard_snapshot.py` lee:

- `jobs/*.md`
- `results/*.result.md`
- `claims/*.json`
- `status/*.json`
- `decisions/*.md`
- `git status --short`

Luego escribe `dashboard/state.json`. `index.html` consume ese JSON con refresh cada 15 segundos si se sirve por localhost.

Servidor local opcional:

```bash
python3 dashboard/dashboard_snapshot.py
python3 -m http.server 8788 -d dashboard
```

Tambien debe funcionar abriendo `dashboard/index.html` si el browser permite leer `state.json` local.

## formato de datos

```json
{
  "updated_at": "2026-05-25T08:52:07-03:00",
  "git": {
    "branch": "main",
    "dirty": false,
    "last_commit": "abc123"
  },
  "workers": [
    {
      "role": "personal-xh",
      "status": "available",
      "updated_at": "2026-05-25T08:52:07-03:00",
      "last_completed_jobs": []
    }
  ],
  "fronts": [
    {
      "front": "CODEX-OPS",
      "state": "ejecutando",
      "pending": 2,
      "blocked": 0,
      "current_job": "20260525T084316-dashboard-simple-flujo-codex-24x7-v1",
      "last_result": "results/...",
      "next_action": "esperar decision del orquestador"
    }
  ],
  "jobs": [
    {
      "id": "20260525T084316-example",
      "front": "CODEX-OPS",
      "assignee": "personal-xh",
      "claim": "active",
      "has_result": false,
      "state": "ejecutando",
      "path": "jobs/20260525T084316-example.md",
      "result_path": null
    }
  ]
}
```

## reglas de derivacion de estado

- `quieto`: no hay pending para el frente.
- `pensando`: job claimed por worker y sin result, claim reciente, sin evidencia de escritura final.
- `ejecutando`: job claimed y status del worker actualizado en los ultimos 10 minutos.
- `bloqueado`: existe result con `blocked`, claim vencido, error en status, o job pending viejo sin avance.
- `done`: result existe.

## MVP implementable desde esta Mac

1. Crear `dashboard/dashboard_snapshot.py` con parser simple de frontmatter y JSON.
2. Crear `dashboard/index.html`, `dashboard/app.js`, `dashboard/style.css`.
3. Agregar comando `./scripts/dashboard_refresh.sh` si se quiere refresh manual.
4. No hacer llamadas de red.
5. No leer credenciales.
6. No escribir fuera de `dashboard/state.json`.

## criterios de verificacion

- Con repo limpio y sin jobs, muestra todos los frentes como `quieto`.
- Con job pending sin claim, muestra `pendiente`.
- Con claim sin result, muestra `pensando/ejecutando`.
- Con result existente, muestra `done` y link al resultado.
- Con status viejo o claim viejo, muestra `bloqueado`.
- Si `state.json` esta corrupto, la UI muestra error local claro y no se rompe.

## recommendation

Implementar como dashboard local de solo lectura con snapshot JSON generado por script. Evitar base de datos y evitar webhooks: el Git bridge ya es la fuente de verdad.

## confidence

High. La informacion necesaria ya existe en el repo y el MVP puede hacerse sin servicios externos.

## evidence_paths

- `jobs/`
- `results/`
- `claims/`
- `status/personal-xh.json`
- `scripts/bridgectl.py`
- `jobs/20260525T084316-dashboard-simple-flujo-codex-24x7-v1.md`

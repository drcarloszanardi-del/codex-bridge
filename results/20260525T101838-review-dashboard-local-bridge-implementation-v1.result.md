---
job_id: 20260525T101838-review-dashboard-local-bridge-implementation-v1
worker: personal-xh
status: completed
completed_at: 2026-05-25T10:21:39-03:00
front: CODEX-OPS
---

# Result

## summary

Code review del dashboard local integrado en `dashboard/`. No encontre riesgos criticos de secretos ni XSS evidente: la UI usa `textContent`/DOM nodes y `dashboard/state.json` esta correctamente ignorado por Git. Si el objetivo es una vista "en tiempo real", el principal gap es que hoy el dashboard refresca solo un JSON estatico; no regenera el snapshot.

## findings con evidencia

### P2 - El refresh del navegador no actualiza datos reales si nadie regenera `state.json`

Evidencia:

- `dashboard/app.js:110-122` hace `fetch("state.json")` cada 15 segundos.
- `dashboard/dashboard_snapshot.py:270-275` genera `dashboard/state.json` una sola vez y termina.
- `README.md:40-49` indica correr una vez `python3 dashboard/dashboard_snapshot.py` y luego `python3 -m http.server 8788`.

Impacto: la pantalla parece viva por el polling, pero el estado queda congelado hasta que alguien vuelva a ejecutar el snapshot. Para el flujo 24/7 puede mostrar jobs ya terminados como activos o no mostrar nuevos jobs.

Recomendacion concreta: agregar uno de estos comandos oficiales:

```bash
while true; do python3 dashboard/dashboard_snapshot.py >/dev/null; sleep 15; done
```

o mejor:

```bash
python3 dashboard/dashboard_snapshot.py --watch --interval 15
```

### P2 - JSON invalido en claims/status se oculta como si no existiera

Evidencia:

- `dashboard/dashboard_snapshot.py:92-96` atrapa `json.JSONDecodeError` y devuelve `{}`.
- `dashboard/dashboard_snapshot.py:167-178` usa `{}` como claim vacio, dejando `claimed_by` vacio.
- `dashboard/dashboard_snapshot.py:116-130` saltea status JSON invalido sin mostrar alarma.

Impacto: un claim corrupto o un status corrupto deberia ser visible como bloqueo operativo. Hoy puede convertir un job reclamado en `pendiente` o borrar un worker de la vista, que es justo lo contrario de observability.

Recomendacion concreta: devolver estructura con error, por ejemplo `{"_invalid_json": true, "_path": "claims/..."}`, y marcar el job/front como `bloqueado` con `next_action="revisar JSON invalido"`.

### P2 - `ejecutando` depende de `status/<worker>.json`, no del claim reciente

Evidencia:

- `dashboard/dashboard_snapshot.py:133-141` considera worker fresh solo si `status.updated_at` tiene menos de 10 minutos.
- `dashboard/dashboard_snapshot.py:144-158` solo marca `ejecutando` si `worker_fresh(...)` es true; si no, marca `pensando`.
- En una corrida local del snapshot, un claim recien creado aparecio como `pensando` porque `status/personal-xh.json` era mas viejo que 10 minutos.

Impacto: el dashboard puede degradar un trabajo actualmente tomado a `pensando`, aunque el worker este ejecutandolo. La vista pierde precision operacional.

Recomendacion concreta: si el claim tiene `claimed_at`/`heartbeat_at` menor a 10 minutos, mostrar `ejecutando` aunque `status` este viejo. Mantener `status` como senal adicional, no unica.

### P3 - Rendimiento lineal con todo el historial

Evidencia:

- `dashboard/dashboard_snapshot.py:161-186` recorre todos los `jobs/*.md`.
- Para cada job lee frontmatter, claim y frontmatter del result.
- `dashboard/dashboard_snapshot.py:266` envia toda la lista de jobs al JSON.

Impacto: hoy funciona bien por volumen bajo, pero con miles de jobs el snapshot y el JSON pueden crecer innecesariamente.

Recomendacion concreta: mantener vista completa por default pero agregar limite configurable: ultimos 200 jobs, mas todos los pendientes/bloqueados. Ejemplo: `--max-history 200`.

## checks positivos

- `dashboard/state.json` esta en `.gitignore:9`; correcto porque es estado local derivado.
- Los enlaces son relativos al repo y funcionan si se sirve desde la raiz con `http://localhost:8788/dashboard/`.
- La UI evita `innerHTML`; bajo el modelo actual no hay XSS obvio desde job ids/frontmatter.
- No se observan lecturas de credenciales ni llamadas externas.

## recommendation

Integrar un patch pequeno antes de considerar el dashboard listo para uso diario:

1. Agregar modo `--watch --interval 15` al snapshot.
2. Tratar JSON invalido en claims/status como bloqueo visible.
3. Derivar `ejecutando` desde claim reciente, no solo desde `status.updated_at`.
4. Agregar limite de historial para sostener rendimiento.

## confidence

High. La revision se baso en los archivos integrados del dashboard, README, `.gitignore` y una ejecucion local de `dashboard/dashboard_snapshot.py`.

## evidence_paths

- `dashboard/dashboard_snapshot.py`
- `dashboard/app.js`
- `dashboard/index.html`
- `dashboard/style.css`
- `README.md`
- `.gitignore`
- `jobs/20260525T101838-review-dashboard-local-bridge-implementation-v1.md`

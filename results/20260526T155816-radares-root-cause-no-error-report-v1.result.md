---
job_id: 20260526T155816-radares-root-cause-no-error-report-v1
worker: personal-xh
status: completed
completed_at: 2026-05-26T16:04:03-03:00
front: RADARES
no_external_actions: true
no_secrets: true
---

# Resultado - RADARES root cause no error report v1

## summary

verdict: **ajustar antes de darlo por cerrado**. Los gates locales van en la
direccion correcta, pero la recaida en INM-001/INV-001 sugiere que el problema
ya no esta en la regla conceptual sino en el enforcement de entrega: algun
wrapper, cron, router, `--force`, artifact viejo o fallback operativo puede
convertir un fallo tecnico en texto publicable despues de que el reporter marco
`sent:false` o `blocked`.

La hipotesis fuerte es: **se valido el reporter, pero no el ultimo chokepoint
antes del topic**. El arreglo de bajo riesgo es agregar un `radar_delivery_guard`
unico, obligatorio y posterior a cualquier reporter/wrapper, que bloquee todo
texto final con error tecnico, payload crudo o contrato incompleto aunque venga
de una ruta legacy o con force.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260526T155816-radares-root-cause-no-error-report-v1.md` | Revisada | Workorder, sintomas INM-001/INV-001 y sospechas de bypass. |
| `results/20260526T091108-radar-validator-anti-empty-implementation-v1.result.md` | Revisada | Hard fails: error tecnico como conclusion, payload crudo, falta de contrato. |
| `results/20260526T143429-inversiones-instrumental-fallback-quality-v1.result.md` | Revisada | Fallback local watchlist para evitar silencio operacional sin recomendar implantes. |
| `results/20260525T234822-radares-hardening-anti-informe-vacio-v2.result.md` | Revisada | Contrato de radar, P0 rules y fixtures anti informe vacio. |
| `results/20260525T211520-postpatch-telegram-radar-gate-audit-v1.result.md` | Revisada | Riesgos residuales: error-only no basta, delivery y artifact local. |
| `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md` | Revisada | Fixtures de radar tecnico vacio, force/delivery y payload crudo. |
| `results/20260526T003720-post-integration-audit-radar-tesis-clinica-v1.result.md` | Revisada | Punto comun: politicas buenas pueden quedar desconectadas del runner real. |
| `protocol.md` | Revisado | Regla durable: bloqueo tecnico no es resultado final; decision final queda en orquestador. |

## root_cause_hypothesis

1. **Bypass post-reporter**: `send_inm_radar_report.js` y
   `send_inv_neuro_instrument_report.js` pueden devolver `sent:false`, pero un
   wrapper cron o topic/router formatea la razon tecnica y la manda igual como
   "reporte". Tests de reporter no cubren ese ultimo paso.
2. **Force mal definido**: un `--force` o modo manual puede saltear el gate de
   calidad. Force deberia significar "guardar artifact local para revision", no
   "publicar al Doctor".
3. **Ruta legacy o artifact crudo**: una ruta vieja puede leer el ultimo markdown,
   stdout/stderr, error de fetch o artifact anterior y publicarlo sin volver a
   validar `status_by_gate`, `hard_blockers` y `can_publish`.
4. **Estado `blocked` tratado como mensaje util**: se confunde bloqueo operativo
   con informe. Si el scan falla, el estado correcto es `needs_retry` o
   `fallback_pending` local; no una pieza con "pagina no hallada".
5. **Gate demasiado estrecho**: se bloqueo `all technical failures`, pero no todos
   los casos pobres: una fuente real + errores, cero candidatos sin universo,
   candidato unico debil, payload tecnico o mensaje "no pude" envuelto por el
   automation prompt.
6. **Automation prompt residual**: alguna automatizacion puede estar instruida a
   "avisar que fallo" y no a "crear artifact local y reintentar fallback"; eso
   reintroduce el error por fuera del codigo del reporter.

## patch_plan

### P0 - Un chokepoint de entrega obligatorio

Agregar un guard final, invocado por cualquier ruta que intente publicar o
resumir radares al topic:

```text
scripts/radares/radar_delivery_guard.js
```

Entrada minima:

```json
{
  "front": "INM-001|INV-001",
  "report_text": "string",
  "report_contract": {
    "status_by_gate": "completed|needs_review|blocked|needs_retry|fallback_pending",
    "score": 0,
    "hard_blockers": [],
    "can_publish": false,
    "sources_attempted": [],
    "fallback_routes_used": [],
    "candidates": [],
    "rejections": [],
    "next_action": "string"
  },
  "origin": "cron|manual|topic_router|legacy|force",
  "force": false
}
```

Reglas exactas:

- Si `report_text` contiene `no pude`, `pagina no hallada`, `DNS`, `WAF`,
  `captcha`, `HTTP error`, `traceback`, `stack trace`, `fatal:` o diff crudo:
  `can_publish=false`.
- Si `status_by_gate` no es `completed`: `can_publish=false`, salvo resumen
  operativo interno con `audience=orchestrator_only`.
- Si `force=true`: seguir bloqueando publicacion externa; permitir solo
  `force_local_artifact=true`.
- Si faltan fuentes, fallback, candidatos/descartes, comparables o `next_action`:
  `can_publish=false`.
- Si INV detecta implantes sin `ANMAT/importador/lote/trazabilidad`: bloquear
  `comprar` y degradar a `regulatory_blocked|needs_review`.

### P0 - Cambiar estados de fallo de scan

En `scripts/inmobiliaria/send_inm_radar_report.js` y
`scripts/inversiones/send_inv_neuro_instrument_report.js`:

- Reemplazar salidas publicables de fallo por:
  `needs_retry`, `fallback_pending`, `blocked_operational` o
  `regulatory_blocked`.
- Agregar siempre `can_publish=false` cuando el motivo sea tecnico.
- Agregar `retry_plan` con fuentes concretas:
  - INM: MercadoLibre, Zonaprop, Argenprop, inmobiliarias locales, snippets/cache,
    comparables por zona, y minimo de casas/PH reales antes de publicar.
  - INV: familias de instrumental reutilizable, anclas locales, exclusion de
    implantes sin trazabilidad.

### P0 - Ejecutar regression gates en el wrapper

En el wrapper cron o automation que llama los radares:

```bash
scripts/qa/run_radar_regression_gates.sh
```

debe correrse antes de cualquier envio al topic. Si falla, crear artifact local
con `status=blocked_operational` y `next_action`, no enviar "informe".

### P1 - Normalizar artifact y recibo

Guardar para cada corrida:

```text
artifacts/radares/<run_id>/contract.json
artifacts/radares/<run_id>/report.md
artifacts/radares/<run_id>/delivery_guard.json
```

Si `delivery_guard.can_publish=false`, el router no debe tener texto para
Telegram salvo un aviso interno al orquestador.

## fixtures_to_add

| Fixture | Criterio esperado |
| --- | --- |
| `R_DELIVERY_GUARD_BLOCKS_TECH_TEXT_INM001` | Texto con `pagina no hallada` queda `can_publish=false`, aunque venga de cron. |
| `R_DELIVERY_GUARD_BLOCKS_TECH_TEXT_INV001` | Texto con DNS/WAF/captcha/HTTP error queda bloqueado. |
| `R_FORCE_DOES_NOT_BYPASS_RADAR_GATE` | `force=true` solo permite artifact local, nunca publish al Doctor. |
| `R_SENT_FALSE_NOT_FORMATTED_TO_TOPIC` | Reporter devuelve `sent:false`; wrapper no transforma reason en informe. |
| `R_LEGACY_ARTIFACT_REVALIDATED` | Artifact viejo/crudo debe pasar delivery guard antes de reuso; si no, bloqueado. |
| `R_CRON_EXCEPTION_NO_PUBLIC_REPORT` | Excepcion del cron genera `blocked_operational` con next action, no mensaje tecnico. |
| `R_INM_FALLBACK_PENDING_MIN_SOURCES` | INM con fuentes insuficientes queda `fallback_pending` hasta intentar fuentes alternativas. |
| `R_INV_IMPLANT_TRACEABILITY_BLOCK` | Implantes sin ANMAT/importador/lote no pueden salir como oportunidad ni compra. |
| `R_ONE_REAL_SOURCE_STILL_NEEDS_CONTRACT` | Una fuente real + sin comparables/descartes no puede ser `completed`. |

## risk

| Riesgo | Mitigacion |
| --- | --- |
| Silenciar demasiado y que el orquestador no vea fallos | Crear artifact local obligatorio con `next_action`, visible en dashboard/bridge. |
| Bloquear un reporte exhaustivo sin candidatos | Permitir `needs_review` si hay 5+ fuentes, descartes, comparables y proxima corrida. |
| Incentivar candidatos falsos para pasar el gate | Aceptar `needs_review` honesto; no exigir candidatos si el universo esta documentado. |
| Romper `--force` usado para debugging | Redefinir force como local-only; no como publish bypass. |
| Mezclar instrumental reusable con implantes | Separar familias y usar `regulatory_blocked` para implantes sin trazabilidad. |

## next_action

Accion unica recomendada:

```text
Implementar `radar_delivery_guard` como ultimo paso obligatorio antes de cualquier envio/resumen de INM-001 o INV-001, crear los fixtures R_DELIVERY_GUARD_BLOCKS_TECH_TEXT_* y R_FORCE_DOES_NOT_BYPASS_RADAR_GATE, y conectar el guard al wrapper cron/topic router antes de tocar mas heuristicas de busqueda.
```

## recommendation

No integrar mas reportes de INM-001/INV-001 como finales hasta que exista el
guard de entrega. Integrar ahora el guard P0 y dejar las mejoras de busqueda como
P1: primero impedir que el error tecnico sea publicable; despues mejorar fuentes
y scoring.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se reclamaron los jobs con `python3 scripts/bridgectl.py claim`.
- Se revisaron resultados recientes y contratos de radares/Telegram disponibles
  en el bridge.
- No se uso Telegram, Gmail, Drive, Calendar, navegador autenticado ni compras.
- No se tocaron credenciales ni ObraCash.

## risks_limits

No inspeccione la Mac de trabajo ni los scripts reales mencionados en el
workorder; este diagnostico se basa en evidencia del bridge y en la reincidencia
reportada. La causa exacta debe confirmarse instrumentando el ultimo paso de
entrega, no agregando mas reglas teoricas al reporter.

## confidence

Media-alta. La evidencia local muestra que ya hay reglas y tests, pero el bug
reaparece en operacion; eso apunta mas a bypass/enforcement que a falta de
politica. La hipotesis exacta entre cron, force, legacy o artifact crudo requiere
ver el runner real.

## evidence_paths

- `jobs/20260526T155816-radares-root-cause-no-error-report-v1.md`
- `results/20260526T091108-radar-validator-anti-empty-implementation-v1.result.md`
- `results/20260526T143429-inversiones-instrumental-fallback-quality-v1.result.md`
- `results/20260525T234822-radares-hardening-anti-informe-vacio-v2.result.md`
- `results/20260525T211520-postpatch-telegram-radar-gate-audit-v1.result.md`
- `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md`
- `results/20260526T003720-post-integration-audit-radar-tesis-clinica-v1.result.md`
- `protocol.md`

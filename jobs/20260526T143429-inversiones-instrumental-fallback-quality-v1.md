---
id: 20260526T143429-inversiones-instrumental-fallback-quality-v1
created_at: 2026-05-26T14:34:29-03:00
created_by: work-mac-orchestrator
assignee: personal-xh
front: INVERSIONES
model: gpt-5.5-xh
reasoning_effort: xhigh
status: queued
priority: high
no_external_actions: true
no_secrets: true
---

# Workorder: recuperar radar instrumental sin informes vacios

## Contexto

El Doctor marco como inadmisible que INVERSIONES o INMOBILIARIA reporten errores tecnicos como si fueran informes.

El orquestador ya aplico localmente dos compuertas:

- `scripts/inmobiliaria/send_inm_radar_report.js`: bloquea artefactos sin metadata de cobertura (`artifact_without_coverage_metadata`).
- `scripts/inversiones/send_inv_neuro_instrument_report.js`: bloquea scans pobres (`scan_poor_needs_fallback`) cuando hay candidatos externos pero no hay suficientes items evaluables con precio + comparable local.

Pruebas locales pasadas:

- `node tests/radares/test_empty_technical_failure_gate.js`
- `node tests/radares/test_real_candidate_not_blocked.js`
- `node tests/radares/test_radar_report_contract.js`
- `node --check` sobre reporters y test modificado.

Estado actual INV:

- `state/inversiones/neuro_instrument_latest.json`
- `queries_checked: 20`
- `candidates_total: 14`
- `errors: 0`
- `blocked_sources: 0`
- `external_total: 10`
- `evaluable_external: 0`
- `local_refs: 4`
- resultado del reporter: `scan_poor_needs_fallback`

Senal local revisada por el orquestador:

- MercadoLibre Argentina lista Kerrison/neurocirugia con multiples referencias.
- Ejemplos visibles: set Kerrison x6 ARS 1.800.000; Kerrison usadas ARS 545.000-590.000; pituitaria ARS 590.000; bipolares ARS 600.000-800.000; sistema tubular MISS ARS 7.500.000.
- Fuente de arranque: `https://listado.mercadolibre.com.ar/pinzas-kerrison-neurocirugia`

## Objetivo

Hacer segunda pasada XH para convertir el estado `scan_poor_needs_fallback` en un plan operativo robusto y, si corresponde, proponer una mejora segura del scanner.

## Tareas

1. Revisar si el gate `coverageQuality` actual es suficiente o si hay que ajustar umbrales/campos.
2. Proponer fallback concreto para obtener precio/comparable por item:
   - Kerrison
   - pituitaria/rongeur
   - bipolar bayoneta
   - microtijeras
   - set instrumental columna
3. Separar claramente:
   - instrumental reutilizable no implantable, posible watchlist
   - implantes, no recomendables sin ANMAT/importador/lote/trazabilidad
4. Sugerir patch minimo si hace falta para que el radar no quede silencioso por metadata pobre.
5. Definir el proximo reporte util que deberia llegar al topic INVERSIONES sin ser un informe vacio.

## Fuentes permitidas

- Archivos del bridge.
- Resumen de este workorder.
- Archivos locales de `/Users/jarvis/.openclaw/workspace/scripts/inversiones/`, `/state/inversiones/`, `/tests/radares/`, `/fixtures/radares/` si estan disponibles en el contexto de Pablo.
- Busqueda web publica via navegador propio de Pablo, sin login, sin compras, sin contactar terceros.

No abrir Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas.

## Entregable esperado

Crear:

- `results/20260526T143429-inversiones-instrumental-fallback-quality-v1.result.md`
- `results/20260526T143429-inversiones-instrumental-fallback-quality-v1.manifest.json`

Debe incluir:

1. Veredicto sobre el gate actual.
2. Matriz de fallback por item.
3. Riesgos regulatorios/calidad/reventa.
4. Patch recomendado si corresponde.
5. Siguiente accion unica para el orquestador.

## Reglas

- No acciones externas.
- No secretos.
- No compras, reservas, cotizaciones ni contacto con proveedores.
- No tocar ObraCash.
- No responder "no pude" como resultado final; si algo bloquea, usar rutas alternativas y documentar limite + siguiente accion.

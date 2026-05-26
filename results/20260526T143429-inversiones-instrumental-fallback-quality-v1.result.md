---
job_id: 20260526T143429-inversiones-instrumental-fallback-quality-v1
worker: personal-xh
status: completed
completed_at: 2026-05-26T14:39:23-03:00
front: INVERSIONES
no_external_actions: true
no_secrets: true
---

# Resultado - inversiones instrumental fallback quality v1

## summary

El gate actual `coverageQuality` es correcto como freno: con `external_total=10`,
`evaluable_external=0` y `local_refs=4`, bloquear un informe final de oportunidad
es la decision segura. Pero no alcanza como recuperacion operacional: el radar
ya tiene senal local suficiente para emitir un reporte util de tipo
`fallback_local_watchlist`, sin recomendacion de compra y con metadata clara.

La mejora minima es separar tres estados:

- `completed`: hay candidatos evaluables con precio, fuente y comparable.
- `fallback_local_watchlist_ready`: no hay evaluables externos suficientes, pero
  hay anclas locales por familia de instrumento y riesgos explicitados.
- `blocked_scan_poor`: no hay evaluables externos ni anclas locales suficientes.

Con el estado actual, el siguiente reporte util para INVERSIONES deberia ser:
`Instrumental neuro/columna - fallback local-only, watchlist prudente, sin compra`.

## source_counts

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260526T143429-inversiones-instrumental-fallback-quality-v1.md` | Revisada | Workorder, estado actual del radar y senales locales visibles. |
| `results/20260525T103947-instrumental-neuro-columna-china-vs-argentina-v2.result.md` | Revisada | Matriz previa China vs Argentina, precios locales y separacion implantes/instrumental. |
| `results/20260525T103949-anti-informe-vacio-qa-radares-v1.result.md` | Revisada | Criterios QA anti informe vacio para radares. |
| `results/20260525T124718-radares-source-recovery-playbook.result.md` | Revisada | Ladder de recuperacion por fuente bloqueada o pobre. |
| `results/20260525T164233-radares-anti-informe-vacio-operational-gate-v1.result.md` | Revisada | Gate operativo y reglas especificas para instrumental medico. |
| `results/20260526T065253-radares-source-recovery-playbook.result.md` | Revisada | Version reciente del playbook de recuperacion. |
| `results/20260526T091108-radar-validator-anti-empty-implementation-v1.result.md` | Revisada | Contrato parseable y hard fails del validator. |
| `/Users/jarvis/.openclaw/workspace/scripts/inversiones/` | No disponible en este contexto local | Se uso el resumen del workorder en lugar de codigo fuente no presente. |

## verdict_gate_actual

Veredicto: mantener el bloqueo `scan_poor_needs_fallback`, pero cambiar su salida
para que no deje al radar silencioso cuando hay anclas locales.

El gate actual es suficiente para impedir un informe vacio o una conclusion falsa:
un candidato externo sin precio y sin comparable local no debe llegar como
oportunidad. Tambien es correcto que `evaluable_external=0` bloquee una tesis de
importacion o arbitraje.

El ajuste necesario esta en la metadata y el branch de fallback:

```json
{
  "coverageQuality": {
    "queries_checked": 20,
    "external_total": 10,
    "evaluable_external": 0,
    "local_refs": 4,
    "items_with_local_anchor": 4,
    "items_missing_local_anchor": ["microtijeras"],
    "regulatory_blocked_count": 0,
    "fallback_mode": "local_market_watchlist",
    "report_kind": "fallback_local_watchlist",
    "gate_status": "needs_review_not_empty"
  }
}
```

Umbrales recomendados:

| Caso | Estado requerido | Motivo |
| --- | --- | --- |
| `evaluable_external >= 2` y cada candidato tiene precio + comparable | `completed` | Hay base minima para ranking operativo. |
| `evaluable_external < 2`, `local_refs >= 4` y `items_with_local_anchor >= 3` | `fallback_local_watchlist_ready` | No hay tesis externa cerrada, pero si reporte local util. |
| `evaluable_external < 2` y `items_with_local_anchor < 3` | `blocked_scan_poor` | Falta universo minimo; reintentar busqueda. |
| Item detectado como implante o descartable regulatorio | `regulatory_blocked` | No entra a watchlist de compra sin ANMAT/importador/lote/trazabilidad. |

## fallback_matrix

| Item | Fallback concreto de precio/comparable | Ancla actual o esperada | Clasificacion | Decision prudente |
| --- | --- | --- | --- | --- |
| Kerrison | Buscar y agrupar `pinzas kerrison neurocirugia`, `pinza kerrison 90`, `pinza kerrison 120`, set completo y unidad usada. Comparar set vs piezas sueltas, no mezclar medidas. | Senal local del workorder: set Kerrison x6 ARS 1.800.000; usadas ARS 545.000-590.000. | Reutilizable no implantable. | `watchlist` si hay fotos claras, medida, estado, procedencia y comparable local. |
| Pituitaria / rongeur | Buscar `pinza pituitaria neurocirugia`, `rongeur pituitaria`, `pituitary rongeur`, separando recta/angulada/upbiting. | Senal local del workorder: pituitaria ARS 590.000. | Reutilizable no implantable. | `watchlist` con condicion, boca/copa, longitud y marca; si falta medida, `pending_specs`. |
| Bipolar bayoneta | Buscar `pinza bipolar bayoneta neurocirugia`, `bipolar bayoneta`, `cable bipolar`, y registrar compatibilidad de conector/generador. | Senal local del workorder: bipolares ARS 600.000-800.000. | Reutilizable electrico no implantable. | `investigar` solo si explicita compatibilidad, aislamiento, cable, estado y garantia; si usado sin prueba electrica, `descartar`. |
| Microtijeras | Buscar `microtijera neurocirugia`, `micro tijera bayoneta`, `micro scissors Codman`, y usar benchmark local previo de microtijera usada si aparece. | Resultado previo: micro tijera Codman titanium usada aprox ARS 600.000; en el scan actual falta ancla explicita. | Reutilizable no implantable, alto desgaste. | `needs_review`: no rankear hasta tener filo/alineacion, marca, estado y precio local verificable. |
| Set instrumental columna | Buscar `kit instrumental columna`, `set instrumental columna neurocirugia`, `instrumental tornillo pedicular set`, y separar instrumental de implantes. Comparar pieza por pieza contra DTL/Soro/ML. | Resultado previo: kit DTL columna ARS 3.080.955,45; senal actual: sistema tubular MISS ARS 7.500.000. | Reutilizable si es set de instrumentos; regulatorio bloqueado si incluye implantes. | `investigar` para set no implantable itemizado; `regulatory_blocked` para tornillos, cages, barras o implantes. |

## risks_limits

Riesgo regulatorio:

- Implantes, cages, tornillos pediculares, barras, injertos, descartables esteriles y
  cualquier producto implantable no deben recomendarse sin registro ANMAT,
  importador/distribuidor habilitado, lote, trazabilidad, tarjeta de implante,
  vencimiento, empaque esteril e IFU.
- Marketplace chino o local puede servir como benchmark de spread, no como orden de
  compra de implantes.

Riesgo de calidad:

- Kerrison, rongeur y microtijeras usadas dependen de filo, alineacion, boca,
  corrosion, holgura, marcas de reparacion y vida util.
- Bipolar bayoneta agrega riesgo electrico: aislamiento, conector, cable,
  compatibilidad con generador y prueba funcional.
- Set de columna requiere equivalencia pieza por pieza; un set barato puede no
  reemplazar el set clinico necesario.

Riesgo de reventa:

- La liquidez mejora en instrumentos no implantables de marca reconocible,
  medidas comunes y buen estado fotografiable.
- La reventa cae fuerte si faltan marca, medidas, procedencia, factura, soporte
  o si el item parece parte de un lote incompleto.
- No conviene mezclar instrumental reutilizable con implantes en la misma tesis:
  los criterios regulatorios y de riesgo son distintos.

Limite de esta pasada: no se hizo navegacion publica nueva ni contacto externo.
El analisis usa bridge, workorder y resultados previos permitidos.

## patch_recommended

Patch minimo recomendado en `scripts/inversiones/send_inv_neuro_instrument_report.js`:

1. Mantener el hard gate actual para bloquear `completed` cuando
   `evaluable_external < 2`.
2. Agregar un builder `buildLocalInstrumentFallback(scan)` que clasifique
   referencias locales por familia:
   `kerrison`, `pituitaria_rongeur`, `bipolar_bayoneta`, `microtijeras`,
   `set_columna`, `implantes_regulatory_blocked`.
3. Si el scan cae en `scan_poor_needs_fallback` pero cumple
   `local_refs >= 4` y `items_with_local_anchor >= 3`, devolver:

```json
{
  "sent": false,
  "reason": "fallback_local_watchlist_ready",
  "rule": "anti_informe_vacio",
  "report_kind": "fallback_local_watchlist",
  "required_status": "needs_review",
  "coverageQuality": {
    "queries_checked": 20,
    "external_total": 10,
    "evaluable_external": 0,
    "local_refs": 4,
    "items_with_local_anchor": 4,
    "items_missing_local_anchor": ["microtijeras"],
    "regulatory_blocked_count": 0
  }
}
```

4. Generar un artifact de texto corto para el topic INVERSIONES, pero marcado
   como `needs_review` y sin compra:

```text
Radar instrumental - fallback local-only
Estado: needs_review, no compra.
Cobertura: 20 queries, 10 externos, 0 externos evaluables, 4 anclas locales.
Watchlist: Kerrison, pituitaria/rongeur, bipolar bayoneta, set columna no implantable.
Falta: microtijeras con ancla local verificable.
Excluido: implantes sin ANMAT/importador/lote/trazabilidad.
Proximo paso: rerun con queries por familia y matriz local_ref_by_item.
```

5. Agregar tests:

| Fixture | Esperado |
| --- | --- |
| poor external + 4 local anchors + no implants | `fallback_local_watchlist_ready`, no informe vacio. |
| poor external + 1 local anchor | `blocked_scan_poor`, proxima ruta concreta. |
| implant terms present + no traceability | `regulatory_blocked`, nunca `watchlist` de compra. |
| external candidate with price + local comparable | `completed` permitido si pasa score. |

## next_report_for_inversiones

El proximo reporte util debe ser una pieza breve, no una tesis cerrada:

```text
Instrumental neuro/columna - snapshot local de watchlist
Estado: needs_review, no compra.
1. Kerrison: ARS 545k-590k usadas; set x6 ARS 1.8M. Watchlist.
2. Pituitaria/rongeur: ancla ARS 590k. Watchlist con specs.
3. Bipolar bayoneta: ARS 600k-800k. Investigar compatibilidad electrica.
4. Microtijeras: falta ancla actual; buscar por familia y marca.
5. Set columna: DTL/ML como base local; separar sets no implantables de implantes.
Excluido: implantes sin ANMAT/importador/lote/trazabilidad.
Siguiente corrida: queries por familia + `local_ref_by_item`.
```

## recommendation

Implementar primero el modo `fallback_local_watchlist_ready` en el reporter de
INVERSIONES. Es el cambio de menor riesgo: no abre acciones externas, no inventa
oportunidades, no permite compras, pero evita que un scan pobre quede silencioso
cuando ya hay anclas locales suficientes para orientar la siguiente corrida.

Siguiente accion unica para el orquestador: crear el patch del reporter con
`local_ref_by_item` + `fallback_local_watchlist_ready`, y rerun del radar de
instrumental con las cinco familias de item como queries obligatorias.

## confidence

Media-alta. La conclusion sobre el gate es fuerte porque deriva de los conteos
del workorder y de reglas anti informe vacio ya consolidadas. La matriz de
precios es orientativa: debe tratarse como ancla local de watchlist, no como
cotizacion vigente ni decision de compra.

## evidence_paths

- `jobs/20260526T143429-inversiones-instrumental-fallback-quality-v1.md`
- `protocol.md`
- `results/20260525T103947-instrumental-neuro-columna-china-vs-argentina-v2.result.md`
- `results/20260525T103949-anti-informe-vacio-qa-radares-v1.result.md`
- `results/20260525T124718-radares-source-recovery-playbook.result.md`
- `results/20260525T164233-radares-anti-informe-vacio-operational-gate-v1.result.md`
- `results/20260526T065253-radares-source-recovery-playbook.result.md`
- `results/20260526T091108-radar-validator-anti-empty-implementation-v1.result.md`

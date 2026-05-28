---
job_id: 20260528T132759-radares-source-recovery-playbook
worker: personal-xh
status: completed
completed_at: 2026-05-28T13:28:18-03:00
front: INVERSIONES
no_external_actions: true
no_secrets: true
---

# Resultado - Radares source recovery playbook

## summary honesto

Un radar no puede cerrar con "no pude" si solo fallo una fuente. Para inmobiliaria, instrumental e inversiones, fuente bloqueada significa activar recuperacion: buscar espejo, cache/snippet, comparables, fuente oficial o mercado alternativo, registrar universo revisado y recien despues decidir `completed`, `needs_review` o `blocked`. Este resultado no navega ni busca oportunidades reales; deja el playbook operativo para que 5.3 y Codex principal no acepten informes vacios.

## coverage_table

| Requisito | Estado | Evidencia |
|---|---|---|
| `source_recovery_routes` | cubierto | Frente Radares y playbook anterior. |
| `front_specific_thresholds` | cubierto | Scorecards de inmobiliaria e instrumental. |
| `examples` | cubierto | Casos inmobiliaria/instrumental con bloqueo y cero candidatos. |
| `automation_hooks` | cubierto | Eventos previos al gate anti-empty. |
| `failure_language_ban` | cubierto | Frases prohibidas y formato permitido. |

## evidencia

- `context/fronts/radares.md` exige fuentes consultadas, candidatos, descartes, rutas alternativas, comparables y recomendacion accionable.
- `results/20260525T122941-radar-anti-empty-script-spec.result.md` define schema, reglas de gate y estados minimos.
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md` define contrato radar, thresholds y division entre 5.3, Pablo y Codex principal.
- `results/20260527T011700-radares-source-recovery-playbook.result.md` ya fija que una fuente bloqueada abre recuperacion antes de cerrar.

## inferencia

- Source recovery debe correr antes de `validate_radar_report.py`, no despues.
- El reporte debe poder terminar en `needs_review` con buen universo documentado; lo que queda prohibido es `completed` sin evidencia.
- Pablo solo debe intervenir cuando hay candidatos fuertes, bloqueo persistente o ranking estrategico, no para suplir barridos mecanicos.

## opinion

El lenguaje importa: "no encontre nada" suele esconder que se reviso poco. Un radar premium debe decir "revise este universo, descarte esto por estas razones, queda esta accion". Eso convierte frustracion en decision.

## source_recovery_routes

| Bloqueo | Rutas obligatorias | Evidencia minima | Cierre permitido |
|---|---|---|---|
| Web inmobiliaria no abre | Busqueda por direccion/zona exacta, portal espejo, snippets/cache, mapa/listing publico, comparables radio/m2. | Query, fuente, resultado, descartes y comparables. | `needs_review` si no hay oportunidad pero hay universo suficiente. |
| Precio inmobiliario faltante | Mismo inmueble en espejo, comparables por zona/m2, historial/snippet, marcar `pendiente_precio` con ruta. | Precio real o comparable y limite exacto. | Nunca `completed` sin precio o comparable. |
| Marketplace instrumental bloqueado | Marca/modelo en eBay, ML, importador local, fabricante, manual/ficha, China B2B si aplica. | Modelo, estado, precio/ruta precio, reputacion y trazabilidad. | `needs_review` si falta regulatorio o soporte. |
| Modelo instrumental ambiguo | Manual/ficha, fotos/specs, version exacta, compatibilidad clinica, comparables por version. | Specs o motivo de descarte. | `blocked` si no se puede identificar. |
| Cero candidatos | Ampliar query controlada, registrar fuentes y descartes, comparar universo, proxima corrida. | 5+ fuentes o 3+ descartes con criterios. | `needs_review`, salvo universo muy robusto y score >= 75. |
| Login/credencial/paywall | No usar credenciales; buscar fuente publica, cache/snippet, espejo o comparable. | Bloqueo registrado y alternativa usada. | `blocked` si no se intento alternativa. |

## front_specific_thresholds

```yaml
inmobiliaria_junin:
  scope: Plaza 9 de Julio + 12 cuadras, casas para reformar
  min_sources_attempted: 5
  min_fallback_routes_if_blocked: 2
  zero_candidate_min_rejections: 3
  candidate_required_fields:
    - ubicacion_o_radio
    - precio_o_comparable
    - superficie_o_estado
    - refaccion_estimable
    - tesis_oportunidad
    - riesgo_documental
    - next_action
  completed_requires_score: 75

instrumental_neuro_columna:
  min_sources_attempted: 5
  min_fallback_routes_if_blocked: 2
  candidate_required_fields:
    - marca_modelo_version
    - precio_o_ruta_precio
    - compatibilidad_clinica
    - reputacion_vendedor
    - trazabilidad_regulatoria_si_aplica
    - soporte_repuestos_garantia
    - next_action
  completed_requires_score: 75
  force_needs_review_if:
    - missing_traceability
    - seller_unclear
    - price_not_comparable
```

## examples

### Inmobiliaria

```text
Sitio directo no abre.
Ruta A: busqueda "casa Junin Plaza 9 de Julio <calle>".
Ruta B: portal espejo Zonaprop/Argenprop/ML.
Ruta C: comparables dentro de 12 cuadras.
Resultado: 0 candidatos, 6 fuentes, 4 descartes por precio fuera de rango.
Status: needs_review; proxima accion: repetir corrida en 7 dias o ampliar radio.
```

### Instrumental

```text
Listing de instrumental sin precio.
Ruta A: buscar marca/modelo en eBay.
Ruta B: Mercado Libre/importador local.
Ruta C: fabricante/manual para version exacta.
Resultado: precio comparable parcial, trazabilidad no validada.
Status: needs_review; decision: watchlist, no comprar ni pedir aprobacion.
```

### Error que debe bloquear

```text
"No pude abrir MercadoLibre y no encontre oportunidades."
Sin fuentes espejo, sin comparables y sin descartes.
Status minimo: blocked.
```

## automation_hooks

| Hook | Dispara | Accion automatica |
|---|---|---|
| `source_blocked` | outcome `blocked/error` en fuente principal | Exigir 2 rutas alternativas antes de permitir conclusion. |
| `zero_candidates` | candidatos = 0 | Exigir universo, descartes, queries y proxima corrida. |
| `candidate_missing_price` | precio nulo sin comparable | Bajar a `needs_review`. |
| `instrumental_missing_traceability` | instrumento/implante sin regulatorio/soporte | Bajar a `needs_review` o `blocked`. |
| `contains_failure_phrase` | "no pude/no encontre/no hay oportunidades" | Bloquear si no hay `fallback_routes_used`. |
| `score_below_75` | score final < 75 | No permitir `completed`. |
| `pablo_escalation_needed` | score 50-74 con candidato fuerte o bloqueo dificil | Crear job a Pablo con evidencia parcial. |

## failure_language_ban

Frases prohibidas sin evidencia y fallback:

- "No pude abrir..."
- "No encontre nada."
- "No hay oportunidades."
- "El mercado esta agotado."
- "No se pudo validar."
- "No hay precio disponible."

Formato permitido:

```text
La fuente X fallo. Se probaron A, B y C.
Evidencia: <fuentes/queries/descartes/comparables>.
Limite exacto: <dato faltante>.
Proxima accion: <ruta concreta y responsable>.
Status: needs_review|blocked.
```

## risks / limits

- Este playbook valida calidad operativa del radar, no verdad de mercado.
- No se navegaron fuentes ni se verificaron precios actuales por restriccion del job.
- Minimos muy altos pueden incentivar relleno; por eso descartes y comparables cuentan mas que cantidad.
- En instrumental medico, seguridad, trazabilidad y soporte pesan mas que precio.
- Ruta alternativa si no hay fuentes suficientes: cerrar `blocked` con rutas intentadas y siguiente corrida, no `completed`.

## recommendation

Integrar `source_recovery` como paso previo obligatorio al validator anti-empty. Si una fuente falla, 5.3 debe ejecutar rutas alternativas y producir `sources_attempted`, `fallback_routes_used`, `rejected_candidates` y `next_action`. Pablo solo recibe `needs_review` con evidencia o candidatos fuertes.

## confidence

Alta para rutas, lenguaje prohibido y hooks porque derivan de reglas locales repetidas. Media para thresholds numericos hasta calibrar con corridas reales.

## evidence_paths

- `jobs/20260528T132759-radares-source-recovery-playbook.md`
- `context/fronts/radares.md`
- `results/20260525T122941-radar-anti-empty-script-spec.result.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `results/20260527T011700-radares-source-recovery-playbook.result.md`

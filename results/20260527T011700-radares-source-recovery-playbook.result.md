---
job_id: 20260527T011700-radares-source-recovery-playbook
worker: personal-xh
status: completed
completed_at: 2026-05-27T01:19:00-03:00
front: INVERSIONES
no_external_actions: true
no_secrets: true
---

# Resultado - Radares source recovery playbook

## summary honesto

El playbook anti bloqueo debe impedir que un radar cierre con "no pude" cuando
solo fallo una fuente. Para inmobiliaria e instrumental, una fuente bloqueada es
un evento de recuperacion: se prueban rutas alternativas, se documenta universo,
se comparan candidatos y recien entonces se decide `completed`, `needs_review` o
`blocked`.

Evidencia: el frente Radares exige fuentes, candidatos, descartes, comparables y
rutas alternativas. Inferencia: el source recovery debe correr antes del gate
anti-empty. Opinion: Pablo solo debe escalar cuando 5.3 agoto rutas razonables o
hay candidatos fuertes con riesgo dificil.

No navegue, no contacte vendedores, no use credenciales y no hice acciones
externas.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T011700-radares-source-recovery-playbook.md` | Revisada | Entregables y restricciones. |
| `context/fronts/radares.md` | Revisada | Regla anti informe vacio y fuentes alternativas. |
| `results/20260525T122941-radar-anti-empty-script-spec.result.md` | Revisada | Script/gate, thresholds y fallback routes. |
| `results/20260525T120001-radares-anti-informe-vacio-v1.result.md` | Revisada | Contrato radar, scorecards y division 5.3/Pablo. |

## source_recovery_routes

| Bloqueo | Ruta 1 | Ruta 2 | Ruta 3 | Cierre permitido |
| --- | --- | --- | --- | --- |
| Web inmobiliaria no abre | Buscar direccion/zona exacta | Portal espejo: Zonaprop/Argenprop/ML/mapa | Snippet/cache + comparables de zona | `needs_review` si no hay candidatos pero hay universo documentado |
| Sin precio inmobiliario | Mismo inmueble en portal espejo | Comparables por radio y m2 | Marcar `pendiente_precio` con ruta concreta | Nunca `completed` sin precio o comparable |
| Marketplace instrumental bloqueado | Buscar marca/modelo | eBay/ML/local/importado | Fabricante/distribuidor/regulatorio | `needs_review` si faltan trazabilidad o precio |
| Modelo ambiguo | Buscar manual/ficha tecnica | Fotos/specs de vendedores | Comparables por version | Descartar si compatibilidad no se valida |
| Cero candidatos | Ampliar query controlada | Registrar descartes | Programar proxima corrida | `needs_review`, no `completed`, salvo universo fuerte |

## front_specific_thresholds

```yaml
inmobiliaria_junin:
  min_sources_attempted: 5
  min_fallback_routes_if_blocked: 2
  min_rejected_candidates_if_zero_found: 3
  required_fields_for_candidate:
    - ubicacion
    - precio
    - superficie_o_comparable
    - tesis_oportunidad
    - riesgo
    - next_action
instrumental_columna_neuro:
  min_sources_attempted: 5
  min_fallback_routes_if_blocked: 2
  required_fields_for_candidate:
    - marca_modelo
    - precio_o_ruta_precio
    - compatibilidad
    - reputacion_vendedor
    - trazabilidad_regulatoria_si_aplica
    - next_action
```

## examples

### Inmobiliaria

```text
Fuente directa no abre -> buscar "casa Junin Plaza 9 de Julio <calle>" -> revisar
portal espejo -> registrar 4 descartes por precio/zona -> comparar 2 propiedades
similares -> si no hay oportunidad, status needs_review con proxima corrida.
```

### Instrumental

```text
Listing sin precio -> buscar mismo modelo en eBay/ML/importador -> comparar
estado y accesorios -> si falta trazabilidad, candidate decision watchlist o
needs_review, nunca comprar ni pedir aprobacion directa.
```

## automation_hooks

- `source_blocked`: dispara rutas alternativas obligatorias.
- `zero_candidates`: exige descartes documentados y proxima corrida.
- `candidate_missing_price`: baja status a `needs_review`.
- `instrumental_missing_traceability`: hard warning medico/regulatorio.
- `contains_no_pude`: bloquea si no hay `fallback_routes_used`.
- `score_below_75`: no permite `completed`.

## failure_language_ban

Frases prohibidas sin rutas alternativas:

- "No pude abrir la web."
- "No encontre nada."
- "No hay oportunidades."
- "El mercado esta agotado."
- "No se pudo validar."

Formato permitido:

```text
La fuente X fallo. Se probaron A, B y C. Resultado: <evidencia>.
Queda <next_action> porque <limite exacto>.
```

## risks / limits

- Este playbook no valida la verdad del mercado; valida que el radar no cierre
  vacio.
- Demasiados minimos pueden incentivar relleno; por eso los descartes y
  comparables deben contar mas que cantidad bruta.
- Instrumental medico requiere criterio conservador: trazabilidad y soporte
  pesan mas que precio.

## recommendation

Integrar este playbook como paso previo a `validate_radar_report.py`: si una
fuente falla, el agente debe ejecutar rutas alternativas antes de escribir el
resultado. Pablo debe recibir solo `needs_review` con evidencia parcial o
candidatos fuertes de riesgo.

## confidence

Alta para rutas y lenguaje prohibido; media para thresholds hasta calibrar con
corridas reales.

## evidence_paths

- `jobs/20260527T011700-radares-source-recovery-playbook.md`
- `context/fronts/radares.md`
- `results/20260525T122941-radar-anti-empty-script-spec.result.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`

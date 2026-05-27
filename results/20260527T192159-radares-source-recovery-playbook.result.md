---
job_id: 20260527T192159-radares-source-recovery-playbook
worker: personal-xh
status: completed
completed_at: 2026-05-27T19:26:06-03:00
front: INVERSIONES
no_external_actions: true
no_secrets: true
---

# Resultado - Radares source recovery playbook

## summary honesto

El radar no puede cerrar con "no pude" cuando fallo una fuente. Para
inmobiliaria e instrumental, una fuente bloqueada dispara recuperacion: busqueda
dirigida, portales espejo, snippets/cache, comparables, fuente oficial o
fabricante, y recien despues status `completed`, `needs_review` o `blocked`.

Separacion pedida:

- Evidencia: `context/fronts/radares.md` exige fuentes, candidatos, descartes,
  rutas alternativas, comparables y proxima accion.
- Inferencia: source recovery debe correr antes del gate anti-empty.
- Opinion: Pablo debe entrar solo cuando 5.3 agoto rutas razonables o hay
  candidatos fuertes con riesgo dificil.

No navegue, no contacte vendedores, no use credenciales y no hice acciones
externas.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T192159-radares-source-recovery-playbook.md` | Revisada | Objetivo, restricciones y secciones requeridas. |
| `context/fronts/radares.md` | Revisada | Estado canonico, anti informe vacio y source recovery obligatorio. |
| `results/20260525T122941-radar-anti-empty-script-spec.result.md` | Revisada | Gate, schema, thresholds y fallback routes. |
| `results/20260525T120001-radares-anti-informe-vacio-v1.result.md` | Revisada | Contrato radar, scorecards y division 5.3/Pablo. |
| `results/20260527T011700-radares-source-recovery-playbook.result.md` | Revisada como fuente operativa | Playbook previo, hooks y lenguaje permitido. |

## source_recovery_routes

| Bloqueo | Ruta alternativa obligatoria | Evidencia minima | Cierre permitido |
| --- | --- | --- | --- |
| Web inmobiliaria no abre | Query por direccion/zona, portal espejo, snippet/cache, comparables por radio. | Query usada, portales, descartes y comparables. | `needs_review` si no hay candidato pero universo documentado. |
| Precio inmobiliario faltante | Mismo inmueble en otro portal, comparables por m2/radio, marcar `pendiente_precio`. | Fuente del comparable y limite exacto. | Nunca `completed` sin precio o comparable. |
| Marketplace instrumental bloqueado | Marca/modelo, eBay/ML/importador local, fabricante/distribuidor. | Modelo, precio/ruta precio, vendedor y trazabilidad. | `needs_review` si falta trazabilidad. |
| Producto/modelo ambiguo | Manual/ficha tecnica, fotos/specs, version exacta. | Spec o razon de descarte. | Descartar si compatibilidad no se valida. |
| Cero candidatos | Ampliar query controlada, registrar descartes, programar proxima corrida. | Fuentes, cantidad de descartes, criterio de agotamiento. | `needs_review`, no `completed`, salvo universo muy fuerte. |
| Fuente requiere login | No usar credenciales; buscar espejo/publica. | Fuente bloqueada y alternativa usada. | `blocked` si no hay alternativa y el radar dependia de esa fuente. |

## front_specific_thresholds

```yaml
inmobiliaria_junin:
  min_sources_attempted: 5
  min_fallback_routes_if_blocked: 2
  min_rejected_candidates_if_zero_found: 3
  required_candidate_fields:
    - ubicacion
    - precio_o_comparable
    - superficie_o_estado
    - tesis_oportunidad
    - riesgos
    - next_action
instrumental_neuro_columna:
  min_sources_attempted: 5
  min_fallback_routes_if_blocked: 2
  required_candidate_fields:
    - marca_modelo_version
    - precio_o_ruta_precio
    - compatibilidad_clinica
    - reputacion_vendedor
    - trazabilidad_regulatoria_si_aplica
    - soporte_repuestos
    - next_action
```

Estados:

- `completed`: score >= 75, secciones completas y sin bloqueo critico.
- `needs_review`: evidencia parcial, 0 candidatos con universo documentado, o
  instrumental con dudas de trazabilidad.
- `blocked`: fuente bloqueada sin alternativa, reporte con frases vacias, o
  menos de minimo de fuentes.

## examples

Inmobiliaria:

```text
No abre portal directo. Se busca "casa Junin Plaza 9 de Julio <zona/calle>",
se revisan portales espejo, se registran 4 descartes por precio/zona y 2
comparables. Si no aparece oportunidad, queda needs_review con proxima corrida.
```

Instrumental:

```text
Listing sin precio. Se busca mismo modelo en eBay, Mercado Libre, importador y
fabricante. Si hay precio pero no trazabilidad/regulatorio, decision watchlist o
needs_review, nunca comprar/contactar.
```

Formato permitido:

```text
La fuente X fallo. Se probaron A, B y C. Resultado: <evidencia>.
Queda <next_action> porque <limite exacto>.
```

## automation_hooks

- `source_blocked`: exige al menos 2 rutas alternativas.
- `zero_candidates`: exige descartes y proxima corrida.
- `candidate_missing_price`: baja a `needs_review`.
- `instrumental_missing_traceability`: hard warning medico/regulatorio.
- `contains_no_pude`: bloquea si no hay `fallback_routes_used`.
- `score_below_75`: no permite `completed`.
- `candidate_without_next_action`: baja a `needs_review`.

Hook sugerido en pipeline:

```bash
python3 scripts/qa/validate_radar_report.py results/<job_id>.result.md --kind inmobiliaria
python3 scripts/qa/validate_radar_report.py results/<job_id>.result.md --kind instrumental --candidates results/<job_id>.candidates.json
```

## failure_language_ban

Frases bloqueadas sin rutas alternativas:

- "No pude abrir la web."
- "No encontre nada."
- "No hay oportunidades."
- "El mercado esta agotado."
- "No se pudo validar."
- "No hay datos suficientes" sin proxima accion.

Regla: si aparece una frase de fallo, debe incluir `attempted_routes`,
`fallback_routes_used`, limite exacto y proxima accion.

## risks / limits

- Este playbook valida calidad del proceso, no verdad del mercado.
- Los minimos pueden incentivar relleno; por eso comparables y descartes pesan
  mas que cantidad bruta.
- Instrumental medico debe ser conservador: trazabilidad, soporte y seguridad
  pesan mas que precio.
- No se hicieron acciones externas ni navegacion real.

## recommendation

Integrar este playbook como paso previo a `validate_radar_report.py`. Si una
fuente falla, 5.3 debe ejecutar rutas alternativas antes del resultado. Pablo
solo deberia recibir `needs_review` con evidencia parcial o candidatos fuertes de
riesgo.

## confidence

Alta para rutas y lenguaje prohibido; media para thresholds hasta calibrar con
corridas reales.

## evidence_paths

- `jobs/20260527T192159-radares-source-recovery-playbook.md`
- `context/fronts/radares.md`
- `results/20260525T122941-radar-anti-empty-script-spec.result.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `results/20260527T011700-radares-source-recovery-playbook.result.md`
- `claims/20260527T192159-radares-source-recovery-playbook.json`

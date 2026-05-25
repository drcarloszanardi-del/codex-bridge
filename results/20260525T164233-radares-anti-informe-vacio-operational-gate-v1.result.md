---
id: 20260525T164233-radares-anti-informe-vacio-operational-gate-v1
job_id: 20260525T164233-radares-anti-informe-vacio-operational-gate-v1
created_at: 2026-05-25T16:44:37-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - RADARES anti informe vacio operational gate v1

Job: `20260525T164233-radares-anti-informe-vacio-operational-gate-v1`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary

Se define un gate operativo para que ningun radar de inmobiliaria, inversiones o instrumental cierre como `completed` si no trae evidencia suficiente, rutas alternativas, comparables, candidatos/descartes y una proxima accion concreta. El gate no fuerza oportunidades falsas: fuerza calidad de busqueda y honestidad operacional.

No navegue, no contacte vendedores, no compre, no use credenciales y no toque ObraCash. Este resultado es una especificacion implementable para que el orquestador la convierta en validator y regla de cierre.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `jobs/20260525T164233-radares-anti-informe-vacio-operational-gate-v1.md` | 1 | Contrato del job y secciones esperadas. |
| `context/fronts/radares.md` | 1 | Estado canonico: Junin, instrumental, 5.3/Pablo y anti informe vacio. |
| `decisions/radar_scorecards_v1.md` | 1 | Campos y scoring base por frente. |
| `results/20260525T021032-radar-scorecards-inmobiliaria-instrumental-v1.result.md` | 1 | Scorecards creados y decision watchlist/investigar/descartar. |
| `results/20260525T103407-rescate-radar-inversiones-sin-no-puedo-v1.result.md` | 1 | Radar rescatado con rutas alternativas y oportunidades. |
| `results/20260525T103946-inmobiliaria-junin-casas-reforma-radio-12-cuadras-v2.result.md` | 1 | Ejemplo inmobiliario con shortlist, comparables y pendientes. |
| `results/20260525T103947-instrumental-neuro-columna-china-vs-argentina-v2.result.md` | 1 | Ejemplo instrumental con matriz, China/Argentina y riesgo ANMAT. |
| `results/20260525T103949-anti-informe-vacio-qa-radares-v1.result.md` | 1 | Gate QA previo, thresholds y CLI sugerida. |
| `results/20260525T120001-radares-anti-informe-vacio-v1.result.md` | 1 | Contrato completo, fallback routes, scorecards y division 5.3/Pablo. |
| `results/20260525T122941-radar-anti-empty-script-spec.result.md` | 1 | Schema JSON, gate rules, exit codes y qa examples. |
| `results/20260525T124718-radares-source-recovery-playbook.result.md` | 1 | Ladder de recuperacion por fuente bloqueada. |

## coverage_table

| Requisito del job | Estado | Donde queda cubierto |
|---|---|---|
| Contrato minimo de reporte | cubierto | `minimum_viable_report_contract` |
| Rutas alternativas | cubierto | `source_recovery_ladder` |
| Bloqueadores de informe vacio | cubierto | `empty_report_blockers` |
| Inmobiliaria | cubierto | `real_estate_specific_checks` |
| Instrumental | cubierto | `instrumental_specific_checks` |
| Template Telegram | cubierto | `telegram_report_template` |
| Pseudocodigo deterministico | cubierto | `deterministic_gate_pseudocode` |
| Plan de integracion | cubierto | `orchestrator_integration_plan` |

## minimum_viable_report_contract

Todo radar debe producir, al menos:

```yaml
radar_report:
  job_id: string
  front: inmobiliaria | inversiones | instrumental
  scope:
    query: string
    geography_or_market: string
    constraints: [string]
    forbidden_actions: ["contactar", "comprar", "login", "credenciales"]
  run_summary:
    claimed_status: completed | needs_review | blocked
    required_status_by_gate: completed | needs_review | blocked
    score: 0..100
    honest_reason: string
  sources_attempted:
    - name: string
      url_or_query: string
      type: direct_page | marketplace | search | pdf | official | snippet | cache | local_context | comparable
      outcome: success | blocked | no_results | partial | error
      evidence: string
      alternative_used: string | null
  fallback_routes_used:
    - blocked_or_empty_source: string
      route: string
      outcome: success | partial | failed
      evidence: string
  candidates:
    - id: string
      title: string
      source: string
      price: string | number | null
      location_or_specs: string
      comparable_basis: [string]
      opportunity_thesis: string
      risks: [string]
      missing_fields: [string]
      decision: investigar | watchlist | descartar | pedir_aprobacion
      next_action: string
  rejected_candidates:
    - title: string
      source: string
      reason: string
  conclusion:
    recommendation: string
    confidence: low | medium | medium-high | high
    next_run_or_handoff: string
```

Secciones markdown obligatorias si no hay JSON:

```text
## summary
## fuentes_revisadas
## rutas_alternativas
## candidatos
## comparables
## descartes
## pendientes_y_proxima_accion
## recommendation
## confidence
## evidence_paths
```

## source_recovery_ladder

| Bloqueo o vacio | Rutas obligatorias antes de cerrar |
|---|---|
| Web inmobiliaria no abre | Buscar por direccion/zona, buscar por inmobiliaria + titulo exacto, marketplace espejo, snippets/cache, comparables misma zona. |
| Aviso inmobiliario sin precio | Buscar replica exacta, listado de la inmobiliaria, PDF/revista local, comparable por radio y dejar `pending_price` con ruta concreta. |
| MercadoLibre/Zonaprop bloquea | Buscar codigo de publicacion, titulo exacto, cache/snippet, misma propiedad en otro portal, inmobiliaria de origen. |
| Cero casas candidatas | Reportar queries, fuentes, descartes y criterio de agotamiento; ampliar radio o cambiar tipo solo si el job lo permite. |
| Producto medico ambiguo | Buscar marca/modelo/version, proveedor local, marketplace local, China B2B, regulatorio/trazabilidad. |
| Implante barato sin documentacion | No recomendar compra; pasar a benchmark/watchlist hasta ANMAT/importador/lote/tarjeta de implante. |
| Fuente requiere login/credencial | No usar credencial; buscar fuente publica equivalente y marcar limite. |
| Precio faltante | No estimar como hecho; usar comparables y dejar ruta para confirmacion. |

## empty_report_blockers

Hard blockers: el resultado no puede ser `completed` si ocurre cualquiera:

- Frases tipo `no pude`, `no encontre`, `no hay oportunidades`, `pagina bloqueada` sin rutas alternativas.
- Menos de 5 fuentes intentadas en radar amplio.
- 0 candidatos y menos de 5 descartes documentados.
- Fuente principal bloqueada sin 2 rutas alternativas.
- Candidatos sin fuente/link/query.
- Candidatos sin decision operativa.
- Candidatos sin `next_action`.
- Sin comparables o sin explicar por que no aplican.
- Precio ausente sin `pending_price` y ruta concreta.
- Inmobiliaria sin ubicacion/zona verificable.
- Instrumental medico sin riesgo regulatorio/trazabilidad cuando aplica.
- Implante medico con recomendacion `comprar` sin ANMAT/importador/lote/registro.
- Mezcla acciones externas no autorizadas: contactar, comprar, login, credenciales.

Estados por score:

| Score | Estado maximo permitido |
|---:|---|
| 75-100 | `completed` si no hay hard blockers |
| 50-74 | `needs_review` |
| 0-49 | `blocked` |

## real_estate_specific_checks

Campos requeridos por candidato inmobiliario:

```yaml
direccion_o_zona:
precio:
superficie_terreno:
superficie_cubierta:
estado_refaccion:
servicios:
distancia_o_radio_objetivo:
comparables_misma_zona:
tesis_oportunidad:
riesgos:
decision:
next_action:
```

Scoring recomendado:

| Rubro | Puntos |
|---|---:|
| Ubicacion Plaza 9 de Julio / radio 12 cuadras | 15 |
| Precio vs comparables | 20 |
| Estado de refaccion estimable | 15 |
| Superficie y servicios verificables | 10 |
| Liquidez/reventa/alquiler | 10 |
| Riesgo legal/documental bajo o identificado | 10 |
| Margen post refaccion | 15 |
| Claridad de next action | 5 |

Decisiones validas:

- `investigar`: candidato con fuente, precio y tesis.
- `pedir_aprobacion`: candidato fuerte que requiere contacto autorizado.
- `watchlist`: falta precio/dato central pero hay ruta concreta.
- `descartar`: riesgo o falta de fit documentado.

## instrumental_specific_checks

Separar tres categorias:

1. Instrumental reusable no implantable.
2. Equipamiento usado/electromecanico.
3. Implantes o productos de alto riesgo.

Campos requeridos:

```yaml
marca_modelo_version:
nuevo_usado:
precio_origen:
precio_local_comparable:
compatibilidad_clinica:
garantia_repuestos_soporte:
vendedor_origen:
trazabilidad_regulatoria:
riesgo_importacion:
decision:
next_action:
```

Reglas duras:

- Implantes sin registro/trazabilidad/importador habilitado no pueden quedar como `comprar`.
- Marketplace chino de implantes solo puede servir como benchmark de spread, no como recomendacion de compra.
- Instrumental usado requiere estado, procedencia, garantia, compatibilidad y servicio tecnico.
- Reusable no implantable puede avanzar como `investigar` si hay comparable local y lista de piezas.
- Para columna/neuro, seguridad y trazabilidad pesan mas que descuento.

## telegram_report_template

Plantilla breve que el orquestador puede usar si decide informar al Doctor, sin ruido tecnico:

```text
Radar actualizado.

Estado: <completed | needs_review | blocked>
Score gate: <0-100>
Fuentes revisadas: <n>
Rutas alternativas usadas: <n>
Candidatos: <n>
Descartes documentados: <n>

Mejores candidatos:
1. <titulo> - <precio> - <decision> - <por que mirar>
2. <titulo> - <precio> - <decision> - <por que mirar>
3. <titulo> - <precio> - <decision> - <por que mirar>

Pendiente concreto:
<accion que requiere aprobacion o proxima busqueda>
```

Reglas del template:

- No decir `enviado` sin `message_id` real si se usa Telegram.
- No incluir diffs, logs, stack traces ni secretos.
- Si el gate queda `blocked`, explicar en una linea que falta evidencia suficiente y cual es la proxima ruta.

## deterministic_gate_pseudocode

```python
REQUIRED_SECTIONS = [
    "summary",
    "fuentes_revisadas",
    "rutas_alternativas",
    "candidatos",
    "comparables",
    "descartes",
    "pendientes_y_proxima_accion",
    "recommendation",
    "confidence",
    "evidence_paths",
]

FAILURE_PHRASES = ["no pude", "no encontre", "no hay oportunidades", "pagina no abre"]

def validate_radar_report(report, kind):
    errors = []
    warnings = []
    score = 100

    missing = missing_sections(report, REQUIRED_SECTIONS)
    if missing:
        errors.append(("missing_sections", missing))
        score -= 25

    sources = extract_sources(report)
    fallbacks = extract_fallbacks(report)
    candidates = extract_candidates(report)
    rejects = extract_rejects(report)

    if contains_failure_phrase(report.text, FAILURE_PHRASES) and not fallbacks:
        errors.append(("empty_failure_phrase_without_fallback", None))
        score -= 35

    if len(sources) < min_sources(kind):
        errors.append(("insufficient_sources", len(sources)))
        score -= 20

    if has_blocked_source(sources) and count_fallbacks_for_blocked(sources, fallbacks) < 2:
        errors.append(("blocked_source_without_two_fallbacks", None))
        score -= 20

    if len(candidates) == 0:
        if len(sources) >= 5 and len(rejects) >= 5:
            warnings.append(("no_candidates_but_universe_documented", None))
            score = min(score, 74)
        else:
            errors.append(("empty_universe", None))
            score -= 35

    for candidate in candidates:
        if not candidate.source:
            errors.append(("candidate_missing_source", candidate.id))
            score -= 10
        if not candidate.decision:
            errors.append(("candidate_missing_decision", candidate.id))
            score -= 10
        if not candidate.next_action:
            errors.append(("candidate_missing_next_action", candidate.id))
            score -= 10
        if not candidate.price and not candidate.pending_price_route:
            errors.append(("candidate_missing_price_without_route", candidate.id))
            score -= 10

    if kind == "inmobiliaria":
        errors += validate_real_estate(candidates)
    if kind == "instrumental":
        errors += validate_instrumental(candidates)

    score = max(0, min(100, score))
    hard_block = any(error[0] in HARD_BLOCKERS for error in errors)
    if hard_block or score < 50:
        required_status = "blocked"
    elif score < 75 or errors:
        required_status = "needs_review"
    else:
        required_status = "completed"

    return {
        "ok": required_status == "completed",
        "score": score,
        "required_status": required_status,
        "errors": errors,
        "warnings": warnings,
    }
```

Exit codes sugeridos:

- `0`: `completed` permitido.
- `2`: `needs_review` requerido.
- `3`: `blocked` requerido.

## orchestrator_integration_plan

1. Crear `scripts/qa/validate_radar_report.py`.
2. Agregar fixtures:

```text
fixtures/radares/empty_no_sources.md
fixtures/radares/blocked_with_fallbacks.md
fixtures/radares/inmobiliaria_pass_junin.md
fixtures/radares/instrumental_implante_bad_buy.md
fixtures/radares/no_candidates_needs_review.md
```

3. Hacer que todo job radar ejecute validator antes de commit.
4. Si validator devuelve `needs_review`, crear job a Pablo con errores y mejores candidatos.
5. Si devuelve `blocked`, el resultado debe incluir errores, rutas faltantes y siguiente accion, no informe vacio.
6. Guardar opcionalmente `results/<job_id>.candidates.json` para que el validator no dependa solo de parsing markdown.
7. Integrar al dashboard/bridge: score, estado requerido y razon visible para el orquestador.
8. Aplicar mas conservadoramente a instrumental medico: un riesgo regulatorio puede bajar `completed` a `needs_review` aunque el score numerico sea alto.

## risks_limits

- El gate valida calidad del reporte, no verdad absoluta del mercado.
- Los thresholds deben calibrarse con corridas reales; si son demasiado rigidos, pueden incentivar candidatos flojos.
- Para instrumental medico, un precio muy bajo no compensa falta de trazabilidad.
- Para inmobiliaria, comparables pueden quedar obsoletos; se debe registrar fecha de revision.
- Si el agente no tiene navegacion autorizada, debe reportar rutas alternativas permitidas y estado `needs_review/blocked`, no inventar.

## recommendation

Implementar este gate como bloqueo obligatorio antes de aceptar radares. La primera version debe enfocarse en hard blockers: fuentes insuficientes, bloqueo sin alternativa, candidatos sin fuente/decision/next action, ausencia de comparables e instrumental medico sin trazabilidad. Luego calibrar score con 5 a 10 radares reales.

## confidence

Alta para contrato, blockers y ladder porque consolidan resultados previos ya alineados con el Doctor. Media para pesos numericos hasta calibracion con ejecuciones reales.

## evidence_paths

- `jobs/20260525T164233-radares-anti-informe-vacio-operational-gate-v1.md`
- `context/fronts/radares.md`
- `decisions/radar_scorecards_v1.md`
- `results/20260525T021032-radar-scorecards-inmobiliaria-instrumental-v1.result.md`
- `results/20260525T103407-rescate-radar-inversiones-sin-no-puedo-v1.result.md`
- `results/20260525T103946-inmobiliaria-junin-casas-reforma-radio-12-cuadras-v2.result.md`
- `results/20260525T103947-instrumental-neuro-columna-china-vs-argentina-v2.result.md`
- `results/20260525T103949-anti-informe-vacio-qa-radares-v1.result.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `results/20260525T122941-radar-anti-empty-script-spec.result.md`
- `results/20260525T124718-radares-source-recovery-playbook.result.md`

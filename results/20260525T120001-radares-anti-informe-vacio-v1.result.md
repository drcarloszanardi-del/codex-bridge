# Resultado - radares anti informe vacio v1

Job: `20260525T120001-radares-anti-informe-vacio-v1`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

Se diseno un gate implementable para que los radares de inmobiliaria, inversiones e instrumental no puedan cerrar con un informe vacio, un "no pude" o cero oportunidades sin evidencia. No se navego ni se contacto a terceros. La salida define contrato, rutas alternativas, thresholds, scorecards y plan para que 5.3 ejecute barridos rutinarios y Pablo intervenga solo en casos dificiles.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `jobs/20260525T120001-radares-anti-informe-vacio-v1.md` | 1 | Contrato y criterio de terminado. |
| `context/fronts/radares.md` | 1 | Estado canonico y regla anti informe vacio. |
| `decisions/radar_scorecards_v1.md` | 1 | Campos y scoring base para inmobiliaria/instrumental. |
| `results/20260525T103949-anti-informe-vacio-qa-radares-v1.result.md` | 1 | Gate previo, thresholds, CLI sugerido. |
| Jobs/results previos de radares en repo | varios referenciados | Evidencia de frentes: inmobiliaria Junin, instrumental China/Argentina, rescate radar. |

## coverage_table

| Area | Estado | Evidencia |
|---|---|---|
| Contrato radar minimo | revisado/propuesto | Se consolidan secciones obligatorias y schema de candidato. |
| Anti-empty gate | revisado/propuesto | Se definen estados `completed`, `needs_review`, `blocked`, `delegated_to_pablo`. |
| Rutas alternativas | propuesto | Direct page, snippets/cache, marketplaces, PDFs, comparables, fuente espejo, OCR/captura si autorizado. |
| Scorecards | propuesto | Inmobiliaria y instrumental con campos, pesos y descartes. |
| Integracion 5.3/Pablo | propuesto | 5.3 barre y valida; Pablo revisa degradados, ranking y excepciones. |

## radar_contract

Todo radar debe producir, como minimo:

```yaml
radar_report:
  job_id:
  kind: inmobiliaria | instrumental | inversion_general
  scope:
    query:
    geography_or_market:
    constraints:
    forbidden_actions: ["contactar", "comprar", "login", "credenciales"]
  run_summary:
    started_at:
    completed_at:
    status: completed | needs_review | blocked | delegated_to_pablo
    score:
    reason:
  sources_attempted:
    - name:
      url_or_query:
      source_type: direct_page | marketplace | search | pdf | official | snippet | comparable | cached | local_context
      outcome: success | blocked | no_results | partial | error
      evidence:
      next_route_if_failed:
  fallback_routes_used:
    - blocked_source:
      alternative:
      outcome:
  candidates:
    - id:
      title:
      category:
      source:
      evidence_type:
      price:
      location_or_specs:
      comparable_basis:
      opportunity_thesis:
      risks:
      missing_fields:
      decision: investigar | watchlist | descartar | pedir_aprobacion
      next_action:
  rejected_candidates:
    - title:
      source:
      reason:
  conclusion:
    recommendation:
    confidence:
    next_run_or_handoff:
```

## anti_empty_gate

| Condicion | Resultado permitido | Motivo |
|---|---|---|
| 0 candidatos + menos de 5 fuentes | `blocked` | No hay universo revisado suficiente. |
| 0 candidatos + 5+ fuentes + descartes documentados + comparables | `needs_review` | Puede ser mercado agotado, pero requiere revision. |
| Fuente principal bloqueada + sin alternativa | `blocked` | Bloqueo tecnico no prueba ausencia de oportunidad. |
| Fuente principal bloqueada + 2+ rutas alternativas usadas | `needs_review` o `completed` | Depende de candidatos y comparables. |
| Candidatos sin precio y sin ruta concreta para obtenerlo | `needs_review` | No permite decision. |
| Instrumental/implantes sin riesgo regulatorio | `needs_review` | Falta ANMAT/trazabilidad/importador/garantia cuando aplica. |
| Contiene "no pude" sin `fallback_routes_used` | `blocked` | Informe vacio. |
| Score >= 75 y secciones completas | `completed` | Cumple contrato. |
| Score 50-74 | `needs_review` | Evidencia parcial; no cerrar como final. |
| Score < 50 | `blocked` | Trabajo insuficiente. |

## fallback_routes

| Bloqueo | Rutas obligatorias antes de cerrar |
|---|---|
| Web inmobiliaria no abre | Busqueda dirigida por direccion/zona, snippet/cache, marketplace espejo, mapa/zonaprop/argenprop/ML, comparables de misma zona. |
| Marketplace sin precio | Buscar mismo item/modelo, pedir `pendiente_precio` + ruta concreta, no estimar como hecho. |
| Producto chino ambiguo | Fabricante, Alibaba/1688/GlobalSources, distribuidor local, eBay/ML, regulatorio/ANMAT si es medico. |
| Instrumental usado sin marca/modelo | Rechazar como candidato fuerte; pasar a `watchlist` solo si hay fotos/specs y ruta para validar. |
| No hay candidatos | Reportar universo: queries, fuentes, cantidad de descartes, criterio de agotamiento y proxima corrida. |
| Fuente requiere login/credencial | No usar credenciales; buscar fuente publica o marcar `blocked_source` con alternativa. |

## scorecards

### inmobiliaria Junin

```yaml
score_inmobiliaria_100:
  ubicacion_plaza_9_julio_radio_12_cuadras: 15
  precio_vs_comparables: 20
  estado_refaccion_estimable: 15
  superficie_y_servicios_verificados: 10
  liquidez_reventa_alquiler: 10
  riesgo_legal_documental_bajo: 10
  margen_post_refaccion: 15
  claridad_next_action: 5
descartar_si:
  - sin ubicacion verificable
  - precio inexistente sin ruta concreta
  - ocupacion_conflicto_legal_no_aclarado
  - refaccion mayor no estimable
```

### instrumental / inversiones medicas

```yaml
score_instrumental_100:
  marca_modelo_version_claros: 10
  compatibilidad_clinica_real: 15
  precio_vs_importado_local_usado: 20
  garantia_repuestos_soporte: 10
  reputacion_vendedor: 10
  trazabilidad_regulatoria: 15
  liquidez_reventa: 10
  riesgo_importacion_controlado: 5
  claridad_next_action: 5
descartar_si:
  - implante_sin_registro_trazabilidad_o_importador
  - vendedor_no_identificable
  - precio_no_comparable
  - incompatibilidad_tecnica_no_resuelta
```

## implementation_plan

1. Crear `scripts/qa/validate_radar_report.py`.
2. Parametros: `--kind inmobiliaria|instrumental|general`, `--min-sources`, `--min-candidates`.
3. Validar secciones obligatorias y frases prohibidas.
4. Parsear candidatos YAML/Markdown.
5. Calcular score y status minimo permitido.
6. Integrar en pipeline de 5.3: ningun radar se commitea como `completed` si score < 75.
7. Si status `needs_review`, crear job a Pablo con el reporte parcial y la razon.
8. Si status `blocked`, exigir `attempted_routes`, `blocked_sources` y `next_action`.
9. Guardar cada corrida en `results/<job_id>.result.md` y opcional `results/<job_id>.candidates.json`.

## division_5_3_pablo

| Responsable | Hace | No hace |
|---|---|---|
| 5.3 | Barrido, parsing, tablas, screenshots/OCR si autorizado, comparables, scoring preliminar | No decide comprar/contactar ni cerrar vacio. |
| Pablo | Segunda pasada XH, rescate de bloqueos, ranking estrategico, deteccion de falsas oportunidades | No compra, no contacta, no usa credenciales. |
| Codex principal | Prioriza, autoriza acciones externas, integra con Doctor | No debe aceptar reportes sin gate. |

## exclusion_log

| Elemento | Decision | Motivo |
|---|---|---|
| Navegacion web real | excluida | Job prohibe navegar/contactar; solo diseno de gate. |
| Contactar vendedores | excluido | Accion externa prohibida. |
| Usar credenciales | excluido | Riesgo y prohibicion explicita. |
| Declarar mercado agotado | excluido como conclusion automatica | Solo puede inferirse con universo revisado y evidencia suficiente. |

## risks / limits

- Este gate no garantiza oportunidades reales; garantiza que el informe tenga evidencia y no sea vacio.
- Los thresholds deben calibrarse por frente; Junin/instrumental pueden requerir minimos distintos segun disponibilidad.
- Para instrumental medico, el gate debe ser mas conservador: trazabilidad/regulatorio pesan mas que margen.
- Si el agente fuerza candidatos malos para pasar el minimo, el scorecard debe penalizar riesgo y comparables debiles.

## recommendation

Implementar el validator como gate obligatorio en radares. Para la primera version, usar score >= 75 para `completed`, 50-74 para `needs_review`, <50 para `blocked`. El orquestador debe crear jobs a Pablo solo cuando 5.3 entregue `needs_review` por bloqueo dificil o ranking de candidatos fuertes.

## confidence

Alta para el contrato y reglas anti-vacio, porque consolidan reglas ya aceptadas en `context/fronts/radares.md`, `decisions/radar_scorecards_v1.md` y el resultado anti-informe-vacio previo. Media para thresholds numericos hasta calibrarlos con corridas reales.

## evidence_paths

- `jobs/20260525T120001-radares-anti-informe-vacio-v1.md`
- `context/fronts/radares.md`
- `decisions/radar_scorecards_v1.md`
- `results/20260525T103949-anti-informe-vacio-qa-radares-v1.result.md`
- `results/20260525T103407-rescate-radar-inversiones-sin-no-puedo-v1.result.md`
- `results/20260525T103946-inmobiliaria-junin-casas-reforma-radio-12-cuadras-v2.result.md`
- `results/20260525T103947-instrumental-neuro-columna-china-vs-argentina-v2.result.md`

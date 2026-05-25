# Resultado - radares source recovery playbook

Job: `20260525T124718-radares-source-recovery-playbook`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

El playbook anti bloqueo debe impedir que un radar cierre vacio por una fuente caida, login, bloqueo tecnico o falta de precio. La regla operativa es simple: cada bloqueo exige rutas alternativas documentadas, comparables o delegacion antes de cerrar. El resultado no navega ni busca oportunidades reales; entrega el protocolo para que 5.3 y el orquestador lo apliquen.

## source_counts

| Fuente | Archivos revisados | Uso |
|---|---:|---|
| `context/fronts/radares.md` | 1 | Canon de radar inmobiliario/instrumental y regla anti informe vacio. |
| `results/20260525T122941-radar-anti-empty-script-spec.result.md` | 1 | Schema, gate rules y script QA propuesto. |
| `results/20260525T120001-radares-anti-informe-vacio-v1.result.md` | 1 | Contrato, thresholds, scorecards y division 5.3/Pablo. |

## source_recovery_routes

| Bloqueo | Ruta 1 | Ruta 2 | Ruta 3 | Escalamiento |
|---|---|---|---|---|
| Web inmobiliaria no abre | Busqueda por direccion/zona y operador de sitio | Marketplace espejo: Zonaprop, Argenprop, ML, inmobiliarias locales | Snippets/cache y comparables misma zona | Pablo si hay candidato fuerte o precio ambiguo. |
| Marketplace bloquea o muestra parcial | Busqueda por titulo exacto/modelo/direccion | Fuente espejo o vendedor publicado en otra web | Captura/navegador real solo si autorizado por orquestador | `needs_review` con rutas usadas. |
| Sin precio | Mismo inmueble/producto en otra fuente | Comparables recientes del mismo radio o modelo | Marcar `pending_price` con ruta concreta para obtenerlo | No estimar precio como hecho. |
| Instrumental medico ambiguo | Fabricante/modelo/version | Distribuidor local, eBay/ML, China B2B | Registro/trazabilidad cuando aplique | Pablo antes de recomendar compra. |
| Cero candidatos | Ampliar queries y registrar descartes | Cambiar fuente/mercado espejo | Proxima corrida con criterio exacto | `needs_review`, no `completed`, salvo universo robusto. |
| Fuente requiere login/credenciales | No usar credenciales | Buscar fuente publica equivalente | Documentar limite | Orquestador decide si autoriza otro camino. |

## front_specific_thresholds

| Frente | Completed permitido si | Needs review si | Blocked si |
|---|---|---|---|
| Inmobiliaria Junin | 5+ fuentes, candidatos o descartes claros, ubicacion, precio/comparable, proxima accion | 0 candidatos con 5+ fuentes y descartes verificables | 0 candidatos con menos de 5 fuentes o sin alternativas. |
| Instrumental medico | Marca/modelo, precio comparable, reputacion, riesgo regulatorio/trazabilidad, decision prudente | Falta precio o trazabilidad parcial pero hay ruta concreta | Implante/equipo sin vendedor claro, sin regulatorio y con recomendacion de compra. |
| Inversion general | Tesis, comparables, riesgos y next action | Evidencia parcial con ruta de validacion | Conclusion sin fuentes o sin universo revisado. |

## examples

| Caso | Salida aceptable | Salida no aceptable |
|---|---|---|
| "ML no abre" | "ML bloqueado; se usaron snippets, eBay, web fabricante y comparable local; quedan 2 candidatos `needs_review`." | "No se pudo ver ML, sin oportunidades." |
| Casa sin precio | "Precio pendiente; se hallaron 3 comparables a 8 cuadras y ruta para validar inmobiliaria." | "Oportunidad probable" sin precio ni comparable. |
| Instrumental usado | "Watchlist hasta confirmar marca/modelo, garantia, vendedor y trazabilidad." | "Comprar" con foto parcial. |
| Cero candidatos | "7 fuentes, 12 descartes, criterios de descarte y proxima corrida." | "Mercado agotado" sin evidencia. |

## automation_hooks

- `scripts/qa/validate_radar_report.py` debe fallar si falta `sources_attempted`, `fallback_routes_used`, `candidates`, `rejected_candidates`, decision o `next_action`.
- Todo job radar debe guardar `results/<job_id>.result.md` y, si hay candidatos, `results/<job_id>.candidates.json`.
- Si el score queda 50-74, crear job a Pablo con reporte parcial, errores del validator y mejores candidatos.
- Si el score queda menor a 50, marcar `blocked` con rutas faltantes, no como final.
- El commit del radar debe incluir salida del validator o resumen de errores.

## failure_language_ban

Frases prohibidas como cierre:

- "no pude"
- "no encontre nada"
- "la pagina no abre"
- "no hay oportunidades"
- "mercado agotado"

Version permitida solo con evidencia: "Fuente X bloqueada; se intentaron A/B/C; resultado parcial; quedan estos descartes/candidatos; proxima accion concreta". El bloqueo tecnico no prueba ausencia de oportunidad.

## risks / limits

- El playbook mejora calidad del informe, no garantiza que el mercado tenga oportunidades.
- Si se exige cantidad minima sin scorecard, el agente podria inflar candidatos malos.
- Para instrumental medico, seguridad y trazabilidad pesan mas que margen.
- Navegador real, OCR o screenshots deben usarse solo si el orquestador lo autoriza y sin credenciales.

## recommendation

Codex principal debe convertir este playbook en checklist obligatorio y conectar `validate_radar_report.py` al cierre de cada radar. 5.3 ejecuta el barrido; Pablo interviene ante bloqueo dificil, ranking estrategico o candidatos con riesgo medico/regulatorio.

## confidence

Alta para rutas y thresholds, porque consolidan reglas ya aceptadas. Media para numeros exactos hasta calibrar con corridas reales.

## evidence_paths

- `jobs/20260525T124718-radares-source-recovery-playbook.md`
- `context/fronts/radares.md`
- `results/20260525T122941-radar-anti-empty-script-spec.result.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`

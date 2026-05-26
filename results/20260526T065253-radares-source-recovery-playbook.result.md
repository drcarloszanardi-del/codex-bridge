# Resultado - 20260526T065253-radares-source-recovery-playbook

## summary honesto

El playbook debe impedir que los radares de inmobiliaria, instrumental o inversiones cierren por bloqueo tecnico o universo pobre. Un radar solo puede terminar como `completed` si muestra fuentes, alternativas, candidatos o descartes, comparables y proxima accion.

**Evidencia:** `context/fronts/radares.md` exige fuentes, cantidad de candidatos, descartes, rutas alternativas y recomendacion accionable. Los resultados previos ya definen schema, thresholds y validator anti informe vacio.

**Inferencia:** el problema operativo no es solo "buscar mas"; es separar bloqueo tecnico, falta real de candidatos y oportunidad incompleta.

**Opinion:** cualquier frase tipo "no pude" debe convertirse en estado estructurado con rutas usadas, limite exacto y siguiente paso.

## coverage_table

| Fuente | Uso | Limite |
| --- | --- | --- |
| `context/fronts/radares.md` | Canon de radares Junin/instrumental y minimo anti informe vacio. | No contiene implementacion de script. |
| `results/20260525T122941-radar-anti-empty-script-spec.result.md` | Schema, gate rules, CLI y exit codes. | No calibra con corridas nuevas. |
| `results/20260525T120001-radares-anti-informe-vacio-v1.result.md` | Contrato, scorecards y division 5.3/Pablo. | No navega ni busca mercado real. |

## source_recovery_routes

| Bloqueo | Ruta obligatoria 1 | Ruta obligatoria 2 | Ruta obligatoria 3 | Escalar a Pablo si |
| --- | --- | --- | --- | --- |
| Web inmobiliaria no abre | Query por direccion/zona/radio | Marketplace espejo: Zonaprop, Argenprop, ML, inmobiliarias locales | Snippets/cache/comparables del mismo radio | Hay precio ambiguo, candidato fuerte o cero candidatos con universo parcial. |
| Marketplace muestra parcial | Buscar titulo exacto, direccion o telefono publico del aviso | Fuente espejo o capturas publicas autorizadas | Comparables por zona/precio/superficie | El reporte queda 50-74 de score. |
| No hay precio | Mismo inmueble/producto en otra fuente | Comparables recientes o mismo modelo | Marcar `pending_price` con ruta concreta | El precio define decision de compra/watchlist. |
| Producto instrumental ambiguo | Fabricante/modelo/version | Distribuidor local, eBay/ML, China B2B | Riesgo regulatorio, reputacion y soporte | Es implante/equipo medico o hay trazabilidad dudosa. |
| Cero candidatos | Ampliar queries y registrar descartes | Cambiar fuente/mercado espejo | Proxima corrida con criterio exacto | No hay 5+ fuentes y descartes suficientes. |
| Requiere login/credenciales | No usar credenciales | Buscar equivalente publico | Documentar limite y alternativa | Solo el orquestador puede autorizar otro camino. |

## front_specific_thresholds

| Frente | `completed` permitido | `needs_review` | `blocked` |
| --- | --- | --- | --- |
| Inmobiliaria Junin | 5+ fuentes, ubicacion, precio o comparable, candidatos/descartes y next action. | 0 candidatos con 5+ fuentes, descartes y comparables. | 0 candidatos con menos de 5 fuentes o sin fallback. |
| Instrumental medico | Marca/modelo, precio comparable, reputacion, soporte, trazabilidad/regulatorio y decision prudente. | Falta precio/trazabilidad pero hay ruta concreta. | Recomendacion de compra sin vendedor claro, regulatorio o comparable. |
| Inversion general | Tesis, universo revisado, comparables, riesgos y proximo paso. | Evidencia parcial con ruta de validacion. | Conclusion sin fuentes o sin candidatos/descartes. |

## examples

| Caso | Salida aceptable | Salida bloqueada |
| --- | --- | --- |
| ML no abre | "ML bloqueado; se usaron snippets, eBay, web fabricante y comparable local; quedan 2 candidatos `needs_review`." | "No se pudo ver ML, sin oportunidades." |
| Casa sin precio | "Precio pendiente; 3 comparables dentro del radio y ruta para validar con fuente publica." | "Oportunidad probable" sin precio ni comparable. |
| Instrumental usado | "Watchlist hasta confirmar marca/modelo, garantia, vendedor y trazabilidad." | "Comprar" con foto parcial. |
| Cero candidatos | "7 fuentes, 12 descartes, criterios y proxima corrida." | "Mercado agotado" sin evidencia. |

## automation_hooks

- `scripts/qa/validate_radar_report.py` debe exigir `sources_attempted`, `fallback_routes_used`, `candidates`, `rejected_candidates`, `recommendation`, `confidence` y `next_action`.
- Si una fuente falla, debe existir al menos una alternativa en `fallback_routes_used`; para fuentes principales, idealmente dos.
- Si score < 50, estado minimo `blocked`; si score 50-74, estado minimo `needs_review`; si score >= 75, `completed` permitido.
- Si el reporte incluye candidatos, guardar `results/<job_id>.candidates.json` con precio, fuente, comparable, riesgo y decision.
- Si el validator retorna `needs_review`, crear job a `personal-xh` con errores, mejores candidatos y rutas ya usadas.
- Si se intenta cerrar con frase prohibida sin evidencia estructurada, el commit debe fallar.

## failure_language_ban

Frases prohibidas como cierre final:

- "no pude"
- "no encontre nada"
- "la pagina no abre"
- "no hay oportunidades"
- "mercado agotado"

Forma permitida: "Fuente X bloqueada; se intentaron A/B/C; resultado parcial; candidatos/descartes; limite exacto; proxima accion". El bloqueo tecnico nunca prueba ausencia de oportunidad.

## risks_limits

- Este playbook valida calidad operacional, no garantiza que la oportunidad sea real.
- Sin navegacion ni fuentes externas en este job, los thresholds vienen de evidencia local previa.
- Un agente podria inflar candidatos para pasar minimo; por eso el score debe penalizar comparables debiles, falta de precio y riesgo regulatorio.
- Para instrumental medico, seguridad/trazabilidad pesa mas que margen.
- Navegador real, OCR o screenshots requieren autorizacion del orquestador y nunca credenciales.

## recommendation

Codex principal debe convertir este playbook en checklist de cierre y conectar `validate_radar_report.py` antes de aceptar resultados de radares. 5.3 puede hacer barrido rutinario; Pablo queda para bloqueos dificiles, ranking estrategico y casos con riesgo medico/regulatorio.

## confidence

Alta para rutas y estados porque consolidan reglas ya aceptadas. Media para thresholds numericos hasta calibrarlos con corridas reales.

## evidence_paths

- `jobs/20260526T065253-radares-source-recovery-playbook.md`
- `context/fronts/radares.md`
- `results/20260525T122941-radar-anti-empty-script-spec.result.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `results/20260525T124718-radares-source-recovery-playbook.result.md`

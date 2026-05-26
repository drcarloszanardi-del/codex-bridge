---
id: 20260525T234822-radares-hardening-anti-informe-vacio-v2
job_id: 20260525T234822-radares-hardening-anti-informe-vacio-v2
created_at: 2026-05-25T23:51:41-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - RADARES hardening anti informe vacio v2

## summary

Paquete portable para endurecer los radares contra informes inutiles. El criterio P0 es que un radar debe terminar en informe util, `needs_review` accionable o bloqueo valido con rutas alternativas agotadas. Error tecnico, fuente caida, pagina bloqueada o una sola oportunidad debil no alcanzan para cerrar.

No se navego, no se contacto a terceros, no se uso Telegram ni se tocaron credenciales. El resultado consolida reglas y tests para que el orquestador los convierta en validator/fixtures reales.

## source_counts

| Fuente permitida | Estado | Uso |
|---|---:|---|
| `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md` | Revisada | Fixtures Telegram/radares y contratos de bloqueo. |
| `results/20260525T211520-postpatch-telegram-radar-gate-audit-v1.result.md` | Revisada | Riesgos residuales post-patch y gates P0. |
| `results/20260525T164233-radares-anti-informe-vacio-operational-gate-v1.result.md` | Revisada | Contrato minimo, thresholds, pseudocodigo y score. |
| `results/20260525T120001-radares-anti-informe-vacio-v1.result.md` | Revisada | Anti-empty gate, fallback routes y division 5.3/Pablo. |
| `results/20260525T124718-radares-source-recovery-playbook.result.md` | Revisada | Ladder de recuperacion por fuente fallida. |
| `results/20260525T103946-inmobiliaria-junin-casas-reforma-radio-12-cuadras-v2.result.md` | Revisada | Ejemplo positivo inmobiliario con candidatos, comparables y pendientes. |
| `results/20260525T103947-instrumental-neuro-columna-china-vs-argentina-v2.result.md` | Revisada | Ejemplo instrumental con prudencia regulatoria y watchlist. |
| `results/20260525T021032-radar-scorecards-inmobiliaria-instrumental-v1.result.md` | Revisada | Scorecards y decisiones validas. |
| `protocol.md` | Revisado | Reglas duras del bridge. |

## findings con evidencia

- Los resultados previos ya definen un contrato minimo: fuentes intentadas, rutas alternativas, candidatos, descartes, comparables, decision, proxima accion y evidencia.
- El ejemplo inmobiliario bueno no fue "una oportunidad": trajo shortlist, precios, comparables, dudas y proximas acciones. Ese es el piso de utilidad.
- El ejemplo instrumental bueno separo oportunidad limpia de instrumental reusable y descarto implantes como compra directa sin trazabilidad/ANMAT/importador/lote.
- El gate Telegram/radar ya bloquea `sent:false` para reportes compuestos solo por fallas tecnicas; falta endurecer reportes pobres que no son tecnicamente vacios pero tampoco utiles.

## P0_rules

1. Nunca cerrar con una frase de fracaso tecnico sin evidencia de recuperacion.
2. Cualquier fuente fallida exige al menos dos rutas alternativas razonables o escalamiento documentado.
3. Un radar amplio requiere minimo 5 fuentes o queries relevantes, salvo scope estrecho justificado.
4. Si hay cero candidatos, debe haber universo revisado, descartes documentados, comparables o proxima corrida concreta.
5. Un candidato sin precio, ubicacion/specs, fuente, comparable, decision y `next_action` no puede sostener `completed`.
6. Un unico candidato debil queda `needs_review`, no informe final.
7. Para instrumental medico, seguridad, trazabilidad y regulatorio pesan mas que margen.
8. Implantes sin registro/trazabilidad/importador/lote nunca quedan como `comprar`; maximo benchmark/watchlist.
9. `completed` exige score >= 75 y cero hard blockers; 50-74 es `needs_review`; <50 es `blocked`.
10. Telegram solo recibe resumen humano si el contrato pasa; no diffs, logs, stack traces ni ruido tecnico.

## acceptable_report_contract

Todo radar debe exponer, en JSON o markdown parseable:

```yaml
radar_report:
  job_id: string
  front: inmobiliaria | inversiones | instrumental | general
  status_by_gate: completed | needs_review | blocked
  score: 0..100
  scope:
    query: string
    market_or_geography: string
    constraints: [string]
  sources_attempted:
    - name: string
      type: direct_page | marketplace | search | pdf | official | snippet | cache | comparable | local_context
      outcome: success | blocked | no_results | partial | error
      evidence: string
  fallback_routes_used:
    - failed_source: string
      route: string
      outcome: success | partial | failed
      evidence: string
  candidates:
    - title: string
      source: string
      price_or_value: string
      location_or_specs: string
      comparable_basis: [string]
      risks: [string]
      decision: investigar | watchlist | descartar | pedir_aprobacion
      next_action: string
  rejected_candidates:
    - title: string
      reason: string
  conclusion:
    recommendation: string
    confidence: low | medium | medium-high | high
    next_run_or_handoff: string
```

## invalid_report_patterns

Hard fail si aparece cualquiera de estos patrones sin evidencia suficiente:

| Patron invalido | Por que falla |
|---|---|
| `no pude`, `no encontre nada`, `pagina no hallada`, `mercado agotado` como cierre | Confunde limite tecnico con ausencia real de oportunidad. |
| 0 candidatos + menos de 5 fuentes | Universo insuficiente. |
| Fuente principal bloqueada sin alternativas | Error recuperable, no conclusion. |
| Candidato unico sin comparables | No permite decidir. |
| Candidato sin precio ni ruta para conseguirlo | Watchlist como maximo. |
| Inmobiliaria sin zona/direccion verificable | No se puede evaluar radio, liquidez ni comparable. |
| Instrumental sin marca/modelo/version | No se puede comparar ni validar compatibilidad. |
| Producto medico sin trazabilidad/regulatorio cuando aplica | Riesgo clinico y legal. |
| Reporte sin descartes | No demuestra busqueda ni criterio. |
| Reporte sin `next_action` | No es accionable. |

## source_recovery_ladder

| Bloqueo | Rutas obligatorias antes de cerrar |
|---|---|
| Portal inmobiliario no abre | Buscar por direccion/zona, inmobiliaria + titulo, marketplace espejo, snippets/cache, comparables misma zona. |
| Aviso sin precio | Buscar replica exacta, sitio del vendedor, PDF/revista local, comparables; dejar `pending_price` con ruta concreta. |
| Marketplace bloqueado | Buscar codigo/titulo exacto, fuente espejo, cache/snippet, navegador/captura solo si autorizado. |
| Cero candidatos inmobiliarios | Ampliar queries permitidas, documentar descartes, comparables y criterio de agotamiento. |
| Instrumental ambiguo | Marca, modelo, version, fabricante, proveedor local, ML/eBay, China B2B, regulatorio si aplica. |
| Fuente requiere login | No usar credenciales; buscar equivalente publico y marcar limite. |
| Imagen/PDF parcial | OCR/captura solo con autorizacion; si no, `needs_review` con ruta exacta. |

## inmobiliaria_specific_contract

Campos minimos por candidato:

| Campo | Regla |
|---|---|
| `direccion_o_zona` | Debe permitir evaluar radio objetivo o justificar fuera de foco. |
| `precio` | Valor real o `pending_price` con ruta concreta. |
| `superficie` | Terreno/cubierta si esta disponible; si falta, marcar pendiente. |
| `estado_refaccion` | Estimado desde fuente; no inventar. |
| `servicios` | Documentados o pendientes. |
| `comparables_misma_zona` | Minimo uno o explicar ausencia. |
| `tesis_oportunidad` | Por que mirar: margen, ubicacion, lote, local, reventa. |
| `riesgos` | Estructura, titulo, ocupacion, zona, precio, refaccion. |
| `decision` | `investigar`, `watchlist`, `descartar`, `pedir_aprobacion`. |
| `next_action` | Accion concreta sin contactar terceros desde worker. |

## inversiones_instrumental_contract

Separar siempre:

1. Reusable no implantable.
2. Equipamiento usado/electromecanico.
3. Implantes o alto riesgo.

Campos minimos:

| Campo | Regla |
|---|---|
| `marca_modelo_version` | Obligatorio para comparar. |
| `nuevo_usado` | Estado declarado o pendiente. |
| `precio_origen` y `precio_local_comparable` | No mezclar productos no equivalentes sin advertencia. |
| `compatibilidad_clinica` | Benchmark no alcanza para uso. |
| `garantia_repuestos_soporte` | Obligatorio en usado/equipo. |
| `trazabilidad_regulatoria` | Obligatorio si producto medico de riesgo. |
| `riesgo_importacion` | Aduana, demora, soporte, certificacion. |
| `decision` | Implantes sin trazabilidad: `descartar` o `watchlist`, nunca `comprar`. |
| `next_action` | Validacion documental o comparacion pieza por pieza. |

## telegram_reporting_gate

Antes de informar al Doctor:

```json
{
  "radar_gate_ok": true,
  "status_by_gate": "completed|needs_review|blocked",
  "score": 0,
  "sources_count": 0,
  "fallback_routes_count": 0,
  "candidates_count": 0,
  "rejections_count": 0,
  "message_id_required_if_sent": true
}
```

Reglas:

- Si `status_by_gate=blocked`, no enviar como informe final; guardar artifact y devolver bloqueo accionable al orquestador.
- Si `needs_review`, el resumen puede decir que hay evidencia parcial y que requiere decision humana.
- Si se envia por Telegram, no decir "enviado" sin `message_id` real.
- Nunca enviar logs, diffs, tracebacks, links sensibles ni secretos.

## test_cases_to_add

| ID | Caso | Expected |
|---|---|---|
| `R_EMPTY_TECH_001` | 4 fuentes, todas error tecnico, 0 candidatos. | `blocked`, no Telegram. |
| `R_BLOCKED_SOURCE_NO_FALLBACK` | Fuente principal bloqueada, 0 alternativas. | `blocked`, reason `fallback_missing`. |
| `R_ZERO_CANDIDATES_EXHAUSTIVE` | 7 fuentes, 12 descartes, comparables y proxima corrida. | `needs_review`, no final automatico. |
| `R_ONE_WEAK_CANDIDATE` | 1 candidato sin precio/comparables/next_action. | `needs_review` o `blocked`. |
| `R_INM_REAL_SHORTLIST` | 3+ candidatos con precio, zona, comparables, riesgos. | `completed` si score >=75. |
| `R_INM_PENDING_PRICE` | Propiedad fuerte sin precio pero con ruta concreta. | `watchlist`, no `completed` por si sola. |
| `R_INST_IMPLANT_NO_TRACE` | Tornillos/cages baratos sin ANMAT/importador/lote. | `descartar|watchlist`, hard fail si `comprar`. |
| `R_INST_REUSABLE_BENCHMARK` | Set reusable con marca/precio/comparable/riesgo. | `investigar` o `watchlist`. |
| `T_RADAR_SEND_NO_MESSAGE_ID` | Outbox creado sin recibo Telegram. | No afirmar envio. |
| `T_RADAR_TECH_PAYLOAD` | Reporte contiene diff/log/traceback. | Bloquear envio. |

## implementation_order

1. Crear fixtures `R_EMPTY_TECH_001`, `R_BLOCKED_SOURCE_NO_FALLBACK`, `R_ONE_WEAK_CANDIDATE`, `R_ZERO_CANDIDATES_EXHAUSTIVE`.
2. Implementar `validate_radar_report` con estados `completed`, `needs_review`, `blocked`.
3. Hacer hard fail de patrones invalidos antes de score.
4. Agregar scorecards inmobiliaria e instrumental.
5. Integrar pre-send gate Telegram: solo resumen humano si `radar_gate_ok`.
6. Guardar artifact local para todo `blocked` y `needs_review` con rutas faltantes.
7. Correr regresion con ejemplos positivos: shortlist inmobiliaria Junin y matriz instrumental reusable.
8. Recalibrar thresholds con corridas reales; no bajar reglas P0.

## recommendation

Implementar como cierre obligatorio de todos los radares: un reporte que no cumpla contrato no puede marcarse `completed` ni reportarse como final. El primer hardening debe enfocarse en: error-only, fuente bloqueada sin alternativas, candidato unico debil, cero candidatos sin universo, e instrumental medico sin trazabilidad.

## risks_limits

- Este pack no garantiza oportunidades reales; garantiza que el informe no sea vacio ni tecnicamente resignado.
- Los thresholds pueden requerir calibracion por frente, pero las reglas P0 no deberian relajarse.
- No se inspecciono codigo real ni se ejecutaron tests de la Mac de trabajo.
- OCR/capturas/navegador real requieren autorizacion del orquestador y no deben usar credenciales.

## confidence

Alta para reglas P0, contratos y test cases porque consolidan incidentes y resultados previos. Media para puntajes numericos exactos hasta ver corridas reales del pipeline.

## evidence_paths

- `jobs/20260525T234822-radares-hardening-anti-informe-vacio-v2.md`
- `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md`
- `results/20260525T211520-postpatch-telegram-radar-gate-audit-v1.result.md`
- `results/20260525T164233-radares-anti-informe-vacio-operational-gate-v1.result.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `results/20260525T124718-radares-source-recovery-playbook.result.md`
- `results/20260525T103946-inmobiliaria-junin-casas-reforma-radio-12-cuadras-v2.result.md`
- `results/20260525T103947-instrumental-neuro-columna-china-vs-argentina-v2.result.md`
- `results/20260525T021032-radar-scorecards-inmobiliaria-instrumental-v1.result.md`
- `protocol.md`

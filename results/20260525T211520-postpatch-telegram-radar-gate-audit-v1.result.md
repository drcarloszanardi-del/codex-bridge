---
id: 20260525T211520-postpatch-telegram-radar-gate-audit-v1
job_id: 20260525T211520-postpatch-telegram-radar-gate-audit-v1
created_at: 2026-05-25T21:21:01-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - auditoria post-patch Telegram + radares anti informe vacio

Job: `20260525T211520-postpatch-telegram-radar-gate-audit-v1`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary

Segunda pasada XH sobre el parche reportado por el orquestador. El diseno va en la direccion correcta: agrego routing explicito para voz/reel hacia `REELS`, bloqueo reportes de radares compuestos solo por fallas tecnicas, y verifico sintaxis/fixtures basicos.

Limite central: esta auditoria no inspecciono el patch real de la Mac de trabajo; evalua la logica a partir del resumen del workorder y resultados previos del bridge. La proxima mejora debe convertir esos asserts manuales en regresion permanente con fixtures que fallen si reaparecen: mezcla de topics, respuesta antes de adjuntos, "enviado" sin `message_id`, diffs/logs crudos y radar vacio con errores tecnicos.

## source_counts

| Fuente | Uso |
|---|---|
| `jobs/20260525T211520-postpatch-telegram-radar-gate-audit-v1.md` | Resumen del parche y contrato de auditoria. |
| `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md` | Suite base de 30 casos Telegram: topics, media buffer, idempotencia, delivery real. |
| `results/20260525T164233-radares-anti-informe-vacio-operational-gate-v1.result.md` | Gate operativo anti informe vacio y pseudocodigo validator. |
| `results/20260525T120001-radares-anti-informe-vacio-v1.result.md` | Contrato minimo de radar, fallback routes y division 5.3/Pablo. |
| `results/20260525T124108-telegram-quality-scorecard.result.md` | Hard fails y scorecard de respuestas Telegram. |
| `context/fronts/telegram.md` | Estado canonico: entrega confirmada, ContextBinder, buffer de media. |
| `context/fronts/radares.md` | Estado canonico de radares y regla anti informe vacio. |
| `protocol.md` | Reglas duras del bridge y prohibicion de acciones externas. |

## coverage_table

| Area auditada | Estado | Observacion |
|---|---:|---|
| Routing voz/reel a `REELS` | mejorado | Keywords nuevas cubren el incidente reportado; falta test negativo para evitar sobreruteo. |
| Radar error-only | mejorado | `sent:false` + `blocked_empty_technical_failure_report` es el gate correcto. |
| Delivery Telegram | pendiente de hard gate permanente | La validacion mencionada es healthcheck/bot; faltan tests de `message_id` para no confundir outbox con enviado. |
| Media buffer | riesgo residual | El parche de keywords no prueba que texto + fotos/videos tardios esperen cierre de album. |
| Contrato de radar | riesgo residual | El bloqueo error-only no reemplaza validator completo de fuentes/candidatos/descartes/comparables. |
| Observability | parcial | Se reportan razones (`reason`, `rule`); conviene un schema unico de decision. |

## what_seems_fixed

1. `codex_telegram_direct.py` ahora reconoce pedidos de voz vinculados a reel con terminos como `voz`, `locucion`, `voiceover`, `graves` y `lata de robot`, y el fixture critico routea a `chat_id=-1003701553547`, `thread_id=6`, `reason=direct_deliverable_topic`.
2. Inmobiliaria ya no debe enviar un informe si todos los items son fallas tecnicas y no hay oportunidades vigentes dentro del radio. El retorno esperado `sent:false` evita ruido al Doctor.
3. Inversiones/instrumental aplica una regla equivalente cuando `queries_checked=0` y existen errores tecnicos, con `rule=anti_informe_vacio`.
4. El ultimo radar inmobiliario real no queda falsamente bloqueado cuando trae oportunidades reales: 12 oportunidades vigentes dentro del radio y 127 candidatos vigentes.
5. Las validaciones basicas de sintaxis y fixtures error-only reducen el riesgo de romper runtime inmediato.

## residual_risks

1. **Sobreruteo por keyword**: palabras como `voz` o `graves` pueden aparecer en clinica, presentaciones o notas personales. La regla debe requerir co-ancla de reel/video/CMP/edicion/pieza creativa, o topic explicito, antes de forzar `REELS`.
2. **Media tardia no cubierta por el patch descrito**: el bug anterior no era solo clasificacion; tambien era responder antes de que llegaran fotos/videos. Mantener test de album incompleto es P0.
3. **Radar con una fuente real pero salida pobre**: bloquear solo `all technical failures` deja pasar informes con una oportunidad debil, sin comparables, sin descartes o sin `next_action`.
4. **Cero oportunidades legitimo**: si no hay oportunidades pero la busqueda fue exhaustiva, el estado debe ser `needs_review` con universo documentado, no `completed` vacio ni `blocked` generico.
5. **Delivery real**: healthcheck `ok:true` del bot no prueba que cada envio tenga `delivery.ok=true` y `message_id`. El hard gate debe vivir en `send()` o `pre_send_gate`, no solo en tests externos.
6. **Errores tecnicos acumulados**: `sent:false` debe crear artifact local accionable para el orquestador; si solo silencia Telegram, el sistema puede quedar ciego.
7. **Razon y schema divergentes**: inmobiliaria usa `reason=blocked_empty_technical_failure_report`; inversiones suma `rule=anti_informe_vacio`. Conviene normalizar ambos.

## regression_tests

Propuesta de suite permanente, sin Telegram real:

```text
tests/telegram/test_direct_reels_voice_routing.py
tests/telegram/test_topic_delivery_gate.py
tests/telegram/test_media_buffer_policy.py
tests/telegram/test_delivery_receipt_gate.py
tests/telegram/test_technical_payload_gate.py
tests/radares/test_empty_technical_failure_gate.js
tests/radares/test_radar_report_contract.js
tests/radares/test_real_candidate_not_blocked.js
```

Fixtures minimos:

```text
fixtures/telegram/direct_reels_voice_argentina_graves_lata_robot.json
fixtures/telegram/direct_voice_non_reels_clinica_negative.json
fixtures/telegram/reels_text_plus_four_photos_late_album.json
fixtures/telegram/outbox_without_message_id.json
fixtures/telegram/raw_diff_payload_blocked.json
fixtures/radares/inmobiliaria_all_technical_failures.json
fixtures/radares/inversiones_queries_zero_technical_errors.json
fixtures/radares/inmobiliaria_real_opportunities_junin.json
fixtures/radares/radar_one_weak_candidate_missing_comparables.json
fixtures/radares/radar_zero_candidates_with_documented_universe.json
```

Comandos sugeridos para el orquestador:

```bash
python3 -m py_compile scripts/codex_telegram_direct.py
node --check scripts/inmobiliaria/send_inm_radar_report.js
node --check scripts/inversiones/send_inv_neuro_instrument_report.js
python3 tests/telegram/test_direct_reels_voice_routing.py
python3 tests/telegram/test_media_buffer_policy.py
python3 tests/telegram/test_delivery_receipt_gate.py
node tests/radares/test_empty_technical_failure_gate.js
node tests/radares/test_radar_report_contract.js
```

## radar_gate_tests

| ID | Fixture | Expected |
|---|---|---|
| R001 | inmobiliaria con todos los items `technical_error` y 0 oportunidades | `sent:false`, `status=blocked`, `reason=blocked_empty_technical_failure_report` |
| R002 | inversiones con `queries_checked=0` + errores tecnicos | `sent:false`, `status=blocked`, `rule=anti_informe_vacio` |
| R003 | inmobiliaria real con 12 oportunidades dentro del radio | `sent:true` o `report_ready:true`, no bloqueado, candidatos > 0 |
| R004 | 1 candidato sin precio/comparables/next_action | no enviar; `status=needs_review`, errores contractuales |
| R005 | 0 candidatos, 7 fuentes, 8 descartes, comparables y rutas alternativas | no Telegram automatico; `status=needs_review`, no informe vacio |
| R006 | fuente principal bloqueada sin 2 alternativas | `status=blocked`, requiere fallback routes |
| R007 | implante/instrumental medico sin trazabilidad | no `comprar`; maximo `watchlist` o `needs_review` |
| R008 | reporte contiene frases de falla tecnica sin `fallback_routes_used` | `status=blocked` |

Assert de contrato para cada radar:

```json
{
  "sources_attempted_min": 5,
  "has_candidates_or_documented_rejections": true,
  "has_fallback_routes_when_blocked": true,
  "has_comparables_or_explained_absence": true,
  "has_next_action": true,
  "forbidden_final_phrases_without_evidence": ["no pude", "no encontre", "pagina no hallada"]
}
```

## telegram_routing_tests

| ID | Input sintetico | Expected |
|---|---|---|
| T001 | "edicion de voz argentina... graves... lata de robot" con ancla reel/CMP | `front=REELS`, `thread_id=6`, `reason=direct_deliverable_topic` |
| T002 | "la voz del paciente esta grave" en contexto clinico | no `REELS`; `front=CLINICA` o `UNKNOWN_REVIEW` |
| T003 | "armar reel con voz" en canal directo | route a `REELS`, no respuesta final al canal principal |
| T004 | mensaje en topic `REELS` con cuatro fotos llegando en ventana de 12s | un solo job, `media_state=closed` antes de model call |
| T005 | `topic_id` desconocido + "usa lo anterior" | `UNKNOWN_REVIEW`, sin heredar contexto global |
| T006 | diff/stack trace largo generado internamente | `send_policy=block`, artifact local |
| T007 | delivery outbox sin `message_id` | no decir enviado; `sent_confirmed=false` |
| T008 | Telegram API `ok=true`, `message_id=123` | `sent_confirmed=true` |
| T009 | feedback negativo "no me mandes eso" | `job_policy=route_fix|policy_update`, no job largo |
| T010 | mensaje de voz/reel sin permiso de publicar | artifact local o topic `REELS`; no envio externo |

El objeto de decision deberia quedar verificable asi:

```json
{
  "front": "REELS",
  "reply_target": {"chat_id": "-1003701553547", "thread_id": 6},
  "job_policy": "create_job",
  "media_state": "closed",
  "send_policy": "suppress_until_result",
  "reason": "direct_deliverable_topic"
}
```

## implementation_cautions

- No confiar solo en keywords. Usar prioridad: `topic_id` real > etiqueta explicita > anclas de dominio > keywords secundarias.
- Separar `route_decision` de `send_decision`; routear bien no autoriza responder ni publicar.
- Ejecutar `technical_payload_gate` antes de cualquier Telegram send.
- Guardar cada `sent:false` de radar con JSON local: `status`, `reason`, `sources_count`, `candidate_count`, `errors`, `next_action`.
- Evitar que el gate anti-vacio incentive candidatos malos. El validator debe permitir `needs_review` con cero candidatos si el universo esta documentado.
- Hacer que todo mensaje "enviado" dependa de recibo real, no de outbox.
- Mantener fixtures de regresion con nombres del incidente; si el Doctor vuelve a describir el bug, debe existir un test que lo capture.

## recommendation

Aceptar el parche como mejora operativa, pero no como cierre definitivo. La condicion de cierre deberia ser una suite automatica con cuatro gates P0:

1. Voz/reel directo routea a `REELS` solo con ancla suficiente.
2. Texto + media tardia no dispara respuesta final hasta cerrar buffer.
3. Radar error-only o contrato incompleto queda `sent:false`.
4. Ningun envio se informa como realizado sin `message_id` real.

Prioridad inmediata: crear fixtures R001/R002/T001/T002/T004/T007 y correrlos en cada cambio de router/radares.

## risks_limits

- Esta auditoria deriva de resumen y resultados previos, no del diff exacto aplicado en la Mac de trabajo.
- Los comandos son sugeridos: el orquestador debe ajustar rutas/nombres al repo real.
- No se tocaron Telegram, Gmail, Drive, Calendar, credenciales ni repos externos.
- No se ejecutaron tests reales de la Mac de trabajo desde este worker.

## confidence

Alta para los riesgos residuales y tests necesarios, porque salen de incidentes ya documentados y del contrato canonico del bridge. Media para asserts exactos de archivos/comandos, porque no se inspecciono el patch real.

## evidence_paths

- `jobs/20260525T211520-postpatch-telegram-radar-gate-audit-v1.md`
- `claims/20260525T211520-postpatch-telegram-radar-gate-audit-v1.json`
- `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md`
- `results/20260525T164233-radares-anti-informe-vacio-operational-gate-v1.result.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `results/20260525T124108-telegram-quality-scorecard.result.md`
- `context/fronts/telegram.md`
- `context/fronts/radares.md`
- `protocol.md`

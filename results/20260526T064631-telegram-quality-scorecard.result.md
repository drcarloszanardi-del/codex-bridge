# Resultado - 20260526T064631-telegram-quality-scorecard

## summary honesto

Scorecard barato para evaluar respuestas de Telegram Directo despues de generarlas y, cuando sea posible, antes de enviarlas. No reemplaza hard gates; los complementa con una nota de calidad y disparadores de postmortem.

**Evidencia:** los incidentes previos fueron responder antes de adjuntos y mandar payload tecnico/diff crudo por canal. El frente Telegram exige delivery confirmado con `ok=true` y `message_id`.

**Inferencia:** los hard fails deben bloquear envio aunque el score total sea alto.

**Opinion:** primero implementaria checks deterministicos; el scoring fino puede venir despues.

## coverage_table

| fuente | uso | limite |
| --- | --- | --- |
| `context/fronts/telegram.md` | Estado canonico: delivery real, buffers, ContextBinder y gates. | No implementa scorecard. |
| `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md` | Bug de respuesta antes de adjuntos. | Caso especifico MAIL-PC. |
| `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md` | Bug de diff/payload tecnico y timeout de gate. | Caso especifico de payload largo. |

## scorecard

100 puntos:

| rubro | puntos | regla |
| --- | ---: | --- |
| Frente/ruta correcta | 15 | Respuesta usa topic/frente correcto y no contamina contexto. |
| Contexto completo | 20 | No responde con media buffer abierto; usa adjuntos relevantes. |
| Evidencia | 15 | Incluye paths/jobs/refs cuando corresponde. |
| Tono formal | 10 | Respuesta sobria, clara y respetuosa para el Doctor. |
| Accion concreta | 15 | Dice resultado, proximo paso o bloqueo exacto. |
| Entrega confirmada | 10 | Si dice enviado, hay `ok=true` y `message_id`. |
| Seguridad | 15 | Sin secretos, diffs crudos, datos sensibles ni permisos indebidos. |

## thresholds

| score | estado | accion |
| ---: | --- | --- |
| 90-100 | `pass` | Registrar y seguir. |
| 75-89 | `pass_with_warning` | Registrar warning. |
| 50-74 | `needs_review` | Crear item de revision o job a Pablo si se repite. |
| <50 | `fail` | Bloquear patron y abrir postmortem. |

Hard fails:

- Media buffer abierto y respuesta final generada.
- "Enviado" sin `message_id`.
- Diff/trace/payload tecnico crudo.
- Pedido de Drive/Gmail/OAuth cuando habia paquete local.
- Datos sensibles o token-like string.

## postmortem_trigger

- Cualquier hard fail.
- Dos `needs_review` seguidos en el mismo frente.
- Correccion del Doctor sobre tono, ruta, evidencia o material ignorado.
- `event_handle_error`.
- `media_arrived_after_response`.
- Mensaje obliga al Doctor a reenviar material ya enviado.

## examples

| caso | esperado |
| --- | --- |
| Estado breve real, sin adjuntos pendientes | 90+ |
| Responde antes de video/fotos tardias | hard fail |
| Dice "lo envie" con outbox queued | hard fail |
| Manda diff/trace crudo | hard fail |
| Respuesta correcta pero verbosa | 75-89 |
| Informe sin evidence_paths | 50-74 |

## implementation_plan

1. Crear `scripts/qa/score_telegram_response.py`.
2. Input JSON: `event`, `decision`, `response_text`, `attachments`, `delivery_result`.
3. Output JSON: `score`, `status`, `hard_fails`, `warnings`, `postmortem_required`.
4. Ejecutar como pre-send cuando haya respuesta sensible/larga; post-send para auditoria liviana.
5. Si hard fail pre-send: no enviar, guardar artifact local y crear item de revision.
6. Guardar score por `event_id/job_id`.

Salida ejemplo:

```json
{
  "score": 82,
  "status": "pass_with_warning",
  "hard_fails": [],
  "warnings": ["verbose"],
  "postmortem_required": false
}
```

## risks_limits

- Score automatico puede castigar respuestas buenas si el contexto esta incompleto.
- Si corre solo post-send, mejora futuro pero no previene dano.
- Debe mantenerse barato; Pablo interviene solo en hard fails o patrones.

## recommendation

Implementar primero hard fails deterministicos en pre-send. Luego sumar puntaje 100 como observabilidad. No permitir nunca override automatico para delivery sin `message_id` o payload tecnico crudo.

## confidence

Alta para rubros y hard fails porque derivan de incidentes concretos; media para pesos exactos hasta calibrar.

## evidence_paths

- `jobs/20260526T064631-telegram-quality-scorecard.md`
- `context/fronts/telegram.md`
- `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md`

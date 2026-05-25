# Resultado - Telegram quality scorecard

Job: `20260525T124108-telegram-quality-scorecard`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary honesto

El scorecard debe ser barato, post-respuesta y ejecutable por 5.3. No reemplaza al orquestador: marca respuestas con riesgo. Debe evaluar frente correcto, contexto usado, evidencia, tono formal, accion concreta, entrega real y ausencia de errores ya detectados: responder antes de adjuntos, mandar diffs crudos o confundir cola con enviado.

## coverage_table

| Fuente | Estado | Uso |
|---|---|---|
| `jobs/20260525T124108-telegram-quality-scorecard.md` | revisado | Contrato del scorecard. |
| `context/fronts/telegram.md` | revisado | Estado canonico de Telegram Directo. |
| `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md` | revisado | Bug: respuesta antes de adjuntos. |
| `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md` | revisado | Bug: diff/payload tecnico por argv y timeout. |

## scorecard

100 puntos:

| Rubro | Puntos | Regla |
|---|---:|---|
| Frente/ruta correcta | 15 | Usa topic/frente correcto y ContextBinder. |
| Contexto completo | 20 | Espera adjuntos/media y usa material relevante. |
| Evidencia/local refs | 15 | Cita paths/jobs/logs cuando corresponde. |
| Tono formal | 10 | Trato de usted, puntual, sin relleno. |
| Accion concreta | 15 | Deja proxima accion clara o resultado entregado. |
| Entrega confirmada | 10 | Si dice enviado, debe haber `ok=true` y `message_id`. |
| Seguridad | 15 | No secretos, no datos sensibles, no diffs crudos en Telegram. |

## thresholds

| Score | Estado | Accion |
|---:|---|---|
| 90-100 | pass | No intervenir. |
| 75-89 | pass_with_warning | Registrar warning. |
| 50-74 | needs_review | Crear item de revision / posible job a Pablo. |
| <50 | fail | Bloquear patron y generar postmortem. |

Hard fails aunque el score sea alto:

- Responde antes de que termine album/media.
- Dice "enviado" sin `message_id`.
- Manda stack trace/diff crudo a Telegram.
- Pide Drive/Gmail/OAuth cuando el job trae paquete local.
- Tutea al Doctor en canal donde pidio trato formal.

## postmortem_trigger

Crear postmortem si:

- 2 respuestas seguidas `needs_review` en el mismo frente.
- Cualquier hard fail.
- El Doctor corrige tono, scope o falta de evidencia.
- Hay `event_handle_error` o `media_arrived_after_response`.
- Una respuesta obliga al Doctor a repetir material ya enviado.

## examples

| Caso | Score esperado |
|---|---:|
| Respuesta breve con accion clara, sin adjuntos pendientes | 90+ |
| Responde antes de recibir videos | hard fail |
| Informe largo sin evidence_paths | 50-74 |
| "Lo envié" pero solo esta en outbox | hard fail |
| Mensaje tecnico con diff crudo | hard fail |
| Respuesta correcta pero algo verbosa | 75-89 |

## implementation_plan

1. Crear `scripts/qa/score_telegram_response.py`.
2. Input: raw event, generated response, route, attachments, delivery result.
3. Output JSON: `score`, `status`, `hard_fails`, `warnings`, `postmortem_required`.
4. Ejecutar con 5.3 despues de respuesta o antes de envio si es posible.
5. Guardar score en estado local del router.
6. Si hard fail: no enviar, crear artifact/postmortem local.
7. Dashboard muestra ultimas respuestas con score.

Schema de salida:

```json
{
  "score": 82,
  "status": "pass_with_warning",
  "hard_fails": [],
  "warnings": ["verbose"],
  "postmortem_required": false,
  "evidence": ["message_id:123", "route:REELS"]
}
```

## risks / limits

- Un score automatico puede castigar respuestas buenas si no tiene contexto completo.
- Si se ejecuta despues del envio, sirve para mejora pero no previene daño.
- Debe ser barato; Pablo solo interviene en hard fails o patrones repetidos.
- No se toca Telegram real desde este worker.

## recommendation

Implementar primero hard-fails deterministicos, luego scoring 100 puntos. Lo mas urgente: media buffer, no diffs crudos y delivery real con `message_id`. El scorecard debe correr con 5.3 y escalar a Pablo solo cuando haya `needs_review` repetido o hard fail.

## confidence

Alta. Los criterios salen de bugs concretos y del estado canonico de Telegram.

## evidence_paths

- `jobs/20260525T124108-telegram-quality-scorecard.md`
- `context/fronts/telegram.md`
- `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md`


---
job_id: 20260527T185434-telegram-quality-scorecard
worker: personal-xh
status: completed
completed_at: 2026-05-27T18:55:44-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram quality scorecard post-respuesta

## summary honesto

El scorecard debe ser barato, casi deterministico y correr despues de respuestas
importantes de Telegram Directo. No tiene que evaluar si la prosa es brillante;
tiene que detectar si la respuesta respeto frente, contexto, evidencia, tono
formal, permisos y accion concreta. Debe devolver `pass`, `warn`,
`needs_review` o `fail`.

Separacion pedida:

- Evidencia: `context/fronts/telegram.md` exige contexto de frente, buffer de
  media, ResultContract y entrega confirmada con `ok=true` + `message_id`.
- Inferencia: el scorecard debe mirar tanto contenido como proceso, porque los
  incidentes previos fueron de timing de adjuntos y de gate con payload tecnico.
- Opinion: 5.3 alcanza para puntuar; Pablo debe entrar solo en postmortems de
  hard fail repetido o riesgo alto.

No use Telegram real, no envie mensajes y no toque credenciales.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T185434-telegram-quality-scorecard.md` | Revisada | Objetivo, secciones y restricciones. |
| `context/fronts/telegram.md` | Revisada | Estado canonico, reformas y deuda activa. |
| `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md` | Revisada | Caso de respuesta antes de adjuntos y necesidad de buffer. |
| `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md` | Revisada | Caso de payload tecnico largo, diff crudo y timeout del gate. |
| `results/20260527T005221-telegram-quality-scorecard.result.md` | Revisada como antecedente | Scorecard previo, thresholds y hard fails. |

## scorecard

```yaml
telegram_quality_scorecard_v1:
  max_score: 100
  dimensions:
    route_context:
      points: 20
      checks:
        - frente_correcto
        - context_front_attached
        - reset_scope_respected
    evidence_and_completeness:
      points: 20
      checks:
        - media_buffer_closed_before_response
        - attachments_referenced_if_present
        - evidence_paths_or_local_refs_for_claims
    safety_permissions:
      points: 20
      checks:
        - no_external_action_without_authorization
        - no_credentials_or_secrets
        - no_sensitive_data_leak
    tone_and_format:
      points: 15
      checks:
        - concise_formal_spanish
        - no_raw_diff_or_stacktrace
        - no_internal_notes
    actionability:
      points: 15
      checks:
        - next_action_clear
        - if_blocked_has_attempts_limits_next_step
    delivery_integrity:
      points: 10
      checks:
        - sent_status_matches_reality
        - message_id_required_for_confirmed_delivery
```

Salida JSON esperada:

```json
{
  "score": 0,
  "status": "pass|warn|needs_review|fail",
  "hard_fails": [],
  "warnings": [],
  "postmortem_required": false,
  "evidence": []
}
```

## thresholds

| Score | Estado | Accion |
| ---: | --- | --- |
| 90-100 | `pass` | Registrar y seguir. |
| 75-89 | `warn` | Registrar warning; no bloquear salvo repeticion. |
| 60-74 | `needs_review` | Revision barata 5.3 o job corto si hay riesgo. |
| <60 | `fail` | Bloquear patron y abrir postmortem si ya fue enviado. |

Hard fails sin depender del score:

- Respuesta final antes de cerrar media buffer/album.
- Payload tecnico crudo con diff o stacktrace al Doctor.
- Entrega afirmada sin `ok=true` y `message_id` real.
- Credencial, secreto o dato sensible visible.
- Accion externa sin autorizacion explicita.
- Frente/contexto equivocado en una respuesta clinica, legal, financiera o de
  publicacion.

## postmortem_trigger

Abrir postmortem si ocurre cualquiera de estos:

- Mismo hard fail 2 veces en 7 dias.
- Cualquier leak de secreto, credencial o dato sensible.
- `fail` en una respuesta ya enviada.
- Mismatch entre `queued/outbox` y entrega confirmada real.
- Usuario corrige explicitamente por frente/contexto equivocado.
- Respuesta importante cierra con "no pude" sin rutas alternativas, limite exacto
  y proxima accion.

Template minimo:

```yaml
incident_id:
message_ids:
route:
failure_type:
what_user_saw:
root_cause:
fix_candidate:
test_to_add:
owner:
due:
```

## examples

| Caso | Resultado esperado | Motivo |
| --- | --- | --- |
| Texto y 2 videos llegan juntos; el router espera buffer y la respuesta cita adjuntos. | `pass` 95 | Proceso completo. |
| Respuesta util pero sin path/evidencia local en tarea tecnica. | `warn` 82 | Falta trazabilidad. |
| "No pude" sin alternativas ni proxima accion. | `needs_review` 55 | Falla accionabilidad. |
| Diff tecnico largo enviado crudo. | `fail` hard fail | Debia resumirse y guardar local ref. |
| Outbox creado pero sin `message_id` real. | `fail` hard fail | No es entrega confirmada. |
| Respuesta simple de saludo sin evidence path. | `pass` o `warn` leve | No exigir contrato completo a mensajes triviales. |

## implementation_plan

1. Crear `scripts/qa/score_telegram_response.py`.
2. Entrada: JSON con `route`, `front_context`, `raw_event_ids`,
   `attachments`, `media_buffer_status`, `response_text` y `delivery_receipt`.
3. Salida: `score`, `status`, `hard_fails`, `warnings`,
   `postmortem_required`, `evidence`.
4. Correr en modo observabilidad durante 7 dias.
5. Persistir en `router/runs/<run_id>/quality_score.json`.
6. Hacer bloqueantes solo los hard fails.
7. Abrir job a Pablo solo cuando hay hard fail repetido, leak o score bajo con
   riesgo alto.

Pseudo-regla:

```python
if delivery.claimed_sent and not delivery.message_id:
    hard_fail("delivery_without_message_id")
if response.contains_raw_diff_or_stacktrace():
    hard_fail("raw_technical_payload_to_telegram")
if event.has_media and media_buffer_status != "closed":
    hard_fail("media_buffer_not_closed")
```

## risks / limits

- Un score automatico puede castigar respuestas buenas por falta de metadata; por
  eso existe `warn`.
- Tono formal no debe volver rigidas respuestas simples del canal.
- No reemplaza secret scan, permisos del orquestador ni revision humana.
- Si se hace bloqueante demasiado pronto, puede frenar el canal; empezar en
  observabilidad.
- Ruta alternativa si falta metadata: marcar `warn_missing_metadata`, no `fail`,
  salvo que haya hard fail.

## recommendation

Implementar el scorecard primero como observabilidad no bloqueante durante 7
dias. Hacer bloqueantes desde el dia 1 solo estos hard fails: media sin buffer,
diff/stacktrace crudo, entrega sin `message_id`, secreto/dato sensible y accion
externa sin autorizacion.

## confidence

Alta para dimensiones y hard fails porque salen de incidentes previos y del
frente canonico. Media para thresholds exactos hasta calibrar con respuestas
reales.

## evidence_paths

- `jobs/20260527T185434-telegram-quality-scorecard.md`
- `context/fronts/telegram.md`
- `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md`
- `results/20260527T005221-telegram-quality-scorecard.result.md`
- `claims/20260527T185434-telegram-quality-scorecard.json`

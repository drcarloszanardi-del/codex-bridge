---
job_id: 20260527T005221-telegram-quality-scorecard
worker: personal-xh
status: completed
completed_at: 2026-05-27T01:14:00-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram quality scorecard

## summary honesto

El scorecard debe ser barato, deterministico en lo posible y correr despues de
cada respuesta importante de Telegram Directo. Su objetivo no es juzgar estilo
literario: es detectar si la respuesta respeto frente, contexto, evidencia, tono
formal, permisos y proxima accion. Debe producir `pass`, `warn` o `fail` y abrir
postmortem solo cuando el fallo sea repetible o de riesgo.

Evidencia: los incidentes previos fueron respuesta antes de recibir medios y
timeout por payload tecnico largo. Inferencia: el scorecard debe mirar tanto
contenido como proceso. Opinion: 5.3 alcanza para puntuar; Pablo solo entra en
postmortems complejos.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T005221-telegram-quality-scorecard.md` | Revisada | Entregables y restricciones. |
| `context/fronts/telegram.md` | Revisada | Estado canonico y reformas activas. |
| `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md` | Revisada | Caso media tardia y buffer. |
| `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md` | Revisada | Caso payload largo/diff y gate por stdin. |

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

## thresholds

| Score | Estado | Accion |
| ---: | --- | --- |
| 90-100 | `pass` | Registrar y seguir. |
| 75-89 | `warn` | Registrar warning; no postmortem salvo repeticion. |
| 60-74 | `needs_review` | Crear revision barata 5.3 o job corto si hay riesgo. |
| <60 | `fail` | Bloquear patron y abrir postmortem. |

Hard fails sin depender de score:

- Envio externo afirmado sin `message_id` real.
- Respuesta final antes de cerrar buffer de media/album.
- Payload tecnico crudo con diff/stacktrace al Doctor.
- Credencial, secreto o dato sensible visible.
- Accion externa sin autorizacion.

## postmortem_trigger

Abrir postmortem si:

- Mismo hard fail ocurre 2 veces en 7 dias.
- Cualquier leak de datos sensibles o credenciales.
- El scorecard marca `fail` y la respuesta ya fue enviada.
- Hay mismatch `queued/outbox` vs `sent ok=true message_id`.
- Usuario corrige explicitamente por contexto/frente equivocado.

Postmortem minimo:

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
```

## examples

| Caso | Score esperado | Motivo |
| --- | ---: | --- |
| Texto y 2 videos llegan juntos, respuesta espera buffer y cita adjuntos | 95 | Proceso completo. |
| Respuesta util pero sin evidence path en tarea tecnica | 82 | Warn por trazabilidad. |
| "No pude" sin rutas alternativas | 55 | Falla accionabilidad. |
| Diff tecnico largo enviado crudo | hard fail | Debia resumirse y guardar local ref. |
| Outbox creado pero sin `message_id` real | hard fail | No es entrega confirmada. |

## implementation_plan

1. Crear `scripts/qa/score_telegram_response.py`.
2. Entrada: JSON con `route`, `front_context`, `raw_event_ids`, `attachments`,
   `response_text`, `delivery_receipt`.
3. Salida JSON: `score`, `status`, `hard_fails`, `warnings`, `postmortem_required`.
4. Correr despues de respuesta importante y antes de marcar `delivered`.
5. Persistir en `router/runs/<run_id>/quality_score.json`.
6. Abrir job a Pablo solo para hard fail repetido o score bajo con riesgo.

## risks / limits

- Un score automatico puede castigar respuestas buenas por falta de metadata; por eso hay `warn`.
- Tono formal depende del canal y usuario; no debe volver rigidas respuestas simples.
- No reemplaza permisos del orquestador ni secret scan.

## recommendation

Implementar el scorecard primero como observabilidad no bloqueante durante 1
semana. Hacer bloqueantes solo los hard fails: no media buffer, no message_id,
diff crudo, secretos/datos sensibles y accion externa sin autorizacion.

## confidence

Alta para dimensiones y hard fails porque salen de incidentes previos; media
para thresholds hasta calibrar con respuestas reales.

## evidence_paths

- `jobs/20260527T005221-telegram-quality-scorecard.md`
- `context/fronts/telegram.md`
- `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md`

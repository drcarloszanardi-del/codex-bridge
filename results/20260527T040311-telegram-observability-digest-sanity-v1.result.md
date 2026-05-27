---
job_id: 20260527T040311-telegram-observability-digest-sanity-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T04:15:00-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram observability digest sanity v1

## summary

Propongo un digest diario barato, local-first y silencioso por defecto. El
digest no debe competir con el contralor ni mandar "todo esta bien" cada dia:
debe producir un JSON local diario y notificar al Doctor solo si hay algo
accionable, repetido o riesgoso. La regla madre: no afirmar entrega Telegram sin
`ok=true` y `message_id`, no exponer payload tecnico crudo y no abrir acciones
externas desde el worker.

Evidencia: el frente Telegram ya exige delivery real con `message_id`, los
resultados post-fix cerraron T13 y el scorecard define hard fails. Inferencia:
el digest debe leer estado y runs locales, no Telegram real. Opinion: conviene
hacer primero un digest dry-run que escriba artefacto local y deje el envio bajo
autorizacion explicita del orquestador.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T040311-telegram-observability-digest-sanity-v1.md` | Revisada | Workorder, restricciones y entregables. |
| `context/fronts/telegram.md` | Revisada | Canon Telegram, delivery real, deuda activa. |
| `results/20260527T005221-telegram-quality-scorecard.result.md` | Revisada | Hard fails, scorecard y postmortem trigger. |
| `results/20260526T054100-telegram-postfix-local-port-review-v1.result.md` | Revisada | Estado post-fix y riesgo residual previo. |
| `results/20260526T071000-telegram-t13-postfix-final-review-v1.result.md` | Revisada | Cierre T13 y modo observacion. |
| `status/orchestrator.json` | Revisado | Estado del orquestador: frente REELS en hold. |
| `status/personal-xh.json` | Revisado | Disponibilidad de Pablo y ultimos jobs. |

## digest_contract

Archivo local sugerido: `state/telegram_observability/daily_digest/YYYY-MM-DD.json`.
No debe incluir tokens, texto completo sensible, adjuntos crudos ni rutas a
media privada. Campos minimos:

```json
{
  "schema": "telegram_observability_daily_digest.v1",
  "date": "2026-05-27",
  "generated_at": "2026-05-27T08:00:00-03:00",
  "mode": "dry_run|notify_candidate|notified",
  "window_hours": 24,
  "overall_status": "quiet|watch|action_needed|incident",
  "should_notify_doctor": false,
  "notify_reason": null,
  "headline": "Sin incidentes accionables.",
  "counts": {
    "events_seen": 0,
    "jobs_created": 0,
    "runs_completed": 0,
    "deliveries_confirmed": 0,
    "delivery_receipt_missing": 0,
    "scorecard_fail": 0,
    "scorecard_warn": 0,
    "stale_jobs": 0
  },
  "fronts": {
    "TELEGRAM": {"status": "observing", "open_items": []},
    "RADARES": {"status": "quiet", "blocked": []},
    "REELS": {"status": "hold", "reason": "from status/orchestrator.json"}
  },
  "action_items": [],
  "suppressed_noise": [],
  "evidence_paths": []
}
```

El texto humano, si el orquestador autoriza envio, debe ser de 3 a 6 lineas:
estado, solo alertas accionables, proxima accion y link/ruta local del digest.
No incluir stack traces, diffs, payloads ni datos de pacientes.

## notify_policy

### Notificar al Doctor

Notificar solo si al menos una condicion es verdadera:

| Condicion | Umbral | Ejemplo de texto permitido |
| --- | --- | --- |
| Incidente P0/P1 confirmado | inmediato | `Telegram: falta message_id en una entrega marcada como enviada. Lo revise y queda accion pendiente.` |
| Scorecard hard fail enviado o repetido | inmediato si enviado; si no, en digest | `Se bloqueo un payload tecnico antes de enviarlo; no requiere accion del Doctor.` |
| Jobs estancados con impacto en pedido del Doctor | >60 min P0 o >24 h backlog | `Hay un job de REELS detenido por decision pendiente.` |
| Radares bloqueados con valor operativo | 2 ciclos fallidos o guard bloqueando entrega | `Radar en hold por falta de evidencia publicable; queda accion de source recovery.` |
| Reel en hold por decision o asset faltante | si bloquea entrega prometida | `Reel en hold por decision editorial/asset; proxima accion requerida.` |
| Contradiccion entre status y realidad local | inmediata si afecta confianza | `Outbox 0 pero run activo stale; revisar listener.` |

### Mantenerse quieto

No notificar si:

- Todo esta OK y no hay accion.
- Solo hay warnings aislados sin repeticion.
- El digest no tiene `message_id` o autorizacion de envio.
- Hay errores tecnicos ya bloqueados y sin impacto visible al Doctor.
- El evento corresponde a trabajo interno de bridge sin decision humana.
- El estado es idle normal y ya hubo senal reciente.

## health_inputs

Lecturas locales seguras:

| Ruta/glob | Uso | Regla de privacidad |
| --- | --- | --- |
| `context/fronts/telegram.md` | Canon y deuda activa. | Texto interno no sensible. |
| `status/orchestrator.json` | Frente activo, hold, updated_at. | No imprimir valores secretos si aparecen. |
| `status/personal-xh.json` | Disponibilidad y jobs recientes. | Usar solo estado/resumen. |
| `jobs/*.md` | Jobs queued/in_progress/stale. | No copiar contenido completo al digest. |
| `claims/*.json` | Claims activos y edad. | Usar job_id/claimed_at/assignee. |
| `results/*.result.md` | Resultados recientes por frente. | Solo paths y estado. |
| `state/codex-telegram-direct/runs/**/*.json` | Runs y receipts si existe. | Excluir tokens, payloads y texto largo. |
| `state/codex-telegram-direct/outbox/**/*.json` | Outbox pendiente y delivery. | No incluir chat_id/thread_id completos en salida humana. |
| `router/runs/**/quality_score.json` | Scorecard. | Solo score/status/hard_fails. |
| `fixtures/telegram/postfix/*.json` | Version de smoke suite. | Fixtures sinteticos permitidos. |

Si una ruta no existe en la Mac local del worker, el digest debe reportar
`input_missing` como `advisory`, no como incidente.

## quality_checks

| Check | Logica | Severidad |
| --- | --- | --- |
| `delivery_requires_message_id` | Si `delivery_label=sent` o `delivered=true`, exigir `ok=true` y `message_id`. | `incident` |
| `topic_message_id_match` | Si hay topic/thread esperado, comparar route esperado vs real; no publicar si mismatch. | `action_needed` |
| `no_raw_technical_payload` | Detectar diff, stacktrace o traceback en candidato de respuesta. | `incident` si enviado, `watch` si bloqueado. |
| `media_buffer_closed_before_response` | No model call final antes de cerrar grupo media/texto. | `incident` si visible al usuario. |
| `scorecard_threshold` | `fail` o hard fail del scorecard genera action item; `warn` solo cuenta. | `action_needed` o `watch` |
| `stale_jobs` | queued/in_progress sin result y claim viejo. Umbrales: P0 60 min, normal 24 h. | `action_needed` |
| `radar_blocked` | Radares con delivery guard bloqueando entrega por falta de evidencia publicable. | `watch` o `action_needed` tras repeticion. |
| `reels_hold` | Estado REELS en hold o job creative esperando assets/decision. | `watch`; `action_needed` si vence promesa. |
| `outbox_drift` | Outbox pendiente >0 por mas de ventana configurada. | `action_needed` |
| `listener_health_age` | Healthcheck viejo o listener sin latido local. | `watch`; `incident` si coincide con outbox. |

## failure_modes

Alertas que deben existir:

- Entrega marcada como enviada sin `message_id` real.
- Texto al Doctor con diff, stacktrace, traceback o payload tecnico crudo.
- Respuesta antes de recibir/cerrar media group o fotos sueltas relevantes.
- Route correction aplicada a grupo cerrado, job ya creado o entrega ya iniciada.
- Topic equivocado: trabajo de REELS/RADARES/CLINICA cae en DIRECT sin razon fuerte.
- Duplicacion de jobs por el mismo cluster de eventos.
- Job P0 estancado con claim viejo y sin result.
- Scorecard `fail` repetido o hard fail enviado.
- Secret/dato sensible detectado en candidato de respuesta.
- Digest intenta enviar sin autorizacion del orquestador.

## implementation_plan

1. Crear `scripts/ops/build_telegram_daily_digest.py`.
2. Entrada: `--date YYYY-MM-DD --window-hours 24 --dry-run`.
3. Leer solo archivos locales allowlisted. Sanitizar: truncar textos, remover
   tokens, ocultar chat ids si no hacen falta y no abrir media.
4. Producir JSON local en `state/telegram_observability/daily_digest/`.
5. Producir `notify_candidate.md` solo si `should_notify_doctor=true`.
6. Integrar a automation diaria local, primero dry-run durante 7 dias.
7. Envio externo queda fuera de este script: solo otro wrapper autorizado por el
   orquestador puede tomar `notify_candidate.md` y enviarlo.
8. Agregar QA:

```bash
python3 scripts/ops/build_telegram_daily_digest.py --date 2026-05-27 --window-hours 24 --dry-run
python3 scripts/qa/score_telegram_response.py --fixture fixtures/telegram/scorecard/sample_ok.json
python3 tests/telegram/test_postfix_regression_fixtures.py
python3 tests/telegram/test_delivery_receipt_gate.py
python3 tests/telegram/test_technical_payload_gate.py
```

## risk_limits

- Privacidad: el digest no debe incluir texto completo de mensajes, nombres,
  telefono, DNI, media, tokens ni rutas privadas innecesarias.
- Ruido: si `overall_status=quiet`, no mandar mensaje. Un "todo bien" diario
  entrena al Doctor a ignorar alertas.
- Falsos positivos: rutas faltantes o status viejo deben empezar como `watch`,
  no como incidente.
- Falsos negativos: si no hay logs locales suficientes, el digest debe decir
  `coverage_gap` y recomendar instrumentacion, no inventar salud.
- Acciones externas: este job no envio Telegram real. La implementacion debe
  mantener el envio desacoplado y autorizado.

## recommendation

Proxima accion unica: implementar `scripts/ops/build_telegram_daily_digest.py`
en modo `--dry-run`, generando `state/telegram_observability/daily_digest/*.json`
y `notify_candidate.md` solo cuando haya `action_needed` o `incident`. Correrlo
7 dias sin envio automatico y despues decidir si se autoriza un wrapper de envio.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso `jobs/20260527T040311-telegram-observability-digest-sanity-v1.md`.
- Se revisaron `context/fronts/telegram.md`, los tres resultados solicitados y
  `status/orchestrator.json` / `status/personal-xh.json`.
- No se uso Telegram real, Gmail, Drive, Photos, iCloud, ObraCash ni acciones
  externas.
- No se leyeron tokens ni credenciales.

## confidence

Media-alta para contrato, politica y checks porque derivan de incidentes y
scorecard previos. Media para rutas exactas `state/` y `router/runs/` hasta que
el orquestador inspeccione la Mac que corre Telegram real.

## evidence_paths

- `jobs/20260527T040311-telegram-observability-digest-sanity-v1.md`
- `context/fronts/telegram.md`
- `results/20260527T005221-telegram-quality-scorecard.result.md`
- `results/20260526T054100-telegram-postfix-local-port-review-v1.result.md`
- `results/20260526T071000-telegram-t13-postfix-final-review-v1.result.md`
- `status/orchestrator.json`
- `status/personal-xh.json`

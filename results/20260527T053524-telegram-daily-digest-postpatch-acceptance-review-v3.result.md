---
job_id: 20260527T053524-telegram-daily-digest-postpatch-acceptance-review-v3
worker: personal-xh
status: completed
completed_at: 2026-05-27T06:06:00-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram daily digest postpatch acceptance review v3

## summary

Veredicto: **ajustar algo puntual antes de observacion dry-run 7 dias**.
No encontre un P0 ni motivo para revertir: el paquete sigue siendo local, no
envia Telegram real, expone `coverage_gap`/`health_inputs_available`, agrega los
tests esperados y el JSON sanitizado queda `quiet` con `should_notify_doctor=false`.

El unico riesgo P1 que detecte es un falso incidente en delivery: un outbox
pendiente con `sent_at: null` se cuenta tambien como `delivery_receipt_missing`
porque el detector busca el substring `"sent"` dentro del JSON redacted. Eso
puede convertir una cola normal en `incident` y crear `notify_candidate.md`
durante la observacion.

## source_counts

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T053524-telegram-daily-digest-postpatch-acceptance-review-v3.md` | Revisada | Workorder y criterios P0/P1. |
| `results/20260527T050413-telegram-daily-digest-handoff-review-v2.postpatch/build_telegram_daily_digest.py.txt` | Revisada | Builder postpatch completo. |
| `results/20260527T050413-telegram-daily-digest-handoff-review-v2.postpatch/test_telegram_daily_digest_builder.py.txt` | Revisada | Tests postpatch. |
| `results/20260527T050413-telegram-daily-digest-handoff-review-v2.postpatch/2026-05-27.sanitized.json` | Revisada | Digest sanitizado generado. |
| `results/20260527T050413-telegram-daily-digest-handoff-review-v2.postpatch/test-output.txt` | Revisada | Py compile, tests y dry-run declarados OK. |
| `results/20260527T050413-telegram-daily-digest-handoff-review-v2.postpatch/sha256sums.txt` | Verificada | Checksums comparados localmente. |

## findings

| Severidad | Hallazgo | Evidencia | Recomendacion |
| --- | --- | --- | --- |
| P1 | Outbox pendiente puede escalar falsamente a `incident`. | En `build_telegram_daily_digest.py.txt`, `pending_outbox` sube cuando falta `sent_at`, pero luego `sentish = any(... "sent" ...)` se calcula sobre todo el JSON redacted; una clave `sent_at: null` contiene `"sent"` y cae en `delivery_receipt_missing` si no hay `message_id`. Un harness local con un unico `state/codex_telegram_outbox/pending.json` `{"sent_at": null, "payload": "queued"}` produjo `overall_status=incident`, `delivery_receipt_missing=1` y `pending_outbox=1`. | Cambiar `sentish` a marcadores explicitos de envio real: `ok` true, `sent` true, `delivered` true, `status in {"sent","delivered","enviado"}` o `sent_at` no nulo; no contar `sent_at: null`. Agregar test de outbox pendiente sin receipt para asegurar que no sea `delivery_receipt_missing`. |
| OK | El parche cubre el gap principal pedido. | `health_input_coverage` devuelve `health_inputs_available` y `coverage_gap`; si faltan roots criticos agrega item `coverage_gap` severity `watch`, y `should_notify_doctor` solo queda true para `incident`/`action_needed`. Tests nuevos cubren quiet, stale, coverage gap watch sin notify, delivery sin message_id, scorecard fail y redaction. | Mantener ese comportamiento. |
| OK | No hay accion externa en el builder revisado. | Imports limitados a stdlib y salida local bajo `state/telegram_observability/daily_digest/`; `--dry-run` es compatibilidad y el docstring dice que el script nunca envia. | Mantener el envio real fuera de este script. |
| OK | Evidencia del paquete consistente. | `shasum -a 256` local coincide con `sha256sums.txt`; `test-output.txt` reporta `py_compile`, 6 tests OK y dry-run con `overall_status=quiet`. | Usar el paquete como base para el ajuste puntual. |

## recommendation

Recomendacion unica: **ajustar el detector `sentish` y agregar el regression
test de outbox pendiente; despues aceptar observacion dry-run 7 dias**.

No revertir. El parche es pequeno y acotado a `delivery_digest`: no debe
marcar `delivery_receipt_missing` por la mera presencia de la clave `sent_at`
cuando su valor es nulo. Si ese test pasa junto con los 6 existentes, el digest
queda apto para observacion dry-run sin envio automatico al Doctor.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso el workorder y el paquete postpatch completo.
- Se verificaron checksums locales con `shasum -a 256`.
- Se revisaron los puntos del parche con busqueda estatica y lineas numeradas.
- Se ejecuto un harness local, efimero, importando el builder sanitizado para
  reproducir el caso de `sent_at: null`.
- No se uso Telegram real, Gmail, Drive, Photos, iCloud ni acciones externas.
- No se leyeron secretos ni credenciales.

## risks_limits

- La revision usa el paquete sanitizado bajo `results/`, no la ruta real de la
  Mac `jarvis`.
- Tome `test-output.txt` como evidencia declarada de la corrida real, y lo
  complemente con revision estatica y un harness local del archivo sanitizado.
- El riesgo detectado es de falso positivo operativo, no de filtracion ni envio
  externo.

## confidence

Alta para el hallazgo P1: el comportamiento se reproduce con el mismo builder
sanitizado y deriva directamente de la condicion `sentish`. Media-alta para
aceptar el resto del parche, porque los tests esperados estan presentes y el
paquete no contiene acciones externas.

## evidence_paths

- `jobs/20260527T053524-telegram-daily-digest-postpatch-acceptance-review-v3.md`
- `results/20260527T050413-telegram-daily-digest-handoff-review-v2.postpatch/build_telegram_daily_digest.py.txt`
- `results/20260527T050413-telegram-daily-digest-handoff-review-v2.postpatch/test_telegram_daily_digest_builder.py.txt`
- `results/20260527T050413-telegram-daily-digest-handoff-review-v2.postpatch/2026-05-27.sanitized.json`
- `results/20260527T050413-telegram-daily-digest-handoff-review-v2.postpatch/test-output.txt`
- `results/20260527T050413-telegram-daily-digest-handoff-review-v2.postpatch/sha256sums.txt`
- `claims/20260527T053524-telegram-daily-digest-postpatch-acceptance-review-v3.json`

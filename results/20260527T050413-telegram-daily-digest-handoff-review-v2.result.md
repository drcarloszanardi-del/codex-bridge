---
job_id: 20260527T050413-telegram-daily-digest-handoff-review-v2
worker: personal-xh
status: completed
completed_at: 2026-05-27T05:12:00-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram daily digest handoff review v2

## summary

Veredicto: **ajustar con parche puntual antes de observacion 7 dias**. El
paquete sanitizado ya permite revisar el digest y mejora claramente el handoff:
hay script, test, JSON diario, salida de tests y checksums coherentes. No vi un
P0 que obligue a revertir: el builder no envia Telegram real, no importa
clientes externos y solo escribe JSON/local notify candidate bajo
`state/telegram_observability/daily_digest/`.

El riesgo P1 es de falso "quiet": si no existen logs/estado Telegram local o si
los checks criticos no estan cubiertos por tests, el digest puede decir "Sin
incidentes accionables" sin aclarar brecha de cobertura. Eso es corregible con
un parche chico: agregar `coverage_gap/watch` y tests de delivery/scorecard.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T050413-telegram-daily-digest-handoff-review-v2.md` | Revisada | Workorder y restricciones. |
| `results/20260527T043725-telegram-daily-digest-implementation-review-v1.handoff/build_telegram_daily_digest.py.txt` | Revisada | Builder sanitizado completo. |
| `results/20260527T043725-telegram-daily-digest-implementation-review-v1.handoff/test_telegram_daily_digest_builder.py.txt` | Revisada | Tests disponibles. |
| `results/20260527T043725-telegram-daily-digest-implementation-review-v1.handoff/2026-05-27.sanitized.json` | Revisada | Digest generado. |
| `results/20260527T043725-telegram-daily-digest-implementation-review-v1.handoff/test-output.txt` | Revisada | Py compile, tests y dry-run declarados OK. |
| `results/20260527T043725-telegram-daily-digest-implementation-review-v1.handoff/sha256sums.txt` | Revisada | Checksums comparados localmente. |
| `results/20260527T040311-telegram-observability-digest-sanity-v1.result.md` | Revisada | Contrato esperado del digest. |

## findings

| Severidad | Hallazgo | Evidencia | Recomendacion |
| --- | --- | --- | --- |
| P1 | Falta `coverage_gap` cuando no hay fuentes Telegram observables. | El JSON sanitizado sale `overall_status=quiet`, `should_notify_doctor=false`, con `deliveries_confirmed=0`, `delivery_receipt_missing=0`, `scorecard_fail=0`, `scorecard_warn=0`, pero no lista si existen o faltan `state/codex-telegram-direct`, `router/runs` o `quality_score`. | Agregar `health_inputs_available` y si faltan inputs criticos devolver `watch` con `suppressed_noise` o `action_items` no notificante. |
| P1 | Tests cubren solo quiet y stale job, no los hard fails del contrato. | `test_telegram_daily_digest_builder.py.txt` tiene 2 tests: `test_quiet_digest` y `test_stale_job_creates_notify_candidate`. | Agregar tests para delivery marcado enviado sin `message_id`, scorecard hard fail, notify candidate solo en action/incident y sanitizer de secretos/payload tecnico. |
| P2 | `claimed_without_result` puede generar watch por claims historicos si no se limpia el bridge. | El builder calcula `claim_ids - result_ids` global y lo agrega como `claims_without_result`. | Limitar por ventana/mtime o excluir claims muy viejos para evitar ruido. |
| OK | No hay envio externo desde el builder. | Imports del script: `argparse`, `json`, `re`, `datetime`, `pathlib`, `typing`, `zoneinfo`; no `requests`, `telegram`, `smtplib`, `urllib`, `socket`. `--dry-run` dice "this script never sends". | Mantener asi; cualquier envio debe vivir en wrapper autorizado separado. |
| OK | Checksums del paquete coinciden. | `shasum -a 256` local coincide con `sha256sums.txt` para script, test, JSON y test-output. | Usar este formato para futuras reviews. |

## recommendation

Proxima accion unica: **ajustar con parche puntual y luego iniciar observacion
dry-run 7 dias**. No revertir. El parche minimo debe:

1. Agregar `coverage_gap`/`health_inputs_available` para no reportar "quiet"
   como salud plena cuando faltan logs Telegram o scorecards.
2. Agregar tests para `delivery_label=sent` sin `message_id`, scorecard hard
   fail, sanitizer y no creacion de `notify_candidate.md` en modo quiet/watch.
3. Mantener envio externo desacoplado; este script solo debe escribir artefactos
   locales.

Si esos tests pasan, aceptar el digest en observacion dry-run, sin envio
automatico al Doctor.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso el workorder y el paquete handoff completo.
- Se calcularon checksums locales con `shasum -a 256` y coincidieron con el
  archivo `sha256sums.txt`.
- Se hizo busqueda estatica de imports/llamadas riesgosas en el script
  sanitizado.
- No se uso Telegram real, Gmail, Drive, Photos, iCloud ni acciones externas.
- No se leyeron secretos ni credenciales.

## risks_limits

- La revision se basa en el paquete sanitizado, no en la ruta real de la Mac
  `jarvis`.
- No ejecute el script real en `/Users/jarvis`; tome `test-output.txt` como
  evidencia declarada y verifique coherencia del paquete.
- El principal riesgo no es envio indebido, sino falsa tranquilidad por falta de
  cobertura observacional.
- El digest puede estar bien para bridge/runs, pero aun necesita calibracion con
  trafico real en dry-run.

## confidence

Media-alta para la recomendacion de ajustar, porque el codigo sanitizado muestra
ausencia de envio externo y el test pack existe. Alta para el gap de cobertura de
tests: el archivo trae solo 2 tests y no cubre delivery/scorecard/sanitizer.
Media para riesgos de runtime real porque no inspeccione la Mac `jarvis`.

## evidence_paths

- `jobs/20260527T050413-telegram-daily-digest-handoff-review-v2.md`
- `results/20260527T043725-telegram-daily-digest-implementation-review-v1.handoff/build_telegram_daily_digest.py.txt`
- `results/20260527T043725-telegram-daily-digest-implementation-review-v1.handoff/test_telegram_daily_digest_builder.py.txt`
- `results/20260527T043725-telegram-daily-digest-implementation-review-v1.handoff/2026-05-27.sanitized.json`
- `results/20260527T043725-telegram-daily-digest-implementation-review-v1.handoff/test-output.txt`
- `results/20260527T043725-telegram-daily-digest-implementation-review-v1.handoff/sha256sums.txt`
- `claims/20260527T050413-telegram-daily-digest-handoff-review-v2.json`

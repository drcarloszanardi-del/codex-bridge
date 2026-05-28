---
job_id: 20260527T210420-telegram-direct-handoff-guardrail-postpatch-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T21:18:10-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram Direct handoff guardrail postpatch review v1

## summary

Revision conceptual del contrato agregado para el puente Telegram Directo ->
Codex Desktop. No use Telegram real, no envie mensajes, no toque credenciales y
no lei datos privados. Los scripts exactos y snapshots `state/codex_live/...`
siguen sin estar versionados en este bridge, asi que este resultado valida el
contrato, no la implementacion real en la Mac de trabajo.

El contrato nuevo va en la direccion correcta: separar `latest_turn_id` /
`latest_turn_role` de `last_user_turn`, `last_user_message_id` y declarar
`pending_source_of_truth=last_user_turn` elimina el bug conceptual principal
detectado antes. La condicion para aceptarlo en Codex principal es que esa regla
sea obligatoria en lectura y escritura: ningun `assistant` ni `tool` puede
avanzar `seen_user`, cerrar un pendiente de usuario ni ocultar un user posterior.

## coverage_table

| Fuente local | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T210420-telegram-direct-handoff-guardrail-postpatch-review-v1.md` | Revisada | Contrato postpatch y restricciones. |
| `results/20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1.result.md` | Revisada | Riesgo previo P0/P1, fixtures base y politica `last_user_turn`. |
| `state/codex_live/telegram_direct_handoff.json` | No existe en bridge | Limite: no se audito snapshot real. |
| `state/codex_live/telegram_direct_handoff_seen.json` | No existe en bridge | Limite: no se audito escritura real de visto. |
| `state/codex_live/telegram_direct_handoff_history.jsonl` | No existe en bridge | Limite: no se audito historia real. |
| `scripts/codex_desktop_telegram_handoff.py` | No existe en bridge | Limite: no se audito parser/renderer Desktop real. |
| `scripts/codex_telegram_direct.py` | No existe en bridge | Limite: no se audito productor real del handoff. |

## riesgos_p0_p1_residuales

| Severidad | Riesgo residual | Condicion que lo dispara | Mitigacion minima |
| --- | --- | --- | --- |
| P0 | `latest_turn` sigue siendo usado por algun consumidor viejo. | Desktop, digest o poller lee `latest_turn_id` como source of truth aunque exista `last_user_turn`. | Agregar gate de compatibilidad: si `latest_turn_role != user`, no puede modificar pending ni seen. |
| P0 | `seen_user` avanza por un cierre de corrida, no por decision sobre user. | Un assistant/tool posterior llama a la rutina comun de "marcar visto". | Separar API: `mark_seen_user(turn_id, role=user)` debe rechazar roles no-user. |
| P0 | User posterior a assistant queda tapado por tool posterior. | Secuencia user 462, assistant 900, user 463, tool 901; latest=tool. | `pending_user_turn_id` debe ser 463 hasta que `seen_user_turn_id >= 463`. |
| P1 | Escritura de seen no es monotona entre procesos. | Dos instancias escriben `seen_user` fuera de orden. | Leer estado actual, comparar orden, escribir temp+fsync+rename; rechazar retrocesos. |
| P1 | `last_user_turn` se calcula por timestamp local, no por orden canonico. | Clock skew o history append fuera de orden. | Ordenar por `turn_sequence`/`telegram_message_id` estable; timestamp solo desempata. |
| P1 | Falta auditoria visible cuando hay divergencia. | `latest_turn_role=assistant/tool` y `last_user_turn` pendiente coexisten, pero no queda evento de health. | Emitir estado local `guardrail_pending_after_non_user_latest=true` sin notificacion externa. |
| P1 | Reprocess interno se confunde con usuario. | Late media o tool reabre contexto con source ambiguo. | Exigir `source=telegram_direct|desktop|internal_reprocess` y filtrar pending solo para source publico/user. |

## fixtures_minimos

| Fixture | Historia sintetica | Esperado |
| --- | --- | --- |
| `T_HANDOFF_ASSISTANT_AFTER_USER_DOES_NOT_ADVANCE_SEEN` | user 462, assistant 900; `seen_user=461`, `latest=assistant`. | `pending_user_turn_id=462`; `seen_user` no cambia. |
| `T_HANDOFF_TOOL_AFTER_USER_DOES_NOT_HIDE_PENDING` | user 463, tool 901; `latest=tool`. | Desktop muestra user 463 pendiente y tool como contexto. |
| `T_HANDOFF_USER_AFTER_ASSISTANT_WINS` | assistant 900, user 463, tool 901. | `last_user_turn=463`; `pending_after_assistant=true`. |
| `T_HANDOFF_NO_USER_NO_PENDING` | assistant/tool sin user nuevo y `seen_user` ya cubre ultimo user. | Sin pendiente; no escribir nuevo `seen_user`. |
| `T_SEEN_REJECTS_NON_USER_ROLE` | llamada `mark_seen(turn_id=901, role=tool)`. | Error local o noop explicito; estado intacto. |
| `T_SEEN_MONOTONIC_CONCURRENT_WRITES` | writer A intenta 462, writer B intenta 463. | Estado final 463; un write tardio de 462 se rechaza. |
| `T_SEEN_SCOPED_BY_CHAT_TOPIC_SOURCE` | mismo message_id en dos scopes distintos. | No hay contaminacion entre scopes. |
| `T_HISTORY_OUT_OF_ORDER_SORTS_BY_SEQUENCE` | timestamps invertidos, sequence correcto. | `last_user_turn` sale del sequence canonico. |
| `T_INTERNAL_REPROCESS_NOT_PUBLIC_PENDING` | event source `internal_reprocess` despues de user visto. | No crea pending publico ni avanza seen. |

## criterio_seen_atomico_monotonico

Regla de aceptacion para `seen_user`:

```text
Only role=user can be marked as seen.
seen_user is scoped by chat_id, topic_id/thread_id and source.
candidate_user_turn.sequence must be >= current_seen_user_turn.sequence.
If candidate is older than current, reject/noop and log local guardrail event.
Write path uses temp file in same directory, fsync file, fsync directory, atomic rename.
After rename, re-read and verify persisted seen_user equals the accepted candidate.
```

El campo `latest_turn_id` debe quedar como display/debug. La fuente de verdad
para trabajo pendiente es siempre:

```text
last_user_turn = newest public turn where role == "user"
pending_user_turn = last_user_turn if last_user_turn.sequence > seen_user.sequence else null
assistant/tool turns cannot advance seen_user
```

## recomendacion

Recomiendo integrar el guardrail en Codex principal en modo bajo riesgo con una
fase de compatibilidad de 24 a 48 horas:

1. Mantener `latest_turn_id` y `latest_turn_role` para UI/contexto, pero cambiar
   todo calculo de pendiente a `last_user_turn`.
2. Centralizar la escritura en una unica funcion `mark_seen_user(...)` que
   rechace roles no-user y updates no monotonicos.
3. Agregar los fixtures minimos antes de activar el cambio como fuente de verdad.
4. En observacion local, registrar divergencias `latest_turn_role != user` con
   user pendiente, sin notificar por Telegram ni crear ruido externo.
5. Solo retirar rutas legacy cuando no aparezcan divergencias durante la ventana
   de observacion.

Decision sugerida: aceptar el contrato postpatch como correcto conceptualmente,
pero no declararlo cerrado hasta que los tests prueben que ningun consumidor usa
`latest_turn` para pending/seen.

## confidence

Alta para la evaluacion del contrato, porque corrige directamente el riesgo
detectado en `results/20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1.result.md`.
Media para el estado real en la Mac de trabajo, porque los scripts y snapshots
sanitizados no estan disponibles en este bridge.

## attempted_routes

- Se hizo `git pull --rebase` y entro el job nuevo `20260527T210420`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se confirmo un job pendiente
  asignado a `personal-xh`.
- Se reviso el workorder actual.
- Se reviso el resultado previo `results/20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1.result.md`.
- Se verifico que los paths exactos `state/codex_live/...` y `scripts/...` no
  estan en el bridge local.
- No se usaron servicios externos ni datos reales.

## risks_limits

- No se certifica implementacion real del script Desktop, solo el contrato
  declarado por el orquestador.
- Si existe algun consumidor legacy fuera del bridge que aun mira `latest_turn`
  como fuente de verdad, el riesgo P0 sigue abierto hasta migrarlo o bloquearlo.
- La decision final de integracion queda en Codex orquestador.

## evidence_paths

- `jobs/20260527T210420-telegram-direct-handoff-guardrail-postpatch-review-v1.md`
- `claims/20260527T210420-telegram-direct-handoff-guardrail-postpatch-review-v1.json`
- `results/20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1.result.md`
- `state/codex_live/telegram_direct_handoff.json`
- `state/codex_live/telegram_direct_handoff_seen.json`
- `state/codex_live/telegram_direct_handoff_history.jsonl`
- `scripts/codex_desktop_telegram_handoff.py`
- `scripts/codex_telegram_direct.py`

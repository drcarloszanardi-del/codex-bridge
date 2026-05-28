---
job_id: 20260528T003850-telegram-direct-consumer-legacy-pending-audit-v1
worker: personal-xh
status: completed
completed_at: 2026-05-28T00:39:34-03:00
front: TELEGRAM
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram Direct consumer legacy pending audit v1

## summary

Auditoria segura de consumidores legacy del handoff Telegram Directo -> Codex
Desktop despues del patch monotono de `last_user_turn`.

En esta Mac no existen las rutas `/Users/jarvis/.openclaw/workspace/scripts` ni
`/Users/jarvis/.openclaw/workspace/tests/telegram`, asi que no pude detectar
consumidores reales con grep local. Con la evidencia declarada, el patch central
esta bien orientado, pero el riesgo residual P0 sigue siendo cualquier consumer
que use `latest_turn`, `latest_turn_id` o `latest_turn_role` como fuente de
verdad para `pending` o `seen`.

Decision: **pedir patch local minimo solo si el grep encuentra usos legacy**. Si
no aparecen usos en pending/seen y los tests siguen OK, no hacen falta cambios
adicionales; agregaria un fixture de compatibilidad para bloquear regresiones.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260528T003850-telegram-direct-consumer-legacy-pending-audit-v1.md` | Revisada | Objetivo, contexto local declarado, alcance y entregables. |
| `results/20260528T003245-telegram-direct-last-user-turn-postpatch-review-v1.result.md` | Revisada | Patch aceptado en observacion y riesgo residual de consumers legacy. |
| `results/20260528T001728-telegram-direct-last-user-turn-null-audit-v1.result.md` | Revisada | Contrato: `latest_turn` debug/display; pending desde `last_user_turn`. |
| `results/20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1.result.md` | Revisada | Fixtures de seen monotono y no-user. |
| `/Users/jarvis/.openclaw/workspace/scripts` | Ausente en esta Mac | Limite: no hubo grep real de consumers. |
| `/Users/jarvis/.openclaw/workspace/tests/telegram` | Ausente en esta Mac | Limite: tests tomados como evidencia declarada del orquestador. |

## consumers_or_patterns

Consumidores reales a revisar en la Mac del orquestador:

1. `scripts/codex_desktop_telegram_handoff.py`
2. `scripts/codex_telegram_direct.py`
3. cualquier script bajo `scripts/` que lea `telegram_direct_handoff.json`
4. cualquier test bajo `tests/telegram/` o `tests/**/handoff*`
5. cualquier dashboard/digest/poller que lea `latest_turn`, `seen` o `pending`

Patrones precisos para correr localmente:

```bash
rg -n "latest_turn|latest_turn_id|latest_turn_role|last_user_turn|last_user_message_id|pending_user|seen_user|telegram_direct_handoff" /Users/jarvis/.openclaw/workspace/scripts /Users/jarvis/.openclaw/workspace/tests
rg -n "pending.*latest|latest.*pending|seen.*latest|latest.*seen|mark_seen|seen_user" /Users/jarvis/.openclaw/workspace/scripts /Users/jarvis/.openclaw/workspace/tests
rg -n "telegram_direct_handoff\\.json|telegram_direct_handoff_seen\\.json|telegram_direct_handoff_history\\.jsonl" /Users/jarvis/.openclaw/workspace
```

## classification

| Severidad | Patron | Clasificacion | Accion |
| --- | --- | --- | --- |
| P0 | `pending = latest_turn` o `pending_id = latest_turn_id` | Uso prohibido: oculta user cuando latest es assistant/tool. | Patch inmediato a `last_user_turn`/history. |
| P0 | `mark_seen(...)` acepta `assistant`/`tool` o usa `latest_turn_id`. | Puede avanzar seen sin haber procesado user. | Separar `mark_seen_user` y rechazar non-user. |
| P0 | Consumer declara no pending si `last_user_turn is null` sin reconstruir history. | Reproduce bug original si writer falla o snapshot legacy llega incompleto. | Fallback local a history o health blocking. |
| P1 | Display usa `latest_turn` pero pending viene de `last_user_turn`. | Aceptable si es solo UI/contexto. | Documentar como display/debug only. |
| P1 | Health/digest lee divergencia `latest_turn_role != user`. | Aceptable si no modifica seen/pending. | Mantener metricas locales. |
| P1 | Scope no incluye chat/thread/source. | Puede mezclar topics/directos. | Completar scope y agregar fixture de colision. |
| P2 | Tests nombran `latest_turn` para armar datos sinteticos. | Aceptable si expected valida `last_user_turn`. | No cambiar salvo confusion. |

## required_tests

Fixtures minimos para cerrar compatibilidad legacy:

| Fixture | Entrada | Esperado |
| --- | --- | --- |
| `T_CONSUMER_PENDING_IGNORES_LATEST_ASSISTANT` | Snapshot `latest_turn_role=assistant`, `last_user_turn=u473`, `seen_user=472`. | Consumer reporta pending `u473`. |
| `T_CONSUMER_PENDING_RECONSTRUCTS_WHEN_LAST_USER_NULL` | Snapshot legacy sin `last_user_turn`, history con `u473`. | Consumer reconstruye o emite health blocking; no declara limpio. |
| `T_CONSUMER_SEEN_REJECTS_LATEST_TOOL` | Intento de seen sobre `latest_turn_id=tool`. | Noop/error local; seen intacto. |
| `T_DISPLAY_LATEST_DOES_NOT_CHANGE_PENDING` | UI muestra latest assistant/tool. | Pending sigue viniendo de `last_user_turn`. |
| `T_GREP_CONTRACT_NO_LATEST_PENDING_CALLERS` | Analisis estatico de scripts. | No hay asignaciones pending/seen desde latest. |

## risks_p0_p1

| Pri | Riesgo | Senal local | Mitigacion |
| --- | --- | --- | --- |
| P0 | Consumer legacy usa latest como source of truth. | `latest_turn_role=assistant`, `last_user_message_id=473`, pero Desktop no muestra pending. | Migrar caller a `last_user_turn`; test de compat. |
| P0 | Seen avanza por non-user. | `seen_user_message_id` cambia tras assistant/tool. | Rechazar roles no-user. |
| P1 | Snapshot legacy sin `last_user_turn` se toma como sano. | `last_user_turn=null` y no se consulta history. | Fallback a history o health local. |
| P1 | Digest/dashboard oculta deuda por latest assistant. | Health muestra divergencia pero UI no. | Mostrar `pending_after_non_user_latest`. |
| P1 | Carrera entre writer y consumer. | Consumer lee snapshot parcial. | Escritura atomica + tolerancia a snapshot incompleto. |

## decision

**Patch local minimo condicionado al grep.**

```yaml
if_grep_finds_latest_used_for_pending_or_seen:
  decision: patch_now
  required_change: replace_latest_source_of_truth_with_last_user_turn_or_history
else:
  decision: no_code_change
  required_change: add_compat_fixture_or_static_guard
always:
  latest_turn: display_debug_only
  pending_source_of_truth: last_user_turn
  seen_source_of_truth: seen_user_turn
```

## recommendation

Que el orquestador corra los `rg` indicados sobre la Mac local y clasifique cada
uso. No tocar usos de `latest_turn` que sean solo display/debug. Parchear de
inmediato cualquier uso que alimente `pending`, `seen`, "no hay pendiente" o
sincronizacion de Desktop.

Agregar al menos un test/guard estatico que falle si aparece una asignacion de
pending/seen desde `latest_turn_id`.

## confidence

Media-alta para la clasificacion de riesgo porque deriva directamente del bug
ya reproducido y del patch postpatch aceptado. Media-baja para la lista de
consumidores reales porque las rutas de la app no existen en esta Mac y no pude
correr grep sobre codigo operativo.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reviso `jobs/20260528T003850-telegram-direct-consumer-legacy-pending-audit-v1.md`.
- Se revisaron resultados previos `20260528T003245`, `20260528T001728` y
  `20260527T212430`.
- Se intento listar `/Users/jarvis/.openclaw/workspace/scripts` y
  `/Users/jarvis/.openclaw/workspace/tests/telegram`, pero no existen en esta Mac.
- No se uso Telegram real, Gmail, Drive, Calendar, iCloud, Photos, adjuntos reales
  ni servicios externos.

## risks_limits

- Este resultado entrega auditoria declarativa y patrones de grep; no certifica
  consumers reales.
- No se leyeron snapshots reales, mensajes reales ni adjuntos.
- Si el grep local encuentra usos P0, el patch debe aplicarse antes de cerrar el
  guardrail.
- La decision final queda en Codex orquestador.

## evidence_paths

- `jobs/20260528T003850-telegram-direct-consumer-legacy-pending-audit-v1.md`
- `claims/20260528T003850-telegram-direct-consumer-legacy-pending-audit-v1.json`
- `results/20260528T003850-telegram-direct-consumer-legacy-pending-audit-v1.result.md`
- `results/20260528T003245-telegram-direct-last-user-turn-postpatch-review-v1.result.md`
- `results/20260528T001728-telegram-direct-last-user-turn-null-audit-v1.result.md`
- `results/20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1.result.md`
- `/Users/jarvis/.openclaw/workspace/scripts`
- `/Users/jarvis/.openclaw/workspace/tests/telegram`

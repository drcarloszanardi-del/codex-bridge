---
job_id: 20260528T001728-telegram-direct-last-user-turn-null-audit-v1
worker: personal-xh
status: completed
completed_at: 2026-05-28T00:19:31-03:00
front: TELEGRAM
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram Direct last user turn null audit v1

## summary

Hallazgo principal: si `telegram_direct_handoff.json` muestra
`last_user_message_id: null` y `last_user_turn: null` mientras `latest_turn`
queda en `assistant/tool` de CODEX-OPS, el guardrail conceptual anterior no esta
cerrado en la escritura real. El root cause mas probable es que alguna ruta del
producer/Desktop sigue calculando el "ultimo turno" desde `latest_turn` o
sobrescribe campos derivados con `null` cuando el ultimo evento no es `role=user`,
en vez de reconstruir y preservar el ultimo user publico desde history.

Decision: **integrar patch ahora, con inspeccion local del orquestador**. No lo
dejaria en backlog: es continuidad P0/P1. Como esta Mac no tiene los scripts ni
state reales, este resultado entrega contrato y tests; la aplicacion debe hacerla
Codex principal sobre la ruta local canonica.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260528T001728-telegram-direct-last-user-turn-null-audit-v1.md` | Revisada | Objetivo, alcance permitido, reglas y entregables. |
| `results/20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1.result.md` | Revisada | Riesgo original de `latest_turn=assistant/tool` ocultando user pendiente. |
| `results/20260527T210420-telegram-direct-handoff-guardrail-postpatch-review-v1.result.md` | Revisada | Contrato postpatch: `last_user_turn` como fuente de verdad. |
| `results/20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1.result.md` | Revisada | Fixtures y pseudocodigo de reconstruccion/seen monotono. |
| `context/fronts/telegram.md` | Revisada | Canon Telegram: entrega real, ContextBinder, idempotencia y deudas. |
| `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py` | Ausente en esta Mac | Limite: no se audito producer real. |
| `/Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py` | Ausente en esta Mac | Limite: no se audito consumer Desktop real. |
| `/Users/jarvis/.openclaw/workspace/state/codex_live/telegram_direct_handoff*.json*` | Ausente en esta Mac | Limite: no se audito snapshot/history real. |

## root_cause_probable

1. **Derivacion desde `latest_turn` en vez de history**: si el snapshot actual es
   `assistant/tool`, el codigo concluye "no hay user" y escribe `last_user_turn=null`.
2. **Overwrite no monotono**: una actualizacion posterior de assistant/tool vuelve
   a serializar todos los campos derivados y pisa un `last_user_turn` anterior con
   `null`.
3. **Reconstruccion ausente o filtrada por scope equivocado**: el user real queda
   en history, pero el filtro exige `front=TELEGRAM`, `source=telegram_direct` o
   `role=user` con nombres no normalizados; un mensaje directo CODEX-OPS puede no
   pasar el filtro aunque sea publico del Doctor.
4. **Alias de IDs incompleto**: el codigo puede buscar `last_user_message_id`
   donde history guarda `message_id`, `telegram_message_id` o `turn_id`, y termina
   nulo aunque exista el turno.
5. **Fallback peligroso ante history no disponible**: si history no se pudo leer,
   el writer deberia preservar el ultimo user no nulo y marcar health local; no
   resetear a null.

La condicion "latest suele ser assistant/tool de CODEX-OPS" es exactamente el
caso que los resultados previos querian volver inocuo. Que ambos `last_user_*`
aparezcan nulos indica que al menos una ruta legacy sigue viva.

## risks_p0_p1

| Pri | Riesgo | Escenario | Mitigacion |
| --- | --- | --- | --- |
| P0 | Pedido directo del Doctor queda invisible en Desktop. | `latest_turn=assistant/tool`, `last_user_turn=null`, Desktop decide que no hay pendiente. | Pending solo desde history user reconstruido; nunca desde latest. |
| P0 | `seen_user` avanza o se sincroniza por assistant/tool. | Run completado llama rutina generica de "seen/latest". | API separada `mark_seen_user` que rechaza roles no-user. |
| P0 | Un user posterior a assistant queda tapado por tool interno. | `user u463`, luego `tool t901`; latest=t901 y last_user=null. | `last_user_turn=u463`; tool solo contexto. |
| P1 | Mezcla de contextos CODEX-OPS/Direct. | Filtro de scope ignora user directo por front/source o mezcla otro topic. | Scope explicito `chat_id`, `thread_id/topic_id`, `source`, con aliases normalizados. |
| P1 | Regresion por carrera de writers. | Writer viejo pisa snapshot mas nuevo con null. | Monotonicidad y escritura atomica con re-read. |
| P1 | Health silencioso inexistente. | History falla y no queda senal local. | `handoff_guardrail_status=history_unavailable_preserved_last_user`. |

## contrato_propuesto

```yaml
source_of_truth:
  latest_turn: display_debug_only
  pending: last_user_turn
  seen: seen_user_turn

last_user_turn:
  scope:
    - chat_id
    - thread_id_or_topic_id
    - source
  candidate_roles:
    - user
  candidate_sources:
    - telegram_direct
    - direct
    - codex_ops_direct
  order:
    - turn_sequence
    - telegram_message_id
    - created_at
  monotonic: true
  preserve_on_non_user_latest: true
  preserve_on_history_unavailable: true
  reset_to_null_only_when:
    - explicit_scope_reset
    - no_user_ever_seen_in_scope

non_user_turns:
  roles:
    - assistant
    - tool
  may_update:
    - latest_turn
    - latest_turn_role
    - assistant_context
  must_not_update:
    - last_user_turn_to_null
    - last_user_message_id_to_null
    - seen_user_turn
    - pending_user_turn
```

Regla concreta de escritura: al serializar `telegram_direct_handoff.json`, primero
leer estado actual + history, reconstruir el ultimo user publico del scope, y
solo reemplazar `last_user_turn` si el candidato nuevo es mas reciente. Si el
ultimo evento es assistant/tool y no hay candidato nuevo, preservar el ultimo
user no nulo.

## fixtures_tests

| Fixture | Entrada sintetica | Esperado |
| --- | --- | --- |
| `T_NULL_LAST_USER_RECONSTRUCTS_FROM_HISTORY` | Snapshot: `latest_turn_role=assistant`, `last_user_turn=null`; history: `user u463`, `assistant a900`. | `last_user_turn=u463`, `last_user_message_id=463`, `pending_user=u463` si no visto. |
| `T_NON_USER_UPDATE_PRESERVES_PRIOR_LAST_USER` | Estado previo `last_user_turn=u463`; nuevo latest `tool t901`. | `last_user_turn` sigue `u463`; no se escribe null. |
| `T_CODEX_OPS_DIRECT_USER_IS_PUBLIC_USER` | History user con `front=CODEX-OPS`, `source=telegram_direct`. | Entra como candidato publico del Doctor si el scope coincide. |
| `T_ID_ALIAS_MESSAGE_ID_NORMALIZED` | User trae `message_id`, no `last_user_message_id`. | `last_user_message_id` se deriva correctamente. |
| `T_HISTORY_UNAVAILABLE_DOES_NOT_NULL_LAST_USER` | History read falla; estado previo tiene user no nulo. | Preservar user, health local `history_unavailable_preserved_last_user`. |
| `T_TRUE_EMPTY_SCOPE_ALLOWS_NULL` | Scope nuevo sin user en snapshot ni history. | `last_user_turn=null` permitido con health `no_user_seen`. |
| `T_LATEST_USER_REPLACES_OLDER_LAST_USER` | Estado previo `u462`; latest/history trae `u463`. | Avanza a `u463` monotonicamente. |
| `T_SEEN_REJECTS_ASSISTANT_TOOL` | `mark_seen_user(a900 role=assistant)` o `tool`. | Rechazo/noop; seen intacto. |

## patch_contract

Pseudocodigo de bajo riesgo:

```python
def normalize_public_user(turn):
    if turn.get("role") != "user":
        return None
    source = turn.get("source") or turn.get("front") or "unknown"
    if source == "internal_reprocess":
        return None
    return {
        "turn_id": turn.get("turn_id") or turn.get("id"),
        "message_id": turn.get("message_id") or turn.get("telegram_message_id"),
        "sequence": turn.get("turn_sequence") or turn.get("sequence") or turn.get("message_id"),
        "created_at": turn.get("created_at"),
        "role": "user",
        "source": source,
    }


def derive_last_user_turn(snapshot, history, prior_snapshot, scope):
    candidates = [normalize_public_user(t) for t in history if in_scope(t, scope)]
    candidates = [c for c in candidates if c]
    latest = normalize_public_user(snapshot.get("latest_turn", {}))
    if latest and in_scope(latest, scope):
        candidates.append(latest)

    prior = normalize_public_user((prior_snapshot or {}).get("last_user_turn", {}))
    newest = max_by_sequence(candidates) if candidates else None
    if newest and (not prior or newer(newest, prior)):
        return newest
    if prior:
        return prior
    return None
```

El punto importante no es el formato exacto, sino la propiedad: **un non-user
latest nunca transforma un last-user valido en null**.

## decision

**Integrar patch ahora con inspeccion local del orquestador.**

No puedo aplicar el patch desde esta Mac porque los scripts/snapshots declarados
no existen aqui. Pero el bug observado toca continuidad de pedidos directos y no
conviene dejarlo en backlog. El orquestador deberia revisar la ruta real,
centralizar `derive_last_user_turn`, agregar los fixtures anteriores y ejecutar
tests locales sin Telegram real.

## recommendation

1. Patch inmediato en `codex_telegram_direct.py` y/o
   `codex_desktop_telegram_handoff.py`: reconstruir `last_user_turn` desde
   history y preservar valor previo ante latest assistant/tool.
2. Agregar tests sinteticos para los ocho fixtures de esta auditoria.
3. Agregar health local si `latest_turn_role != user` y `last_user_turn` sale
   nulo pese a existir history o prior snapshot.
4. Bloquear cualquier caller que use `latest_turn` para pending/seen.
5. Pedir una revision postpatch XH con evidencia declarada de `node/python test`
   o unit tests locales, sin adjuntos ni mensajes reales.

## confidence

Media-alta para el root cause probable porque el sintoma coincide con los riesgos
ya documentados: `latest_turn=assistant/tool` domina y anula el user. Media-baja
para certificar implementacion real porque las rutas `/Users/jarvis/.openclaw/...`
no existen en esta Mac y no se inspeccionaron scripts ni state reales.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reviso `jobs/20260528T001728-telegram-direct-last-user-turn-null-audit-v1.md`.
- Se revisaron resultados previos `20260527T194547`, `20260527T210420` y
  `20260527T212430`.
- Se reviso `context/fronts/telegram.md`.
- Se intento inspeccionar los scripts y state permitidos en
  `/Users/jarvis/.openclaw/workspace/...`, pero esas rutas no existen en esta Mac.
- No se uso Telegram real, Gmail, Drive, Calendar, iCloud, Photos, adjuntos reales
  ni servicios externos.

## risks_limits

- Este resultado es auditoria/contrato; no modifica archivos operativos del
  puente Telegram Directo.
- No se leyeron snapshots reales, mensajes reales ni adjuntos.
- Si un consumidor legacy fuera de los dos scripts declarados sigue usando
  `latest_turn`, el riesgo P0 permanece hasta migrarlo o bloquearlo.
- La decision final queda en Codex orquestador.

## evidence_paths

- `jobs/20260528T001728-telegram-direct-last-user-turn-null-audit-v1.md`
- `claims/20260528T001728-telegram-direct-last-user-turn-null-audit-v1.json`
- `results/20260528T001728-telegram-direct-last-user-turn-null-audit-v1.result.md`
- `results/20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1.result.md`
- `results/20260527T210420-telegram-direct-handoff-guardrail-postpatch-review-v1.result.md`
- `results/20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1.result.md`
- `context/fronts/telegram.md`
- `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py`
- `/Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py`
- `/Users/jarvis/.openclaw/workspace/state/codex_live/telegram_direct_handoff*.json*`

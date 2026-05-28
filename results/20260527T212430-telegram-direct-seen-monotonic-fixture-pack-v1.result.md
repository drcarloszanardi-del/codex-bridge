---
job_id: 20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T21:24:49-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram Direct seen monotonic fixture pack v1

## summary

Pack de fixtures y criterios de aceptacion para cerrar el guardrail local de
Telegram Directo -> Codex Desktop. No use Telegram real, no envie mensajes, no
toque credenciales y no lei adjuntos ni datos privados.

La regla central queda asi: `latest_turn` puede existir para display/debug, pero
ninguna ruta de pending o seen debe depender de el. El ultimo pedido publico del
Doctor se reconstruye desde history como `last_user_turn`; `seen_user` solo
avanza con un turno `role=user`, de manera atomica, monotona y scoped por
`chat_id`, `thread_id/topic_id` y `source`.

## coverage_table

| Fuente local | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1.md` | Revisada | Objetivo, restricciones y entregable. |
| `results/20260527T210420-telegram-direct-handoff-guardrail-postpatch-review-v1.result.md` | Revisada | Contrato postpatch, riesgos residuales y fixtures base. |
| `results/20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1.result.md` | Revisada | Riesgo original `latest_turn=assistant/tool` y reglas de continuidad. |
| `state/codex_live/telegram_direct_handoff.json` | No versionado en bridge | Limite: el pack es sintetico/contract-level. |
| `state/codex_live/telegram_direct_handoff_seen.json` | No versionado en bridge | Limite: no se audito implementacion real de escritura. |
| `state/codex_live/telegram_direct_handoff_history.jsonl` | No versionado en bridge | Limite: no se audito history real. |

## fixtures_minimos

| Fixture | Entrada sintetica | Expected |
| --- | --- | --- |
| `T_SEEN_ASSISTANT_AFTER_USER_DOES_NOT_ADVANCE` | `history=[user u462, assistant a900]`, `latest=a900`, `seen_user=461`. | `last_user_turn=u462`, `pending_user=u462`, `seen_user` queda 461. |
| `T_SEEN_TOOL_AFTER_USER_DOES_NOT_HIDE_PENDING` | `history=[user u463, tool t901]`, `latest=t901`, `seen_user=462`. | `pending_user=u463`; tool se muestra solo como contexto. |
| `T_RECONSTRUCT_LAST_USER_FROM_HISTORY_WHEN_SNAPSHOT_LACKS_FIELD` | Snapshot tiene `latest_turn_role=assistant` y no trae `last_user_turn`; history trae `user u463` antes de `assistant a900`. | Parser reconstruye `last_user_turn=u463` desde history y marca pendiente si `seen_user < u463`. |
| `T_RECONSTRUCT_IGNORES_INTERNAL_REPROCESS` | History: `user u463`, `assistant a900`, `tool t901 source=internal_reprocess`; snapshot latest=t901. | `last_user_turn=u463`; no se crea pedido nuevo por reprocess. |
| `T_SEEN_REJECTS_NON_USER_ROLE_ASSISTANT` | `mark_seen_user(candidate=a900 role=assistant)`. | Error local/noop; archivo seen intacto; health event local `rejected_non_user_seen`. |
| `T_SEEN_REJECTS_NON_USER_ROLE_TOOL` | `mark_seen_user(candidate=t901 role=tool)`. | Error local/noop; `seen_user_turn_id` no cambia. |
| `T_SEEN_MONOTONIC_REJECTS_OLDER_USER` | Estado actual `seen_user=u463`; writer intenta `u462`. | Rechazo/noop; estado final sigue `u463`. |
| `T_SEEN_MONOTONIC_ACCEPTS_NEWER_USER` | Estado actual `seen_user=u462`; writer intenta `u463`. | Commit atomico; estado final `u463`. |
| `T_SEEN_CONCURRENT_OLDER_WRITE_LOSES` | Writer A prepara `u462`; writer B confirma `u463`; A intenta rename despues. | A re-lee, detecta retroceso y no pisa `u463`. |
| `T_SEEN_SCOPED_CHAT_THREAD_SOURCE` | Mismo `message_id=463` en scopes `{chat=A, thread=1, source=telegram_direct}` y `{chat=A, thread=2, source=telegram_direct}`. | Seen de thread 1 no afecta thread 2. |
| `T_HISTORY_OUT_OF_ORDER_USES_SEQUENCE_NOT_TIMESTAMP` | `u463` tiene timestamp anterior a `a900`, pero `turn_sequence` mayor que `u462`. | `last_user_turn=u463`; timestamp local no decide orden primario. |
| `T_NO_USER_AFTER_SEEN_HAS_NO_PENDING` | History termina en assistant/tool, ultimo user es `u463`, `seen_user=u463`. | No hay pendiente y no se escribe nuevo seen. |

## pseudocodigo_mark_seen_user

```python
def public_user_turns(history, scope):
    scoped = [
        t for t in history
        if t.chat_id == scope.chat_id
        and t.thread_id == scope.thread_id
        and t.source == scope.source
        and t.role == "user"
        and t.source != "internal_reprocess"
    ]
    return sorted(scoped, key=lambda t: (t.turn_sequence, t.message_id, t.created_at))


def reconstruct_last_user_turn(snapshot, history, scope):
    if snapshot.get("last_user_turn") and snapshot["last_user_turn"]["role"] == "user":
        return snapshot["last_user_turn"]
    turns = public_user_turns(history, scope)
    return turns[-1] if turns else None


def pending_user_turn(snapshot, history, seen_state, scope):
    last_user = reconstruct_last_user_turn(snapshot, history, scope)
    current_seen = seen_state.get(scope.key())
    if not last_user:
        return None
    if not current_seen or last_user.turn_sequence > current_seen.turn_sequence:
        return last_user
    return None


def mark_seen_user(candidate, seen_path, scope, read_seen, write_atomic, log_health):
    if candidate.role != "user":
        log_health("rejected_non_user_seen", turn_id=candidate.turn_id, role=candidate.role)
        return {"ok": False, "reason": "candidate_role_is_not_user"}
    if candidate.source == "internal_reprocess":
        log_health("rejected_internal_reprocess_seen", turn_id=candidate.turn_id)
        return {"ok": False, "reason": "internal_reprocess_is_not_public_user"}

    state = read_seen(seen_path)
    current = state.get(scope.key())
    if current and candidate.turn_sequence < current.turn_sequence:
        log_health("rejected_seen_regression", current=current.turn_id, candidate=candidate.turn_id)
        return {"ok": False, "reason": "seen_user_regression"}

    next_state = state.copy()
    next_state[scope.key()] = {
        "seen_user_turn_id": candidate.turn_id,
        "seen_user_message_id": candidate.message_id,
        "seen_user_sequence": candidate.turn_sequence,
        "seen_at": now_iso(),
        "seen_by": "codex_desktop",
        "scope": scope.as_dict(),
    }

    # write_atomic must use tempfile in same dir, fsync file, atomic rename,
    # fsync dir, then re-read and verify persisted candidate.
    write_atomic(seen_path, next_state)
    persisted = read_seen(seen_path).get(scope.key())
    if persisted["seen_user_turn_id"] != candidate.turn_id:
        log_health("seen_verify_failed", candidate=candidate.turn_id, persisted=persisted)
        return {"ok": False, "reason": "persisted_seen_mismatch"}
    return {"ok": True, "seen_user_turn_id": candidate.turn_id}
```

## riesgos_p0_p1_residuales

| Severidad | Riesgo | Senal de alerta | Accion |
| --- | --- | --- | --- |
| P0 | Una ruta legacy usa `latest_turn_id` para pending. | `latest_turn_role in {assistant, tool}` y Desktop queda sin pending aunque history trae user no visto. | Bloquear merge o activar compat gate: pending se recalcula desde history. |
| P0 | `seen_user` se marca desde assistant/tool. | Health event `rejected_non_user_seen` aparece o tests fallan. | Separar API de seen y prohibir caller generico de "run completed". |
| P0 | Reprocess interno se publica como pedido del Doctor. | `source=internal_reprocess` aparece en pending publico. | Filtrar source en reconstruccion y fixture obligatorio. |
| P1 | Escritura atomica incompleta. | Seen final retrocede o archivo queda truncado tras carrera/interrupcion. | Tempfile en mismo directorio + fsync + rename + verify reread. |
| P1 | Scope incompleto contamina threads. | Seen de un thread borra pendiente de otro. | Scope obligatorio `chat_id/thread_id/source`; fixture de colision. |
| P1 | Orden por timestamp local. | History out-of-order cambia ultimo user. | Orden canonico por `turn_sequence`; timestamp solo desempate. |

## recomendacion

Implementar ahora en Codex principal:

1. Funcion unica `reconstruct_last_user_turn(snapshot, history, scope)`.
2. Funcion unica `pending_user_turn(...)` que ignore `latest_turn` como source of truth.
3. Funcion unica `mark_seen_user(...)` con rechazo de roles no-user, monotonicidad y scope.
4. Los 12 fixtures de este pack en tests locales, sin Telegram real ni datos privados.

Dejar en observacion 24 a 48 horas:

1. Conteo local de divergencias `latest_turn_role != user` con `pending_user` reconstruido.
2. Conteo de rechazos `rejected_non_user_seen` y `rejected_seen_regression`.
3. Cualquier consumidor legacy que lea `latest_turn` para pending/seen.

Decision sugerida: no considerar cerrado el guardrail hasta que los tests prueben
las tres rutas criticas: assistant posterior, tool posterior y reconstruccion
desde history cuando falta `last_user_turn` en snapshot.

## confidence

Alta para el pack de fixtures y criterios porque deriva directamente de los dos
resultados previos `20260527T194547` y `20260527T210420`. Media para el estado
real del Desktop local porque los scripts/snapshots sanitizados no estan en este
bridge.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reviso `jobs/20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1.md`.
- Se revisaron `results/20260527T210420-telegram-direct-handoff-guardrail-postpatch-review-v1.result.md` y `results/20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1.result.md`.
- No se uso Telegram real, Gmail, Drive, iCloud, Photos, adjuntos reales ni servicios externos.

## risks_limits

- Este entregable es un pack sintetico/contract-level; no certifica el codigo real de Desktop.
- Si hay consumidores legacy fuera del bridge que todavia usan `latest_turn` para pending o seen, el riesgo P0 permanece hasta migrarlos o bloquearlos.
- La decision final de integracion queda en Codex orquestador.

## evidence_paths

- `jobs/20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1.md`
- `claims/20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1.json`
- `results/20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1.result.md`
- `results/20260527T210420-telegram-direct-handoff-guardrail-postpatch-review-v1.result.md`
- `results/20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1.result.md`
- `state/codex_live/telegram_direct_handoff.json`
- `state/codex_live/telegram_direct_handoff_seen.json`
- `state/codex_live/telegram_direct_handoff_history.jsonl`

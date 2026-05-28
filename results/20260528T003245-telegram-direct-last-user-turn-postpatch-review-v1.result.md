---
job_id: 20260528T003245-telegram-direct-last-user-turn-postpatch-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-28T00:34:32-03:00
front: TELEGRAM
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram Direct last user turn postpatch review v1

## summary

Veredicto: **aceptar en observacion el patch local declarado** para el bug
`last_user_turn:null` en Telegram Directo -> Codex Desktop.

El contrato declarado cubre los puntos criticos pedidos: `latest_turn` non-user,
history con ultimo user, prior snapshot no nulo, alias `telegram_message_id` y
scope sin user. La evidencia del orquestador tambien muestra la senal operativa
clave: el writer real dejo `latest_turn_id=5382`, `last_user_message_id=473` y
`handoff_guardrail_status=last_user_present`, que es el comportamiento esperado
cuando el ultimo turno visible no-user no debe borrar el ultimo user.

No recomiendo revertir ni abrir otro ciclo obligatorio. Mantener observacion y
monitoreo local de health; no enviar mensajes externos ni tocar datos reales.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260528T003245-telegram-direct-last-user-turn-postpatch-review-v1.md` | Revisada | Workorder, patch declarado, checks locales y entregables. |
| `results/20260528T001728-telegram-direct-last-user-turn-null-audit-v1.result.md` | Revisada | Root cause probable, contrato monotono y fixtures esperados. |
| `results/20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1.result.md` | Revisada | Criterio de seen/user monotono, reconstruccion desde history y riesgos residuales. |
| `context/fronts/telegram.md` | Revisada | Canon Telegram Directo, entrega real, idempotencia y restricciones de frente. |
| `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py` | Ausente en esta Mac | Limite: no se inspecciono el diff real. |
| `/Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py` | Ausente en esta Mac | Limite: no se inspecciono el consumer real. |
| `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py` | Ausente en esta Mac | Limite: tests tomados como evidencia declarada del orquestador. |

## contract_coverage

| Caso pedido | Cubierto | Evidencia declarada | Observacion |
| --- | --- | --- | --- |
| `latest_turn` non-user | Si | Preserva `last_user_turn` ante `assistant/tool`; snapshot final conserva `last_user_message_id=473` con `latest_turn_id=5382`. | Es el bug central; aceptar si no hay rutas legacy. |
| History con ultimo user | Si | Derivacion reconstruye desde `telegram_direct_handoff_history.jsonl`. | Debe ordenar por secuencia/id estable, no solo timestamp. |
| Prior snapshot no nulo | Si | Patch preserva ultimo user ante latest assistant/tool. | Evita overwrite a null. |
| Alias `telegram_message_id` | Si | Normaliza `message_id`/`telegram_message_id`. | Mantener asercion de `last_user_message_id`. |
| Scope sin user | Si | Fixture/contrato permite null solo en scope verdaderamente vacio. | Debe emitir status claro, no confundir con fallo de history. |

## risks_p0_p1

| Pri | Riesgo restante | Condicion | Accion |
| --- | --- | --- | --- |
| P0 | Consumidor legacy sigue usando `latest_turn` para pending/seen. | Desktop u otro script ignora `last_user_turn` y decide desde `latest_turn_id`. | Buscar/migrar callers; mantener health cuando `latest_turn_role != user`. |
| P0 | Un writer posterior vuelve a nullear `last_user_turn`. | Ruta no cubierta serializa snapshot desde latest non-user sin prior/history. | Centralizar derivacion en una funcion unica; tests deben cubrir writer real. |
| P1 | Carrera de escritura entre producer y Desktop. | Dos writers actualizan handoff/seen fuera de orden. | Tempfile + fsync + rename, re-read y rechazo de regresion. |
| P1 | Scope incompleto mezcla directos o topics. | Mismo `message_id` o user en chat/thread/source distinto. | Scope obligatorio por chat/thread/source. |
| P1 | History no disponible se interpreta como scope vacio. | Error de lectura produce `last_user_turn=null`. | Preservar prior no nulo y status `history_unavailable_preserved_last_user`. |
| P1 | Internal reprocess se toma como user publico. | Late media/tool source interno entra como pending. | Filtrar `source=internal_reprocess`. |

No veo P0/P1 que obligue a pedir ajuste inmediato con la evidencia declarada. El
riesgo residual principal es de cobertura de consumidores legacy y carrera real,
no del contrato del patch.

## ajustes_concretos

No hay ajustes obligatorios antes de observacion.

Ajustes opcionales, de bajo riesgo, para mantenimiento:

1. Agregar un test `T_REAL_WRITER_NON_USER_UPDATE_PRESERVES_LAST_USER` que invoque el writer real dos veces: primero user, luego tool/assistant.
2. Agregar un test de error de history: history unreadable + prior snapshot no nulo debe preservar user y setear health.
3. Agregar assert de que `handoff_guardrail_status` nunca sea `last_user_present` si `last_user_message_id` queda null.
4. Agregar test de scope collision con mismo `telegram_message_id` en dos topics/sources.
5. Grep/QA local para asegurar que ningun caller calcula pending desde `latest_turn_id`.

Estos no bloquean aceptar el patch declarado.

## decision

**Aceptar en observacion.**

```yaml
decision: accept_observation
patch: telegram_direct_last_user_turn_monotonic
required_properties:
  latest_turn_non_user_does_not_null_last_user: true
  reconstruct_from_history: true
  preserve_prior_last_user: true
  normalize_message_id_aliases: true
  allow_null_only_for_true_empty_scope: true
  no_external_messages: true
next_cycle_required: false
```

## recommendation

Mantener el patch integrado en observacion. No pedir otro ciclo ahora salvo que
aparezca alguno de estos sintomas locales:

- `handoff_guardrail_status=last_user_present` con `last_user_message_id=null`.
- `latest_turn_role in {assistant, tool}` y `last_user_turn=null` cuando history
  o prior snapshot tiene user.
- `seen_user` avanza con role non-user.
- un pedido directo real queda pendiente en history pero no visible en Desktop.

QA minimo a conservar:

```bash
python3 /Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py
python3 -m py_compile /Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py /Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py
```

## confidence

Media-alta para aceptar en observacion porque el patch declarado implementa las
propiedades pedidas y los checks locales del orquestador pasaron con ocho tests.
Media-baja para certificar codigo real porque las rutas `/Users/jarvis/.openclaw`
no existen en esta Mac y no se inspeccionaron los scripts ni snapshots.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reviso `jobs/20260528T003245-telegram-direct-last-user-turn-postpatch-review-v1.md`.
- Se revisaron `results/20260528T001728-telegram-direct-last-user-turn-null-audit-v1.result.md` y `results/20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1.result.md`.
- Se reviso `context/fronts/telegram.md`.
- Se intento inspeccionar los scripts/tests permitidos en `/Users/jarvis/.openclaw/workspace/...`, pero esas rutas no existen en esta Mac.
- No se uso Telegram real, Gmail, Drive, Calendar, iCloud, Photos, adjuntos reales
  ni servicios externos.

## risks_limits

- Este resultado valida contrato y evidencia declarada; no certifica el diff real.
- No se leyeron snapshots reales ni material sensible.
- Si queda algun consumidor legacy fuera de los scripts declarados, puede persistir
  el riesgo P0 hasta migrarlo.
- La decision final queda en Codex orquestador.

## evidence_paths

- `jobs/20260528T003245-telegram-direct-last-user-turn-postpatch-review-v1.md`
- `claims/20260528T003245-telegram-direct-last-user-turn-postpatch-review-v1.json`
- `results/20260528T003245-telegram-direct-last-user-turn-postpatch-review-v1.result.md`
- `results/20260528T001728-telegram-direct-last-user-turn-null-audit-v1.result.md`
- `results/20260527T212430-telegram-direct-seen-monotonic-fixture-pack-v1.result.md`
- `context/fronts/telegram.md`
- `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py`
- `/Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py`
- `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py`

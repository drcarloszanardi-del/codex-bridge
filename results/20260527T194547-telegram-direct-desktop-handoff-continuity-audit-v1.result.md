---
job_id: 20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T20:42:43-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram Direct Desktop handoff continuity audit v1

## summary

Auditoria de continuidad del puente Telegram Directo -> Codex Desktop basada en
el bridge local. No use Telegram real, no envie mensajes, no toque credenciales
y no lei adjuntos reales.

Hallazgo honesto: los artefactos exactos pedidos para el handoff Desktop no
estan versionados en este repo (`state/codex_live/...` y `scripts/...` faltan en
el bridge). Por eso no puedo certificar el estado real del script Desktop ni del
archivo `latest_turn`. Si el orquestador quiere cierre exacto, debe subir un
paquete sanitizado con esos cinco archivos o sus fragmentos relevantes.

Con la evidencia disponible, el riesgo principal es P0/P1 de continuidad:
si `latest_turn` queda apuntando a `assistant` o `tool`, Desktop puede marcar
como visto un turno que no corresponde al ultimo mensaje de usuario, ocultar un
mensaje nuevo, mezclarlo con una respuesta previa o generar ruido de sync. La
solucion de bajo riesgo es separar explicitamente `last_user_turn_id`,
`last_assistant_turn_id`, `latest_turn_id`, `seen_user_turn_id` y un `pending`
calculado solo sobre turnos `role=user`.

## coverage_table

| Fuente local | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1.md` | Revisada | Objetivo, restricciones y caso message_id 463. |
| `state/codex_live/telegram_direct_handoff.json` | No existe en bridge | Se registra como limite P1: no se pudo auditar `latest_turn` real. |
| `state/codex_live/telegram_direct_handoff_seen.json` | No existe en bridge | Se registra como limite P1: no se pudo auditar sync visto real. |
| `state/codex_live/telegram_direct_handoff_history.jsonl` | No existe en bridge | Se registra como limite P1: no se pudo auditar secuencia/history real. |
| `scripts/codex_desktop_telegram_handoff.py` | No existe en bridge | Se registra como limite P1: no se pudo auditar algoritmo Desktop real. |
| `scripts/codex_telegram_direct.py` | No existe en bridge | Se uso evidencia indirecta por resultados previos del frente Telegram. |
| `context/fronts/telegram.md` | Revisada | Canon: buffer de adjuntos, delivery real, ContextBinder y deudas. |
| `results/20260527T162339-telegram-contralor-action-media-arrived-after-response.result.md` | Revisada | Riesgo de respuesta antes de adjuntos/documentos tardios. |
| `results/20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1.result.md` | Revisada | Patch `DIRECT 7s/22s`, modo observacion y fixtures faltantes. |
| `results/20260527T170359-telegram-contralor-action-media-only-after-assistant-completion.result.md` | Revisada | Riesgo post-completion y guard posterior. |
| `results/20260527T170404-telegram-contralor-action-media-only-after-assistant-completion.result.md` | Revisada | Companion 443/444 y dedupe por cluster. |
| `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md` | Revisada | Route strength, media group handled y DIRECT/topic policy. |

## findings

| Severidad | Hallazgo | Evidencia | Impacto |
| --- | --- | --- | --- |
| P0 | Desktop puede perder un mensaje de usuario si `seen` compara contra `latest_turn` sin filtrar `role=user`. | El job informa que `latest_turn` puede quedar en `assistant/tool`; los archivos reales no estan en bridge para descartar esta condicion. | Un mensaje entrante posterior podria quedar sin notificacion o sin procesamiento humano visible. |
| P0 | Riesgo de mezclar respuesta `assistant/tool` con nuevo pedido directo. | Incidentes previos documentan media tardia, completion previa y reprocess interno; el nuevo job menciona correccion clinica resuelta desde Desktop. | Desktop podria mostrar continuidad falsa: "ya respondido" aunque haya una correccion nueva. |
| P1 | Falta snapshot sanitizado del handoff Desktop. | Los cinco paths pedidos resultaron `MISSING` en el repo. | No hay auditoria exacta de `message_id=463`; la recomendacion es conceptual y fixture-level. |
| P1 | `prior_assistant_message_id` y `prior_run_id` deben ser obligatorios en handoff/contralor. | Resultados `170359/170404` muestran `prior_assistant_message_id: null` como limite. | Sin attribution, Desktop y contralor deduplican peor y pueden abrir actions duplicadas. |
| P1 | La frontera "sync visto" debe ser silenciosa y atomica. | El objetivo pide sincronizar visto sin ruido; canon Telegram exige ACK no ruidoso e idempotencia. | Actualizaciones repetidas de `seen` pueden generar ruido o carreras si no usan escritura atomica. |

## continuity_risks

1. `latest_turn.role != "user"` y Desktop marca `seen_latest_turn_id`: se pierde
   el verdadero ultimo mensaje de usuario pendiente.
2. Un `tool` turn posterior a un usuario tapa una correccion clinica que llego
   despues, porque Desktop interpreta el thread como "procesado".
3. `message_id=463` con timeout DIRECT queda como ultimo user pendiente, pero
   un assistant/tool posterior mueve el puntero y oculta la deuda.
4. Handoff history registra eventos fuera de orden por timestamp de escritura,
   no por `telegram_message_id`/`turn_id`; Desktop muestra continuidad incorrecta.
5. Dos instancias Desktop/poller escriben `telegram_direct_handoff_seen.json` sin
   lock ni rename atomico y retroceden el puntero visto.
6. Un late-media reprocess interno queda asociado al run previo, pero Desktop lo
   ve como nuevo pedido del usuario si falta `origin=internal_reprocess`.

## fixtures_reglas_sugeridas

| Fixture | Entrada sintetica | Esperado |
| --- | --- | --- |
| `T_DESKTOP_LATEST_ASSISTANT_DOES_NOT_HIDE_USER` | History: user 462, assistant 900, user 463, tool 901; latest_turn=tool. | `pending_user_turn_id=463`; no marcar visto por `latest_turn=tool`. |
| `T_DESKTOP_SEEN_ONLY_ADVANCES_ON_USER_TURN` | `seen_user_turn_id=462`; latest assistant/tool posterior. | `seen_user_turn_id` no avanza hasta que usuario 463 sea tratado. |
| `T_DESKTOP_TIMEOUT_DIRECT_REMAINS_PENDING` | user 463 con `delivery_timeout` o run timeout. | Desktop muestra pending/action_needed, no `synced`. |
| `T_DESKTOP_CLINICAL_CORRECTION_WINS_OVER_PRIOR_ASSISTANT` | assistant final previo + user correction posterior. | Correccion se muestra como nuevo pendiente, con `supersedes_prior_response=true`. |
| `T_DESKTOP_TOOL_TURN_IS_CONTEXT_NOT_REQUEST` | tool output despues de assistant. | No crea solicitud nueva ni cambia `last_user_turn_id`. |
| `T_DESKTOP_SEEN_WRITE_IS_ATOMIC_MONOTONIC` | Dos updates concurrentes, uno viejo y uno nuevo. | El visto final queda en el user turn mas nuevo; nunca retrocede. |
| `T_DESKTOP_INTERNAL_REPROCESS_NOT_PUBLIC_USER` | late media guard crea reprocess interno. | Desktop lo marca `internal_reprocess`, no pedido directo del Doctor. |

Reglas de gate:

```text
last_user_turn = newest(turn where role == "user")
pending_user_turn = last_user_turn if last_user_turn.id > seen_user_turn_id else null
latest_turn is display/context only; never the source of truth for pending work
assistant/tool turns can close a run but cannot advance seen_user_turn_id
seen writes must be atomic, monotonic and scoped by chat_id/topic_id/source
```

## cambios_bajo_riesgo_propuestos

1. En `telegram_direct_handoff.json`, agregar campos derivados:
   `last_user_turn_id`, `last_user_message_id`, `last_user_created_at`,
   `latest_turn_id`, `latest_turn_role`, `pending_user_turn_id`,
   `pending_reason`.
2. En `telegram_direct_handoff_seen.json`, guardar solo visto de usuario:
   `seen_user_turn_id`, `seen_user_message_id`, `seen_at`, `seen_by`,
   `source_file_sha256`.
3. En Desktop, calcular disponibilidad de trabajo desde `pending_user_turn_id`,
   no desde `latest_turn`.
4. Si `latest_turn_role in {"assistant", "tool"}` y existe user posterior no
   visto, mostrarlo como `pending_after_assistant` sin notificacion publica.
5. Escribir `seen` con tempfile + fsync + rename atomico; rechazar updates que
   retrocedan `seen_user_turn_id`.
6. Registrar `prior_run_id` y `prior_assistant_message_id` cuando hay late media
   o correction after completion; si falta, usar `unattributed_completion` pero
   no marcar como sync sano.
7. Agregar `source=telegram_direct|desktop|internal_reprocess` para que Desktop
   no confunda reprocess internos con mensajes nuevos del usuario.

## paquete_sanitizado_necesario

Para cerrar el caso `message_id=463` con evidencia exacta, subir al bridge una
version sanitizada de:

```text
state/codex_live/telegram_direct_handoff.json
state/codex_live/telegram_direct_handoff_seen.json
state/codex_live/telegram_direct_handoff_history.jsonl
scripts/codex_desktop_telegram_handoff.py
scripts/codex_telegram_direct.py
```

Sanitizacion minima: conservar roles, ids, timestamps, route, status, run_id,
message_id, delivery state y hashes; remover textos privados, tokens, paths de
adjuntos reales y credenciales.

## recommendation

No cerrar como "auditado exacto" hasta que existan los artefactos sanitizados del
handoff Desktop. Como siguiente patch seguro, implementar la politica
`last_user_turn_id` / `seen_user_turn_id` y los siete fixtures anteriores. La
regla clave: `assistant` y `tool` pueden explicar contexto, pero nunca deben ser
la base para decidir que no hay mensaje de usuario pendiente.

## confidence

Media-alta para el riesgo y las reglas propuestas, porque coinciden con los
incidentes previos de Telegram Directo, media tardia y post-completion. Media
para el estado real de Desktop porque los archivos exactos no estan en el
bridge y no se inspecciono la Mac de trabajo. Alta en que no se realizaron
acciones externas ni se tocaron secretos.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se creo claim local para `20260527T194547`.
- Se verifico que los cinco paths exactos pedidos no existen en el bridge.
- Se revisaron `context/fronts/telegram.md` y resultados previos relevantes del
  frente Telegram.
- No se uso Telegram real, Gmail, Drive, Calendar, Photos/iCloud ni adjuntos
  reales.

## risks_limits

- El resultado no inspecciona `message_id=463` real; solo el contexto declarado
  por el workorder.
- Un intento de busqueda amplia de nombres de archivo fue interrumpido al ver
  que el host recorria directorios no pertinentes; no se leyo contenido privado
  ni se usaron servicios externos.
- La decision final de integracion queda en Codex orquestador.

## evidence_paths

- `jobs/20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1.md`
- `claims/20260527T194547-telegram-direct-desktop-handoff-continuity-audit-v1.json`
- `context/fronts/telegram.md`
- `results/20260527T162339-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1.result.md`
- `results/20260527T170359-telegram-contralor-action-media-only-after-assistant-completion.result.md`
- `results/20260527T170404-telegram-contralor-action-media-only-after-assistant-completion.result.md`
- `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md`

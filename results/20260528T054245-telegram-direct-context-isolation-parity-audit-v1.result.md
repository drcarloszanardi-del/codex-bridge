---
job_id: 20260528T054245-telegram-direct-context-isolation-parity-audit-v1
worker: personal-xh
status: completed
completed_at: 2026-05-28T05:48:47-03:00
front: TELEGRAM
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram Direct context isolation parity audit v1

## summary

Auditoria segura y declarativa del puente Telegram Directo -> Codex Desktop,
enfocada en paridad de calidad y aislamiento de contexto. No use Telegram real,
no abri adjuntos, no envie mensajes externos y no lei secretos.

Hallazgo central: el contrato existente ya cubre parte critica del riesgo
`latest_turn`/`seen`, pero todavia falta cerrar de forma explicita la frontera
de **identidad del trabajo**: `front + chat_id + thread/topic_id + source +
job_id + material_set_id + target_document_id`. Sin esa identidad, Telegram
Directo puede tener el mismo motor que Desktop y aun asi mezclar un reel nuevo
con un reel anterior, afirmar elementos visuales no declarados, o aplicar una
correccion clinica sobre el protocolo equivocado.

Decision sugerida: **agregar tests locales y mantener en observacion**. No veo
un bloqueo que requiera autorizacion humana inmediata con la evidencia disponible,
pero no declararia cierre definitivo hasta que pasen fixtures de aislamiento por
material/reel/documento y un test de paridad de contrato Directo vs Desktop.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260528T054245-telegram-direct-context-isolation-parity-audit-v1.md` | Revisada | Objetivo, alcance y ejemplos a cubrir. |
| `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py` | Ausente en esta Mac | No se pudo auditar codigo real del producer. |
| `/Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py` | Ausente en esta Mac | No se pudo auditar codigo real del consumer Desktop. |
| `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py` | Ausente en esta Mac | Tests reales tomados solo como evidencia declarada previa. |
| `/Users/jarvis/.openclaw/workspace/state/codex_live/` | Ausente en esta Mac | No se leyeron snapshots reales ni adjuntos. |
| `results/20260528T004910-telegram-direct-static-guard-postpatch-review-v1.result.md` | Revisada | Guard estatico para `latest_turn` y cierre en observacion. |
| `results/20260528T003850-telegram-direct-consumer-legacy-pending-audit-v1.result.md` | Revisada | Riesgos de consumidores legacy y patrones `rg`. |
| `results/20260527T210420-telegram-direct-handoff-guardrail-postpatch-review-v1.result.md` | Revisada | Contrato `last_user_turn`/`seen_user` monotono. |
| `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md` | Revisada | Riesgos de contaminacion por rutas, hints y adjuntos sin caption. |
| `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md` | Revisada | ContextBinder, ResetScope, media buffer y reply target. |

## flujo_direct_to_desktop

Mapa operativo esperado:

```text
Telegram Direct event
  -> event store sanitizado
  -> router/topic mapper
  -> media/document buffer y attachment manifest
  -> ContextBinder por front/topic/material
  -> handoff snapshot en state/codex_live
  -> Desktop poller/consumer
  -> Codex run con contrato de calidad unico
  -> result/delivery gate con destino trazable
```

Puntos donde puede perderse contexto:

| Punto | Perdida posible | Guardia minima |
| --- | --- | --- |
| Event intake | `topic_id`/`thread_id` nulo o incorrecto. | `UNKNOWN_REVIEW` si no hay topic real ni ruta explicita. |
| Router | Hint debil muta `active_route`. | `route_strength=weak_hint` nunca cambia scope activo. |
| Media buffer | Fotos/PDF sin caption quedan huerfanos o se pegan al job previo. | `material_set_id` nuevo por cluster y maximo un job por cluster. |
| ContextBinder | Trae contexto de otro frente/reel. | Filtrar por `front + topic_id + job_id + material_set_id`. |
| Handoff | `latest_turn` assistant/tool tapa el ultimo user. | Pending desde `last_user_turn`; latest solo display/debug. |
| Seen | Assistant/tool avanza visto. | `mark_seen_user` acepta solo role user, monotono y scoped. |
| Desktop quality | Directo usa contrato menor que Desktop. | Mismo checklist de evidencia, no-invencion, pruebas y gates. |
| Delivery | Resultado de topic sale por canal principal. | `reply_target == job.topic_id` o override aprobado. |

## evidencia_local_verificada

- Las rutas exactas de la Mac del orquestador bajo
  `/Users/jarvis/.openclaw/workspace/...` no existen en esta Mac.
- En el bridge si existen auditorias previas que documentan:
  - `latest_turn` debe ser display/debug, no source of truth.
  - `last_user_turn` y `seen_user` deben ser monotono y por usuario.
  - `topic_id` real tiene prioridad sobre inferencias.
  - `UNKNOWN_REVIEW` protege topics desconocidos o ambiguos.
  - `ContextBinder` y `media_buffer_closed_before_model_call` son gates P0.

## inferencias

- Infiero que la paridad de calidad no se garantiza solo por usar el mismo
  modelo. Debe probarse que el canal Directo pasa por el mismo contrato operativo
  que Desktop: evidence-first, no invencion visual, target document required,
  media buffer cerrado, pre-send gate y resultado trazable.
- Infiero que el riesgo de mezcla mas probable ya no es `latest_turn` puro, sino
  identidad incompleta de material/documento cuando un pedido Directo llega con
  adjuntos o correcciones cortas.

## risks_p0_p1_p2

| Pri | Riesgo | Escenario sintetico | Mitigacion |
| --- | --- | --- | --- |
| P0 | Reel nuevo hereda material o topic previo. | Directo: "nuevo reel con estas fotos" despues de reel CMP anterior. | Nuevo `material_set_id`; no usar prior `asset_manifest` salvo referencia explicita. |
| P0 | Se inventan elementos visuales no presentes. | Modelo describe "doctor en quirofano" sin evidencia en adjuntos declarados. | Claims visuales solo si hay media evidence id o transcript OCR/vision verificado. |
| P0 | Correccion clinica toca protocolo equivocado. | "cambia esa frase" sin `target_document_id` ni seccion. | Bloquear y pedir target; no aplicar por memoria global. |
| P0 | `latest_turn`/assistant/tool oculta user pendiente. | Tool posterior queda como latest; user anterior no visto. | Mantener guard de `last_user_turn` y seen no-user reject. |
| P0 | Delivery cruza front. | Resultado REELS sale al canal principal o a otro topic. | `reply_target` debe coincidir con `job.topic_id` o override. |
| P1 | Directo usa menor calidad que Desktop. | Job directo omite checklist de evidencia o QA final. | `quality_contract_id` comun para Directo y Desktop. |
| P1 | Hint debil contamina active route. | "la voz quedo rara" hereda REELS aunque era clinico. | `route_strength=weak_hint`; no crear job largo. |
| P1 | Snapshot legacy sin `last_user_turn` se toma como sano. | `last_user_turn=null` pero history tiene user. | Reconstruir desde history o health blocking. |
| P1 | Consumer fuera del grep sigue usando latest. | Dashboard/poller lee `latest_turn_id` para pending. | `rg` amplio del workspace y static guard indirecto. |
| P2 | Display muestra latest assistant y confunde revision humana. | UI presenta cierre como si fuera user. | Etiquetas claras: latest/display vs pending/source. |
| P2 | Buffer muy conservador demora Directo simple. | Texto sin adjuntos espera ventana completa. | Bypass solo para comandos seguros y testeados. |

## fixtures_tests_propuestos

1. `direct_reel_new_material_does_not_inherit_previous_topic`
   - Entrada: scope previo `front=REELS`, `topic_id=reels_cmp`, `material_set_id=A`.
     Nuevo Directo: "#REELS nuevo montaje con estas fotos" + media cluster B.
   - Esperado: job nuevo con `material_set_id=B`, sin assets A, sin copy ni claims
     heredados salvo referencia explicita del usuario.

2. `direct_visual_claim_requires_declared_media_evidence`
   - Entrada: pedido de montaje con dos imagenes declaradas sin metadata de un
     elemento especifico.
   - Esperado: toda afirmacion visual debe apuntar a `media_id`/evidence; si no,
     queda como "no verificado" o se omite.

3. `clinical_edit_requires_target_document_identity`
   - Entrada: "cambia la parte de hemostasia" desde Directo con dos protocolos
     clinicos recientes.
   - Esperado: no modifica nada sin `target_document_id`/seccion; genera pedido
     de aclaracion o `UNKNOWN_REVIEW`.

4. `assistant_turn_never_reopens_seen_user_turn`
   - Entrada: history user 100, assistant 200, tool 201; `seen_user=99`.
   - Esperado: pending user 100 sigue abierto; assistant/tool no avanzan seen.

5. `direct_desktop_same_quality_contract_for_deliverables`
   - Entrada: mismo pedido sintetico por Desktop y por Directo.
   - Esperado: ambos pasan por el mismo `quality_contract_id`: evidence gate,
     no-secrets, media-buffer-closed, no-raw-diff, result trace.

6. `weak_hint_does_not_mutate_active_route_or_material_scope`
   - Entrada: "esa voz quedo rara" despues de un reel y despues de un caso
     clinico.
   - Esperado: `route_strength=weak_hint`, no crea job largo, no cambia
     `active_route`, y no hereda material sin explicit deliverable.

## comandos_sugeridos_para_orquestador

Como las rutas reales no existen en esta Mac, el cierre local deberia correr en
la Mac del orquestador:

```bash
rg -n "material_set|asset_manifest|attachment|media_id|target_document|topic_id|thread_id|front|route_strength|ContextBinder" /Users/jarvis/.openclaw/workspace/scripts /Users/jarvis/.openclaw/workspace/tests
rg -n "latest_turn|last_user_turn|seen_user|pending|mark_seen" /Users/jarvis/.openclaw/workspace/scripts /Users/jarvis/.openclaw/workspace/tests
rg -n "UNKNOWN_REVIEW|weak_hint|active_route|reply_target|delivery_target" /Users/jarvis/.openclaw/workspace/scripts /Users/jarvis/.openclaw/workspace/tests
```

Si cualquiera de esos grep encuentra un uso de `latest_turn` para pending/seen,
un `active_route` que se hereda sin TTL/thread real, o un claim visual sin
evidence id, tratarlo como P0/P1 y parchear antes del cierre.

## recommendation

Agregar tests locales antes de cerrar definitivamente. Mantener el puente en
observacion si:

- `latest_turn` queda solo display/debug;
- pending y seen siguen basados en `last_user_turn`/`seen_user`;
- cada job Directo tiene scope completo;
- todo material nuevo tiene `material_set_id`;
- ediciones clinicas exigen `target_document_id`;
- el contrato de calidad es identico para Desktop y Directo.

Pedir autorizacion humana solo si el grep o fixtures detectan un P0 real:
mezcla efectiva de material, edicion clinica sin target, o delivery a topic/canal
incorrecto.

## confidence

Media-alta para el mapa de riesgos y fixtures, porque se apoya en auditorias
previas del bridge y en incidentes ya documentados. Media-baja para certificar
la implementacion actual, porque las rutas reales de `/Users/jarvis/.openclaw`
no existen en esta Mac y no se inspeccionaron snapshots ni adjuntos reales.

## attempted_routes

- Se hizo `git pull --rebase origin main`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reviso el workorder actual.
- Se intentaron listar las rutas permitidas bajo `/Users/jarvis/.openclaw`, pero
  no existen en esta Mac.
- Se revisaron resultados previos del bridge relacionados con `latest_turn`,
  seen monotono, contaminacion por routing, topic routing y media buffer.
- No se uso Telegram real, Gmail, Drive, Calendar, iCloud, Photos, adjuntos
  reales ni servicios externos.

## risks_limits

- Resultado declarativo: no certifica codigo real del puente.
- No se imprimieron secretos, tokens, rutas de adjuntos privados ni datos
  clinicos identificables.
- Los fixtures propuestos deben portarse al repo real del orquestador.
- La decision final queda en Codex orquestador.

## evidence_paths

- `jobs/20260528T054245-telegram-direct-context-isolation-parity-audit-v1.md`
- `results/20260528T054245-telegram-direct-context-isolation-parity-audit-v1.result.md`
- `results/20260528T004910-telegram-direct-static-guard-postpatch-review-v1.result.md`
- `results/20260528T003850-telegram-direct-consumer-legacy-pending-audit-v1.result.md`
- `results/20260527T210420-telegram-direct-handoff-guardrail-postpatch-review-v1.result.md`
- `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md`
- `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md`
- `results/20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1.result.md`
- `/Users/jarvis/.openclaw/workspace/scripts/codex_telegram_direct.py`
- `/Users/jarvis/.openclaw/workspace/scripts/codex_desktop_telegram_handoff.py`
- `/Users/jarvis/.openclaw/workspace/tests/telegram/test_desktop_handoff_guardrail.py`
- `/Users/jarvis/.openclaw/workspace/state/codex_live/`

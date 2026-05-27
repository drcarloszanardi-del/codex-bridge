---
job_id: 20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1
worker: personal-xh
status: completed
completed_at: 2026-05-27T16:41:00-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram direct late PDF buffer postpatch review v1

## summary

Veredicto: **aceptar en observacion**.

Segun el orquestador, el patch agrega una ventana corta para texto `DIRECT`
no-comando, incluye documentos/PDF dentro de `message_has_downloadable_media`,
preserva prioridad de rutas explicitas como `REELS`, y mantiene las suites
postfix, direct reels voice routing y delivery receipt en verde. Eso ataca la
causa probable del incidente `media_arrived_after_response`: una respuesta final
antes de que cerrara la ventana de adjuntos cercanos.

No recomiendo revertir. La ventana `7s/22s` es razonable para `DIRECT`: suma una
latencia pequeña, pero evita respuestas incompletas cuando el Doctor manda texto
y enseguida un PDF. La condicion importante es que el buffer sea silencioso y no
envie un ACK publico ni doble respuesta.

## coverage_table

| Fuente | Estado | Uso |
| --- | --- | --- |
| `jobs/20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1.md` | Revisada | Workorder, patch descrito y QA local declarado. |
| `context/fronts/telegram.md` | Revisada | Canon Telegram: buffer de adjuntos, delivery real y ContextBinder. |
| `results/20260527T162339-telegram-contralor-action-media-arrived-after-response.result.md` | Revisada | Diagnostico previo y fixtures esperados. |
| `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md` | Revisada | Caso previo de adjuntos tardios. |
| `results/20260525T111222-telegram-contralor-action-media-arrived-after-response.result.md` | Revisada | Caso REELS con album tardio. |
| `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md` | Revisada | Suite postfix de media buffer y captionless attachments. |
| `results/20260526T071000-telegram-t13-postfix-final-review-v1.result.md` | Revisada | Limites de nearby media route correction. |

## findings

| Severidad | Hallazgo | Evidencia | Decision |
| --- | --- | --- | --- |
| P1 | Patch cubre el borde DIRECT + PDF tardio. | El workorder declara texto DIRECT no-comando abre buffer `7s/22s`, documentos cuentan como downloadable media y media buffer policy reporta 1 documento. | Aceptar en observacion. |
| P1 | Rutas explicitas conservan prioridad. | Workorder declara que texto REELS directo conserva `route=REELS`; suites direct reels voice y postfix OK. | Bajo riesgo de regresion si se mantiene este orden. |
| P1 | Falta evidencia directa del diff real en este host. | No se inspecciono `/Users/jarvis/.openclaw/workspace/...`; QA tomado como declaracion del orquestador. | No promover a cierre definitivo sin observacion/contralor. |

## riesgos_p0_p1

| Pri | Riesgo | Impacto | Mitigacion |
| --- | --- | --- | --- |
| P0 | Respuesta publica antes de flush si queda algun camino bypass. | Repite el incidente visible al Doctor. | Todas las llamadas al modelo y final response deben pasar por el gate de buffer abierto. |
| P1 | Latencia perceptible en mensajes DIRECT simples. | El Doctor puede sentir que Codex tarda. | `settle_seconds=7` y `max_wait=22` son aceptables; permitir bypass solo para comandos internos seguros. |
| P1 | Agrupar texto DIRECT no relacionado con un PDF posterior. | El modelo podria mezclar pedidos distintos. | Key por chat/topic/route, quiet period corto, max wait y cierre despues de respuesta. |
| P1 | Regresion en route explicita REELS. | Texto con destino claro podria quedar como DIRECT por el nuevo buffer. | Mantener prioridad de explicit route antes del buffer; ya cubierto por direct reels voice/postfix. |
| P1 | Documentos descargables sin payload normalizado. | PDF podria existir en `incoming-files` pero no entrar al contexto final. | Test explicito para `document_payload_from_message` + attachment collector. |
| P1 | Doble respuesta si llega PDF despues del primer envio. | Ruido y perdida de confianza. | Reprocess interno unico, sin disculpa publica automatica. |

## ventana_direct_7s_22s

La ventana es razonable:

```yaml
direct_buffer:
  settle_seconds: 7
  max_wait_seconds: 22
  expected_tradeoff: small_latency_for_complete_context
  acceptable_for:
    - texto_DIRECT_con_posibles_adjuntos
    - PDF/documento_suelto
    - fotos_sueltas_sin_media_group
  watch:
    - comandos_que_deben_responder_inmediato
    - chats_con_mensajes_separados_no_relacionados
```

No la haria mas larga por defecto. Si el contralor sigue viendo adjuntos tardios
despues de 7 segundos pero antes de 22, el problema probablemente seria de
flush prematuro, no de duracion maxima. Si aparecen quejas de lentitud, el ajuste
seria bajar settle a `5-6s` solo para DIRECT sin palabras como "te paso",
"adjunto", "presupuesto", "archivo", "pdf" o "esto".

## fixtures_faltantes

Antes de cerrar el incidente definitivamente, agregaria o confirmaria estos
fixtures:

| Fixture | Tipo | Esperado |
| --- | --- | --- |
| `T_DIRECT_TEXT_THEN_LATE_PDF_BUFFERED` | Positivo | No model call ni final response antes del PDF; una llamada con texto + documento. |
| `T_DIRECT_TEXT_NO_MEDIA_FLUSHES_AFTER_QUIET` | Negativo | Un texto sin adjuntos responde despues del quiet period. |
| `T_DIRECT_EXPLICIT_REELS_WITH_LATE_MEDIA_ROUTES_REELS` | Regresion | Texto direct con ruta REELS y media tardia conserva `route=REELS`. |
| `T_DIRECT_COMMAND_NO_ATTACHMENT_BUFFER_BYPASS` | Negativo | Comando interno seguro no espera 7s si no corresponde. |
| `T_INCOMING_FILES_DOCUMENT_PAYLOAD_COLLECTED` | Positivo | `incoming-files` aparece como attachment document en el model call. |
| `T_LATE_PDF_AFTER_FINAL_RESPONSE_INTERNAL_REPROCESS_ONLY` | Frontera | Si ya hubo respuesta, crear reprocess interno y no doble mensaje publico. |
| `T_DIRECT_TWO_UNRELATED_MESSAGES_NOT_MERGED` | Falso positivo | Dos textos/PDFs separados por cierre de buffer crean grupos distintos. |
| `T_MEDIA_GROUP_AND_DOCUMENT_COMBINED_SORTED` | Frontera | Fotos + PDF cercanos entran ordenados y sin duplicar attachments. |

## regresion_reels_topic_routing

Riesgo bajo con la evidencia declarada. Pasaron:

- `test_postfix_regression_fixtures.py` con 13 fixtures;
- `test_direct_reels_voice_routing.py`;
- `test_delivery_receipt_gate.py`;
- status del bot antes y despues del restart.

La condicion a vigilar es que el buffer DIRECT no degrade la ruta fuerte. Orden
correcto:

```text
explicit route / topic mapping
then nearby attachment buffering
then model call after buffer close
then delivery gate with ok=true and message_id
```

Si el orden se invierte, podrian volver falsos positivos: REELS explicito
quedando como DIRECT, o DIRECT generico heredando REELS por media cercana.

## recommendation

Aceptar el patch en observacion y mantener el contralor mirando
`media_arrived_after_response` por al menos las proximas sesiones reales. No
revertir ni ampliar la ventana todavia. El siguiente trabajo util para Pablo es
una review de evidencia si el orquestador sube un paquete sanitizado con:

- snippet del gate de buffer y collector de documentos;
- salida completa de `test_media_buffer_policy.py`;
- evento sintetico DIRECT texto + PDF;
- ultimo reporte del contralor sin nuevos hallazgos.

## confidence

Media-alta para aceptar en observacion: el patch descrito coincide con el
diagnostico previo y las suites declaradas cubren las regresiones importantes.
Media para certificar el diff concreto porque no inspeccione la app real ni los
tests en `/Users/jarvis`. Alta para mantener prohibido cualquier envio externo
desde tests o desde este worker.

## attempted_routes

- Se hizo `git pull --rebase`.
- Se ejecuto `./scripts/personal_xh_check.sh` y se detecto el job asignado.
- Se reclamo el job con `python3 scripts/bridgectl.py claim`.
- Se reviso el workorder, `context/fronts/telegram.md` y resultados Telegram
  previos relevantes.
- No se abrio Telegram real, Gmail, Drive, Photos/iCloud, ObraCash ni el PDF del
  incidente.

## risks_limits

- El QA local fue tomado como declaracion del orquestador; no se ejecuto contra
  la app real desde el bridge.
- No se leyeron logs ni adjuntos reales.
- La decision final de integracion y cierre queda en Codex orquestador.

## evidence_paths

- `jobs/20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1.md`
- `claims/20260527T163550-telegram-direct-late-pdf-buffer-postpatch-review-v1.json`
- `context/fronts/telegram.md`
- `results/20260527T162339-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T111222-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md`
- `results/20260526T071000-telegram-t13-postfix-final-review-v1.result.md`

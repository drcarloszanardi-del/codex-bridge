# Resultado - 20260526T101406-artifactdraft-router-pilot-safe-plan-v1

## summary

Plan seguro para conectar `ArtifactDraft` al router operativo sin enviar nada afuera. La integracion recomendada es parcial y por feature flag: crear artefactos locales antes de respuestas largas, adjuntos, reels, presentaciones e informes, pero mantener el envio externo actual deshabilitado o inalterado hasta que pasen fixtures de regresion.

La regla central: el router puede crear `draft`, mover a `qa_ready` o `approved_local`, pero no debe declarar `delivered` sin recibo real (`message_id`, `email_sent_id`, `drive_file_id` o firma manual). Para Telegram, el piloto debe empezar antes del send real y bloquear contaminacion de topic, payload tecnico crudo y falso "enviado".

## source_counts

| Fuente permitida | Estado | Uso |
| --- | ---: | --- |
| `results/20260526T094214-artifactdraft-minimal-filesystem-implementation-v1.result.md` | Revisada | Estructura, schema, estados, recibos, helper y fixtures base. |
| `results/20260526T073800-batch-results-priority-triage-v1.result.md` | Revisada | Priorizacion de ArtifactDraft, hard fails Telegram y enfoque bajo riesgo. |
| `protocol.md` | Revisado | Sin acciones externas, sin secretos, orquestador conserva decision final. |
| `docs/telegram_topic_routing_regression_suite_v1.md` | No existe en `docs/` | Se registra ausencia; se proponen fixtures equivalentes sin asumir contenido. |

## integration_map

Como no hay ruta exacta del router en las fuentes permitidas, el orquestador debe localizar los puntos reales con busquedas locales acotadas:

```bash
rg -n "send|message_id|topic|route|router|artifact|telegram|outbox" .
rg -n "long|attachment|reels|presentaciones|radar|viaje|delivery" .
rg -n "new_artifact|validate_artifact|artifact.json" scripts tests .
```

Puntos de integracion probables:

| Punto | Momento | Accion ArtifactDraft | Estado inicial |
| --- | --- | --- | --- |
| Route classifier / topic resolver | Despues de detectar front/topic y antes de generar respuesta larga. | Decidir si `artifact_required=true`; crear artifact si aplica. | `draft` |
| Context binder / brief builder | Despues de armar brief y refs, antes del model call largo. | Escribir `brief.md`, `context_refs.md`, `source.refs`. | `draft` |
| Long Telegram response | Antes de preparar payload de envio. | Guardar draft/final candidato, correr `validate_artifact.py`; no enviar si QA falla. | `qa_ready` |
| Attachment/media path | Antes de adjuntar archivos, imagenes, audio o video. | Registrar assets en `assets/manifest.json`; marcar `needs_review` si no hay aprobacion. | `draft` o `blocked` |
| Reels CMP pipeline | Antes de render final o antes de presentar preview como entrega. | Exigir evidence/contact sheet/audio/privacy segun gate premium. | `qa_ready` |
| Presentaciones/documentos | Despues de render/QA local y antes de entregar. | Guardar final candidato y QA report; no marcar delivered. | `approved_local` |
| Radar/viajes/informes | Antes de resumen al Doctor. | Adjuntar validator del informe y bloqueo si es evidencia parcial. | `qa_ready` o `blocked` |
| Delivery/outbox | Inmediatamente antes y despues del envio real por orquestador. | Pre-send: exigir `approved_local`; post-send: registrar recibo real. | `queued_external` -> `delivered` |

## router_min_fields

Campos minimos que el router debe pasar al helper al crear un artifact:

```json
{
  "artifact_id": "YYYYMMDDTHHMMSS-front-topic-slug",
  "front": "telegram|reels_cmp|presentaciones|informes|radar|viajes",
  "job_id": "bridge job id or empty",
  "title": "short human title",
  "source_kind": "bridge_job|telegram_context|manual|local_brief",
  "source_refs": ["jobs/<job_id>.md", "context/fronts/<front>.md"],
  "route": {
    "topic": "string",
    "target_channel": "none|telegram|email|drive|manual",
    "artifact_required": true,
    "reason": "long_response|attachment|reel|presentation|report|privacy_risk"
  },
  "privacy": {
    "contains_personal_material": false,
    "contains_patient_data": false,
    "safe_for_external_review": false
  }
}
```

Campos minimos que el router debe actualizar antes de `queued_external`:

```json
{
  "status": "approved_local",
  "qa": {
    "status": "pass",
    "required_checks": ["no_internal_notes", "topic_match", "receipt_required"],
    "passed_checks": ["no_internal_notes", "topic_match", "receipt_required"],
    "failed_checks": []
  },
  "delivery": {
    "target": "telegram",
    "requires_receipt": true,
    "receipt_type": "message_id",
    "receipt_value": null
  }
}
```

## state_usage_by_router

| Estado | Quien lo puede setear | Uso en piloto |
| --- | --- | --- |
| `draft` | Router/helper | Creado despues de route/brief. |
| `qa_ready` | Router despues de generar final candidato | Hay material listo para QA local, no envio. |
| `approved_local` | Validator/QA local del orquestador | QA pasa; el orquestador puede decidir envio. |
| `queued_external` | Solo orquestador, justo antes de envio real | Hay decision de enviar, pero falta recibo. |
| `delivered` | Solo orquestador despues del envio | Requiere recibo real. |
| `blocked` | Router/validator/orquestador | Falta material, QA falla, topic dudoso, privacidad o payload tecnico. |

Reglas duras:

- `personal-xh` nunca setea recibos externos.
- `delivered` sin `receipt_value` es hard fail.
- `queued_external` con `qa.status != pass` es hard fail.
- `queued_external` con datos de paciente o material personal no aprobado es hard fail.
- Todo bypass debe registrar `artifact_required=false` y razon concreta, por ejemplo healthcheck corto.

## p0_p1_risks

### P0

| Riesgo | Motivo | Mitigacion |
| --- | --- | --- |
| Falso entregado | El sistema dice "enviado" sin `message_id`. | Post-send exige recibo real antes de `delivered`. |
| Contaminacion de topic | Respuesta larga entra a topic equivocado o mezcla contextos. | Fixture de topic match antes de `approved_local`. |
| Payload tecnico crudo | Diff/log/traceback llega al Doctor. | QA `no_raw_technical_payload`; bloquear antes de outbox. |
| Datos de paciente | Riesgo medico-legal y privacidad. | `privacy.contains_patient_data=true` bloquea `queued_external`. |
| Reels preview como final | Preview/contact sheet pobre se trata como entrega. | Gate premium: evidencia visual/audio/contact sheet antes de `approved_local`. |
| Adjuntos sin aprobacion | Se envian assets no revisados o rutas internas. | `assets/manifest.json` con `approved` obligatorio. |

### P1

| Riesgo | Motivo | Mitigacion |
| --- | --- | --- |
| Overhead en respuestas simples | Todo se vuelve lento. | Bypass permitido para healthchecks y estado corto. |
| Repo pesado | Binarios grandes en Git. | Manifestar rutas locales/derivados seguros; no versionar pesados por defecto. |
| Doble artifact | Retry crea duplicados. | `artifact_id` deterministico por job/run y check de existencia. |
| Estado trabado | QA falla y no hay handoff. | `blocked` debe incluir `next_action` y faltantes. |
| Incompatibilidad router actual | Cambio grande en flujo de envio. | Primer piloto solo crea/valida artifacts sin tocar send real. |

## required_fixtures

Fixtures minimos obligatorios antes de tocar router real:

| ID | Caso | Esperado |
| --- | --- | --- |
| `A_ROUTER_LONG_TELEGRAM_CREATES_DRAFT` | Respuesta Telegram larga o con adjunto. | Crea ArtifactDraft en `draft`; no envia nada. |
| `A_ROUTER_HEALTHCHECK_BYPASS` | Heartbeat/estado corto. | No crea artifact; registra bypass seguro si hay logging. |
| `A_ROUTER_TOPIC_MISMATCH_BLOCKS` | Route topic != target topic esperado. | `blocked`, no `queued_external`. |
| `A_ROUTER_RAW_TECH_PAYLOAD_BLOCKS` | Draft contiene diff/log/traceback. | QA fail, `blocked`. |
| `A_ROUTER_ATTACHMENT_NEEDS_APPROVAL` | Hay asset `needs_review`. | No pasa a `approved_local`. |
| `A_ROUTER_REEL_PREVIEW_NOT_FINAL` | Reel con preview/contact sheet insuficiente. | `blocked` o `qa_ready`, nunca `approved_local`. |
| `A_ROUTER_APPROVED_LOCAL_NO_DELIVERED` | QA pass y final candidate existe. | `approved_local`, `receipt_value=null`, no `delivered`. |
| `A_ROUTER_QUEUED_WITHOUT_MESSAGE_ID` | Se intenta marcar enviado sin `message_id`. | Hard fail; no `delivered`. |
| `A_ROUTER_MESSAGE_ID_DELIVERED` | Orquestador registra `message_id` y `chat_id`. | `delivered` permitido. |
| `A_ROUTER_PATIENT_DATA_EXTERNAL_BLOCK` | `contains_patient_data=true` + target externo. | Hard fail. |

Regresiones de compatibilidad:

- Rutas existentes de Telegram corto siguen funcionando.
- Jobs bridge sin entrega externa pueden adjuntar `artifact_id` sin cambiar resultado.
- Reels/presentaciones pueden crear artifact aunque el render final quede fuera del repo.
- Radar bloqueado puede quedar como artifact `blocked` sin generar mensaje externo.

## acceptance_criteria

El piloto se acepta si:

1. Los helpers `new_artifact.py` y `validate_artifact.py` pasan tests existentes.
2. El router crea artifact solo para respuestas largas, adjuntos, reels, presentaciones e informes configurados.
3. Ningun test puede pasar de `draft`/`qa_ready` a `delivered` sin recibo real.
4. `queued_external` requiere `approved_local` previo o QA pass equivalente.
5. Los fixtures de topic mismatch, payload tecnico, asset `needs_review` y paciente bloquean envio.
6. El flujo de healthcheck/heartbeat corto no se ralentiza ni exige artifact.
7. El resultado del bridge puede incluir `artifact_id` y path local sin exponer material sensible.
8. El piloto se puede desactivar con feature flag sin migracion.

## bounded_patch_plan

### Paso 1 - feature flag

Agregar config local:

```text
ARTIFACTDRAFT_ROUTER_PILOT=0|1
ARTIFACTDRAFT_DRY_RUN=1
```

Default recomendado: `ROUTER_PILOT=1` solo en entorno local del orquestador y `DRY_RUN=1` para no enviar nada durante fixtures.

### Paso 2 - adapter pequeno

Crear funcion adapter, no acoplar el router completo al schema:

```python
def maybe_create_artifact(route, brief, job_id=None):
    if not route.artifact_required:
        return None
    return new_artifact(front=route.front, artifact_id=make_id(route, job_id), job_id=job_id, title=route.title)
```

### Paso 3 - pre-send gate

Antes del outbox/send:

```python
if artifact_id:
    validation = validate_artifact(artifact_path)
    if not validation["ok"]:
        mark_blocked(artifact_id, validation)
        return internal_blocked_result(validation)
```

### Paso 4 - post-send receipt

Solo en el orquestador y solo si el envio real ocurre:

```python
if send_result.ok and send_result.message_id:
    update_receipt(artifact_id, receipt_type="message_id", receipt_value=send_result.message_id)
    transition(artifact_id, "delivered")
else:
    transition(artifact_id, "blocked")
```

### Paso 5 - tests primero

Implementar fixtures y tests antes de activar flujo real. Si alguna ruta exacta falta, localizarla con `rg` y tocar solo el modulo que arma payload o llama al sender.

## exact_route_discovery_without_assuming

Si el router real no esta claro, buscar en este orden:

1. Donde se decide topic/front:
   ```bash
   rg -n "topic|front|route|router|classif" .
   ```
2. Donde se arma el payload de Telegram:
   ```bash
   rg -n "sendMessage|message_id|chat_id|outbox|telegram" .
   ```
3. Donde se manejan adjuntos:
   ```bash
   rg -n "attachment|media|photo|video|document|asset" .
   ```
4. Donde se generan reels/presentaciones/informes:
   ```bash
   rg -n "reels_cmp|presentaciones|pptx|render|radar|viaje" .
   ```
5. Donde ya se llamaron los helpers:
   ```bash
   rg -n "new_artifact|validate_artifact|artifact_id|artifact.json" .
   ```

No asumir que el nombre del archivo es `router.py`; confirmar por llamadas a sender/outbox y por tests existentes.

## recommendation

Aplicar ahora, pero parcial: activar el piloto en modo local/dry-run para crear y validar artifacts antes de envios, sin cambiar el envio real hasta que pasen los fixtures P0. El primer hook productivo debe ser pre-send de Telegram largo/con adjuntos y el segundo Reels/Presentaciones, porque ahi el costo de una entrega falsa o un preview confundido como final es mas alto.

No recomiendo activar `delivered` automatico todavia. Esa transicion debe quedar en post-send del orquestador y solo con recibo real.

## attempted_routes

- Se revisaron solo fuentes permitidas.
- Se verifico que `docs/telegram_topic_routing_regression_suite_v1.md` no existe en `docs/`; por eso se propusieron fixtures equivalentes sin citar contenido inexistente.
- No se abrio Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas.
- No se hicieron acciones externas ni se tocaron credenciales.

## risks_limits

- El plan usa rutas probables porque el job no autorizo inspeccion del router real.
- Los comandos `rg` propuestos deben ejecutarse localmente por el orquestador en el repo donde vive el router.
- El piloto no prueba entrega externa; solo evita que el sistema confunda estados internos con entrega real.
- La calibracion de "respuesta larga" debe fijarla el orquestador, por ejemplo longitud, adjuntos o front.
- Si el router actual no tiene objeto de route/brief, conviene crear un adapter minimo antes de introducir ArtifactDraft.

## confidence

Alta para reglas P0, estados, recibos y fixtures porque derivan de resultados locales recientes y `protocol.md`. Media para nombres de archivos/rutas exactas hasta inspeccionar el repo real del router.

## evidence_paths

- `jobs/20260526T101406-artifactdraft-router-pilot-safe-plan-v1.md`
- `results/20260526T094214-artifactdraft-minimal-filesystem-implementation-v1.result.md`
- `results/20260526T073800-batch-results-priority-triage-v1.result.md`
- `protocol.md`
- `docs/telegram_topic_routing_regression_suite_v1.md` (ausente; no se uso contenido)

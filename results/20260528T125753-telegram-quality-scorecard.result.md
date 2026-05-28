---
job_id: 20260528T125753-telegram-quality-scorecard
worker: personal-xh
status: completed
completed_at: 2026-05-28T12:59:48-03:00
front: CODEX-OPS
no_external_actions: true
no_secrets: true
---

# Resultado - Telegram quality scorecard

## summary honesto

El scorecard barato 5.3 debe funcionar como contralor post-respuesta, no como otro generador de texto. Evalua si la respuesta respeto frente, contexto, evidencia, tono formal y accion concreta. Debe producir un JSON corto, barato y accionable: `pass`, `needs_review` o `fail`, con razones codificadas y disparador de postmortem solo cuando hay riesgo real.

## coverage_table

| Requisito | Estado | Evidencia |
|---|---|---|
| `scorecard` | cubierto | Frente Telegram y bugs previos de media tardia/gate tecnico. |
| `thresholds` | cubierto | Ponderacion 0-100 con hard fails. |
| `postmortem_trigger` | cubierto | Reglas para abrir investigacion solo ante regresion/riesgo. |
| `examples` | cubierto | Casos sinteticos derivados de fallas locales documentadas. |
| `implementation_plan` | cubierto | Hook post-respuesta y fixtures locales. |

## evidencia

- `context/fronts/telegram.md` exige contexto global en canal principal, topics por frente, `ok=true` y `message_id` real para entrega confirmada.
- `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md` muestra riesgo de responder antes de recibir todos los adjuntos.
- `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md` muestra riesgo de enviar o procesar payload tecnico/diff largo de forma inadecuada.
- El frente ya tiene Brief operativo, ContextBinder, ResetScope y deuda de ResultContract/ArtifactDraft.

## inferencia

- 5.3 alcanza porque el scorecard no decide estrategia; solo puntua reglas observables y deja casos dudosos en `needs_review`.
- El scorecard debe leer artefactos locales del run, no Telegram real.
- El criterio mas importante es seguridad de entrega/contexto, no elegancia del texto.

## opinion

La mejor metrica no es si la respuesta "suena bien"; es si no hizo dano operativo: no contesto sin adjuntos, no mezclo frentes, no filtro diff, no prometio acciones externas y dejo una proxima accion clara.

## scorecard

Salida JSON sugerida:

```json
{
  "score": 0,
  "status": "pass|needs_review|fail",
  "route": "",
  "message_id": "",
  "checks": {
    "front_match": {"points": 0, "max": 20, "reason": ""},
    "context_used": {"points": 0, "max": 15, "reason": ""},
    "evidence_or_limits": {"points": 0, "max": 15, "reason": ""},
    "tone_formal": {"points": 0, "max": 10, "reason": ""},
    "action_concrete": {"points": 0, "max": 15, "reason": ""},
    "delivery_integrity": {"points": 0, "max": 15, "reason": ""},
    "safety_privacy": {"points": 0, "max": 10, "reason": ""}
  },
  "hard_fails": [],
  "recommended_action": "none|review|postmortem|block_send_next_time",
  "evidence_paths": []
}
```

Rubrica:

| Check | Max | Pregunta |
|---|---:|---|
| `front_match` | 20 | La respuesta uso el frente/ruta correcto y no mezclo temas. |
| `context_used` | 15 | Uso Brief operativo, ContextBinder o contexto canonico aplicable. |
| `evidence_or_limits` | 15 | Cito evidencia local o declaro limite exacto sin inventar. |
| `tone_formal` | 10 | Tono claro, formal y adecuado al Doctor/canal. |
| `action_concrete` | 15 | Dejo proxima accion, decision o estado verificable. |
| `delivery_integrity` | 15 | No respondio antes de adjuntos; entrega confirmada con `ok=true/message_id` si aplica. |
| `safety_privacy` | 10 | No expuso secretos, datos sensibles, diffs crudos ni acciones externas no autorizadas. |

## thresholds

| Score/condicion | Estado | Accion |
|---|---|---|
| 85-100 sin hard fail | `pass` | Registrar score. |
| 70-84 sin hard fail | `needs_review` | Revisar si es frente sensible o respuesta importante. |
| 50-69 | `needs_review` | Crear item de QA local con razones. |
| <50 | `fail` | Postmortem si hubo respuesta enviada. |
| Cualquier hard fail | `fail` | Abrir postmortem o bloquear siguiente envio similar. |

Hard fails:

- `media_arrived_after_response`: hubo adjuntos cercanos posteriores no incluidos.
- `wrong_front`: respuesta de un frente enviada a otro.
- `raw_technical_diff_sent`: diff/log tecnico crudo enviado al canal.
- `external_action_claimed_without_confirmation`: promete envio/compra/contacto sin `ok/message_id` o permiso.
- `sensitive_data_exposed`: datos sensibles/secretos en respuesta.
- `no_message_id_for_claimed_delivery`: afirma entrega sin confirmacion real.

## postmortem_trigger

Abrir postmortem si:

- `status=fail` y la respuesta fue enviada al usuario.
- Hay hard fail de privacidad, frente incorrecto, media tardia o diff tecnico.
- Dos `needs_review` del mismo tipo aparecen en 24 horas.
- Score cae mas de 20 puntos contra el promedio de la misma ruta.
- El Doctor corrige que faltaba contexto o adjunto.

No abrir postmortem si:

- La respuesta quedo bloqueada antes de envio.
- El problema es solo estilo menor con score >= 85.
- El run era prueba sintetica marcada como fixture.

Formato de postmortem:

```text
postmortem_id:
route:
message_ids:
scorecard_path:
hard_fails:
root_cause_candidate:
minimal_fixture_needed:
owner_next_action:
```

## examples

Caso bueno:

```json
{
  "score": 93,
  "status": "pass",
  "hard_fails": [],
  "recommended_action": "none"
}
```

Razon: ruta correcta, contexto canonico usado, limite declarado, accion concreta y entrega confirmada.

Caso media tardia:

```json
{
  "score": 48,
  "status": "fail",
  "hard_fails": ["media_arrived_after_response"],
  "recommended_action": "postmortem"
}
```

Razon: el modelo respondio sin todos los videos/adjuntos del mismo cluster temporal.

Caso diff tecnico largo:

```json
{
  "score": 55,
  "status": "fail",
  "hard_fails": ["raw_technical_diff_sent"],
  "recommended_action": "block_send_next_time"
}
```

Razon: el canal recibio contenido tecnico que debia resumirse y guardarse localmente.

Caso tono/accion floja:

```json
{
  "score": 76,
  "status": "needs_review",
  "hard_fails": [],
  "recommended_action": "review"
}
```

Razon: no hay riesgo grave, pero falta proxima accion concreta.

## implementation_plan

1. Guardar por run un paquete local: `brief.json`, `context_refs.json`, `response.txt`, `delivery.json`, `attachments_manifest.json`.
2. Crear `scripts/telegram/score_response.py --run-dir <path>` que emita JSON y no toque Telegram.
3. Usar 5.3 o evaluator barato con prompt cerrado: devolver solo JSON valido y razones cortas.
4. Agregar fixtures sinteticos para media tardia, diff tecnico, frente incorrecto, entrega sin `message_id` y respuesta buena.
5. Registrar score en `router/runs/<run_id>/scorecard.json`.
6. Si `fail` o hard fail enviado, crear `router/postmortems/<id>.md` o job local para el orquestador.
7. Dashboard simple: listar ultimos scores por ruta y tipo de fail.

Prompt evaluador sugerido:

```text
Evalua una respuesta Telegram ya generada. No reescribas la respuesta.
Devuelve solo JSON segun schema. Penaliza promesas de envio sin ok/message_id,
frente incorrecto, falta de adjuntos, diffs tecnicos crudos, datos sensibles,
falta de evidencia/limite y ausencia de accion concreta.
```

## risks / limits

- Un evaluador barato puede pasar por alto matices clinicos o legales; hard fails deben ser reglas deterministicas cuando sea posible.
- Si el scorecard se ejecuta antes de cerrar el cluster de adjuntos, puede repetir el bug original; debe correr despues del delivery attempt o final block.
- El score no reemplaza tests de router ni secret scan.
- Ruta alternativa: si no hay evaluador 5.3 disponible, empezar con checks deterministas y ejemplos manuales.
- Limite exacto: este job no implementa el script, entrega especificacion y fixtures esperados.

## recommendation

Implementar primero `score_response.py` con checks deterministas para hard fails y un JSON de score manual/evaluator. El primer fixture obligatorio debe ser `media_arrived_after_response`, porque ya produjo una falla real y es facil de detectar por `message_ids`, timestamps y attachments manifest.

## confidence

Alta para checks y thresholds porque derivan de fallas locales concretas. Media para calibracion de puntaje, que debe ajustarse con runs reales o fixtures historicos.

## evidence_paths

- `jobs/20260528T125753-telegram-quality-scorecard.md`
- `context/fronts/telegram.md`
- `results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md`
- `results/20260525T111227-telegram-contralor-action-event-handle-error.result.md`

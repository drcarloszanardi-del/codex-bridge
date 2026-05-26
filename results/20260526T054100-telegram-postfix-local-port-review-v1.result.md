# Resultado - 20260526T054100-telegram-postfix-local-port-review-v1

## summary

Revision XH post-port local de fixtures Telegram. No use Telegram real, no inspeccione archivos de la Mac de trabajo y no abri secretos. Tome las verificaciones locales como evidencia declarada por el orquestador.

Juicio corto: para esta ronda, el ruteo directo/topic puede considerarse estabilizado en nivel operativo. Estan cubiertos los bugs P0 que motivaron el ciclo: contaminacion por hints debiles, adjuntos sin caption, topic desconocido, drenaje benigno de media group, delivery falso y payload tecnico crudo.

## coverage_table

| fuente permitida | evidencia usada | limite |
| --- | --- | --- |
| Workorder `20260526T054100` | Declara port local, 12 fixtures OK, suites previas OK, listener reiniciado, healthcheck OK, contralor sin hallazgos y outbox 0. | No equivale a inspeccion directa del patch ni a prueba real de Telegram desde este worker. |
| `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md` | Define T_POSTFIX_001 a T_POSTFIX_012 y gates de route_strength, media, contralor, delivery y payload. | Suite portable; los helpers reales viven en la Mac de trabajo. |
| `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md` | Identifica riesgos del fix y criterios direct/topic. | Auditoria conceptual basada en fuentes permitidas. |
| `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md` | Recalca P0: no mezclar frente, no responder antes de media, no decir enviado sin message_id. | No revalida el port local. |
| `results/20260525T124108-telegram-quality-scorecard.result.md` | Hard fails: media incompleta, diff crudo, delivery sin message_id, pedidos indebidos. | Scorecard complementa, no reemplaza tests deterministas. |
| `protocol.md` | Decision final e integracion quedan en el orquestador. | Pablo solo recomienda. |

## stabilization_judgement

**Evidencia declarada por el orquestador:** compila `codex_telegram_direct.py`, `codex_telegram_channel_contralor.py` y el runner; pasan `12/12` fixtures post-fix; pasan suites direct voice routing, media buffer, delivery receipt y technical payload; listener reiniciado; healthcheck final OK; contralor final sin hallazgos; outbox pendiente 0.

**Inferencia:** eso alcanza para considerar cerrada esta ronda de estabilizacion de ruteo directo/topic. No prueba cada combinacion futura, pero si cubre el conjunto minimo que venia causando contaminacion operativa.

**Criterio:** no abriria otro ciclo ahora salvo que aparezca evidencia nueva en logs reales o correccion directa del Doctor. Seguir iterando sin incidente nuevo puede endurecer de mas el router y aumentar falsos `DIRECT/UNKNOWN_REVIEW`.

## covered_failure_modes

- Direct weak hints quedan en `DIRECT` y no mutan `active_route`.
- Direct explicit front o explicit deliverable routea al frente correcto.
- Mensajes tipo "voz del paciente" no disparan `REELS` por palabra aislada.
- Adjuntos sin caption no heredan rutas vencidas ni threads falsos.
- Adjuntos sin caption si pueden heredar contexto reciente con thread real y expectativa de media.
- `media_group_handled` sano es benigno solo con trazabilidad.
- `media_group_handled` sin trazabilidad queda visible como warning/error.
- Direct CODEX-OPS conserva respuesta por main channel aunque `GENERAL` no tenga thread heredado.
- Outbox sin `message_id` no se considera enviado.
- Diff/trace crudo se bloquea antes de Telegram.
- Topic desconocido no hereda contexto global.
- Suites previas de media buffer, voice routing, delivery y payload tecnico siguen pasando.

## remaining_p0_risk

Riesgo P0 residual principal: **carrera temporal real entre texto directo, album sin `media_group_id` y correccion posterior de destino**.

Ejemplo: el Doctor escribe en directo "armalo con esto", sube 3 fotos sueltas sin `media_group_id`, y 15 segundos despues agrega "era para REELS / el reel de cavernoma". Los fixtures actuales cubren album con `media_group_id`, route reciente, stale route, explicit deliverable y topic desconocido, pero no fuerzan una decision ante correccion tardia que llega dentro de `max_wait` o apenas despues del quiet period.

Impacto si falla: podria crear un job `DIRECT/UNKNOWN_REVIEW` incompleto o, peor, responder antes de incorporar la correccion de destino. No hay evidencia de que este bug exista; es el borde P0 mas plausible que queda sin fixture explicita.

## one_next_fixture_if_needed

Agregar solo si se quiere endurecer una vuelta mas:

```json
{
  "id": "T_POSTFIX_013_DIRECT_CAPTIONLESS_MEDIA_LATE_ROUTE_CORRECTION",
  "kind": "telegram_event_cluster",
  "description": "Direct text plus loose captionless media plus late route correction should create one REELS job, not premature DIRECT.",
  "input": {
    "chat_type": "direct",
    "topic_id": null,
    "events": [
      {"t_ms": 0, "type": "text", "text": "Armalo con esto."},
      {"t_ms": 2500, "type": "photo", "file_id": "photo_1", "caption": null, "media_group_id": null},
      {"t_ms": 5600, "type": "photo", "file_id": "photo_2", "caption": null, "media_group_id": null},
      {"t_ms": 9200, "type": "photo", "file_id": "photo_3", "caption": null, "media_group_id": null},
      {"t_ms": 15000, "type": "text", "text": "Era para REELS, el reel de cavernoma."}
    ]
  },
  "expected": {
    "front": "REELS",
    "route_strength_in": ["explicit_front", "explicit_front_deliverable", "recent_media_context"],
    "jobs_created": 1,
    "attachments_count": 3,
    "model_call_before_media_closed": false,
    "premature_direct_job_created": false,
    "send_policy": "suppress_until_result"
  }
}
```

Este test es valioso porque mezcla los tres bordes complicados: media sin album id, texto ambiguo inicial y correccion de frente tardia.

## recommendation

Dejar esta rama quieta por ahora y pasar a observacion. No abriria un nuevo ciclo salvo que el orquestador quiera sumar `T_POSTFIX_013` como cierre fino o aparezca un incidente real.

Accion sugerida: registrar el estado como estabilizado, conservar los tests en smoke post-patch y revisar logs/contralor despues de actividad real del Doctor. Si el proximo incidente toca media suelta + correccion tardia, entonces agregar `T_POSTFIX_013` y reabrir ciclo.

## risks_limits

- No vi el patch local ni los archivos de tests portados; use evidencia declarada por el orquestador.
- No use Telegram real ni valide el listener desde esta Mac.
- La estabilizacion aplica a esta ronda de contaminacion directo/topic, no a toda la plataforma Telegram.
- El riesgo residual es inferido, no observado.

## confidence

Media-alta. Alta para concluir que los modos de falla conocidos estan cubiertos segun verificaciones declaradas; media para declarar estabilidad global porque falta observacion de trafico real post-reinicio.

## evidence_paths

- `jobs/20260526T054100-telegram-postfix-local-port-review-v1.md`
- `results/20260526T050800-telegram-postfix-regression-fixtures-v1.result.md`
- `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md`
- `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md`
- `results/20260525T124108-telegram-quality-scorecard.result.md`
- `protocol.md`

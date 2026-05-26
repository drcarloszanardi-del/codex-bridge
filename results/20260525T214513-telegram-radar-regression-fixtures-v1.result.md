---
id: 20260525T214513-telegram-radar-regression-fixtures-v1
job_id: 20260525T214513-telegram-radar-regression-fixtures-v1
created_at: 2026-05-25T21:51:04-03:00
created_by: personal-xh
worker: personal-xh
status: completed
no_external_actions: true
no_secrets: true
---

# Resultado - paquete de regresion Telegram + radares anti informe vacio

Job: `20260525T214513-telegram-radar-regression-fixtures-v1`
Worker: `personal-xh` / Pablo
Fecha: `2026-05-25`

## summary

Paquete portable de fixtures y asserts para que el orquestador lo lleve al repo real sin reinterpretar la auditoria. No inspeccione el patch real de la Mac de trabajo; esto convierte la logica verificada por resumen en casos de regresion concretos.

Objetivo P0: si vuelve a mezclarse voz/reel con canal incorrecto, si se responde antes de cerrar media, si un radar tecnico vacio intenta enviarse, o si se declara enviado sin `message_id`, estos tests deben fallar.

## coverage_table

| Gate P0 | Fixtures que lo cubren |
|---|---|
| Voz/reel directo routea a `REELS` con ancla suficiente | `direct_reels_voice_argentina_graves_lata_robot.json` |
| Voz clinica no se sobrerutea a `REELS` | `direct_voice_non_reels_clinica_negative.json` |
| Texto + media tardia espera cierre de buffer | `reels_text_plus_four_photos_late_album.json` |
| Outbox no equivale a enviado | `outbox_without_message_id.json`, `telegram_ok_with_message_id.json` |
| Diffs/logs crudos bloqueados | `raw_diff_payload_blocked.json` |
| Radar tecnico vacio no envia | `inmobiliaria_all_technical_failures.json`, `inversiones_queries_zero_technical_errors.json` |
| Radar real no se bloquea | `inmobiliaria_real_opportunities_junin.json` |
| Contrato incompleto no envia | `radar_one_weak_candidate_missing_comparables.json`, `radar_source_blocked_without_fallback.json` |
| Cero candidatos con universo documentado queda review | `radar_zero_candidates_with_documented_universe.json` |

## fixture_tree

```text
fixtures/
  telegram/
    direct_reels_voice_argentina_graves_lata_robot.json
    direct_voice_non_reels_clinica_negative.json
    reels_text_plus_four_photos_late_album.json
    outbox_without_message_id.json
    telegram_ok_with_message_id.json
    raw_diff_payload_blocked.json
  radares/
    inmobiliaria_all_technical_failures.json
    inversiones_queries_zero_technical_errors.json
    inmobiliaria_real_opportunities_junin.json
    radar_one_weak_candidate_missing_comparables.json
    radar_zero_candidates_with_documented_universe.json
    radar_source_blocked_without_fallback.json
```

## fixtures_json

`fixtures/telegram/direct_reels_voice_argentina_graves_lata_robot.json`

```json
{
  "id": "T_REELS_VOICE_DIRECT_POSITIVE",
  "kind": "telegram_event",
  "input": {
    "chat_type": "direct",
    "topic_id": null,
    "text": "Edicion de voz argentina para el reel CMP, mas grave, que no suene a lata de robot.",
    "attachments": []
  },
  "expected": {
    "front": "REELS",
    "reply_target": {"chat_id_ref": "REELS_CHAT_ID", "thread_id": 6},
    "reason": "direct_deliverable_topic",
    "job_policy": "create_job",
    "send_policy": "suppress_until_result"
  }
}
```

`fixtures/telegram/direct_voice_non_reels_clinica_negative.json`

```json
{
  "id": "T_VOICE_CLINICA_NEGATIVE",
  "kind": "telegram_event",
  "input": {
    "chat_type": "direct",
    "topic_id": null,
    "text": "La voz del paciente esta mas grave y refiere dolor cervical.",
    "attachments": []
  },
  "expected": {
    "front_in": ["CLINICA", "UNKNOWN_REVIEW"],
    "front_not": "REELS",
    "reason_not": "direct_deliverable_topic",
    "job_policy_in": ["create_job", "unknown_review"]
  }
}
```

`fixtures/telegram/reels_text_plus_four_photos_late_album.json`

```json
{
  "id": "T_REELS_LATE_MEDIA_BUFFER",
  "kind": "telegram_event_cluster",
  "input": {
    "chat_type": "topic",
    "topic_id_ref": "REELS_THREAD_ID",
    "events": [
      {"t_ms": 0, "type": "text", "text": "Arme el reel con estas fotos."},
      {"t_ms": 1500, "type": "photo", "file_id": "photo_1", "media_group_id": "grp_a"},
      {"t_ms": 3200, "type": "photo", "file_id": "photo_2", "media_group_id": "grp_a"},
      {"t_ms": 6100, "type": "photo", "file_id": "photo_3", "media_group_id": "grp_a"},
      {"t_ms": 9800, "type": "photo", "file_id": "photo_4", "media_group_id": "grp_a"}
    ]
  },
  "expected": {
    "front": "REELS",
    "jobs_created": 1,
    "model_call_before_media_closed": false,
    "media_state_after_quiet_period": "closed",
    "attachments_count": 4,
    "send_policy": "suppress_until_result"
  }
}
```

`fixtures/telegram/outbox_without_message_id.json`

```json
{
  "id": "T_DELIVERY_OUTBOX_NOT_SENT",
  "kind": "delivery_result",
  "input": {
    "outbox_status": "queued",
    "telegram_response": null
  },
  "expected": {
    "sent_confirmed": false,
    "may_say_sent": false,
    "required_reason": "missing_message_id"
  }
}
```

`fixtures/telegram/telegram_ok_with_message_id.json`

```json
{
  "id": "T_DELIVERY_CONFIRMED",
  "kind": "delivery_result",
  "input": {
    "telegram_response": {"ok": true, "result": {"message_id": 123, "chat": {"id_ref": "TARGET_CHAT"}}}
  },
  "expected": {
    "sent_confirmed": true,
    "may_say_sent": true,
    "message_id": 123
  }
}
```

`fixtures/telegram/raw_diff_payload_blocked.json`

```json
{
  "id": "T_TECHNICAL_PAYLOAD_BLOCKED",
  "kind": "telegram_response_candidate",
  "input": {
    "route": "CODEX-OPS",
    "text": "diff --git a/script.py b/script.py\n@@ -1,2 +1,2 @@\n- old\n+ new\nTraceback: sample internal error"
  },
  "expected": {
    "send_policy": "block",
    "artifact_local_required": true,
    "hard_fail": "raw_technical_payload_to_telegram"
  }
}
```

`fixtures/radares/inmobiliaria_all_technical_failures.json`

```json
{
  "id": "R_INM_ALL_TECHNICAL_FAILURES",
  "kind": "radar_report_input",
  "front": "inmobiliaria",
  "input": {
    "queries_checked": 4,
    "items": [
      {"source": "portal_a", "outcome": "technical_error"},
      {"source": "portal_b", "outcome": "technical_error"},
      {"source": "portal_c", "outcome": "technical_error"}
    ],
    "opportunities_in_radius": 0,
    "candidates": []
  },
  "expected": {
    "sent": false,
    "status": "blocked",
    "reason": "blocked_empty_technical_failure_report"
  }
}
```

`fixtures/radares/inversiones_queries_zero_technical_errors.json`

```json
{
  "id": "R_INV_ZERO_QUERIES_TECH_ERRORS",
  "kind": "radar_report_input",
  "front": "inversiones_instrumental",
  "input": {
    "queries_checked": 0,
    "technical_errors": ["search_failed", "source_unavailable"],
    "candidates": []
  },
  "expected": {
    "sent": false,
    "status": "blocked",
    "reason": "blocked_empty_technical_failure_report",
    "rule": "anti_informe_vacio"
  }
}
```

`fixtures/radares/inmobiliaria_real_opportunities_junin.json`

```json
{
  "id": "R_INM_REAL_OPPORTUNITIES_JUNIN",
  "kind": "radar_report_input",
  "front": "inmobiliaria",
  "input": {
    "scope": "Junin, Plaza 9 de Julio + 12 cuadras",
    "queries_checked": 9,
    "candidates_total": 127,
    "opportunities_in_radius": 12,
    "candidates": [
      {"id": "inm_001", "title": "Casa a refaccionar zona centro", "price": "ARS visible", "decision": "investigar", "next_action": "validar precio y estado"},
      {"id": "inm_002", "title": "Casa lote propio radio objetivo", "price": "ARS visible", "decision": "watchlist", "next_action": "comparar superficie"}
    ]
  },
  "expected": {
    "blocked": false,
    "sent_or_report_ready": true,
    "min_opportunities_in_radius": 1
  }
}
```

`fixtures/radares/radar_one_weak_candidate_missing_comparables.json`

```json
{
  "id": "R_WEAK_CANDIDATE_MISSING_CONTRACT",
  "kind": "radar_report_input",
  "front": "inmobiliaria",
  "input": {
    "sources_attempted": [{"name": "portal_a", "outcome": "success"}],
    "candidates": [{"id": "weak_001", "title": "Casa sin precio", "source": "portal_a", "price": null, "comparables": [], "next_action": null}]
  },
  "expected": {
    "sent": false,
    "status": "needs_review",
    "errors_include": ["insufficient_sources", "candidate_missing_price_without_route", "missing_comparables", "candidate_missing_next_action"]
  }
}
```

`fixtures/radares/radar_zero_candidates_with_documented_universe.json`

```json
{
  "id": "R_ZERO_CANDIDATES_DOCUMENTED_UNIVERSE",
  "kind": "radar_report_input",
  "front": "inmobiliaria",
  "input": {
    "sources_attempted_count": 7,
    "rejected_candidates_count": 8,
    "fallback_routes_used_count": 3,
    "comparables_count": 5,
    "candidates": [],
    "next_action": "ampliar radio o esperar nueva publicacion segun autorizacion"
  },
  "expected": {
    "sent": false,
    "status": "needs_review",
    "reason": "no_candidates_but_universe_documented"
  }
}
```

`fixtures/radares/radar_source_blocked_without_fallback.json`

```json
{
  "id": "R_SOURCE_BLOCKED_WITHOUT_FALLBACK",
  "kind": "radar_report_input",
  "front": "instrumental",
  "input": {
    "sources_attempted": [{"name": "source_main", "outcome": "blocked"}],
    "fallback_routes_used": [],
    "candidates": []
  },
  "expected": {
    "sent": false,
    "status": "blocked",
    "errors_include": ["blocked_source_without_two_fallbacks", "empty_universe"]
  }
}
```

## telegram_asserts

Pseudo-asserts portables:

```python
assert decision["front"] == fixture["expected"].get("front", decision["front"])
assert decision.get("front") != fixture["expected"].get("front_not")
assert decision["reply_target"].get("thread_id") == fixture["expected"].get("reply_target", {}).get("thread_id", decision["reply_target"].get("thread_id"))
assert decision["send_policy"] in {"suppress_until_result", "allow", "block", "needs_approval"}
assert not (delivery_label == "sent" and not delivery.get("message_id"))
assert not (response_contains_diff_or_trace(response_text) and send_policy != "block")
```

Hard fails:

- `front=REELS` con `reply_target=main_channel` sin override explicito.
- `media_state=buffering` y ya hubo model call final.
- `delivery_label=sent` sin `telegram_response.ok=true` y `message_id`.
- Texto con diff/trace/path tecnico enviado a Telegram.

## radar_asserts

Pseudo-asserts portables:

```javascript
assert(!(report.sent === true && report.status === "blocked"));
assert(!(allTechnicalFailures(report) && report.sent === true));
assert(!(report.queries_checked === 0 && report.technical_errors?.length && report.sent === true));
assert(!(hasBlockedSource(report) && fallbackCount(report) < 2 && report.status === "completed"));
assert(!(candidateMissingContract(report) && report.sent === true));
assert(!(report.candidates.length === 0 && undocumentedUniverse(report) && report.status === "completed"));
```

Estados esperados:

| Caso | Estado maximo |
|---|---|
| Todo falla tecnicamente | `blocked` |
| Fuente bloqueada sin alternativas | `blocked` |
| Candidato unico incompleto | `needs_review` |
| Cero candidatos con universo documentado | `needs_review` |
| Oportunidades reales con contrato minimo | `completed` o `report_ready` |

## negative_cases

- `voz` en contexto clinico no debe activar `REELS` sin ancla de reel/video/edicion/CMP.
- Una respuesta "procesando" puede existir solo como ACK breve permitido; no debe ser respuesta final ni decir que el material fue usado si el album sigue abierto.
- `sent:false` en radar no debe desaparecer: debe dejar artifact local con razon y proxima accion.
- Un radar con un candidato flojo no debe pasar solo por tener `candidate_count > 0`.
- `ok:true` de healthcheck del bot no equivale a envio de una respuesta concreta.

## commands_to_port

```bash
python3 -m py_compile scripts/codex_telegram_direct.py
node --check scripts/inmobiliaria/send_inm_radar_report.js
node --check scripts/inversiones/send_inv_neuro_instrument_report.js
python3 tests/telegram/test_direct_reels_voice_routing.py fixtures/telegram/direct_reels_voice_argentina_graves_lata_robot.json
python3 tests/telegram/test_direct_reels_voice_routing.py fixtures/telegram/direct_voice_non_reels_clinica_negative.json
python3 tests/telegram/test_media_buffer_policy.py fixtures/telegram/reels_text_plus_four_photos_late_album.json
python3 tests/telegram/test_delivery_receipt_gate.py fixtures/telegram/outbox_without_message_id.json fixtures/telegram/telegram_ok_with_message_id.json
python3 tests/telegram/test_technical_payload_gate.py fixtures/telegram/raw_diff_payload_blocked.json
node tests/radares/test_empty_technical_failure_gate.js fixtures/radares/inmobiliaria_all_technical_failures.json fixtures/radares/inversiones_queries_zero_technical_errors.json
node tests/radares/test_radar_report_contract.js fixtures/radares/radar_one_weak_candidate_missing_comparables.json fixtures/radares/radar_zero_candidates_with_documented_universe.json fixtures/radares/radar_source_blocked_without_fallback.json
node tests/radares/test_real_candidate_not_blocked.js fixtures/radares/inmobiliaria_real_opportunities_junin.json
```

## acceptance_gate

Release bloqueado si falla cualquiera:

1. `direct_reels_voice_argentina_graves_lata_robot` no routea a `REELS`.
2. `direct_voice_non_reels_clinica_negative` routea a `REELS`.
3. `reels_text_plus_four_photos_late_album` crea mas de un job o llama modelo antes de cerrar media.
4. `outbox_without_message_id` permite decir enviado.
5. `raw_diff_payload_blocked` permite salida a Telegram.
6. Cualquier fixture radar tecnico vacio tiene `sent:true`.
7. `inmobiliaria_real_opportunities_junin` queda bloqueado.

## implementation_order

1. Portar fixtures JSON a `fixtures/telegram/` y `fixtures/radares/`.
2. Crear helpers puros: `route_event(fixture)`, `cluster_media(events)`, `confirm_delivery(response)`, `validate_radar(report)`.
3. Implementar primero asserts P0 sin Telegram real ni red.
4. Agregar estos tests al comando de smoke post-patch del orquestador.
5. Solo despues sumar scorecards finos y dashboard.

## risks_limits

- Los nombres de funciones son stubs portables; el orquestador debe mapearlos al repo real.
- Los fixtures no contienen credenciales ni IDs reales; `chat_id_ref` y `topic_id_ref` son referencias simbolicas.
- No se ejecuto Telegram real, Gmail, Drive, Calendar, Chrome ni repos fuera del bridge.
- No se afirma inspeccion del patch real; esto deriva de resultados previos y del resumen del workorder.

## recommendation

Portar este paquete como tests deterministas antes de agregar mas heuristica. La primera meta es que seis fixtures Telegram y seis fixtures Radar corran en menos de 5 segundos y bloqueen release si violan los cuatro gates P0.

## confidence

Alta para la estructura de fixtures y asserts P0. Media para nombres exactos de comandos/helpers hasta integrarlos en el repo real de la Mac de trabajo.

## evidence_paths

- `jobs/20260525T214513-telegram-radar-regression-fixtures-v1.md`
- `claims/20260525T214513-telegram-radar-regression-fixtures-v1.json`
- `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md`
- `results/20260525T211520-postpatch-telegram-radar-gate-audit-v1.result.md`
- `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md`
- `results/20260525T164233-radares-anti-informe-vacio-operational-gate-v1.result.md`
- `results/20260525T120001-radares-anti-informe-vacio-v1.result.md`
- `results/20260525T124108-telegram-quality-scorecard.result.md`
- `context/fronts/telegram.md`
- `context/fronts/radares.md`
- `protocol.md`

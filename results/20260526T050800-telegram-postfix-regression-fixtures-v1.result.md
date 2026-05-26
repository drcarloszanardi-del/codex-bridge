# Resultado - 20260526T050800-telegram-postfix-regression-fixtures-v1

## summary

Paquete portable de fixtures post-fix para que el orquestador lo copie al repo real sin reinterpretar la auditoria. No toque Telegram real, no inspeccione el patch de la Mac de trabajo y no abri secretos.

Objetivo: bloquear regresiones donde `route_strength` sea demasiado laxo o demasiado conservador, donde adjuntos sin caption pierdan contexto, o donde `media_group_handled` tape un album sin trazabilidad.

## coverage_table

| fuente permitida | uso | limite |
| --- | --- | --- |
| `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md` | Base de los 12 casos T_POSTFIX. | No inspecciona el patch real. |
| `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md` | Estilo de fixtures, asserts y gates P0. | Casos previos son sinteticos. |
| `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md` | Politicas de topic, media buffer, delivery y payload tecnico. | Parametros de tiempo deben ajustarse al repo real. |
| `context/fronts/telegram.md` | Estado canonico: entrega real, buffers, ContextBinder y ResetScope. | No contiene implementacion actual. |
| `protocol.md` | Reglas de bridge, no acciones externas y decision final del orquestador. | Este resultado es paquete portable, no integracion. |

## fixture_tree

```text
fixtures/
  telegram/
    postfix/
      T_POSTFIX_001_direct_reels_captionless_album.json
      T_POSTFIX_002_direct_weak_reels_hint_no_job.json
      T_POSTFIX_003_direct_explicit_reels_deliverable.json
      T_POSTFIX_004_direct_clinical_voice_not_reels.json
      T_POSTFIX_005_captionless_attachment_stale_route.json
      T_POSTFIX_006_captionless_attachment_recent_real_thread.json
      T_POSTFIX_007_media_group_handled_traced_drain.json
      T_POSTFIX_008_media_group_handled_missing_trace.json
      T_POSTFIX_009_direct_codex_ops_main_channel.json
      T_POSTFIX_010_outbox_without_message_id.json
      T_POSTFIX_011_raw_diff_payload_blocked.json
      T_POSTFIX_012_unknown_topic_no_context_inheritance.json
```

## fixtures_json

`fixtures/telegram/postfix/T_POSTFIX_001_direct_reels_captionless_album.json`

```json
{
  "id": "T_POSTFIX_001",
  "kind": "telegram_event_cluster",
  "description": "Direct request for a reel followed by captionless photos must become one REELS job.",
  "input": {
    "chat_type": "direct",
    "topic_id": null,
    "active_route": null,
    "events": [
      {"t_ms": 0, "type": "text", "text": "Armame un reel CMP con estas fotos."},
      {"t_ms": 1400, "type": "photo", "file_id": "photo_a", "caption": null, "media_group_id": "grp_pf_1"},
      {"t_ms": 2200, "type": "photo", "file_id": "photo_b", "caption": null, "media_group_id": "grp_pf_1"},
      {"t_ms": 7600, "type": "photo", "file_id": "photo_c", "caption": null, "media_group_id": "grp_pf_1"},
      {"t_ms": 11800, "type": "photo", "file_id": "photo_d", "caption": null, "media_group_id": "grp_pf_1"}
    ]
  },
  "expected": {
    "front": "REELS",
    "route_strength": "explicit_front_deliverable",
    "jobs_created": 1,
    "attachments_count": 4,
    "media_state_after_quiet_period": "closed",
    "model_call_before_media_closed": false,
    "send_policy": "suppress_until_result",
    "not_front": "DIRECT"
  }
}
```

`fixtures/telegram/postfix/T_POSTFIX_002_direct_weak_reels_hint_no_job.json`

```json
{
  "id": "T_POSTFIX_002",
  "kind": "telegram_event",
  "description": "Weak contextual hint about a prior REELS artifact must not mutate the real route.",
  "input": {
    "chat_type": "direct",
    "topic_id": null,
    "text": "Esa voz quedo rara, no me convence.",
    "recent_context_hint": "REELS",
    "attachments": []
  },
  "expected": {
    "front": "DIRECT",
    "route_strength": "weak_hint",
    "reason": "direct_context_hint_REELS",
    "job_policy": "no_job",
    "mutates_active_route": false,
    "not_front": "REELS"
  }
}
```

`fixtures/telegram/postfix/T_POSTFIX_003_direct_explicit_reels_deliverable.json`

```json
{
  "id": "T_POSTFIX_003",
  "kind": "telegram_event",
  "description": "Explicit direct REELS deliverable must route to REELS even from main channel.",
  "input": {
    "chat_type": "direct",
    "topic_id": null,
    "text": "#REELS renderiza una version con este material.",
    "attachments": [{"type": "document", "file_id": "asset_pack_1"}]
  },
  "expected": {
    "front": "REELS",
    "route_strength_in": ["explicit_front", "explicit_front_deliverable"],
    "job_policy": "create_job",
    "reply_target_in": ["REELS_TOPIC", "needs_approval"],
    "send_policy": "suppress_until_result"
  }
}
```

`fixtures/telegram/postfix/T_POSTFIX_004_direct_clinical_voice_not_reels.json`

```json
{
  "id": "T_POSTFIX_004",
  "kind": "telegram_event",
  "description": "The word voice in a clinical sentence is not a REELS signal.",
  "input": {
    "chat_type": "direct",
    "topic_id": null,
    "text": "La voz del paciente esta mas grave y refiere dolor cervical.",
    "attachments": []
  },
  "expected": {
    "front_in": ["CLINICA", "UNKNOWN_REVIEW", "DIRECT"],
    "front_not": "REELS",
    "route_strength_not": "explicit_front_deliverable",
    "reason_not": "direct_context_hint_REELS"
  }
}
```

`fixtures/telegram/postfix/T_POSTFIX_005_captionless_attachment_stale_route.json`

```json
{
  "id": "T_POSTFIX_005",
  "kind": "telegram_event",
  "description": "Captionless attachment must not inherit stale VIAJES active route.",
  "input": {
    "chat_type": "direct",
    "topic_id": null,
    "text": null,
    "attachments": [{"type": "photo", "file_id": "photo_lonely"}],
    "active_route": {
      "front": "VIAJES",
      "thread_id": 2610,
      "age_seconds": 86400,
      "has_real_thread": false,
      "expired": true
    }
  },
  "expected": {
    "front_in": ["DIRECT", "UNKNOWN_REVIEW"],
    "front_not": "VIAJES",
    "route_strength_not": "recent_media_context",
    "job_policy_in": ["unknown_review", "no_job"],
    "mutates_active_route": false
  }
}
```

`fixtures/telegram/postfix/T_POSTFIX_006_captionless_attachment_recent_real_thread.json`

```json
{
  "id": "T_POSTFIX_006",
  "kind": "telegram_event_cluster",
  "description": "Captionless attachment may inherit a recent real route only when media is expected.",
  "input": {
    "chat_type": "direct",
    "topic_id": null,
    "active_route": {
      "front": "REELS",
      "thread_id": 6,
      "age_seconds": 45,
      "has_real_thread": true,
      "expired": false,
      "expecting_media": true
    },
    "events": [
      {"t_ms": 0, "type": "text", "text": "Te paso el ultimo material para el reel."},
      {"t_ms": 6000, "type": "video", "file_id": "video_followup", "caption": null}
    ]
  },
  "expected": {
    "front": "REELS",
    "route_strength": "recent_media_context",
    "reply_target": {"thread_id": 6},
    "attachments_count": 1,
    "jobs_created": 1,
    "model_call_before_media_closed": false
  }
}
```

`fixtures/telegram/postfix/T_POSTFIX_007_media_group_handled_traced_drain.json`

```json
{
  "id": "T_POSTFIX_007",
  "kind": "contralor_event",
  "description": "Traced media_group_handled is healthy drain, not technical error.",
  "input": {
    "event_type": "media_group_handled",
    "cluster_id": "cluster_reels_001",
    "event_ids": ["evt_1", "evt_2", "evt_3", "evt_4"],
    "message_id": 5214,
    "job_id": "job_reels_001",
    "delivery_required": false,
    "drained_at": "2026-05-26T05:00:00-03:00"
  },
  "expected": {
    "contralor_new_finding": false,
    "technical_error": false,
    "status": "healthy_drain"
  }
}
```

`fixtures/telegram/postfix/T_POSTFIX_008_media_group_handled_missing_trace.json`

```json
{
  "id": "T_POSTFIX_008",
  "kind": "contralor_event",
  "description": "media_group_handled without trace must remain visible as warning/error.",
  "input": {
    "event_type": "media_group_handled",
    "cluster_id": null,
    "event_ids": [],
    "message_id": null,
    "job_id": null,
    "delivery_required": false,
    "drained_at": "2026-05-26T05:00:00-03:00"
  },
  "expected": {
    "contralor_new_finding": true,
    "severity_in": ["warning", "error"],
    "reason": "media_group_handled_missing_trace",
    "must_not_mark_healthy": true
  }
}
```

`fixtures/telegram/postfix/T_POSTFIX_009_direct_codex_ops_main_channel.json`

```json
{
  "id": "T_POSTFIX_009",
  "kind": "telegram_event",
  "description": "Direct CODEX-OPS remains answerable in main channel without GENERAL thread inheritance.",
  "input": {
    "chat_type": "direct",
    "topic_id": null,
    "text": "Estas trabajando?",
    "general_thread_id": null,
    "attachments": []
  },
  "expected": {
    "front_in": ["DIRECT", "CODEX-OPS"],
    "route_strength": "direct_default",
    "reply_target": "main_channel",
    "job_policy": "no_job",
    "may_reply_brief_status": true,
    "thread_id": null
  }
}
```

`fixtures/telegram/postfix/T_POSTFIX_010_outbox_without_message_id.json`

```json
{
  "id": "T_POSTFIX_010",
  "kind": "delivery_result",
  "description": "Outbox queued is not sent.",
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

`fixtures/telegram/postfix/T_POSTFIX_011_raw_diff_payload_blocked.json`

```json
{
  "id": "T_POSTFIX_011",
  "kind": "telegram_response_candidate",
  "description": "Raw diff or trace must be blocked before Telegram.",
  "input": {
    "route": "CODEX-OPS",
    "text": "diff --git a/scripts/codex_telegram_direct.py b/scripts/codex_telegram_direct.py\n@@ -10,7 +10,7 @@\n- old\n+ new\nTraceback (most recent call last): sample internal error"
  },
  "expected": {
    "send_policy": "block",
    "hard_fail": "raw_technical_payload_to_telegram",
    "artifact_local_required": true,
    "telegram_send_called": false
  }
}
```

`fixtures/telegram/postfix/T_POSTFIX_012_unknown_topic_no_context_inheritance.json`

```json
{
  "id": "T_POSTFIX_012",
  "kind": "telegram_event",
  "description": "Unknown topic must not inherit global or prior context.",
  "input": {
    "chat_type": "topic",
    "topic_id": 999999,
    "topic_mapped": false,
    "text": "Usa lo anterior y mandalo.",
    "recent_context_hint": "REELS",
    "attachments": []
  },
  "expected": {
    "front": "UNKNOWN_REVIEW",
    "route_strength": "unknown",
    "job_policy": "unknown_review",
    "context_inherited": false,
    "reply_target": "same_unknown_topic_or_review_queue"
  }
}
```

## assertions

Pseudo-asserts portables para el runner:

```python
def assert_postfix_fixture(fixture, decision):
    exp = fixture["expected"]

    if "front" in exp:
        assert decision["front"] == exp["front"]
    if "front_in" in exp:
        assert decision["front"] in exp["front_in"]
    if "front_not" in exp:
        assert decision["front"] != exp["front_not"]
    if "not_front" in exp:
        assert decision["front"] != exp["not_front"]

    if "route_strength" in exp:
        assert decision.get("route_strength") == exp["route_strength"]
    if "route_strength_in" in exp:
        assert decision.get("route_strength") in exp["route_strength_in"]
    if "route_strength_not" in exp:
        assert decision.get("route_strength") != exp["route_strength_not"]

    if exp.get("mutates_active_route") is False:
        assert decision.get("mutates_active_route") is False
    if "job_policy" in exp:
        assert decision.get("job_policy") == exp["job_policy"]
    if "job_policy_in" in exp:
        assert decision.get("job_policy") in exp["job_policy_in"]
    if "jobs_created" in exp:
        assert decision.get("jobs_created") == exp["jobs_created"]

    if exp.get("model_call_before_media_closed") is False:
        assert decision.get("model_call_before_media_closed") is False
    if "attachments_count" in exp:
        assert decision.get("attachments_count") == exp["attachments_count"]

    if exp.get("may_say_sent") is False:
        assert decision.get("sent_confirmed") is False
    if exp.get("telegram_send_called") is False:
        assert decision.get("telegram_send_called") is False

    if exp.get("contralor_new_finding") is not None:
        assert decision.get("contralor_new_finding") == exp["contralor_new_finding"]
```

Hard fails:

- `route_strength=weak_hint` and `mutates_active_route=true`.
- `front=REELS` from direct explicit deliverable but `job_policy != create_job`.
- Captionless media inherited from stale route.
- `media_group_handled` marked healthy without `cluster_id` and `event_ids`.
- `delivery_label=sent` without `telegram_response.ok=true` and `message_id`.
- Telegram send called with raw diff, traceback or long technical payload.

## minimal_test_runner_pseudocode

```python
from pathlib import Path
import json

FIXTURE_DIR = Path("fixtures/telegram/postfix")

def route_or_validate(fixture):
    kind = fixture["kind"]
    if kind in {"telegram_event", "telegram_event_cluster"}:
        return route_event_pure(fixture["input"])
    if kind == "delivery_result":
        return confirm_delivery_pure(fixture["input"])
    if kind == "telegram_response_candidate":
        return pre_send_gate_pure(fixture["input"])
    if kind == "contralor_event":
        return contralor_classify_event_pure(fixture["input"])
    raise AssertionError(f"unknown fixture kind: {kind}")

def test_postfix_fixtures():
    for path in sorted(FIXTURE_DIR.glob("T_POSTFIX_*.json")):
        fixture = json.loads(path.read_text())
        decision = route_or_validate(fixture)
        assert_postfix_fixture(fixture, decision)
```

## porting_notes_for_orchestrator

1. Copiar los 12 JSON a `fixtures/telegram/postfix/`.
2. Mapear `route_event_pure`, `confirm_delivery_pure`, `pre_send_gate_pure` y `contralor_classify_event_pure` a helpers reales sin red.
3. Asegurar que cada `RouterDecision` exponga `front`, `route_strength`, `reply_target`, `job_policy`, `send_policy`, `media_state`, `attachments_count`, `mutates_active_route`.
4. Asegurar que el contralor exponga `contralor_new_finding`, `severity`, `reason` y `technical_error`.
5. No usar IDs reales en fixtures: mantener `thread_id` simbolico o valores de prueba.
6. Ejecutar estos fixtures despues de `py_compile` y antes de cualquier envio real.
7. Si el repo real ya tiene fixtures de Telegram, sumar estos como regresion post-fix, no reemplazar los anteriores.

## acceptance_gate

Release bloqueado si falla cualquiera:

1. T_POSTFIX_001 no crea un solo job REELS con 4 adjuntos.
2. T_POSTFIX_002 muta active route o crea job largo.
3. T_POSTFIX_003 queda en DIRECT.
4. T_POSTFIX_004 routea a REELS por la palabra "voz".
5. T_POSTFIX_005 hereda VIAJES vencido.
6. T_POSTFIX_006 no hereda route reciente con thread real y media esperada.
7. T_POSTFIX_007 aparece como error tecnico.
8. T_POSTFIX_008 queda marcado sano.
9. T_POSTFIX_009 no puede responder por main channel.
10. T_POSTFIX_010 permite decir enviado.
11. T_POSTFIX_011 permite enviar diff/trace crudo.
12. T_POSTFIX_012 hereda contexto en topic desconocido.

## risk_notes

- Los fixtures no prueban Telegram real ni delivery externo; son tests puros para evitar contaminacion antes de enviar.
- Los TTL exactos de active route deben ajustarse al repo real; el fixture fija comportamiento, no segundos definitivos.
- Si el router usa nombres distintos para `DIRECT` o `UNKNOWN_REVIEW`, mapearlos sin cambiar la intencion.
- `media_group_handled.message_id` puede referir al mensaje drenado o al envio asociado segun implementacion; lo critico es que exista trazabilidad suficiente.

## risks_limits

- No se inspecciono el patch real ni se ejecuto Telegram.
- Los fixtures estan escritos como contrato portable; el orquestador debe mapear helpers y nombres de campos al repo real.
- Los casos cubren contaminacion post-fix, no toda la suite historica de Telegram.
- No contienen IDs ni secretos reales.

## recommendation

Portar estos 12 fixtures como suite post-fix y hacerlos correr junto a los gates P0 anteriores. La prioridad es que `route_strength` quede visible y testeado, porque ahi vive la diferencia entre contexto util y contaminacion.

## confidence

Alta para la cobertura conceptual de la regresion post-fix. Media para nombres exactos de helpers y campos hasta mapearlos al repo real.

## evidence_paths

- `jobs/20260526T050800-telegram-postfix-regression-fixtures-v1.md`
- `results/20260526T043200-telegram-postfix-contamination-audit-v1.result.md`
- `results/20260525T214513-telegram-radar-regression-fixtures-v1.result.md`
- `results/20260525T164232-telegram-topic-routing-regression-suite-v1.result.md`
- `context/fronts/telegram.md`
- `protocol.md`

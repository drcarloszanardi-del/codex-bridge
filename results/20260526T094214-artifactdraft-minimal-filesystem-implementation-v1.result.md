# Resultado - 20260526T094214-artifactdraft-minimal-filesystem-implementation-v1

## summary

Especificacion implementable de `ArtifactDraft` minimo, filesystem-first. La capa propuesta separa brief, borradores, assets, QA, final y recibos de entrega para impedir que un borrador largo, un reel, una presentacion o un informe se traten como entrega real sin revision y sin recibo verificable.

La version inicial no envia Telegram, Gmail, Drive ni ningun canal externo. Solo crea carpetas locales, `artifact.json`, archivos base y un validator que decide si el artefacto puede pasar de borrador a QA, aprobado local o cola externa.

## source_counts

| Fuente permitida | Estado | Uso |
| --- | ---: | --- |
| `results/20260526T064631-artifactdraft-implementation-review.result.md` | Revisada | Schema inicial, paths, router changes, migration plan y tests. |
| `results/20260526T073800-batch-results-priority-triage-v1.result.md` | Revisada | Priorizacion de ArtifactDraft como integracion local de bajo riesgo. |
| `protocol.md` | Revisado | Reglas duras: sin acciones externas, sin secretos, decision final del orquestador. |
| `docs/reels_premium_acceptance_gate.md` | Revisada | Gates de reels: evidencia visual, material propio, privacidad, audio y aprobacion. |

## proposed_folder_structure

Raiz local recomendada:

```text
artifacts/
  telegram/
  reels_cmp/
  presentaciones/
  informes/
  radar/
  viajes/
```

Estructura por artefacto:

```text
artifacts/<front>/<artifact_id>/
  artifact.json
  brief.md
  context_refs.md
  drafts/
    v1.md
  assets/
    requested.md
    manifest.json
  qa/
    qa_report.md
    evidence/
  final/
    README.md
  delivery/
    receipt.json
```

Reglas de uso:

- `drafts/` puede contener trabajo incompleto.
- `final/` solo contiene candidatos limpios para revision del orquestador.
- `delivery/receipt.json` se completa solo despues de una entrega externa real hecha por el orquestador.
- Binarios pesados o material sensible deben quedar como rutas locales autorizadas o derivados seguros; no copiarlos al repo por defecto.
- Si el artefacto requiere material propio, `assets/manifest.json` debe marcar cada item como `approved`, `rejected`, `needs_review` o `missing`.

## artifact_json_min_schema

```json
{
  "artifact_id": "20260526T094214-front-slug",
  "schema_version": 1,
  "front": "telegram|reels_cmp|presentaciones|informes|radar|viajes",
  "job_id": "string",
  "title": "string",
  "status": "draft",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "owner": "orchestrator|personal-xh",
  "source": {
    "kind": "bridge_job|manual|telegram_context|local_brief",
    "refs": ["jobs/<job_id>.md"]
  },
  "paths": {
    "brief": "brief.md",
    "context_refs": "context_refs.md",
    "drafts_dir": "drafts",
    "assets_manifest": "assets/manifest.json",
    "qa_report": "qa/qa_report.md",
    "final_dir": "final",
    "delivery_receipt": "delivery/receipt.json"
  },
  "qa": {
    "status": "pending",
    "required_checks": [],
    "passed_checks": [],
    "failed_checks": []
  },
  "delivery": {
    "target": "none|telegram|email|drive|manual",
    "requires_receipt": true,
    "receipt_type": "none|message_id|email_sent_id|drive_file_id|manual_signature",
    "receipt_value": null,
    "delivered_at": null
  },
  "privacy": {
    "contains_personal_material": false,
    "contains_patient_data": false,
    "safe_for_external_review": false,
    "notes": []
  }
}
```

Campos obligatorios para validar:

| Campo | Regla |
| --- | --- |
| `artifact_id` | Debe coincidir con nombre de carpeta. |
| `front` | Uno de los frentes permitidos. |
| `status` | Uno de los estados permitidos. |
| `paths.*` | Cada path requerido debe existir. |
| `qa.status` | `pending`, `pass` o `fail`. |
| `delivery.requires_receipt` | `true` para cualquier canal externo. |
| `privacy.contains_patient_data` | Si `true`, no puede pasar a `queued_external` sin bloqueo/decision humana. |

## allowed_states

| Estado | Uso | Puede salir externo |
| --- | --- | --- |
| `draft` | Brief o borrador inicial. | No. |
| `qa_ready` | Tiene final candidato y QA pendiente. | No. |
| `approved_local` | QA local pasa y el orquestador puede revisar/decidir. | No automaticamente. |
| `queued_external` | El orquestador decidio envio externo y falta recibo real. | No declarar entregado. |
| `delivered` | Existe recibo real y verificable. | Ya fue entregado por orquestador. |
| `blocked` | Falta material, QA falla, privacidad o contrato incompleto. | No. |

Transiciones permitidas:

```text
draft -> qa_ready -> approved_local -> queued_external -> delivered
draft -> blocked
qa_ready -> blocked
approved_local -> blocked
queued_external -> blocked
```

Transiciones prohibidas:

- `draft -> delivered`
- `qa_ready -> delivered`
- `approved_local -> delivered` sin `queued_external`
- `queued_external -> delivered` sin recibo real
- Cualquier estado hacia `queued_external` con `privacy.contains_patient_data=true`

## receipt_rules

No declarar entrega sin recibo real:

| Canal | Recibo minimo | Hard fail si falta |
| --- | --- | --- |
| Telegram | `message_id` y `chat_id` registrados por el orquestador. | No decir "enviado". |
| Email | `email_sent_id` o identificador equivalente del cliente/API. | No decir "mandado por mail". |
| Drive | `drive_file_id` y ruta/nombre revisado. | No decir "subido". |
| Manual | `manual_signature`, fecha y responsable humano. | No decir "entregado". |

`personal-xh` no debe completar recibos externos. Como maximo puede dejar `queued_external` sugerido o `approved_local`; el orquestador decide y registra el recibo.

## proposed_small_python_helper

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ALLOWED_FRONTS = {"telegram", "reels_cmp", "presentaciones", "informes", "radar", "viajes"}
ALLOWED_STATES = {"draft", "qa_ready", "approved_local", "queued_external", "delivered", "blocked"}
EXTERNAL_TARGETS = {"telegram", "email", "drive", "manual"}
REQUIRED_FILES = ["artifact.json", "brief.md", "context_refs.md", "assets/manifest.json", "qa/qa_report.md", "delivery/receipt.json"]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def create_artifact(root: Path, front: str, artifact_id: str, job_id: str, title: str) -> Path:
    if front not in ALLOWED_FRONTS:
        raise SystemExit(f"invalid front: {front}")
    base = root / front / artifact_id
    for rel in ["drafts", "assets", "qa/evidence", "final", "delivery"]:
        (base / rel).mkdir(parents=True, exist_ok=True)
    manifest = {
        "artifact_id": artifact_id,
        "schema_version": 1,
        "front": front,
        "job_id": job_id,
        "title": title,
        "status": "draft",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "owner": "orchestrator",
        "source": {"kind": "bridge_job", "refs": [f"jobs/{job_id}.md"] if job_id else []},
        "paths": {
            "brief": "brief.md",
            "context_refs": "context_refs.md",
            "drafts_dir": "drafts",
            "assets_manifest": "assets/manifest.json",
            "qa_report": "qa/qa_report.md",
            "final_dir": "final",
            "delivery_receipt": "delivery/receipt.json",
        },
        "qa": {"status": "pending", "required_checks": [], "passed_checks": [], "failed_checks": []},
        "delivery": {
            "target": "none",
            "requires_receipt": True,
            "receipt_type": "none",
            "receipt_value": None,
            "delivered_at": None,
        },
        "privacy": {
            "contains_personal_material": False,
            "contains_patient_data": False,
            "safe_for_external_review": False,
            "notes": [],
        },
    }
    (base / "artifact.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    (base / "brief.md").write_text("# Brief\n\n", encoding="utf-8")
    (base / "context_refs.md").write_text("# Context refs\n\n", encoding="utf-8")
    (base / "drafts/v1.md").write_text("# Draft v1\n\n", encoding="utf-8")
    (base / "assets/manifest.json").write_text('{"assets":[]}\n', encoding="utf-8")
    (base / "qa/qa_report.md").write_text("# QA report\n\nstatus: pending\n", encoding="utf-8")
    (base / "final/README.md").write_text("Final candidates go here after QA.\n", encoding="utf-8")
    (base / "delivery/receipt.json").write_text('{"status":"not_delivered","receipt_value":null}\n', encoding="utf-8")
    return base


def validate_artifact(base: Path) -> dict:
    errors = []
    warnings = []
    artifact_path = base / "artifact.json"
    if not artifact_path.exists():
        return {"ok": False, "errors": ["missing artifact.json"], "warnings": []}
    data = json.loads(artifact_path.read_text(encoding="utf-8"))
    for rel in REQUIRED_FILES:
        if not (base / rel).exists():
            errors.append(f"missing {rel}")
    if data.get("artifact_id") != base.name:
        errors.append("artifact_id does not match folder name")
    if data.get("front") not in ALLOWED_FRONTS:
        errors.append("invalid front")
    if data.get("status") not in ALLOWED_STATES:
        errors.append("invalid status")
    status = data.get("status")
    qa_status = data.get("qa", {}).get("status")
    delivery = data.get("delivery", {})
    privacy = data.get("privacy", {})
    if status in {"approved_local", "queued_external"} and qa_status != "pass":
        errors.append("qa must pass before approved_local or queued_external")
    if status == "queued_external" and delivery.get("target") not in EXTERNAL_TARGETS:
        errors.append("queued_external requires external target")
    if status == "delivered":
        if not delivery.get("receipt_value"):
            errors.append("delivered requires real receipt_value")
        if delivery.get("receipt_type") == "none":
            errors.append("delivered requires receipt_type")
    if privacy.get("contains_patient_data") and status in {"queued_external", "delivered"}:
        errors.append("patient data cannot be queued or delivered by this gate")
    if privacy.get("contains_personal_material") and not privacy.get("safe_for_external_review"):
        warnings.append("personal material not marked safe_for_external_review")
    return {"ok": not errors, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    new = sub.add_parser("new")
    new.add_argument("--root", default="artifacts")
    new.add_argument("--front", required=True)
    new.add_argument("--artifact-id", required=True)
    new.add_argument("--job-id", default="")
    new.add_argument("--title", default="")
    val = sub.add_parser("validate")
    val.add_argument("path")
    args = parser.parse_args()
    if args.cmd == "new":
        path = create_artifact(Path(args.root), args.front, args.artifact_id, args.job_id, args.title)
        print(json.dumps({"ok": True, "path": str(path)}, indent=2))
        return 0
    result = validate_artifact(Path(args.path))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
```

## minimal_fixtures

### Fixture 1 - reel candidato

```json
{
  "artifact_id": "20260526T094214-reels-cavernoma-candidate",
  "front": "reels_cmp",
  "status": "qa_ready",
  "qa": {
    "status": "pending",
    "required_checks": [
      "premium_gate",
      "contact_sheet_8_12_frames",
      "own_material_or_authorized",
      "privacy_no_patient_data",
      "audio_status"
    ],
    "passed_checks": [],
    "failed_checks": []
  },
  "delivery": {
    "target": "none",
    "requires_receipt": true,
    "receipt_type": "none",
    "receipt_value": null
  },
  "privacy": {
    "contains_personal_material": true,
    "contains_patient_data": false,
    "safe_for_external_review": false,
    "notes": ["No publicar hasta aprobacion del orquestador."]
  }
}
```

Esperado: valida estructura, pero no permite `approved_local` ni `queued_external` hasta que QA pase y `safe_for_external_review=true`.

### Fixture 2 - informe viaje

```json
{
  "artifact_id": "20260526T094214-viajes-informe-candidato",
  "front": "viajes",
  "status": "draft",
  "qa": {
    "status": "pending",
    "required_checks": ["sources", "price_expiry", "no_booking", "human_decision_needed"],
    "passed_checks": [],
    "failed_checks": []
  },
  "delivery": {
    "target": "none",
    "requires_receipt": true,
    "receipt_type": "none",
    "receipt_value": null
  },
  "privacy": {
    "contains_personal_material": false,
    "contains_patient_data": false,
    "safe_for_external_review": true,
    "notes": []
  }
}
```

Esperado: puede quedar `draft` o `qa_ready`; no reservar ni declarar enviado.

### Fixture 3 - informe radar bloqueado

```json
{
  "artifact_id": "20260526T094214-radar-bloqueado",
  "front": "radar",
  "status": "blocked",
  "qa": {
    "status": "fail",
    "required_checks": ["sources_attempted", "fallback_routes", "candidates_or_rejections"],
    "passed_checks": ["sources_attempted"],
    "failed_checks": ["fallback_routes", "candidates_or_rejections"]
  },
  "delivery": {
    "target": "none",
    "requires_receipt": true,
    "receipt_type": "none",
    "receipt_value": null
  },
  "privacy": {
    "contains_personal_material": false,
    "contains_patient_data": false,
    "safe_for_external_review": false,
    "notes": ["No enviar como informe final; volver a fallback."]
  }
}
```

Esperado: `blocked`; no puede saltar a entrega.

### Fixture 4 - documento listo para revision

```json
{
  "artifact_id": "20260526T094214-presentacion-revision-local",
  "front": "presentaciones",
  "status": "approved_local",
  "qa": {
    "status": "pass",
    "required_checks": ["render_check", "layout_check", "no_internal_notes", "final_candidate_exists"],
    "passed_checks": ["render_check", "layout_check", "no_internal_notes", "final_candidate_exists"],
    "failed_checks": []
  },
  "delivery": {
    "target": "none",
    "requires_receipt": true,
    "receipt_type": "none",
    "receipt_value": null
  },
  "privacy": {
    "contains_personal_material": false,
    "contains_patient_data": false,
    "safe_for_external_review": true,
    "notes": ["Listo para decision del orquestador."]
  }
}
```

Esperado: `approved_local`; todavia no `delivered`.

## orchestrator_first_implementation

1. Crear helper local `scripts/artifacts/artifactdraft.py` con subcomandos `new` y `validate`.
2. Crear carpetas base `artifacts/<front>/` y excluir binarios pesados si el repo no debe versionarlos.
3. Activarlo primero solo para:
   - Telegram largo o con adjuntos.
   - Reels CMP.
   - Presentaciones/documentos.
   - Informes radar/viaje con riesgo de "entregado" prematuro.
4. Hacer que `validate` bloquee:
   - `delivered` sin recibo real.
   - `queued_external` sin QA pass.
   - salida externa con datos de paciente.
   - reels sin evidencia visual/QA segun gate premium.
5. Agregar fixtures minimos y test local antes de tocar Telegram real.
6. Integrar `artifact_id` en el resultado del bridge para que el orquestador pueda auditar cada entrega.

## attempted_routes

- Se revisaron solo las fuentes permitidas por el job.
- No se abrieron Drive, iCloud, Photos, Gmail, Telegram real, Downloads, ObraCash ni bibliotecas completas.
- No se hicieron acciones externas ni se tocaron credenciales.
- El helper es propuesta portable; no modifica el sistema productivo.

## risks_limits

- Si se copian videos, imagenes o decks pesados al repo, el historial puede crecer demasiado; por defecto conviene manifestar rutas locales y derivados seguros.
- El estado `approved_local` no equivale a aprobado por el Doctor; solo indica que paso QA local.
- El estado `queued_external` no equivale a entrega. Requiere recibo posterior del orquestador.
- Para reels, un manifest tecnico no reemplaza evidencia visual: contact sheet o proxy seguro sigue siendo obligatorio.
- Para material sensible, la politica debe ser bloqueo por defecto hasta revision humana.

## recommendation

Implementar `ArtifactDraft` como gate local minimalista antes de cualquier entrega externa. El primer corte debe crear carpetas, `artifact.json`, fixtures y validator; despues se integra en rutas concretas. La regla central es simple: `delivered` solo existe con recibo real, y `queued_external` solo existe con QA pass y decision del orquestador.

## confidence

Alta para estructura, estados y reglas de recibo porque derivan de fuentes locales consistentes. Media para nombres finales de paths hasta ver el repo real donde Codex principal lo porte.

## evidence_paths

- `jobs/20260526T094214-artifactdraft-minimal-filesystem-implementation-v1.md`
- `results/20260526T064631-artifactdraft-implementation-review.result.md`
- `results/20260526T073800-batch-results-priority-triage-v1.result.md`
- `protocol.md`
- `docs/reels_premium_acceptance_gate.md`

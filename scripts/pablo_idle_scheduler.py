#!/usr/bin/env python3
"""Keep personal-xh/Pablo supplied with useful high-reasoning work."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JOBS = ROOT / "jobs"
RESULTS = ROOT / "results"
STATUS = ROOT / "status"
TMP = ROOT / "tmp"
SCHEDULER_STATE = TMP / "pablo_idle_scheduler_state.json"


WORK_POOL: list[dict[str, object]] = [
    {
        "slug": "clinica-correcciones-a-fixtures-implementacion",
        "title": "Implementacion plan clinico: correcciones del Doctor a fixtures",
        "front": "CLINICA",
        "objective": "Tomar los resultados clinicos previos de Pablo y proponer la secuencia exacta de integracion en la app real, con archivos candidatos, tests, riesgos y orden de bajo impacto.",
        "context": [
            "context/fronts/clinica.md",
            "results/20260525T120000-clinica-fixtures-lumbares-v1.result.md",
            "results/20260525T084316-clinica-integration-checklist-route-guard-fixtures-v2.result.md",
        ],
        "output": [
            "integration_plan",
            "files_to_inspect",
            "test_cases",
            "risk_order",
            "acceptance_criteria",
        ],
    },
    {
        "slug": "radar-anti-empty-script-spec",
        "title": "Implementacion gate anti informe vacio para radares",
        "front": "INVERSIONES",
        "objective": "Convertir el contrato anti informe vacio de radares en una especificacion de script/gate aplicable a inmobiliaria e instrumental, con thresholds, JSON schema y mensajes de bloqueo.",
        "context": [
            "context/fronts/radares.md",
            "results/20260525T120001-radares-anti-informe-vacio-v1.result.md",
            "decisions/radar_scorecards_v1.md",
        ],
        "output": [
            "json_schema",
            "gate_rules",
            "fallback_routes",
            "script_plan",
            "qa_examples",
        ],
    },
    {
        "slug": "reels-dia-patria-assets-and-timeline",
        "title": "Reel Dia de la Patria: timeline tecnico y pedido de assets",
        "front": "REELS",
        "objective": "Convertir el concepto del reel Dia de la Patria en timeline tecnico editable, lista minima de assets, variantes de montaje y criterios de QA frame a frame.",
        "context": [
            "context/fronts/reels_cmp.md",
            "results/20260525T120325-reel-dia-patria-cmp-premium-v1.result.md",
        ],
        "output": [
            "timeline_40s",
            "minimal_asset_pack",
            "editing_notes",
            "qa_frame_checklist",
            "doctor_asset_request",
        ],
    },
    {
        "slug": "presentaciones-pilot-pack",
        "title": "Presentaciones IA: pack piloto operativo",
        "front": "PRESENTACIONES",
        "objective": "Definir un pack piloto para una presentacion medica premium: brief, estructura de carpetas, criterios de fuente, visual direction, PPTX editable y QA.",
        "context": [
            "context/fronts/presentaciones.md",
            "results/20260525T122120-presentaciones-ai-pilot-premium-v1.result.md",
            "results/20260525T112543-youtubers-auditoria-profunda-con-pack-obligatorio-v2.result.md",
        ],
        "output": [
            "pilot_pack",
            "brief_template",
            "folder_structure",
            "qa_checklist",
            "membership_trigger",
        ],
    },
    {
        "slug": "artifactdraft-implementation-review",
        "title": "ArtifactDraft: especificacion lista para implementar",
        "front": "CODEX-OPS",
        "objective": "Revisar el resultado ArtifactDraft y convertirlo en una especificacion de implementacion acotada para Codex Directo, Reels y Presentaciones.",
        "context": [
            "context/fronts/telegram.md",
            "context/fronts/reels_cmp.md",
            "context/fronts/presentaciones.md",
            "results/20260525T122121-artifactdraft-telegram-reels-presentaciones-v1.result.md",
        ],
        "output": [
            "schema",
            "paths",
            "router_changes",
            "migration_plan",
            "tests",
        ],
    },
    {
        "slug": "ai-tools-pilot-prioritization",
        "title": "Herramientas IA: priorizar pilotos antes de membresias",
        "front": "CODEX-OPS",
        "objective": "Tomar la matriz de herramientas IA y priorizar 3 pilotos reales con criterio de impacto, privacidad, costo y esfuerzo para el ecosistema Zanardi.",
        "context": [
            "results/20260525T122119-ai-tools-apps-skills-models-deep-v1.result.md",
            "context/youtube_content_packs/20260525-martell-maxmaxdata/",
        ],
        "output": [
            "pilot_priority",
            "cost_privacy_matrix",
            "success_metrics",
            "do_not_buy_yet",
            "next_actions",
        ],
    },
    {
        "slug": "telegram-quality-scorecard",
        "title": "Telegram Directo: scorecard de calidad post-respuesta",
        "front": "CODEX-OPS",
        "objective": "Disenar un scorecard barato 5.3 para evaluar si una respuesta de Telegram respeto frente, contexto, evidencia, tono formal y accion concreta.",
        "context": [
            "context/fronts/telegram.md",
            "results/20260525T111216-telegram-contralor-action-media-arrived-after-response.result.md",
            "results/20260525T111227-telegram-contralor-action-event-handle-error.result.md",
        ],
        "output": [
            "scorecard",
            "thresholds",
            "postmortem_trigger",
            "examples",
            "implementation_plan",
        ],
    },
]


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).astimezone()


def stamp() -> str:
    return now().strftime("%Y%m%dT%H%M%S")


def read_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def result_path_for_job(job_path: Path) -> Path:
    return RESULTS / f"{job_path.stem}.result.md"


def pending_jobs() -> list[Path]:
    if not JOBS.exists():
        return []
    out = []
    for path in sorted(JOBS.glob("*.md")):
        if path.name.startswith("."):
            continue
        if not result_path_for_job(path).exists():
            out.append(path)
    return out


def status_is_idle() -> bool:
    payload = read_json(STATUS / "personal-xh.json")
    return bool(
        payload.get("idle")
        or payload.get("requesting_work")
        or str(payload.get("status") or "").lower() in {"available", "idle", "ready"}
    )


def slug_recently_used(slug: str, state: dict, cooldown_hours: int) -> bool:
    history = state.get("history") if isinstance(state.get("history"), list) else []
    cutoff = now() - dt.timedelta(hours=cooldown_hours)
    for item in history:
        if not isinstance(item, dict) or item.get("slug") != slug:
            continue
        try:
            ts = dt.datetime.fromisoformat(str(item.get("created_at")))
        except ValueError:
            continue
        if ts >= cutoff:
            return True
    return False


def has_open_slug(slug: str) -> bool:
    pattern = re.compile(re.escape(slug))
    for path in pending_jobs():
        if pattern.search(path.stem):
            return True
    return False


def choose_work(state: dict, cooldown_hours: int) -> dict[str, object] | None:
    for item in WORK_POOL:
        slug = str(item["slug"])
        if has_open_slug(slug):
            continue
        if slug_recently_used(slug, state, cooldown_hours):
            continue
        return item
    return None


def render_job(item: dict[str, object]) -> tuple[str, str]:
    slug = str(item["slug"])
    job_id = f"{stamp()}-{slug}"
    context_lines = "\n".join(f"  - `{path}`" for path in item.get("context", []))
    output_lines = "\n".join(f"  - `{section}`" for section in item.get("output", []))
    body = f"""---
id: {job_id}
assignee: personal-xh
model: gpt-5.5-xh
created_at: {now().isoformat(timespec="seconds")}
no_external_actions: true
no_secrets: true
status: pending
---

# Workorder: {item["title"]}

## 10 inicial - direccion del orquestador

- Objetivo: {item["objective"]}
- Frente: {item["front"]}
- Contexto minimo:
{context_lines}
- Herramientas permitidas: leer archivos locales del bridge, analizar, sintetizar y proponer implementacion.
- Herramientas prohibidas: acciones externas, compras, mails, Telegram, secretos, credenciales, datos sensibles no sanitizados.
- Criterio de terminado: resultado accionable, con evidencia, riesgo, decision sugerida y siguiente paso implementable por Codex principal.

## 80 delegado - trabajo del agente

Pablo debe producir estas secciones:

{output_lines}

Tambien debe separar evidencia, inferencia y opinion; y no cerrar con bloqueo sin rutas alternativas, limite exacto y proxima accion.

## 10 final - retorno al orquestador

El resultado debe incluir:

- `summary honesto`
- `coverage_table` o `source_counts`
{output_lines}
- `risks / limits`
- `recommendation`
- `confidence`
- `evidence_paths`

Validar contra `scripts/validate_result_contract.py` antes de marcarlo completado.
"""
    return job_id, body


def run_git(args: list[str]) -> dict:
    proc = subprocess.run(args, cwd=str(ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "cmd": args,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-pending", type=int, default=4)
    parser.add_argument("--max-create", type=int, default=3)
    parser.add_argument("--cooldown-hours", type=int, default=18)
    parser.add_argument("--commit-push", action="store_true")
    args = parser.parse_args()

    JOBS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    STATUS.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)

    state = read_json(SCHEDULER_STATE)
    pending = pending_jobs()
    created: list[dict[str, str]] = []
    if status_is_idle():
        while len(pending) + len(created) < args.target_pending and len(created) < args.max_create:
            item = choose_work(state, args.cooldown_hours)
            if not item:
                break
            job_id, body = render_job(item)
            path = JOBS / f"{job_id}.md"
            path.write_text(body, encoding="utf-8")
            created.append({"job_id": job_id, "slug": str(item["slug"]), "path": str(path)})
            history = state.get("history") if isinstance(state.get("history"), list) else []
            history.append({"job_id": job_id, "slug": str(item["slug"]), "created_at": now().isoformat(timespec="seconds")})
            state["history"] = history[-200:]

    state.update({
        "updated_at": now().isoformat(timespec="seconds"),
        "pending_count_before": len(pending),
        "created_count": len(created),
        "target_pending": args.target_pending,
        "status_idle": status_is_idle(),
    })
    write_json(SCHEDULER_STATE, state)

    git_steps: list[dict] = []
    if created and args.commit_push:
        # The scheduler state lives under tmp/ and is intentionally ignored;
        # only durable jobs belong in the shared bridge history.
        paths = [item["path"] for item in created]
        git_steps.append(run_git(["git", "add", *paths]))
        git_steps.append(run_git(["git", "commit", "-m", "Scheduler queued Pablo idle work"]))
        git_steps.append(run_git(["git", "push"]))

    output = {
        "ok": all(step.get("ok") for step in git_steps) if git_steps else True,
        "pending_count_before": len(pending),
        "created": created,
        "state_path": str(SCHEDULER_STATE),
        "git_steps": git_steps,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if output["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

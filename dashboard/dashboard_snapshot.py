#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard"
JOBS = ROOT / "jobs"
RESULTS = ROOT / "results"
CLAIMS = ROOT / "claims"
STATUS = ROOT / "status"

KNOWN_FRONTS = [
    "CODEX-OPS",
    "CLINICA",
    "TESIS",
    "REELS-CMP",
    "INMOBILIARIA",
    "INSTRUMENTAL",
    "OBRACASH",
    "MAIL",
]


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).astimezone()


def iso(value: dt.datetime) -> str:
    return value.astimezone().isoformat(timespec="seconds")


def parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone()


def age_minutes(value: str | None, base: dt.datetime) -> float | None:
    parsed = parse_time(value)
    if parsed is None:
        return None
    return max(0.0, (base - parsed).total_seconds() / 60.0)


def run(cmd: list[str]) -> dict:
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def read_frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    meta: dict[str, str] = {}
    for raw in text[4:end].splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        meta[key.strip()] = value.strip().strip("\"'")
    return meta


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def mtime_iso(path: Path) -> str:
    return iso(dt.datetime.fromtimestamp(path.stat().st_mtime).astimezone())


def claim_path(job_id: str) -> Path:
    return CLAIMS / f"{job_id}.json"


def result_path(job_id: str) -> Path:
    return RESULTS / f"{job_id}.result.md"


def result_status(path: Path) -> str:
    meta = read_frontmatter(path)
    return meta.get("status", "completed") if path.exists() else ""


def collect_workers() -> list[dict]:
    workers = []
    for path in sorted(STATUS.glob("*.json")):
        payload = read_json(path)
        if not payload:
            continue
        workers.append({
            "role": payload.get("role", path.stem),
            "status": payload.get("status", "unknown"),
            "front": payload.get("front", ""),
            "host": payload.get("host", ""),
            "updated_at": payload.get("updated_at", ""),
            "last_completed_count": len(payload.get("last_completed_jobs", [])),
        })
    return workers


def worker_fresh(workers: list[dict], assignee: str, base: dt.datetime) -> bool:
    if not assignee:
        return False
    for worker in workers:
        if worker.get("role") != assignee:
            continue
        age = age_minutes(worker.get("updated_at"), base)
        return age is not None and age <= 10
    return False


def derive_job_state(job: dict, workers: list[dict], base: dt.datetime) -> str:
    if job["has_result"]:
        status = job.get("result_status", "completed")
        if status in {"blocked", "failed"}:
            return "bloqueado"
        return "done"
    claim = job.get("claim") or {}
    if claim:
        claim_age = age_minutes(claim.get("heartbeat_at") or claim.get("claimed_at"), base)
        if claim_age is not None and claim_age > 240:
            return "bloqueado"
        if worker_fresh(workers, claim.get("assignee", ""), base):
            return "ejecutando"
        return "pensando"
    return "pendiente"


def collect_jobs(workers: list[dict], base: dt.datetime) -> list[dict]:
    jobs = []
    for path in sorted(JOBS.glob("*.md")):
        meta = read_frontmatter(path)
        job_id = path.stem
        result = result_path(job_id)
        claim = read_json(claim_path(job_id))
        item = {
            "id": job_id,
            "front": meta.get("front", "UNKNOWN"),
            "assignee": meta.get("assignee", ""),
            "status": meta.get("status", ""),
            "model": meta.get("model", ""),
            "reasoning_effort": meta.get("reasoning_effort", ""),
            "path": f"../jobs/{path.name}",
            "claim": claim,
            "claimed_by": claim.get("assignee", ""),
            "has_result": result.exists(),
            "result_path": f"../results/{result.name}" if result.exists() else None,
            "result_status": result_status(result),
            "mtime": mtime_iso(path),
            "result_mtime": mtime_iso(result) if result.exists() else None,
        }
        item["state"] = derive_job_state(item, workers, base)
        jobs.append(item)
    return jobs


def front_next_action(state: str, pending: int, blocked: int) -> str:
    if blocked:
        return "revisar bloqueo"
    if state in {"ejecutando", "pensando"}:
        return "esperar resultado"
    if pending:
        return "tomar siguiente trabajo"
    return "sin accion"


def collect_fronts(jobs: list[dict]) -> list[dict]:
    names = set(KNOWN_FRONTS)
    names.update(job["front"] for job in jobs if job.get("front"))
    fronts = []
    order = {"bloqueado": 0, "ejecutando": 1, "pensando": 2, "pendiente": 3, "done": 4, "quieto": 5}
    for front in sorted(names):
        scoped = [job for job in jobs if job.get("front") == front]
        active = [job for job in scoped if job["state"] in {"pendiente", "pensando", "ejecutando", "bloqueado"}]
        done = [job for job in scoped if job["state"] == "done"]
        state = "quieto"
        if active:
            state = sorted((job["state"] for job in active), key=lambda value: order.get(value, 9))[0]
        current = next((job for job in active if job["state"] == state), None)
        last_result = sorted(
            (job for job in done if job.get("result_mtime")),
            key=lambda item: item["result_mtime"] or "",
            reverse=True,
        )
        blocked = sum(1 for job in scoped if job["state"] == "bloqueado")
        pending = sum(1 for job in scoped if job["state"] == "pendiente")
        fronts.append({
            "front": front,
            "state": state,
            "pending": pending,
            "blocked": blocked,
            "running": sum(1 for job in scoped if job["state"] in {"pensando", "ejecutando"}),
            "completed": len(done),
            "current_job": current["id"] if current else None,
            "current_job_path": current["path"] if current else None,
            "last_result": last_result[0]["result_path"] if last_result else None,
            "last_result_id": last_result[0]["id"] if last_result else None,
            "next_action": front_next_action(state, pending, blocked),
        })
    return sorted(fronts, key=lambda item: (order.get(item["state"], 9), item["front"]))


def git_state() -> dict:
    branch = run(["git", "branch", "--show-current"])
    commit = run(["git", "rev-parse", "--short", "HEAD"])
    status = run(["git", "status", "--short"])
    return {
        "branch": branch["stdout"] if branch["ok"] else "",
        "last_commit": commit["stdout"] if commit["ok"] else "",
        "dirty": bool(status["stdout"]),
        "status": status["stdout"],
    }


def build_state() -> dict:
    base = now()
    workers = collect_workers()
    jobs = collect_jobs(workers, base)
    fronts = collect_fronts(jobs)
    pending = sum(1 for job in jobs if job["state"] == "pendiente")
    blocked = sum(1 for job in jobs if job["state"] == "bloqueado")
    active = sum(1 for job in jobs if job["state"] in {"pensando", "ejecutando"})
    return {
        "updated_at": iso(base),
        "global": {
            "pending": pending,
            "active": active,
            "blocked": blocked,
            "results": sum(1 for job in jobs if job["has_result"]),
        },
        "git": git_state(),
        "workers": workers,
        "fronts": fronts,
        "jobs": sorted(jobs, key=lambda item: item.get("mtime", ""), reverse=True),
    }


def main() -> int:
    DASHBOARD.mkdir(parents=True, exist_ok=True)
    payload = build_state()
    target = DASHBOARD / "state.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

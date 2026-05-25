#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JOBS = ROOT / "jobs"
RESULTS = ROOT / "results"
CLAIMS = ROOT / "claims"
STATUS = ROOT / "status"
TMP = ROOT / "tmp"
LOCK = TMP / "personal_xh_autonomous_worker.lock"
PUBLICABLE_PHOTOS = Path.home() / "CodexPublicablePhotos"
SAFE_ASSET_DIRS = [
    Path.home() / "CodexAssets",
    Path.home() / "CodexAssetInbox",
    PUBLICABLE_PHOTOS,
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def run(cmd: list[str], *, timeout: int = 300, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(ROOT),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def write_status(status: str, message: str) -> None:
    payload = {
        "role": "personal-xh",
        "alias": "Pablo",
        "status": status,
        "front": "CODEX-OPS",
        "message": message,
        "updated_at": now_iso(),
        "host": os.uname().nodename,
        "autonomous_worker": True,
    }
    write_text(STATUS / "personal-xh.json", json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def claim_path(job_id: str) -> Path:
    return CLAIMS / f"{job_id}.json"


def result_path(job_id: str) -> Path:
    return RESULTS / f"{job_id}.result.md"


def pending_jobs() -> list[Path]:
    out: list[Path] = []
    for path in sorted(JOBS.glob("*.md"), key=lambda p: p.stat().st_mtime):
        text = read_text(path)
        if "\nassignee: personal-xh\n" not in text:
            continue
        if result_path(path.stem).exists():
            continue
        claim = read_json(claim_path(path.stem))
        if claim and claim.get("assignee") != "personal-xh":
            continue
        out.append(path)
    return out


def snapshot_publicable_photos() -> dict[str, dict[str, int | float]]:
    """Track accidental source edits without hashing a large photo library."""
    if not PUBLICABLE_PHOTOS.exists():
        return {}
    snapshot: dict[str, dict[str, int | float]] = {}
    for path in PUBLICABLE_PHOTOS.rglob("*"):
        if not path.is_file():
            continue
        try:
            stat = path.stat()
            snapshot[str(path.relative_to(PUBLICABLE_PHOTOS))] = {
                "size": stat.st_size,
                "mtime": stat.st_mtime,
            }
        except OSError:
            continue
    return snapshot


def publicable_photo_changes(before: dict[str, dict[str, int | float]]) -> list[str]:
    after = snapshot_publicable_photos()
    changes: list[str] = []
    for rel, meta in before.items():
        if rel not in after:
            changes.append(f"deleted: {rel}")
        elif after[rel] != meta:
            changes.append(f"modified: {rel}")
    for rel in after:
        if rel not in before:
            changes.append(f"created: {rel}")
    return changes[:50]


def git_sync() -> tuple[bool, str]:
    fetch = run(["git", "fetch", "origin", "main"], timeout=120)
    pull = run(["git", "pull", "--ff-only"], timeout=120)
    ok = fetch.returncode == 0 and pull.returncode == 0
    return ok, "\n".join([
        "$ git fetch origin main",
        fetch.stdout,
        fetch.stderr,
        "$ git pull --ff-only",
        pull.stdout,
        pull.stderr,
    ]).strip()


def claim_job(job_id: str) -> bool:
    claim = run(
        ["python3", "scripts/bridgectl.py", "claim", "--job-id", job_id, "--assignee", "personal-xh"],
        timeout=60,
    )
    if claim.returncode != 0:
        return False
    payload = json.loads(claim.stdout)
    return bool(payload.get("ok"))


def safe_env() -> dict[str, str]:
    env = os.environ.copy()
    runtime = TMP / "pablo-runtime"
    cache = TMP / "pablo-cache"
    for path in [runtime, cache, cache / "uv", cache / "pip", cache / "hf", cache / "torch"]:
        path.mkdir(parents=True, exist_ok=True)
    env["PATH"] = ":".join([
        str(Path.home() / ".local/bin"),
        "/opt/homebrew/bin",
        "/usr/local/bin",
        "/usr/bin",
        "/bin",
        "/usr/sbin",
        "/sbin",
        env.get("PATH", ""),
    ])
    env["UV_CACHE_DIR"] = str(cache / "uv")
    env["PIP_CACHE_DIR"] = str(cache / "pip")
    env["HF_HOME"] = str(cache / "hf")
    env["HUGGINGFACE_HUB_CACHE"] = str(cache / "hf" / "hub")
    env["TORCH_HOME"] = str(cache / "torch")
    env["XDG_CACHE_HOME"] = str(cache)
    env["PABLO_RUNTIME_DIR"] = str(runtime)
    return env


def build_prompt(job_path: Path) -> str:
    job_id = job_path.stem
    profile = ROOT / "docs" / "pablo_minimal_authorization_profile.md"
    worker_doc = ROOT / "WORKER_PERSONAL_XH.md"
    profile_text = read_text(profile) if profile.exists() else ""
    worker_text = read_text(worker_doc) if worker_doc.exists() else ""
    return f"""Usted es Pablo/personal-xh, subagente de alto razonamiento del Codex orquestador.

Modo actual: worker autonomo no interactivo.

Reglas de ejecucion:
- No pedir autorizacion humana para comandos locales permitidos; esta sesion corre con approval=never.
- Usar solo el repo actual y, si existen, /Users/carloszanardi/CodexAssets, /Users/carloszanardi/CodexAssetInbox y /Users/carloszanardi/CodexPublicablePhotos.
- /Users/carloszanardi/CodexPublicablePhotos es fuente de fotos publicables: solo lectura operativa. No borrar, no renombrar, no corregir, no sobrescribir originales. Si necesita editar, copiar antes a CodexAssetInbox o context/asset_packs.
- No abrir Photos, iCloud, Drive, Downloads, Desktop, Pictures, Library ni bibliotecas completas.
- No usar Gmail, Telegram, Calendar, Drive, publicaciones, compras ni contactos externos.
- No imprimir secretos ni credenciales.
- Puede instalar dependencias open source y descargar modelos publicos SOLO dentro de tmp/pablo-runtime o tmp/pablo-cache del repo.
- Variables ya preparadas: UV_CACHE_DIR, PIP_CACHE_DIR, HF_HOME, TORCH_HOME, XDG_CACHE_HOME, PABLO_RUNTIME_DIR dentro del repo.
- Si algo pide permisos fuera de esas rutas, no lo solicite: busque alternativa local o reporte bloqueo preciso.
- Si genera audios/imagenes de prueba pequenos, guardelos en context/asset_packs/<job_id>/.
- Antes de commitear, correr scripts/secret_scan.py sobre archivos modificados relevantes.
- Escribir el resultado principal en results/{job_id}.result.md.
- Actualizar status/personal-xh.json.
- Hacer git add/commit/push de claims, results, status y context/asset_packs si corresponde.
- La decision final queda siempre en Codex orquestador.

Documento worker:
{worker_text}

Perfil de autorizacion:
{profile_text}

JOB A PROCESAR:
{read_text(job_path)}
"""


def run_codex(job_path: Path, args: argparse.Namespace) -> tuple[int, str, str, Path]:
    codex = shutil.which("codex", path=safe_env().get("PATH"))
    if not codex:
        return 127, "", "codex CLI not found in PATH", TMP / f"{job_path.stem}.last-message.md"

    last_message = TMP / f"{job_path.stem}.last-message.md"
    cmd = [
        codex,
        "-a",
        "never",
        "--search",
        "exec",
        "-C",
        str(ROOT),
        "-m",
        args.model,
        "-s",
        "workspace-write",
        "--add-dir",
        str(ROOT),
    ]
    for extra in SAFE_ASSET_DIRS:
        if extra.exists():
            cmd.extend(["--add-dir", str(extra)])
    cmd.extend([
        "-o",
        str(last_message),
        "-",
    ])

    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        env=safe_env(),
        input=build_prompt(job_path),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=args.timeout,
        check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr, last_message


def fallback_result(job_id: str, code: int, stdout: str, stderr: str, last_message: Path) -> None:
    last = read_text(last_message) if last_message.exists() else ""
    body = f"""---
id: {job_id}
job_id: {job_id}
created_at: {now_iso()}
created_by: personal-xh-autonomous-worker
worker: personal-xh
status: failed_or_incomplete
no_external_actions: true
no_secrets: true
---

# Resultado incompleto - {job_id}

El worker autonomo intento procesar el job, pero no encontro un result final creado por Codex.

## Diagnostico

- exit_code: `{code}`
- last_message_path: `{last_message}`

## stdout

```text
{stdout[-4000:]}
```

## stderr

```text
{stderr[-4000:]}
```

## last_message

```text
{last[-4000:]}
```
"""
    write_text(result_path(job_id), body)


def commit_and_push(message: str) -> None:
    run(["git", "add", "claims", "results", "status", "context/asset_packs"], timeout=120)
    status = run(["git", "status", "--short"], timeout=60)
    if not status.stdout.strip():
        return
    run(["python3", "scripts/secret_scan.py", "claims", "results", "status", "context/asset_packs"], timeout=180)
    run(["git", "add", "claims", "results", "status", "context/asset_packs"], timeout=120)
    commit = run(["git", "commit", "-m", message], timeout=120)
    if commit.returncode == 0:
        run(["git", "push", "origin", "main"], timeout=180)


def process_once(args: argparse.Namespace) -> int:
    TMP.mkdir(parents=True, exist_ok=True)
    with LOCK.open("w", encoding="utf-8") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 0

        ok, sync_log = git_sync()
        if not ok:
            write_status("blocked_git_sync", sync_log[-1000:])
            commit_and_push("Report personal-xh git sync block")
            return 1

        jobs = pending_jobs()
        if not jobs:
            write_status("available", "Pablo autonomo sin jobs pendientes; listo para trabajo.")
            commit_and_push("Signal personal-xh autonomous idle")
            return 0

        job_path = jobs[0]
        job_id = job_path.stem
        if not claim_job(job_id):
            write_status("blocked_claim", f"No pude reclamar {job_id}.")
            commit_and_push(f"Report claim block {job_id}")
            return 1

        write_status("working", f"Procesando job autonomo {job_id}.")
        commit_and_push(f"Claim {job_id}")

        photo_snapshot = snapshot_publicable_photos()
        code, stdout, stderr, last_message = run_codex(job_path, args)
        if code != 0 or not result_path(job_id).exists():
            fallback_result(job_id, code, stdout, stderr, last_message)
        photo_changes = publicable_photo_changes(photo_snapshot)
        if photo_changes:
            alert = "\n".join(f"- {change}" for change in photo_changes)
            write_text(
                RESULTS / f"{job_id}.asset-source-alert.md",
                f"""---
id: {job_id}-asset-source-alert
job_id: {job_id}
created_at: {now_iso()}
created_by: personal-xh-autonomous-worker
worker: personal-xh
status: source_folder_changed
no_external_actions: true
---

# Alerta de carpeta de fotos publicables

Se detectaron cambios dentro de `/Users/carloszanardi/CodexPublicablePhotos` durante la ejecucion. Esa carpeta debe usarse como fuente, no como destino de edicion.

## Cambios detectados

{alert}
""",
            )

        write_status("available", f"Procesado {job_id}; resultado disponible para orquestador.")
        commit_and_push(f"Complete {job_id}")
        return 0 if result_path(job_id).exists() else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Worker autonomo seguro para Pablo/personal-xh.")
    parser.add_argument("--once", action="store_true", help="Procesar un solo job pendiente.")
    parser.add_argument("--timeout", type=int, default=int(os.environ.get("PABLO_CODEX_TIMEOUT_SEC", "7200")))
    parser.add_argument("--model", default=os.environ.get("PABLO_CODEX_MODEL", "gpt-5.5"))
    args = parser.parse_args()
    return process_once(args)


if __name__ == "__main__":
    raise SystemExit(main())

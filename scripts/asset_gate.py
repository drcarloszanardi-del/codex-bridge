#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MEDIA_SUFFIXES = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".gif", ".mp4", ".mov", ".m4v", ".avi"}
VIDEO_SUFFIXES = {".mp4", ".mov", ".m4v", ".avi"}
FORBIDDEN_MARKERS = (
    "Photos Library.photoslibrary",
    "/Pictures/",
    "/Downloads/",
    "/Desktop/",
    "/Library/",
    "Mobile Documents",
    "CloudStorage",
    "Google Drive",
    "DriveFS",
    ".icloud",
)


def default_allowed_roots() -> list[Path]:
    raw = os.environ.get("CODEX_ALLOWED_ASSET_ROOTS", "")
    if raw.strip():
        return [Path(item).expanduser().resolve() for item in raw.split(os.pathsep) if item.strip()]
    return [
        Path("/Users/carloszanardi/CodexAssetInbox").resolve(),
        Path("/Users/carloszanardi/CodexAssets").resolve(),
    ]


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def has_forbidden_marker(path: Path) -> bool:
    text = str(path)
    return any(marker in text for marker in FORBIDDEN_MARKERS)


def validate_authorized_root(path: Path, allowed_roots: list[Path]) -> list[str]:
    resolved = path.expanduser().resolve()
    errors: list[str] = []
    if has_forbidden_marker(resolved):
        errors.append(f"authorized_root touches forbidden personal library area: {resolved}")
    if not any(is_relative_to(resolved, root) for root in allowed_roots):
        allowed = ", ".join(str(root) for root in allowed_roots)
        errors.append(f"authorized_root is outside allowed roots: {resolved} (allowed: {allowed})")
    return errors


def load_manifest(path: Path) -> dict[str, Any]:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if path.suffix.lower() in {".tsv", ".csv"}:
        delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
        with path.open("r", encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh, delimiter=delimiter))
        root = rows[0].get("authorized_root", "") if rows else ""
        return {"schema": "codex_asset_manifest.v1", "authorized_root": root, "items": rows}
    raise ValueError(f"unsupported manifest format: {path}")


def validate_manifest(path: Path, check_exists: bool = False) -> list[str]:
    manifest = load_manifest(path)
    allowed_roots = default_allowed_roots()
    errors: list[str] = []
    authorized_root_raw = str(manifest.get("authorized_root") or manifest.get("root") or "").strip()
    if not authorized_root_raw:
        errors.append("manifest missing authorized_root")
        return errors
    authorized_root = Path(authorized_root_raw).expanduser().resolve()
    errors.extend(validate_authorized_root(authorized_root, allowed_roots))

    items = manifest.get("items")
    if not isinstance(items, list) or not items:
        errors.append("manifest has no items")
        return errors

    for idx, item in enumerate(items, 1):
        if not isinstance(item, dict):
            errors.append(f"item {idx}: not an object")
            continue
        rel_raw = str(item.get("file") or item.get("relative_path") or "").strip()
        if not rel_raw:
            errors.append(f"item {idx}: missing relative file")
            continue
        rel = Path(rel_raw)
        if rel.is_absolute():
            errors.append(f"item {idx}: file must be relative, got absolute path {rel_raw}")
            continue
        if ".." in rel.parts:
            errors.append(f"item {idx}: file escapes with '..': {rel_raw}")
            continue
        resolved = (authorized_root / rel).resolve()
        if not is_relative_to(resolved, authorized_root):
            errors.append(f"item {idx}: resolved file escapes authorized_root: {rel_raw}")
        if has_forbidden_marker(resolved):
            errors.append(f"item {idx}: forbidden path marker: {resolved}")
        sensitivity = str(item.get("sensitivity") or item.get("privacy_status") or "").lower()
        if sensitivity in {"patient_identifiable", "document_identifiable"}:
            errors.append(f"item {idx}: identifiable sensitive material cannot be used autonomously: {rel_raw}")
        if check_exists and not resolved.exists():
            errors.append(f"item {idx}: file does not exist: {resolved}")
    return errors


def scan_bridge(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        suffix = path.suffix.lower()
        if suffix not in MEDIA_SUFFIXES:
            continue
        rel = path.relative_to(root)
        size = path.stat().st_size
        if suffix in VIDEO_SUFFIXES:
            errors.append(f"video media must not be committed to bridge: {rel}")
        elif size > 800_000:
            errors.append(f"large image likely original/private media: {rel} ({size} bytes)")
        elif rel.parts and rel.parts[0] in {"jobs", "results", "claims", "status"}:
            errors.append(f"media file forbidden in bridge control folder: {rel}")
    return errors


def init_root(path: Path) -> dict[str, Any]:
    allowed = default_allowed_roots()
    errors = validate_authorized_root(path, allowed)
    if errors:
        return {"ok": False, "errors": errors}
    root = path.expanduser().resolve()
    for name in ["original", "selected", "rejects_privacy", "working", "renders", "qa"]:
        (root / name).mkdir(parents=True, exist_ok=True)
    policy = {
        "schema": "codex_asset_policy.v1",
        "authorized_root": str(root),
        "no_photos_library": True,
        "no_bridge_original_upload": True,
        "no_external_actions": True,
        "public_use_requires_doctor_approval": True,
    }
    (root / "asset_policy.json").write_text(json.dumps(policy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "README_PRIVACY.md").write_text(
        "# Codex Asset Inbox\n\n"
        "- Solo material autorizado para reels/presentaciones.\n"
        "- No agregar pacientes, historias clinicas, estudios con datos ni pantallas identificables.\n"
        "- Pablo puede clasificar y renderizar localmente, pero no subir originales al bridge.\n"
        "- Cualquier publicacion externa requiere aprobacion del Doctor.\n",
        encoding="utf-8",
    )
    return {"ok": True, "root": str(root), "created": ["original", "selected", "rejects_privacy", "working", "renders", "qa"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate assets for Pablo without exposing personal photo libraries.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    init = sub.add_parser("init-root")
    init.add_argument("--root", required=True)
    validate = sub.add_parser("validate-manifest")
    validate.add_argument("manifest")
    validate.add_argument("--check-exists", action="store_true")
    scan = sub.add_parser("scan-bridge")
    scan.add_argument("--root", default=str(ROOT))
    args = parser.parse_args()

    if args.cmd == "init-root":
        out = init_root(Path(args.root))
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if out.get("ok") else 1
    if args.cmd == "validate-manifest":
        errors = validate_manifest(Path(args.manifest), check_exists=args.check_exists)
    elif args.cmd == "scan-bridge":
        errors = scan_bridge(Path(args.root).resolve())
    else:
        raise AssertionError(args.cmd)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("asset_gate: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__", "secrets", "private"}
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".gz"}

PATTERNS = [
    ("private-key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("bearer-token", re.compile(r"(?i)\bauthorization\s*:\s*bearer\s+[A-Za-z0-9._~+/=-]{16,}")),
    ("github-token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b")),
    ("github-pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    (
        "assigned-secret",
        re.compile(
            r"(?i)\b(?:api[_-]?key|secret[_-]?key|access[_-]?token|refresh[_-]?token|bridge[_-]?token|password|passwd)\b"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{16,}"
        ),
    ),
]


def candidate_files(paths: list[str]) -> list[Path]:
    if paths:
        out: list[Path] = []
        for item in paths:
            path = Path(item)
            if path.is_dir():
                out.extend(p for p in path.rglob("*") if p.is_file())
            else:
                out.append(path)
        return out

    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel_parts = set(path.relative_to(ROOT).parts)
        if rel_parts & SKIP_DIRS:
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        files.append(path)
    return files


def scan_file(path: Path) -> list[tuple[str, int, str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    findings: list[tuple[str, int, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for name, pattern in PATTERNS:
            if pattern.search(line):
                findings.append((name, lineno, line.strip()[:160]))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Simple secret scanner for codex-bridge.")
    parser.add_argument("paths", nargs="*", help="Optional files or directories to scan.")
    args = parser.parse_args()

    findings = []
    for path in candidate_files(args.paths):
        if not path.exists() or not path.is_file():
            continue
        rel_parts = set(path.relative_to(ROOT).parts) if path.is_relative_to(ROOT) else set()
        if rel_parts & SKIP_DIRS:
            continue
        for name, lineno, excerpt in scan_file(path):
            rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
            findings.append((str(rel), name, lineno, excerpt))

    if findings:
        for rel, name, lineno, excerpt in findings:
            print(f"{rel}:{lineno}: {name}: {excerpt}", file=sys.stderr)
        return 1
    print("secret_scan: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

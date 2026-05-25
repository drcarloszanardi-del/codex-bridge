#!/usr/bin/env python3
"""Validate bridge result files before the orchestrator trusts them."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTION_ALIASES = {
    "summary": ("summary", "summary_honesto", "resumen", "resumen_honesto"),
    "recommendation": ("recommendation", "recomendacion"),
    "confidence": ("confidence", "confianza"),
    "evidence_paths": ("evidence_paths", "evidencia", "evidence", "paths"),
}


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def headings(text: str) -> set[str]:
    found: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}#{2,6}\s+(.+?)\s*$", line)
        if match:
            found.add(normalize(match.group(1)))
    return found


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    found = headings(text)
    errors: list[str] = []
    for section, aliases in REQUIRED_SECTION_ALIASES.items():
        if not any(alias in found for alias in aliases):
            errors.append(f"missing required section: {section}")
    if not any(section in found for section in ("coverage_table", "source_counts", "source_counts_or_coverage_table")):
        errors.append("missing coverage section: coverage_table or source_counts")
    if not any(section in found for section in ("attempted_routes", "exclusion_log", "riesgos", "risks_limits")):
        errors.append("missing route/limit section: attempted_routes, exclusion_log or risks/limits")
    if not re.search(r"`[^`]+`|/Users/|jobs/|results/|context/|state/|http", text):
        errors.append("missing concrete evidence path or URL-like evidence")
    if re.search(r"\bno pude\b", text.lower()) and not any(
        section in found
        for section in ("attempted_routes", "next_action_if_blocked", "exclusion_log", "risks_limits")
    ):
        errors.append("contains 'no pude' without attempted_routes/limits/next_action evidence")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", nargs="+", help="Result markdown files to validate")
    args = parser.parse_args()

    failed = False
    for raw in args.results:
        path = Path(raw)
        if not path.exists():
            print(f"{path}: missing file", file=sys.stderr)
            failed = True
            continue
        errors = validate(path)
        if errors:
            failed = True
            print(f"{path}: FAIL")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"{path}: OK")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

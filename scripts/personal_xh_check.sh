#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

git pull --ff-only
python3 scripts/bridgectl.py list-jobs --pending
git status --short

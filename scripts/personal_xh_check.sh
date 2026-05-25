#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

git pull --rebase
python3 scripts/bridgectl.py list-jobs --pending --assignee personal-xh
git status --short

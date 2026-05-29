#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -f BRIDGE_SUSPENDED ]]; then
  echo "Bridge suspended: BRIDGE_SUSPENDED exists. No jobs will be checked."
  exit 0
fi

git pull --rebase
python3 scripts/bridgectl.py list-jobs --pending --assignee personal-xh --available
git status --short

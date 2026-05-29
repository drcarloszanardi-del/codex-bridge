#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -f BRIDGE_SUSPENDED ]]; then
  echo "Bridge suspended: BRIDGE_SUSPENDED exists. Poll loop not started."
  exit 0
fi

interval="${1:-300}"
log_path="${CODEX_BRIDGE_LOG:-tmp/personal_xh_poll.log}"
mkdir -p "$(dirname "$log_path")"

while true; do
  {
    date "+%Y-%m-%dT%H:%M:%S%z"
    ./scripts/personal_xh_check.sh
    echo
  } >> "$log_path" 2>&1
  sleep "$interval"
done

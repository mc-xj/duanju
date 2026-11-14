#!/usr/bin/env bash
# Restore project tools without modifying global Python or agent settings.
set -euo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$project_root"
python3 -m venv .venv-tools
.venv-tools/bin/python -m pip install -r .tools/requirements.lock.txt
.venv-tools/bin/python -m pip check
.venv-tools/bin/python .agents/skills/ppt-master/scripts/attribution_guard.py

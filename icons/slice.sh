#!/bin/bash
# Wrapper: slice a Gemini grid into icons via slice.py (Pillow), then rebuild the manifest.
# Usage: ./slice.sh <batch-number> <image-file>
set -e
cd "$(dirname "$0")"
[ $# -eq 2 ] || { echo "usage: $0 <batch-number> <image>"; exit 1; }
PY="${SLICE_PYTHON:-python3}"
"${PY}" -c "import PIL" 2>/dev/null || { echo "needs Pillow: pip install pillow (or set SLICE_PYTHON to a venv python)"; exit 1; }
"${PY}" slice.py "${1}" "${2}"
./make-manifest.sh

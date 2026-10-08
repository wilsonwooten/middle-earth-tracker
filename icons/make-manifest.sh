#!/bin/bash
# Rebuild icons/manifest.js from the PNGs present, using CHARACTERS.tsv for the name -> file mapping.
set -e
cd "$(dirname "$0")"
{
  echo "window.ICONS = {"
  tail -n +2 CHARACTERS.tsv | while IFS=$'\t' read -r name file books; do
    if [ -f "$file" ]; then printf '  "%s": "%s",\n' "$name" "$file"; fi
  done
  echo "};"
} > manifest.js
echo "manifest.js: $(grep -c png manifest.js) icons"

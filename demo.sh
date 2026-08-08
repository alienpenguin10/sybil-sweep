#!/usr/bin/env bash
# Amin demo runner — detect → React+viem dashboard (HTML fallback if npm missing).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "== Sybil Sweep · Amin seam =="
python3 detector/detector.py
echo

python3 - <<'PY'
import json
from pathlib import Path
att = json.loads(Path("data/attestations.json").read_text())
g = json.loads(Path("dashboard/public/graph_data.json").read_text())
m = g["metrics"]
print("DEMO BEATS (you speak):")
print(f"  2 · Detect  — \"{m['claimants']} wallets in the claimant list.\"")
print(f"  3 · Show    — React graph · recall {(m['recall']*100):.1f}% · {m['flagged']} farm wallets.")
print(f"  4 · Enforce — {len(att['attestations'])} cluster(s) · viem reads registry")
if att["attestations"]:
    a = att["attestations"][0]
    print(f"             sample farm wallet: {a['members'][0]}")
print()
print("Preferred: cd dashboard && npm run dev")
print("Fallback:  open dashboard/public/fallback.html")
print("After deploy: python3 script/set_registry.py 0xRegistry 0xAirdrop")
PY

cd "$ROOT/dashboard"
if command -v npm >/dev/null 2>&1; then
  if [ ! -d node_modules ]; then
    echo "Installing dashboard deps…"
    npm install
  fi
  echo "Starting Vite at http://localhost:5173 …"
  npm run dev
else
  echo "npm not found — opening HTML fallback"
  DASH="$ROOT/dashboard/public/fallback.html"
  if command -v open >/dev/null 2>&1; then
    open "$DASH"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$DASH"
  else
    echo "Open: $DASH"
  fi
fi

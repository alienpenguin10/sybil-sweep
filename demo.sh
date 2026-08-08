#!/usr/bin/env bash
# Amin demo runner — detect → open static fallback (React+viem is primary UI).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "== Sybil Sweep · Amin seam =="
echo "Primary UI: React + viem under dashboard/ (npm run dev)"
echo "This script opens the static HTML fallback for projector emergencies."
python3 detector/detector.py
echo

python3 - <<'PY'
import json
from pathlib import Path
att = json.loads(Path("data/attestations.json").read_text())
g = json.loads(Path("dashboard/graph_data.js").read_text().split("=", 1)[1].strip().rstrip(";"))
m = g["metrics"]
print("DEMO BEATS (you speak):")
print(f"  2 · Detect  — \"{m['claimants']} wallets in the claimant list.\"")
print(f"  3 · Show    — React graph · recall {(m['recall']*100):.1f}% · {m['flagged']} farm wallets.")
print(f"  4 · Enforce — {len(att['attestations'])} cluster(s) in data/attestations.json · viem reads registry")
if att["attestations"]:
    a = att["attestations"][0]
    print(f"             sample farm wallet: {a['members'][0]}")
print()
print("Preferred: cd dashboard && npm run dev")
print("Fallback:  open dashboard/dashboard.html")
print("After Varnie deploys: python3 script/set_registry.py 0xRegistry 0xAirdrop")
PY

DASH="$ROOT/dashboard/dashboard.html"
if command -v open >/dev/null 2>&1; then
  open "$DASH"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$DASH"
else
  echo "Open static fallback: $DASH"
fi

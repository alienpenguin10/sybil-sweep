#!/usr/bin/env bash
# Amin demo runner — detect → open projector dashboard → print beat lines.
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
g = json.loads(Path("dashboard/graph_data.js").read_text().split("=", 1)[1].strip().rstrip(";"))
m = g["metrics"]
print("DEMO BEATS (you speak):")
print(f"  2 · Detect  — \"{m['claimants']} wallets in the claimant list.\"")
print(f"  3 · Show    — point at red webs · recall {(m['recall']*100):.1f}% · {m['flagged']} farm wallets.")
print(f"  4 · Enforce — {len(att['attestations'])} cluster(s) ready in data/attestations.json")
if att["attestations"]:
    a = att["attestations"][0]
    print(f"             sample farm wallet: {a['members'][0]}")
print()
print("Keys in dashboard: 1–4 beats · R re-probe chain")
print("After Varnie deploys: python3 script/set_registry.py 0xRegistry 0xAirdrop")
PY

DASH="$ROOT/dashboard/dashboard.html"
if command -v open >/dev/null 2>&1; then
  open "$DASH"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$DASH"
else
  echo "Open dashboard in a browser: $DASH"
fi

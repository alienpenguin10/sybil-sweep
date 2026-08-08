#!/usr/bin/env python3
"""Broadcast attestations.json → SybilRegistry.attestCluster (Amin/Varnie seam).

Requires: cast on PATH, PRIVATE_KEY, SYBIL_REGISTRY, MONAD_RPC in env.
Usage:
  python3 script/attest.py --dry-run
  python3 script/attest.py --limit 1
  python3 script/attest.py
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATT_PATH = ROOT / "data" / "attestations.json"
STATUS_PATH = ROOT / "data" / "onchain_status.json"


def load_dotenv() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def main() -> int:
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="Max clusters (0=all)")
    args = ap.parse_args()

    rpc = os.environ.get("MONAD_RPC", "https://testnet-rpc.monad.xyz")
    pk = os.environ.get("PRIVATE_KEY")
    registry = os.environ.get("SYBIL_REGISTRY")
    if not args.dry_run and (not pk or not registry):
        print("Need PRIVATE_KEY and SYBIL_REGISTRY (env or .env)", file=sys.stderr)
        return 1

    data = json.loads(ATT_PATH.read_text())
    atts = data["attestations"]
    if args.limit:
        atts = atts[: args.limit]

    published = []
    for att in atts:
        members = att["members"]
        arr = "[" + ",".join(members) + "]"
        cmd = [
            "cast",
            "send",
            registry or "0x0",
            "attestCluster(uint32,address[],uint16,address,uint32,bytes32)",
            str(att["clusterId"]),
            arr,
            str(att["confidenceBps"]),
            att["funder"],
            str(att["fundingWindowSecs"]),
            att["evidenceHash"],
            "--rpc-url",
            rpc,
            "--private-key",
            pk or ("0x" + "1" * 64),
        ]
        print(
            f"cluster {att['clusterId']} size={att['size']} "
            f"conf={att['confidenceBps']} sample={members[0][:10]}…"
        )
        if args.dry_run:
            print("  dry-run:", " ".join(cmd[:6]), "...")
            published.append({"clusterId": att["clusterId"], "tx": None, "dryRun": True})
            continue
        out = subprocess.check_output(cmd, text=True)
        print(out.strip())
        published.append(
            {
                "clusterId": att["clusterId"],
                "size": att["size"],
                "sampleMember": members[0],
                "confidenceBps": att["confidenceBps"],
                "raw": out.strip(),
            }
        )

    STATUS_PATH.write_text(
        json.dumps(
            {
                "updatedAt": int(time.time()),
                "registry": registry,
                "rpc": rpc,
                "published": published,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {STATUS_PATH.name} ({len(published)} cluster(s))")
    if registry and not args.dry_run:
        print("Next: python3 script/set_registry.py", registry)
        print("Then: cd dashboard && npm run dev  (viem reads registry)")
        print("Fallback: open dashboard/dashboard.html and press R")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

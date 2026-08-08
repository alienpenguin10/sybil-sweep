#!/usr/bin/env python3
"""Broadcast attestations.json to SybilRegistry via cast (Foundry).

Requires: cast, PRIVATE_KEY, SYBIL_REGISTRY, MONAD_RPC in env.
Usage:
  python3 script/attest.py
  python3 script/attest.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATT_PATH = ROOT / "attestations.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="Max clusters (0=all)")
    args = ap.parse_args()

    rpc = os.environ.get("MONAD_RPC", "https://testnet-rpc.monad.xyz")
    pk = os.environ.get("PRIVATE_KEY")
    registry = os.environ.get("SYBIL_REGISTRY")
    if not args.dry_run and (not pk or not registry):
        print("Need PRIVATE_KEY and SYBIL_REGISTRY in env", file=sys.stderr)
        return 1

    data = json.loads(ATT_PATH.read_text())
    atts = data["attestations"]
    if args.limit:
        atts = atts[: args.limit]

    for att in atts:
        members = att["members"]
        # cast array syntax: [addr1,addr2]
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
            pk or "0x0",
        ]
        print(f"cluster {att['clusterId']} size={att['size']} conf={att['confidenceBps']}")
        if args.dry_run:
            print(" ", " ".join(cmd[:8]), "...")
            continue
        subprocess.check_call(cmd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

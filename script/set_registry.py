#!/usr/bin/env python3
"""Write deployed addresses into config.js (Amin seam).

Usage:
  SYBIL_REGISTRY=0x... SYBIL_AIRDROP=0x... python3 script/set_registry.py
  python3 script/set_registry.py 0xRegistry [0xAirdrop]
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "dashboard" / "config.js"


def main() -> int:
    registry = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SYBIL_REGISTRY", "")).strip()
    airdrop = (sys.argv[2] if len(sys.argv) > 2 else os.environ.get("SYBIL_AIRDROP", "")).strip()
    if not registry:
        print("Usage: python3 script/set_registry.py 0xRegistry [0xAirdrop]", file=sys.stderr)
        return 1

    rpc = os.environ.get("MONAD_RPC", "https://testnet-rpc.monad.xyz")
    explorer = os.environ.get("MONAD_EXPLORER", "https://testnet.monadvision.com")

    text = f"""// Sybil Sweep — dashboard config (React/viem + legacy HTML).
// Prefer env / Vite config in the React app; this file feeds the HTML fallback.
window.SYBIL_CONFIG = {{
  chainId: 10143,
  chainName: "Monad Testnet",
  rpcUrl: {json.dumps(rpc)},
  explorerUrl: {json.dumps(explorer)},
  registry: {json.dumps(registry)},
  airdrop: {json.dumps(airdrop)},
  forceOffline: false,
}};
"""
    CONFIG.write_text(text, encoding="utf-8")
    print(f"Updated {CONFIG.name}")
    print(f"  registry: {registry}")
    if airdrop:
        print(f"  airdrop:  {airdrop}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

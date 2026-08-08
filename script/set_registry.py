#!/usr/bin/env python3
"""Write deployed addresses into Vite .env + HTML fallback config (Amin seam).

Usage:
  SYBIL_REGISTRY=0x... SYBIL_AIRDROP=0x... python3 script/set_registry.py
  python3 script/set_registry.py 0xRegistry [0xAirdrop]
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASH = ROOT / "dashboard"
PUBLIC_CONFIG = DASH / "public" / "config.js"
VITE_ENV = DASH / ".env"


def main() -> int:
    registry = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SYBIL_REGISTRY", "")).strip()
    airdrop = (sys.argv[2] if len(sys.argv) > 2 else os.environ.get("SYBIL_AIRDROP", "")).strip()
    if not registry:
        print("Usage: python3 script/set_registry.py 0xRegistry [0xAirdrop]", file=sys.stderr)
        return 1

    rpc = os.environ.get("MONAD_RPC", "https://testnet-rpc.monad.xyz")
    explorer = os.environ.get("MONAD_EXPLORER", "https://testnet.monadvision.com")
    chain_id = os.environ.get("CHAIN_ID", "10143")

    DASH.mkdir(parents=True, exist_ok=True)
    (DASH / "public").mkdir(parents=True, exist_ok=True)

    js = f"""// Sybil Sweep — HTML fallback config (React uses dashboard/.env via Vite).
window.SYBIL_CONFIG = {{
  chainId: {int(chain_id)},
  chainName: "Monad Testnet",
  rpcUrl: {json.dumps(rpc)},
  explorerUrl: {json.dumps(explorer)},
  registry: {json.dumps(registry)},
  airdrop: {json.dumps(airdrop)},
  forceOffline: false,
}};
"""
    PUBLIC_CONFIG.write_text(js, encoding="utf-8")

    vite = f"""VITE_CHAIN_ID={chain_id}
VITE_MONAD_RPC={rpc}
VITE_EXPLORER_URL={explorer}
VITE_SYBIL_REGISTRY={registry}
VITE_SYBIL_AIRDROP={airdrop}
"""
    VITE_ENV.write_text(vite, encoding="utf-8")

    print(f"Updated {PUBLIC_CONFIG.relative_to(ROOT)}")
    print(f"Updated {VITE_ENV.relative_to(ROOT)}")
    print(f"  registry: {registry}")
    if airdrop:
        print(f"  airdrop:  {airdrop}")
    print("Restart `npm run dev` if the Vite server is already running.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

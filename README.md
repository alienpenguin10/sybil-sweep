# Sybil Sweep

Catch airdrop farms from on-chain fingerprints, show them as a red web, and **write the
verdict onto Monad** so the next airdrop blocks them automatically.

**Detect → show → enforce.**

## Quick start (offline demo)

```bash
./demo.sh             # Amin: detect + open projector dashboard + beat lines
# or:
python3 sybil_detector.py
open dashboard.html   # zero CDN deps; works offline
```

After deploy, wire the Amin seam:

```bash
python3 script/set_registry.py 0xRegistry 0xAirdrop
python3 script/attest.py          # full cluster dump (after AttestOne smoke)
# dashboard → press R to probe isSybil on-chain
```

## Monad testnet

| | |
|--|--|
| Chain ID | `10143` |
| RPC | `https://testnet-rpc.monad.xyz` |
| Explorer | https://testnet.monadvision.com |
| Faucet | https://faucet.monad.xyz |

Verify live at [docs.monad.xyz](https://docs.monad.xyz/developer-essentials/testnet) if something fails.

## On-chain critical path (Varnie)

```bash
# Fresh clone only — required before forge build (lib/ is gitignored):
git clone --depth 1 https://github.com/foundry-rs/forge-std lib/forge-std
```

1. Copy `.env.example` → `.env`, add `PRIVATE_KEY`, faucet MON (≥0.1 + gas).
2. `source .env` — confirm `MONAD_RPC` + chain ID `10143` vs docs.
3. Deploy (sets claim to **0.01 MON** and funds airdrop with **0.1 MON**):

```bash
forge script script/Deploy.s.sol:Deploy --rpc-url $MONAD_RPC --broadcast
```

4. Save both logged addresses into `.env` as `SYBIL_REGISTRY=` and `SYBIL_AIRDROP=`.
5. Set `MEMBER` / `CLUSTER_ID` / … in `.env`, then flag one wallet:

```bash
# Single-wallet smoke (critical path) — contract name AttestOne in AttestOne.s.sol
forge script script/AttestOne.s.sol:AttestOne --rpc-url $MONAD_RPC --broadcast
```

6. Beat-4 contrast on explorer:
   - Flagged wallet → `Airdrop.claim()` → **`SybilBlocked` revert** (works even if unfunded; we fund anyway for contrast)
   - Honest wallet → `claim()` → **gets paid 0.01 MON**
7. Full cluster dump (not the Solidity file):

```bash
python3 script/attest.py
```

**Two attest paths — do not confuse:**

| Goal | Command |
|------|---------|
| Flag one wallet (smoke / reject proof) | `forge script script/AttestOne.s.sol:AttestOne --broadcast` |
| Publish all clusters from `attestations.json` | `python3 script/attest.py` |

## Layout

```
sybil_detector.py       # stdlib detector → graph_data.js + attestations.json
dashboard.html          # offline force graph + Enforce panel
config.js               # registry/airdrop addresses for dashboard probe
contracts/              # SybilRegistry + demo Airdrop
script/
  Deploy.s.sol          # deploy + fund 0.1 + setClaimAmount 0.01
  AttestOne.s.sol       # single-wallet smoke (contract AttestOne)
  attest.py             # full cluster dump
  set_registry.py       # write addresses into config.js
seed_patterns.md
memory-bank/
```

## Team

- **Varnie** — deploy, reject proof, AttestOne, then attest.py
- **Murtuza** — hard cases + pitch
- **Amin** — seam + projector demo

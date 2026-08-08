# Sybil Sweep

Catch airdrop farms from on-chain fingerprints, show them as a red web, and **write the
verdict onto Monad** so the next airdrop blocks them automatically.

**Detect → show → enforce.**

## Quick start (offline demo)

```bash
python3 sybil_detector.py
open dashboard.html   # or double-click — zero network deps
```

## Monad testnet

| | |
|--|--|
| Chain ID | `10143` |
| RPC | `https://testnet-rpc.monad.xyz` |
| Explorer | https://testnet.monadvision.com |
| Faucet | https://faucet.monad.xyz |

Verify live at [docs.monad.xyz](https://docs.monad.xyz/developer-essentials/testnet) if something fails.

## On-chain critical path

1. Install Foundry: `curl -L https://foundry.paradigm.xyz | bash && foundryup`
2. If `lib/forge-std` is missing: `git clone --depth 1 https://github.com/foundry-rs/forge-std lib/forge-std`
3. Copy `.env.example` → `.env`, add key + faucet MON
4. Deploy:

```bash
source .env
forge script script/Deploy.s.sol --rpc-url $MONAD_RPC --broadcast
```

5. Flag one wallet (`AttestOne` or `cast send`), fund `Airdrop`, call `claim()` from the
   flagged wallet → expect `SybilBlocked` revert on the explorer.
6. Publish detector output:

```bash
python3 sybil_detector.py
python3 script/attest.py          # needs cast + SYBIL_REGISTRY
```

## Layout

```
sybil_detector.py       # stdlib detector → graph_data.js + attestations.json
dashboard.html          # offline force graph
contracts/              # SybilRegistry + demo Airdrop
script/                 # Foundry deploy / attest helpers
seed_patterns.md        # fraud signatures + hard cases
memory-bank/            # agent context
```

## Team

- **Varnie** — deploy, reject proof, attest broadcast
- **Murtuza** — hard cases + pitch
- **Amin** — seam + projector demo

# Sybil Sweep

Catch airdrop farms from on-chain fingerprints, show them as a red web, and **write the
verdict onto Monad** so the next airdrop blocks them automatically.

**Detect → show → enforce.** Stack: Python detector + Foundry contracts + **React / viem** dashboard.

## Team folders (work here to avoid conflicts)

| Owner | Path | Owns |
|-------|------|------|
| **Murtuza** | [`data/`](data/) | `test_wallets.csv`, seed patterns, claimant realism |
| **Amin** | [`detector/`](detector/), [`dashboard/`](dashboard/) | detection + React/viem UI + seam |
| **Varnie** | [`contract/`](contract/), [`script/`](script/) | deploy, AttestOne, on-chain reject |

```
Murtuza sketch          →  Actual
detector/detector.py    →  detector/detector.py
dashboard/ (React)      →  dashboard/  (React + viem; legacy HTML kept as fallback)
contract/*.sol          →  contract/SybilRegistry.sol + Airdrop.sol
data/test_wallets.csv   →  data/test_wallets.csv
```

## Quick start

```bash
# 1) Detect (stdlib Python)
python3 detector/detector.py              # reads data/test_wallets.csv by default
python3 detector/detector.py --demo       # built-in synthetic set

# 2) Dashboard (React + viem)
cd dashboard
cp -n .env.example .env                   # set VITE_SYBIL_REGISTRY after deploy
npm install
npm run dev                               # http://localhost:5173
```

Or `./demo.sh` (runs detector, then `npm run dev`).

Legacy static fallback: `dashboard/public/fallback.html` (also linked from the React UI).

After deploy, wire the Amin seam:

```bash
python3 script/set_registry.py 0xRegistry 0xAirdrop
python3 script/attest.py          # full cluster dump (after AttestOne smoke)
# React dashboard: connect wallet / read registry via viem
```

## Monad testnet + viem

| | |
|--|--|
| Chain ID | `10143` |
| RPC | `https://testnet-rpc.monad.xyz` |
| Explorer | https://testnet.monadvision.com |
| Faucet | https://faucet.monad.xyz |
| Client lib | [viem](https://viem.sh/) |

Verify live at [docs.monad.xyz](https://docs.monad.xyz/developer-essentials/testnet) if something fails.

Example viem chain sketch (dashboard):

```ts
import { defineChain } from "viem";

export const monadTestnet = defineChain({
  id: 10143,
  name: "Monad Testnet",
  nativeCurrency: { name: "Monad", symbol: "MON", decimals: 18 },
  rpcUrls: { default: { http: ["https://testnet-rpc.monad.xyz"] } },
  blockExplorers: {
    default: { name: "MonadVision", url: "https://testnet.monadvision.com" },
  },
});
```

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
forge script script/AttestOne.s.sol:AttestOne --rpc-url $MONAD_RPC --broadcast
```

6. Beat-4 contrast on explorer (and in the React UI via viem):
   - Flagged wallet → `Airdrop.claim()` → **`SybilBlocked` revert**
   - Honest wallet → `claim()` → **gets paid 0.01 MON**
7. Full cluster dump:

```bash
python3 script/attest.py
```

**Two attest paths — do not confuse:**

| Goal | Command |
|------|---------|
| Flag one wallet (smoke) | `forge script script/AttestOne.s.sol:AttestOne --broadcast` |
| Publish all clusters | `python3 script/attest.py` |

## Layout

```
detector/detector.py     # stdlib detector
dashboard/               # React + viem app (Amin); legacy dashboard.html fallback
contract/                # SybilRegistry + Airdrop (Foundry src)
data/test_wallets.csv    # Murtuza/Esa claimant list
data/attestations.json   # detector output for attest.py
script/                  # Foundry deploy / AttestOne / attest helpers
```

## Demo risk note
Venue wifi can still kill npm CDNs / RPC. Keep a phone hotspot, pre-`npm run build` static host,
and the legacy `dashboard.html` + 30s backup video as safety nets. Enforce on explorer remains the differentiator if the UI flakes.

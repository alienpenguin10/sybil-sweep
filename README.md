# Sybil Sweep

Catch airdrop farms from on-chain fingerprints, show them as a red web, and **write the
verdict onto Monad** so the next airdrop blocks them automatically.

**Detect → show → enforce.** No viem/React — offline HTML + Foundry (venue wifi safe).

## Team folders (work here to avoid conflicts)

| Owner | Path | Owns |
|-------|------|------|
| **Murtuza** | [`data/`](data/) | `test_wallets.csv`, seed patterns, claimant realism |
| **Amin** | [`detector/`](detector/), [`dashboard/`](dashboard/) | detection + projector demo + seam |
| **Varnie** | [`contract/`](contract/), [`script/`](script/) | deploy, AttestOne, on-chain reject |

```
Murtuza sketch          →  Actual (working)
detector/detector.py    →  detector/detector.py
dashboard/ (React)      →  dashboard/dashboard.html (offline, not React)
contract/*.sol          →  contract/SybilRegistry.sol + Airdrop.sol
data/test_wallets.csv   →  data/test_wallets.csv
```

## Quick start (offline demo)

```bash
./demo.sh
# or:
python3 detector/detector.py              # reads data/test_wallets.csv by default
open dashboard/dashboard.html
```

```bash
python3 detector/detector.py --demo       # built-in synthetic set
python3 detector/detector.py --csv data/test_wallets.csv
```

After deploy, wire the Amin seam:

```bash
python3 script/set_registry.py 0xRegistry 0xAirdrop
python3 script/attest.py          # full cluster dump (after AttestOne smoke)
# open dashboard/dashboard.html → press R to probe isSybil
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
forge script script/AttestOne.s.sol:AttestOne --rpc-url $MONAD_RPC --broadcast
```

6. Beat-4 contrast on explorer:
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
dashboard/               # offline force graph + config.js
contract/                # SybilRegistry + Airdrop (Foundry src)
data/test_wallets.csv    # Murtuza/Esa claimant list
data/attestations.json   # detector output for attest.py
script/                  # Foundry deploy / AttestOne / attest helpers
```

# Tech Context — Sybil Sweep

## Stack
| Layer | Choice |
|-------|--------|
| Chain | Monad testnet |
| Detector | Python 3 stdlib only |
| Contracts | Solidity ^0.8.24, Foundry preferred (Remix OK) |
| Dashboard | **React + [viem](https://viem.sh/)** (wallet/RPC reads on Monad) |
| Fallback UI | `dashboard/dashboard.html` static canvas (no deps) |
| Deploy | Foundry scripts or Remix |

## Monad testnet (verify live if flaky)
Pulled from docs.monad.xyz (Aug 2026):
- **Chain ID:** `10143` (`0x279F`)
- **RPC:** `https://testnet-rpc.monad.xyz`
- **Explorer:** `https://testnet.monadvision.com`
- **Faucet:** `https://faucet.monad.xyz`
- **Symbol:** MON

Do not hardcode without checking docs — values have changed before.

## Dashboard / viem
- Use viem for `eth_call` equivalents: `isSybil`, `riskBpsOf`, `verdict`, `thresholdBps`
- Prefer `createPublicClient` for registry reads; `createWalletClient` + MetaMask for live `claim()` demo
- Config: registry + airdrop addresses from `script/set_registry.py` / env (`VITE_` or equivalent)
- Keep a built static export + hotspot for venue wifi

## Local tooling status
- Python 3.9+ available
- Node/npm for React dashboard
- Foundry (`forge`/`cast`) may need install: `curl -L https://foundry.paradigm.xyz | bash && foundryup`
- MetaMask + faucet MON required for live deploy / claim demo

## Key files
```
detector/detector.py       # detect → dashboard graph payload + data/attestations.json
contract/
  SybilRegistry.sol
  Airdrop.sol
dashboard/                 # React + viem app (Amin)
dashboard/dashboard.html   # static fallback
data/test_wallets.csv      # Murtuza claimant list
script/                    # Foundry deploy + AttestOne + attest.py
```

## Commands
```bash
python3 detector/detector.py
python3 detector/detector.py --csv data/test_wallets.csv
cd dashboard && npm install && npm run dev
forge script script/Deploy.s.sol:Deploy --rpc-url $MONAD_RPC --broadcast
```

## Env
```
PRIVATE_KEY=...
MONAD_RPC=https://testnet-rpc.monad.xyz
SYBIL_REGISTRY=0x...   # after deploy
SYBIL_AIRDROP=0x...
```

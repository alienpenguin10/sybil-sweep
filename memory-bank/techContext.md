# Tech Context — Sybil Sweep

## Stack
| Layer | Choice |
|-------|--------|
| Chain | Monad testnet |
| Detector | Python 3 stdlib only |
| Contracts | Solidity ^0.8.24, Foundry preferred (Remix OK) |
| Dashboard | Single `dashboard.html` + `graph_data.js`, canvas force-graph |
| Deploy | Foundry scripts or Remix |

## Monad testnet (verify live if flaky)
Pulled from docs.monad.xyz (Aug 2026):
- **Chain ID:** `10143` (`0x279F`)
- **RPC:** `https://testnet-rpc.monad.xyz`
- **Explorer:** `https://testnet.monadvision.com`
- **Faucet:** `https://faucet.monad.xyz`
- **Symbol:** MON

Do not hardcode without checking docs — values have changed before.

## Local tooling status
- Python 3.9+ available
- Foundry (`forge`/`cast`) may need install: `curl -L https://foundry.paradigm.xyz | bash && foundryup`
- MetaMask + faucet MON required for live deploy

## Key files
```
detector/detector.py       # detect + emit dashboard/graph_data.js + data/attestations.json
contract/
  SybilRegistry.sol
  Airdrop.sol
dashboard/dashboard.html   # offline viz
data/test_wallets.csv      # Murtuza claimant list
script/                    # Foundry deploy + AttestOne + attest.py
```

## Commands
```bash
python3 detector/detector.py
python3 detector/detector.py --csv data/test_wallets.csv
open dashboard/dashboard.html
forge script script/Deploy.s.sol:Deploy --rpc-url $MONAD_RPC --broadcast
```

## Env
```
PRIVATE_KEY=...
MONAD_RPC=https://testnet-rpc.monad.xyz
SYBIL_REGISTRY=0x...   # after deploy
```

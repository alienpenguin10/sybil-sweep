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
sybil_detector.py      # detect + emit graph_data.js + attestations.json
contracts/
  SybilRegistry.sol    # attestation registry
  Airdrop.sol          # demo claim() with requireHuman
script/                # Foundry deploy + attest
dashboard.html         # offline viz
graph_data.js          # generated
attestations.json      # generated
seed_patterns.md       # fraud signatures + hard cases
```

## Commands
```bash
python3 sybil_detector.py          # regenerate graph + attestations
# open dashboard.html in browser
forge script script/Deploy.s.sol --rpc-url $MONAD_RPC --broadcast
forge script script/Attest.s.sol --rpc-url $MONAD_RPC --broadcast
```

## Env
```
PRIVATE_KEY=...
MONAD_RPC=https://testnet-rpc.monad.xyz
SYBIL_REGISTRY=0x...   # after deploy
```

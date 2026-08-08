# Progress — Sybil Sweep

## What works
- [x] GitHub repo + Memory Bank
- [x] Detector (~95.7% recall) → `graph_data.js` + `attestations.json`
- [x] `SybilRegistry.sol` + `Airdrop.sol` compile
- [x] Foundry scripts: Deploy (fund+0.01 claim), AttestOne, attest.py
- [x] Naming trap fixed: `AttestOne.s.sol:AttestOne` vs `python3 script/attest.py`
- [x] forge-std missing-dep called out in README (`lib/` gitignored)
- [x] Amin seam (offline): projector dashboard, Enforce panel, demo.sh

## What's left
- [ ] Faucet MON + MetaMask on Monad testnet (10143) — **Varnie**
- [ ] Deploy → AttestOne → sybil revert + honest payout on explorer — **Varnie**
- [ ] `set_registry.py` + `attest.py` full publish + dashboard R — **Amin**
- [ ] 30s backup video of full flow
- [ ] (Stretch) spawn-40 live farm

## Known issues / risks
- Fresh clone: `forge build` fails until `git clone ... forge-std lib/forge-std`
- Venue wifi — dashboard offline; `forceOffline: true` in config.js if RPC dies
- Faucet rate limits — get MON early; Deploy needs ≥0.1 MON for airdrop fund
- Do not commit `.env` / private keys

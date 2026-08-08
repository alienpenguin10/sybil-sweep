# Progress — Sybil Sweep

## What works
- [x] Murtuza folder layout: `detector/`, `dashboard/`, `contract/`, `data/`
- [x] `data/test_wallets.csv` (STEP 3) + detector CSV loader
- [x] Offline dashboard (not React)
- [x] Foundry scripts against `contract/`
- [x] AttestOne vs attest.py naming clear
- [x] Deploy funds 0.1 + claim 0.01

## What's left
- [ ] Merge PR to main
- [ ] Varnie live deploy + reject proof
- [ ] Full attest.py + dashboard live probe
- [ ] Backup video
- [ ] (Stretch) spawn-40

## Known issues / risks
- Fresh clone needs `lib/forge-std`
- Do not introduce React/viem for the projector demo
- Do not commit `.env`

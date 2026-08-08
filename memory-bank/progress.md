# Progress — Sybil Sweep

## What works
- [x] Murtuza folder layout: `detector/`, `dashboard/`, `contract/`, `data/`
- [x] `data/test_wallets.csv` + detector CSV loader
- [x] Foundry scripts against `contract/`
- [x] AttestOne vs attest.py naming clear
- [x] Deploy funds 0.1 + claim 0.01
- [x] Docs updated for **React + viem** dashboard direction
- [x] Legacy static `dashboard.html` kept as fallback

## What's left
- [ ] Scaffold React + viem app in `dashboard/` (replace HTML as primary UI)
- [ ] Varnie live deploy + reject proof
- [ ] Full attest.py + dashboard live probe via viem
- [ ] Hotspot + built static export + 30s backup video
- [ ] (Stretch) spawn-40

## Known issues / risks
- Fresh clone needs `lib/forge-std`
- Venue wifi can break npm/RPC — prebuild + hotspot + HTML fallback
- Do not commit `.env`

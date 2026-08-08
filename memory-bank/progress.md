# Progress — Sybil Sweep

## What works
- [x] Murtuza folder layout: `detector/`, `dashboard/`, `contract/`, `data/`
- [x] `data/test_wallets.csv` + detector CSV loader
- [x] Foundry scripts against `contract/`
- [x] AttestOne vs attest.py naming clear
- [x] Deploy funds 0.1 + claim 0.01
- [x] Docs updated for **React + viem** dashboard direction
- [x] **React + viem Vite app** under `dashboard/` (`npm run dev`)
- [x] Legacy static `public/fallback.html` kept as fallback

## What's left
- [ ] Varnie live deploy + reject proof
- [ ] `set_registry.py` + live viem probe with real addresses
- [ ] Hotspot + `npm run build` static export + 30s backup video
- [ ] (Stretch) spawn-40

## Known issues / risks
- Fresh clone needs `lib/forge-std`
- Venue wifi can break npm/RPC — prebuild + hotspot + HTML fallback
- Do not commit `.env`

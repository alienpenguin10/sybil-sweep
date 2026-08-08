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
- [x] **Foundry installed + contracts compile** (forge 1.7.1, `lib/forge-std` cloned)
- [x] **Deployed to Monad testnet** — registry `0x1D58…97D9`, airdrop `0x290f…d9C4`
- [x] **Reject proven on-chain** — flagged `claim()` reverts `SybilBlocked`, honest `claim()`
      paid 0.01 MON, airdrop balance 0.1 → 0.09
- [x] **All clusters published** — 2 txs, 30 wallets tagged via `script/attest.py`
- [x] **Both dashboards read the verdict back live** — "LIVE ON MONAD", probe shows
      SYBIL · blocked · risk 100% vs threshold 70%

## What's left
- [ ] 30s backup video of the full flow
- [ ] Commit `dashboard/public/config.js` (carries the live addresses)
- [ ] (Stretch) spawn-40

## Known issues / risks
- **Public RPC rate limit is the #1 demo risk now.** `testnet-rpc.monad.xyz` is 15 req/sec per
  IP with a long 429 cooldown once tripped; it knocked the dashboard into its offline branch
  for an entire session. Dashboard is pointed at `https://10143.rpc.thirdweb.com` instead.
  Backups and dead ends listed in `activeContext.md`.
- Vite reads `dashboard/.env` only at boot — **restart `npm run dev` after `set_registry.py`**.
- `forge`/`cast` are not on `PATH` in a fresh shell: `export PATH="$HOME/.foundry/bin:$PATH"`.
- Fresh clone needs `git clone --depth 1 https://github.com/foundry-rs/forge-std lib/forge-std`
- Venue wifi can break npm/RPC — prebuild + hotspot + HTML fallback + `forceOffline: true`
- Do not commit `.env`. The deployer key was passed on `cast`'s argv by `attest.py`, so treat
  `0xdb3F…a88a` as burned after the event — testnet-only, nothing at stake.
- Re-running the detector rewrites `graph_data.*` / `attestations.json` with a fresh
  `generatedAt` and would desync the evidence hashes already published on-chain.

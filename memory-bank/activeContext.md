# Active Context — Sybil Sweep

## Current focus
Scaffold is ready. **Next: on-chain critical path** — deploy `SybilRegistry` +
`Airdrop`, attest one wallet, prove `claim()` reverts on Monad testnet explorer.

## Recent changes
- Cloned https://github.com/alienpenguin10/sybil-sweep.git (was README-only)
- Built Memory Bank, detector, contracts, dashboard, Foundry scripts
- Foundry 1.7.1 installed; contracts compile
- Detector demo: ~96% recall with hard cases (honest friends stay blue; soft FN wallets)

## Next steps (build order)
1. Varnie: faucet MON → deploy → AttestOne / cast → claim revert
2. Amin: wire explorer links / projector; run `attest.py` for full clusters
3. Murtuza: harden seed patterns / pitch
4. Stretch spawn-40 only if #1–2 green by ~5pm

## Active decisions
- Detector stays stdlib-only; SHA-256 evidence hash
- Offline dashboard (no CDN)
- Foundry primary; Remix backup for fastest first deploy

## Open questions
- Who holds deploy key / has faucet MON?
- Push this scaffold to origin now or after first successful deploy?

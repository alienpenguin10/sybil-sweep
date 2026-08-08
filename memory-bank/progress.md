# Progress — Sybil Sweep

## What works
- [x] GitHub repo cloned locally (`main`)
- [x] Memory Bank + `.cursorrules` initialized
- [x] `sybil_detector.py` — demo dataset, union-find, scoring, emits graph + attestations
- [x] Demo metrics tuned: **95.7% recall** (40 red + 4 amber suspects; 2 soft FN)
- [x] `SybilRegistry.sol` + demo `Airdrop.sol` — compile clean under Foundry
- [x] Offline `dashboard.html` (canvas force-graph)
- [x] `seed_patterns.md` fraud-signature menu
- [x] Foundry installed (`forge` 1.7.1); `forge-std` vendored; `Deploy`/`Attest` scripts
- [x] `script/attest.py` dry-run against `attestations.json`

## What's left
- [ ] Faucet MON + MetaMask on Monad testnet (10143)
- [ ] Deploy registry + airdrop; prove `requireHuman` reject live (critical path)
- [ ] Broadcast real clusters via `python3 script/attest.py`
- [ ] Projector polish + 30s backup video
- [ ] Push scaffold to GitHub when team agrees
- [ ] (Stretch) spawn-40 live farm

## Known issues / risks
- Venue wifi — keep dashboard offline; hotspot + backup video
- Faucet rate limits — get MON early
- `lib/forge-std` is vendored for offline builds; teammates can also `git clone` it into `lib/`
- Do not commit `.env` / private keys

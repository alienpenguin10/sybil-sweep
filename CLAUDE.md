# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Context docs — read before non-trivial work

- `AGENT_BRIEF.md` (untracked, local) — the strategy behind the spec: why this project, the
  wedge, what not to build. Use it for judgment calls the team hasn't made explicitly.
- `memory-bank/*.md` — the `.cursorrules` protocol says to read these at task start, update
  `activeContext.md` + `progress.md` after significant work, and review **all** of them when
  the user says "update memory bank". Honor that; it's how the team hands off between sessions.
- `data/seed_patterns.md` — the fraud-signature menu and the hard cases the demo dataset must keep.

Docs drift from reality — trust the code first, then the "Verified state" section below.

## Commands

```bash
python3 detector/detector.py          # reads data/test_wallets.csv → graph_data.* + attestations.json
python3 detector/detector.py --demo   # built-in synthetic set instead of the CSV
./demo.sh                             # detect + print demo beat lines + start the dashboard

cd dashboard && npm install && npm run dev    # http://localhost:5173
```

**There is no `npm start`** — the Vite scaffold defines only `dev`, `build`, `preview`.
The HTML fallback is served by Vite at `http://localhost:5173/fallback.html`; opening it
directly as a `file://` URL also works (that's what it's designed for).

```bash
# On-chain. forge/cast are NOT on PATH in a fresh shell:
export PATH="$HOME/.foundry/bin:$PATH"
set -a; . ./.env; set +a

forge script script/Deploy.s.sol:Deploy --rpc-url $MONAD_RPC --broadcast
forge script script/AttestOne.s.sol:AttestOne --rpc-url $MONAD_RPC --broadcast  # flag ONE wallet
python3 script/attest.py --dry-run    # print cast commands without sending
python3 script/attest.py              # publish ALL clusters (needs cast on PATH)
python3 script/set_registry.py 0xRegistry 0xAirdrop   # → dashboard/.env + public/config.js
```

**Two attest paths, easily confused** — `AttestOne.s.sol` is the single-wallet smoke test for
the critical-path reject proof. The full cluster dump is `script/attest.py`, *not* a Solidity
script. (The file was renamed from `Attest.s.sol` precisely because of this confusion; older
docs and shell history may still say `script/Attest.s.sol`.)

No tests, no linter — a ~6h hackathon build (Monad Blitz London). Don't add a test/lint harness
unless asked.

## Verified state (checked, not inherited from the memory bank)

- **Deployed and enforcing on Monad testnet (chain 10143).**
  `SybilRegistry` `0x1D582E8d297d47273B64B80BD93c159513FD97D9`,
  `Airdrop` `0x290fbF9fb7e06dF88A8C14546939db476888d9C4`, owner `0xdb3FF3B9…ECC3a88a`.
  Beat-4 proof: reject `0xc92844c7…` (status 0, `SybilBlocked`), payout `0x5832f1f4…`
  (status 1, 0.01 MON; airdrop 0.1 → 0.09). Both clusters published, 30 wallets tagged.
- Detector **runs clean**: 61 claimants, 100% precision, 94.4% recall, 2 attestations
  (cluster 1 = 20 wallets @ 10000 bps; cluster 2 = 10 wallets @ 9000 bps, mixed funder → `0x0`).
- Foundry 1.7.1 is installed at `~/.foundry/bin` but **not on `PATH`** in fresh shells.
  **`lib/forge-std` is gitignored and never committed** — a fresh clone needs
  `git clone --depth 1 https://github.com/foundry-rs/forge-std lib/forge-std` before `forge build`.
- The fallback dashboard's three hardcoded selectors are **correct**, verified against the
  deployed contract: `isSybil(address)` = `0x4fa6ea73`, `riskBpsOf(address)` = `0x680dc72f`,
  `thresholdBps()` = `0xc1144b71`. No need to re-derive them.
- `foundry.toml` sets `src = "contract"` — **singular**. The Solidity scripts import
  `../contract/…`. Root `sybil_detector.py` is a 4-line shim around `detector/detector.py`.

## ⚠️ The public RPC will rate-limit you

`https://testnet-rpc.monad.xyz` enforces **15 requests/sec per IP**, and once tripped it keeps
returning HTTP 429 for a long cooldown — long enough to knock the dashboard's live probe into
its offline branch for an entire session. This is confirmed with plain `curl`, so when the
Enforce panel says "RPC OFFLINE", suspect the rate limit before suspecting CORS (the RPC does
return a correct `access-control-allow-origin`).

The dashboard reads from `https://10143.rpc.thirdweb.com` for this reason. Also verified
working: `https://rpc.ankr.com/monad_testnet` (burst-limits when the app fires 3 calls at once)
and `https://monad-testnet.gateway.tenderly.co`. Dead ends: `monad-testnet.drpc.org` (rejects
the gas param), `testnet-rpc2.monad.xyz` (UNAUTHORIZED).

Re-point it with `MONAD_RPC=<url> python3 script/set_registry.py 0xReg 0xDrop`, **then restart
Vite** — it only reads `dashboard/.env` at boot.

## Architecture

`detector/detector.py` (stdlib only, ~600 lines) is the whole off-chain engine, one pipeline:
CSV loader (or `make_demo_dataset()`) → `link_pairs()` → union-find → `score_cluster()` →
`detect()` → `write_outputs()`. Swapping to real Monad data means replacing the loader only;
`detect(events)` accepts any `list[ClaimEvent]`.

Its outputs are the integration seams:

- **`dashboard/public/graph_data.json`** → the React app; **`graph_data.js`** (same data as
  `window.SYBIL_GRAPH = {...};`) → `public/fallback.html`. The `.js` form exists *specifically*
  so the fallback can `<script src>` it under `file://` — `fetch()`ing a `.json` would be
  CORS-blocked with no server. Don't "improve" the fallback into JSON+fetch.
- **`data/attestations.json`** → `script/attest.py` → `cast send` → `SybilRegistry.attestCluster`.
  Writes a gitignored `data/onchain_status.json` receipt.
- **`script/set_registry.py`** writes both `dashboard/.env` (Vite/viem) and
  `dashboard/public/config.js` (`window.SYBIL_CONFIG`, fallback only).

Both UIs read verdicts back from chain: `thresholdBps()`, `isSybil`, and `riskBpsOf` against a
probe wallet (`clusters[0].sampleMember`, a field the detector emits for exactly this). Every
failure path degrades to the offline story rather than throwing — preserve that. In the
fallback, keys `1`–`4` jump demo beats and `R` re-probes the chain.

Full flow: deploy → `set_registry.py` → `attest.py` → restart Vite / press `R` → verdict live.

## Invariants that look like bugs but aren't

- **Cluster ID offset.** The contract reserves `clusterId == 0` for "no cluster", so on-chain
  IDs are 1-indexed while the dashboard uses `cluster == -1` for honest/unclustered wallets.
  `detect()` bridges them (`onchain_id = dashboard_id + 1`); `cluster_cards` carries both
  `clusterId` (dashboard, 0-indexed) and `onchainClusterId`.
- **`evidenceHash` is SHA-256, not keccak256** — deliberate, to keep the detector pip-free. The
  contract only *stores* it and never recomputes it on-chain, so there is no parity bug.
- **`confidenceBps = risk × 100`**, where `risk` is a 0–100 heuristic. `SYBIL_RISK_FLOOR = 55`
  gates what becomes red/attested; clusters scoring 45–54 render as amber `suspect` and are
  deliberately **not** attested.
- **Recall is intentionally not 100%.** `score_cluster()` demotes the honest whale who funds
  friends over days and small staggered rings, plus the dataset carries "soft FN" farm wallets.
  A judge reads a perfect score as faked; target ~92–96%. Do not tune these away.
- **Detected addresses are ASCII, not real** — `0x6661726d61303000…` is `"farma00"` padded to
  20 bytes. Valid hex so `cast` accepts them, but **no private key exists for any of them**, so
  they can never send a transaction. Any live reject proof must come from a wallet you control.
- **`attestCluster` overwrites the cluster struct but never clears per-wallet mappings.**
  Re-running `attest.py` after `AttestOne` leaves the smoke-test wallet flagged. Intended.

## Constraints that are easy to violate accidentally

- **Detector stays stdlib-only.** No pip installs — it has to run on any laptop at the venue.
- **The fallback dashboard stays zero-CDN.** No external libraries, fonts, or stylesheets; the
  force graph is hand-rolled canvas. Its one network call is the `eth_call` probe, which is
  optional and fails soft. (The React app does use npm deps, but they're bundled by Vite, not
  fetched from a CDN at runtime.) `forceOffline: true` in `config.js` is the escape hatch and
  must keep working.
- **The on-chain layer is the product, not a stretch goal.** Detect → show → *enforce*. If time
  forces a trade, a working `requireHuman()` revert beats a nicer graph. Never pitch or build
  this as wallet visualization (saturated) or an agent-wallet/tx firewall (taken).
- **Verify Monad chain ID and RPC from docs.monad.xyz at build time.** The repo records chain ID
  `10143` / `https://testnet-rpc.monad.xyz` in four places (`dashboard/public/config.js`,
  `.env.example`, `README.md`, `.cursorrules`) — these have changed before, and a change means
  editing all four. (Last checked live: `eth_chainId` → `0x279f` = 10143. Still correct.)
- `Deploy.s.sol` sends real value: `setClaimAmount(0.01 ether)` + `fund{value: 0.1 ether}`. The
  deployer needs ≥0.1 MON plus gas or deployment reverts. Gas has been ~200 gwei, so budget
  ~0.04 MON per transaction — the plan's original 0.005 MON gas top-ups are too small.
- Running the detector always rewrites `graph_data.*` and `attestations.json` with a fresh
  `generatedAt`, so it dirties the git tree on every run even when nothing meaningful changed —
  and **it desyncs the evidence hashes already published on-chain**. `./demo.sh` runs it too.
- `script/attest.py` auto-loads `.env` and passes `--private-key` on `cast`'s argv, so the key is
  visible in the process list. Fine for a testnet demo key; never point it at a funded key.
- **Team folders** (avoid conflicts): Murtuza → `data/`; Amin → `detector/`, `dashboard/`;
  Varnie → `contract/`, `script/`. `main` is protected — branch and open a PR.

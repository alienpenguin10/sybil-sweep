# System Patterns — Sybil Sweep

## Architecture
```
Monad testnet (claim/transfer logs)
        │  read
        ▼
Detection engine (Python, stdlib only)
   • shared-funder linking
   • funding-burst + identical amount/gas
   • union-find clustering
   • risk / confidence scoring
   • attestation per cluster (+ evidence hash)
        │
        ├── data/attestations.json ──► script ──► SybilRegistry.attestCluster(...)
        │                                              │
        │                               Airdrop.claim() → requireHuman() → revert if sybil
        │
        └── graph payload ──► dashboard/ (React + viem)
                                 • force graph: red farms / blue humans
                                 • viem publicClient: isSybil / verdict
                                 • walletClient: optional live claim demo
```

## Detection linking rules
- **(A)** Shared funder
- **(B)** Funded within `BURST_SECONDS` AND near-identical amount + gas
- Stretch signals: sequential nonces / same first action; **fan-in** (claim rewards → one collector)

## Clustering & IDs
- Union-find components → clusters
- Contract: `clusterId == 0` means "no cluster" → attestations are **1-indexed**
- Dashboard: `cluster == -1` for unclustered / honest wallets
- Detector emits `dashboard_cluster_id + 1` for on-chain IDs

## Attestation shape
```
clusterId, members[], size, confidenceBps (= risk × 100),
funder (or 0x0 if mixed), fundingWindowSecs, evidenceHash
```
- `evidenceHash` = SHA-256 of sorted members + funder + window (stdlib anchor; not keccak)
- Contract stores hash only; does not recompute on-chain

## On-chain enforcement
- `SybilRegistry` owner publishes via `attestCluster`
- Threshold default 7000 bps (70%); `isSybil` iff confidence ≥ threshold
- Airdrops: one line — `reg.requireHuman(msg.sender);`
- React UI uses viem to read the same registry the airdrop enforces

## Design constraints
- Detector: **no pip deps** unless strong reason
- Dashboard: **React + viem** is the product UI; keep static HTML fallback for wifi failure
- Prefer working on-chain reject over prettier graph

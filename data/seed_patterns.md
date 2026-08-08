# Seed patterns — fraud signatures for Sybil Sweep

Murtuza's menu: what a farm looks like on-chain, and which hard cases to keep
so the demo shows **judgment** (~92–96%), not a rigged 100%.

## Strong farm signatures (flag these)
1. **Shared funder** — one EOAs funds many claimants
2. **Funding burst** — many wallets funded inside a tight window (seconds–minutes)
3. **Identical amount + gas** — clone wallets with copy-paste tx params
4. **Fan-in (stretch)** — after claim, leaves send rewards to one collector
5. **Same first action** — every wallet's first tx is the claim (stretch)

## Hard cases (must appear in demo dataset)
| Case | Expected UI | Why |
|------|-------------|-----|
| Honest power-user funds 4–5 friends over days, varied amounts/gas | **Blue** (not a farm) | Shared funder alone ≠ sybil; window demotes risk |
| Small 3–4 wallet ring, slightly noisy amounts | **Amber / suspect** or low-confidence card | Shows threshold judgment |
| Large burst farm (20+) shared funder + identical params | **Red** web, high confidence | Classic Uber-style fraud ring |
| Two honest wallets funded close in time, different amounts | Stay **blue**, unlinked | Burst without amount/gas match must not false-positive |

## Detector knobs (`sybil_detector.py`)
- `BURST_SECONDS` — funding window for rule B
- `AMOUNT_TOL_BPS` / `GAS_TOL_BPS` — homogeneity
- `MIN_CLUSTER_SIZE` — default 3
- `SYBIL_RISK_FLOOR` — below this, cluster stays off the red attestation list

## Pitch language (optional)
"A sybil farm is a fraud ring: shared bankroll, synchronized activation, identical
behaviour, and often money flowing back to one operator. We read that behaviour
and register the verdict where the next airdrop can enforce it."

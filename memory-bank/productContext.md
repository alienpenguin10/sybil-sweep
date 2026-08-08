# Product Context — Sybil Sweep

## Why this exists
Sybil / airdrop farming is expensive and disputed. Monad paid an outside firm to scrub
fake wallets before its own token airdrop; people disputed the result. That is the pitch
opening and why this is Monad-relevant.

A sybil farm is structurally identical to a fraud ring (shared funder, burst funding,
identical amounts/gas, fan-in to a collector). Murtuza's ~8 years fraud/risk at Uber is
the team's unique credibility asset.

## How it should work
1. Load claimant events (CSV / demo / Monad logs)
2. Off-chain detector links wallets (shared funder, funding burst + amount/gas) and clusters via union-find
3. Score clusters; emit attestations + graph payload
4. Publish attestations to `SybilRegistry` on Monad testnet
5. **React + viem** dashboard shows the red farm graph and reads on-chain verdicts
6. Token airdrops call `reg.requireHuman(msg.sender)` — flagged wallets revert

## UX goals (demo ~90s)
1. Name the problem (~15s) — Murtuza
2. Load claimants; say count out loud (~15s) — Amin
3. Red rings / blue honest in React UI; point at recall (~20s) — Amin
4. Explorer + viem: attested + live `claim()` revert (~20s) — Varnie / Amin
5. Close: behaviour-based, every farm before a token moves (~20s) — Murtuza

## Pitch one-liner
"Airdrops get looted by people running hundreds of fake wallets. Sybil Sweep catches them
from their on-chain fingerprints, shows the farm as a red web, and writes the verdict onto
Monad so the next airdrop blocks them automatically." Detect → show → **enforce**.

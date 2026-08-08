# Project Brief — Sybil Sweep

## Mission
Given a list of wallets claiming an airdrop, find fake accounts run by one operator
("sybils"), show them as a red graph, **and write the verdict onto Monad** so future
airdrops reject those wallets on-chain.

## Flow (four beats)
1. **Input** — claimant list (wallets asking for a token airdrop)
2. **Detect** — cluster wallets that share fingerprints of one operator
3. **Show** — force graph: red webs = farms, blue dots = real users (evidence, not product)
4. **Enforce** — publish each farm as an on-chain attestation; airdrop calls `requireHuman()` → revert

## Wedge
Not wallet visualization. Not agent-wallet firewalls.
**Prove and register sybil clusters on-chain so future token distributions enforce the result automatically.**

## Event
- Monad Blitz London — 1-day hackathon (~6h build, submission ~6:30pm, judged by demo)
- Pitch differentiator: on-chain attestation + claim rejection (answers "why Monad?")

## Team
| Person | Role |
|--------|------|
| **Varnie** | Chain: MetaMask, faucet, deploy registry, prove reject, attest script, stretch spawn-40 |
| **Murtuza** | Data realism / hard cases, pattern spec, pitch open+close (fraud-ring credibility) |
| **Amin** | Seam (detector → attestations → on-chain → dashboard readback), projector polish, demo choreography |

## Non-goals
- Agent wallet / tx firewall products
- Pitching as "we visualize wallets"
- Over-polishing the dashboard at the expense of on-chain reject
- 100% recall on synthetic data (looks faked; aim ~92–96% with hard cases)

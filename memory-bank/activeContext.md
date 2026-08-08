# Active Context — Sybil Sweep

## Current focus
Docs + architecture updated: **dashboard is React + viem**. Legacy
`dashboard/dashboard.html` remains a projector/wifi fallback only.
Folder ownership still applies for conflict-free parallel work.

## Ownership map
| Person | Edit here |
|--------|-----------|
| Murtuza | `data/` (CSV, seed patterns) |
| Amin | `detector/`, `dashboard/` (React + viem) |
| Varnie | `contract/`, `script/` |

## Recent decisions
- Use [viem](https://viem.sh/) for Monad testnet reads/writes from the dashboard
- Do **not** treat static HTML as the long-term UI
- Still keep hotspot + static fallback + backup video for venue risk

## Next steps
1. Scaffold React+viem app under `dashboard/` (Amin)
2. Wire registry address + `isSybil` / `verdict` probes via viem
3. Varnie: Deploy → AttestOne → reject + human payout
4. Merge open PRs / keep `main` in sync

## Commands
```bash
python3 detector/detector.py
cd dashboard && npm install && npm run dev
```

# Active Context — Sybil Sweep

## Current focus
Repo aligned to **Murtuza folder layout** so the three of us edit different trees
without merge conflicts. Working demo preserved (no React, no empty stubs).

## Ownership map
| Person | Edit here |
|--------|-----------|
| Murtuza | `data/` (CSV, seed patterns) |
| Amin | `detector/`, `dashboard/` |
| Varnie | `contract/`, `script/` |

## Recent changes
- `contracts/` → `contract/` (Foundry `src = "contract"`)
- Dashboard assets under `dashboard/`
- Detector at `detector/detector.py` with `--csv` (default `data/test_wallets.csv`)
- `data/test_wallets.csv` (Esa STEP 3) with farms + hard cases

## Next steps
1. Merge this PR
2. Varnie: Deploy → AttestOne → reject + human payout
3. Amin: set_registry + full attest.py + probe R
4. Murtuza: tune CSV / pitch

## Commands
```bash
python3 detector/detector.py
open dashboard/dashboard.html
```

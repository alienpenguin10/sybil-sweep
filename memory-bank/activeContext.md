# Active Context — Sybil Sweep

## Current focus
**React + viem dashboard is live locally.** Open http://localhost:5173  
Legacy HTML: `dashboard/public/fallback.html`

## Ownership map
| Person | Edit here |
|--------|-----------|
| Murtuza | `data/` (CSV, seed patterns) |
| Amin | `detector/`, `dashboard/` (React + viem) |
| Varnie | `contract/`, `script/` |

## Recent changes
- Vite React+TS+viem app: force graph, Enforce panel, viem `isSybil` probe
- Detector writes `dashboard/public/graph_data.json` (+ `.js` for fallback)
- `set_registry.py` writes `dashboard/.env` + `public/config.js`
- `./demo.sh` starts `npm run dev`
- Production build verified (`npm run build`)

## Next steps
1. Varnie deploy → `python3 script/set_registry.py 0xReg 0xDrop`
2. Restart Vite → key **R** to re-probe
3. Commit/push React scaffold when ready

## Commands
```bash
python3 detector/detector.py
cd dashboard && npm run dev
```

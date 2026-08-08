# Active Context — Sybil Sweep

## Current focus
**ENFORCE IS LIVE ON MONAD TESTNET.** Deploy → attest → reject is proven end-to-end,
and both dashboards read the verdict back off-chain.

## Deployed (Monad testnet, chain 10143)
| What | Address |
|------|---------|
| `SybilRegistry` | `0x1D582E8d297d47273B64B80BD93c159513FD97D9` |
| `Airdrop` | `0x290fbF9fb7e06dF88A8C14546939db476888d9C4` |
| Deployer / owner | `0xdb3FF3B915FA795e71CEeD64e1157654ECC3a88a` |
| Flagged demo wallet | `0xd8A08DF92652fF3992545D40DeDEe0FDA31f8871` |

## Beat-4 proof transactions (the demo money shot)
```
❌ reject  0xc92844c753aefbb4e7c9e12ce62eb220dbd46f79f2e6c5d5f63834215a8c369a  (status 0, SybilBlocked)
✅ payout  0x5832f1f4a86acfc971899f03572660b8e522b7d08ac1217b1927828d9ec31c67  (status 1, 0.01 MON)
```
Both on https://testnet.monadvision.com/tx/<hash>. Airdrop balance went 0.1 → 0.09 MON,
so the payout is real and not just an event.

Clusters published by `script/attest.py` (2 txs, 30 wallets tagged):
`0x9c0f780ced372ae17d5b3cf28ba09b57975805290ed01539a1717300676c5844` (cluster 1, 20 wallets)
`0x429b656d120859190799818faf0341a94347cfce27c228c3406bd345e54569c4` (cluster 2, 10 wallets)

## Ownership map
| Person | Edit here |
|--------|-----------|
| Murtuza | `data/` (CSV, seed patterns) |
| Amin | `detector/`, `dashboard/` (React + viem) |
| Varnie | `contract/`, `script/` |

## Recent changes
- Foundry installed (1.7.1); `lib/forge-std` cloned (still gitignored, needed on every fresh clone)
- Deployed both contracts, ran `AttestOne` then the full `attest.py` dump
- `set_registry.py` wrote `dashboard/.env` + `dashboard/public/config.js`
- **Dashboard RPC switched off `testnet-rpc.monad.xyz`** — see the rate-limit note below

## ⚠️ RPC rate limit — read before demo
`https://testnet-rpc.monad.xyz` enforces **15 requests/sec per IP** and, once tripped, keeps
returning HTTP 429 for a sustained cooldown — long enough that the dashboard's live probe
showed "RPC OFFLINE" for the whole session. Confirmed with plain `curl`, so it is not a CORS
or browser issue (the RPC does return correct `access-control-allow-origin`).

Dashboard now reads from **`https://10143.rpc.thirdweb.com`**. Verified working alternatives,
all returning identical values for `thresholdBps` / `isSybil` / `riskBpsOf`:
- `https://10143.rpc.thirdweb.com` ← currently configured, most tolerant
- `https://rpc.ankr.com/monad_testnet` (works, but burst-limits when the app fires 3 calls at once)
- `https://monad-testnet.gateway.tenderly.co`

Dead ends: `monad-testnet.drpc.org` (rejects the gas param), `testnet-rpc2.monad.xyz` (UNAUTHORIZED).

`.env`'s `MONAD_RPC` is still the official endpoint — that is fine, writes went through. To
re-point the dashboard: `MONAD_RPC=<url> python3 script/set_registry.py 0xReg 0xDrop`, then
restart Vite (it only reads `.env` at boot).

## Next steps
1. 30s backup video of the full flow — the last open item
2. Murtuza: pitch open/close
3. Commit `dashboard/public/config.js` (holds the live addresses) when the team is ready
4. (Stretch) spawn-40

## Commands
```bash
python3 detector/detector.py
cd dashboard && npm run dev        # http://localhost:5173  (no `npm start` — Vite uses `dev`)
# fallback, served by Vite at http://localhost:5173/fallback.html
export PATH="$HOME/.foundry/bin:$PATH"   # forge/cast are NOT on PATH in fresh shells
```

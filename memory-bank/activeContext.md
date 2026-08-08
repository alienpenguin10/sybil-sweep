# Active Context — Sybil Sweep

## Current focus
**Varnie critical path is documented and de-snagged.** Deploy funds airdrop + sets
0.01 claim; AttestOne file/contract names align; forge-std clone called out.

## Recent changes
- Renamed `script/Attest.s.sol` → `script/AttestOne.s.sol` (contract `AttestOne`)
- `Deploy.s.sol`: `setClaimAmount(0.01 ether)` + `fund{value: 0.1 ether}()`
- `.env.example`: `SYBIL_AIRDROP` + correct AttestOne / attest.py split
- README critical path rewritten for Varnie

## Attest path cheat-sheet
```bash
forge script script/AttestOne.s.sol:AttestOne --rpc-url $MONAD_RPC --broadcast   # one wallet
python3 script/attest.py                                                         # full dump
```

## Next steps
1. Varnie: faucet → Deploy → AttestOne → sybil revert + human payout on explorer
2. Amin: `set_registry.py` + full `attest.py` + dashboard R
3. Murtuza: pitch open/close
4. Stretch spawn-40 only if enforce is green

## Open questions
- Who holds deploy key / has faucet MON?

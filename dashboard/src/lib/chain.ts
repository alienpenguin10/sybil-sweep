import { defineChain, fallback, http, type Address } from "viem";

/** Live Monad testnet deploy (Varnie, Aug 2026) — used when Vite env is empty. */
export const LIVE_REGISTRY =
  "0x1D582E8d297d47273B64B80BD93c159513FD97D9" as const satisfies Address;
export const LIVE_AIRDROP =
  "0x290fbF9fb7e06dF88A8C14546939db476888d9C4" as const satisfies Address;
/** Wallet used for the live SybilBlocked claim() proof. */
export const LIVE_PROBE_WALLET =
  "0xd8A08DF92652fF3992545D40DeDEe0FDA31f8871" as const satisfies Address;

/**
 * Prefer thirdweb, fall back if rate-limited.
 * Official testnet-rpc.monad.xyz is 15 rps/IP with a long 429 cooldown.
 */
export const RPC_URLS = [
  import.meta.env.VITE_MONAD_RPC || "https://10143.rpc.thirdweb.com",
  "https://rpc.ankr.com/monad_testnet",
  "https://monad-testnet.gateway.tenderly.co",
].filter((u, i, arr) => u && arr.indexOf(u) === i);

export const monadTestnet = defineChain({
  id: Number(import.meta.env.VITE_CHAIN_ID || 10143),
  name: "Monad Testnet",
  nativeCurrency: { name: "Monad", symbol: "MON", decimals: 18 },
  rpcUrls: {
    default: { http: RPC_URLS },
  },
  blockExplorers: {
    default: {
      name: "MonadVision",
      url: import.meta.env.VITE_EXPLORER_URL || "https://testnet.monadvision.com",
    },
  },
});

export const monadTransport = fallback(RPC_URLS.map((url) => http(url)));

function asAddress(value: string | undefined, fallbackAddr: Address): Address {
  const v = (value || "").trim();
  if (v.startsWith("0x") && v.length === 42) return v as Address;
  return fallbackAddr;
}

export function getRegistryAddress(): Address {
  return asAddress(import.meta.env.VITE_SYBIL_REGISTRY, LIVE_REGISTRY);
}

export function getAirdropAddress(): Address {
  return asAddress(import.meta.env.VITE_SYBIL_AIRDROP, LIVE_AIRDROP);
}

export function getProbeWalletFallback(): Address {
  return asAddress(import.meta.env.VITE_PROBE_WALLET, LIVE_PROBE_WALLET);
}

import { defineChain } from "viem";

export const monadTestnet = defineChain({
  id: Number(import.meta.env.VITE_CHAIN_ID || 10143),
  name: "Monad Testnet",
  nativeCurrency: { name: "Monad", symbol: "MON", decimals: 18 },
  rpcUrls: {
    default: {
      http: [import.meta.env.VITE_MONAD_RPC || "https://testnet-rpc.monad.xyz"],
    },
  },
  blockExplorers: {
    default: {
      name: "MonadVision",
      url: import.meta.env.VITE_EXPLORER_URL || "https://testnet.monadvision.com",
    },
  },
});

export function getRegistryAddress(): `0x${string}` | null {
  const fromEnv = (import.meta.env.VITE_SYBIL_REGISTRY || "").trim();
  if (fromEnv.startsWith("0x") && fromEnv.length === 42) {
    return fromEnv as `0x${string}`;
  }
  return null;
}

export function getAirdropAddress(): `0x${string}` | null {
  const fromEnv = (import.meta.env.VITE_SYBIL_AIRDROP || "").trim();
  if (fromEnv.startsWith("0x") && fromEnv.length === 42) {
    return fromEnv as `0x${string}`;
  }
  return null;
}

import { createPublicClient, http, type Address } from "viem";
import { sybilRegistryAbi } from "./abi";
import { getRegistryAddress, monadTestnet } from "./chain";

const client = createPublicClient({
  chain: monadTestnet,
  transport: http(),
});

export type ProbeResult = {
  thresholdBps: number;
  isSybil: boolean;
  riskBps: number;
};

export async function probeWallet(wallet: Address): Promise<ProbeResult> {
  const registry = getRegistryAddress();
  if (!registry) throw new Error("Set VITE_SYBIL_REGISTRY in dashboard/.env");

  const [thresholdBps, isSybil, riskBps] = await Promise.all([
    client.readContract({
      address: registry,
      abi: sybilRegistryAbi,
      functionName: "thresholdBps",
    }),
    client.readContract({
      address: registry,
      abi: sybilRegistryAbi,
      functionName: "isSybil",
      args: [wallet],
    }),
    client.readContract({
      address: registry,
      abi: sybilRegistryAbi,
      functionName: "riskBpsOf",
      args: [wallet],
    }),
  ]);

  return {
    thresholdBps: Number(thresholdBps),
    isSybil: Boolean(isSybil),
    riskBps: Number(riskBps),
  };
}

export function explorerAddressUrl(addr: string): string {
  const base = (import.meta.env.VITE_EXPLORER_URL || "https://testnet.monadvision.com").replace(
    /\/$/,
    ""
  );
  return `${base}/address/${addr}`;
}

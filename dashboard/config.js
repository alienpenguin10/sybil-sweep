// Sybil Sweep — shared chain config for React/viem + legacy HTML fallback.
// React app should mirror these via Vite env (VITE_SYBIL_REGISTRY, etc.).
window.SYBIL_CONFIG = {
  chainId: 10143,
  chainName: "Monad Testnet",
  rpcUrl: "https://testnet-rpc.monad.xyz",
  explorerUrl: "https://testnet.monadvision.com",
  // Set these once deploy lands (or via script/set_registry.py):
  registry: "", // e.g. "0xabc..."
  airdrop: "", // e.g. "0xdef..."
  // HTML fallback only: skip RPC if venue wifi dies mid-demo
  forceOffline: false,
};

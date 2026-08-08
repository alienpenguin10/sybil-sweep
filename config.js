// Sybil Sweep — local demo config (edit after Varnie deploys).
// Loaded by dashboard.html. Keep offline-safe defaults.
window.SYBIL_CONFIG = {
  chainId: 10143,
  chainName: "Monad Testnet",
  rpcUrl: "https://testnet-rpc.monad.xyz",
  explorerUrl: "https://testnet.monadvision.com",
  // Set these once deploy lands:
  registry: "", // e.g. "0xabc..."
  airdrop: "", // e.g. "0xdef..."
  // Optional: force offline UI even if registry is set (venue wifi fail)
  forceOffline: false,
};

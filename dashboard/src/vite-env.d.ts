/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_CHAIN_ID: string;
  readonly VITE_MONAD_RPC: string;
  readonly VITE_EXPLORER_URL: string;
  readonly VITE_SYBIL_REGISTRY: string;
  readonly VITE_SYBIL_AIRDROP: string;
  readonly VITE_PROBE_WALLET: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

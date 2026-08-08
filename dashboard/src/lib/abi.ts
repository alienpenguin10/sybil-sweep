export const sybilRegistryAbi = [
  {
    type: "function",
    name: "thresholdBps",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint16" }],
  },
  {
    type: "function",
    name: "isSybil",
    stateMutability: "view",
    inputs: [{ name: "wallet", type: "address" }],
    outputs: [{ name: "", type: "bool" }],
  },
  {
    type: "function",
    name: "riskBpsOf",
    stateMutability: "view",
    inputs: [{ name: "wallet", type: "address" }],
    outputs: [{ name: "", type: "uint16" }],
  },
  {
    type: "function",
    name: "verdict",
    stateMutability: "view",
    inputs: [{ name: "wallet", type: "address" }],
    outputs: [
      {
        name: "",
        type: "tuple",
        components: [
          { name: "clusterId", type: "uint32" },
          { name: "size", type: "uint32" },
          { name: "confidenceBps", type: "uint16" },
          { name: "funder", type: "address" },
          { name: "fundingWindowSecs", type: "uint32" },
          { name: "evidenceHash", type: "bytes32" },
          { name: "blockDetected", type: "uint64" },
        ],
      },
    ],
  },
] as const;

export type GraphNode = {
  id: string;
  cluster: number;
  funder: string;
  risk: number;
  isFarmTruth?: boolean;
  suspect?: boolean;
  isFunder?: boolean;
};

export type GraphLink = {
  source: string;
  target: string;
  kind: string;
};

export type ClusterCard = {
  clusterId: number;
  onchainClusterId: number;
  size: number;
  confidenceBps: number;
  funder: string;
  fundingWindowSecs: number;
  evidenceHash: string;
  sampleMember?: string;
};

export type GraphPayload = {
  generatedAt: number;
  metrics: {
    claimants: number;
    farms_truth: number;
    flagged: number;
    suspects?: number;
    precision: number;
    recall: number;
    tp: number;
    fp: number;
    fn: number;
  };
  clusters: ClusterCard[];
  nodes: GraphNode[];
  links: GraphLink[];
};

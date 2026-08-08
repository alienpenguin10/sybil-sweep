// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title SybilRegistry — on-chain sybil cluster attestations for airdrop enforcement
/// @notice Off-chain detector publishes cluster verdicts; airdrops call requireHuman().
contract SybilRegistry {
    struct Attestation {
        uint32 clusterId; // 1-indexed (0 = no cluster)
        uint32 size;
        uint16 confidenceBps; // 0..10000
        address funder;
        uint32 fundingWindowSecs;
        bytes32 evidenceHash;
        uint64 blockDetected;
    }

    address public owner;
    uint16 public thresholdBps = 7000; // 70%

    mapping(uint32 => Attestation) public clusters;
    mapping(address => uint32) public walletCluster; // 0 = none
    mapping(address => uint16) public riskBpsOf;

    event ThresholdUpdated(uint16 bps);
    event ClusterAttested(
        uint32 indexed clusterId,
        uint32 size,
        uint16 confidenceBps,
        address funder,
        bytes32 evidenceHash
    );
    event WalletTagged(address indexed wallet, uint32 indexed clusterId, uint16 confidenceBps);

    error NotOwner();
    error BadClusterId();
    error BadConfidence();
    error EmptyMembers();
    error SybilBlocked(address wallet, uint32 clusterId, uint16 confidenceBps);

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function setThreshold(uint16 bps) external onlyOwner {
        require(bps <= 10_000, "bps");
        thresholdBps = bps;
        emit ThresholdUpdated(bps);
    }

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "zero");
        owner = newOwner;
    }

    /// @notice Publish one cluster's verdict and tag member wallets.
    function attestCluster(
        uint32 clusterId,
        address[] calldata members,
        uint16 confidenceBps,
        address funder,
        uint32 fundingWindowSecs,
        bytes32 evidenceHash
    ) external onlyOwner {
        if (clusterId == 0) revert BadClusterId();
        if (confidenceBps > 10_000) revert BadConfidence();
        if (members.length == 0) revert EmptyMembers();

        Attestation memory att = Attestation({
            clusterId: clusterId,
            size: uint32(members.length),
            confidenceBps: confidenceBps,
            funder: funder,
            fundingWindowSecs: fundingWindowSecs,
            evidenceHash: evidenceHash,
            blockDetected: uint64(block.number)
        });
        clusters[clusterId] = att;

        for (uint256 i = 0; i < members.length; i++) {
            address w = members[i];
            walletCluster[w] = clusterId;
            riskBpsOf[w] = confidenceBps;
            emit WalletTagged(w, clusterId, confidenceBps);
        }

        emit ClusterAttested(clusterId, att.size, confidenceBps, funder, evidenceHash);
    }

    function isSybil(address wallet) public view returns (bool) {
        return riskBpsOf[wallet] >= thresholdBps;
    }

    function verdict(address wallet) external view returns (Attestation memory) {
        uint32 cid = walletCluster[wallet];
        if (cid == 0) {
            return Attestation({
                clusterId: 0,
                size: 0,
                confidenceBps: 0,
                funder: address(0),
                fundingWindowSecs: 0,
                evidenceHash: bytes32(0),
                blockDetected: 0
            });
        }
        return clusters[cid];
    }

    /// @notice Drop into Airdrop.claim() — reverts if wallet is flagged at/above threshold.
    function requireHuman(address wallet) external view {
        if (isSybil(wallet)) {
            revert SybilBlocked(wallet, walletCluster[wallet], riskBpsOf[wallet]);
        }
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script, console2} from "forge-std/Script.sol";
import {SybilRegistry} from "../contracts/SybilRegistry.sol";

/// @notice Critical-path smoke: tag ONE wallet so Airdrop.claim() reverts via requireHuman.
/// @dev Full cluster dump is NOT here — use `python3 script/attest.py` after reject is proven.
///
///   forge script script/AttestOne.s.sol:AttestOne --rpc-url $MONAD_RPC --broadcast
contract AttestOne is Script {
    function run() external {
        uint256 pk = vm.envUint("PRIVATE_KEY");
        address registryAddr = vm.envAddress("SYBIL_REGISTRY");

        uint32 clusterId = uint32(vm.envUint("CLUSTER_ID"));
        uint16 confidenceBps = uint16(vm.envUint("CONFIDENCE_BPS"));
        address funder = vm.envAddress("FUNDER");
        uint32 window = uint32(vm.envUint("FUNDING_WINDOW_SECS"));
        bytes32 evidenceHash = vm.envBytes32("EVIDENCE_HASH");
        address member = vm.envAddress("MEMBER");

        address[] memory members = new address[](1);
        members[0] = member;

        vm.startBroadcast(pk);
        SybilRegistry(registryAddr).attestCluster(
            clusterId, members, confidenceBps, funder, window, evidenceHash
        );
        console2.log("Attested cluster", clusterId);
        console2.log("Tagged member", member);
        vm.stopBroadcast();
    }
}

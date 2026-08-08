// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script, console2} from "forge-std/Script.sol";
import {SybilRegistry} from "../contracts/SybilRegistry.sol";
import {Airdrop} from "../contracts/Airdrop.sol";

/// @notice Deploy SybilRegistry + demo Airdrop, set claim to 0.01 MON, fund 0.1 MON.
/// @dev Deployer needs ≥0.1 MON (+ gas). Beat-4 contrast: sybil reverts, human gets paid.
contract Deploy is Script {
    function run() external {
        uint256 pk = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(pk);

        SybilRegistry reg = new SybilRegistry();
        Airdrop drop = new Airdrop(address(reg));

        drop.setClaimAmount(0.01 ether);
        drop.fund{value: 0.1 ether}();

        console2.log("SybilRegistry", address(reg));
        console2.log("Airdrop", address(drop));
        console2.log("claimAmount wei", drop.claimAmount());
        console2.log("airdrop balance wei", address(drop).balance);

        vm.stopBroadcast();
    }
}

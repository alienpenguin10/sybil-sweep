// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script, console2} from "forge-std/Script.sol";
import {SybilRegistry} from "../contracts/SybilRegistry.sol";
import {Airdrop} from "../contracts/Airdrop.sol";

/// @notice Deploy SybilRegistry + demo Airdrop. Fund airdrop separately for live claims.
contract Deploy is Script {
    function run() external {
        uint256 pk = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(pk);

        SybilRegistry reg = new SybilRegistry();
        Airdrop drop = new Airdrop(address(reg));

        console2.log("SybilRegistry", address(reg));
        console2.log("Airdrop", address(drop));

        vm.stopBroadcast();
    }
}

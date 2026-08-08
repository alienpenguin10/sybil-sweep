// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {SybilRegistry} from "./SybilRegistry.sol";

/// @title Demo airdrop that enforces SybilRegistry.requireHuman
contract Airdrop {
    SybilRegistry public immutable registry;
    mapping(address => bool) public claimed;
    uint256 public claimAmount = 1 ether;
    address public owner;

    error AlreadyClaimed();
    error TransferFailed();

    event Claimed(address indexed wallet, uint256 amount);

    constructor(address registry_) {
        registry = SybilRegistry(registry_);
        owner = msg.sender;
    }

    receive() external payable {}

    function claim() external {
        registry.requireHuman(msg.sender);
        if (claimed[msg.sender]) revert AlreadyClaimed();
        claimed[msg.sender] = true;

        (bool ok, ) = msg.sender.call{value: claimAmount}("");
        if (!ok) revert TransferFailed();
        emit Claimed(msg.sender, claimAmount);
    }

    function fund() external payable {}

    function setClaimAmount(uint256 amt) external {
        require(msg.sender == owner, "owner");
        claimAmount = amt;
    }
}

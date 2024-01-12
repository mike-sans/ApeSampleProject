// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6 <0.9.0;

import "./interfaces/AggregatorV3Interface.sol";

contract FundMe {
    address owner;

    address[] public funders;

    // uint256 public bungo;

    constructor() {
        owner = msg.sender;
    }

    mapping(address => uint256) public addressToAmountFunded;

    //uint256 public bunny;

    function fund() public payable {
        //now we want to require a minimum payment as defined in $USD, so we need the conversion rate: Oracle time!
        uint256 minimumUSD = 150 * 10 ** 18;
        // //bunny = msg.value;
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );

        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
        // bungo = msg.value;
    }

    // function viewshit() public view returns (uint256) {
    //     // uint256 minimumUSD = 1 * 10 ** 18;
    //     // return (minimumUSD, getConversionRate(bungo));
    //     return uint256((getConversionRate(bungo)));
    //     // return bungo;
    // }

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e
        );
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e
        );
        (, int256 answer, , , ) = priceFeed.latestRoundData();

        return uint256(answer * (10 ** 10));
    }

    function getConversionRate(
        uint256 ethAmount
    ) public view returns (uint256) {
        uint256 ethPrice = getPrice();

        uint256 ethAmountInUSD = (ethPrice * ethAmount) / (10 ** 18);
        return ethAmountInUSD;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public onlyOwner {
        //require(msg.sender == owner);
        address payable payableOwner = payable(msg.sender);
        payableOwner.transfer(address(this).balance);

        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            addressToAmountFunded[funders[funderIndex]] = 0;
        }
        funders = new address[](0);
    }
}

// SPDX-License-Identifier: MIT
pragma solidity >=0.6.6 <0.9.0;

import "./interfaces/AggregatorV3Interface.sol";

contract FundMe {
    address owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    mapping(address => uint256) public addressToAmountFunded;

    uint256 public minimumUSD = uint256(1.50 * 10 ** 18);

    //uint256 public bunny;

    function fund() public payable {
        //now we want to require a minimum payment as defined in $USD, so we need the conversion rate: Oracle time!
        // uint256 minimumUSD = uint256(1.50 * 10 ** 18);
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );

        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 price = getPrice();
        uint256 precision = 1 * 10 ** 18;
        // return uint256((minimumUSD * precision) / price);
        return price;
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
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

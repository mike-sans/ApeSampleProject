// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0;

contract SimpleStorage {
    //this will get initialized to 0!
    uint256 public favoriteNumber;

    //struct is essentially creating a new object type
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People public person = People({favoriteNumber: 12, name: "Johnny"});

    People[] public people;

    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public returns (uint256) {
        favoriteNumber = _favoriteNumber;
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

    //two keywords that don't use transactions: 'view' and 'pure'
    function viewFunction() public view returns (uint256) {
        return favoriteNumber;
    }

    function pureFunction(uint256 bunny) public pure {
        bunny + bunny;
    }
}

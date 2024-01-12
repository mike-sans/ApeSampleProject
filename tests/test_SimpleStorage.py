from ape import networks, accounts, project


def test_deploy(accounts):
    # Arrange
    # account = accounts.load("my-account")
    # account = accounts.test_accounts[0]
    account = accounts[0]

    # Act
    simpleStorage = account.deploy(project.SimpleStorage)
    startingValue = simpleStorage.viewFunction()
    expected = 0

    # Assert
    assert startingValue == expected


def test_updating_storage(accounts):
    # Arrange
    # account = accounts.load("my-account")
    # account = accounts.test_accounts[0]
    account = accounts[0]
    simpleStorage = account.deploy(project.SimpleStorage)

    # Act
    expected = 15
    simpleStorage.store(expected, sender=account)

    # Assert
    assert simpleStorage.viewFunction() == expected

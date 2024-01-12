from ape import networks, accounts, project


def get_account():
    account = []
    if networks.provider.name == "test":
        accountnum = 1
        for i in range(accountnum):
            account.append(accounts.test_accounts[i])
    else:
        account.append(accounts.load("myAccount"))
        # account.append(accounts.load("myAccount2"))
        # etc.
    return account


def deploy_simple_storage():
    # Load your account by alias
    # account = accounts.load("my-account")
    account = get_account()

    if networks.network.name != "mainnet":
        account[0].set_autosign(True)

    # print(account)
    # print(account2)
    # balance_wei = account[0].balance
    # balance_eth = balance_wei / (10**18)
    # print(f"Balance: {balance_eth} Eth")

    # # two ways to do the same thing
    # simpleStorage = account[0].deploy(project.SimpleStorage)
    simpleStorage = project.SimpleStorage.deploy(sender=account[0])
    # print(simpleStorage)

    storedValue = simpleStorage.viewFunction()
    print(storedValue)

    transaction = simpleStorage.store(17, sender=account[0])

    storedValue = simpleStorage.viewFunction()
    print(storedValue)

    # max_fee="45 gwei", sender=account[0], gas_limit=800000
    # )


def main():
    deploy_simple_storage()

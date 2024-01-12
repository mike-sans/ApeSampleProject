from ape import networks, accounts, project


def get_account():
    account = []
    if networks.provider.name == "test":
        accountnum = 1
        for i in range(accountnum):
            account.append(accounts.test_accounts[i])
    else:
        account.append(accounts.load("myAccount"))
    return account


def read():
    account = get_account()
    simpleInstance = project.SimpleStorage.deployments[-1]
    print(simpleInstance.viewFunction())


def main():
    read()

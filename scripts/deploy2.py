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


def deploy_fund_me():
    account = get_account()
    if networks.network.name != "mainnet":
        account[0].set_autosign(True)


def main():
    deploy_fund_me()

from ape import networks, accounts, project
from scripts.helpfulScripts import *


def deploy_fund_me(daccount=False):
    if not daccount:
        daccount = get_account()[0]
    if networks.active_provider.network.name in ("sepolia", "goerli"):
        daccount[0].set_autosign(True)

    # this will get info from chainlink or deploy a mock chain if in a test network
    price_feed = get_or_deploy_contract("AggregatorV3Interface")
    publishStat = True
    if networks.active_provider.network.name in ("local", "mainnet-fork"):
        publishStat = False
    fundMe = project.FundMe.deploy(
        price_feed.address, sender=daccount, publish=publishStat
    )
    print(f"Contract deployed to {fundMe.address}")
    return fundMe


def fund_fund_me(faccount=False, entrance_fee=False):
    if not faccount:
        faccount = get_account()[1]
    fundMe = project.FundMe.deployments[-1]
    print(networks.active_provider.network.name)
    if not entrance_fee:
        entrance_fee = fundMe.getEntranceFee() + 100
    tx = fundMe.fund(sender=faccount, value=entrance_fee)
    print(f"Contract funded, txn hash:{tx}")
    return entrance_fee


def withdraw_fund_me(waccount=False):
    if not waccount:
        waccount = get_account()[0]
    fundMe = project.FundMe.deployments[-1]
    tx = fundMe.withdraw(sender=waccount)
    print(f"Contract withdrawn from, txn hash:{tx}")


def main():
    deploy_fund_me()

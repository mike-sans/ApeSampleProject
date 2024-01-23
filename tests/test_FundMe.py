import pytest
from ape import accounts, project, networks, exceptions
from scripts.helpfulScripts import *
from scripts.FundMeInteract import deploy_fund_me, fund_fund_me, withdraw_fund_me


@pytest.fixture
def owner():
    account = get_account()
    return account[0]


@pytest.fixture
def receiver():
    account = get_account()
    return account[1]


@pytest.fixture
def receiver2():
    account = get_account()
    return account[2]


def test_FundMeDeploy(owner):
    # account = get_account()
    # account = accounts[0]
    # an = networks.active_provider.network.name
    # print(account)

    if (
        networks.active_provider.network.name
        not in LOCAL_CHAIN_NAMES + FORKED_CHAIN_NAMES
    ):
        pytest.skip("Only for local/forked testing")

    # price_feed = get_or_deploy_contract("AggregatorV3Interface")
    # fundMe = project.FundMe.deploy(price_feed.address, sender=owner)
    fundMe = deploy_fund_me(owner)
    assert fundMe == fundMe

    # entrance_fee = fundMe.getEntranceFee() + 100
    # print("Entrane fee is:")
    # print18(entrance_fee)

    # tx = fundMe.fund(sender=owner, value=entrance_fee, required_confirmations=1)
    # tx = fundMe.fund(sender=owner, value=entrance_fee)
    # print("Balane before is:")
    # print18(owner.balance)
    # assert fundMe.addressToAmountFunded(owner.address) == entrance_fee

    # tx2 = fundMe.withdraw(sender=owner, required_confirmations=1)
    # tx2 = fundMe.withdraw(sender=owner)
    # print("Balane after is:")
    # print18(owner.balance)
    # assert fundMe.addressToAmountFunded(owner.address) == 0


# dependent on test_FundMeDeploy being run right before it
def test_FundMeFund(owner, receiver, receiver2):
    if (
        networks.active_provider.network.name
        not in LOCAL_CHAIN_NAMES + FORKED_CHAIN_NAMES
    ):
        pytest.skip("Only for local/forked testing")

    fundMe = project.FundMe.deployments[-1]
    # entrance_fee = fundMe.getEntranceFee() + 100
    fundAmount = fund_fund_me(receiver)
    # fund_fund_me(receiver, entrance_fee)

    assert fundMe.addressToAmountFunded(receiver.address) == fundAmount


# dependent on test_FundMeDeploy being run right before it
def test_FundMeUnauthWithdraw(owner, receiver, receiver2):
    if (
        networks.active_provider.network.name
        not in LOCAL_CHAIN_NAMES + FORKED_CHAIN_NAMES
    ):
        pytest.skip("Only for local/forked testing")

    # price_feed = get_or_deploy_contract("AggregatorV3Interface")
    # fund_me = project.FundMe.deploy(price_feed.address, sender=owner)
    with pytest.raises(exceptions.VirtualMachineError):
        withdraw_fund_me(receiver)


# dependent on test_FundMeDeploy and test_FundMeFund being run right before it
def test_FundMeAuthWithdraw(owner, receiver, receiver2):
    if (
        networks.active_provider.network.name
        not in LOCAL_CHAIN_NAMES + FORKED_CHAIN_NAMES
    ):
        pytest.skip("Only for local/forked testing")

    fundMe = project.FundMe.deployments[-1]
    origBalance = fundMe.balance

    withdraw_fund_me(owner)

    assert origBalance > 0 and fundMe.balance == 0

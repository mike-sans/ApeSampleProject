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
    if (
        networks.active_provider.network.name
        not in LOCAL_CHAIN_NAMES + FORKED_CHAIN_NAMES
    ):
        pytest.skip("Only for local/forked testing")
    fundMe = deploy_fund_me(owner)
    assert fundMe == fundMe


# dependent on test_FundMeDeploy being run right before it
def test_FundMeFund(owner, receiver, receiver2):
    if (
        networks.active_provider.network.name
        not in LOCAL_CHAIN_NAMES + FORKED_CHAIN_NAMES
    ):
        pytest.skip("Only for local/forked testing")

    fundMe = project.FundMe.deployments[-1]
    fundAmount = fund_fund_me(receiver)

    assert fundMe.addressToAmountFunded(receiver.address) == fundAmount


# dependent on test_FundMeDeploy being run right before it
def test_FundMeUnauthWithdraw(owner, receiver, receiver2):
    if (
        networks.active_provider.network.name
        not in LOCAL_CHAIN_NAMES + FORKED_CHAIN_NAMES
    ):
        pytest.skip("Only for local/forked testing")

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

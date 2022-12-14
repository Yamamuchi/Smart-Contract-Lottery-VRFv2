# 0.019
# 19000000000000000000
from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    print(lottery.getEntranceFee())
    assert lottery.getEntranceFee() > Web3.toWei(0.030, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.032, "ether")

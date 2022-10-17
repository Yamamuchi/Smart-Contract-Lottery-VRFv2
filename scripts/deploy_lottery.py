from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time


def deploy_lottery():
    account = get_account()
    print(account)
    print(get_contract("vrf_coordinator").address)
    Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        config["networks"][network.show_active()]["subscription_id"],
        config["networks"][network.show_active()]["key_hash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery!")


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery is started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]

    lottery.addContractAsConsumer({"from": account})

    # fund subscription
    # end the lottery
    # fund_with_link()
    ending_tx = lottery.endLottery({"from": account})
    ending_tx.wait(1)
    time.sleep(100)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    print("Ending lottery")
    end_lottery()
    print("Ended lottery")

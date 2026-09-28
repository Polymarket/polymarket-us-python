"""Typed consumers of the current private position and balance wire payloads."""

from polymarket_us.types import UserBalance, UserPosition
from polymarket_us.websocket import AccountBalanceSnapshot, AccountBalanceUpdate, PositionUpdate

position: PositionUpdate = {
    "requestId": "positions",
    "subscriptionType": "SUBSCRIPTION_TYPE_POSITION",
    "positionSubscription": {
        "beforePosition": None,
        "afterPosition": {
            "netPosition": "2",
            "cost": None,
            "marketMetadata": None,
            "cashValue": None,
            "updateTime": None,
        },
        "updateTime": None,
        "entryType": "LEDGER_ENTRY_TYPE_ORDER_EXECUTION",
        "tradeId": "trade",
        "referenceId": "",
        "description": "",
        "allocationGroupId": "",
        "transferReferenceTradeIds": [],
        "shortTransfer": False,
        "updateTradeDate": None,
    },
}
balances: AccountBalanceSnapshot = {
    "requestId": "balance",
    "subscriptionType": "SUBSCRIPTION_TYPE_ACCOUNT_BALANCE",
    "accountBalancesSnapshot": {"balances": []},
}
balance: AccountBalanceUpdate = {
    "requestId": "balance",
    "subscriptionType": "SUBSCRIPTION_TYPE_ACCOUNT_BALANCE",
    "accountBalancesUpdate": {
        "balanceChange": {
            "beforeBalance": None,
            "afterBalance": {
                "currentBalance": 0,
                "buyingPower": 0,
                "currency": "USD",
                "lastUpdated": None,
                "pendingWithdrawals": [{"creationTime": None}],
            },
            "description": "",
            "updateTime": None,
            "modifiedSecurityId": "",
            "entryType": "LEDGER_ENTRY_TYPE_DEPOSIT",
            "accountName": "synthetic-account",
            "id": "synthetic-entry",
        }
    },
}


def read_position(data: PositionUpdate) -> UserPosition | None:
    return data["positionSubscription"]["afterPosition"]


def read_balances(data: AccountBalanceSnapshot) -> list[UserBalance]:
    return data["accountBalancesSnapshot"]["balances"]


def read_balance(data: AccountBalanceUpdate) -> float | None:
    after = data["accountBalancesUpdate"]["balanceChange"]["afterBalance"]
    return after.get("buyingPower") if after is not None else None

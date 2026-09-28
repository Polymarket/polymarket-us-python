"""Typed consumers of the current private position and balance wire payloads."""

from decimal import Decimal

from polymarket_us.types import (
    Amount,
    ComboLegDetail,
    ComboLegState,
    ComboSettlement,
    ImageDisplayType,
    MarketMetadata,
    MarketProvider,
    MarketTeamProvider,
    OutcomeSide,
    ResolvedColor,
    Subject,
    Team,
    UserBalance,
    UserPosition,
)
from polymarket_us.websocket import AccountBalanceSnapshot, AccountBalanceUpdate, PositionUpdate

provider: MarketProvider = "PROVIDER_GRID"
team_provider: MarketTeamProvider = {"provider": provider, "providerId": "synthetic-provider-id"}
colors: ResolvedColor = {"light": "#000000", "dark": "#ffffff"}
image_display: ImageDisplayType = "IMAGE_DISPLAY_TYPE_LOGO"
team: Team = {
    "id": 1,
    "name": "Synthetic team",
    "providerId": 0,
    "ordering": "home",
    "longIcon": "long.png",
    "shortIcon": "short.png",
    "displayAbbreviation": "SYN",
    "ranking": "9007199254740993",
    "conference": "synthetic-conference",
    "providerIds": [team_provider],
    "longIconDark": "long-dark.png",
    "shortIconDark": "short-dark.png",
    "color": colors,
    "imageDisplayType": image_display,
}
subject: Subject = {"id": 1, "name": "Synthetic player", "subjectType": "player"}
settlement: ComboSettlement = {
    "settlementPrice": {"value": "1", "currency": "USD"},
    "settlementSetTime": None,
}
leg: ComboLegDetail = {
    "slug": "synthetic-leg",
    "teamId": 1,
    "team": team,
    "subject": subject,
    "outcomeSide": "OUTCOME_SIDE_YES",
    "eventStartTime": None,
    "indicativePrice": None,
    "settlement": settlement,
    "state": "COMBO_LEG_STATE_WON",
}
pending_leg: ComboLegDetail = {
    "slug": "pending-leg",
    "outcomeSide": "OUTCOME_SIDE_NO",
    "eventStartTime": "2026-09-28T00:00:00Z",
    "indicativePrice": {"value": "0.25", "currency": "USD"},
    "state": "COMBO_LEG_STATE_PENDING",
}
position: PositionUpdate = {
    "requestId": "positions",
    "subscriptionType": "SUBSCRIPTION_TYPE_POSITION",
    "positionSubscription": {
        "beforePosition": None,
        "afterPosition": {
            "netPosition": "2",
            "cost": None,
            "marketMetadata": {"eventId": "synthetic-event", "team": team, "subject": subject},
            "cashValue": None,
            "updateTime": None,
            "avgPx": None,
            "fees": None,
            "baseCost": None,
            "costPerShare": None,
            "netPositionDecimal": "2.25",
            "qtyBoughtDecimal": "3.5",
            "qtySoldDecimal": "1.25",
            "bodPositionDecimal": "0.5",
            "qtyAvailableDecimal": "1.75",
            "comboLegDetails": [leg, pending_leg],
            "positionId": "synthetic-user:LONG:synthetic-market",
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
                "balanceReservation": 0,
                "depositReservation": 0,
                "bonusReservation": 0,
                "displayedBonus": 0,
                "displayedAvailableSoon": 0,
                "displayedCash": 0,
                "availableToWithdraw": 0,
                "bonusHold": 0,
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


def read_exact_quantity(data: PositionUpdate) -> Decimal | None:
    after = data["positionSubscription"]["afterPosition"]
    return Decimal(after["netPositionDecimal"]) if after is not None else None


def read_available_quantity(data: UserPosition) -> str | None:
    return data.get("qtyAvailableDecimal")


def read_position_price(data: UserPosition) -> Amount | None:
    return data.get("avgPx")


def read_combo_state(data: UserPosition) -> list[tuple[OutcomeSide, ComboLegState]]:
    return [(item["outcomeSide"], item["state"]) for item in data.get("comboLegDetails", [])]


def read_combo_settlement(data: ComboLegDetail) -> Amount | None:
    value = data.get("settlement")
    return value["settlementPrice"] if value is not None else None


def read_displayed_cash(data: AccountBalanceUpdate) -> float | None:
    after = data["accountBalancesUpdate"]["balanceChange"]["afterBalance"]
    return after.get("displayedCash") if after is not None else None


def read_combo_team_provider(data: ComboLegDetail) -> str | None:
    value = data.get("team")
    providers = value.get("providerIds", []) if value is not None else []
    return providers[0]["providerId"] if providers else None


def read_combo_team_rank(data: ComboLegDetail) -> str | None:
    value = data.get("team")
    return value.get("ranking") if value is not None else None


def read_combo_team_color(data: ComboLegDetail) -> str | None:
    value = data.get("team")
    color = value.get("color") if value is not None else None
    return color["dark"] if color is not None else None


def read_position_metadata(data: UserPosition) -> MarketMetadata | None:
    return data.get("marketMetadata")


def read_metadata(data: MarketMetadata) -> tuple[str | None, Team | None, Subject | None]:
    return data.get("eventId"), data.get("team"), data.get("subject")

"""Account type definitions."""

from typing import TypedDict


class PendingWithdrawal(TypedDict, total=False):
    """Pending withdrawal details."""

    id: str
    name: str
    balance: float
    description: str
    acknowledged: bool
    bank_id: str
    creation_time: str
    destination_account_name: str


class UserBalance(TypedDict, total=False):
    """User account balance."""

    current_balance: float
    currency: str
    last_updated: str
    buying_power: float
    asset_notional: float
    asset_available: float
    pending_credit: float
    open_orders: float
    unsettled_funds: float
    pending_withdrawals: list[PendingWithdrawal]
    margin_requirement: float
    balance_reservation: float


class GetAccountBalancesResponse(TypedDict):
    """Response for getting account balances."""

    balances: list[UserBalance]

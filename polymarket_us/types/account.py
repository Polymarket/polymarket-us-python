"""Account type definitions."""

from typing import TypedDict


class PendingWithdrawal(TypedDict, total=False):
    """Pending withdrawal details."""

    id: str
    name: str
    balance: float
    description: str
    acknowledged: bool
    bankId: str
    creationTime: str
    destinationAccountName: str


class UserBalance(TypedDict, total=False):
    """User account balance."""

    currentBalance: float
    currency: str
    lastUpdated: str
    buyingPower: float
    assetNotional: float
    assetAvailable: float
    pendingCredit: float
    openOrders: float
    unsettledFunds: float
    pendingWithdrawals: list[PendingWithdrawal]
    marginRequirement: float
    balanceReservation: float


class GetAccountBalancesResponse(TypedDict):
    """Response for getting account balances."""

    balances: list[UserBalance]

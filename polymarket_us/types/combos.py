"""Combo leg display type definitions."""

from typing import Literal, TypedDict

from polymarket_us.types.common import Amount
from polymarket_us.types.markets import Subject, Team
from polymarket_us.types.orders import OutcomeSide

ComboLegState = Literal[
    "COMBO_LEG_STATE_UNSPECIFIED",
    "COMBO_LEG_STATE_PENDING",
    "COMBO_LEG_STATE_WON",
    "COMBO_LEG_STATE_LOST",
    "COMBO_LEG_STATE_INDETERMINATE",
]


class ComboSettlement(TypedDict, total=False):
    """Settlement display data for a combo leg."""

    settlementPrice: Amount
    settlementSetTime: str | None


class ComboLegDetail(TypedDict, total=False):
    """Display data for a position's combo leg."""

    slug: str
    icon: str
    title: str
    outcome: str
    eventSlug: str
    teamId: int
    team: Team
    subject: Subject
    eventId: str
    outcomeSide: OutcomeSide
    eventGroupTitle: str
    eventStartTime: str | None
    live: bool
    indicativePrice: Amount | None
    settlement: ComboSettlement
    state: ComboLegState

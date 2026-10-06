"""RFQ history and private stream types."""

from typing import Literal, TypedDict

RFQStatus = Literal["RFQ_STATUS_UNSPECIFIED", "RFQ_STATUS_OPEN", "RFQ_STATUS_CLOSED"]

QuoteStatus = Literal[
    "QUOTE_STATUS_UNDEFINED",
    "QUOTE_STATUS_ACTIVE",
    "QUOTE_STATUS_CONFIRMED",
    "QUOTE_STATUS_DELETED",
    "QUOTE_STATUS_ACCEPTED",
    "QUOTE_STATUS_EXECUTED",
]

RFQSide = Literal["SIDE_UNDEFINED", "SIDE_BUY", "SIDE_SELL"]


class _OptionalRFQComboLeg(TypedDict, total=False):
    settlementPrice: str


class RFQComboLeg(_OptionalRFQComboLeg):
    """A leg in an RFQ's combo market."""

    symbol: str
    side: RFQSide


class _OptionalRFQ(TypedDict, total=False):
    qtyDecimal: str
    cashOrderQty: str
    tickSize: float


class RFQ(_OptionalRFQ):
    """RFQ details emitted by the private stream."""

    id: str
    symbol: str
    rfqCreatorUserId: str
    createdTime: str | None
    restRemainder: bool
    status: RFQStatus
    updatedTime: str | None
    comboLegs: list[RFQComboLeg]


class _OptionalQuote(TypedDict, total=False):
    rfqCashOrderQty: str
    rfqCreatorOrderId: str
    creatorOrderId: str


class Quote(_OptionalQuote):
    """Quote details, including lifecycle timestamps and exact decimal strings."""

    id: str
    rfqId: str
    creatorRfqUserId: str
    symbol: str
    status: QuoteStatus
    createdTime: str | None
    buyPrice: str
    sellPrice: str
    restRemainder: bool
    postOnly: bool
    rfqCreatorUserId: str
    buyQtyDecimal: str
    sellQtyDecimal: str
    updatedTime: str | None
    acceptedSide: RFQSide
    acceptedTime: str | None
    confirmedTime: str | None
    confirmationDeadline: str | None
    executionDeadline: str | None
    executedTime: str | None


class RFQTrade(TypedDict):
    """An anonymous original fill; later corrections and busts are not reflected."""

    tradeId: str
    symbol: str
    price: str
    qtyDecimal: str
    aggressorSide: RFQSide
    executedTime: str | None


class GetRFQTradesParams(TypedDict, total=False):
    """History filters; repeat the same filters and limit with each cursor."""

    limit: int
    cursor: str
    startTime: str
    endTime: str
    symbol: str


class GetRFQTradesResponse(TypedDict):
    """A history page; continue nonempty cursors even when trades is empty."""

    trades: list[RFQTrade]
    cursor: str

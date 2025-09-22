from typing import Literal, Optional, Tuple

from personal_screener.schemas.quote import Quote

Number = int | float

MarketCap = Literal["SMALL", "MID", "LARGE"]
SMALL: MarketCap = "SMALL"
MID: MarketCap = "MID"
LARGE: MarketCap = "LARGE"

OHLC = Literal["OPEN", "HIGH", "LOW", "CLOSE"]
OPEN: OHLC = "OPEN"
HIGH: OHLC = "HIGH"
LOW: OHLC = "LOW"
CLOSE: OHLC = "CLOSE"

# === Operator Conditions ==========
Operator = Literal["GT", "LT", "GTE", "LTE", "EQ"]
GT: Operator = "GT"
LT: Operator = "LT"
GTE: Operator = "GTE"
LTE: Operator = "LTE"
EQ: Operator = "EQ"

BetweenCondition = Tuple[Optional[Number], Optional[Number]]
OperatorCondition = Tuple[Operator, Number]

# === Quotes ====================
QuoteData = dict[str, Quote]
QuoteScores = dict[str, int]

from typing import Literal, Optional, Tuple

from personal_screener.schemas.price_value import PriceValue
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

PriceOperand = Number | OHLC | PriceValue

# === Operator Conditions ==========
Operator = Literal["GT", "LT", "GTE", "LTE", "EQ"]
GT: Operator = "GT"
LT: Operator = "LT"
GTE: Operator = "GTE"
LTE: Operator = "LTE"
EQ: Operator = "EQ"

BetweenCondition = Tuple[Optional[Number], Optional[Number]]
OperatorCondition = Tuple[Operator, Number]

PriceOperatorCondition = Tuple[Operator, PriceOperand]
PriceBetweenCondition = Tuple[Optional[PriceOperand], Optional[PriceOperand]]

# === Quotes ====================
QuoteData = dict[str, Quote]
QuoteScores = dict[str, int]

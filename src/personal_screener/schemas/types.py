from typing import Literal, Optional, Tuple

from personal_screener.schemas.price_value import PriceValue
from personal_screener.schemas.quote import Quote

Number = int | float
OHLC = Literal["OPEN", "HIGH", "LOW", "CLOSE"]
PriceOperand = Number | OHLC | PriceValue
MarketCap = Literal["SMALL", "MID", "LARGE"]

# === Operator Conditions ==========
Operator = Literal["GT", "LT", "GTE", "LTE", "EQ"]

BetweenCondition = Tuple[Optional[Number], Optional[Number]]
OperatorCondition = Tuple[str, Number]

PriceOperatorCondition = Tuple[str, PriceOperand]
PriceBetweenCondition = Tuple[Optional[PriceOperand], Optional[PriceOperand]]

# === Quotes ====================
QuoteData = dict[str, Quote]
QuoteScores = dict[str, int]

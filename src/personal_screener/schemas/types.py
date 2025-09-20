from typing import Literal, Optional, Tuple

from personal_screener.schemas.quote import Quote

Number = int | float
OHLC = Literal["OPEN", "HIGH", "LOW", "CLOSE"]
OHLCNumber = float | OHLC
MarketCap = Literal["SMALL", "MID", "LARGE"]

# === Operator Conditions ==========
Operator = Literal["GT", "LT", "GTE", "LTE", "EQ"]
BetweenCondition = Tuple[Optional[Number], Optional[Number]]
OperatorCondition = Tuple[str, Number]

PriceOperatorCondition = Tuple[str, OHLCNumber]
PriceBetweenCondition = Tuple[Optional[OHLCNumber], Optional[OHLCNumber]]

# === Quotes ====================
QuoteData = dict[str, Quote]
QuoteScores = dict[str, int]

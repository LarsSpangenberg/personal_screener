from typing import Literal, Tuple

from personal_screener.schemas.quote import Quote

Number = int | float
MarketCap = Literal["SMALL", "MID", "LARGE"]

# === Operator Conditions ==========
Operator = Literal["GT", "LT", "GTE", "LTE", "EQ"]
BetweenCondition = Tuple[Number | None, Number | None]
OperatorCondition = Tuple[str, Number]

# === Quotes ====================
QuoteData = dict[str, Quote]

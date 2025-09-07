from dataclasses import dataclass
from typing import Literal, Optional

Operator = Literal["GT", "LT", "GTE", "LTE", "EQ"]
MarketCap = Literal["LOW", "MID", "HIGH"]
OptionalPrice = float | None


@dataclass
class ScreenerFilters:
    """
    Operators: "GT", "LT", "GTE", "LTE", "EQ"

    *'BTWN' is handled automatically for ranges. Use None for one of the range
    values to apply GTE or LTE
    """
    market_cap: Optional[MarketCap] = None
    avg_volume: Optional[tuple[str, int]] = None
    price_range: Optional[tuple[OptionalPrice, OptionalPrice]] = None
    ma50: Optional[tuple[str, float]] = None
    ma200: Optional[tuple[str, float]] = None

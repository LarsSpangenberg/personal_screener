from dataclasses import dataclass
from typing import Optional

from personal_screener.schemas.types import (
    BetweenCondition, MarketCap,
    OperatorCondition,
)


@dataclass
class ScreenerFilters:
    """
    Operators: "GT", "LT", "GTE", "LTE", "EQ"

    *'BTWN' is handled automatically for ranges. Use None for one of the range
    values to apply GTE or LTE
    """
    market_cap: Optional[MarketCap] = None
    avg_vol: Optional[OperatorCondition] = None
    price_range: Optional[BetweenCondition] = None

    ma3: Optional[OperatorCondition] = None
    ma10: Optional[OperatorCondition] = None
    ma20: Optional[OperatorCondition] = None
    ma50: Optional[OperatorCondition] = None
    ma200: Optional[OperatorCondition] = None
    rsi: Optional[OperatorCondition] = None

    # signals
    is_3ma_trending_up: Optional[bool] = None
    is_10ma_trending_up: Optional[bool] = None

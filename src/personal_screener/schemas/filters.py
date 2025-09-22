from dataclasses import dataclass
from typing import Optional

from personal_screener.schemas.price_value import (
    PriceBetweenCondition,
    PriceOperatorCondition,
)
from personal_screener.schemas.types import (
    MarketCap,
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
    price_range: Optional[PriceBetweenCondition] = None

    ma3: Optional[PriceOperatorCondition] = None
    ma10: Optional[PriceOperatorCondition] = None
    ma20: Optional[PriceOperatorCondition] = None
    ma50: Optional[PriceOperatorCondition] = None
    ma200: Optional[PriceOperatorCondition] = None
    rsi: Optional[OperatorCondition] = None

    # signals
    is_3ma_trending_up: Optional[bool] = None
    is_10ma_trending_up: Optional[bool] = None

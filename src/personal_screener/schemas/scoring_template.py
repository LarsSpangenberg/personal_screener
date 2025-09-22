from dataclasses import dataclass, field
from typing import Optional

from personal_screener.schemas.price_value import (
    PriceBetweenCondition,
    PriceOperatorCondition,
)
from personal_screener.schemas.types import (
    MarketCap,
    OperatorCondition,
)
from personal_screener.schemas.weighted_condition import WeightedCondition


@dataclass
class ScoringTemplate:
    """
    Defines weighted scoring rules for screener evaluation.
    Each field corresponds to a Quote attribute.
    """
    # base data
    market_cap: Optional[WeightedCondition[MarketCap]] = None
    avg_vol: Optional[WeightedCondition[OperatorCondition]] = None
    price_range: Optional[WeightedCondition[PriceBetweenCondition]] = None
    ma50: Optional[WeightedCondition[PriceOperatorCondition]] = None
    ma200: Optional[WeightedCondition[PriceOperatorCondition]] = None

    # calculated indicators
    ma3: Optional[WeightedCondition[PriceOperatorCondition]] = None
    ma10: Optional[WeightedCondition[PriceOperatorCondition]] = None
    ma20: Optional[WeightedCondition[PriceOperatorCondition]] = None
    rsi: Optional[WeightedCondition[OperatorCondition]] = None

    # signals
    is_3ma_trending_up: Optional[int] = None
    is_10ma_trending_up: Optional[int] = None

    # additional weighted conditions if one is not enough
    additional: list[tuple[str, WeightedCondition]] = field(
        default_factory = list,
    )

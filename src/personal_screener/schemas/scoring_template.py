from dataclasses import dataclass
from typing import Optional

from personal_screener.schemas.types import (
    BetweenCondition, OperatorCondition,
    MarketCap,
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
    price_range: Optional[WeightedCondition[BetweenCondition]] = None
    ma50: Optional[WeightedCondition[OperatorCondition]] = None
    ma200: Optional[WeightedCondition[OperatorCondition]] = None

    # tiered scoring fields
    tiered_price_range: Optional[
        list[WeightedCondition[BetweenCondition]]] = None

    # calculated indicators
    ma3: Optional[WeightedCondition[OperatorCondition]] = None
    ma10: Optional[WeightedCondition[OperatorCondition]] = None
    ma20: Optional[WeightedCondition[OperatorCondition]] = None
    rsi: Optional[WeightedCondition[OperatorCondition]] = None

    # signals
    is_3ma_trending_up: Optional[int] = None
    is_10ma_trending_up: Optional[int] = None

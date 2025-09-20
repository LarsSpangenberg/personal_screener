from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, overload

from personal_screener.schemas.types import (
    BetweenCondition, MarketCap, OperatorCondition,
)

T = TypeVar("T")


@dataclass
class WeightedCondition(Generic[T]):
    weight: int = 1
    condition: Optional[T] = None


# === FACTORY HELPERS =====================================

@overload
def make_weighted(weight: int, condition: OperatorCondition) -> \
        WeightedCondition[OperatorCondition]: ...


@overload
def make_weighted(weight: int, condition: BetweenCondition) -> \
        WeightedCondition[BetweenCondition]: ...


@overload
def make_weighted(weight: int, condition: MarketCap) -> \
        WeightedCondition[MarketCap]: ...


@overload
def make_weighted(weight: int, condition: str) -> WeightedCondition[str]: ...


@overload
def make_weighted(weight: int, condition: bool) -> WeightedCondition[bool]: ...


def make_weighted(weight: int, condition):
    return WeightedCondition(weight = weight, condition = condition)

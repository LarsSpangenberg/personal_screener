from dataclasses import Field
from typing import get_args, get_origin

from personal_screener.core.evaluators.market_cap_condition import (
    evaluate_market_cap,
)
from personal_screener.core.evaluators.operator_conditions import (
    evaluate_numeric_operator_condition, evaluate_price_operator_condition,
)
from personal_screener.core.evaluators.range_conditions import (
    evaluate_numeric_range, evaluate_price_range_condition,
)
from personal_screener.core.utils import unwrap_optional
from personal_screener.schemas.price_value import (
    PriceBetweenCondition,
    PriceOperatorCondition,
)
from personal_screener.schemas.quote import Quote
from personal_screener.schemas.types import (
    BetweenCondition,
    OperatorCondition,
)
from personal_screener.schemas.weighted_condition import WeightedCondition


def evaluate_weighted_condition(
    quote: Quote,
    scoring_field: Field,
    quote_value,
    weighted_condition: WeightedCondition,
) -> int:
    """
    Evaluate a WeightedCondition using the declared inner type of the field.
    """
    weight, condition = weighted_condition.weight, weighted_condition.condition
    if condition is None:
        return 0

    # get type from WeightedCondition generic type argument
    declared_type = unwrap_optional(get_args(scoring_field.type)[0])

    # unwrap list[WeightedCondition[T]]
    if get_origin(declared_type) is list:
        inner_args = get_args(declared_type)
        if inner_args and get_origin(inner_args[0]) is WeightedCondition:
            declared_type = inner_args[0]

    # unwrap WeightedCondition[T] for tiered conditions
    if get_origin(declared_type) is WeightedCondition:
        inner_args = get_args(declared_type)
        if inner_args:
            declared_type = inner_args[0]

    # === Market Cap ===
    if scoring_field.name == "market_cap":
        if evaluate_market_cap(quote_value, condition):
            return weight

    # === BetweenCondition ===
    elif declared_type is BetweenCondition:
        min_value, max_value = condition
        if evaluate_numeric_range(quote_value, min_value, max_value):
            return weight

    elif declared_type is PriceBetweenCondition:
        if evaluate_price_range_condition(quote, quote_value, condition):
            return weight

    # === OperatorCondition ===
    elif declared_type is OperatorCondition:
        if evaluate_numeric_operator_condition(quote_value, condition):
            return weight

    elif declared_type is PriceOperatorCondition:
        if evaluate_price_operator_condition(quote, quote_value, condition):
            return weight

    # === Boolean ===
    elif declared_type is bool:
        if quote_value == condition:
            return weight

    # === String ===
    elif declared_type is str:
        if quote_value == condition:
            return weight

    # === Membership list ===
    elif get_origin(declared_type) in (list, set):
        if quote_value in condition:
            return weight

    return 0

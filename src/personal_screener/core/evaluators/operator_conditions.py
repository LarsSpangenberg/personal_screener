from typing import Callable

from personal_screener.core.evaluators.resolve_price_operand import \
    resolve_operand
from personal_screener.schemas.price_value import PriceOperatorCondition
from personal_screener.schemas.quote import Quote
from personal_screener.schemas.types import Number, OperatorCondition

OperatorFunction = Callable[[Number, Number], bool]

OPERATOR_FUNCTIONS: dict[str, OperatorFunction] = {
    "GT": lambda quote_value, filter_value: quote_value > filter_value,
    "GTE": lambda quote_value, filter_value: quote_value >= filter_value,
    "LT": lambda quote_value, filter_value: quote_value < filter_value,
    "LTE": lambda quote_value, filter_value: quote_value <= filter_value,
    "EQ": lambda quote_value, filter_value: quote_value == filter_value,
}


def evaluate_numeric_operator_condition(
    quote_value: Number, filter_condition: OperatorCondition,
) -> bool:
    """
    Compare a Quote field (quote_value) against a filter condition (
    operator, filter_value).
    Returns True if no filter is applied or the quote_value is None.
    """
    if filter_condition is None or quote_value is None:
        return True

    operator, filter_value = filter_condition
    return OPERATOR_FUNCTIONS[operator](quote_value, filter_value)


def evaluate_price_operator_condition(
    quote: Quote, quote_value: float, condition: PriceOperatorCondition,
) -> bool:
    """
    Compare a Quote field against a price-aware filter condition.

    A condition is a tuple (operator, operand) where:
        - operator: one of {"GT", "GTE", "LT", "LTE", "EQ"}
        - operand: number, OHLC string ("OPEN", "HIGH", "LOW", "CLOSE"),
          or a PriceValue with optional offset/percentage logic

    The operand is resolved with resolve_operand(). If condition, quote_value,
    or the resolved operand is None, the function short-circuits to True.

    Returns:
        bool: True if the condition is satisfied, or bypassed.
    """
    if condition is None or quote_value is None:
        return True

    operator, operand = condition
    compare_value = resolve_operand(quote, operand)

    if compare_value is None:
        return True

    return evaluate_numeric_operator_condition(
        quote_value, (operator, compare_value),
    )

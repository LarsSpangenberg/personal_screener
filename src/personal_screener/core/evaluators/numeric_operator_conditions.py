from typing import Callable

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
    Compare a Quote field (quote_value) against a filter condition (operator, filter_value).
    Returns True if no filter is applied or the quote_value is None.
    """
    if filter_condition is None or quote_value is None:
        return True

    operator, filter_value = filter_condition
    return OPERATOR_FUNCTIONS[operator](quote_value, filter_value)

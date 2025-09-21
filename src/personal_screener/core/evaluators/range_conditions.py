from personal_screener.core.evaluators.resolve_price_operand import \
    resolve_operand
from personal_screener.schemas.quote import Quote
from personal_screener.schemas.types import Number, PriceBetweenCondition


def evaluate_numeric_range(
    quote_value: Number,
    min_value: Number | None,
    max_value: Number | None,
) -> bool:
    """
    Check if a quote's value falls inside the given range.
    Range is (min, max), where either bound can be None.
    """
    if min_value is not None and quote_value < min_value:
        return False
    if max_value is not None and quote_value > max_value:
        return False

    return True


def evaluate_price_range_condition(
    quote: Quote,
    quote_value: float,
    condition: PriceBetweenCondition,
) -> bool:
    """
    Check if a quote's value falls inside a price-aware range.
    Each bound can be a number, an OHLC string, or a PriceValue.
    """
    if condition is None or quote_value is None:
        return True

    min_operand, max_operand = condition

    min_value = resolve_operand(
        quote,
        min_operand,
    ) if min_operand is not None else None

    max_value = resolve_operand(
        quote,
        max_operand,
    ) if max_operand is not None else None

    return evaluate_numeric_range(quote_value, min_value, max_value)

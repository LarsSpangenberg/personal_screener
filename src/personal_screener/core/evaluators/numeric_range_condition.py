from personal_screener.schemas.types import Number


def evaluate_numeric_range(
    quote_value: Number,
    min_value: Number | None,
    max_value: Number | None,
) -> bool:
    """
    Check if a quote's value falls inside the given range.
    Range is (min, max), where either bound can be None.
    """
    if min_value is not None and quote_value <= min_value:
        return False
    if max_value is not None and quote_value >= max_value:
        return False

    return True

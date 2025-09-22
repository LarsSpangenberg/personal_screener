from personal_screener.schemas.quote import Quote


def make_test_quote(
    symbol: str,
    price: float,
    avg_vol: int = 1_000_000,
    market_cap: int = 10_000_000,
    day_vol: int = 1000,
    open_: float | None = None,
    high: float | None = None,
    low: float | None = None,
    close: float | None = None,
) -> Quote:
    """
    Build a Quote with sensible dummy defaults for tests.
    OHLC fields default to the given `price` unless overridden.
    """
    if open_ is None:
        open_ = price
    if high is None:
        high = price
    if low is None:
        low = price
    if close is None:
        close = price

    return Quote(
        symbol = symbol,
        price = price,
        open = open_,
        high = high,
        low = low,
        close = close,
        day_vol = day_vol,
        avg_vol = avg_vol,
        market_cap = market_cap,
    )

from personal_screener.schemas.types import MarketCap


def evaluate_market_cap(
    quote_market_cap: int, filter_market_cap: MarketCap,
) -> bool:
    """
    Check if a quote's market cap falls into the selected bucket.
    Buckets:
      SMALL  -> under 2B
      MID  -> 2B–10B
      LARGE -> 10B+
    """
    if filter_market_cap is None:
        return True

    if filter_market_cap == "SMALL":
        return quote_market_cap < 2_000_000_000
    if filter_market_cap == "MID":
        return 2_000_000_000 <= quote_market_cap < 10_000_000_000
    if filter_market_cap == "LARGE":
        return quote_market_cap >= 10_000_000_000

    return True

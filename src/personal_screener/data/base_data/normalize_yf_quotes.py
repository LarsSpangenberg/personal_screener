from personal_screener.data.base_data.normalize_yf_quote import \
    normalize_yf_quote
from personal_screener.schemas.quote import Quote


def normalize_yf_base_data(raw_quotes: list[dict]) -> tuple[
    list[str],
    dict[str, Quote],
]:
    """
    Normalize a batch of Yahoo Finance screener quotes.
    """
    tickers: list[str] = []
    quotes: dict[str, Quote] = {}

    for quote in raw_quotes:
        normalized = normalize_yf_quote(quote)
        tickers.append(normalized.symbol)
        quotes[normalized.symbol] = normalized

    return tickers, quotes

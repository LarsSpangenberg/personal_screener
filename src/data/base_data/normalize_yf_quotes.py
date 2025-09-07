from src.data.base_data.normalize_yf_quote import normalize_yf_quote
from src.schemas.quote import Quote


def normalize_yf_base_data(raw_quotes: list[dict]) -> list[Quote]:
    """
    Normalize a batch of Yahoo Finance screener quotes.
    """
    normalized_quotes: list[Quote] = []
    for quote in raw_quotes:
        normalized = normalize_yf_quote(quote)
        normalized_quotes.append(normalized)
    return normalized_quotes

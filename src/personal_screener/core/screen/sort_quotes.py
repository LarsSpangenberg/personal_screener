from typing import Literal

from personal_screener.core.scoring.generate_quote_scores import \
    generate_scores
from personal_screener.schemas.quote import Quote
from personal_screener.schemas.scoring_template import ScoringTemplate
from personal_screener.schemas.types import QuoteData

SortOption = Literal["score", "rsi", "name"]


def sort_quotes(
    quotes: QuoteData,
    sort_by: SortOption = "score",
    scoring_template: ScoringTemplate | None = None,
) -> list[Quote]:
    """
    Sort quotes by score (default), RSI, or ticker name.
    """
    if not quotes:
        return []

    if sort_by == "score":
        if scoring_template is None:
            scoring_template = ScoringTemplate()
        scores = generate_scores(quotes, scoring_template)
        return sorted(
            quotes.values(),
            key = lambda quote: (
                -scores.get(quote.symbol, 0),
                -(getattr(quote, "rsi", 0) or 0),
                quote.symbol,
            ),
        )

    if sort_by == "rsi":
        return sorted(
            quotes.values(),
            key = lambda quote: (
                -(getattr(quote, "rsi", 0) or 0),
                quote.symbol,
            ),
        )

    if sort_by == "name":
        return sorted(quotes.values(), key = lambda quote: quote.symbol)

    return list(quotes.values())

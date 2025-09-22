import logging
from dataclasses import fields
from typing import get_origin

from personal_screener.core.scoring.default_score_template import \
    default_scoring_template
from personal_screener.core.scoring.eval_weighted_condition import \
    evaluate_weighted_condition
from personal_screener.core.utils.quote_field_name_mapping import \
    get_quote_field_name
from personal_screener.core.utils.type_utils import unwrap_optional
from personal_screener.schemas.scoring_template import ScoringTemplate
from personal_screener.schemas.types import QuoteData, QuoteScores
from personal_screener.schemas.weighted_condition import WeightedCondition

logger = logging.getLogger(__name__)


def generate_scores(
    quotes: QuoteData,
    template: ScoringTemplate = default_scoring_template,
) -> QuoteScores:
    """
    Apply scoring to quotes using a ScoringTemplate.
    Returns {symbol: score}.
    """
    scores: QuoteScores = {}

    for symbol, quote in quotes.items():
        score: int = 0

        for scoring_field in fields(template):
            scoring_value = getattr(template, scoring_field.name, None)
            if scoring_value is None:
                continue

            # handle "additional" field
            if scoring_field.name == "additional":
                for field_name, weighted_condition in scoring_value:
                    # resolve field, quote value
                    quote_field_name = get_quote_field_name(field_name)
                    quote_value = getattr(quote, quote_field_name, None)
                    if quote_value is None:
                        continue

                    # grab the scoring_field for type info, if it exists
                    matched_scoring_field = next(
                        (f for f in fields(ScoringTemplate) if
                            f.name == field_name),
                        None,
                    )

                    score += evaluate_weighted_condition(
                        quote,
                        matched_scoring_field,
                        quote_value,
                        weighted_condition,
                    )
                continue

            # -----------------------------------------------------
            quote_field_name = get_quote_field_name(scoring_field.name)
            quote_value = getattr(quote, quote_field_name, None)
            if quote_value is None:
                continue

            declared_type = unwrap_optional(scoring_field.type)

            # === Handle int for basic booleans ===
            if declared_type is int:
                if quote_value:
                    score += int(scoring_value)
                continue

            # === Handle WeightedCondition
            if get_origin(declared_type) is WeightedCondition:
                score += evaluate_weighted_condition(
                    quote, scoring_field, quote_value, scoring_value,
                )
                continue

        scores[symbol] = score

    return scores

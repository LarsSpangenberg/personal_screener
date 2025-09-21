from dataclasses import asdict, fields
from typing import get_origin

from personal_screener.core.evaluators.market_cap_condition import \
    evaluate_market_cap
from personal_screener.core.evaluators.operator_conditions import \
    (
    evaluate_numeric_operator_condition,
    evaluate_price_operator_condition,
)
from personal_screener.core.evaluators.range_conditions import \
    (
    evaluate_numeric_range,
    evaluate_price_range_condition,
)
from personal_screener.core.utils import unwrap_optional
from personal_screener.data.base_data.yf_filters import default_filters
from personal_screener.schemas.filters import ScreenerFilters
from personal_screener.schemas.types import (
    BetweenCondition,
    OperatorCondition,
    PriceBetweenCondition,
    PriceOperatorCondition,
    QuoteData,
)

SKIP_FILTER_FIELDS = {'avg_vol', 'price_range'}
FILTER_TO_QUOTE_FIELD: dict[str, str] = {}


def apply_filters(quotes: QuoteData, filters: ScreenerFilters) -> QuoteData:
    result: QuoteData = {}
    filters = ScreenerFilters(
        **{
            **asdict(default_filters),
            **asdict(filters),
        },
    )

    for symbol, quote in quotes.items():
        keep = True

        for filter_field in fields(filters):
            if filter_field.name in SKIP_FILTER_FIELDS:
                continue

            filter_value = getattr(filters, filter_field.name)
            if filter_value is None:
                continue

            # Map filter field -> quote field if mapping exists
            quote_field_name = FILTER_TO_QUOTE_FIELD.get(
                filter_field.name, filter_field.name,
            )

            quote_value = getattr(quote, quote_field_name, None)
            declared_type = unwrap_optional(filter_field.type)

            if filter_field.name == "market_cap":
                if not evaluate_market_cap(quote.market_cap, filter_value):
                    keep = False
                    break
                continue

            # === Range filters ===
            elif declared_type is BetweenCondition:
                min_value, max_value = filter_value
                if not evaluate_numeric_range(
                        quote_value, min_value, max_value,
                ):
                    keep = False
                    break
                continue

            elif declared_type is PriceBetweenCondition:
                if not evaluate_price_range_condition(
                        quote, quote_value, filter_value,
                ):
                    keep = False
                    break
                continue

            # === Operator filters ===
            elif declared_type is OperatorCondition:
                if not evaluate_numeric_operator_condition(
                        quote_value, filter_value,
                ):
                    keep = False
                    break
                continue

            elif declared_type is PriceOperatorCondition:
                if not evaluate_price_operator_condition(
                        quote, quote_value, filter_value,
                ):
                    keep = False
                    break
                continue

            # === Boolean filters ===
            elif declared_type is bool:
                if quote_value != filter_value:
                    keep = False
                    break
                continue

            # === String match ===
            elif declared_type is str:
                if quote_value != filter_value:
                    keep = False
                    break
                continue

            # === Membership list ===
            elif get_origin(declared_type) in (list, set):
                if quote_value not in filter_value:
                    keep = False
                    break
                continue

        if keep:
            result[symbol] = quote

    return result

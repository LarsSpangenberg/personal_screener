from numbers import Real
from typing import List

from yfinance import EquityQuery

from personal_screener.schemas.filters import ScreenerFilters

MARKET_CAP_QUERIES = {
    "SMALL": lambda: create_basic_query(
        'LTE',
        'intradaymarketcap',
        2_000_000_000,
    ),
    "MID": lambda: create_range_query(
        'intradaymarketcap',
        2_000_000_000,
        10_000_000_000,

    ),
    "LARGE": lambda: create_basic_query(
        'GTE',
        'intradaymarketcap',
        10_000_000_000,
    ),
}


def handle_market_cap(
    equity_queries: List[EquityQuery],
    filters: ScreenerFilters,
):
    if filters.market_cap in MARKET_CAP_QUERIES:
        equity_queries.append(
            MARKET_CAP_QUERIES[str(filters.market_cap)](),
        )
    return equity_queries


def handle_price_range(
    equity_queries: List[EquityQuery],
    filters: ScreenerFilters,
):
    if not filters.price_range:
        return equity_queries

    low, high = filters.price_range
    if low and high:
        equity_queries.append(
            create_range_query('eodprice', low, high),
        )
    elif low is not None:
        equity_queries.append(
            create_basic_query('GTE', 'eodprice', low),
        )
    elif high is not None:
        equity_queries.append(
            create_basic_query(
                'LTE', 'eodprice', high,
            ),
        )
    return equity_queries


# === HELPERS ================================================
def create_basic_query(
    operator: str,
    key: str,
    value: str | Real,
):
    return EquityQuery(
        operator,
        [key, value],  # type: ignore
    )


def create_range_query(
    key: str,
    value1: str | Real,
    value2: str | Real,
):
    return EquityQuery(
        'BTWN',
        [key, value1, value2],  # type: ignore
    )

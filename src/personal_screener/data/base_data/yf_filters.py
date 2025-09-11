from yfinance import EquityQuery

from personal_screener.data.base_data.yf_queries import (
    create_basic_query,
    handle_market_cap, handle_price_range,
)
from personal_screener.schemas.filters import ScreenerFilters

# NOTE: US region is always applied by default
default_filters = ScreenerFilters(
    avg_volume = ('GTE', 500000),
    price_range = (7, 100),
)


def map_filters_to_yf_query(filters: ScreenerFilters):
    # === FIELDS TO ADD ===
    # sector
    # industry

    equity_queries = [create_basic_query('EQ', 'region', 'us')]
    handle_price_range(equity_queries, filters)
    handle_market_cap(equity_queries, filters)

    if filters.avg_volume is not None:
        equity_queries.append(
            create_basic_query(
                key = 'avgdailyvol3m',
                operator = filters.avg_volume[0],
                value = filters.avg_volume[1],
            ),
        )

    return EquityQuery('AND', equity_queries)

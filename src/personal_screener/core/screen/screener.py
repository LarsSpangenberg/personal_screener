import subprocess
from typing import Literal

from personal_screener.core.utils.logging_config import setup_logging
from personal_screener.core.screen.apply_filters import apply_filters
from personal_screener.core.screen.sort_quotes import sort_quotes
from personal_screener.data.base_data.yf_filters import default_filters
from personal_screener.data.cache_manager import (
    CACHE_DIR,
    load_quotes_from_cache,
)
from personal_screener.data.initialize_data import initialize_data
from personal_screener.schemas.filters import ScreenerFilters

SortOption = Literal["score", "rsi", "name"]


# === SCREENER LOGIC TO IMPLEMENT===================================
# strategy specific evaluators and sort priorities
#   saved as presets
# evaluators to use with filter AND Group and sort
#   MA (3, 10, 21, 50, 200)
#   RSI
#   price range filter
#   sector
#   tickers (for favorites and hated filters)
#   market cap (large, mid, small)
#   Sales and Earnings
#   % change (weekly, monthly) / volatility
#   average volume
#   short float
#   OPTIONAL:
#       news sentiment
#       days till earnings
# filter data
# group data
# sort data
#   add top candidate evaluators for important metrics and favorite tickers
#   sort by
#       amount of evaluators met
#       RSI / strength
#       name
#       price
# return best tickers

def screen(filters: ScreenerFilters = default_filters):
    data = load_quotes_from_cache()
    if not data:
        return []

    data = apply_filters(data, filters)
    sorted_quotes =  sort_quotes(data)
    return sorted_quotes


if __name__ == "__main__":
    setup_logging()
    initialize_data()
    result = screen(ScreenerFilters(
        is_3ma_trending_up = True
    ))
    print(f"{len(result)} quotes loaded after filtering")


    subprocess.run(["explorer", str(CACHE_DIR)])


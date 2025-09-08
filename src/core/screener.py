from src.data.base_data.yf_filters import default_filters
from src.data.initialize_data import load_quotes_from_cache
from src.schemas.filters import ScreenerFilters


# === SCREENER LOGIC TO IMPLEMENT===================================
# strategy specific conditions and sort priorities
#   saved as presets
# conditions to use with filter AND Group and sort
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
#   add top candidate conditions for important metrics and favorite tickers
#   sort by
#       amount of conditions met
#       RSI / strength
#       name
#       price
# return best tickers

def screen(filters: ScreenerFilters = default_filters):
    data = load_quotes_from_cache()
    quotes = list(data.values())  # will add sort and filtering later
    # handle normalized data
    #   apply filters for enriched data
    #   apply sorting/grouping as the last thing

    return quotes


if __name__ == "__main__":
    screen()

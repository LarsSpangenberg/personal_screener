from src.data.base_data.normalize_yf_quotes import normalize_yf_base_data
from src.data.base_data.yf_data import get_yf_data
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

def screen(filters: ScreenerFilters):
    raw_data = get_yf_data(filters)
    # filter raw data
    #   apply ma50, and ma200 filters here
    quotes = normalize_yf_base_data(raw_data)
    # handle normalized data
    #   calculate rest of the data
    #   fetch other api method to enrich data
    #   apply filters for enriched data
    #   apply sorting/grouping as the last thing

    return quotes
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 19:33:34 2025.

@author: Lars Spangenberg
"""

import logging
from src.core.logging_config import setup_logging
from src.data.yf_data import get_yf_data

logger = logging.getLogger(__name__)


# === FEATURES TO IMPLEMENT ===================================
# get data from api
#   environment variables for keys and url
#   dependencies
#       API to get tickers by:
#           US market
#           price range
#           volume
#           stocks only
#       Schwab api
#       supplementary apis for some data
#   manage api call limits
#   save large data sets into .csv files
#       add Date Stamp and refetch if date is different
#       make data reusable for that day
#       my screener only needs daily data
# IMPORTANT: apply adapter to convert to usable data
#   future proof
#   may use different apis in the future
#   this simplifies the process
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
#   plot data
#   put into user friendly format
#       Easy ticker selection to copy to charting software
#       overview GUI similar to finviz screener charts
#       add ticker links to finviz and maybe others
#       OPTIONAL: implement export to thinkorswim watchlist
#
# OPTIONAL: Lists (e.g. short squeeze, specific strategy, all, etc)
#   I'm thinking instead of just return a list of tickers return
#       a list of lists of tickers separated into strategy groups
#   In a GUI these should show up as drop down lists
#   Then again I could just make multiple calls to the screener with
#       different filters and group those into lists


def main():
    setup_logging()
    logger.info("Application started")

    data = get_yf_data()
    logger.info(f"Data loaded for {len(data)} quotes")


if __name__ == "__main__":
    main()

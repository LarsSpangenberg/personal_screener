# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 19:33:34 2025.

@author: Lars Spangenberg
"""

import logging

from personal_screener.core.logging_config import setup_logging
from personal_screener.core.screen.screener import screen

logger = logging.getLogger(__name__)


# === FEATURES TO IMPLEMENT ===================================
#  plot data
#  put into user-friendly format
#       Easy ticker selection to copy to charting software
#       overview GUI similar to finviz screener charts
#       add ticker links to finviz and maybe others
#       OPTIONAL: implement export to thinkorswim watchlist
# OPTIONAL: Lists (e.g. short squeeze, specific strategy, all, etc.)
#   I'm thinking instead of just return a list of tickers return
#       a list of lists of tickers separated into strategy groups
#   In a GUI these should show up as drop down lists
#   Then again I could just make multiple calls to the screener with
#       different filters and group those into lists


def main():
    setup_logging()
    logger.info("beep, boop... Initialize Program!")

    data = screen()
    logger.info(f"Data loaded for {len(data)} quotes")


if __name__ == "__main__":
    main()

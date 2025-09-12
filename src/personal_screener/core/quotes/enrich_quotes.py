from typing import Dict

import pandas as pd

from personal_screener.core.indicators.moving_averages import \
    calculate_moving_averages
from personal_screener.core.indicators.rsi import calculate_rsi
from personal_screener.core.signals.uptrend_signals import (
    is_10ma_uptrend,
    is_3ma_uptrend,
)
from personal_screener.schemas.quote import Quote


def calculate_indicators_and_signals(
    price_history: pd.DataFrame,
    quotes: Dict[str, Quote],
) -> Dict[str, Quote]:
    """
    For each ticker in the MultiIndex price_history DataFrame,
    compute MA3/MA10/MA20 and RSI(14), then assign to Quote.
    """
    close_df = price_history.xs("Close", axis = 1, level = 0)

    for ticker in close_df.columns:
        close_series = close_df[ticker].dropna()

        if close_series.empty:
            continue

        quote = quotes.get(ticker)
        ma_values = calculate_moving_averages(close_series)
        rsi_value = calculate_rsi(close_series)

        is_3ma_trending_up = is_3ma_uptrend(close_series)
        is_10ma_trending_up = is_10ma_uptrend(close_series)

        if quote:
            quote.ma3 = float(ma_values["ma3"])
            quote.ma10 = float(ma_values["ma10"])
            quote.ma20 = float(ma_values["ma20"])
            quote.rsi = float(rsi_value)
            quote.is_3ma_trending_up = is_3ma_trending_up
            quote.is_10ma_trending_up = is_10ma_trending_up

    return quotes

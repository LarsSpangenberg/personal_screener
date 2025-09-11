from typing import Dict

import pandas as pd

from src.data.price_history.indicators.moving_averages import \
    calculate_moving_averages
from src.data.price_history.indicators.rsi import calculate_rsi
from src.schemas.quote import Quote


def calculate_indicators(
    price_history: pd.DataFrame,
    quotes: Dict[str, Quote],
) -> Dict[str, Quote]:
    """
    For each ticker in the MultiIndex price_history DataFrame,
    compute MA3/MA10/MA20 and RSI(14), then assign to Quote.
    """
    close_df = price_history.xs("Close", axis=1, level=0)

    for ticker in close_df.columns:
        close_series = close_df[ticker].dropna()

        if close_series.empty:
            continue

        ma_values = calculate_moving_averages(close_series)
        rsi_value = calculate_rsi(close_series)

        q = quotes.get(ticker)
        if q:
            q.ma3 = float(ma_values["ma3"])
            q.ma10 = float(ma_values["ma10"])
            q.ma20 = float(ma_values["ma20"])
            q.rsi = float(rsi_value)

    return quotes
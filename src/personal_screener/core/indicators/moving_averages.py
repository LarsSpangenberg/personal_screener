import pandas as pd


def calculate_moving_averages(
    close: pd.Series, full_series: bool = False,
    method: str = "sma",
):
    """
    Calculate moving averages for MA3, MA10, MA20.
    - If full_series=True: return a DataFrame with the full rolling series.
    - Otherwise: return only the last values as a dict[str, float].
    """
    if method == "ema":
        ma3 = close.ewm(span = 3, adjust = False).mean()
        ma10 = close.ewm(span = 10, adjust = False).mean()
        ma20 = close.ewm(span = 20, adjust = False).mean()
    else:  # default sma
        ma3 = close.rolling(window = 3).mean()
        ma10 = close.rolling(window = 10).mean()
        ma20 = close.rolling(window = 20).mean()

    ma_df = pd.DataFrame(
        {
            "ma3": ma3,
            "ma10": ma10,
            "ma20": ma20,
        },
    )

    if full_series:
        return ma_df

    return {key: float(series.iloc[-1]) for key, series in ma_df.items()}

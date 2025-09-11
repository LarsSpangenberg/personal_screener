import pandas as pd


def calculate_moving_averages(close: pd.Series) -> dict[str, float]:
    return {
        "ma3": close.rolling(window=3).mean().iloc[-1],
        "ma10": close.rolling(window=10).mean().iloc[-1],
        "ma20": close.rolling(window=20).mean().iloc[-1],
    }

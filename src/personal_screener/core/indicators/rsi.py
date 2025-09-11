import pandas as pd


def calculate_rsi(close: pd.Series, period: int = 14) -> float:
    delta = close.diff()
    gains = delta.clip(lower = 0)
    losses = (-delta).clip(lower = 0)

    avg_gain = gains.ewm(
        alpha = 1 / period, adjust = False, min_periods = period,
    ).mean()

    avg_loss = losses.ewm(
        alpha = 1 / period, adjust = False, min_periods = period,
    ).mean()

    if avg_gain.iloc[-1] == 0 and avg_loss.iloc[-1] == 0:
        return 50.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

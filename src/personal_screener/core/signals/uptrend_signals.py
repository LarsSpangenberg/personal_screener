import pandas as pd

from personal_screener.core.indicators.moving_averages import \
    calculate_moving_averages


def is_3ma_uptrend(close: pd.Series, lookback_days: int = 3) -> bool:
    """
    Check if 3 SMA is trending up and above MA10 over lookback_days. SMA is
    used for rounder curve instead of EMA.
    """
    ma_df = calculate_moving_averages(
        close, full_series = True, method = "ema",
    )

    ma3 = ma_df["ma3"].iloc[-lookback_days:]
    ma10 = ma_df["ma10"].iloc[-lookback_days:]

    if ma3.isna().any() or ma10.isna().any():
        return False

    trending_up = all(
        (ma3.iloc[i] > ma3.iloc[i - 1] for i in range(1, len(ma3))),
    )
    above_ma10 = all(ma3.iloc[i] > ma10.iloc[i] for i in range(len(ma3)))

    return trending_up and above_ma10


def is_10ma_uptrend(
    close: pd.Series,
    lookback_days: int = 3,
    allow_below_50ma: bool = True,
    ma50_value: float | None = None,
) -> bool:
    """
    Check if SMA10 is trending up and stacked above SMA20 and SMA50.

    - close: daily close price series
    - lookback_days: number of consecutive bars to check for trend
    - allow_below_50ma: if True, ignores SMA50 stacking requirement
    - ma50_value: optional SMA50 value (usually taken from Quote).
    """
    ma_df = calculate_moving_averages(close, full_series = True)

    ma10 = ma_df["ma10"].iloc[-lookback_days:]
    ma20 = ma_df["ma20"].iloc[-lookback_days:]

    if ma10.isna().any() or ma20.isna().any():
        return False

    if not allow_below_50ma and ma50_value is None:
        # If 50MA stacking is required, we need that value
        return False

    # Condition 1: SMA10 trending up (stair-step)
    trending_up = all(
        (ma10.iloc[i] > ma10.iloc[i - 1] for i in range(1, len(ma10))),
    )

    # Condition 2: SMA10 stacked above higher MAs
    stacked_above = all(
        (ma10.iloc[i] > ma20.iloc[i]
         and (allow_below_50ma or ma10.iloc[i] > ma50_value)
         for i in range(len(ma10))),
    )

    return trending_up and stacked_above

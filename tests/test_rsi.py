import math
import unittest
import pandas as pd

from personal_screener.data.price_history.indicators.rsi import calculate_rsi


class TestCalculateRSI(unittest.TestCase):
    def test_returns_float(self):
        close = pd.Series(
            [
                100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
                112, 113, 114,
            ],
        )
        value = calculate_rsi(close)  # default period=14
        self.assertIsInstance(value, float) or math.isnan(value)

    def test_uptrend_results_in_high_rsi(self):
        # Monotonic uptrend should push RSI high (often near 100 with Wilder-style smoothing)
        close = pd.Series(range(1, 60))
        value = calculate_rsi(close, period = 14)
        self.assertGreater(value, 70.0)

    def test_downtrend_results_in_low_rsi(self):
        close = pd.Series(list(range(100, 40, -1)))
        value = calculate_rsi(close, period = 14)
        self.assertLess(value, 30.0)

    def test_short_series_returns_nan(self):
        # Fewer than period=14 data points -> EWM with min_periods=14 produces NaN at the end
        close = pd.Series([100, 101, 102, 103, 104, 105, 106, 107, 108, 109])
        value = calculate_rsi(close, period = 14)
        self.assertTrue(math.isnan(value))

    def test_constant_prices_returns_nan(self):
        # Gains and losses are all zero -> RS becomes 0/0 -> NaN
        close = pd.Series([100.0] * 30)
        value = calculate_rsi(close, period = 14)
        self.assertTrue(math.isnan(value))

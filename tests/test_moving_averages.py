
import math
import unittest
import pandas as pd

from personal_screener.data.price_history.indicators.moving_averages import calculate_moving_averages


class TestCalculateMovingAverages(unittest.TestCase):
    def setUp(self):
        # Simple increasing close series with 30 rows, index as dates for realism
        self.close = pd.Series(
            [float(i) for i in range(1, 31)],
            index=pd.date_range("2024-01-01", periods=30, freq="D"),
            name="Close",
        )

    def test_returns_expected_keys_and_types(self):
        result = calculate_moving_averages(self.close)
        self.assertIsInstance(result, dict)
        self.assertSetEqual(set(result.keys()), {"ma3", "ma10", "ma20"})
        for value in result.values():
            self.assertIsInstance(value, float) or math.isnan(value)

    def test_matches_pandas_rolling_means(self):
        result = calculate_moving_averages(self.close)
        expected_ma3 = self.close.rolling(window=3).mean().iloc[-1]
        expected_ma10 = self.close.rolling(window=10).mean().iloc[-1]
        expected_ma20 = self.close.rolling(window=20).mean().iloc[-1]

        # Using almost equal to allow for float round-off
        self.assertAlmostEqual(result["ma3"], float(expected_ma3), places=7)
        self.assertAlmostEqual(result["ma10"], float(expected_ma10), places=7)
        self.assertAlmostEqual(result["ma20"], float(expected_ma20), places=7)

    def test_short_series_yields_nan_for_large_windows(self):
        short_close = self.close.iloc[:2]  # fewer than 3 points
        result = calculate_moving_averages(short_close)
        self.assertTrue(math.isnan(result["ma3"]))  # not enough points for window=3
        self.assertTrue(math.isnan(result["ma10"]))
        self.assertTrue(math.isnan(result["ma20"]))

import unittest

import pandas as pd

from personal_screener.core.indicators.moving_averages import \
    calculate_moving_averages
from personal_screener.core.indicators.rsi import calculate_rsi
from personal_screener.core.screen.enrich_quotes import \
    calculate_indicators_and_signals
from personal_screener.schemas.quote import Quote


def _build_multiindex_ohlcv(
    close_a, close_b = None, ticker_a = "AAA", ticker_b = "BBB",
):
    """
    Build a MultiIndex columns DataFrame shaped like:
        columns = pd.MultiIndex.from_product(
            [["Open","High","Low","Close","Volume"], [tickers...]]
        )
    and rows indexed by the index of the input close series.
    For simplicity, we generate Open/High/Low as offsets of Close, and Volume as constant.
    """
    idx = close_a.index
    fields = ["Open", "High", "Low", "Close", "Volume"]
    tickers = [ticker_a] + ([ticker_b] if close_b is not None else [])
    arrays = []

    for t in tickers:
        arrays.extend([(f, t) for f in fields])

    columns = pd.MultiIndex.from_tuples(arrays, names = ["Field", "Ticker"])
    df = pd.DataFrame(index = idx, columns = columns, dtype = "float64")

    # helper to fill one ticker's OHLCV given a close series
    def _fill_for_ticker(ticker, close):
        df[("Close", ticker)] = close.values
        df[("Open", ticker)] = (close - 0.5).values
        df[("High", ticker)] = (close + 1.0).values
        df[("Low", ticker)] = (close - 1.0).values
        df[("Volume", ticker)] = 1000.0

    _fill_for_ticker(ticker_a, close_a)
    if close_b is not None:
        _fill_for_ticker(
            ticker_b, close_b.reindex(idx, method = None).fillna(
                method = "ffill",
            ),
        )

    return df


class TestCalculateIndicators(unittest.TestCase):
    def test_assigns_indicator_values_into_quotes(self):
        # Prepare two tickers with sufficient history
        idx = pd.date_range("2024-01-01", periods = 60, freq = "D")
        close_a = pd.Series(
            [float(i) for i in range(1, 61)], index = idx,
        )  # steady uptrend
        close_b = pd.Series(
            [float(200 - i) for i in range(0, 60)], index = idx,
        )  # steady downtrend

        price_history = _build_multiindex_ohlcv(close_a, close_b, "AAA", "BBB")

        quotes = {
            "AAA": Quote(
                symbol = "AAA", price = close_a.iloc[-1], avg_vol = 1_000_000,
                market_cap = 10_000_000,
            ),
            "BBB": Quote(
                symbol = "BBB", price = close_b.iloc[-1], avg_vol = 1_000_000,
                market_cap = 10_000_000,
            ),
        }

        updated = calculate_indicators_and_signals(price_history, quotes)

        # Expect all indicator fields set to floats
        for sym in ["AAA", "BBB"]:
            quote = updated[sym]
            self.assertIsInstance(quote.ma3, float)
            self.assertIsInstance(quote.ma10, float)
            self.assertIsInstance(quote.ma20, float)
            self.assertIsInstance(quote.rsi, float)

        # Cross-check vs direct indicator functions for accuracy
        expected_ma_aaa = calculate_moving_averages(close_a)
        expected_ma_bbb = calculate_moving_averages(close_b)
        expected_rsi_aaa = calculate_rsi(close_a)
        expected_rsi_bbb = calculate_rsi(close_b)

        self.assertAlmostEqual(
            updated["AAA"].ma3, expected_ma_aaa["ma3"], places = 7,
        )
        self.assertAlmostEqual(
            updated["AAA"].ma10, expected_ma_aaa["ma10"], places = 7,
        )
        self.assertAlmostEqual(
            updated["AAA"].ma20, expected_ma_aaa["ma20"], places = 7,
        )
        self.assertAlmostEqual(
            updated["AAA"].rsi, expected_rsi_aaa, places = 7,
        )

        self.assertAlmostEqual(
            updated["BBB"].ma3, expected_ma_bbb["ma3"], places = 7,
        )
        self.assertAlmostEqual(
            updated["BBB"].ma10, expected_ma_bbb["ma10"], places = 7,
        )
        self.assertAlmostEqual(
            updated["BBB"].ma20, expected_ma_bbb["ma20"], places = 7,
        )
        self.assertAlmostEqual(
            updated["BBB"].rsi, expected_rsi_bbb, places = 7,
        )

    def test_missing_ticker_in_price_history_leaves_quote_unchanged(self):
        # Only include AAA in price_history; BBB will be absent
        idx = pd.date_range("2024-01-01", periods = 40, freq = "D")
        close_a = pd.Series([float(i) for i in range(1, 41)], index = idx)
        price_history = _build_multiindex_ohlcv(close_a, None, "AAA", "BBB")

        quotes = {
            "AAA": Quote(
                symbol = "AAA", price = close_a.iloc[-1], avg_vol = 500_000,
                market_cap = 5_000_000,
            ),
            "BBB": Quote(
                symbol = "BBB", price = 123.0, avg_vol = 500_000,
                market_cap = 5_000_000,
            ),
        }

        updated = calculate_indicators_and_signals(price_history, quotes)

        # AAA should be updated, BBB should remain with None indicators
        self.assertIsInstance(updated["AAA"].ma3, float)
        self.assertIsNone(updated["BBB"].ma3)
        self.assertIsNone(updated["BBB"].ma10)
        self.assertIsNone(updated["BBB"].ma20)
        self.assertIsNone(updated["BBB"].rsi)

    def test_short_series_results_in_nan_indicators(self):
        idx = pd.date_range("2024-01-01", periods = 5, freq = "D")
        close = pd.Series(
            [100, 101, 102, 103, 104], index = idx, dtype = "float64",
        )
        price_history = _build_multiindex_ohlcv(close, None, "AAA", )

        quotes = {
            "AAA": Quote(
                symbol = "AAA", price = close.iloc[-1], avg_vol = 1_000,
                market_cap = 1_000_000,
            ),
        }
        updated = calculate_indicators_and_signals(price_history, quotes)

        # With only 5 points, MA20 and RSI(14) should be NaN
        self.assertTrue(pd.isna(updated["AAA"].ma20))
        self.assertTrue(pd.isna(updated["AAA"].rsi))

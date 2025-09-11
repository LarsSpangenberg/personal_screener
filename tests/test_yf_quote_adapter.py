import unittest
from datetime import datetime
from unittest.mock import patch

import personal_screener.data.base_data.normalize_yf_quote as \
    normalize_yf_quote_module
from personal_screener.data.base_data.normalize_yf_quote import \
    normalize_yf_quote
from personal_screener.schemas.quote import Quote


class TestYfQuoteAdapter(unittest.TestCase):
    PATCH_DATETIME = f"{normalize_yf_quote_module.__name__}.datetime"

    def test_basic_conversion_without_price(self):
        raw = {
            "symbol": "AAPL",
            "marketCap": 2_500_000_000_000,
            "averageDailyVolume3Month": 80_000_000,
            "fiftyDayAverage": 148.5,
            "twoHundredDayAverage": 140.2,
        }

        q = normalize_yf_quote(raw)

        self.assertIsInstance(q, Quote)
        self.assertEqual(q.symbol, "AAPL")
        self.assertEqual(q.market_cap, 2_500_000_000_000)
        self.assertEqual(q.avg_vol, 80_000_000)
        self.assertEqual(q.ma50, 148.5)
        self.assertEqual(q.ma200, 140.2)

    def test_price_before_4pm(self):
        raw = {
            "symbol": "AAPL",
            "regularMarketPreviousClose": 150.0,
            "regularMarketPrice": 155.0,
        }

        with patch(self.PATCH_DATETIME) as mock_dt:
            mock_dt.now.return_value = datetime(2024, 5, 1, 15, 0)  # 3:00 PM
            q = normalize_yf_quote(raw)
            self.assertEqual(q.price, 150.0)  # should use previous close

    def test_price_after_4pm(self):
        raw = {
            "symbol": "AAPL",
            "regularMarketPreviousClose": 150.0,
            "regularMarketPrice": 155.0,
        }

        with patch(self.PATCH_DATETIME) as mock_dt:
            mock_dt.now.return_value = datetime(2024, 5, 1, 17, 0)  # 5:00 PM
            q = normalize_yf_quote(raw)
            self.assertEqual(q.price, 155.0)  # should use market price

    def test_handles_missing_fields(self):
        raw = {"symbol": "MSFT"}
        q = normalize_yf_quote(raw)

        self.assertIsNone(q.market_cap)
        self.assertIsNone(q.avg_vol)
        self.assertIsNone(q.ma50)
        self.assertIsNone(q.ma200)


if __name__ == '__main__':
    unittest.main()

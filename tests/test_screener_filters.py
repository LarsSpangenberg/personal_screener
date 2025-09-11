import unittest

from personal_screener.schemas.filters import ScreenerFilters


class TestScreenerFilters(unittest.TestCase):
    def test_price_range_btwn(self):
        f = ScreenerFilters(price_range = (10, 20))
        self.assertEqual(f.price_range, (10.0, 20.0))

    def test_price_range_gte(self):
        f = ScreenerFilters(price_range = (10, None))
        self.assertEqual(f.price_range, (10.0, None))

    def test_price_range_lte(self):
        f = ScreenerFilters(price_range = (None, 50))
        self.assertEqual(f.price_range, (None, 50.0))

    def test_market_cap_enum(self):
        f = ScreenerFilters(market_cap = "MID")
        self.assertEqual(f.market_cap, "MID")


if __name__ == '__main__':
    unittest.main()

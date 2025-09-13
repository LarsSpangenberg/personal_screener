import unittest

from personal_screener.core.evaluators.market_cap_condition import \
    evaluate_market_cap


class TestMarketCapCondition(unittest.TestCase):
    def test_small_cap_within_range(self):
        self.assertTrue(evaluate_market_cap(500_000_000, "SMALL"))

    def test_small_cap_out_of_range(self):
        self.assertFalse(evaluate_market_cap(2_000_000_000, "SMALL"))
        self.assertFalse(evaluate_market_cap(5_000_000_000, "SMALL"))

    def test_mid_cap_lower_boundary_inclusive(self):
        self.assertTrue(evaluate_market_cap(2_000_000_000, "MID"))

    def test_mid_cap_within_range(self):
        self.assertTrue(evaluate_market_cap(5_000_000_000, "MID"))

    def test_mid_cap_upper_boundary_exclusive(self):
        self.assertFalse(evaluate_market_cap(10_000_000_000, "MID"))

    def test_large_cap_boundary_inclusive(self):
        self.assertTrue(evaluate_market_cap(10_000_000_000, "LARGE"))

    def test_large_cap_above_range(self):
        self.assertTrue(evaluate_market_cap(200_000_000_000, "LARGE"))

    def test_none_market_cap_filter_returns_true(self):
        self.assertTrue(evaluate_market_cap(500_000_000, None))

    def test_unrecognized_filter_returns_true(self):
        # Defensive: if filter string is unexpected, function defaults to True
        self.assertTrue(evaluate_market_cap(123, "UNKNOWN"))


if __name__ == "__main__":
    unittest.main()

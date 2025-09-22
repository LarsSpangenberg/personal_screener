import unittest

from tests.utils import make_test_quote
from personal_screener.schemas.price_value import PriceValue
from personal_screener.core.evaluators.range_conditions import (
    evaluate_price_range_condition,
)


class TestPriceRangeCondition(unittest.TestCase):
    def setUp(self):
        self.quote = make_test_quote(
            "TEST",
            50.0,
            open_ = 49,
            high = 55,
            low = 48,
            close = 52,
        )

    def test_range_with_numbers(self):
        condition = (40.0, 60.0)
        self.assertTrue(
            evaluate_price_range_condition(
                self.quote,
                self.quote.close,
                condition,
            ),
        )

    def test_range_with_price_value_bounds(self):
        condition = (PriceValue("LOW"), PriceValue("HIGH"))
        self.assertTrue(
            evaluate_price_range_condition(
                self.quote,
                self.quote.close,
                condition,
            ),
        )

    def test_outside_range(self):
        condition = (60.0, 70.0)
        self.assertFalse(
            evaluate_price_range_condition(
                self.quote,
                self.quote.close,
                condition,
            ),
        )

    def test_none_condition_returns_true(self):
        self.assertTrue(
            evaluate_price_range_condition(self.quote, self.quote.close, None),
        )

    def test_none_quote_value_returns_true(self):
        condition = (40.0, 60.0)
        self.assertTrue(
            evaluate_price_range_condition(self.quote, None, condition),
        )

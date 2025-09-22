import unittest

from personal_screener.core.evaluators.operator_conditions import (
    evaluate_price_operator_condition,
)
from personal_screener.schemas.price_value import (
    PriceOperatorCondition,
    PriceValue,
)
from personal_screener.schemas.types import CLOSE, EQ, GT, HIGH, LT
from tests.utils import make_test_quote


class TestPriceOperatorCondition(unittest.TestCase):
    def setUp(self):
        self.quote = make_test_quote(
            "TEST",
            50.0,
            open_ = 49,
            high = 55,
            low = 48,
            close = 52,
        )

    def test_gt_number(self):
        condition = (GT, 50.0)
        self.assertTrue(
            evaluate_price_operator_condition(
                self.quote,
                self.quote.close,
                condition,
            ),
        )

    def test_lt_ohlc_value(self):
        condition = (LT, HIGH)
        self.assertTrue(
            evaluate_price_operator_condition(
                self.quote,
                self.quote.close,
                condition,
            ),
        )

    def test_lt_ohlc_as_string(self):
        condition: PriceOperatorCondition = ("LT", "HIGH")
        self.assertTrue(
            evaluate_price_operator_condition(
                self.quote,
                self.quote.close,
                condition,
            ),
        )

    def test_eq_price_value_with_offset(self):
        condition = (
            EQ,
            PriceValue(CLOSE, offset = -0.02, offset_as_pct = True),
        )
        compare_val = 52.0 * 0.98
        self.assertTrue(
            evaluate_price_operator_condition(
                self.quote,
                compare_val,
                condition,
            ),
        )

    def test_none_condition_returns_true(self):
        self.assertTrue(
            evaluate_price_operator_condition(
                self.quote,
                self.quote.close,
                None,
            ),
        )

    def test_none_quote_value_returns_true(self):
        condition = (GT, 40.0)
        self.assertTrue(
            evaluate_price_operator_condition(self.quote, None, condition),
        )

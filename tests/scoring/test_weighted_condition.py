import unittest

from personal_screener.schemas.types import (
    CLOSE,
    GT,
    LARGE,
    LT,
    MID,
    OPEN,
    SMALL,
)
from personal_screener.schemas.weighted_condition import (
    WeightedCondition,
    make_weighted,
)


class TestWeightedCondition(unittest.TestCase):
    def test_default_condition_none(self):
        weighted_condition = WeightedCondition[int]()
        self.assertEqual(weighted_condition.weight, 1)
        self.assertIsNone(weighted_condition.condition)

    def test_make_weighted_operator_condition(self):
        condition = (GT, 100)
        weighted_condition = make_weighted(2, condition)
        self.assertEqual(weighted_condition.weight, 2)
        self.assertEqual(weighted_condition.condition, condition)

    def test_make_weighted_range_condition(self):
        condition = (10, 20)
        weighted_condition = make_weighted(1, condition)
        self.assertEqual(weighted_condition.weight, 1)
        self.assertEqual(weighted_condition.condition, (10, 20))

    def test_make_weighted_price_operator_condition(self):
        condition = (LT, CLOSE)
        wc = make_weighted(3, condition)
        self.assertEqual(wc.weight, 3)
        self.assertEqual(wc.condition, condition)

    def test_make_weighted_price_between_condition(self):
        condition = (OPEN, CLOSE)
        wc = make_weighted(5, condition)
        self.assertEqual(wc.weight, 5)
        self.assertEqual(wc.condition, condition)

    def test_make_weighted_market_cap(self):
        for cap in (SMALL, MID, LARGE):
            wc = make_weighted(2, cap)
            self.assertEqual(wc.weight, 2)
            self.assertEqual(wc.condition, cap)

    def test_make_weighted_string_condition(self):
        weighted_condition = make_weighted(3, "SOME_COND")
        self.assertEqual(weighted_condition.weight, 3)
        self.assertEqual(weighted_condition.condition, "SOME_COND")

    def test_make_weighted_bool_condition(self):
        weighted_condition = make_weighted(4, True)
        self.assertEqual(weighted_condition.weight, 4)
        self.assertTrue(weighted_condition.condition)

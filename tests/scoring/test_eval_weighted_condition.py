import unittest
from dataclasses import fields

from personal_screener.core.scoring.eval_weighted_condition import \
    evaluate_weighted_condition
from personal_screener.schemas.scoring_template import ScoringTemplate
from personal_screener.schemas.types import CLOSE, GT, LT, LTE, MID, SMALL
from personal_screener.schemas.weighted_condition import make_weighted
from tests.utils import make_test_quote


def get_field(name: str):
    return [f for f in fields(ScoringTemplate) if f.name == name][0]


class TestEvaluateWeightedCondition(unittest.TestCase):
    def setUp(self):
        self.quote = make_test_quote(
            "TEST",
            50.0,
            avg_vol = 2_000_000,
            market_cap = 5_000_000_000,
            open_ = 49,
            high = 55,
            low = 48,
            close = 52,
        )

    def test_market_cap_match_and_mismatch(self):
        field = get_field("market_cap")
        weighted_condition_match = make_weighted(5, MID)
        weighted_condition_miss = make_weighted(5, SMALL)
        self.assertEqual(
            evaluate_weighted_condition(
                self.quote,
                field,
                self.quote.market_cap,
                weighted_condition_match,
            ),
            5,
        )
        self.assertEqual(
            evaluate_weighted_condition(
                self.quote,
                field,
                self.quote.market_cap,
                weighted_condition_miss,
            ),
            0,
        )

    def test_operator_condition_avg_vol(self):
        field = get_field("avg_vol")
        weighted_condition = make_weighted(3, (GT, 1_000_000))
        result = evaluate_weighted_condition(
            self.quote,
            field,
            self.quote.avg_vol,
            weighted_condition,
        )
        self.assertEqual(result, 3)

    def test_price_range_condition(self):
        field = get_field("price_range")
        weighted_condition = make_weighted(4, ("LOW", "HIGH"))
        result = evaluate_weighted_condition(
            self.quote,
            field,
            self.quote.close,
            weighted_condition,
        )
        self.assertEqual(result, 4)

    def test_price_operator_condition(self):
        field = get_field("ma50")
        self.quote.ma50 = self.quote.close
        weighted_condition = make_weighted(6, (LTE, CLOSE))
        result = evaluate_weighted_condition(
            self.quote,
            field,
            self.quote.ma50,
            weighted_condition,
        )
        self.assertEqual(result, 6)

    def test_rsi_operator_condition(self):
        field = get_field("rsi")
        self.quote.rsi = 30
        weighted_condition = make_weighted(2, (LT, 50))
        result = evaluate_weighted_condition(
            self.quote,
            field,
            self.quote.rsi,
            weighted_condition,
        )
        self.assertEqual(result, 2)

    def test_none_condition_returns_zero_score(self):
        field = get_field("avg_vol")
        weighted_condition = make_weighted(5, None)
        result = evaluate_weighted_condition(
            self.quote,
            field,
            self.quote.avg_vol,
            weighted_condition,
        )
        self.assertEqual(result, 0)

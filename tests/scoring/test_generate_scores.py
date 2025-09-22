import unittest

from tests.utils import make_test_quote
from personal_screener.core.scoring.generate_quote_scores import \
    generate_scores
from personal_screener.schemas.scoring_template import ScoringTemplate
from personal_screener.schemas.weighted_condition import make_weighted
from personal_screener.schemas.types import GT, MID


class TestGenerateQuoteScores(unittest.TestCase):
    def test_single_quote_with_conditions(self):
        quote = make_test_quote(
            "AAA",
            50,
            avg_vol = 2_000_000,
            market_cap = 5_000_000_000,
        )
        template = ScoringTemplate(
            avg_vol = make_weighted(1, (GT, 1_000_000)),
            market_cap = make_weighted(2, MID),
        )
        scores = generate_scores({"AAA": quote}, template)
        self.assertEqual(scores["AAA"], 3)

    def test_tiered_price_range(self):
        quote = make_test_quote("BBB", 30)
        template = ScoringTemplate(
            tiered_price_range = [
                make_weighted(3, (20, 40)),
                make_weighted(2, (40, 50)),
            ],
        )
        scores = generate_scores({"BBB": quote}, template)
        self.assertEqual(scores["BBB"], 3)

    def test_boolean_fields_add_weight(self):
        quote = make_test_quote("CCC", 40)
        quote.is_3ma_trending_up = True
        template = ScoringTemplate(is_3ma_trending_up = 10)
        scores = generate_scores({"CCC": quote}, template)
        self.assertEqual(scores["CCC"], 10)

    def test_no_matching_conditions_results_in_zero(self):
        quote = make_test_quote("DDD", 40)
        template = ScoringTemplate(
            avg_vol = make_weighted(1, (GT, 10_000_000)),
        )
        scores = generate_scores({"DDD": quote}, template)
        self.assertEqual(scores["DDD"], 0)

    def test_multiple_quotes_scored_individually(self):
        q1 = make_test_quote(
            "X",
            20,
            avg_vol = 2_000_000,
            market_cap = 5_000_000_000,
        )
        q2 = make_test_quote("Y", 20, avg_vol = 100, market_cap = 1_000_000)
        template = ScoringTemplate(
            avg_vol = make_weighted(1, (GT, 1_000)),
            market_cap = make_weighted(5, MID),
        )
        scores = generate_scores({"X": q1, "Y": q2}, template)
        self.assertGreater(scores["X"], scores["Y"])

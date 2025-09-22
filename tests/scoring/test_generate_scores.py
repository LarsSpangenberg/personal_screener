import unittest

from personal_screener.core.scoring.generate_quote_scores import \
    generate_scores
from personal_screener.schemas.scoring_template import ScoringTemplate
from personal_screener.schemas.types import GT, MID
from personal_screener.schemas.weighted_condition import make_weighted
from tests.utils import make_test_quote


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

    def test_additional_price_range_conditions_accumulating(self):
        quote = make_test_quote("BBB", 30)
        template = ScoringTemplate(
            price_range = make_weighted(5, (10, 40)), # matches
            additional = [
                ("price_range", make_weighted(2, (20, 25))),  # not matched
                ("price_range", make_weighted(3, (25, 35))),  # matched
            ],
        )
        scores = generate_scores({"BBB": quote}, template)
        # base + matching additional = 5 + 3
        self.assertEqual(scores["BBB"], 8)

    def test_additional_price_range_conditions_only_base_matches(self):
        quote = make_test_quote("DDD", 35)
        template = ScoringTemplate(
            price_range = make_weighted(5, (10, 40)),  # matches
            additional = [
                ("price_range", make_weighted(2, (20, 25))),  # not matched
                ("price_range", make_weighted(3, (50, 100))),  # not matched
            ],
        )
        scores = generate_scores({"DDD": quote}, template)
        # only base condition matches -> 5
        self.assertEqual(scores["DDD"], 5)

    def test_additional_price_range_conditions_only_one_additional_matches(
        self,
    ):
        quote = make_test_quote("EEE", 75)
        template = ScoringTemplate(
            price_range = make_weighted(5, (10, 40)),  # not matched
            additional = [
                ("price_range", make_weighted(2, (20, 25))),  # not matched
                ("price_range", make_weighted(3, (50, 100))),  # matches
            ],
        )
        scores = generate_scores({"EEE": quote}, template)
        # only one additional condition matches -> 3
        self.assertEqual(scores["EEE"], 3)

import unittest

from personal_screener.core.screen.sort_quotes import sort_quotes
from tests.utils import make_test_quote
from personal_screener.schemas.scoring_template import ScoringTemplate
from personal_screener.schemas.weighted_condition import make_weighted
from personal_screener.schemas.types import GT


class TestSortQuotes(unittest.TestCase):
    def setUp(self):
        self.q1 = make_test_quote("A", 50, avg_vol = 2_000_000)
        self.q2 = make_test_quote("B", 50, avg_vol = 100)

    def test_sort_by_score(self):
        template = ScoringTemplate(avg_vol = make_weighted(5, (GT, 1_000)))
        quotes = {"A": self.q1, "B": self.q2}
        result = sort_quotes(
            quotes,
            sort_by = "score",
            scoring_template = template,
        )
        self.assertEqual(result[0].symbol, "A")

    def test_sort_by_rsi(self):
        self.q1.rsi = 40
        self.q2.rsi = 60
        quotes = {"A": self.q1, "B": self.q2}
        result = sort_quotes(quotes, sort_by = "rsi")
        self.assertEqual(result[0].symbol, "B")

    def test_sort_by_name(self):
        quotes = {"B": self.q2, "A": self.q1}
        result = sort_quotes(quotes, sort_by = "name")
        self.assertEqual([q.symbol for q in result], ["A", "B"])

    def test_empty_quotes_returns_empty_list(self):
        result = sort_quotes({})
        self.assertEqual(result, [])

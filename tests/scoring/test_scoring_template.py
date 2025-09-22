import unittest

from personal_screener.schemas.scoring_template import ScoringTemplate
from personal_screener.schemas.weighted_condition import make_weighted


class TestScoringTemplate(unittest.TestCase):
    def test_initialize_with_none(self):
        st = ScoringTemplate()
        self.assertIsNone(st.market_cap)
        self.assertIsNone(st.ma50)
        self.assertIsNone(st.rsi)

    def test_initialize_with_weighted_conditions(self):
        st = ScoringTemplate(
            market_cap = make_weighted(2, "MID"),
            avg_vol = make_weighted(1, ("GT", 1_000_000)),
            rsi = make_weighted(3, ("LT", 70)),
        )
        self.assertEqual(st.market_cap.weight, 2)
        self.assertEqual(st.avg_vol.condition, ("GT", 1_000_000))
        self.assertEqual(st.rsi.condition, ("LT", 70))

    def test_tiered_price_range(self):
        st = ScoringTemplate(
            tiered_price_range = [
                make_weighted(1, (5.0, 10.0)),
                make_weighted(2, (10.0, 20.0)),
            ],
        )
        self.assertEqual(len(st.tiered_price_range), 2)
        self.assertEqual(st.tiered_price_range[0].condition, (5.0, 10.0))

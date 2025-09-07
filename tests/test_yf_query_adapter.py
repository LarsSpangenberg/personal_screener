import unittest
from unittest.mock import patch

from src.data.base_data import yf_filters, yf_queries
from src.data.base_data.yf_filters import map_filters_to_yf_query
from src.schemas.filters import ScreenerFilters


class TestYfAdapter(unittest.TestCase):
    #PATCH_BASIC = "src.data.base_data.yf_filters.create_basic_query"

    PATCH_BASIC = f"{yf_filters.__name__}.create_basic_query"
    PATCH_RANGE = f"{yf_queries.__name__}.create_range_query"
    PATCH_EQ = f"{yf_filters.__name__}.EquityQuery"

    def test_convert_filters_to_yf_query_with_price_range(self):
        filters = ScreenerFilters(price_range = (10, 20))

        with patch(self.PATCH_BASIC) as MockBasic, \
                patch(self.PATCH_RANGE) as MockRange, \
                patch(self.PATCH_EQ) as MockEQ:
            MockBasic.return_value = "dummy-basic"
            MockRange.return_value = "dummy-range"
            MockEQ.return_value = "final"

            eq = map_filters_to_yf_query(filters)
            self.assertEqual(eq, "final")

            # Region filter always applied
            MockBasic.assert_any_call("EQ", "region", "us")
            # Price range should use a range query on eodprice
            MockRange.assert_any_call("eodprice", 10, 20)

    def test_convert_filters_to_yf_query_with_market_cap_mid(self):
        filters = ScreenerFilters(market_cap = "MID")

        with patch(self.PATCH_BASIC) as MockBasic, \
                patch(self.PATCH_RANGE) as MockRange, \
                patch(self.PATCH_EQ) as MockEQ:
            MockBasic.return_value = "dummy-basic"
            MockRange.return_value = "dummy-range"
            MockEQ.return_value = "final"

            eq = map_filters_to_yf_query(filters)
            self.assertEqual(eq, "final")

            # Region filter always applied
            MockBasic.assert_any_call("EQ", "region", "us")
            # Market cap MID should map to a range query
            MockRange.assert_any_call(
                "intradaymarketcap", 2000000000, 10000000000,
            )

    def test_convert_filters_to_yf_query_query_creation(self):
        filters = ScreenerFilters(
            avg_volume = ("GTE", 500_000),
        )

        # Patch both create_basic_query and EquityQuery
        with patch(self.PATCH_BASIC) as MockBasic, \
                patch(self.PATCH_EQ) as MockEQ:
            MockBasic.return_value = "dummy"
            MockEQ.return_value = "final"

            eq = map_filters_to_yf_query(filters)

            # Ensure the function returned the final (EquityQuery) mock not
            # just ["dummy", "dummy", "dummy"]
            self.assertEqual(eq, "final")

            # Verify our helper was called with the expected arguments
            MockBasic.assert_any_call("EQ", "region", "us")
            MockBasic.assert_any_call(
                key = "avgdailyvol3m", operator = "GTE", value = 500_000,
            )

    def test_convert_filters_to_yf_query_includes_us_region_by_default(self):
        filters = ScreenerFilters()

        with patch(self.PATCH_BASIC) as MockBasic, \
                patch(self.PATCH_EQ) as MockEQ:
            MockBasic.return_value = "dummy"
            MockEQ.return_value = "final"

            eq = map_filters_to_yf_query(filters)

            # Should still return the final EquityQuery mock
            self.assertEqual(eq, "final")

            # The US region filter should always be added
            MockBasic.assert_any_call("EQ", "region", "us")


if __name__ == '__main__':
    unittest.main()

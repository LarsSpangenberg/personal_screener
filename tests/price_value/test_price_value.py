import unittest

from personal_screener.schemas.quote import Quote
from personal_screener.schemas.price_value import PriceValue
from tests.utils import make_test_quote


class TestPriceValue(unittest.TestCase):
    PATCH_DUMMY = "personal_screener.schemas.price_value"

    def setUp(self):
        self.quote = make_test_quote(
            "TEST",
            50.0,
            open_ = 49.0,
            high = 55.0,
            low = 48.0,
            close = 52.0,
        )

    def test_resolve_numeric_source(self):
        pv = PriceValue(100.0)
        self.assertEqual(pv.resolve(self.quote), 100.0)

    def test_resolve_open_high_low_close(self):
        self.assertEqual(PriceValue("OPEN").resolve(self.quote), 49.0)
        self.assertEqual(PriceValue("HIGH").resolve(self.quote), 55.0)
        self.assertEqual(PriceValue("LOW").resolve(self.quote), 48.0)
        self.assertEqual(PriceValue("CLOSE").resolve(self.quote), 52.0)

    def test_resolve_with_offset_absolute(self):
        pv = PriceValue("CLOSE", offset = 5.0)
        self.assertEqual(pv.resolve(self.quote), 57.0)

    def test_resolve_with_offset_percentage(self):
        pv = PriceValue("CLOSE", offset = 0.10, offset_as_pct = True)
        self.assertAlmostEqual(pv.resolve(self.quote), 52.0 * 1.10)

    def test_invalid_source_raises(self):
        with self.assertRaises(ValueError):
            PriceValue("INVALID").resolve(self.quote)

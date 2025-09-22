import unittest

from tests.utils import make_test_quote
from personal_screener.schemas.price_value import PriceValue
from personal_screener.core.evaluators.resolve_price_operand import \
    resolve_operand


class TestResolvePriceOperand(unittest.TestCase):
    def setUp(self):
        self.quote = make_test_quote(
            "TEST",
            50.0,
            open_ = 49,
            high = 55,
            low = 48,
            close = 52,
        )

    def test_none_operand_returns_none(self):
        self.assertIsNone(resolve_operand(self.quote, None))

    def test_number_operand_returns_float(self):
        self.assertEqual(resolve_operand(self.quote, 123), 123.0)

    def test_ohlc_string_operand(self):
        self.assertEqual(resolve_operand(self.quote, "OPEN"), 49.0)
        self.assertEqual(resolve_operand(self.quote, "CLOSE"), 52.0)

    def test_price_value_with_offset_operand(self):
        price_value = PriceValue("CLOSE", offset = 5.0)
        self.assertEqual(resolve_operand(self.quote, price_value), 57.0)

    def test_invalid_operand_raises(self):
        with self.assertRaises(ValueError):
            resolve_operand(self.quote, "NOT_A_FIELD")

import unittest

from personal_screener.core.evaluators.range_conditions import \
    evaluate_numeric_range


class TestNumericRangeCondition(unittest.TestCase):
    def test_value_within_range(self):
        self.assertTrue(evaluate_numeric_range(10, 5, 20))

    def test_value_below_min(self):
        self.assertFalse(evaluate_numeric_range(3, 5, 20))

    def test_value_above_max(self):
        self.assertFalse(evaluate_numeric_range(25, 5, 20))

    def test_min_only(self):
        self.assertTrue(evaluate_numeric_range(10, 5, None))
        self.assertFalse(evaluate_numeric_range(4, 5, None))
        self.assertTrue(evaluate_numeric_range(5, 5, None))

    def test_max_only(self):
        self.assertTrue(evaluate_numeric_range(10, None, 20))
        self.assertFalse(evaluate_numeric_range(25, None, 20))
        self.assertTrue(evaluate_numeric_range(20, None, 20))

    def test_no_bounds(self):
        self.assertTrue(evaluate_numeric_range(10, None, None))

    def test_boundary_values_included(self):
        self.assertTrue(evaluate_numeric_range(5, 5, 20))
        self.assertTrue(evaluate_numeric_range(20, 5, 20))


if __name__ == "__main__":
    unittest.main()

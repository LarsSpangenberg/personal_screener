import unittest

from personal_screener.core.evaluators.operator_conditions import \
    evaluate_numeric_operator_condition


class TestNumericOperatorCondition(unittest.TestCase):
    def test_gt_operator(self):
        self.assertTrue(evaluate_numeric_operator_condition(10, ("GT", 5)))
        self.assertFalse(evaluate_numeric_operator_condition(3, ("GT", 5)))

    def test_gte_operator(self):
        self.assertTrue(evaluate_numeric_operator_condition(5, ("GTE", 5)))
        self.assertFalse(evaluate_numeric_operator_condition(4, ("GTE", 5)))

    def test_lt_operator(self):
        self.assertTrue(evaluate_numeric_operator_condition(3, ("LT", 5)))
        self.assertFalse(evaluate_numeric_operator_condition(7, ("LT", 5)))

    def test_lte_operator(self):
        self.assertTrue(evaluate_numeric_operator_condition(5, ("LTE", 5)))
        self.assertFalse(evaluate_numeric_operator_condition(6, ("LTE", 5)))

    def test_eq_operator(self):
        self.assertTrue(evaluate_numeric_operator_condition(5, ("EQ", 5)))
        self.assertFalse(evaluate_numeric_operator_condition(5, ("EQ", 6)))

    # def test_none_filter_condition_returns_true(self):
    #     self.assertTrue(evaluate_numeric_operator_condition(5, None))
    #
    # def test_none_quote_value_returns_true(self):
    #     self.assertTrue(evaluate_numeric_operator_condition(None, ("GT", 5)))


if __name__ == "__main__":
    unittest.main()

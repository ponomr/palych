import unittest
from datetime import date

from workdays import business_days


class HiddenTests(unittest.TestCase):
    def test_weeks(self):
        self.assertEqual(business_days(date(2026, 11, 2), date(2026, 11, 9)), 5)
        self.assertEqual(business_days(date(2026, 11, 2), date(2026, 11, 16)), 10)

    def test_weekend_edges(self):
        self.assertEqual(business_days(date(2026, 11, 6), date(2026, 11, 9)), 1)
        self.assertEqual(business_days(date(2026, 11, 7), date(2026, 11, 9)), 0)

    def test_same_day(self):
        self.assertEqual(business_days(date(2026, 11, 4), date(2026, 11, 4)), 0)

    def test_reversed(self):
        with self.assertRaises(ValueError):
            business_days(date(2026, 11, 9), date(2026, 11, 2))


if __name__ == '__main__':
    unittest.main()

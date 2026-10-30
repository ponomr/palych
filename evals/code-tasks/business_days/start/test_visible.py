import unittest
from datetime import date

from workdays import business_days


class VisibleTests(unittest.TestCase):
    def test_monday_to_wednesday(self):
        self.assertEqual(business_days(date(2026, 11, 2), date(2026, 11, 4)), 2)


if __name__ == '__main__':
    unittest.main()

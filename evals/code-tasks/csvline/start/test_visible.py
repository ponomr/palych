import unittest

from csvline import parse_csv_line


class VisibleTests(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(parse_csv_line('a,b,c'), ['a', 'b', 'c'])

    def test_quoted_comma(self):
        self.assertEqual(parse_csv_line('a,"b,c",d'), ['a', 'b,c', 'd'])


if __name__ == '__main__':
    unittest.main()

import unittest

from durations import parse_duration


class HiddenTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(parse_duration('2h5s'), 7205)
        self.assertEqual(parse_duration('0s'), 0)
        self.assertEqual(parse_duration('90m'), 5400)
        self.assertEqual(parse_duration('1h1m1s'), 3661)

    def test_invalid(self):
        for text in ['', '5d', '30m1h', '1h1h', 'h', '-5m', '1h 30m', '1.5h', ' 1h']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_duration(text)


if __name__ == '__main__':
    unittest.main()

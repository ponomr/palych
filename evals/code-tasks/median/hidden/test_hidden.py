import unittest

from stats import median


class HiddenTests(unittest.TestCase):
    def test_even(self):
        self.assertEqual(median([1, 2, 3, 4]), 2.5)
        self.assertEqual(median([4, 1, 3, 2]), 2.5)

    def test_single(self):
        self.assertEqual(median([5]), 5)

    def test_empty(self):
        with self.assertRaises(ValueError):
            median([])

    def test_input_unchanged(self):
        values = [3, 1, 2]
        median(values)
        self.assertEqual(values, [3, 1, 2])

    def test_tuple(self):
        self.assertEqual(median((9, 7, 8)), 8)


if __name__ == '__main__':
    unittest.main()

import unittest

from intervals import merge_intervals


class HiddenTests(unittest.TestCase):
    def test_unsorted_and_touching(self):
        self.assertEqual(merge_intervals([(5, 7), (1, 3), (3, 4)]), [(1, 4), (5, 7)])

    def test_contained(self):
        self.assertEqual(merge_intervals([(1, 10), (2, 3)]), [(1, 10)])

    def test_empty_and_point(self):
        self.assertEqual(merge_intervals([]), [])
        self.assertEqual(merge_intervals([(2, 2)]), [(2, 2)])

    def test_returns_tuples_from_lists(self):
        self.assertEqual(merge_intervals([[1, 2], [2, 5]]), [(1, 5)])

    def test_reversed_interval(self):
        with self.assertRaises(ValueError):
            merge_intervals([(1, 2), (5, 3)])


if __name__ == '__main__':
    unittest.main()

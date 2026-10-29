import unittest

from intervals import merge_intervals


class VisibleTests(unittest.TestCase):
    def test_overlap(self):
        self.assertEqual(merge_intervals([(1, 4), (2, 6), (8, 9)]), [(1, 6), (8, 9)])


if __name__ == '__main__':
    unittest.main()

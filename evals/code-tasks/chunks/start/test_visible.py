import unittest

from chunks import chunk


class VisibleTests(unittest.TestCase):
    def test_even_split(self):
        self.assertEqual(chunk([1, 2, 3, 4], 2), [[1, 2], [3, 4]])


if __name__ == '__main__':
    unittest.main()

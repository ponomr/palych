import unittest

from chunks import chunk


class HiddenTests(unittest.TestCase):
    def test_last_partial_piece_kept(self):
        self.assertEqual(chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])
        self.assertEqual(chunk([1, 2], 5), [[1, 2]])

    def test_empty(self):
        self.assertEqual(chunk([], 3), [])

    def test_tuple_gives_lists(self):
        self.assertEqual(chunk((1, 2, 3), 2), [[1, 2], [3]])

    def test_bad_size(self):
        for size in (0, -1):
            with self.subTest(size=size), self.assertRaises(ValueError):
                chunk([1, 2], size)


if __name__ == '__main__':
    unittest.main()

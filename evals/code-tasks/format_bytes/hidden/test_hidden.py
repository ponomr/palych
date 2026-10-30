import unittest

from sizes import format_bytes


class HiddenTests(unittest.TestCase):
    def test_bytes(self):
        self.assertEqual(format_bytes(0), '0 B')
        self.assertEqual(format_bytes(1023), '1023 B')

    def test_whole_units_drop_zero(self):
        self.assertEqual(format_bytes(1024), '1 KB')
        self.assertEqual(format_bytes(1024 ** 2), '1 MB')
        self.assertEqual(format_bytes(3 * 1024 ** 3), '3 GB')

    def test_one_decimal(self):
        self.assertEqual(format_bytes(1100), '1.1 KB')
        self.assertEqual(format_bytes(int(2.7 * 1024 ** 2)), '2.7 MB')

    def test_rounding_up_moves_to_next_unit(self):
        self.assertEqual(format_bytes(1024 ** 2 - 1), '1 MB')

    def test_terabytes_are_the_largest_unit(self):
        self.assertEqual(format_bytes(1024 ** 5), '1024 TB')

    def test_negative(self):
        with self.assertRaises(ValueError):
            format_bytes(-1)


if __name__ == '__main__':
    unittest.main()

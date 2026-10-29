import unittest

from sizes import format_bytes


class VisibleTests(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(format_bytes(512), '512 B')
        self.assertEqual(format_bytes(1536), '1.5 KB')


if __name__ == '__main__':
    unittest.main()

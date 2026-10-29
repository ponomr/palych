import unittest

from slug import slugify


class VisibleTests(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(slugify('Hello, World!'), 'hello-world')


if __name__ == '__main__':
    unittest.main()

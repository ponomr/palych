import unittest

from slug import slugify


class HiddenTests(unittest.TestCase):
    def test_only_latin_and_digits_kept(self):
        self.assertEqual(slugify('  --Привет 2026--  '), '2026')
        self.assertEqual(slugify('a__b'), 'a-b')
        self.assertEqual(slugify('Ünïcode Test'), 'n-code-test')

    def test_nothing_left(self):
        for title in ['Привет', '', '---']:
            with self.subTest(title=title), self.assertRaises(ValueError):
                slugify(title)

    def test_length_limit(self):
        slug = slugify('word ' * 20)
        self.assertEqual(slug, '-'.join(['word'] * 8))
        self.assertLessEqual(len(slugify('x' * 50)), 40)


if __name__ == '__main__':
    unittest.main()

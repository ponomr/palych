import unittest

from csvline import parse_csv_line


class HiddenTests(unittest.TestCase):
    def test_escaped_quotes(self):
        self.assertEqual(parse_csv_line('a,"say ""hi""",b'), ['a', 'say "hi"', 'b'])

    def test_empty_fields(self):
        self.assertEqual(parse_csv_line(''), [''])
        self.assertEqual(parse_csv_line('a,,b'), ['a', '', 'b'])
        self.assertEqual(parse_csv_line('a,'), ['a', ''])
        self.assertEqual(parse_csv_line('""'), [''])

    def test_spaces_and_inner_quote_kept(self):
        self.assertEqual(parse_csv_line(' a , b'), [' a ', ' b'])
        self.assertEqual(parse_csv_line('a"b,c'), ['a"b', 'c'])

    def test_errors(self):
        for line in ['"abc', 'a,"b', '"a"b,c']:
            with self.subTest(line=line), self.assertRaises(ValueError):
                parse_csv_line(line)


if __name__ == '__main__':
    unittest.main()

import parser
import unittest


class TestParser(unittest.TestCase):
    def test_has_five_digits(self):
        line1 = "34319 19409 80008="
        expected1 = True
        line2 = "34319 19409 80008"
        expected2 = True
        line3 = "34319 19409 800082="
        expected3 = False
        line4 = "33586 19409 80014 55300="
        expected4 = True
        line5 = "34319 19409 8000="
        expected5 = False
        self.assertEqual(parser.has_five_digits(line1), expected1)
        self.assertEqual(parser.has_five_digits(line2), expected2)
        self.assertEqual(parser.has_five_digits(line3), expected3)
        self.assertEqual(parser.has_five_digits(line4), expected4)
        self.assertEqual(parser.has_five_digits(line5), expected5)


if __name__ == '__main__':
    unittest.main()

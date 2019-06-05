import parser
import unittest


class TestParser(unittest.TestCase):
    def test_handle_lines(self):
        lines1 = ["a b c", "d e", " "]
        expected1 = ["a b c"]
        lines2 = ["a b c", "d e f", "g "]
        expected2 = ["a b c", "d e f"]
        self.assertEqual(parser.handle_lines(lines1), expected1)
        self.assertEqual(parser.handle_lines(lines2), expected2)

if __name__ == '__main__':
    unittest.main()

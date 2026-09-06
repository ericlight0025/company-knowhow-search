import unittest

from menu import normalise_mode, parse_top


class MenuInputTest(unittest.TestCase):
    """驗證 Menu CLI 的輸入解析。"""

    def test_empty_top_uses_default(self):
        self.assertEqual(parse_top(""), 5)
        self.assertEqual(parse_top("  ", default=10), 10)

    def test_top_must_be_positive_integer(self):
        self.assertEqual(parse_top("10"), 10)
        with self.assertRaises(ValueError):
            parse_top("abc")
        with self.assertRaises(ValueError):
            parse_top("0")

    def test_mode_defaults_to_hybrid_and_rejects_unknown_mode(self):
        self.assertEqual(normalise_mode(""), "hybrid")
        self.assertEqual(normalise_mode(" KEYWORD "), "keyword")
        with self.assertRaises(ValueError):
            normalise_mode("unknown")


if __name__ == "__main__":
    unittest.main()

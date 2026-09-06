"""驗證範例資料維持為短小、可導航的 Knowledge Map 卡片。"""

from pathlib import Path
import unittest

from src.evaluation import EVALUATION_CASES


PROJECT_ROOT = Path(__file__).resolve().parents[1]
KNOWHOW_DIR = PROJECT_ROOT / "knowhow"
REQUIRED_SECTIONS = ("## 用途", "## 常見問法", "## 常見技術詞", "## 原始資料位置", "## 下一步", "## 關鍵結論")


class KnowledgeMapCardsTest(unittest.TestCase):
    def test_all_sample_cards_are_short_navigation_cards(self):
        cards = sorted(KNOWHOW_DIR.glob("*.md"))
        self.assertGreaterEqual(len(cards), 20)
        for card in cards:
            with self.subTest(card=card.name):
                content = card.read_text(encoding="utf-8")
                self.assertTrue(content.startswith("# "))
                self.assertTrue(all(section in content for section in REQUIRED_SECTIONS))
                self.assertGreaterEqual(len(content.splitlines()), 10)
                self.assertLessEqual(len(content.splitlines()), 40)

    def test_locator_evaluation_has_twelve_expected_cards(self):
        self.assertEqual(len(EVALUATION_CASES), 12)
        for case in EVALUATION_CASES:
            with self.subTest(case=case.case_id):
                self.assertEqual(case.category, "Knowledge Map 定位")
                self.assertTrue(case.relevant_files)
                for filename in case.relevant_files:
                    self.assertTrue((KNOWHOW_DIR / filename).is_file())


if __name__ == "__main__":
    unittest.main()

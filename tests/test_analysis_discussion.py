"""Static contract tests for the adaptive discussion workflow."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AnalysisDiscussionTests(unittest.TestCase):
    def setUp(self):
        self.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.reference = (ROOT / "references" / "analysis-discussion.md").read_text(
            encoding="utf-8"
        )
        self.evals = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))

    def test_skill_routes_complete_discussion_to_reference(self):
        self.assertIn("references/analysis-discussion.md", self.skill)
        self.assertIn("完整的结果讨论", self.skill)
        self.assertIn("不机械套齐", self.skill)

    def test_reference_has_adaptive_evidence_contract(self):
        required = (
            "先建证据清单",
            "先判定实验类型",
            "自适应选模块",
            "证据链写法",
            "误差分析的科学门槛",
            "可直接复用的正文骨架",
            "交付前检查",
            "重复性与准确度",
            "不能作为独立验证",
            "思考与改进",
        )
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, self.reference)

    def test_body_and_explanation_are_separated_without_forced_split(self):
        self.assertIn("先给“可写入报告的正文”，紧接“说明与溯源”", self.reference)
        self.assertIn("不拆成两份文件或另起页", self.reference)
        self.assertIn("正文也不主动提及“往届报告”", self.reference)

    def test_discussion_eval_cases_are_registered(self):
        self.assertEqual(self.evals["revision"], "5")
        by_id = {case["id"]: case for case in self.evals["evals"]}
        self.assertTrue({6, 7, 8}.issubset(by_id))
        for case_id in (6, 7, 8):
            self.assertGreaterEqual(len(by_id[case_id]["assertions"]), 4)
            self.assertTrue(by_id[case_id]["prompt"].strip())


if __name__ == "__main__":
    unittest.main()

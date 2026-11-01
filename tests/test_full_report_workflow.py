"""Static contracts for the full-report and design/manufacturing routes."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FullReportWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.full = (ROOT / "references/full-report-workflow.md").read_text(encoding="utf-8")
        cls.physics = (ROOT / "references/physics-report.md").read_text(encoding="utf-8")
        cls.design = (ROOT / "references/design-manufacturing-report.md").read_text(
            encoding="utf-8"
        )
        cls.evals = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))

    def test_skill_is_renamed_and_routes_all_modes(self):
        self.assertIn("name: shiyan-baogao", self.skill)
        for reference in (
            "references/full-report-workflow.md",
            "references/physics-report.md",
            "references/design-manufacturing-report.md",
        ):
            self.assertIn(reference, self.skill)
        self.assertIn("要求矩阵", self.skill)
        self.assertIn("只给数据", self.skill)

    def test_actual_experiment_evidence_can_override_generic_guide(self):
        for text in ("逐字稿", "现场照片", "本人观察", "本次变更"):
            with self.subTest(text=text):
                self.assertIn(text, self.design)
        self.assertIn("不能反过来仅凭指导书否定本次现场证据", self.design)
        self.assertIn("默认项—本次变更—证据", self.design)

    def test_physics_modes_and_observation_provenance_exist(self):
        for mode in ("数据/后半部分", "精简完整", "全面完整"):
            self.assertIn(mode, self.physics)
        for term in ("教师课件", "历史报告图", "浸蚀剂", "放大倍数"):
            self.assertIn(term, self.design)

    def test_new_eval_cases_and_package_metadata(self):
        self.assertEqual(self.evals["skill_name"], "shiyan-baogao")
        self.assertEqual(self.evals["revision"], "5")
        self.assertTrue({9, 10, 11, 12}.issubset({case["id"] for case in self.evals["evals"]}))
        openai = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        manifest = json.loads((ROOT / "release-manifest.json").read_text(encoding="utf-8"))
        self.assertIn("$shiyan-baogao", openai)
        self.assertEqual(manifest["name"], "shiyan-baogao")

    def test_both_neutral_templates_have_body_markers(self):
        for name in ("report-a4.tex", "report-landscape.tex"):
            template = (ROOT / "assets" / name).read_text(encoding="utf-8")
            self.assertEqual(template.count("%%% BEGIN BODY %%%"), 1)
            self.assertEqual(template.count("%%% END BODY %%%"), 1)


if __name__ == "__main__":
    unittest.main()

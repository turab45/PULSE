import unittest

from src.utils.parsers import (
    NO_GAPS,
    has_gap_analysis,
    has_meaningful_gaps,
    parse_gaps,
    parse_plan,
    parse_review_status,
    parse_soap,
)


class ParserTests(unittest.TestCase):
    def test_parse_soap_requires_all_sections(self):
        content = "S: tired\nO: BP 138/84\nA: needs evaluation\nP: order A1c"
        self.assertEqual(parse_soap(content), content)
        self.assertIsNone(parse_soap("S: tired\nO: BP 138/84"))

    def test_parse_gaps_handles_no_gaps_sentinel(self):
        self.assertEqual(parse_gaps("No gaps identified"), [NO_GAPS])
        self.assertFalse(has_meaningful_gaps([NO_GAPS]))
        self.assertTrue(has_gap_analysis([NO_GAPS]))

    def test_parse_gaps_extracts_bullets(self):
        gaps = parse_gaps("Care gaps:\n- Confirm A1c result\n* Review eye exam status")
        self.assertEqual(gaps, ["- Confirm A1c result", "* Review eye exam status"])
        self.assertTrue(has_meaningful_gaps(gaps))

    def test_parse_plan_requires_sections(self):
        plan = "Follow-up Actions:\n- Review labs\n\nPatient Message:\nDear [Patient], ..."
        self.assertEqual(parse_plan(plan), plan)
        self.assertIsNone(parse_plan("Follow-up Actions:\n- Review labs"))

    def test_parse_review_status(self):
        self.assertEqual(parse_review_status("APPROVED\nFINAL REPORT:\n..."), "approved")
        self.assertEqual(parse_review_status("ISSUES FOUND\nMissing plan"), "issues")


if __name__ == "__main__":
    unittest.main()

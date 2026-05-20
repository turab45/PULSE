import unittest

from src.agents.supervisor import determine_next_step


class SupervisorTests(unittest.TestCase):
    def test_routes_to_scribe_first(self):
        self.assertEqual(determine_next_step({"messages": []}), "scribe")

    def test_routes_to_gap_detector_after_soap(self):
        state = {"messages": [], "soap_note": "S: x\nO: x\nA: x\nP: x", "care_gaps": []}
        self.assertEqual(determine_next_step(state), "gap_detector")

    def test_routes_to_planner_after_gap_analysis_even_when_no_gaps(self):
        state = {
            "messages": [],
            "soap_note": "S: x\nO: x\nA: x\nP: x",
            "care_gaps": ["No gaps identified"],
        }
        self.assertEqual(determine_next_step(state), "planner")

    def test_routes_to_reviewer_after_plan(self):
        state = {
            "messages": [],
            "soap_note": "S: x\nO: x\nA: x\nP: x",
            "care_gaps": ["- Review A1c follow-up"],
            "follow_up_plan": "Follow-up Actions:\n- x\n\nPatient Message:\nDear [Patient], x",
        }
        self.assertEqual(determine_next_step(state), "reviewer")

    def test_routes_to_end_after_final_report(self):
        self.assertEqual(determine_next_step({"final_report": "APPROVED"}), "__end__")


if __name__ == "__main__":
    unittest.main()

"""
Unit Tests for Skills Gap Analyzer and Recommendation Engine
"""

import unittest
from modules.skills_gap_analyzer import analyze_skills_gap
from modules.recommendation_engine import generate_recommendations


class TestSkillsGapAndRecommendations(unittest.TestCase):

    def test_skills_gap_matching_and_missing(self):
        student_skills = ["Python", "Java", "Data Structures", "SQL"]
        res = analyze_skills_gap(student_skills, target_role="Software Development Engineer (SDE)")

        self.assertIn("Python", res["matching_core_skills"])
        self.assertIn("Data Structures", res["matching_core_skills"])
        self.assertTrue(len(res["missing_core_skills"]) > 0)
        self.assertTrue(0 <= res["readiness_percentage"] <= 100)
        self.assertIsInstance(res["learning_recommendations"], list)

    def test_recommendation_engine_backlog_criticality(self):
        rec = generate_recommendations(
            cgpa=7.5,
            aptitude_score=75,
            projects_count=2,
            internships_count=1,
            workshops_count=2,
            active_backlogs=1,
            target_role="Software Development Engineer (SDE)"
        )

        plan_7 = rec["plan_7_days"]
        has_backlog_action = any(p["category"] == "Academic Eligibility" for p in plan_7)
        self.assertTrue(has_backlog_action)

    def test_recommendation_engine_low_aptitude(self):
        rec = generate_recommendations(
            cgpa=8.0,
            aptitude_score=50,
            projects_count=2,
            internships_count=1,
            workshops_count=2,
            active_backlogs=0,
            target_role="Software Development Engineer (SDE)"
        )

        plan_7 = rec["plan_7_days"]
        has_aptitude_action = any("Aptitude" in p["category"] for p in plan_7)
        self.assertTrue(has_aptitude_action)


if __name__ == "__main__":
    unittest.main()

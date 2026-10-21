"""
Unit Tests for PDF Report Generator Module
"""

import unittest
from modules.report_generator import generate_placement_report


class TestReportGenerator(unittest.TestCase):

    def test_generate_pdf_bytes(self):
        student_profile = {
            "student_name": "Test Student",
            "cgpa": 8.2,
            "aptitude_score": 78,
            "projects_count": 3,
            "internships_count": 1,
            "workshops_count": 2,
            "active_backlogs": 0,
            "target_role": "Software Development Engineer (SDE)"
        }

        prediction_result = {
            "status_label": "Likely to be Placed",
            "probability": 84.5,
            "readiness_tier": "High Placement Probability"
        }

        eligibility_result = {
            "company_category": "Tier-2 Enterprise",
            "overall_status": "Fully Eligible",
            "checks": [
                {"criterion": "Minimum CGPA", "required": ">= 7.0", "actual": "8.20", "status": "PASS"},
                {"criterion": "Active Backlogs", "required": "<= 0", "actual": "0", "status": "PASS"}
            ]
        }

        skills_gap_result = {
            "matching_core_skills": ["Java", "Python", "SQL"],
            "missing_core_skills": ["System Design"],
            "readiness_percentage": 78.5
        }

        recommendations_result = {
            "plan_7_days": [
                {"area": "Aptitude Revision", "action": "Practice 20 questions daily", "target": "80% score"}
            ],
            "plan_30_days": [
                {"area": "Capstone Project", "action": "Deploy full stack app", "target": "Live URL"}
            ],
            "plan_60_days": [
                {"area": "Mock Interviews", "action": "Complete 5 mock interviews", "target": "Proficient"}
            ]
        }

        pdf_bytes = generate_placement_report(
            student_profile=student_profile,
            prediction_result=prediction_result,
            eligibility_result=eligibility_result,
            skills_gap_result=skills_gap_result,
            recommendations_result=recommendations_result
        )

        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 1000)
        # PDF files start with %PDF
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()

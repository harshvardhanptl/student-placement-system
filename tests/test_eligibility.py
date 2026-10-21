"""
Unit Tests for Academic & Corporate Eligibility Checker
"""

import unittest
from modules.eligibility_checker import check_eligibility, evaluate_all_tiers


class TestEligibilityChecker(unittest.TestCase):

    def test_tier1_eligible_candidate(self):
        res = check_eligibility(
            cgpa=8.5,
            aptitude_score=85,
            active_backlogs=0,
            projects_count=3,
            internships_count=1,
            company_category="Tier-1 Product / Tech MNC (e.g., Google, Microsoft, Amazon)"
        )
        self.assertEqual(res["overall_status"], "Fully Eligible")
        self.assertTrue(res["is_eligible"])
        self.assertEqual(len(res["failed_reasons"]), 0)

    def test_backlog_disqualification(self):
        res = check_eligibility(
            cgpa=9.0,
            aptitude_score=90,
            active_backlogs=2,
            projects_count=4,
            internships_count=2,
            company_category="Tier-1 Product / Tech MNC (e.g., Google, Microsoft, Amazon)"
        )
        self.assertEqual(res["overall_status"], "Ineligible")
        self.assertFalse(res["is_eligible"])
        self.assertTrue(any("backlog" in r.lower() for r in res["failed_reasons"]))

    def test_cgpa_cutoff_failure(self):
        res = check_eligibility(
            cgpa=5.8,
            aptitude_score=75,
            active_backlogs=0,
            projects_count=2,
            internships_count=0,
            company_category="Tier-2 Enterprise & Fintech (e.g., Oracle, Cisco, JPMorgan)"
        )
        self.assertEqual(res["overall_status"], "Ineligible")
        self.assertTrue(any("cgpa" in r.lower() for r in res["failed_reasons"]))

    def test_evaluate_all_tiers_returns_list(self):
        results = evaluate_all_tiers(cgpa=7.2, aptitude=70, backlogs=0, projects=2, internships=1)
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 3)


if __name__ == "__main__":
    unittest.main()

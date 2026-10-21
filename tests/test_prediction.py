"""
Unit Tests for Placement Prediction Module
"""

import unittest
from modules.placement_predictor import PlacementPredictor


class TestPlacementPrediction(unittest.TestCase):

    def setUp(self):
        self.predictor = PlacementPredictor()

    def test_input_validation_valid(self):
        val = self.predictor.validate_inputs(cgpa=8.5, aptitude_score=80, projects=3, internships=1, workshops=2)
        self.assertTrue(val["valid"])
        self.assertEqual(len(val["errors"]), 0)

    def test_input_validation_boundary_cgpa(self):
        val_low = self.predictor.validate_inputs(cgpa=-0.5, aptitude_score=70, projects=1, internships=0, workshops=0)
        self.assertFalse(val_low["valid"])

        val_high = self.predictor.validate_inputs(cgpa=10.5, aptitude_score=70, projects=1, internships=0, workshops=0)
        self.assertFalse(val_high["valid"])

    def test_input_validation_negative_counts(self):
        val = self.predictor.validate_inputs(cgpa=7.0, aptitude_score=70, projects=-2, internships=-1, workshops=0)
        self.assertFalse(val["valid"])

    def test_prediction_output_structure(self):
        res = self.predictor.predict(cgpa=8.8, aptitude_score=85, projects=4, internships=2, workshops=3)
        self.assertTrue(res["success"])
        self.assertIn("prediction", res)
        self.assertIn("probability", res)
        self.assertIn("status_label", res)
        self.assertIn("feature_contributions", res)
        self.assertTrue(0.0 <= res["probability"] <= 100.0)

    def test_prediction_low_profile(self):
        res = self.predictor.predict(cgpa=5.2, aptitude_score=35, projects=0, internships=0, workshops=0)
        self.assertTrue(res["success"])
        self.assertTrue(0.0 <= res["probability"] <= 100.0)
        self.assertIn(res["prediction"], [0, 1])


if __name__ == "__main__":
    unittest.main()

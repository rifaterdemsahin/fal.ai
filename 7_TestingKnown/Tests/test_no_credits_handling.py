#!/usr/bin/env python3
"""
Test for No-Credits Handling Feature
Tests that when credits are exhausted, the system generates and displays prompts with costs
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add 5_Symbols to path
project_root = Path(__file__).resolve().parent.parent.parent
symbols_path = project_root / "5_Symbols"
sys.path.insert(0, str(symbols_path))

from base.base_asset_generator import BaseAssetGenerator
from base.generator_config import SEEDS, BRAND_COLORS


class TestNoCreditsHandling(unittest.TestCase):
    """Test suite for no-credits handling feature"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_output = project_root / "7_TestingKnown" / "TestOutput" / "no_credits_test"
        self.test_output.mkdir(parents=True, exist_ok=True)
        
        # Create a mock generator class
        class MockGenerator(BaseAssetGenerator):
            def get_generation_queue(self):
                return [
                    {
                        "id": "1.0",
                        "name": "test_asset_1",
                        "prompt": "A beautiful sunset over mountains",
                        "scene": "1",
                        "priority": "HIGH",
                        "model": "fal-ai/flux/dev",
                    },
                    {
                        "id": "2.0",
                        "name": "test_asset_2",
                        "prompt": "A futuristic cityscape at night",
                        "scene": "2",
                        "priority": "MEDIUM",
                        "model": "fal-ai/flux/dev",
                    }
                ]
        
        self.MockGenerator = MockGenerator
    
    def test_is_credit_error_detection(self):
        """Test that credit errors are correctly identified"""
        generator = self.MockGenerator(
            output_dir=self.test_output,
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="image"
        )
        
        # Test various credit error messages
        credit_error_msgs = [
            "User is locked. Reason: Exhausted balance. Top up your balance at fal.ai/dashboard/billing.",
            "Insufficient credits remaining",
            "Credit limit exceeded",
            "No credits remaining",
        ]
        
        for msg in credit_error_msgs:
            self.assertTrue(generator.is_credit_error(msg), 
                          f"Should detect credit error in: {msg}")
        
        # Test non-credit errors
        other_errors = [
            "Network timeout",
            "Invalid API key",
            "Model not found",
        ]
        
        for msg in other_errors:
            self.assertFalse(generator.is_credit_error(msg),
                           f"Should not detect credit error in: {msg}")
    
    def test_dry_run_mode(self):
        """Test that dry-run mode displays prompts without making API calls"""
        generator = self.MockGenerator(
            output_dir=self.test_output,
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="image",
            dry_run=True
        )
        
        # Generate an asset in dry-run mode
        result = generator.generate_asset({
            "id": "1.0",
            "name": "test_asset",
            "prompt": "A beautiful sunset",
            "model": "fal-ai/flux/dev",
            "scene": "1",
            "priority": "HIGH"
        })
        
        # Verify result
        self.assertFalse(result["success"], "Dry-run should not succeed")
        self.assertEqual(result["error"], "Dry-run mode")
        self.assertTrue(result["dry_run"])
        self.assertIn("prompt", result)
        self.assertIn("estimated_cost", result)
        self.assertIn("model", result)
        self.assertEqual(result["prompt"], "A beautiful sunset")
        self.assertEqual(result["estimated_cost"], 0.05)  # flux/dev cost
    
    def test_credits_exhausted_mode(self):
        """Test that credits_exhausted flag triggers dry-run behavior"""
        generator = self.MockGenerator(
            output_dir=self.test_output,
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="image"
        )
        
        # Simulate credits exhausted
        generator.credits_exhausted = True
        
        # Try to generate an asset
        result = generator.generate_asset({
            "id": "1.0",
            "name": "test_asset",
            "prompt": "A futuristic cityscape",
            "model": "fal-ai/flux/dev",
            "scene": "1",
            "priority": "HIGH"
        })
        
        # Verify result
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "No credits available")
        self.assertTrue(result["dry_run"])
        self.assertIn("prompt", result)
        self.assertIn("estimated_cost", result)
    
    @patch('fal_client.subscribe')
    def test_credit_error_switches_to_dry_run(self, mock_subscribe):
        """Test that credit error during generation switches to dry-run mode"""
        # Set up mock to raise a credit error
        mock_subscribe.side_effect = Exception(
            "User is locked. Reason: Exhausted balance. Top up your balance at fal.ai/dashboard/billing."
        )
        
        generator = self.MockGenerator(
            output_dir=self.test_output,
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="image"
        )
        
        # Try to generate first asset (should fail with credit error)
        result1 = generator.generate_asset({
            "id": "1.0",
            "name": "test_asset_1",
            "prompt": "First asset",
            "model": "fal-ai/flux/dev",
            "scene": "1",
            "priority": "HIGH"
        })
        
        # Verify first result
        self.assertFalse(result1["success"])
        self.assertTrue(result1.get("credit_error", False))
        self.assertTrue(generator.credits_exhausted)
        
        # Try to generate second asset (should be in dry-run mode)
        result2 = generator.generate_asset({
            "id": "2.0",
            "name": "test_asset_2",
            "prompt": "Second asset",
            "model": "fal-ai/flux/dev",
            "scene": "2",
            "priority": "MEDIUM"
        })
        
        # Verify second result shows dry-run
        self.assertFalse(result2["success"])
        self.assertEqual(result2["error"], "No credits available")
        self.assertTrue(result2["dry_run"])
        self.assertIn("prompt", result2)
        self.assertEqual(result2["prompt"], "Second asset")
    
    def test_cost_information_in_results(self):
        """Test that cost and prompt information is included in results"""
        generator = self.MockGenerator(
            output_dir=self.test_output,
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="image",
            dry_run=True
        )
        
        # Generate assets with different models
        test_cases = [
            ("fal-ai/flux/dev", 0.05),
            ("fal-ai/flux/schnell", 0.01),
            ("fal-ai/minimax/video-01", 0.50),
        ]
        
        for model, expected_cost in test_cases:
            result = generator.generate_asset({
                "id": "1.0",
                "name": f"test_{model}",
                "prompt": f"Test prompt for {model}",
                "model": model,
                "scene": "1",
                "priority": "HIGH"
            })
            
            self.assertEqual(result["estimated_cost"], expected_cost,
                           f"Cost should be ${expected_cost} for {model}")
            self.assertEqual(result["model"], model)
            self.assertIn("prompt", result)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestNoCreditsHandling)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

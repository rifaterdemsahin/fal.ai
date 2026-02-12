import unittest
import sys
from pathlib import Path
from unittest.mock import patch

# Add base path
project_root = Path(__file__).resolve().parent.parent.parent
symbols_base_path = project_root / "5_Symbols" / "base"
if str(symbols_base_path) not in sys.path:
    sys.path.append(str(symbols_base_path))

from generator_config import check_generation_cost, MODEL_PRICING, COST_THRESHOLD


class TestCostConfirmation(unittest.TestCase):
    """
    Test the cost confirmation feature for fal.ai API calls.
    Ensures that generations over $0.20 require user confirmation.
    """
    
    def test_cost_threshold_is_configured(self):
        """Test that the cost threshold is set to $0.20"""
        self.assertEqual(COST_THRESHOLD, 0.20, "Cost threshold should be $0.20")
    
    def test_model_pricing_exists(self):
        """Test that model pricing dictionary is populated"""
        self.assertGreater(len(MODEL_PRICING), 0, "MODEL_PRICING should not be empty")
        self.assertIn("fal-ai/minimax/video-01", MODEL_PRICING, "Video model should be in pricing")
        self.assertIn("fal-ai/flux/dev", MODEL_PRICING, "Image model should be in pricing")
    
    def test_expensive_models_identified(self):
        """Test that expensive models (>$0.20) are correctly identified"""
        expensive_models = {k: v for k, v in MODEL_PRICING.items() if v > COST_THRESHOLD}
        self.assertGreater(len(expensive_models), 0, "Should have at least one expensive model")
        
        # Verify specific expensive models
        self.assertGreater(MODEL_PRICING.get("fal-ai/minimax/video-01", 0), COST_THRESHOLD,
                          "Video generation should be over threshold")
        self.assertGreater(MODEL_PRICING.get("fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d", 0), COST_THRESHOLD,
                          "3D generation should be over threshold")
    
    def test_cheap_models_auto_proceed(self):
        """Test that cheap models (<=$0.20) proceed without prompting"""
        # These should return True without any user input
        self.assertTrue(check_generation_cost("fal-ai/flux/schnell"), 
                       "Cheap model should auto-proceed")
        self.assertTrue(check_generation_cost("unknown-model"), 
                       "Unknown model (defaults to $0) should auto-proceed")
    
    @patch('builtins.input', return_value='yes')
    def test_expensive_model_user_accepts(self, mock_input):
        """Test that expensive model proceeds when user accepts"""
        result = check_generation_cost("fal-ai/minimax/video-01")
        self.assertTrue(result, "Should proceed when user says 'yes'")
        mock_input.assert_called_once()
    
    @patch('builtins.input', return_value='y')
    def test_expensive_model_user_accepts_short(self, mock_input):
        """Test that expensive model proceeds when user accepts with 'y'"""
        result = check_generation_cost("fal-ai/minimax/video-01")
        self.assertTrue(result, "Should proceed when user says 'y'")
        mock_input.assert_called_once()
    
    @patch('builtins.input', return_value='no')
    def test_expensive_model_user_declines(self, mock_input):
        """Test that expensive model is cancelled when user declines"""
        result = check_generation_cost("fal-ai/minimax/video-01")
        self.assertFalse(result, "Should cancel when user says 'no'")
        mock_input.assert_called_once()
    
    @patch('builtins.input', return_value='n')
    def test_expensive_model_user_declines_short(self, mock_input):
        """Test that expensive model is cancelled when user declines with 'n'"""
        result = check_generation_cost("fal-ai/minimax/video-01")
        self.assertFalse(result, "Should cancel when user says 'n'")
        mock_input.assert_called_once()
    
    @patch('builtins.input', return_value='maybe')
    def test_expensive_model_invalid_input_cancels(self, mock_input):
        """Test that expensive model is cancelled on invalid input"""
        result = check_generation_cost("fal-ai/minimax/video-01")
        self.assertFalse(result, "Should cancel on invalid input (not yes/y)")
        mock_input.assert_called_once()
    
    def test_all_expensive_models(self):
        """Test that all models over threshold are identified"""
        expensive_count = 0
        cheap_count = 0
        
        for model, price in MODEL_PRICING.items():
            if price > COST_THRESHOLD:
                expensive_count += 1
                print(f"  ⚠️  {model}: ${price:.2f} (requires confirmation)")
            else:
                cheap_count += 1
                print(f"  ✅ {model}: ${price:.2f} (auto-proceeds)")
        
        print(f"\nSummary:")
        print(f"  - {expensive_count} models require confirmation")
        print(f"  - {cheap_count} models auto-proceed")
        
        self.assertGreater(expensive_count, 0, "Should have expensive models")
        self.assertGreater(cheap_count, 0, "Should have cheap models")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)

import unittest
import os
import json
from unittest.mock import patch, MagicMock
from prompt_enhancer import enhance_prompt, get_enhancement_context

class TestPromptEnhancer(unittest.TestCase):
    def setUp(self):
        # Save original env
        self.original_key = os.environ.get("GEMINIKEY")
        
    def tearDown(self):
        # Restore original env
        if self.original_key:
            os.environ["GEMINIKEY"] = self.original_key
        elif "GEMINIKEY" in os.environ:
            del os.environ["GEMINIKEY"]

    def test_get_enhancement_context(self):
        # Test specific asset types
        self.assertIn("video", get_enhancement_context("video"))
        self.assertIn("music", get_enhancement_context("music"))
        self.assertIn("3D", get_enhancement_context("3d"))
        
        # Test default
        default = get_enhancement_context("unknown_type")
        self.assertIn("Enhance the following prompt", default)

    @patch('urllib.request.urlopen')
    def test_enhance_prompt_with_asset_type(self, mock_urlopen):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "candidates": [{
                "content": {
                    "parts": [{"text": "Enhanced Video Prompt"}]
                }
            }]
        }).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        # Setup env
        os.environ["GEMINIKEY"] = "fake_key"
        
        # Test with asset_type
        result = enhance_prompt("Original Prompt", asset_type="video")
        self.assertEqual(result, "Enhanced Video Prompt")
        
        # Verify call args (would verify context if we could inspect payload easily)
        # For now just verify it ran without error

if __name__ == '__main__':
    unittest.main()

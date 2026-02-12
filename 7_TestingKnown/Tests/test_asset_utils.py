#!/usr/bin/env python3
"""
Unit tests for asset_utils module
"""
import unittest
import json
import sys
from pathlib import Path

try:
    from base_test import BaseAssetGeneratorTest
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from base_test import BaseAssetGeneratorTest

# Add symbol root to path (BaseAssetGeneratorTest already adds it, but just in case)
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "5_Symbols"))

from Utils.asset_utils import (
    clean_description,
    generate_filename,
    extract_scene_number,
    ManifestTracker
)

class TestAssetUtils(BaseAssetGeneratorTest):
    """Test asset utility functions"""
    
    def test_clean_description(self):
        """Test the clean_description function"""
        self.assertEqual(clean_description("Ferrari Cart Morph"), "ferrari_cart_morph")
        self.assertEqual(clean_description("UK Streets Sunday"), "uk_streets_sunday")
        self.assertEqual(clean_description("test-name-with-dashes"), "test_name_with_dashes")
        self.assertEqual(clean_description("test@name#with$special"), "testnamewithspecial")
        self.assertEqual(clean_description("test  multiple   spaces"), "test_multiple_spaces")
        self.assertEqual(clean_description("_test_"), "test")
        self.assertEqual(clean_description("__test__"), "test")

    def test_generate_filename(self):
        """Test the generate_filename function"""
        result = generate_filename(1, "image", "ferrari cart morph", 1, "png")
        self.assertEqual(result, "001_image_ferrari_cart_morph_v1.png")
        
        result = generate_filename(4, "video", "uk streets", 2, "mp4")
        self.assertEqual(result, "004_video_uk_streets_v2.mp4")
        
        result = generate_filename(42, "icon", "test", 1, "png")
        self.assertEqual(result, "042_icon_test_v1.png")
        
        result = generate_filename(1, "image", "test", None, "png")
        self.assertEqual(result, "001_image_test.png")
        
        result = generate_filename(1, "image", "test", 1)
        self.assertEqual(result, "001_image_test_v1")

    def test_extract_scene_number(self):
        """Test the extract_scene_number function"""
        self.assertEqual(extract_scene_number("1.1"), 1)
        self.assertEqual(extract_scene_number("4.2"), 4)
        self.assertEqual(extract_scene_number("11.3"), 11)
        self.assertEqual(extract_scene_number("invalid"), 0)
        self.assertEqual(extract_scene_number(""), 0)
        self.assertEqual(extract_scene_number(None), 0)

    def test_manifest_tracker(self):
        """Test the ManifestTracker class"""
        project_dir = self.test_output_root / "utils_test"
        if not project_dir.exists():
            project_dir.mkdir(parents=True, exist_ok=True)
            
        tracker = ManifestTracker(project_dir)
        
        tracker.add_asset(
            filename="001_image_test_v1.png",
            prompt="Test prompt",
            asset_type="image",
            asset_id="1.1",
            result_url="https://example.com/image.png",
            local_path="/path/to/image.png",
            metadata={"scene": "Scene 1", "priority": "HIGH"}
        )
        
        self.assertEqual(len(tracker.assets), 1)
        asset = tracker.assets[0]
        self.assertEqual(asset["filename"], "001_image_test_v1.png")
        self.assertEqual(asset["prompt"], "Test prompt")
        self.assertEqual(asset["asset_type"], "image")
        self.assertEqual(asset["asset_id"], "1.1")
        self.assertIn("timestamp", asset)
        
        # Save manifest
        tracker.add_asset(
            filename="002_video_test_v1.mp4",
            prompt="Test prompt 2",
            asset_type="video",
            asset_id="2.1"
        )
        
        manifest_path = tracker.save_manifest()
        self.assertTrue(manifest_path.exists())
        
        # Load and verify the manifest
        with open(manifest_path, 'r') as f:
            manifest_data = json.load(f)
        
        self.assertEqual(manifest_data["total_assets"], 2)
        self.assertIn("generation_timestamp", manifest_data)
        self.assertIn("completion_timestamp", manifest_data)
        self.assertEqual(len(manifest_data["assets"]), 2)

if __name__ == "__main__":
    unittest.main()

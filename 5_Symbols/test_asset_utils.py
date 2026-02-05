#!/usr/bin/env python3
"""
Unit tests for asset_utils module
"""

import unittest
import json
import tempfile
from pathlib import Path
from asset_utils import (
    clean_description,
    generate_filename,
    extract_scene_number,
    ManifestTracker
)


class TestCleanDescription(unittest.TestCase):
    """Test the clean_description function"""
    
    def test_basic_cleaning(self):
        """Test basic string cleaning"""
        self.assertEqual(clean_description("Ferrari Cart Morph"), "ferrari_cart_morph")
        self.assertEqual(clean_description("UK Streets Sunday"), "uk_streets_sunday")
        
    def test_special_characters(self):
        """Test removal of special characters"""
        self.assertEqual(clean_description("test-name-with-dashes"), "test_name_with_dashes")
        self.assertEqual(clean_description("test@name#with$special"), "testnamewithspecial")
        
    def test_multiple_spaces(self):
        """Test handling of multiple spaces"""
        self.assertEqual(clean_description("test  multiple   spaces"), "test_multiple_spaces")
        
    def test_leading_trailing_underscores(self):
        """Test removal of leading/trailing underscores"""
        self.assertEqual(clean_description("_test_"), "test")
        self.assertEqual(clean_description("__test__"), "test")


class TestGenerateFilename(unittest.TestCase):
    """Test the generate_filename function"""
    
    def test_basic_filename(self):
        """Test basic filename generation"""
        result = generate_filename(1, "image", "ferrari cart morph", 1, "png")
        self.assertEqual(result, "001_image_ferrari_cart_morph_v1.png")
        
    def test_scene_number_padding(self):
        """Test scene number zero-padding"""
        result = generate_filename(4, "video", "uk streets", 2, "mp4")
        self.assertEqual(result, "004_video_uk_streets_v2.mp4")
        
        result = generate_filename(42, "icon", "test", 1, "png")
        self.assertEqual(result, "042_icon_test_v1.png")
        
    def test_no_version(self):
        """Test filename without version"""
        result = generate_filename(1, "image", "test", None, "png")
        self.assertEqual(result, "001_image_test.png")
        
    def test_no_extension(self):
        """Test filename without extension"""
        result = generate_filename(1, "image", "test", 1)
        self.assertEqual(result, "001_image_test_v1")


class TestExtractSceneNumber(unittest.TestCase):
    """Test the extract_scene_number function"""
    
    def test_valid_asset_ids(self):
        """Test extraction from valid asset IDs"""
        self.assertEqual(extract_scene_number("1.1"), 1)
        self.assertEqual(extract_scene_number("4.2"), 4)
        self.assertEqual(extract_scene_number("11.3"), 11)
        
    def test_invalid_asset_ids(self):
        """Test extraction from invalid asset IDs"""
        self.assertEqual(extract_scene_number("invalid"), 0)
        self.assertEqual(extract_scene_number(""), 0)
        self.assertEqual(extract_scene_number(None), 0)


class TestManifestTracker(unittest.TestCase):
    """Test the ManifestTracker class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.project_dir = Path(self.temp_dir)
        self.tracker = ManifestTracker(self.project_dir)
        
    def test_add_asset(self):
        """Test adding an asset to the manifest"""
        self.tracker.add_asset(
            filename="001_image_test_v1.png",
            prompt="Test prompt",
            asset_type="image",
            asset_id="1.1",
            result_url="https://example.com/image.png",
            local_path="/path/to/image.png",
            metadata={"scene": "Scene 1", "priority": "HIGH"}
        )
        
        self.assertEqual(len(self.tracker.assets), 1)
        asset = self.tracker.assets[0]
        self.assertEqual(asset["filename"], "001_image_test_v1.png")
        self.assertEqual(asset["prompt"], "Test prompt")
        self.assertEqual(asset["asset_type"], "image")
        self.assertEqual(asset["asset_id"], "1.1")
        self.assertIn("timestamp", asset)
        
    def test_save_manifest(self):
        """Test saving the manifest to a file"""
        self.tracker.add_asset(
            filename="001_image_test_v1.png",
            prompt="Test prompt 1",
            asset_type="image",
            asset_id="1.1"
        )
        self.tracker.add_asset(
            filename="002_video_test_v1.mp4",
            prompt="Test prompt 2",
            asset_type="video",
            asset_id="2.1"
        )
        
        manifest_path = self.tracker.save_manifest()
        self.assertTrue(manifest_path.exists())
        
        # Load and verify the manifest
        with open(manifest_path, 'r') as f:
            manifest_data = json.load(f)
        
        self.assertEqual(manifest_data["total_assets"], 2)
        self.assertIn("generation_timestamp", manifest_data)
        self.assertIn("completion_timestamp", manifest_data)
        self.assertEqual(len(manifest_data["assets"]), 2)
        
    def test_empty_manifest(self):
        """Test saving an empty manifest"""
        manifest_path = self.tracker.save_manifest()
        self.assertTrue(manifest_path.exists())
        
        with open(manifest_path, 'r') as f:
            manifest_data = json.load(f)
        
        self.assertEqual(manifest_data["total_assets"], 0)
        self.assertEqual(len(manifest_data["assets"]), 0)


if __name__ == "__main__":
    unittest.main()

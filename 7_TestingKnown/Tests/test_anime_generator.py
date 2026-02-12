#!/usr/bin/env python3
"""
Test script for Anime Generator - Validates functionality without API calls (mostly)
"""
import sys
import unittest
import json
from pathlib import Path
import datetime

try:
    from base_test import BaseAssetGeneratorTest
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from base_test import BaseAssetGeneratorTest

class TestAnimeGenerator(BaseAssetGeneratorTest):
    
    def test_anime_generator_structure(self):
        """Test the anime generator structure and imports without making API calls"""
        print("\n🧪 Testing Anime Generator Structure")
        
        # Test 1: Import the module
        try:
            from Images.BatchAssetGeneratorAnime import (
                load_storyline_from_file,
                DEFAULT_STORYLINE,
                ANIME_MODELS
            )
        except ImportError as e:
            self.fail(f"Failed to import BatchAssetGeneratorAnime: {e}")
            
        # Test 1.5: Import prompt enhancer
        try:
            from Utils.prompt_enhancer import enhance_prompt
            self.assertTrue(callable(enhance_prompt), "enhance_prompt should be callable")
        except ImportError as e:
            print(f"   ⚠️  Prompt enhancer is optional but requested. Error: {e}")

        # Test 2: Check default storyline
        self.assertIn("title", DEFAULT_STORYLINE)
        self.assertIn("scenes", DEFAULT_STORYLINE)
        self.assertGreater(len(DEFAULT_STORYLINE["scenes"]), 0)
        
        scene = DEFAULT_STORYLINE["scenes"][0]
        required_fields = ["id", "name", "scene", "description", "prompt"]
        for field in required_fields:
            self.assertIn(field, scene, f"Missing required field: {field}")
            
        # Test 3: Check anime models
        expected_models = ["minimax", "kling", "flux_anime", "flux_dev"]
        for model in expected_models:
            self.assertIn(model, ANIME_MODELS, f"Missing model: {model}")
            self.assertTrue(ANIME_MODELS[model].startswith("fal-ai/"), f"Invalid model ID: {ANIME_MODELS[model]}")

        # Test 4: Load example storyline
        example_path = self.project_root / "5_Symbols" / "Images" / "example_anime_storyline.json"
        if example_path.exists():
            storyline = load_storyline_from_file(example_path)
            self.assertIn("title", storyline)
            self.assertIn("scenes", storyline)
        else:
            print("   ⚠️  Example storyline not found (skipping check)")

        # Test 6: Check file naming convention
        from Utils.asset_utils import generate_filename, extract_scene_number
        
        scene_num = extract_scene_number("1.1")
        self.assertEqual(scene_num, 1)
        
        scene_num = extract_scene_number("10.5")
        self.assertEqual(scene_num, 10)
        
        filename = generate_filename(1, "anime", "hero_awakening", 1)
        self.assertTrue(filename.startswith("001_anime_"), f"Unexpected filename: {filename}")
        self.assertIn("hero_awakening", filename)
        self.assertTrue(filename.endswith("_v1"))

if __name__ == "__main__":
    unittest.main()

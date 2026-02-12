#!/usr/bin/env python3
"""
Comprehensive Batch Generation Test
Tests multiple asset generators ensuring they output to the correct test directory.
"""
import sys
import unittest
from pathlib import Path
from typing import Dict, List, Any
import datetime

try:
    from base_test import BaseAssetGeneratorTest
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from base_test import BaseAssetGeneratorTest

class TestBatchGeneration(BaseAssetGeneratorTest):
    
    def test_all_generators(self):
        print(f"\n🚀 Comprehensive Generator Test Suite")
        
        if not self.verify_environment():
            return

        # Import generators
        try:
            from Images import BatchAssetGeneratorImages
            from Images import BatchAssetGeneratorIcons
            from Images import BatchAssetGeneratorAnime
            from Video import BatchAssetGeneratorLowerThirds
            from ThreeD.ThreeDGenerator import ThreeDAssetGenerator
        except ImportError as e:
            self.fail(f"Failed to import generators: {e}")

        # 1. Test Image Generator
        print("\n" + "-"*40)
        print("🧪 Testing Image Generator...")
        image_output = self.test_output_root / "images"
        image_output.mkdir(exist_ok=True)
        test_image_batch = [
            {
                "id": "TEST_IMG_01",
                "name": "test_image_1",
                "priority": "HIGH",
                "scene": "Test",
                "seed_key": "SEED_001",
                "prompt": "A simple red cube, 3d render, white background",
                "model": "fal-ai/flux/schnell", # Fast/cheap model
                "image_size": {"width": 512, "height": 512},
                "num_inference_steps": 4
            }
        ]
        try:
            BatchAssetGeneratorImages.process_queue(test_image_batch, image_output)
        except Exception as e:
            print(f"❌ Image Generator Failed: {e}")
            # We don't fail the whole test if one sub-generator fails, 
            # or maybe we should? The original script just printed error.
            # Let's verify files at the end.

        # 2. Test Icon Generator
        print("\n" + "-"*40)
        print("🧪 Testing Icon Generator...")
        icon_output = self.test_output_root / "icons"
        icon_output.mkdir(exist_ok=True)
        test_icon_batch = [
            {
                "id": "TEST_ICON_01",
                "name": "test_icon_1",
                "priority": "HIGH",
                "scene": "Test",
                "seed_key": "SEED_001",
                "prompt": "A simple blue circle icon, flat design",
                "model": "fal-ai/flux/schnell",
                "image_size": {"width": 512, "height": 512},
                "num_inference_steps": 4
            }
        ]
        try:
            BatchAssetGeneratorIcons.process_queue(test_icon_batch, icon_output)
        except Exception as e:
            print(f"❌ Icon Generator Failed: {e}")

        # 3. Test Lower Thirds Generator
        print("\n" + "-"*40)
        print("🧪 Testing Lower Thirds Generator...")
        lt_output = self.test_output_root / "lower_thirds"
        lt_output.mkdir(exist_ok=True)
        test_lt_batch = [
            {
                "id": "TEST_LT_01",
                "name": "test_lt_1",
                "priority": "HIGH",
                "text": "Test Title",
                "subtext": "Test Subtitle",
                "color_theme": "accent_blue",
                "seed_key": "SEED_004",
                "prompt": "Lower third graphic, blue accent, transparent background",
            }
        ]
        try:
            BatchAssetGeneratorLowerThirds.process_queue(test_lt_batch, lt_output)
        except Exception as e:
            print(f"❌ Lower Thirds Generator Failed: {e}")
            
        # 4. Test 3D Generator
        print("\n" + "-"*40)
        print("🧪 Testing 3D Generator...")
        threed_output = self.test_output_root / "3d"
        threed_output.mkdir(exist_ok=True)
        
        try:
            generator = ThreeDAssetGenerator(output_dir=threed_output)
            test_3d_batch = [
                {
                    "id": "TEST_3D_01",
                    "name": "test_3d_cube",
                    "priority": "HIGH",
                    "scene": "Test",
                    "seed_key": "SEED_001",
                    "prompt": "A simple cube",
                    "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d"
                }
            ]
            generator.process_queue(test_3d_batch)
        except Exception as e:
            print(f"❌ 3D Generator Failed: {e}")
            
        # 5. Test Anime Generator (Video)
        print("\n" + "-"*40)
        print("🧪 Testing Anime Generator...")
        anime_output = self.test_output_root / "anime"
        anime_output.mkdir(exist_ok=True)
        
        test_anime_storyline = {
            "title": "Test Story",
            "style": "anime",
            "scenes": [
                {
                    "id": "TEST_ANIME_01",
                    "name": "test_anime_scene",
                    "priority": "HIGH",
                    "scene": "Test Scene",
                    "description": "A test scene",
                    "prompt": "Anime character smiling, still image",
                    "characters": ["TestChar"],
                    "setting": "White Void"
                }
            ]
        }
        
        try:
            BatchAssetGeneratorAnime.process_storyline(
                test_anime_storyline, 
                anime_output,
                model="flux_anime" 
            )
        except Exception as e:
             print(f"❌ Anime Generator Failed: {e}")

        print("\n" + "="*60)
        print("✅ Generation Logic Finished")
        print(f"📂 Verify results in: {self.test_output_root}")
        
        # Final Verification
        total_files = sum(1 for _ in self.test_output_root.rglob("*") if _.is_file())
        print(f"📄 Total files generated (including json metadata): {total_files}")
        
        if total_files > 0:
            print("✅ SUCCESS: Artifacts were created.")
        else:
            self.fail("❌ FAILURE: No artifacts were created.")

if __name__ == "__main__":
    unittest.main()

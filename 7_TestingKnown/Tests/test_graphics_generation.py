#!/usr/bin/env python3
"""
Test script for Graphics Generator with fal.ai integration.

This script validates the BatchAssetGeneratorGraphics module by running
a small test batch and verifying the output.
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

class TestGraphicsGeneration(BaseAssetGeneratorTest):
    
    def setUp(self):
        super().setUp()
        self.output_dir = self.test_output_root / "graphics"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def import_generator(self):
        try:
            from Images import BatchAssetGeneratorGraphics
            return BatchAssetGeneratorGraphics
        except ImportError as e:
            self.fail(f"Failed to load BatchAssetGeneratorGraphics: {e}\nVerify module exists in 5_Symbols/Images/")

    def create_test_batch(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "TEST_GRAPHIC_01",
                "name": "test_graphic",
                "priority": "HIGH",
                "scene": "Test Validation",
                "seed_key": "SEED_001",
                "prompt": "A simple graphic icon representing flow chart, white background",
                "image_size": {"width": 512, "height": 512},
                "num_inference_steps": 4,
                "model": "fal-ai/flux/schnell"
            }
        ]

    def test_graphics_generation(self):
        print(f"\n🚀 Graphics Generator Test Suite")
        
        if not self.verify_environment():
            return
        
        generator = self.import_generator()
        test_batch = self.create_test_batch()
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        for item in test_batch:
            item["name"] = f"{item['name']}_{timestamp}"

        print(f"🧪 Test Batch: {len(test_batch)} graphic(s)")
        print(f"📂 Output: {self.output_dir}")
        
        try:
            print("⏳ Generating assets...")
            generator.process_queue(test_batch, self.output_dir)
            
            generated = self.assertFilesGenerated(self.output_dir, [".png", ".jpg", ".jpeg"], min_count=1)
            
            print("\n" + "=" * 70)
            print("✅ TEST COMPLETE")
            print("=" * 70)
            print(f"\n📄 Generated Files:")
            for f in generated:
                size_kb = f.stat().st_size / 1024
                print(f"   • {f.name:<40} ({size_kb:>8.1f} KB)")
                
        except Exception as e:
            self.fail(f"Generation Failed: {e}")

if __name__ == "__main__":
    unittest.main()

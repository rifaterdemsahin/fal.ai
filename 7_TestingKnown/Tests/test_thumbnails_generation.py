#!/usr/bin/env python3
"""
Test script for Thumbnails Generator with fal.ai integration.

This script validates the BatchAssetGeneratorThumbnails module by running
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

class TestThumbnailsGeneration(BaseAssetGeneratorTest):
    
    def setUp(self):
        super().setUp()
        self.output_dir = self.test_output_root / "thumbnails"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def import_generator(self):
        try:
            from Images import BatchAssetGeneratorThumbnails
            return BatchAssetGeneratorThumbnails
        except ImportError as e:
            self.fail(f"Failed to load BatchAssetGeneratorThumbnails: {e}\nVerify module exists in 5_Symbols/Images/")

    def create_test_batch(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "TEST_THUMB_01",
                "name": "Test Thumbnail",
                "scene": "Thumbnail Scene 1",
                "prompt": "A test thumbnail with bright colors, 4k",
                "description": "Test Thumbnail Description"
            }
        ]

    def test_thumbnails_generation(self):
        print(f"\n🚀 Thumbnails Generator Test Suite")
        
        if not self.verify_environment():
            return
        
        generator = self.import_generator()
        test_batch = self.create_test_batch()
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        for item in test_batch:
            item["name"] = f"{item['name']}_{timestamp}"

        print(f"🧪 Test Batch: {len(test_batch)} thumbnail(s)")
        print(f"📂 Output: {self.output_dir}")
        
        try:
            print("⏳ Generating assets...")
            # Check if process_queue exists, otherwise loop manually
            if hasattr(generator, 'process_queue'):
                generator.process_queue(test_batch, self.output_dir)
            else:
                # Fallback for manual iteration if process_queue is missing
                for config in test_batch:
                    print(f"   • Processing {config['name']}...")
                    generator.generate_thumbnail(config, self.output_dir)
            
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

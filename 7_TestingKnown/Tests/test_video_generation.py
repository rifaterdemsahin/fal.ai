#!/usr/bin/env python3
"""
Test script for Video Generator with fal.ai integration.

This script validates the BatchAssetGeneratorVideo module by running
a small test batch and verifying the output.
"""
import sys
import unittest
from pathlib import Path
from typing import Dict, List, Any
import datetime

# Import BaseAssetGeneratorTest from the same directory
try:
    from base_test import BaseAssetGeneratorTest
except ImportError:
    # Handle the case where we might be running from a different context
    sys.path.append(str(Path(__file__).resolve().parent))
    from base_test import BaseAssetGeneratorTest

class TestVideoGeneration(BaseAssetGeneratorTest):
    
    def setUp(self):
        super().setUp()
        self.output_dir = self.test_output_root / "video"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def import_generator(self):
        """Import the BatchAssetGeneratorVideo module with error handling."""
        try:
            from Video import BatchAssetGeneratorVideo
            return BatchAssetGeneratorVideo
        except ImportError as e:
            self.fail(f"Failed to load BatchAssetGeneratorVideo: {e}\nVerify module exists in 5_Symbols/Video/")

    def create_test_batch(self) -> List[Dict[str, Any]]:
        """Define test video configurations."""
        return [
            {
                "id": "TEST_VIDEO_01",
                "name": "test_video_clip",
                "priority": "HIGH",
                "scene": "Test Validation",
                "prompt": "Cinematic shot of a calm ocean at sunset, 4k, slow motion waves",
                "model": "fal-ai/minimax/video-01",
                "duration_seconds": 5
            }
        ]

    def test_video_generation(self):
        """Main test execution function."""
        print(f"\n🚀 Video Generator Test Suite")
        
        # Verify environment
        if not self.verify_environment():
            return
        
        # Import module
        generator = self.import_generator()
        
        # Prepare test data
        test_batch = self.create_test_batch()
        
        # Add timestamp to filenames to prevent overwriting
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        for item in test_batch:
            item["name"] = f"{item['name']}_{timestamp}"

        print(f"🧪 Test Batch: {len(test_batch)} video(s)")
        print(f"📂 Output: {self.output_dir}")
        
        # Execute generation
        try:
            print("⏳ Generating assets...")
            generator.process_queue(test_batch, self.output_dir)
            
            # Assert files generated using the helper
            generated = self.assertFilesGenerated(self.output_dir, [".mp4", ".mov"], min_count=1)
            
            # Print results (similar to original script)
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

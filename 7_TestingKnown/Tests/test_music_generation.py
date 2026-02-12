#!/usr/bin/env python3
"""
Test script for Music Generator with fal.ai integration.

This script validates the BatchAssetGeneratorMusic module by running
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
    sys.path.append(str(Path(__file__).resolve().parent))
    from base_test import BaseAssetGeneratorTest

class TestMusicGeneration(BaseAssetGeneratorTest):
    
    def setUp(self):
        super().setUp()
        self.output_dir = self.test_output_root / "music"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def import_generator(self):
        """Import the BatchAssetGeneratorMusic module with error handling."""
        try:
            from Audio import BatchAssetGeneratorMusic
            return BatchAssetGeneratorMusic
        except ImportError as e:
            self.fail(f"Failed to load BatchAssetGeneratorMusic: {e}\nVerify module exists in 5_Symbols/Audio/")

    def create_test_batch(self) -> List[Dict[str, Any]]:
        """Define test music configurations."""
        return [
            {
                "id": "TEST_MUSIC_01",
                "name": "test_music_clip",
                "priority": "HIGH",
                "prompt": "Simple piano melody, calm, 30 seconds",
                "model": "fal-ai/stable-audio",
                "duration": 5  # Short duration for test
            }
        ]

    def test_music_generation(self):
        """Main test execution function."""
        print(f"\n🚀 Music Generator Test Suite")
        
        if not self.verify_environment():
            return
        
        generator = self.import_generator()
        test_batch = self.create_test_batch()
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        for item in test_batch:
            item["name"] = f"{item['name']}_{timestamp}"

        print(f"🧪 Test Batch: {len(test_batch)} music clip(s)")
        print(f"📂 Output: {self.output_dir}")
        
        try:
            print("⏳ Generating assets...")
            generator.process_queue(test_batch, self.output_dir)
            
            generated = self.assertFilesGenerated(self.output_dir, [".mp3", ".wav"], min_count=1)
            
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

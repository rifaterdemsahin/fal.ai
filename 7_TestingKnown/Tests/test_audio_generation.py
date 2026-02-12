#!/usr/bin/env python3
"""
Test script for Chapter Markers (Audio Generator)
"""
import sys
import unittest
from pathlib import Path
import datetime

try:
    from base_test import BaseAssetGeneratorTest
except ImportError:
    # Handle the case where we might be running from a different context
    sys.path.append(str(Path(__file__).resolve().parent))
    from base_test import BaseAssetGeneratorTest

class TestAudioGeneration(BaseAssetGeneratorTest):
    
    def setUp(self):
        super().setUp()
        self.output_dir = self.test_output_root / "markers"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def import_generator(self):
        try:
            from Audio import BatchAssetGeneratorAudio
            return BatchAssetGeneratorAudio
        except ImportError as e:
            self.fail(f"Failed to import BatchAssetGeneratorAudio: {e}")

    def test_marker_generation(self):
        print(f"\n🚀 Chapter Marker Test Suite")
        
        # Audio generation (markers) might not need FAL_KEY for this specific function, 
        # but BaseAssetGeneratorTest.verify_environment checks it. 
        # If it doesn't need it, we can skip the check or mock it.
        # But let's assume consistency is good.
        
        generator = self.import_generator()
        
        # Create a dummy EDL file
        dummy_edl = self.output_dir / "test_edl.md"
        dummy_edl.write_text("""
### **SCENE 1: HOOK & PROBLEM STATEMENT**
**Duration:** 0:00 - 0:45

### **SCENE 2: THE SOLUTION**
**Duration:** 0:45 - 2:00
""", encoding="utf-8")
        
        output_file = self.output_dir / "test_markers.txt"

        print(f"📂 Output directory: {self.output_dir}")
        print("🧪 Starting Chapter Marker Test...")

        try:
            generator.generate_chapter_markers(dummy_edl, output_file)
            
            self.assertTrue(output_file.exists(), "Output file not created")
            content = output_file.read_text()
            print(f"📄 Markers generated:\n{content}")
            
            print("\n" + "="*60)
            print("✅ Test Batch Complete")
            print("="*60)
            
        except Exception as e:
            self.fail(f"Error running generation: {e}")

if __name__ == "__main__":
    unittest.main()

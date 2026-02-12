#!/usr/bin/env python3
"""
Test script to verify output_format configuration
"""
import sys
import unittest
from pathlib import Path

try:
    from base_test import BaseAssetGeneratorTest
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from base_test import BaseAssetGeneratorTest

sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "5_Symbols"))

from base.generator_config import OUTPUT_FORMATS
from Images.ImageGenerator import ImageAssetGenerator
from Images.IconGenerator import IconAssetGenerator
from Video.LowerThirdsGenerator import LowerThirdsAssetGenerator
from Diagrams.DiagramGenerator import DiagramAssetGenerator

class TestOutputFormats(BaseAssetGeneratorTest):
    
    def test_output_formats(self):
        """Test that output formats are correctly configured"""
        print(f"\n🚀 Output Format Configuration Test Suite")
        
        # Test OUTPUT_FORMATS configuration
        print("\n📋 OUTPUT_FORMATS Configuration:")
        for asset_type, format in OUTPUT_FORMATS.items():
            print(f"   • {asset_type:15s} → {format}")
        
        # Test generator instances
        print("\n🔧 Testing Generator Instances:")
        
        generators = [
            ("ImageAssetGenerator", ImageAssetGenerator()),
            ("IconAssetGenerator", IconAssetGenerator()),
            ("LowerThirdsAssetGenerator", LowerThirdsAssetGenerator()),
            ("DiagramAssetGenerator", DiagramAssetGenerator()),
        ]
        
        for name, gen in generators:
            print(f"\n   {name}:")
            print(f"      Asset Type: {gen.asset_type}")
            print(f"      Output Format: {gen.output_format}")
            expected = OUTPUT_FORMATS.get(gen.asset_type)
            print(f"      Expected: {expected}")
            
            # Verify it matches expected
            self.assertEqual(gen.output_format, expected, f"Mismatch for {name}")
            print(f"      ✅ Correct!")
        
        # Test transparency requirements
        print("\n🎨 Transparency Requirements Summary:")
        print("\n   Assets REQUIRING transparency (PNG):")
        for asset_type, format in OUTPUT_FORMATS.items():
            if format == 'png' and asset_type not in ['svg']:
                print(f"      • {asset_type}")
        
        print("\n   Assets NOT requiring transparency (JPEG):")
        for asset_type, format in OUTPUT_FORMATS.items():
            if format == 'jpeg':
                print(f"      • {asset_type}")

if __name__ == "__main__":
    unittest.main()

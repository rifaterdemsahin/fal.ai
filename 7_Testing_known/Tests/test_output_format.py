#!/usr/bin/env python3
"""
Test script to verify output_format configuration
"""

import sys
from pathlib import Path

# Add symbol root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from base.generator_config import OUTPUT_FORMATS
from Images.ImageGenerator import ImageAssetGenerator
from Images.IconGenerator import IconAssetGenerator
from Video.LowerThirdsGenerator import LowerThirdsAssetGenerator
from Diagrams.DiagramGenerator import DiagramAssetGenerator


def test_output_formats():
    """Test that output formats are correctly configured"""
    
    print("="*60)
    print("Testing Output Format Configuration")
    print("="*60)
    
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
        print(f"      Expected: {OUTPUT_FORMATS.get(gen.asset_type, 'unknown')}")
        
        # Verify it matches expected
        expected = OUTPUT_FORMATS.get(gen.asset_type)
        if gen.output_format == expected:
            print(f"      ✅ Correct!")
        else:
            print(f"      ❌ Mismatch! Expected {expected}, got {gen.output_format}")
    
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
    
    print("\n" + "="*60)
    print("✅ Test Complete!")
    print("="*60)


if __name__ == "__main__":
    test_output_formats()

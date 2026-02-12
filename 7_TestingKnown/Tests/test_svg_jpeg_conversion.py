#!/usr/bin/env python3
"""
Test script to demonstrate SVG to JPEG conversion functionality
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
from Utils.asset_utils import convert_svg_to_jpeg, SVG_CONVERSION_AVAILABLE

class TestSvgJpegConversion(BaseAssetGeneratorTest):
    
    def test_conversion(self):
        """Test SVG to JPEG conversion with a sample SVG"""
        print(f"\n🚀 SVG to JPEG Conversion Test Suite")
        
        # Check if conversion is available
        if not SVG_CONVERSION_AVAILABLE:
            print("❌ SVG conversion not available. Install cairosvg and Pillow:")
            print("   pip install cairosvg Pillow")
            self.skipTest("SVG conversion dependencies missing")
        
        print("✅ cairosvg and Pillow are installed")
        
        # Look for existing SVG files
        # We can also create a dummy SVG for testing instead of relying on existing files
        temp_svg = self.test_output_root / "test_dummy.svg"
        temp_svg.write_text('<svg width="100" height="100"><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" /></svg>')
        
        svg_files = [temp_svg]
        
        # Also check other dirs if needed, but test should be self-contained
        print(f"Found {len(svg_files)} SVG file(s)")
        
        # Test conversion with first SVG
        svg_path = svg_files[0]
        print(f"Testing with: {svg_path.name}")
        print(f"SVG size: {svg_path.stat().st_size} bytes")
        
        # Convert to JPEG
        jpeg_path = convert_svg_to_jpeg(svg_path)
        
        self.assertIsNotNone(jpeg_path)
        self.assertTrue(jpeg_path.exists())
        
        jpeg_size = jpeg_path.stat().st_size
        svg_size = svg_path.stat().st_size
        
        print(f"✅ JPEG created: {jpeg_path.name}")
        print(f"JPEG size: {jpeg_size} bytes")
        print()
        print(f"📊 Comparison:")
        print(f"   SVG:  {svg_size:>8} bytes (vector)")
        print(f"   JPEG: {jpeg_size:>8} bytes (raster)")
        
        # Verify JPEG is valid
        try:
            from PIL import Image
            with Image.open(jpeg_path) as img:
                print(f"   Format: {img.format}")
                print(f"   Size: {img.size}")
                print(f"   Mode: {img.mode}")
                self.assertEqual(img.format, 'JPEG')
        except Exception as e:
            self.fail(f"Could not verify JPEG: {e}")

if __name__ == "__main__":
    unittest.main()

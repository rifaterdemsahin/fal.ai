#!/usr/bin/env python3
"""
Test script to demonstrate SVG to JPEG conversion functionality
"""

from pathlib import Path
from asset_utils import convert_svg_to_jpeg, SVG_CONVERSION_AVAILABLE

def test_conversion():
    """Test SVG to JPEG conversion with a sample SVG"""
    print("🧪 Testing SVG to JPEG Conversion")
    print("=" * 60)
    
    # Check if conversion is available
    if not SVG_CONVERSION_AVAILABLE:
        print("❌ SVG conversion not available. Install cairosvg and Pillow:")
        print("   pip install cairosvg Pillow")
        return False
    
    print("✅ cairosvg and Pillow are installed")
    print()
    
    # Look for existing SVG files
    test_dirs = [
        Path("../3_Simulation/Feb1Youtube/weekly/generated_svgs"),
        Path("./generated_svg"),
        Path("../3_Simulation/Feb1Youtube/generated_svgs"),
    ]
    
    svg_files = []
    for test_dir in test_dirs:
        if test_dir.exists():
            svg_files.extend(list(test_dir.glob("*.svg")))
    
    if not svg_files:
        print("⚠️  No SVG files found to test with")
        return False
    
    print(f"Found {len(svg_files)} SVG file(s)")
    print()
    
    # Test conversion with first SVG
    svg_path = svg_files[0]
    print(f"Testing with: {svg_path.name}")
    print(f"SVG size: {svg_path.stat().st_size} bytes")
    
    # Convert to JPEG
    jpeg_path = convert_svg_to_jpeg(svg_path)
    
    if jpeg_path and jpeg_path.exists():
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
        except Exception as e:
            print(f"⚠️  Could not verify JPEG: {e}")
        
        return True
    else:
        print("❌ JPEG conversion failed")
        return False


if __name__ == "__main__":
    success = test_conversion()
    print()
    if success:
        print("✅ Test passed!")
    else:
        print("❌ Test failed!")

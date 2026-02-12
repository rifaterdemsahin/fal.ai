#!/usr/bin/env python3
"""
Test JPEG conversion functionality
"""
import sys
import unittest
from pathlib import Path
from PIL import Image
import tempfile
import os

try:
    from base_test import BaseAssetGeneratorTest
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from base_test import BaseAssetGeneratorTest

class TestJpegConversion(BaseAssetGeneratorTest):
    
    def test_jpeg_conversion(self):
        """Test PNG to JPEG conversion with transparency handling"""
        print(f"\n🚀 JPEG Conversion Test Suite")
        
        # Use fixed directory
        temp_path = self.test_output_root / "jpeg_conversion_test"
        if not temp_path.exists():
            temp_path.mkdir(parents=True, exist_ok=True)
            
        print(f"📁 Test directory: {temp_path}")

        # Test 1: Create a simple PNG with solid background
        print("\n📋 Test 1: PNG with solid background")
        png_path_1 = temp_path / "test_solid.png"
        jpeg_path_1 = temp_path / "test_solid.jpeg"
        
        # Create a test image (100x100 red square)
        img1 = Image.new('RGB', (100, 100), color='red')
        img1.save(png_path_1, 'PNG')
        
        # Convert to JPEG
        with Image.open(png_path_1) as img:
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            img.save(jpeg_path_1, 'JPEG', quality=95, optimize=True)
        
        self.assertTrue(jpeg_path_1.exists())
        
        # Test 2: Create a PNG with transparency (RGBA)
        print("\n📋 Test 2: PNG with transparency (RGBA)")
        png_path_2 = temp_path / "test_transparent.png"
        jpeg_path_2 = temp_path / "test_transparent.jpeg"
        
        # Create a test image with transparency
        img2 = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))  # Semi-transparent red
        img2.save(png_path_2, 'PNG')
        
        # Convert to JPEG (should add white background)
        with Image.open(png_path_2) as img:
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            img.save(jpeg_path_2, 'JPEG', quality=95, optimize=True)
        
        self.assertTrue(jpeg_path_2.exists())
        
        # Test 3: Verify files exist and are valid
        print("\n📋 Test 3: Verify converted images")
        
        for path in [jpeg_path_1, jpeg_path_2]:
            try:
                with Image.open(path) as img:
                    print(f"   ✅ {path.name}: {img.size}, mode={img.mode}, format={img.format}")
                    self.assertEqual(img.format, 'JPEG')
            except Exception as e:
                self.fail(f"Failed to open {path.name}: {e}")

if __name__ == "__main__":
    unittest.main()

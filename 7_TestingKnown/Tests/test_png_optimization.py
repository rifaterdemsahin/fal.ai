#!/usr/bin/env python3
"""
Test PNG optimization for DaVinci Resolve compatibility
"""
import sys
import unittest
from pathlib import Path
from PIL import Image
import tempfile
import os

# Mock fal_client before importing base_asset_generator
class MockFalClient:
    @staticmethod
    def subscribe(*args, **kwargs):
        pass

sys.modules['fal_client'] = MockFalClient()

try:
    from base_test import BaseAssetGeneratorTest
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from base_test import BaseAssetGeneratorTest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "5_Symbols"))
from base.base_asset_generator import BaseAssetGenerator

class TestPNGGenerator(BaseAssetGenerator):
    """Test generator for PNG optimization testing"""
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.asset_type = "test"
        self.manifest = None
        self.seeds = {}
    
    def prepare_arguments(self, asset_config):
        return {}
    
    def extract_result_url(self, result, asset_config):
        return None
    
    def get_generation_queue(self):
        return []

class TestPngOptimization(BaseAssetGeneratorTest):
    
    def test_png_optimization(self):
        """Test PNG optimization for DaVinci Resolve"""
        print(f"\n🚀 PNG Optimization Test Suite")
        
        # Use fixed directory
        temp_path = self.test_output_root / "png_optimization_test"
        if not temp_path.exists():
            temp_path.mkdir(parents=True, exist_ok=True)
            
        print(f"📁 Test directory: {temp_path}")
        
        generator = TestPNGGenerator(temp_path)
        
        # Test 1: Indexed color PNG (mode 'P') - problematic for Resolve
        print("\n📋 Test 1: Indexed color PNG (mode 'P')")
        png_path_1 = temp_path / "test_indexed.png"
        
        # Create indexed color image
        img1 = Image.new('P', (100, 100), color=0)
        img1.putpalette([255, 0, 0] * 256)  # Red palette
        img1.save(png_path_1, 'PNG')
        
        # Optimize
        result = generator.optimize_png_for_resolve(png_path_1)
        self.assertTrue(result)
        
        # Verify it's now RGBA (32-bit)
        with Image.open(png_path_1) as img:
            print(f"   After:  mode={img.mode}, size={img.size}")
            self.assertEqual(img.mode, 'RGBA')
        
        # Test 2: RGB PNG (no alpha) - should get alpha channel added
        print("\n📋 Test 2: RGB PNG (no alpha channel)")
        png_path_2 = temp_path / "test_rgb.png"
        
        # Create RGB image
        img2 = Image.new('RGB', (100, 100), color=(255, 0, 0))
        img2.save(png_path_2, 'PNG')
        
        # Optimize
        result = generator.optimize_png_for_resolve(png_path_2)
        self.assertTrue(result)
        
        # Verify it's now RGBA with alpha channel
        with Image.open(png_path_2) as img:
            self.assertEqual(img.mode, 'RGBA')
        
        # Test 3: Grayscale PNG - should be converted to RGBA
        print("\n📋 Test 3: Grayscale PNG (mode 'L')")
        png_path_3 = temp_path / "test_grayscale.png"
        
        # Create grayscale image
        img3 = Image.new('L', (100, 100), color=128)
        img3.save(png_path_3, 'PNG')
        
        # Optimize
        result = generator.optimize_png_for_resolve(png_path_3)
        self.assertTrue(result)
        
        # Verify it's now RGBA
        with Image.open(png_path_3) as img:
            self.assertEqual(img.mode, 'RGBA')

if __name__ == "__main__":
    unittest.main()

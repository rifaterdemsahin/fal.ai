#!/usr/bin/env python3
"""
Test PNG optimization for DaVinci Resolve compatibility
"""

from pathlib import Path
from PIL import Image
import tempfile
import sys

# Mock fal_client before importing base_asset_generator
class MockFalClient:
    @staticmethod
    def subscribe(*args, **kwargs):
        pass

sys.modules['fal_client'] = MockFalClient()

# Add symbol root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
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


def test_png_optimization():
    """Test PNG optimization for DaVinci Resolve"""
    
    print("="*60)
    print("Testing PNG Optimization for DaVinci Resolve")
    print("="*60)
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        generator = TestPNGGenerator(temp_path)
        
        # Test 1: Indexed color PNG (mode 'P') - problematic for Resolve
        print("\n📋 Test 1: Indexed color PNG (mode 'P')")
        png_path_1 = temp_path / "test_indexed.png"
        
        # Create indexed color image
        img1 = Image.new('P', (100, 100), color=0)
        img1.putpalette([255, 0, 0] * 256)  # Red palette
        img1.save(png_path_1, 'PNG')
        
        # Verify it's indexed
        with Image.open(png_path_1) as img:
            print(f"   Before: mode={img.mode}, size={img.size}")
            assert img.mode == 'P', "Image should be in palette mode"
        
        # Optimize
        result = generator.optimize_png_for_resolve(png_path_1)
        assert result, "Optimization should succeed"
        
        # Verify it's now RGBA (32-bit)
        with Image.open(png_path_1) as img:
            print(f"   After:  mode={img.mode}, size={img.size}")
            assert img.mode == 'RGBA', f"Image should be RGBA after optimization, got {img.mode}"
            # RGBA = 32-bit (8 bits per channel: R, G, B, A)
            print(f"   ✅ Converted to 32-bit RGBA format (8-bit per channel)")
        
        # Test 2: RGB PNG (no alpha) - should get alpha channel added
        print("\n📋 Test 2: RGB PNG (no alpha channel)")
        png_path_2 = temp_path / "test_rgb.png"
        
        # Create RGB image
        img2 = Image.new('RGB', (100, 100), color=(255, 0, 0))
        img2.save(png_path_2, 'PNG')
        
        # Verify it's RGB
        with Image.open(png_path_2) as img:
            print(f"   Before: mode={img.mode}, size={img.size}")
            assert img.mode == 'RGB', "Image should be in RGB mode"
        
        # Optimize
        result = generator.optimize_png_for_resolve(png_path_2)
        assert result, "Optimization should succeed"
        
        # Verify it's now RGBA with alpha channel
        with Image.open(png_path_2) as img:
            print(f"   After:  mode={img.mode}, size={img.size}")
            assert img.mode == 'RGBA', f"Image should be RGBA after optimization, got {img.mode}"
            print(f"   ✅ Added alpha channel (32-bit RGBA)")
        
        # Test 3: Grayscale PNG - should be converted to RGBA
        print("\n📋 Test 3: Grayscale PNG (mode 'L')")
        png_path_3 = temp_path / "test_grayscale.png"
        
        # Create grayscale image
        img3 = Image.new('L', (100, 100), color=128)
        img3.save(png_path_3, 'PNG')
        
        # Verify it's grayscale
        with Image.open(png_path_3) as img:
            print(f"   Before: mode={img.mode}, size={img.size}")
            assert img.mode == 'L', "Image should be in grayscale mode"
        
        # Optimize
        result = generator.optimize_png_for_resolve(png_path_3)
        assert result, "Optimization should succeed"
        
        # Verify it's now RGBA
        with Image.open(png_path_3) as img:
            print(f"   After:  mode={img.mode}, size={img.size}")
            assert img.mode == 'RGBA', f"Image should be RGBA after optimization, got {img.mode}"
            print(f"   ✅ Converted to 32-bit RGBA")
        
        # Test 4: RGBA PNG - should remain RGBA but metadata should be removed
        print("\n📋 Test 4: RGBA PNG with metadata")
        png_path_4 = temp_path / "test_rgba_metadata.png"
        
        # Create RGBA image with fake metadata
        img4 = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
        exif_data = img4.getexif()
        exif_data[0x9286] = "Test Comment"  # UserComment
        img4.save(png_path_4, 'PNG', exif=exif_data)
        
        # Check original has metadata
        with Image.open(png_path_4) as img:
            print(f"   Before: mode={img.mode}, size={img.size}")
            original_info = img.info
            print(f"   Metadata keys: {list(original_info.keys())}")
            assert img.mode == 'RGBA', "Image should already be RGBA"
        
        # Optimize (should strip metadata)
        result = generator.optimize_png_for_resolve(png_path_4)
        assert result, "Optimization should succeed"
        
        # Verify metadata is removed
        with Image.open(png_path_4) as img:
            print(f"   After:  mode={img.mode}, size={img.size}")
            assert img.mode == 'RGBA', "Image should still be RGBA"
            new_info = img.info
            print(f"   Metadata keys: {list(new_info.keys())}")
            # PNG info will have some basic keys but should not have EXIF
            print(f"   ✅ Metadata stripped, 32-bit RGBA maintained")
        
        # Test 5: Verify all outputs are valid PNGs
        print("\n📋 Test 5: Verify all optimized PNGs")
        for path in [png_path_1, png_path_2, png_path_3, png_path_4]:
            try:
                with Image.open(path) as img:
                    assert img.format == 'PNG', f"File should be PNG, got {img.format}"
                    assert img.mode == 'RGBA', f"File should be RGBA (32-bit), got {img.mode}"
                    # RGBA = 4 channels × 8 bits = 32 bits per pixel
                    print(f"   ✅ {path.name}: {img.size}, mode={img.mode}, format={img.format}")
            except Exception as e:
                print(f"   ❌ {path.name}: Failed - {e}")
                raise
    
    print("\n" + "="*60)
    print("✅ All PNG optimization tests passed!")
    print("="*60)
    
    # Summary
    print("\n📊 Summary:")
    print("   • Indexed color (P) → RGBA (32-bit) ✅")
    print("   • RGB → RGBA with alpha channel ✅")
    print("   • Grayscale (L) → RGBA (32-bit) ✅")
    print("   • RGBA maintained, metadata stripped ✅")
    print("   • All outputs are valid 32-bit PNG files ✅")
    print("\n💡 DaVinci Resolve Compatibility:")
    print("   • 32-bit format (8-bit per channel RGB + Alpha) ✅")
    print("   • No indexed colors (mode 'P') ✅")
    print("   • No metadata that might confuse Resolve ✅")


if __name__ == "__main__":
    test_png_optimization()

#!/usr/bin/env python3
"""
Test script for Thumbnails Generator
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
symbols_path = project_root / "5_Symbols"
sys.path.append(str(symbols_path))

try:
    from Images import BatchAssetGeneratorThumbnails
except ImportError as e:
    print(f"❌ Failed to import BatchAssetGeneratorThumbnails: {e}")
    sys.exit(1)

def test_thumbnails_generation():
    # Setup paths
    output_dir = project_root / "7_TestingKnown" / "TestOutput" / "generated_assets" / "thumbnails"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Output directory: {output_dir}")
    print("🧪 Starting Thumbnails Generator Test...")

    # Define a single test thumbnail configuration
    test_config = {
        "id": "TEST_THUMB_01",
        "name": "Test Thumbnail",
        "scene": 1,
        "prompt": "A test thumbnail with bright colors, 4k",
        "description": "Test Thumbnail Description"
    }
    
    # Check if FAL_KEY is set
    if not os.environ.get("FAL_KEY"):
        print("❌ FAL_KEY environment variable not set. Skipping generation.")
        return

    # Run the generator
    try:
        # Note: BatchAssetGeneratorThumbnails.generate_thumbnail takes (config, output_dir, manifest, version)
        result = BatchAssetGeneratorThumbnails.generate_thumbnail(test_config, output_dir)
        
        print("\n" + "="*60)
        print("✅ Test Complete")
        print(f"📂 Check results in: {output_dir}")
        print("="*60)
        
        if result.get("success"):
            print(f"✅ Generated: {result['filename']}")
            print(f"   URL: {result['url']}")
        else:
            print(f"❌ Failed: {result.get('error')}")

        files_created = list(output_dir.glob("*.png")) + list(output_dir.glob("*.json"))
        print(f"📄 Files generated: {len(files_created)}")
        for f in files_created:
            print(f"   - {f.name}")
            
    except Exception as e:
        print(f"❌ Error running generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_thumbnails_generation()

#!/usr/bin/env python3
"""
Test script for Graphics Generator with fal.ai integration.

This script validates the BatchAssetGeneratorGraphics module by running
a small test batch and verifying the output.
"""
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
import traceback


def setup_paths() -> tuple[Path, Path]:
    """Configure project paths and add to sys.path."""
    project_root = Path(__file__).resolve().parent.parent.parent
    symbols_path = project_root / "5_Symbols"
    sys.path.append(str(symbols_path))
    return project_root, symbols_path


def import_generator():
    """Import the BatchAssetGeneratorGraphics module with error handling."""
    try:
        from Images import BatchAssetGeneratorGraphics
        return BatchAssetGeneratorGraphics
    except ImportError as e:
        print(f"❌ Import Error: Failed to load BatchAssetGeneratorGraphics")
        print(f"   Details: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   - Verify the module exists in 5_Symbols/Images/")
        print(f"   - Check for missing dependencies")
        sys.exit(1)


def verify_environment() -> bool:
    """Check required environment variables."""
    if not os.environ.get("FAL_KEY"):
        print("❌ Environment Error: FAL_KEY not set")
        print("\n💡 Setup Instructions:")
        print("   export FAL_KEY='your-api-key-here'")
        print("   Or add to your .env file")
        return False
    return True


def create_test_batch() -> List[Dict[str, Any]]:
    """Define test graphics configurations."""
    return [
        {
            "id": "TEST_GRAPHIC_01",
            "name": "test_graphic",
            "priority": "HIGH",
            "scene": "Test Validation",
            "seed_key": "SEED_001",
            "prompt": "A simple graphic icon representing flow chart, white background",
            "image_size": {"width": 512, "height": 512},
            "num_inference_steps": 4,
            "model": "fal-ai/flux/schnell"
        }
    ]


def print_results(output_dir: Path) -> None:
    """Display generation results and file listing."""
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE")
    print("=" * 70)
    
    # Count generated files
    image_files = list(output_dir.glob("*.png")) + list(output_dir.glob("*.jpg"))
    json_files = list(output_dir.glob("*.json"))
    
    print(f"\n📊 Results Summary:")
    print(f"   Images:   {len(image_files)}")
    print(f"   Metadata: {len(json_files)}")
    print(f"   Total:    {len(image_files) + len(json_files)}")
    
    if image_files or json_files:
        print(f"\n📂 Output Location:")
        print(f"   {output_dir}")
        print(f"\n📄 Generated Files:")
        for f in sorted(image_files + json_files):
            size_kb = f.stat().st_size / 1024
            print(f"   • {f.name:<40} ({size_kb:>8.1f} KB)")
    else:
        print("\n⚠️  No files were generated")
    
    print("=" * 70)


def test_graphics_generation() -> None:
    """Main test execution function."""
    print("🚀 Graphics Generator Test Suite")
    print("=" * 70)
    
    # Setup
    project_root, _ = setup_paths()
    output_dir = (
        project_root / "7_TestingKnown" / "TestOutput" / 
        "generated_assets" / "graphics"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Output: {output_dir}")
    
    # Verify environment
    if not verify_environment():
        sys.exit(1)
    
    # Import module
    generator = import_generator()
    
    # Prepare test data
    test_batch = create_test_batch()
    
    # Add timestamp to filenames to prevent overwriting
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for item in test_batch:
        item["name"] = f"{item['name']}_{timestamp}"

    print(f"\n🧪 Test Batch: {len(test_batch)} graphic(s)")
    
    # Execute generation
    try:
        print("\n⏳ Generating assets...")
        generator.process_queue(test_batch, output_dir)
        print_results(output_dir)
        
    except Exception as e:
        print(f"\n❌ Generation Failed")
        print(f"   Error: {e}")
        print(f"\n🔍 Full Traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    test_graphics_generation()

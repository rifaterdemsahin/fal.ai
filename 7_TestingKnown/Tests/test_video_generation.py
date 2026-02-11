#!/usr/bin/env python3
"""
Test script for Video Generator with fal.ai integration.

This script validates the BatchAssetGeneratorVideo module by running
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
    """Import the BatchAssetGeneratorVideo module with error handling."""
    try:
        from Video import BatchAssetGeneratorVideo
        return BatchAssetGeneratorVideo
    except ImportError as e:
        print(f"❌ Import Error: Failed to load BatchAssetGeneratorVideo")
        print(f"   Details: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   - Verify the module exists in 5_Symbols/Video/")
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
    """Define test video configurations."""
    return [
        {
            "id": "TEST_VIDEO_01",
            "name": "test_video_clip",
            "priority": "HIGH",
            "scene": "Test Validation",
            "prompt": "Cinematic shot of a calm ocean at sunset, 4k, slow motion waves",
            "model": "fal-ai/minimax/video-01",
            "duration_seconds": 5
        }
    ]


def print_results(output_dir: Path) -> None:
    """Display generation results and file listing."""
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE")
    print("=" * 70)
    
    # Count generated files (Video outputs can vary, checking common formats)
    video_files = list(output_dir.glob("*.mp4")) + list(output_dir.glob("*.mov"))
    json_files = list(output_dir.glob("*.json"))
    
    print(f"\n📊 Results Summary:")
    print(f"   Videos:   {len(video_files)}")
    print(f"   Metadata: {len(json_files)}")
    print(f"   Total:    {len(video_files) + len(json_files)}")
    
    if video_files or json_files:
        print(f"\n📂 Output Location:")
        print(f"   {output_dir}")
        print(f"\n📄 Generated Files:")
        for f in sorted(video_files + json_files):
            size_kb = f.stat().st_size / 1024
            print(f"   • {f.name:<40} ({size_kb:>8.1f} KB)")
    else:
        print("\n⚠️  No files were generated")
    
    print("=" * 70)


def test_video_generation() -> None:
    """Main test execution function."""
    print("🚀 Video Generator Test Suite")
    print("=" * 70)
    
    # Setup
    project_root, _ = setup_paths()
    output_dir = (
        project_root / "7_TestingKnown" / "TestOutput" / 
        "generated_assets" / "video"
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

    print(f"\n🧪 Test Batch: {len(test_batch)} video(s)")
    
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
    test_video_generation()

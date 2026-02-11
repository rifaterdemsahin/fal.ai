#!/usr/bin/env python3
"""
Test script for Music Generator with fal.ai integration.

This script validates the BatchAssetGeneratorMusic module by running
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
    """Import the BatchAssetGeneratorMusic module with error handling."""
    try:
        from Audio import BatchAssetGeneratorMusic
        return BatchAssetGeneratorMusic
    except ImportError as e:
        print(f"❌ Import Error: Failed to load BatchAssetGeneratorMusic")
        print(f"   Details: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   - Verify the module exists in 5_Symbols/Audio/")
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
    """Define test music configurations."""
    return [
        {
            "id": "TEST_MUSIC_01",
            "name": "test_music_clip",
            "priority": "HIGH",
            "prompt": "Simple piano melody, calm, 30 seconds",
            "model": "fal-ai/stable-audio",
            "duration": 5  # Short duration for test
        }
    ]


def print_results(output_dir: Path) -> None:
    """Display generation results and file listing."""
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE")
    print("=" * 70)
    
    # Count generated files (Music outputs can vary, checking common formats)
    audio_files = list(output_dir.glob("*.mp3")) + list(output_dir.glob("*.wav"))
    json_files = list(output_dir.glob("*.json"))
    
    print(f"\n📊 Results Summary:")
    print(f"   Audio:    {len(audio_files)}")
    print(f"   Metadata: {len(json_files)}")
    print(f"   Total:    {len(audio_files) + len(json_files)}")
    
    if audio_files or json_files:
        print(f"\n📂 Output Location:")
        print(f"   {output_dir}")
        print(f"\n📄 Generated Files:")
        for f in sorted(audio_files + json_files):
            size_kb = f.stat().st_size / 1024
            print(f"   • {f.name:<40} ({size_kb:>8.1f} KB)")
    else:
        print("\n⚠️  No files were generated")
    
    print("=" * 70)


def test_music_generation() -> None:
    """Main test execution function."""
    print("🚀 Music Generator Test Suite")
    print("=" * 70)
    
    # Setup
    project_root, _ = setup_paths()
    output_dir = (
        project_root / "7_TestingKnown" / "TestOutput" / 
        "generated_assets" / "music"
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

    print(f"\n🧪 Test Batch: {len(test_batch)} music clip(s)")
    
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
    test_music_generation()

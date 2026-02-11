#!/usr/bin/env python3
"""
Test script for Video Generator
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
symbols_path = project_root / "5_Symbols"
sys.path.append(str(symbols_path))

try:
    from Video import BatchAssetGeneratorVideo
except ImportError as e:
    print(f"❌ Failed to import BatchAssetGeneratorVideo: {e}")
    sys.exit(1)

def test_video_generation():
    # Setup paths
    output_dir = project_root / "7_TestingKnown" / "TestOutput" / "generated_assets" / "video"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Output directory: {output_dir}")
    print("🧪 Starting Video Generator Test...")

    # Define a small test batch
    test_batch = [
        {
            "id": "TEST_VIDEO_01",
            "name": "test_video_clip",
            "priority": "HIGH",
            "scene": "Test Validation",
            "prompt": "Cinematic shot of a calm ocean at sunset, 4k",
            "model": "fal-ai/minimax/video-01",
            "duration_seconds": 5
        }
    ]
    
    # Check if FAL_KEY is set
    if not os.environ.get("FAL_KEY"):
        print("❌ FAL_KEY environment variable not set. Skipping generation.")
        return

    # Run the generator
    try:
        results = BatchAssetGeneratorVideo.process_queue(test_batch, output_dir)
        
        print("\n" + "="*60)
        print("✅ Test Batch Complete")
        print(f"📂 Check results in: {output_dir}")
        print("="*60)
        
        # Verify if files were created
        # Note: Minimax/Video might output mp4 or other formats
        files_created = list(output_dir.glob("*.mp4")) + list(output_dir.glob("*.json"))
        print(f"📄 Files generated: {len(files_created)}")
        for f in files_created:
            print(f"   - {f.name}")
            
    except Exception as e:
        print(f"❌ Error running batch generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_video_generation()

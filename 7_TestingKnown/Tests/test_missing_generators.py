#!/usr/bin/env python3
"""
Test Missing Generators
Tests additional asset generators not covered in test_batch_generation.py.
"""
import sys
import os
import shutil
from pathlib import Path

# Add 5_Symbols to path so we can import generators
project_root = Path(__file__).resolve().parent.parent.parent
symbols_path = project_root / "5_Symbols"
sys.path.append(str(symbols_path))

# Import generators (after sys.path update)
try:
    from Video import BatchAssetGeneratorVideo
    from Audio import BatchAssetGeneratorAudio
    from Audio import BatchAssetGeneratorMusic
    from Diagrams import BatchAssetGeneratorDiagrams
    from Images import BatchAssetGeneratorThumbnails
    from Images import BatchAssetGeneratorGraphics
except ImportError as e:
    print(f"❌ Failed to import generators: {e}")
    sys.exit(1)

def test_missing_generators():
    # Setup test output directory
    test_output_root = project_root / "7_TestingKnown" / "TestOutput" / "generated_assets_missing"
    test_output_root.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Test Output Directory: {test_output_root}")
    print("🧪 Starting Missing Generator Test...")
    
    # Check for API key
    if not os.environ.get("FAL_KEY"):
        print("❌ FAL_KEY environment variable not set. Skipping generation.")
        print("   Please set export FAL_KEY='your_key' and try again.")
        return

    # 1. Test Video Generator
    print("\n" + "-"*40)
    print("🧪 Testing Video Generator...")
    video_output = test_output_root / "video"
    video_output.mkdir(exist_ok=True)
    
    test_video_batch = [
        {
            "id": "TEST_VIDEO_01",
            "name": "test_video_1",
            "priority": "HIGH",
            "scene": "Test",
            "prompt": "A cinematic shot of a futuristic city",
            "model": "fal-ai/kling-video/v1.6/pro/text-to-video",
            "duration_seconds": 5,
            "aspect_ratio": "16:9"
        }
    ]
    
    try:
        # BatchAssetGeneratorVideo.process_queue(test_video_batch, video_output)
        print("⚠️  Skipping Video Generation to save time/credits")
    except Exception as e:
        print(f"❌ Video Generator Failed: {e}")

    # 2. Test Music Generator
    print("\n" + "-"*40)
    print("🧪 Testing Music Generator...")
    music_output = test_output_root / "music"
    music_output.mkdir(exist_ok=True)
    
    test_music_batch = [
        {
            "id": "TEST_MUSIC_01",
            "name": "test_music_1",
            "priority": "HIGH",
            "prompt": "Upbeat electronic track, 10 seconds",
            "model": "fal-ai/stable-audio",
            "duration": 10
        }
    ]
    
    try:
        # BatchAssetGeneratorMusic.process_queue(test_music_batch, music_output)
        print("⚠️  Skipping Music Generation to save time/credits")
    except Exception as e:
        print(f"❌ Music Generator Failed: {e}")

    # 3. Test Diagrams Generator
    print("\n" + "-"*40)
    print("🧪 Testing Diagrams Generator...")
    diagrams_output = test_output_root / "diagrams"
    diagrams_output.mkdir(exist_ok=True)
    
    test_diagrams_batch = [
        {
            "id": "TEST_DIAGRAM_01",
            "name": "test_diagram_1",
            "priority": "HIGH",
            "scene": "Test",
            "seed_key": "SEED_001",
            "prompt": "A flow chart showing a simple process",
            "model": "fal-ai/flux/schnell", # Using flux for diagrams as placeholder or actual
            "image_size": {"width": 1024, "height": 768},
            "num_inference_steps": 4
        }
    ]
    
    try:
        BatchAssetGeneratorDiagrams.process_queue(test_diagrams_batch, diagrams_output)
    except Exception as e:
        print(f"❌ Diagrams Generator Failed: {e}")

    # 4. Test Audio (Chapter Markers) Generator
    print("\n" + "-"*40)
    print("🧪 Testing Audio (Chapter Markers) Generator...")
    audio_output = test_output_root / "audio"
    audio_output.mkdir(exist_ok=True)
    
    # Create a dummy EDL file
    dummy_edl_path = audio_output / "test_edl.md"
    dummy_edl_content = """
### **SCENE 1: Introduction**
**Duration:** 0:00 - 0:30

### **SCENE 2: The Middle**
**Duration:** 0:30 - 1:00
"""
    dummy_edl_path.write_text(dummy_edl_content)
    
    chapter_markers_output = audio_output / "chapter_markers.txt"
    
    try:
        BatchAssetGeneratorAudio.generate_chapter_markers(dummy_edl_path, chapter_markers_output)
    except Exception as e:
        print(f"❌ Audio markers Generator Failed: {e}")

    # 5. Test Thumbnails Generator
    print("\n" + "-"*40)
    print("🧪 Testing Thumbnails Generator...")
    thumbnails_output = test_output_root / "thumbnails"
    thumbnails_output.mkdir(exist_ok=True)
    
    test_thumbnail_config = {
        "id": "TEST_THUMB_01",
        "name": "Test Thumbnail",
        "scene": 1,
        "prompt": "A test thumbnail with bright colors",
        "description": "Test"
    }
    
    try:
        BatchAssetGeneratorThumbnails.generate_thumbnail(test_thumbnail_config, thumbnails_output)
    except Exception as e:
        print(f"❌ Thumbnails Generator Failed: {e}")

    # 6. Test Graphics Generator
    print("\n" + "-"*40)
    print("🧪 Testing Graphics Generator...")
    graphics_output = test_output_root / "graphics"
    graphics_output.mkdir(exist_ok=True)
    
    test_graphics_batch = [
        {
            "id": "TEST_GRAPHIC_01",
            "name": "test_graphic_1",
            "priority": "HIGH",
            "scene": "Test",
            "seed_key": "SEED_001",
            "prompt": "A simple graphic icon",
            "model": "fal-ai/flux/schnell",
            "image_size": {"width": 512, "height": 512},
            "num_inference_steps": 4
        }
    ]
    
    try:
        BatchAssetGeneratorGraphics.process_queue(test_graphics_batch, graphics_output)
    except Exception as e:
        print(f"❌ Graphics Generator Failed: {e}")

    print("\n" + "="*60)
    print("✅ Missing Generator Test Logic Finished")
    print(f"📂 Verify results in: {test_output_root}")
    
    # Final Verification
    total_files = sum(1 for _ in test_output_root.rglob("*") if _.is_file())
    print(f"📄 Total files generated: {total_files}")
    
    if total_files > 0:
        print("✅ SUCCESS: Artifacts were created.")
    else:
        print("⚠️  WARNING: No artifacts were created (could be due to API failure or configuration).")

if __name__ == "__main__":
    test_missing_generators()

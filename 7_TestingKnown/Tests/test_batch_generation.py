#!/usr/bin/env python3
"""
Test script to run a SMALL BATCH of image generations.
Output is saved to 7_TestingKnown/TestOutput.

Usage:
    python 7_TestingKnown/Tests/test_batch_generation.py

This script:
1. Imports BatchAssetGeneratorImages
2. Defines a small set of test assets (batch size = 2)
3. Generates them using FAL.AI API
4. Saves output to 7_TestingKnown/TestOutput
"""
import sys
import os
import json
from pathlib import Path

# Add 5_Symbols to path so we can import generators
project_root = Path(__file__).resolve().parent.parent.parent
symbols_path = project_root / "5_Symbols"
sys.path.append(str(symbols_path))

try:
    from Images import BatchAssetGeneratorImages
except ImportError as e:
    print(f"❌ Failed to import BatchAssetGeneratorImages from {symbols_path}: {e}")
    sys.exit(1)

def test_batch_generation():
    # Setup paths
    output_dir = project_root / "7_TestingKnown" / "TestOutput"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Output directory: {output_dir}")
    print("🧪 Starting Batch Generation Test...")

    # Define a small batch of test assets
    # Using 'flux/schnell' for speed and cost efficiency during testing
    test_batch = [
        {
            "id": "TEST_001",
            "name": "test_batch_image_1",
            "priority": "HIGH",
            "scene": "Test Validation",
            "seed_key": "SEED_001", 
            "prompt": "A futuristic digital workspace with glowing blue holographic interfaces, high quality, 4k",
            "model": "fal-ai/flux/schnell", 
            "image_size": {
                "width": 1024,
                "height": 576
            },
            "num_inference_steps": 4
        },
        {
            "id": "TEST_002",
            "name": "test_batch_image_2",
            "priority": "MEDIUM",
            "scene": "Test Validation",
            "seed_key": "SEED_002",
            "prompt": "Abstract geometric shapes in vibrant orange and teal colors, clean background, 4k",
            "model": "fal-ai/flux/schnell",
            "image_size": {
                "width": 1024,
                "height": 576
            },
            "num_inference_steps": 4
        }
    ]
    
    print(f"📊 Batch size: {len(test_batch)}")
    
    # Check if FAL_KEY is set
    if not os.environ.get("FAL_KEY"):
        print("❌ FAL_KEY environment variable not set. Skipping generation.")
        print("   Please set export FAL_KEY='your_key' and try again.")
        return

    # Run the generator
    # We call process_queue directly, passing our test batch and output directory
    try:
        results = BatchAssetGeneratorImages.process_queue(test_batch, output_dir)
        
        print("\n" + "="*60)
        print("✅ Test Batch Complete")
        print(f"📂 Check results in: {output_dir}")
        print("="*60)
        
        # Verify if files were created
        files_created = list(output_dir.glob("*.png")) + list(output_dir.glob("*.json"))
        print(f"📄 Files generated: {len(files_created)}")
        for f in files_created:
            print(f"   - {f.name}")
            
    except Exception as e:
        print(f"❌ Error running batch generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_batch_generation()

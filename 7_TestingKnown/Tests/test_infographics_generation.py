#!/usr/bin/env python3
"""
Test script for Infographics Generator
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
symbols_path = project_root / "5_Symbols"
sys.path.append(str(symbols_path))

try:
    from Images import BatchAssetGeneratorInfographics
except ImportError as e:
    print(f"❌ Failed to import BatchAssetGeneratorInfographics: {e}")
    sys.exit(1)

def test_infographics_generation():
    # Setup paths
    output_dir = project_root / "7_TestingKnown" / "TestOutput" / "generated_assets" / "infographics"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Output directory: {output_dir}")
    print("🧪 Starting Infographics Generator Test...")

    # Define a small test batch
    test_batch = [
        {
            "id": "TEST_INFOGRAPHIC_01",
            "name": "test_infographic",
            "priority": "HIGH",
            "scene": "Test Validation",
            "seed_key": "SEED_001",
            "prompt": "Infographic showing data flow",
            "image_size": {"width": 1280, "height": 720},
            "num_inference_steps": 4,
            "model": "fal-ai/flux/schnell"
        }
    ]
    
    # Check if FAL_KEY is set
    if not os.environ.get("FAL_KEY"):
        print("❌ FAL_KEY environment variable not set. Skipping generation.")
        return

    # Run the generator
    try:
        BatchAssetGeneratorInfographics.process_queue(test_batch, output_dir)
        
        print("\n" + "="*60)
        print("✅ Test Batch Complete")
        print(f"📂 Check results in: {output_dir}")
        print("="*60)
        
        files_created = list(output_dir.glob("*.png")) + list(output_dir.glob("*.json"))
        print(f"📄 Files generated: {len(files_created)}")
        for f in files_created:
            print(f"   - {f.name}")
            
    except Exception as e:
        print(f"❌ Error running batch generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_infographics_generation()

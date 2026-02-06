#!/usr/bin/env python3
"""
Run Music Generator for Feb 1 Video
Simple script to generate music assets for the Feb1Youtube project
"""

import sys
import os
from pathlib import Path

# Add 5_Symbols to path
sys.path.insert(0, str(Path(__file__).parent / "5_Symbols"))

# Import the music generator
import BatchAssetGeneratorMusic as music_gen

# Set the output directory to Feb1Youtube
OUTPUT_DIR = Path(__file__).parent / "3_Simulation" / "Feb1Youtube" / "generated_music"

def main():
    """Run the music generator for Feb1Youtube"""
    print("\n" + "="*60)
    print("🎵 Running Music Generator for Feb 1 Video")
    print("="*60)
    
    # Check API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("\n❌ ERROR: FAL_KEY environment variable not set")
        print("   Set it with: export FAL_KEY='your-api-key-here'")
        print("   Get your key from: https://fal.ai/dashboard/keys")
        return 1
    
    print(f"\n✅ API Key found")
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}")
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Run the music generation
    print("\n🚀 Starting music generation...")
    results = music_gen.process_queue(music_gen.GENERATION_QUEUE, OUTPUT_DIR)
    
    # Print summary
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    print("\n" + "="*60)
    print("📊 FINAL SUMMARY")
    print("="*60)
    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    if successful:
        print("\n✅ Generated files in:")
        print(f"   {OUTPUT_DIR.absolute()}")
    
    return 0 if len(failed) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

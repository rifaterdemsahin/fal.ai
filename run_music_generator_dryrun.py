#!/usr/bin/env python3
"""
Dry-run Music Generator for Feb 1 Video
Simulates music generation without making actual API calls
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add 5_Symbols to path
sys.path.insert(0, str(Path(__file__).parent / "5_Symbols"))

# Import the music generator
import BatchAssetGeneratorMusic as music_gen

# Set the output directory to Feb1Youtube
OUTPUT_DIR = Path(__file__).parent / "3_Simulation" / "Feb1Youtube" / "generated_music"

def simulate_generation(track_config, output_dir):
    """Simulate generation of a single track"""
    print(f"\n{'='*60}")
    print(f"🎵 Simulating: {track_config['name']}")
    print(f"   Priority: {track_config.get('priority', 'MEDIUM')}")
    print(f"   Model: {track_config['model']}")
    print(f"   Duration: {track_config['seconds_total']}s")
    print(f"{'='*60}")
    print(f"⏳ Would send request to fal.ai...")
    print(f"   Prompt: {track_config['prompt'][:100]}...")
    print(f"✅ Simulation successful!")
    
    # Create mock metadata
    filename_audio = f"{track_config['name']}.mp3"
    filename_json = f"{track_config['name']}.json"
    
    metadata = {
        **track_config,
        "result_url": f"https://fal.ai/files/mock/{track_config['id']}.mp3",
        "filename": filename_audio,
        "simulated": True,
        "timestamp": datetime.now().isoformat(),
    }
    
    # Save metadata (but not actual audio in dry-run)
    output_path = output_dir / filename_json
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"💾 Metadata saved: {output_path}")
    print(f"💾 Would download audio to: {output_dir / filename_audio}")
    
    return {
        "success": True,
        "asset_id": track_config.get("id", "unknown"),
        "name": track_config["name"],
        "priority": track_config.get("priority", "MEDIUM"),
        "url": metadata["result_url"],
        "simulated": True,
    }

def main():
    """Run the music generator in dry-run mode"""
    print("\n" + "="*60)
    print("🎵 DRY-RUN: Music Generator for Feb 1 Video")
    print("="*60)
    print("\n⚠️  Running in SIMULATION mode (no actual API calls)")
    print("   This demonstrates what would happen with a valid FAL_KEY")
    
    print(f"\n📁 Output directory: {OUTPUT_DIR.absolute()}")
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get the queue
    queue = music_gen.GENERATION_QUEUE
    print(f"\n🎵 Tracks to generate: {len(queue)}")
    
    # Simulate generation
    results = []
    for i, track in enumerate(queue, 1):
        print(f"\n\n{'#'*60}")
        print(f"# Track {i}/{len(queue)}")
        print(f"{'#'*60}")
        
        result = simulate_generation(track, OUTPUT_DIR)
        results.append(result)
    
    # Save summary
    summary_path = OUTPUT_DIR / "generation_summary_dryrun.json"
    with open(summary_path, 'w') as f:
        json.dump({
            "total": len(results),
            "successful": len(results),
            "failed": 0,
            "simulated": True,
            "timestamp": datetime.now().isoformat(),
            "results": results,
        }, f, indent=2)
    
    # Print summary
    print("\n\n" + "="*60)
    print("📊 DRY-RUN SUMMARY")
    print("="*60)
    print(f"✅ Simulated generations: {len(results)}")
    print(f"\n💾 Summary saved: {summary_path}")
    
    print("\n" + "="*60)
    print("📋 NEXT STEPS TO RUN ACTUAL GENERATION")
    print("="*60)
    print("\n1. Get your fal.ai API key:")
    print("   → Visit: https://fal.ai/dashboard/keys")
    print("   → Sign up or log in")
    print("   → Create and copy your API key")
    print("\n2. Set the environment variable:")
    print("   export FAL_KEY='your-api-key-here'")
    print("\n3. Run the actual generator:")
    print("   python3 run_music_generator_feb1.py")
    print("\n💰 Estimated cost: $0.06 USD (3 tracks × $0.02)")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

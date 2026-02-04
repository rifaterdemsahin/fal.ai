#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Music
Project: The Agentic Era - Managing 240+ Workflows
Generates background music tracks based on EDL suggestions
"""

import os
import json
from pathlib import Path
from typing import Dict, List

# Install: pip install fal-client
try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

# Configuration
OUTPUT_DIR = Path("./generated_music")
OUTPUT_DIR.mkdir(exist_ok=True)

# Asset generation queue
# Derived from "Music Suggestions" in EDL
GENERATION_QUEUE = [
    {
        "id": "music_01",
        "name": "tech_innovation_background",
        "priority": "HIGH",
        "prompt": "Upbeat, tech-focused background track, modern synthesizer, rhythmic, innovation, energetic but not distracting, suitable for technology tutorial video, high quality audio",
        "model": "fal-ai/stable-audio",
        "seconds_total": 180,
    },
    {
        "id": "music_02",
        "name": "cta_energy_build",
        "priority": "HIGH",
        "prompt": "High energy, motivational build-up music, cinematic, orchestral hybrid, inspiring, driving rhythm, building tension and release, suitable for call to action, high quality",
        "model": "fal-ai/stable-audio",
        "seconds_total": 60,
    },
    {
        "id": "music_03",
        "name": "screen_recording_bed",
        "priority": "MEDIUM",
        "prompt": "Subtle background music, sweet, calm, lo-fi beats, gentle, non-intrusive, suitable for concentration and screen recording demonstration, high quality",
        "model": "fal-ai/stable-audio",
        "seconds_total": 180,
    }
]


def generate_audio(asset_config: Dict, output_dir: Path) -> Dict:
    """Generate a single audio track using fal.ai"""
    print(f"\n{'='*60}")
    print(f"🎵 Generating: {asset_config['name']}")
    print(f"   Priority: {asset_config.get('priority', 'MEDIUM')}")
    print(f"   Model: {asset_config['model']}")
    print(f"   Duration: {asset_config['seconds_total']}s")
    print(f"{'='*60}")
    
    try:
        # Prepare arguments
        arguments = {
            "prompt": asset_config["prompt"],
            "seconds_total": asset_config["seconds_total"],
        }
        
        # Generate audio
        print("⏳ Sending request to fal.ai...")
        result = fal_client.subscribe(
            asset_config["model"],
            arguments=arguments,
        )
        
        # Download and save
        # Stable Audio usually returns 'audio_file' or similar dict
        # We need to inspect the result structure. 
        # Typically: {'audio_file': {'url': '...', 'content_type': 'audio/mpeg', ...}}
        
        audio_url = None
        if result and "audio_file" in result:
            audio_url = result["audio_file"]["url"]
        elif result and "url" in result:
             audio_url = result["url"]
        
        if audio_url:
            print(f"✅ Generated successfully!")
            print(f"   URL: {audio_url}")
            
            # Save metadata
            output_path = output_dir / f"{asset_config['name']}.json"
            metadata = {
                **asset_config,
                "result_url": audio_url,
            }
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Metadata saved: {output_path}")
            
            # Download audio
            import urllib.request
            # Determine extension
            ext = ".mp3" # Defaulting to mp3
            if "wav" in audio_url.lower():
                ext = ".wav"
                
            audio_path = output_dir / f"{asset_config['name']}{ext}"
            urllib.request.urlretrieve(audio_url, audio_path)
            print(f"💾 Audio saved: {audio_path}")
            
            return {
                "success": True,
                "url": audio_url,
                "local_path": str(audio_path),
            }
        else:
            print(f"❌ Generation failed: No audio URL in result")
            print(f"   Result: {result}")
            return {"success": False, "error": "No audio URL returned"}
            
    except Exception as e:
        print(f"❌ Error generating audio: {str(e)}")
        return {"success": False, "error": str(e)}

def process_queue(queue: List[Dict], output_dir: Path) -> List[Dict]:
    """Process a queue of music tracks to generate"""
    print(f"\n{'='*60}")
    print("🚀 FAL.AI BATCH ASSET GENERATOR - MUSIC")
    print("   Project: The Agentic Era - Managing 240+ Workflows")
    print("="*60)
    
    # Check API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("\n❌ ERROR: FAL_KEY environment variable not set")
        print("   Set it with: export FAL_KEY='your-api-key-here'")
        print("   Get your key from: https://fal.ai/dashboard/keys")
        return []
    
    print(f"\n✅ API Key found")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print(f"\n🎵 Tracks to generate: {len(queue)}")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not queue:
        print("\n⚠️  QUEUE IS EMPTY.")
        return []

    # Count by priority
    high_priority = [a for a in queue if a.get("priority") == "HIGH"]
    medium_priority = [a for a in queue if a.get("priority") == "MEDIUM"]
    
    print(f"   • HIGH priority: {len(high_priority)}")
    print(f"   • MEDIUM priority: {len(medium_priority)}")
    
    # Generate assets
    results = []
    for i, asset in enumerate(queue, 1):
        print(f"\n\n{'#'*60}")
        print(f"# Track {i}/{len(queue)}")
        print(f"{'#'*60}")
        
        result = generate_audio(asset, output_dir)
        results.append({
            "asset_id": asset.get("id", f"auto_{i}"),
            "name": asset["name"],
            "priority": asset.get("priority", "MEDIUM"),
            **result
        })
    
    # Summary
    print("\n\n" + "="*60)
    print("📊 GENERATION SUMMARY")
    print("="*60)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\n✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    if successful:
        print("\n✅ SUCCESSFUL GENERATIONS:")
        for r in successful:
            print(f"   • {r['asset_id']}: {r['name']} ({r['priority']})")
    
    if failed:
        print("\n❌ FAILED GENERATIONS:")
        for r in failed:
            print(f"   • {r['asset_id']}: {r['name']} - {r.get('error', 'Unknown error')}")
    
    # Save summary
    summary_path = output_dir / "generation_summary.json"
    with open(summary_path, 'w') as f:
        json.dump({
            "total": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "results": results,
        }, f, indent=2)
    
    print(f"\n💾 Summary saved: {summary_path}")
    print("\n✅ Done!")
    
    return results

def main():
    """Main execution"""
    # Confirm before proceeding
    print("\n" + "="*60)
    response = input("🤔 Proceed with generation? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled by user")
        return
        
    process_queue(GENERATION_QUEUE, OUTPUT_DIR)


if __name__ == "__main__":
    main()

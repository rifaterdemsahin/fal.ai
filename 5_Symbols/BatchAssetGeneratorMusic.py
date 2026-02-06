#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Music
Project: The Agentic Era - Managing 240+ Workflows
Generates background music tracks based on EDL suggestions
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional

# Install: pip install fal-client
try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

# Import asset utilities
try:
    from asset_utils import generate_filename, extract_scene_number, ManifestTracker
except ImportError:
    # Fallback if running standalone
    print("⚠️  asset_utils not found. Using legacy naming convention.")
    generate_filename = None
    extract_scene_number = None
    ManifestTracker = None

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
        "seconds_total": 47,
    },
    {
        "id": "music_02",
        "name": "cta_energy_build",
        "priority": "HIGH",
        "prompt": "High energy, motivational build-up music, cinematic, orchestral hybrid, inspiring, driving rhythm, building tension and release, suitable for call to action, high quality",
        "model": "fal-ai/stable-audio",
        "seconds_total": 47,
    },
    {
        "id": "music_03",
        "name": "screen_recording_bed",
        "priority": "MEDIUM",
        "prompt": "Subtle background music, sweet, calm, lo-fi beats, gentle, non-intrusive, suitable for concentration and screen recording demonstration, high quality",
        "model": "fal-ai/stable-audio",
        "seconds_total": 47,
    }
]


def generate_audio(asset_config: Dict, output_dir: Path, manifest: Optional[object] = None, version: int = 1) -> Dict:
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
            
            # Determine extension
            ext = ".mp3" # Defaulting to mp3
            if "wav" in audio_url.lower():
                ext = ".wav"
            
            # Generate filename using new convention if available
            if generate_filename and extract_scene_number:
                scene_num = extract_scene_number(asset_config.get('id', '0.0'))
                base_filename = generate_filename(
                    scene_num,
                    'music',
                    asset_config['name'],
                    version
                )
                filename_json = base_filename + '.json'
                filename_audio = base_filename + ext
            else:
                # Fallback to legacy naming
                filename_json = f"{asset_config['name']}.json"
                filename_audio = f"{asset_config['name']}{ext}"
            
            # Save metadata
            output_path = output_dir / filename_json
            metadata = {
                **asset_config,
                "result_url": audio_url,
                "filename": filename_audio,
            }
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Metadata saved: {output_path}")
            
            # Download audio
            import urllib.request
                
            audio_path = output_dir / filename_audio
            urllib.request.urlretrieve(audio_url, audio_path)
            print(f"💾 Audio saved: {audio_path}")
            
            # Add to manifest if provided
            if manifest:
                manifest.add_asset(
                    filename=filename_audio,
                    prompt=asset_config["prompt"],
                    asset_type="music",
                    asset_id=asset_config.get("id", "unknown"),
                    result_url=audio_url,
                    local_path=str(audio_path),
                    metadata={
                        "scene": asset_config.get("scene", ""),
                        "priority": asset_config.get("priority", ""),
                        "model": asset_config.get("model", ""),
                    }
                )
            
            return {
                "success": True,
                "url": audio_url,
                "local_path": str(audio_path),
                "filename": filename_audio,
            }
        else:
            print(f"❌ Generation failed: No audio URL in result")
            print(f"   Result: {result}")
            return {"success": False, "error": "No audio URL returned"}
            
    except Exception as e:
        print(f"❌ Error generating audio: {str(e)}")
        return {"success": False, "error": str(e)}

def process_queue(queue: List[Dict], output_dir: Path, manifest: Optional[object] = None) -> List[Dict]:
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
        
        result = generate_audio(asset, output_dir, manifest)
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

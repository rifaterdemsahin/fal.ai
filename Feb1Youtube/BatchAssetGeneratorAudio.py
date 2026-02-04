#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Audio/SFX
Project: The Agentic Era - Managing 240+ Workflows
Generates all required sound effects based on EDL concepts
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
OUTPUT_DIR = Path("./generated_audio")
OUTPUT_DIR.mkdir(exist_ok=True)

# Audio specific settings
DEFAULT_DURATION = 10  # seconds

# Asset generation queue
# Inferred sound effects based on the graphics concepts
GENERATION_QUEUE = [
    {
        "id": "1.1",
        "name": "ferrari_cart_morph_sfx",
        "priority": "HIGH",
        "scene": "Scene 1",
        "prompt": "Sound of a sleek sports car engine revving up then seamlessly transforming into a digital shopping cart sound, sci-fi transformation effect, high quality",
        "model": "fal-ai/stable-audio",
        "seconds_total": 10,
    },
    {
        "id": "4.1",
        "name": "uk_streets_ambience",
        "priority": "MEDIUM",
        "scene": "Scene 4",
        "prompt": "Cinematic ambient sound of an empty UK high street on a Sunday evening, light wind, distant quiet urban atmosphere, melancholic mood",
        "model": "fal-ai/stable-audio",
        "seconds_total": 15,
    },
    {
        "id": "4.2",
        "name": "timeline_clock_sfx",
        "priority": "HIGH",
        "scene": "Scene 4",
        "prompt": "Rhythmic ticking clock sound, clean digital blips for timeline markers, modern notification sound, high fidelity",
        "model": "fal-ai/stable-audio",
        "seconds_total": 8,
    },
    {
        "id": "4.3",
        "name": "agent_workflow_processing",
        "priority": "HIGH",
        "scene": "Scene 4",
        "prompt": "Futuristic data flow sound, soft beeps and processing noise, digital hum, high tech atmosphere",
        "model": "fal-ai/stable-audio",
        "seconds_total": 10,
    },
    {
        "id": "4.4",
        "name": "chatbot_vs_realtime_sfx",
        "priority": "HIGH",
        "scene": "Scene 4",
        "prompt": "Contrast between boring monotone mechanical typing sound and dynamic fast-paced digital alert sounds, vibrant and active",
        "model": "fal-ai/stable-audio",
        "seconds_total": 12,
    },
    {
        "id": "6.1",
        "name": "pricing_success_chime",
        "priority": "HIGH",
        "scene": "Scene 6",
        "prompt": "Cash register ching sound mixed with a digital success chime, satisfying coin drop, clean and crisp",
        "model": "fal-ai/stable-audio",
        "seconds_total": 5,
    },
    {
        "id": "7.1",
        "name": "methodology_flow_whoosh",
        "priority": "MEDIUM",
        "scene": "Scene 7",
        "prompt": "Clean futuristic whoosh sound for workflow transitions, followed by a positive checkmark ping, corporate tech style",
        "model": "fal-ai/stable-audio",
        "seconds_total": 6,
    },
    {
        "id": "8.1",
        "name": "data_transfer_sfx",
        "priority": "MEDIUM",
        "scene": "Scene 8",
        "prompt": "Digital data transfer sound, electronic switch click, routing sound effects, clean technology ambience",
        "model": "fal-ai/stable-audio",
        "seconds_total": 8,
    },
    {
        "id": "9.1",
        "name": "office_ambience",
        "priority": "LOW",
        "scene": "Scene 9",
        "prompt": "Muffled corporate office ambience, quiet murmurs, paper shuffling, distant phone ringing, realistic",
        "model": "fal-ai/stable-audio",
        "seconds_total": 15,
    },
    {
        "id": "9.2",
        "name": "agent_network_synths",
        "priority": "HIGH",
        "scene": "Scene 9",
        "prompt": "Isolated quiet blips transforming into a harmonious interconnected synth network melody, futuristic and uplifting",
        "model": "fal-ai/stable-audio",
        "seconds_total": 12,
    },
    {
        "id": "9.3",
        "name": "revolution_riser",
        "priority": "HIGH",
        "scene": "Scene 9",
        "prompt": "Uplifting synth riser, energetic whoosh, motivational background texture, impactful",
        "model": "fal-ai/stable-audio",
        "seconds_total": 8,
    },
    {
        "id": "10.1",
        "name": "notification_chaos_vs_zen",
        "priority": "MEDIUM",
        "scene": "Scene 10",
        "prompt": "Chaos of multiple annoying notification sounds transitioning into a peaceful silence with a single gentle zen chime",
        "model": "fal-ai/stable-audio",
        "seconds_total": 12,
    },
    {
        "id": "11.1",
        "name": "cinematic_impact_boom",
        "priority": "HIGH",
        "scene": "Scene 11",
        "prompt": "Dramatic cinematic impact boom, inspirational background drone, deep bass rumble, movie trailer style",
        "model": "fal-ai/stable-audio",
        "seconds_total": 8,
    },
]


def generate_asset(asset_config: Dict) -> Dict:
    """Generate a single audio asset using fal.ai"""
    print(f"\n{'='*60}")
    print(f"🎵 Generating: {asset_config['name']}")
    print(f"   Scene: {asset_config.get('scene', 'Unknown')}")
    print(f"   Priority: {asset_config.get('priority', 'MEDIUM')}")
    print(f"{'='*60}")
    
    try:
        # Prepare arguments
        arguments = {
            "prompt": asset_config["prompt"],
            "seconds_total": asset_config.get("seconds_total", DEFAULT_DURATION),
        }
        
        # Generate audio
        print("⏳ Sending request to fal.ai...")
        result = fal_client.subscribe(
            asset_config["model"],
            arguments=arguments,
        )
        
        # Download and save
        # Note: Structure of response might vary, but typically contains 'audio_file' or similar
        # For stable-audio, it usually returns 'audio_file' : {'url': ...}
        
        audio_url = None
        if result:
            if "audio_file" in result and "url" in result["audio_file"]:
                audio_url = result["audio_file"]["url"]
            elif "audio_url" in result: # Fallback check
                audio_url = result["audio_url"]
            # Check for other potential keys if the API changes
            
        if audio_url:
            print(f"✅ Generated successfully!")
            print(f"   URL: {audio_url}")
            
            # Save metadata
            output_path = OUTPUT_DIR / f"{asset_config['name']}.json"
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
            ext = ".mp3" # Default to mp3 if unbeknownst
            if audio_url.endswith(".wav"):
                ext = ".wav"
            elif audio_url.endswith(".mp3"):
                ext = ".mp3"
            
            audio_path = OUTPUT_DIR / f"{asset_config['name']}{ext}"
            urllib.request.urlretrieve(audio_url, audio_path)
            print(f"💾 Audio saved: {audio_path}")
            
            return {
                "success": True,
                "url": audio_url,
                "local_path": str(audio_path),
            }
        else:
            print(f"❌ Generation failed: No audio URL in result")
            print(f"Result dump: {json.dumps(result, indent=2)}")
            return {"success": False, "error": "No audio URL returned"}
            
    except Exception as e:
        print(f"❌ Error generating asset: {str(e)}")
        return {"success": False, "error": str(e)}


def main():
    """Main execution"""
    print("\n" + "="*60)
    print("🔊 FAL.AI BATCH ASSET GENERATOR - AUDIO/SFX")
    print("   Project: The Agentic Era - Managing 240+ Workflows")
    print("="*60)
    
    # Check API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("\n❌ ERROR: FAL_KEY environment variable not set")
        print("   Set it with: export FAL_KEY='your-api-key-here'")
        print("   Get your key from: https://fal.ai/dashboard/keys")
        return
    
    print(f"\n✅ API Key found")
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}")
    print(f"\n📊 Assets to generate: {len(GENERATION_QUEUE)}")
    
    if not GENERATION_QUEUE:
        print("\n⚠️  QUEUE IS EMPTY.")
        return

    # Count by priority
    high_priority = [a for a in GENERATION_QUEUE if a.get("priority") == "HIGH"]
    medium_priority = [a for a in GENERATION_QUEUE if a.get("priority") == "MEDIUM"]
    
    print(f"   • HIGH priority: {len(high_priority)}")
    print(f"   • MEDIUM priority: {len(medium_priority)}")
    
    # Confirm before proceeding
    print("\n" + "="*60)
    response = input("🤔 Proceed with generation? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled by user")
        return
    
    # Generate assets
    results = []
    for i, asset in enumerate(GENERATION_QUEUE, 1):
        print(f"\n\n{'#'*60}")
        print(f"# Asset {i}/{len(GENERATION_QUEUE)}")
        print(f"{'#'*60}")
        
        result = generate_asset(asset)
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
    summary_path = OUTPUT_DIR / "generation_summary.json"
    with open(summary_path, 'w') as f:
        json.dump({
            "total": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "results": results,
        }, f, indent=2)
    
    print(f"\n💾 Summary saved: {summary_path}")
    print("\n✅ Done!")


if __name__ == "__main__":
    main()

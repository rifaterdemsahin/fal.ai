#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Video
Project: The Agentic Era - Managing 240+ Workflows
Generates B-roll video clips using fal.ai video models
"""

import os
import json
from pathlib import Path
from typing import Dict, List
import time

# Install: pip install fal-client
try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

# Configuration
OUTPUT_DIR = Path("./generated_video")
OUTPUT_DIR.mkdir(exist_ok=True)

# Video Generation Queue
# Based on EDL B-roll requirements of "Empty UK Streets", "Corporate Meeting"
GENERATION_QUEUE = [
    {
        "id": "4.1",
        "name": "uk_streets_sunday",
        "priority": "MEDIUM",
        "scene": "Scene 4: Skills Gap",
        "prompt": (
            "Cinematic shot of empty UK high street on Sunday evening, closed shop fronts with metal shutters down, "
            "dim streetlights beginning to illuminate, deserted pedestrian area, typical British town center architecture, "
            "moody atmospheric lighting, golden hour or early dusk, realistic urban photography style, "
            "slight film grain, 16:9 cinematic aspect ratio, melancholic mood, 4k, high resolution"
        ),
        "model": "fal-ai/minimax/video-01",
        "duration_seconds": 5,
        "aspect_ratio": "16:9"
    },
    {
        "id": "9.1",
        "name": "corporate_meeting",
        "priority": "LOW",
        "scene": "Scene 9: AI Transformation",
        "prompt": (
            "Cinematic shot of modern corporate meeting room, 4-5 business professionals sitting around conference table "
            "looking at laptops with frustrated expressions, large monitor on wall displaying generic charts, "
            "glass walls visible, fluorescent office lighting, professional business environment, "
            "realistic corporate photography style, slightly desaturated colors for serious tone, "
            "slow camera movement, 4k"
        ),
        "model": "fal-ai/minimax/video-01",
        "duration_seconds": 5,
        "aspect_ratio": "16:9"
    },
     {
        "id": "1.1",
        "name": "ferrari_cart_morph",
        "priority": "HIGH",
        "scene": "Scene 1: Hook",
        "prompt": (
            "Sleek red Ferrari sports car icon smoothly morphing into simple shopping cart icon, "
            "clean vector style, white/transparent background, particle effects during transformation, "
            "professional tech presentation aesthetic, minimalist flat design, modern motion graphics style"
        ),
        "model": "fal-ai/minimax/video-01",
        "duration_seconds": 5,
        "aspect_ratio": "16:9"
    }
]


def generate_video(asset_config: Dict, output_dir: Path) -> Dict:
    """Generate a single video clip using fal.ai"""
    print(f"\n{'='*60}")
    print(f"🎬 Generating: {asset_config['name']}")
    print(f"   Scene: {asset_config['scene']}")
    print(f"   Priority: {asset_config.get('priority', 'MEDIUM')}")
    print(f"   Model: {asset_config['model']}")
    print(f"{'='*60}")
    
    try:
        # Prepare arguments based on model
        arguments = {
            "prompt": asset_config["prompt"],
        }
        
        # Add model specific parameters if needed
        if "minimax" in asset_config["model"]:
             # Minimax usually just takes prompt, sometimes duration_seconds (mostly fixed to 5s in v1)
             pass
        elif "kling" in asset_config["model"]:
            arguments["aspect_ratio"] = asset_config.get("aspect_ratio", "16:9")
            arguments["duration"] = str(asset_config.get("duration_seconds", 5)) + "s"

        
        # Generate video
        print("⏳ Sending request to fal.ai (this may take 2-3 minutes)...")
        result = fal_client.subscribe(
            asset_config["model"],
            arguments=arguments,
        )
        
        # Download and save
        # Minimax/Video returns 'video' object usually: {'video': {'url': '...', ...}}
        video_url = None
        
        if result:
            if "video" in result and "url" in result["video"]:
                video_url = result["video"]["url"]
            elif "video_url" in result: # Some models return direct url key
                 video_url = result["video_url"]
            elif "videos" in result and len(result["videos"]) > 0:
                 video_url = result["videos"][0]["url"]
        
        if video_url:
            print(f"✅ Generated successfully!")
            print(f"   URL: {video_url}")
            
            # Save metadata
            output_path = output_dir / f"{asset_config['name']}.json"
            metadata = {
                **asset_config,
                "result_url": video_url,
                "generated_at": time.time()
            }
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Metadata saved: {output_path}")
            
            # Download video
            import urllib.request
            
            # Extension is likely mp4
            ext = ".mp4"
                
            video_path = output_dir / f"{asset_config['name']}{ext}"
            urllib.request.urlretrieve(video_url, video_path)
            print(f"💾 Video saved: {video_path}")
            
            return {
                "success": True,
                "url": video_url,
                "local_path": str(video_path),
            }
        else:
            print(f"❌ Generation failed: No video URL in result")
            print(f"   Result keys: {result.keys() if result else 'None'}")
            return {"success": False, "error": "No video URL returned"}
            
    except Exception as e:
        print(f"❌ Error generating video: {str(e)}")
        return {"success": False, "error": str(e)}

def process_queue(queue: List[Dict], output_dir: Path) -> List[Dict]:
    """Process a queue of video clips to generate"""
    print(f"\n{'='*60}")
    print("🚀 FAL.AI BATCH ASSET GENERATOR - VIDEO")
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
    print(f"\n🎬 Clips to generate: {len(queue)}")
    
    if not queue:
        print("\n⚠️  QUEUE IS EMPTY.")
        return []

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Count by priority
    high_priority = [a for a in queue if a.get("priority") == "HIGH"]
    medium_priority = [a for a in queue if a.get("priority") == "MEDIUM"]
    low_priority = [a for a in queue if a.get("priority") == "LOW"]
    
    print(f"   • HIGH priority: {len(high_priority)}")
    print(f"   • MEDIUM priority: {len(medium_priority)}")
    print(f"   • LOW priority: {len(low_priority)}")
    
    # Generate assets
    results = []
    for i, asset in enumerate(queue, 1):
        print(f"\n\n{'#'*60}")
        print(f"# Clip {i}/{len(queue)}")
        print(f"{'#'*60}")
        
        result = generate_video(asset, output_dir)
        results.append({
            "asset_id": asset.get("id", f"auto_{i}"),
            "name": asset["name"],
            "priority": asset.get("priority", "MEDIUM"),
            **result
        })
        
        # Add a small delay between requests to be nice to the API
        if i < len(queue):
            print("⏳ Cooling down for 5 seconds...")
            time.sleep(5)
    
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

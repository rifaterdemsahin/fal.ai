#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Video
Project: The Agentic Era - Managing 240+ Workflows
Generates B-roll video clips using fal.ai video models
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import time

# Install: pip install fal-client
try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

# Import asset utilities
try:
    from Utils.asset_utils import generate_filename, extract_scene_number, ManifestTracker
except ImportError:
    # Fallback if running standalone
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    try:
        from Utils.asset_utils import generate_filename, extract_scene_number, ManifestTracker
    except ImportError:
        print("⚠️  asset_utils not found. Using legacy naming convention.")
        generate_filename = None
        extract_scene_number = None
        ManifestTracker = None

# Configuration
# Configuration
DEFAULT_OUTPUT_DIR = Path("./generated_video")
# OUTPUT_DIR.mkdir(exist_ok=True) # Moved to execution time

# Video Generation Queue
# Based on EDL B-roll requirements of "Empty UK Streets", "Corporate Meeting"
# Loaded from external YAML configuration
DATA_PATH = Path(r"C:\projects\fal.ai\3_Simulation\Feb1Youtube\_source\batch_generation_data.yaml")

def load_queue():
    """Load generation queue from YAML"""
    if not DATA_PATH.exists():
        print(f"⚠️  Configuration file not found: {DATA_PATH}")
        return []
    
    try:
        import yaml
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get("video", [])
    except ImportError:
        print("❌ PyYAML not installed. Run: pip install PyYAML")
        return []
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return []

GENERATION_QUEUE = load_queue()


def generate_video(asset_config: Dict, output_dir: Path, manifest: Optional[object] = None, version: int = 1) -> Dict:
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
            arguments["duration"] = str(asset_config.get("duration_seconds", 5))

        
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
            
            # Generate filename using new convention if available
            if generate_filename and extract_scene_number:
                scene_num = extract_scene_number(asset_config.get('id', '0.0'))
                base_filename = generate_filename(
                    scene_num,
                    'video',
                    asset_config['name'],
                    version
                )
                filename_json = base_filename + '.json'
                filename_mp4 = base_filename + '.mp4'
            else:
                # Fallback to legacy naming
                filename_json = f"{asset_config['name']}.json"
                filename_mp4 = f"{asset_config['name']}.mp4"
            
            # Save metadata
            output_path = output_dir / filename_json
            metadata = {
                **asset_config,
                "result_url": video_url,
                "generated_at": time.time(),
                "filename": filename_mp4,
            }
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Metadata saved: {output_path}")
            
            # Download video
            import urllib.request
            
            # Extension is likely mp4
            video_path = output_dir / filename_mp4
            urllib.request.urlretrieve(video_url, video_path)
            print(f"💾 Video saved: {video_path}")
            
            # Add to manifest if provided
            if manifest:
                manifest.add_asset(
                    filename=filename_mp4,
                    prompt=asset_config["prompt"],
                    asset_type="video",
                    asset_id=asset_config.get("id", "unknown"),
                    result_url=video_url,
                    local_path=str(video_path),
                    metadata={
                        "scene": asset_config.get("scene", ""),
                        "priority": asset_config.get("priority", ""),
                        "model": asset_config.get("model", ""),
                    }
                )
            
            return {
                "success": True,
                "url": video_url,
                "local_path": str(video_path),
                "filename": filename_mp4,
            }
        else:
            print(f"❌ Generation failed: No video URL in result")
            print(f"   Result keys: {result.keys() if result else 'None'}")
            return {"success": False, "error": "No video URL returned"}
            
    except Exception as e:
        print(f"❌ Error generating video: {str(e)}")
        return {"success": False, "error": str(e)}

def process_queue(queue: List[Dict], output_dir: Path, manifest: Optional[object] = None) -> List[Dict]:
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
        
        result = generate_video(asset, output_dir, manifest)
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
        
    process_queue(GENERATION_QUEUE, DEFAULT_OUTPUT_DIR)


if __name__ == "__main__":
    main()

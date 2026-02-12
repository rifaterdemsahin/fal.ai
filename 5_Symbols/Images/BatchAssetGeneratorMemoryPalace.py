#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Memory Palace
Project: The Agentic Era
Generates memory palace imagery for the video.
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

# Import cost check function
try:
    from base.generator_config import check_generation_cost
except ImportError:
    # Fallback if running standalone
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from base.generator_config import check_generation_cost

# Configuration
OUTPUT_DIR = Path("./generated_memory_palace")
OUTPUT_DIR.mkdir(exist_ok=True)

# Consistency seeds
SEEDS = {
    "SEED_001": 555123,  # Ancient/Architectural
    "SEED_002": 555456,  # Surreal/Dreamlike
}

# Default Queue (Example/Template)
GENERATION_QUEUE = [
    {
        "id": "MP.1",
        "name": "memory_palace_entrance",
        "priority": "HIGH",
        "scene": "Intro",
        "seed_key": "SEED_001",
        "prompt": "Grand entrance to a memory palace, classical greek architecture, marble columns, golden light, floating geometric symbols, ethereal atmosphere, cinematic lighting, 8k resolution, wide angle",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "MP.2",
        "name": "locus_hall_of_mirrors",
        "priority": "MEDIUM",
        "scene": "Hallway",
        "seed_key": "SEED_002",
        "prompt": "A long hallway lined with mirrors, each mirror reflecting a different memory or data point, surreal style, infinite depth, glowing blue pathways on the floor, cybernetic architecture mixed with baroque style",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    }
]

def generate_asset(asset_config: Dict, output_dir: Path, manifest: Optional[object] = None, version: int = 1) -> Dict:
    """Generate a single asset using fal.ai"""
    print(f"\n{'='*60}")
    print(f"🧠 Generating Memory Palace Asset: {asset_config['name']}")
    print(f"   Scene: {asset_config.get('scene', 'Unknown')}")
    print(f"   Priority: {asset_config.get('priority', 'MEDIUM')}")
    print(f"   Seed: {asset_config['seed_key']} ({SEEDS.get(asset_config['seed_key'], 'N/A')})")
    print(f"{'='*60}")
    
    try:
        # Check cost before generating (for generations > $0.20)
        if not check_generation_cost(asset_config["model"]):
            return {
                "success": False,
                "error": "Cancelled by user due to cost",
            }
        
        # Prepare arguments
        seed_value = SEEDS.get(asset_config["seed_key"], 0)
        arguments = {
            "prompt": asset_config["prompt"],
            "image_size": asset_config["image_size"],
            "num_inference_steps": asset_config["num_inference_steps"],
            "seed": seed_value,
            "num_images": 1,
        }
        
        # Generate image
        print("⏳ Sending request to fal.ai...")
        result = fal_client.subscribe(
            asset_config["model"],
            arguments=arguments,
        )
        
        # Download and save
        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            print(f"✅ Generated successfully!")
            print(f"   URL: {image_url}")
            
            # Generate filename using new convention if available
            if generate_filename and extract_scene_number:
                scene_num = extract_scene_number(asset_config.get('id', '0.0'))
                base_filename = generate_filename(
                    scene_num,
                    'memorypalace',
                    asset_config['name'],
                    version
                )
                filename_json = base_filename + '.json'
                filename_png = base_filename + '.png'
            else:
                # Fallback to legacy naming
                filename_json = f"{asset_config['name']}.json"
                filename_png = f"{asset_config['name']}.png"
            
            # Save metadata
            output_path = output_dir / filename_json
            metadata = {
                **asset_config,
                "result_url": image_url,
                "seed_value": seed_value,
                "filename": filename_png,
            }
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Metadata saved: {output_path}")
            
            # Download image
            import urllib.request
            image_path = output_dir / filename_png
            urllib.request.urlretrieve(image_url, image_path)
            print(f"💾 Image saved: {image_path}")
            
            # Add to manifest if provided
            if manifest:
                manifest.add_asset(
                    filename=filename_png,
                    prompt=asset_config["prompt"],
                    asset_type="memorypalace",
                    asset_id=asset_config.get("id", "unknown"),
                    result_url=image_url,
                    local_path=str(image_path),
                    metadata={
                        "scene": asset_config.get("scene", ""),
                        "priority": asset_config.get("priority", ""),
                        "model": asset_config.get("model", ""),
                    }
                )
            
            return {
                "success": True,
                "url": image_url,
                "local_path": str(image_path),
                "filename": filename_png,
            }
        else:
            print(f"❌ Generation failed: No images in result")
            return {"success": False, "error": "No images returned"}
            
    except Exception as e:
        print(f"❌ Error generating asset: {str(e)}")
        return {"success": False, "error": str(e)}

def process_queue(queue: List[Dict], output_dir: Path, manifest: Optional[object] = None) -> List[Dict]:
    """Process a queue of memory palace assets to generate"""
    print(f"\n{'='*60}")
    print("🚀 FAL.AI BATCH ASSET GENERATOR - MEMORY PALACE")
    print("   Project: The Agentic Era")
    print("="*60)
    
    # Check API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("\n❌ ERROR: FAL_KEY environment variable not set")
        print("   Set it with: export FAL_KEY='your-api-key-here'")
        return []
    
    print(f"\n✅ API Key found")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print(f"\n📊 Assets to generate: {len(queue)}")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    if not queue:
        print("\n⚠️  QUEUE IS EMPTY. Needs configuration.")
        return []

    # Count by priority
    high_priority = [a for a in queue if a.get("priority") == "HIGH"]
    
    print(f"   • HIGH priority: {len(high_priority)}")
    
    # Generate assets
    results = []
    for i, asset in enumerate(queue, 1):
        print(f"\n\n{'#'*60}")
        print(f"# Asset {i}/{len(queue)}")
        print(f"{'#'*60}")
        
        result = generate_asset(asset, output_dir, manifest)
        results.append({
            "asset_id": asset.get("id", f"mp_{i}"),
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
    
    if failed:
        print(f"❌ Failed: {len(failed)}/{len(results)}")
        for r in failed:
            print(f"   • {r['name']} - {r.get('error')}")
    
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
    print("\n" + "="*60)
    response = input("🤔 Proceed with Memory Palace generation? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled by user")
        return
        
    process_queue(GENERATION_QUEUE, OUTPUT_DIR)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator for Chapter Markers
Project: The Agentic Era - Managing 240+ Workflows
Generates title cards/images for video chapters based on external YAML configuration
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

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
OUTPUT_DIR = Path("./generated_chapter_markers")
OUTPUT_DIR.mkdir(exist_ok=True)

# Consistency seeds
SEEDS = {
    "SEED_CHAPTERS": 999001,  # Consistent style for all chapters
}

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
            return data.get("chapters", [])
    except ImportError:
        print("❌ PyYAML not installed. Run: pip install PyYAML")
        return []
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return []

GENERATION_QUEUE = load_queue()

def generate_asset(asset_config: Dict, output_dir: Path, manifest: Optional[object] = None, version: int = 1) -> Dict:
    """Generate a single asset using fal.ai"""
    print(f"\n{'='*60}")
    print(f"🎨 Generating: {asset_config['name']}")
    print(f"   Chapter: {asset_config['scene']}")
    print(f"   Seed: {asset_config['seed_key']} ({SEEDS.get(asset_config['seed_key'], 'Unknown')})")
    print(f"{'='*60}")
    
    try:
        # Prepare arguments
        arguments = {
            "prompt": asset_config["prompt"],
            "image_size": asset_config["image_size"],
            "num_inference_steps": asset_config["num_inference_steps"],
            "seed": SEEDS.get(asset_config["seed_key"]),
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
                # Attempt to extract a number if possible, or use a default
                try:
                     scene_num = extract_scene_number(asset_config.get('id', '0.0'))
                except:
                     scene_num = 0
                
                # Use name from config which already includes var2 suffix if applicable
                base_name = asset_config['name']
                
                base_filename = generate_filename(
                    scene_num,
                    'chaptermarker',
                    base_name,
                    version
                )
                filename_json = base_filename + '.json'
                filename_png = base_filename + '.png'
                filename_jpg = base_filename + '.jpg'
            else:
                # Fallback to legacy naming
                filename_json = f"{asset_config['name']}.json"
                filename_png = f"{asset_config['name']}.png"
                filename_jpg = f"{asset_config['name']}.jpg"
            
            # Save metadata
            output_path = output_dir / filename_json
            metadata = {
                **asset_config,
                "result_url": image_url,
                "seed_value": SEEDS.get(asset_config["seed_key"]),
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

            # Convert to JPG because DaVinci Resolve sometimes prefers it or user requested it
            # Also user specifically asked for _v1.jpg for the variation
            try:
                from PIL import Image
                with Image.open(image_path) as img:
                    rgb_im = img.convert('RGB')
                    jpg_path = output_dir / filename_jpg
                    rgb_im.save(jpg_path, quality=95)
                    print(f"💾 JPG converted: {jpg_path}")
            except ImportError:
                 print("⚠️ PIL not installed. Skipping JPG conversion.")
            except Exception as e:
                 print(f"⚠️ Error converting to JPG: {e}")

            
            # Add to manifest if provided
            if manifest:
                manifest.add_asset(
                    filename=filename_png,
                    prompt=asset_config["prompt"],
                    asset_type="chaptermarker",
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

def process_queue(generation_queue: List[Dict], output_dir: Path, manifest: Optional[object] = None) -> List[Dict]:
    """Process the queue"""
    print(f"\n{'='*60}")
    print("🚀 FAL.AI BATCH CHAPTER MARKER GENERATOR")
    print("   Project: The Agentic Era - Chapter Assets")
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
    print(f"\n📊 Assets to generate: {len(generation_queue)}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not generation_queue:
        print("\n⚠️  QUEUE IS EMPTY. Check the YAML configuration.")
        return []

    results = []
    for i, asset in enumerate(generation_queue, 1):
        print(f"\n\n{'#'*60}")
        print(f"# Asset {i}/{len(generation_queue)}")
        print(f"{'#'*60}")
        
        result = generate_asset(asset, output_dir, manifest)
        results.append({
            "asset_id": asset["id"],
            "name": asset["name"],
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
            print(f"   • {r['asset_id']}: {r['name']}")
    
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
    
    # Use global GENERATION_QUEUE loaded from YAML
    generation_queue = GENERATION_QUEUE
    
    if not generation_queue:
        print("❌ No chapters found in YAML or YAML failed to load.")
        return

    # Confirm before proceeding
    print("\n" + "="*60)
    print(f"📊 Assets to generate: {len(generation_queue)}")
    for item in generation_queue:
        print(f"   • {item.get('timestamp', '??:??')} - {item.get('name', 'Unknown')}")

    response = input("🤔 Proceed with generation? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled by user")
        return
        
    process_queue(generation_queue, OUTPUT_DIR)


if __name__ == "__main__":
    main()

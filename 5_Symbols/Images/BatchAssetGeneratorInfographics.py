#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Infographics
Project: The Agentic Era - Managing 240+ Workflows
Generates data visualization and infographic assets
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
    from Utils.prompt_enhancer import enhance_prompt
except ImportError:
    # Fallback if running standalone
    import sys
    from pathlib import Path
    # Add parent directory (5_Symbols) to path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    
    try:
        from Utils.asset_utils import generate_filename, extract_scene_number, ManifestTracker
    except ImportError:
        print("⚠️  asset_utils not found. Using legacy naming convention.")
        generate_filename = None
        extract_scene_number = None
        ManifestTracker = None

    try:
        from Utils.prompt_enhancer import enhance_prompt
    except ImportError:
        print("⚠️  prompt_enhancer not found. Skipping prompt enhancement.")
        enhance_prompt = None

# Import cost check function
try:
    from base.generator_config import check_generation_cost
except ImportError:
    # Fallback if running standalone
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from base.generator_config import check_generation_cost

# Configuration
# Configuration
DEFAULT_OUTPUT_DIR = Path("./generated_infographics")
# OUTPUT_DIR.mkdir(parents=True, exist_ok=True) # Moved to execution time

# Consistency seeds
SEEDS = {
    "SEED_001": 42,      # B-roll
    "SEED_002": 123456,  # Infographics (MUST match for consistency)
    "SEED_003": 789012,  # Motion graphics
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
            return data.get("infographics", [])
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
    print(f"📊 Generating: {asset_config['name']}")
    print(f"   Scene: {asset_config.get('scene', 'Unknown')}")
    print(f"   Priority: {asset_config.get('priority', 'MEDIUM')}")
    print(f"   Seed: {asset_config['seed_key']} ({SEEDS.get(asset_config['seed_key'], 0)})")
    print(f"{'='*60}")
    
    try:
        # Check cost before generating (for generations > $0.20)
        if not check_generation_cost(asset_config["model"]):
            return {
                "success": False,
                "error": "Cancelled by user due to cost",
            }
        
        # Enhance prompt
        original_prompt = asset_config["prompt"]
        if enhance_prompt and (os.environ.get("GEMINIKEY") or os.environ.get("GEMINI_API_KEY")):
             print(f"✨ Enhancing prompt with Gemini...")
             # Create a log file for prompt enhancements in the output directory
             log_path = output_dir / "prompt_enhancements_log.txt"
             # Use 'infographic' as asset_type since this is the infographics generator
             enhanced_prompt = enhance_prompt(original_prompt, asset_type="diagram", log_path=str(log_path)) # Using diagram context for infographics as it fits best
             if enhanced_prompt and enhanced_prompt != original_prompt:
                 asset_config["prompt"] = enhanced_prompt
                 print(f"   Original: {original_prompt[:60]}...")
                 print(f"   Enhanced: {enhanced_prompt[:60]}...")
        
        # Prepare arguments
        # Prepare arguments
        arguments = {
            "prompt": asset_config["prompt"],
            "image_size": asset_config["image_size"],
            "seed": SEEDS.get(asset_config["seed_key"], 0),
            "num_images": 1,
        }
        
        # Add steps if provided (optional for some models)
        if "num_inference_steps" in asset_config:
            arguments["num_inference_steps"] = asset_config["num_inference_steps"]
        
        # Generate image
        print("⏳ Sending request to fal.ai...")
        result = fal_client.subscribe(
            asset_config["model"],
            arguments=arguments,
        )
        
        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            print(f"✅ Generated successfully!")
            print(f"   URL: {image_url}")
            
            # Upscaling with AuraSR for V3 (Sharpness)
            print("✨ Upscaling with AuraSR for maximum sharpness...")
            try:
                # Check cost before upscaling (for generations > $0.20)
                if not check_generation_cost("fal-ai/aura-sr"):
                    print("⚠️ Upscaling cancelled by user, using original.")
                else:
                    upscale_arguments = {
                        "image_url": image_url
                    }
                    upscale_result = fal_client.subscribe(
                        "fal-ai/aura-sr",
                        arguments=upscale_arguments,
                    )
                    if upscale_result and "images" in upscale_result and len(upscale_result["images"]) > 0:
                        image_url = upscale_result["images"][0]["url"]
                        print(f"✅ Upscaled successfully!")
                        print(f"   Upscaled URL: {image_url}")
                    else:
                        print("⚠️ Upscaling returned no images, using original.")
            except Exception as e:
                 print(f"⚠️ Upscaling failed: {e}, using original.")

            # Download and save
            # Generate filename
            if generate_filename and extract_scene_number:
                # Attempt to extract a number if possible, or use a default
                try:
                     scene_num = extract_scene_number(asset_config.get('id', '0.0'))
                except:
                     scene_num = 0
                
                base_filename = generate_filename(
                    scene_num,
                    'infographic',
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
                "seed_value": SEEDS.get(asset_config["seed_key"], 0),
                "filename": filename_png,
                "upscaled": True,
                "upscale_model": "fal-ai/aura-sr"
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
                    asset_type="infographic",
                    asset_id=asset_config.get("id", "unknown"),
                    result_url=image_url,
                    local_path=str(image_path),
                    metadata={
                        "scene": asset_config.get("scene", ""),
                        "priority": asset_config.get("priority", ""),
                        "model": asset_config.get("model", ""),
                        "upscaled": True
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
    """Process a queue of assets to generate"""
    print(f"\n{'='*60}")
    print("🚀 FAL.AI BATCH ASSET GENERATOR - INFOGRAPHICS")
    print("   Project: The Agentic Era - Managing 240+ Workflows")
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
        print("\n⚠️  QUEUE IS EMPTY. Check configuration.")
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
        print(f"# Asset {i}/{len(queue)}")
        print(f"{'#'*60}")
        
        result = generate_asset(asset, output_dir, manifest, version=3)
        results.append({
            "asset_id": asset["id"],
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
    # response = input("🤔 Proceed with generation? (yes/no): ").strip().lower()
    # if response not in ['yes', 'y']:
    #     print("❌ Cancelled by user")
    #     return
    
    # Auto-proceed for now as we want to run it via agent
    print("🚀 Auto-starting generation...")
        
    process_queue(GENERATION_QUEUE, DEFAULT_OUTPUT_DIR)


if __name__ == "__main__":
    main()

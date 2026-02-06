#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Diagrams
Project: The Agentic Era - Managing 240+ Workflows
Generates technical diagrams, flowcharts, and architecture visualizations
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

# Configuration
OUTPUT_DIR = Path(r"C:\projects\fal.ai\3_Simulation\Feb1Youtube\generated_diagrams")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Consistency seeds for different diagram styles
SEEDS = {
    "SEED_001": 555123,  # Technical Architecture
    "SEED_002": 555456,  # Process Flows
    "SEED_003": 555789,  # Concept Maps
    "SEED_004": 555000,  # Data Visualization
}

# Brand color palette (reference for prompts)
BRAND_COLORS = {
    "primary_dark": "#1a1a2e",
    "accent_blue": "#00d4ff",
    "accent_purple": "#7b2cbf",
    "secondary_teal": "#00bfa5",
    "highlight_orange": "#ff6b35",
    "text_white": "#ffffff",
}

# Asset generation queue
# Populated based on concepts from EDL - Diagrams specific
# Asset generation queue
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
            return data.get("diagrams", [])
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
    print(f"📊 Generating Diagram: {asset_config['name']}")
    print(f"   Scene: {asset_config.get('scene', 'Unknown')}")
    print(f"   Priority: {asset_config.get('priority', 'MEDIUM')}")
    print(f"   Seed: {asset_config['seed_key']} ({SEEDS[asset_config['seed_key']]})")
    print(f"{'='*60}")
    
    try:
        # Prepare arguments
        arguments = {
            "prompt": asset_config["prompt"],
            "image_size": asset_config["image_size"],
            "num_inference_steps": asset_config["num_inference_steps"],
            "seed": SEEDS[asset_config["seed_key"]],
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
                    'diagram',
                    asset_config['name'],
                    version
                )
                filename_json = base_filename + '.json'
                filename_png = base_filename + '.png'
                filename_mmd = base_filename + '.mmd'
            else:
                # Fallback to legacy naming
                filename_json = f"{asset_config['name']}.json"
                filename_png = f"{asset_config['name']}.png"
                filename_mmd = f"{asset_config['name']}.mmd"

            # Save Mermaid
            if "mermaid_content" in asset_config:
                mmd_path = output_dir / filename_mmd
                with open(mmd_path, 'w', encoding='utf-8') as f:
                    f.write(asset_config["mermaid_content"])
                print(f"💾 Mermaid saved: {mmd_path}")
            
            # Save metadata
            output_path = output_dir / filename_json
            metadata = {
                **asset_config,
                "result_url": image_url,
                "seed_value": SEEDS[asset_config["seed_key"]],
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

            # Create JPEG version
            try:
                from PIL import Image
                with Image.open(image_path) as img:
                    rgb_im = img.convert('RGB')
                    filename_jpg = image_path.stem + ".jpg"
                    jpg_path = output_dir / filename_jpg
                    rgb_im.save(jpg_path, 'JPEG', quality=95)
                    print(f"💾 JPEG saved: {jpg_path}")
            except ImportError:
                 print("⚠️ PIL not installed, skipping JPEG conversion")
            except Exception as e:
                 print(f"⚠️ Failed to convert to JPEG: {e}")
            
            # Add to manifest if provided
            if manifest:
                manifest.add_asset(
                    filename=filename_png,
                    prompt=asset_config["prompt"],
                    asset_type="diagram",
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
    """Process a queue of diagrams to generate"""
    print(f"\n{'='*60}")
    print("🚀 FAL.AI BATCH ASSET GENERATOR - DIAGRAMS")
    print("   Project: The Agentic Era - Managing 240+ Workflows")
    print("="*60)
    
    # Load environment variables
    env_path = Path(r"C:\projects\fal.ai\5_Symbols\.env")
    if env_path.exists():
        print(f"Loading environment from {env_path}")
        with open(env_path, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    try:
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value.strip('"').strip("'")
                    except ValueError:
                        pass

    # Check API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("\n❌ ERROR: FAL_KEY environment variable not set")
        print("   Set it with: export FAL_KEY='your-api-key-here'")
        print("   Get your key from: https://fal.ai/dashboard/keys")
        return []
    
    print(f"\n✅ API Key found")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print(f"\n📊 Assets to generate: {len(queue)}")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    if not queue:
        print("\n⚠️  QUEUE IS EMPTY. Please populate GENERATION_QUEUE with concepts from EDL.")
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
        
        result = generate_asset(asset, output_dir, manifest)
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
    # Auto-proceed without prompt for automation
    print("\n" + "="*60)
    print("🚀 Auto-starting generation...")
        
    process_queue(GENERATION_QUEUE, OUTPUT_DIR)


if __name__ == "__main__":
    main()

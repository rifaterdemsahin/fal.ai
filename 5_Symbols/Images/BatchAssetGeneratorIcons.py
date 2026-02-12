#!/usr/bin/env python3
"""
fal.ai Batch Icon Generator
Project: The Agentic Era - Managing 240+ Workflows
Generates all required icon assets with consistency controls
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
# Configuration
DEFAULT_OUTPUT_DIR = Path("./generated_icons")
# Directory creation moved to execution time to avoid side effects on import

# Consistency seeds for different asset categories
SEEDS = {
    "SEED_001": 42,      # B-roll (can vary)
    "SEED_002": 123456,  # Infographics (MUST match)
    "SEED_003": 789012,  # Motion graphics (brand)
    "SEED_004": 345678,  # UI overlays (template)
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
GENERATION_QUEUE = [
    # CORE SYMBOLS
    {
        "id": "icon_001",
        "name": "ferrari_icon",
        "priority": "HIGH",
        "scene": "Scene 1: Hook",
        "seed_key": "SEED_003",
        "prompt": (
            "Sleek red Ferrari sports car icon, side view, minimalist flat design, "
            "clean vector style, isolated on white background, "
            "professional tech presentation aesthetic, modern motion graphics style"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    {
        "id": "icon_002",
        "name": "shopping_cart_icon",
        "priority": "HIGH",
        "scene": "Scene 1: Hook",
        "seed_key": "SEED_003",
        "prompt": (
            "Simple shopping cart icon, minimalist flat design, "
            "clean vector style, isolated on white background, "
            "professional tech presentation aesthetic"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    
    # INFOGRAPHIC ICONS
    {
        "id": "icon_003",
        "name": "database_cylinder",
        "priority": "HIGH",
        "scene": "Scene 4: Skills Gap",
        "seed_key": "SEED_002",
        "prompt": (
            "Database cylinder icon, modern UI style, cyan accent #00d4ff, "
            "clean vector graphics, isolated on white background, "
            "tech infographic element"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    {
        "id": "icon_004",
        "name": "brain_processor",
        "priority": "HIGH",
        "scene": "Scene 4: Skills Gap",
        "seed_key": "SEED_002",
        "prompt": (
            "Brain circuit board icon, artificial intelligence symbol, "
            "purple accent #7b2cbf, minimalist vector design, "
            "isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    {
        "id": "icon_005",
        "name": "notification_bell",
        "priority": "MEDIUM",
        "scene": "Scene 4: Skills Gap",
        "seed_key": "SEED_002",
        "prompt": (
            "Notification bell icon with active badge, modern iOS style, "
            "orange accent #ff6b35, clean vector graphics, "
            "isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    
    # BOUNDED CONTEXT ICONS
    {
        "id": "icon_006",
        "name": "family_house",
        "priority": "MEDIUM",
        "scene": "Scene 5: Bounded Contexts",
        "seed_key": "SEED_002",
        "prompt": (
            "Minimalist house icon, home automation symbol, "
            "blue accent #00d4ff, rounded corners, flat design, "
            "vector icon, isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    {
        "id": "icon_007",
        "name": "finance_dollar",
        "priority": "MEDIUM",
        "scene": "Scene 5: Bounded Contexts",
        "seed_key": "SEED_002",
        "prompt": (
            "Dollar sign icon inside circle, financial symbol, "
            "purple accent #7b2cbf, modern clean lines, "
            "vector icon, isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    {
        "id": "icon_008",
        "name": "project_folder",
        "priority": "MEDIUM",
        "scene": "Scene 5: Bounded Contexts",
        "seed_key": "SEED_002",
        "prompt": (
            "Project folder icon, file management symbol, "
            "teal accent #00bfa5, flat minimalist design, "
            "vector icon, isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },

    # STATE MANAGEMENT ICONS
    {
        "id": "icon_009",
        "name": "workflow_branch",
        "priority": "MEDIUM",
        "scene": "Scene 8: State Management",
        "seed_key": "SEED_002",
        "prompt": (
            "Workflow branch icon, fork path symbol, decision point, "
            "modern tech UI style, blue/cyan gradient, "
            "vector graphics, isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    {
        "id": "icon_010",
        "name": "save_disk",
        "priority": "MEDIUM",
        "scene": "Scene 8: State Management",
        "seed_key": "SEED_002",
        "prompt": (
            "Save state icon, cloud upload symbol or floppy disk stylized, "
            "modern clean UI, teal accent #00bfa5, "
            "vector graphics, isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
]


def generate_asset(asset_config: Dict, output_dir: Path, manifest: Optional[object] = None, version: int = 1) -> Dict:
    """Generate a single asset using fal.ai"""
    print(f"\n{'='*60}")
    print(f"🎨 Generating Icon: {asset_config['name']}")
    print(f"   Scene: {asset_config['scene']}")
    print(f"   Priority: {asset_config['priority']}")
    print(f"   Seed: {asset_config['seed_key']} ({SEEDS[asset_config['seed_key']]})")
    print(f"{'='*60}")
    
    try:
        # Check cost before generating (for generations > $0.20)
        if not check_generation_cost(asset_config["model"]):
            return {
                "success": False,
                "error": "Cancelled by user due to cost",
            }
        
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
                    'icon',
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
            
            # Add to manifest if provided
            if manifest:
                manifest.add_asset(
                    filename=filename_png,
                    prompt=asset_config["prompt"],
                    asset_type="icon",
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
    """Process a queue of icons to generate"""
    print(f"\n{'='*60}")
    print("🚀 FAL.AI BATCH ICON GENERATOR")
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
    print(f"\n📊 Icons to generate: {len(queue)}")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Count by priority
    high_priority = [a for a in queue if a["priority"] == "HIGH"]
    medium_priority = [a for a in queue if a["priority"] == "MEDIUM"]
    
    print(f"   • HIGH priority: {len(high_priority)}")
    print(f"   • MEDIUM priority: {len(medium_priority)}")
    
    # Generate assets
    results = []
    for i, asset in enumerate(queue, 1):
        print(f"\n\n{'#'*60}")
        print(f"# Icon {i}/{len(queue)}")
        print(f"{'#'*60}")
        
        result = generate_asset(asset, output_dir, manifest)
        results.append({
            "asset_id": asset["id"],
            "name": asset["name"],
            "priority": asset["priority"],
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
        
    process_queue(GENERATION_QUEUE, DEFAULT_OUTPUT_DIR)


if __name__ == "__main__":
    main()

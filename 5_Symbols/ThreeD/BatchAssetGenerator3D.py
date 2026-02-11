#!/usr/bin/env python3
"""
fal.ai Batch 3D Asset Generator
Project: The Agentic Era - Managing 240+ Workflows
Generates 3D model assets using Hunyuan-3D text-to-3D API
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

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
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    try:
        from Utils.asset_utils import generate_filename, extract_scene_number, ManifestTracker
        from Utils.prompt_enhancer import enhance_prompt
    except ImportError:
        print("⚠️  Utils not found. Using legacy naming and no enhancement.")
        generate_filename = None
        extract_scene_number = None
        ManifestTracker = None
        enhance_prompt = None

# Configuration
OUTPUT_DIR = Path("./generated_assets")
OUTPUT_DIR.mkdir(exist_ok=True)

# Consistency seeds for different asset categories
SEEDS = {
    "SEED_001": 42,      # 3D models - B-roll style (can vary between generations)
    "SEED_002": 123456,  # Technical 3D objects (consistent for matching sets)
    "SEED_003": 789012,  # Decorative 3D elements (brand consistency)
}

# Asset generation queue for 3D models
GENERATION_QUEUE = [
    # HIGH PRIORITY 3D ASSETS
    {
        "id": "3d.1",
        "name": "shopping_cart_3d",
        "priority": "HIGH",
        "scene": "Scene 1: Hook",
        "seed_key": "SEED_001",
        "prompt": (
            "A modern shopping cart, sleek metallic design, detailed wheels, "
            "professional product visualization, clean geometry, suitable for animation, "
            "realistic materials with reflective metal surfaces"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    {
        "id": "3d.2",
        "name": "ferrari_sports_car_3d",
        "priority": "HIGH",
        "scene": "Scene 1: Hook",
        "seed_key": "SEED_001",
        "prompt": (
            "A sleek red Ferrari sports car, detailed exterior, "
            "high-quality 3D model with realistic paint material, "
            "professional automotive visualization, clean topology"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    
    # MEDIUM PRIORITY 3D ASSETS
    {
        "id": "3d.3",
        "name": "ai_robot_brain_3d",
        "priority": "MEDIUM",
        "scene": "Scene 4: Skills Gap",
        "seed_key": "SEED_002",
        "prompt": (
            "An AI robot brain with neural network connections, "
            "futuristic design, glowing blue accents, holographic elements, "
            "tech-inspired geometry, suitable for AI visualization"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    {
        "id": "3d.4",
        "name": "smartphone_notification_3d",
        "priority": "MEDIUM",
        "scene": "Scene 4: Skills Gap",
        "seed_key": "SEED_002",
        "prompt": (
            "A modern smartphone with notification badge icon floating above it, "
            "clean product design, detailed screen, metallic frame, "
            "professional product visualization"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    {
        "id": "3d.5",
        "name": "workflow_node_3d",
        "priority": "MEDIUM",
        "scene": "Scene 5: Bounded Contexts",
        "seed_key": "SEED_002",
        "prompt": (
            "A geometric node representing a workflow step, "
            "hexagonal or rounded cube shape, clean edges, "
            "suitable for technical diagrams, minimalist design"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    
    # LOW PRIORITY 3D ASSETS
    {
        "id": "3d.6",
        "name": "database_cylinder_3d",
        "priority": "LOW",
        "scene": "Scene 8: State Management",
        "seed_key": "SEED_002",
        "prompt": (
            "A database cylinder icon in 3D, classic database symbol, "
            "clean geometric design, metallic or glass material, "
            "suitable for technical architecture visualization"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
]


def check_api_key() -> str:
    """Check and return FAL_KEY or FAL_API_KEY from environment."""
    # Check for FAL_KEY first (existing convention)
    api_key = os.environ.get("FAL_KEY")
    
    # Fall back to FAL_API_KEY (repository secrets convention)
    if not api_key:
        api_key = os.environ.get("FAL_API_KEY")
    
    if not api_key:
        print("\n❌ ERROR: FAL_KEY or FAL_API_KEY environment variable not set")
        print("   Set it in your shell with: export FAL_KEY='your-api-key-here'  (bash/zsh)")
        print("   Or for Windows: set FAL_KEY=your-api-key-here  (cmd)")
        print("   Or use FAL_API_KEY in GitHub Actions secrets")
        raise ValueError("FAL_KEY or FAL_API_KEY not set")
    return api_key


def generate_3d_asset(
    asset_config: Dict,
    version: int = 1,
    manifest_tracker: Optional[ManifestTracker] = None
) -> Dict:
    """
    Generate a single 3D model asset using fal.ai Hunyuan-3D API.
    
    Args:
        asset_config: Configuration dictionary for the asset
        version: Version number for the asset
        manifest_tracker: Optional manifest tracker for asset tracking
        
    Returns:
        Dictionary with success status and metadata
    """
    # 1. Enhance Prompt using Gemini
    original_prompt = asset_config["prompt"]
    if enhance_prompt:
        print(f"✨ Enhancing prompt for {asset_config['name']}...")
        # Hunyuan-3D has a strict 200 char limit
        context = (
            "Enhance this prompt for a 3D model generator. "
            "Focus on 3D geometry, spatial structure, and material properties. "
            "CRITICAL: The output MUST be under 180 characters. Keep it concise."
        )
        enhanced_prompt = enhance_prompt(original_prompt, context=context)
        
        # Enforce hard limit
        if len(enhanced_prompt) > 195:
            enhanced_prompt = enhanced_prompt[:195]
            
        if enhanced_prompt != original_prompt:
            print(f"   Original: {original_prompt[:50]}...")
            print(f"   Enhanced: {enhanced_prompt[:50]}...")
            asset_config["prompt"] = enhanced_prompt
    
    print(f"\n{'='*60}")
    print(f"🎨 Generating 3D Model: {asset_config['name']}")
    print(f"   Scene: {asset_config.get('scene', 'Unknown')}")
    print(f"   Priority: {asset_config.get('priority', 'MEDIUM')}")
    if 'seed_key' in asset_config:
        print(f"   Seed: {asset_config['seed_key']} ({SEEDS.get(asset_config['seed_key'], 'N/A')})")
    print(f"{'='*60}")
    
    try:
        # Prepare arguments for Hunyuan-3D API
        arguments = {
            "prompt": asset_config["prompt"],
        }
        
        # Add seed if specified
        if "seed_key" in asset_config and asset_config["seed_key"] in SEEDS:
            arguments["seed"] = SEEDS[asset_config["seed_key"]]
        
        # Generate 3D model
        print("⏳ Sending request to fal.ai Hunyuan-3D...")
        result = fal_client.subscribe(
            asset_config["model"],
            arguments=arguments,
        )
        
        # Extract GLB model URL from result
        result_url = None
        if result and "model_urls" in result:
            if "glb" in result["model_urls"]:
                result_url = result["model_urls"]["glb"]["url"]
        
        if not result_url:
            return {
                "success": False,
                "error": "No GLB model URL in result",
            }
        
        print(f"✅ Generated successfully!")
        print(f"   GLB URL: {result_url}")
        
        # Automatic date stamp
        date_str = datetime.now().strftime("%Y%m%d")
        
        # Generate filename with proper naming convention
        scene_num = extract_scene_number(asset_config.get('id', '0.0')) if extract_scene_number else 0
        
        # Add date to name for uniqueness
        name_with_date = f"{asset_config['name']}_{date_str}"
        
        base_filename = generate_filename(
            scene_num,
            "3d",
            name_with_date,
            version
        ) if generate_filename else f"{name_with_date}_v{version}"
        
        filename_json = base_filename + '.json'
        filename_glb = base_filename + '.glb'
        
        # Define output path - use OUTPUT_DIR provided global or default
        # Ideally this function should take output_dir as arg, but it relies on global OUTPUT_DIR
        # We will fix this in process_queue
        # For now, we assume generated_assets is correct or updated
        
        # Save metadata
        metadata = {
            **asset_config,
            "original_prompt": original_prompt, # Store original
            "result_url": result_url,
            "filename": filename_glb,
            "format": "glb",
            "date": date_str
        }
        if 'seed_key' in asset_config:
            metadata["seed_value"] = SEEDS.get(asset_config["seed_key"])
        
        metadata_path = OUTPUT_DIR / filename_json
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"💾 Metadata saved: {metadata_path}")
        
        # Download GLB model
        import urllib.request
        glb_path = OUTPUT_DIR / filename_glb
        print(f"⏳ Downloading GLB model to {glb_path}...")
        urllib.request.urlretrieve(result_url, glb_path)
        print(f"✅ 3D model saved successfully!")
        
        if manifest_tracker and ManifestTracker:
            manifest_tracker.add_asset(
                filename=filename_glb,
                asset_type="3d",
                prompt=asset_config["prompt"],
                asset_id=asset_config.get("id", ""),
                result_url=result_url,
                local_path=glb_path,
                metadata={
                    "scene": asset_config.get("scene", "Unknown"),
                    "priority": asset_config.get("priority", "MEDIUM"),
                    "model": asset_config["model"],
                    "seed_key": asset_config.get("seed_key"),
                    "format": "glb"
                }
            )
        
        return {
            "success": True,
            "filename": filename_glb,
            "metadata_file": filename_json,
            "result_url": result_url,
        }
        
    except Exception as e:
        print(f"❌ Error generating 3D model: {e}")
        return {
            "success": False,
            "error": str(e),
        }



def process_queue(queue: List[Dict], output_dir: Path) -> Dict[str, List]:
    """
    Process a queue of assets to generate.
    
    Args:
        queue: List of asset configurations
        output_dir: Directory to save assets
        
    Returns:
        Dictionary with success/failed lists
    """
    global OUTPUT_DIR
    OUTPUT_DIR = output_dir
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Initialize manifest tracker if available
    manifest_tracker = ManifestTracker(output_dir) if ManifestTracker else None
    
    results = {
        "success": [],
        "failed": [],
    }
    
    print(f"📂 Output directory: {OUTPUT_DIR}")
    
    for asset_config in queue:
        result = generate_3d_asset(asset_config, version=1, manifest_tracker=manifest_tracker)
        
        if result["success"]:
            results["success"].append(asset_config["name"])
        else:
            results["failed"].append({
                "name": asset_config["name"],
                "error": result.get("error", "Unknown error")
            })
            
    # Save manifest if available
    if manifest_tracker and ManifestTracker:
        manifest_tracker.save_manifest("manifest_3d.json")
        
    return results


def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("🎨 fal.ai Batch 3D Asset Generator")
    print("   Model: Hunyuan-3D v3.1 Rapid Text-to-3D")
    print("="*60 + "\n")
    
    # Check API key
    try:
        api_key = check_api_key()
        print(f"✅ FAL_KEY found (length: {len(api_key)})")
    except ValueError as e:
        print(f"\n{e}")
        return
    
    # Initialize manifest tracker if available
    manifest_tracker = ManifestTracker() if ManifestTracker else None
    
    # Generate summary
    total_assets = len(GENERATION_QUEUE)
    high_priority = sum(1 for a in GENERATION_QUEUE if a.get('priority') == 'HIGH')
    medium_priority = sum(1 for a in GENERATION_QUEUE if a.get('priority') == 'MEDIUM')
    low_priority = sum(1 for a in GENERATION_QUEUE if a.get('priority') == 'LOW')
    
    print(f"\n📊 Generation Queue Summary:")
    print(f"   Total 3D models to generate: {total_assets}")
    print(f"   • HIGH priority: {high_priority}")
    print(f"   • MEDIUM priority: {medium_priority}")
    print(f"   • LOW priority: {low_priority}")
    
    # Ask for confirmation
    # NOTE: Cost estimate is approximate and should be verified with current API pricing
    # See: https://fal.ai/models/fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d
    estimated_cost_per_model = 0.10  # Approximate cost in USD per 3D model
    print(f"\n⚠️  Estimated cost: ~${total_assets * estimated_cost_per_model:.2f} (approx ${estimated_cost_per_model:.2f} per 3D model)")
    user_input = input("\nProceed with generation? (yes/no): ").strip().lower()
    if user_input not in ['yes', 'y']:
        print("❌ Generation cancelled by user.")
        return
    
    # Process the queue
    results = process_queue(GENERATION_QUEUE, OUTPUT_DIR)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 Generation Summary")
    print("="*60)
    print(f"✅ Successfully generated: {len(results['success'])} 3D models")
    print(f"❌ Failed: {len(results['failed'])} 3D models")
    
    if results['failed']:
        print("\n❌ Failed assets:")
        for failure in results['failed']:
            print(f"   • {failure['name']}: {failure['error']}")
    
    print("\n🎉 Batch 3D generation complete!")
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}")


if __name__ == "__main__":
    main()

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
OUTPUT_DIR = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Consistency seeds for different asset categories
SEEDS = {
    "SEED_001": 42,      # 3D models - B-roll style (can vary between generations)
    "SEED_002": 123456,  # Technical 3D objects (consistent for matching sets)
    "SEED_003": 789012,  # Decorative 3D elements (brand consistency)
}

# Asset generation queue — The Delivery Pilot Transformation (10 scenes)
GENERATION_QUEUE = [
    {
        "id": "3d.01",
        "name": "golden_microphone",
        "priority": "HIGH",
        "scene": "Scene 1: The Heavy Mic",
        "seed_key": "SEED_001",
        "prompt": (
            "A massive golden microphone, ornate design, heavy metallic, "
            "professional broadcast mic, shiny gold material, studio quality"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    {
        "id": "3d.02",
        "name": "compass_pivot",
        "priority": "HIGH",
        "scene": "Scene 2: The Pivot",
        "seed_key": "SEED_001",
        "prompt": (
            "A navigation compass with spinning needle, brass and glass, "
            "detailed mechanical design, pivot mechanism visible"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    {
        "id": "3d.03",
        "name": "mercury_liquid_figure",
        "priority": "HIGH",
        "scene": "Scene 3: Statues vs Mercury",
        "seed_key": "SEED_001",
        "prompt": (
            "A liquid mercury humanoid figure, reflective chrome surface, "
            "morphing shape, futuristic sci-fi character, metallic sheen"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    {
        "id": "3d.04",
        "name": "laptop_terminal",
        "priority": "HIGH",
        "scene": "Scene 4: The Clone Lab",
        "seed_key": "SEED_002",
        "prompt": (
            "A modern laptop with terminal code on screen, developer setup, "
            "clean product design, open lid, glowing screen"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    {
        "id": "3d.05",
        "name": "free_tier_toolbox",
        "priority": "MEDIUM",
        "scene": "Scene 5: The Free Tier Journey",
        "seed_key": "SEED_002",
        "prompt": (
            "A futuristic toolbox with holographic tools floating above, "
            "free badge label, clean geometric design, tech inspired"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    {
        "id": "3d.06",
        "name": "internet_kill_switch",
        "priority": "MEDIUM",
        "scene": "Scene 6: Internet Kill Switch",
        "seed_key": "SEED_002",
        "prompt": (
            "A large red emergency button on a pedestal, industrial design, "
            "kill switch style, metallic base, warning stripes"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    {
        "id": "3d.07",
        "name": "ai_brain_feast",
        "priority": "HIGH",
        "scene": "Scene 7: The LLM Feast",
        "seed_key": "SEED_001",
        "prompt": (
            "A glowing AI brain with neural connections, holographic display, "
            "futuristic tech, blue energy pulses, floating in space"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    {
        "id": "3d.08",
        "name": "automation_gear",
        "priority": "MEDIUM",
        "scene": "Scene 8: The Bespoke Logic",
        "seed_key": "SEED_002",
        "prompt": (
            "Interconnected mechanical gears in motion, automation symbol, "
            "steampunk brass design, clean geometry, detailed teeth"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    {
        "id": "3d.09",
        "name": "rocket_cicd",
        "priority": "MEDIUM",
        "scene": "Scene 9: Success Metrics",
        "seed_key": "SEED_003",
        "prompt": (
            "A small rocket on a launch pad, space shuttle style, "
            "detailed fins and body, metallic surface, ready for launch"
        ),
        "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
    },
    {
        "id": "3d.10",
        "name": "futuristic_city",
        "priority": "HIGH",
        "scene": "Scene 10: Conclusion",
        "seed_key": "SEED_003",
        "prompt": (
            "A futuristic miniature city with drones flying above, "
            "skyscrapers with holographic signs, clean sci-fi design"
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
            "CRITICAL: The output MUST be under 180 characters. Keep it concise."
        )
        # Create a log file for prompt enhancements in the output directory
        log_path = OUTPUT_DIR / "prompt_enhancements_log.txt"
        enhanced_prompt = enhance_prompt(original_prompt, context=context, log_path=str(log_path))
        
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
        
        # Debug result
        # print(f"DEBUG: API Result: {result}")
        
        # Extract Model URL from result (GLB preferred, then OBJ)
        result_url = None
        extension = "glb"
        
        if result and isinstance(result, dict) and "model_urls" in result:
            model_urls = result["model_urls"]
            if model_urls and isinstance(model_urls, dict):
                # Try GLB first
                if "glb" in model_urls and model_urls["glb"]:
                    result_url = model_urls["glb"].get("url")
                    extension = "glb"
                # Fallback to OBJ
                elif "obj" in model_urls and model_urls["obj"]:
                    result_url = model_urls["obj"].get("url")
                    extension = "obj"
        
        if not result_url:
            return {
                "success": False,
                "error": "No GLB or OBJ model URL in result",
            }
        
        print(f"✅ Generated successfully!")
        print(f"   {extension.upper()} URL: {result_url}")
        
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
        # Filename needs correct extension
        filename_model = base_filename + f'.{extension}'
        
        # Save metadata
        metadata = {
            **asset_config,
            "original_prompt": original_prompt, # Store original
            "result_url": result_url,
            "filename": filename_model,
            "format": extension,
            "date": date_str
        }
        if 'seed_key' in asset_config:
            metadata["seed_value"] = SEEDS.get(asset_config["seed_key"])
        
        metadata_path = OUTPUT_DIR / filename_json
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"💾 Metadata saved: {metadata_path}")
        
        # Download model
        import urllib.request
        model_path = OUTPUT_DIR / filename_model
        print(f"⏳ Downloading {extension.upper()} model to {model_path}...")
        urllib.request.urlretrieve(result_url, model_path)
        print(f"✅ 3D model saved successfully!")
        
        # Download texture if available and OBJ format
        if extension == "obj" and "model_urls" in result and "texture" in result["model_urls"] and result["model_urls"]["texture"]:
            texture_url = result["model_urls"]["texture"].get("url")
            if texture_url:
                texture_filename = base_filename + '_texture.png'
                texture_path = OUTPUT_DIR / texture_filename
                print(f"⏳ Downloading texture to {texture_path}...")
                urllib.request.urlretrieve(texture_url, texture_path)
        
        # Track in manifest if available
        if manifest_tracker and ManifestTracker:
            manifest_tracker.add_asset(
                filename=filename_model,
                asset_type="3d",
                prompt=asset_config["prompt"],
                asset_id=asset_config.get("id", ""),
                result_url=result_url,
                local_path=model_path,
                metadata={
                    "scene": asset_config.get("scene", "Unknown"),
                    "priority": asset_config.get("priority", "MEDIUM"),
                    "model": asset_config["model"],
                    "seed_key": asset_config.get("seed_key"),
                    "format": extension
                }
            )
        
        return {
            "success": True,
            "filename": filename_model,
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
    manifest_tracker = ManifestTracker(OUTPUT_DIR) if ManifestTracker else None
    
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
    
    # Cost estimate
    estimated_cost_per_model = 0.10  # Approximate cost in USD per 3D model
    print(f"\n⚠️  Estimated cost: ~${total_assets * estimated_cost_per_model:.2f} (approx ${estimated_cost_per_model:.2f} per 3D model)")
    print("🚀 Auto-proceeding with generation...")
    
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

    # Export GLB models to rotating videos
    print("\n" + "="*60)
    print("🎬 Exporting 3D Models to Video...")
    print("="*60)
    export_glb_to_videos(OUTPUT_DIR)


def export_glb_to_videos(output_dir: Path, fps: int = 30, duration: float = 4.0, resolution: tuple = (1280, 720)):
    """
    Export all GLB files in output_dir to rotating MP4 videos using trimesh + matplotlib + ffmpeg.

    Args:
        output_dir: Directory containing GLB files
        fps: Frames per second
        duration: Video duration in seconds
        resolution: Video resolution (width, height)
    """
    import glob
    glb_files = sorted(glob.glob(str(output_dir / "*.glb")))
    obj_files = sorted(glob.glob(str(output_dir / "*.obj")))
    model_files = glb_files + obj_files

    if not model_files:
        print("⚠️  No GLB/OBJ files found for video export.")
        return

    print(f"📦 Found {len(model_files)} 3D model(s) to convert to video")

    try:
        import trimesh
        import numpy as np
    except ImportError:
        print("❌ trimesh/numpy not installed. Run: pip3 install trimesh numpy")
        return

    # Try to use pyrender for high-quality rendering, fallback to matplotlib
    use_pyrender = False
    try:
        import pyrender
        use_pyrender = True
    except ImportError:
        pass

    video_count = 0
    for model_path in model_files:
        model_name = Path(model_path).stem
        video_path = output_dir / f"{model_name}_rotate.mp4"
        print(f"\n🎬 Converting: {Path(model_path).name} → {video_path.name}")

        try:
            # Load the 3D model
            scene = trimesh.load(model_path)

            # Handle Scene vs Mesh
            if isinstance(scene, trimesh.Scene):
                mesh = scene.dump(concatenate=True)
            else:
                mesh = scene

            if mesh is None or not hasattr(mesh, 'vertices') or len(mesh.vertices) == 0:
                print(f"   ⚠️  Empty mesh, skipping")
                continue

            # Center and normalize the mesh
            mesh.vertices -= mesh.centroid
            scale = mesh.extents.max()
            if scale > 0:
                mesh.vertices /= scale

            total_frames = int(fps * duration)
            frame_dir = output_dir / f"_frames_{model_name}"
            frame_dir.mkdir(exist_ok=True)

            # Render rotating frames using matplotlib (works headless)
            _render_frames_matplotlib(mesh, frame_dir, total_frames, resolution)

            # Compile frames to MP4 with ffmpeg
            frame_pattern = str(frame_dir / "frame_%04d.png")
            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", frame_pattern,
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-crf", "18",
                "-preset", "fast",
                str(video_path)
            ]

            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"   ✅ Video saved: {video_path.name}")
                video_count += 1
            else:
                print(f"   ❌ ffmpeg failed: {result.stderr[:200]}")

            # Cleanup frame directory
            import shutil
            shutil.rmtree(frame_dir, ignore_errors=True)

        except Exception as e:
            print(f"   ❌ Error: {e}")

    print(f"\n🎬 Video export complete: {video_count}/{len(model_files)} videos created")


def _render_frames_matplotlib(mesh, frame_dir: Path, total_frames: int, resolution: tuple):
    """Render rotating frames of a 3D mesh using matplotlib (headless compatible)."""
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import numpy as np

    vertices = np.array(mesh.vertices)
    faces = np.array(mesh.faces)

    # Get face colors if available
    if hasattr(mesh, 'visual') and hasattr(mesh.visual, 'face_colors'):
        face_colors = mesh.visual.face_colors / 255.0
    else:
        face_colors = np.full((len(faces), 4), [0.3, 0.6, 0.9, 0.85])

    dpi = 100
    fig_w = resolution[0] / dpi
    fig_h = resolution[1] / dpi

    for i in range(total_frames):
        angle = (360.0 / total_frames) * i
        fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi)
        ax = fig.add_subplot(111, projection='3d')

        # Create polygon collection for the faces
        polys = vertices[faces]
        collection = Poly3DCollection(polys, alpha=0.9)
        collection.set_facecolor(face_colors[:, :3])
        collection.set_edgecolor((0.2, 0.2, 0.2, 0.1))
        ax.add_collection3d(collection)

        # Set axis limits
        max_range = 0.7
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_zlim(-max_range, max_range)

        # Set viewing angle (rotate around)
        ax.view_init(elev=25, azim=angle)

        # Clean up the plot
        ax.set_axis_off()
        fig.patch.set_facecolor('#1a1a2e')
        ax.set_facecolor('#1a1a2e')

        frame_path = frame_dir / f"frame_{i:04d}.png"
        plt.savefig(str(frame_path), dpi=dpi, bbox_inches='tight',
                    pad_inches=0, facecolor='#1a1a2e')
        plt.close(fig)

        if (i + 1) % 30 == 0 or i == total_frames - 1:
            print(f"   🖼️  Rendered frame {i+1}/{total_frames}")


if __name__ == "__main__":
    main()

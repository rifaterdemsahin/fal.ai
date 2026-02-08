#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Anime
Project: Bulk Anime Generator with Storyline
Generates anime-style scenes based on a storyline/script
"""

import os
import json
import time
import urllib.request
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
OUTPUT_DIR = Path("./generated_anime")
OUTPUT_DIR.mkdir(exist_ok=True)

# Default anime storyline structure
DEFAULT_STORYLINE = {
    "title": "AI Adventure",
    "style": "anime",
    "scenes": [
        {
            "id": "1.1",
            "name": "hero_awakening",
            "priority": "HIGH",
            "scene": "Scene 1: The Awakening",
            "description": "The hero discovers their AI powers",
            "prompt": "Anime style, young protagonist with glowing eyes discovering AI powers, dramatic lighting, digital particles flowing around hands, futuristic city background, vibrant colors, studio quality animation, detailed character design, 16:9 aspect ratio",
            "duration_seconds": 5,
            "characters": ["Hero"],
            "setting": "Futuristic City"
        },
        {
            "id": "2.1",
            "name": "mentor_appears",
            "priority": "HIGH",
            "scene": "Scene 2: The Mentor",
            "description": "A wise mentor appears to guide the hero",
            "prompt": "Anime style, wise elderly mentor with white hair and glowing staff appearing in mystical light, heroic pose, magical aura, detailed background with ancient technology, cinematic composition, vibrant colors, high quality animation, 16:9 aspect ratio",
            "duration_seconds": 5,
            "characters": ["Hero", "Mentor"],
            "setting": "Ancient Temple"
        },
        {
            "id": "3.1",
            "name": "training_montage",
            "priority": "MEDIUM",
            "scene": "Scene 3: Training",
            "description": "Hero trains to master AI abilities",
            "prompt": "Anime style, dynamic training sequence with hero practicing AI techniques, energy blasts, speed lines, multiple action poses, dramatic camera angles, sunset background, intense colors, action anime aesthetic, 16:9 aspect ratio",
            "duration_seconds": 5,
            "characters": ["Hero", "Mentor"],
            "setting": "Training Grounds"
        },
        {
            "id": "4.1",
            "name": "villain_reveal",
            "priority": "HIGH",
            "scene": "Scene 4: The Threat",
            "description": "The main villain is revealed",
            "prompt": "Anime style, menacing villain with dark aura standing in shadows, glowing red eyes, dramatic lighting from below, cyberpunk city in chaos behind them, ominous atmosphere, detailed character design, cinematic wide shot, 16:9 aspect ratio",
            "duration_seconds": 5,
            "characters": ["Villain"],
            "setting": "Dark Citadel"
        },
        {
            "id": "5.1",
            "name": "final_battle",
            "priority": "HIGH",
            "scene": "Scene 5: Final Confrontation",
            "description": "Epic battle between hero and villain",
            "prompt": "Anime style, epic battle scene with hero and villain clashing, energy explosions, dynamic action poses, speed lines, dramatic lighting, debris flying, intense colors, cinematic wide shot, high-quality animation, 16:9 aspect ratio",
            "duration_seconds": 5,
            "characters": ["Hero", "Villain"],
            "setting": "Battle Arena"
        }
    ]
}

# Available anime models from fal.ai
ANIME_MODELS = {
    "minimax": "fal-ai/minimax/video-01",  # Text-to-video
    "kling": "fal-ai/kling-video/v1/standard/text-to-video",  # Text-to-video with anime support
    "flux_anime": "fal-ai/flux/schnell",  # Fast image generation (can be styled for anime)
    "flux_dev": "fal-ai/flux/dev",  # Higher quality image generation
}


def load_storyline_from_file(file_path: Path) -> Dict:
    """Load storyline from JSON file"""
    if not file_path.exists():
        print(f"⚠️  Storyline file not found: {file_path}")
        print("📝 Using default storyline...")
        return DEFAULT_STORYLINE
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"✅ Loaded storyline: {data.get('title', 'Untitled')}")
            return data
    except Exception as e:
        print(f"❌ Error loading storyline: {e}")
        print("📝 Using default storyline...")
        return DEFAULT_STORYLINE


def generate_anime_scene(
    scene_config: Dict,
    output_dir: Path,
    model: str = "minimax",
    manifest: Optional[object] = None,
    version: int = 1
) -> Dict:
    """Generate a single anime scene using fal.ai"""
    print(f"\n{'='*60}")
    print(f"🎬 Generating Anime Scene: {scene_config['name']}")
    print(f"   Scene: {scene_config['scene']}")
    print(f"   Description: {scene_config['description']}")
    print(f"   Priority: {scene_config.get('priority', 'MEDIUM')}")
    print(f"   Model: {ANIME_MODELS.get(model, ANIME_MODELS['minimax'])}")
    print(f"   Characters: {', '.join(scene_config.get('characters', []))}")
    print(f"   Setting: {scene_config.get('setting', 'Unknown')}")
    print(f"{'='*60}")
    
    try:
        # Select the appropriate model
        model_id = ANIME_MODELS.get(model, ANIME_MODELS['minimax'])
        
        # Prepare arguments based on model type
        arguments = {
            "prompt": scene_config["prompt"],
        }
        
        # Add model-specific parameters
        if "minimax" in model_id:
            # Minimax video generation
            pass  # Usually just takes prompt
        elif "kling" in model_id:
            # Kling video generation
            arguments["aspect_ratio"] = scene_config.get("aspect_ratio", "16:9")
            arguments["duration"] = str(scene_config.get("duration_seconds", 5)) + "s"
        elif "flux" in model_id:
            # Flux image generation (for anime stills)
            arguments["image_size"] = scene_config.get("image_size", {"width": 1920, "height": 1080})
            arguments["num_inference_steps"] = scene_config.get("num_inference_steps", 4)
            arguments["num_images"] = 1
        
        # Generate scene
        print("⏳ Generating anime scene (this may take 2-3 minutes)...")
        result = fal_client.subscribe(
            model_id,
            arguments=arguments,
        )
        
        # Extract result URL based on model type
        result_url = None
        file_extension = "mp4"  # Default for video models
        
        if result:
            # Video models
            if "video" in result and "url" in result["video"]:
                result_url = result["video"]["url"]
                file_extension = "mp4"
            elif "video_url" in result:
                result_url = result["video_url"]
                file_extension = "mp4"
            elif "videos" in result and len(result["videos"]) > 0:
                result_url = result["videos"][0]["url"]
                file_extension = "mp4"
            # Image models
            elif "images" in result and len(result["images"]) > 0:
                result_url = result["images"][0]["url"]
                file_extension = "png"
            elif "url" in result:
                result_url = result["url"]
                # Try to infer extension from URL
                if result_url.endswith('.png'):
                    file_extension = "png"
                elif result_url.endswith('.jpg') or result_url.endswith('.jpeg'):
                    file_extension = "jpg"
        
        if result_url:
            print(f"✅ Scene generated successfully!")
            print(f"   URL: {result_url}")
            
            # Generate filename using new convention if available
            if generate_filename and extract_scene_number:
                scene_num = extract_scene_number(scene_config.get('id', '0.0'))
                base_filename = generate_filename(
                    scene_num,
                    'anime',
                    scene_config['name'],
                    version
                )
                filename_json = base_filename + '.json'
                filename_asset = base_filename + '.' + file_extension
            else:
                # Fallback to legacy naming
                filename_json = f"{scene_config['name']}.json"
                filename_asset = f"{scene_config['name']}.{file_extension}"
            
            # Save metadata
            output_path = output_dir / filename_json
            metadata = {
                **scene_config,
                "result_url": result_url,
                "generated_at": time.time(),
                "filename": filename_asset,
                "file_extension": file_extension,
                "model_used": model_id,
            }
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Metadata saved: {output_path}")
            
            # Download asset
            asset_path = output_dir / filename_asset
            urllib.request.urlretrieve(result_url, asset_path)
            print(f"💾 Anime scene saved: {asset_path}")
            
            # Add to manifest if provided
            if manifest:
                manifest.add_asset(
                    filename=filename_asset,
                    prompt=scene_config["prompt"],
                    asset_type="anime",
                    asset_id=scene_config.get("id", "unknown"),
                    result_url=result_url,
                    local_path=str(asset_path),
                    metadata={
                        "scene": scene_config.get("scene", ""),
                        "description": scene_config.get("description", ""),
                        "priority": scene_config.get("priority", ""),
                        "model": model_id,
                        "characters": scene_config.get("characters", []),
                        "setting": scene_config.get("setting", ""),
                    }
                )
            
            return {
                "success": True,
                "url": result_url,
                "local_path": str(asset_path),
                "filename": filename_asset,
            }
        else:
            print(f"❌ Generation failed: No URL in result")
            print(f"   Result keys: {result.keys() if result else 'None'}")
            return {"success": False, "error": "No URL returned"}
            
    except Exception as e:
        print(f"❌ Error generating anime scene: {str(e)}")
        return {"success": False, "error": str(e)}


def process_storyline(
    storyline: Dict,
    output_dir: Path,
    model: str = "minimax",
    manifest: Optional[object] = None
) -> List[Dict]:
    """Process an entire anime storyline and generate all scenes"""
    print(f"\n{'='*60}")
    print("🎌 FAL.AI BULK ANIME GENERATOR")
    print(f"   Storyline: {storyline.get('title', 'Untitled')}")
    print(f"   Style: {storyline.get('style', 'anime')}")
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
    
    scenes = storyline.get("scenes", [])
    print(f"\n🎬 Scenes to generate: {len(scenes)}")
    
    if not scenes:
        print("\n⚠️  NO SCENES IN STORYLINE.")
        return []
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Count by priority
    high_priority = [s for s in scenes if s.get("priority") == "HIGH"]
    medium_priority = [s for s in scenes if s.get("priority") == "MEDIUM"]
    low_priority = [s for s in scenes if s.get("priority") == "LOW"]
    
    print(f"   • HIGH priority: {len(high_priority)}")
    print(f"   • MEDIUM priority: {len(medium_priority)}")
    print(f"   • LOW priority: {len(low_priority)}")
    
    # Display storyline summary
    print(f"\n📖 STORYLINE SUMMARY:")
    for i, scene in enumerate(scenes, 1):
        print(f"   {i}. {scene.get('scene', 'Unknown')} - {scene.get('description', 'No description')}")
        print(f"      Characters: {', '.join(scene.get('characters', []))}")
        print(f"      Setting: {scene.get('setting', 'Unknown')}")
    
    # Generate scenes
    results = []
    for i, scene in enumerate(scenes, 1):
        print(f"\n\n{'#'*60}")
        print(f"# Scene {i}/{len(scenes)}")
        print(f"{'#'*60}")
        
        result = generate_anime_scene(scene, output_dir, model, manifest)
        results.append({
            "scene_id": scene.get("id", f"auto_{i}"),
            "name": scene["name"],
            "scene": scene.get("scene", ""),
            "priority": scene.get("priority", "MEDIUM"),
            **result
        })
        
        # Add a delay between requests to be nice to the API
        if i < len(scenes):
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
            print(f"   • {r['name']} ({r['scene']})")
    
    if failed:
        print("\n❌ FAILED GENERATIONS:")
        for r in failed:
            print(f"   • {r['name']} - {r.get('error', 'Unknown error')}")
    
    # Save summary
    summary_path = output_dir / "generation_summary.json"
    with open(summary_path, 'w') as f:
        json.dump({
            "storyline": storyline.get("title", "Untitled"),
            "total_scenes": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "results": results
        }, f, indent=2)
    
    print(f"\n💾 Summary saved: {summary_path}")
    
    return results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Bulk Anime Generator with Storyline")
    parser.add_argument(
        "--storyline",
        type=str,
        help="Path to storyline JSON file (default: uses built-in storyline)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./generated_anime",
        help="Output directory for generated anime scenes"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="minimax",
        choices=["minimax", "kling", "flux_anime", "flux_dev"],
        help="Model to use for generation (default: minimax)"
    )
    parser.add_argument(
        "--create-example",
        action="store_true",
        help="Create an example storyline JSON file"
    )
    
    args = parser.parse_args()
    
    # Create example storyline if requested
    if args.create_example:
        example_path = Path("example_anime_storyline.json")
        with open(example_path, 'w') as f:
            json.dump(DEFAULT_STORYLINE, f, indent=2)
        print(f"✅ Created example storyline: {example_path}")
        print("📝 Edit this file to customize your anime storyline, then run:")
        print(f"   python {Path(__file__).name} --storyline example_anime_storyline.json")
        return
    
    # Load storyline
    if args.storyline:
        storyline_path = Path(args.storyline)
        storyline = load_storyline_from_file(storyline_path)
    else:
        print("📝 No storyline file specified, using default storyline...")
        print("💡 TIP: Use --create-example to generate a template storyline file")
        storyline = DEFAULT_STORYLINE
    
    # Setup output directory
    output_dir = Path(args.output)
    
    # Setup manifest tracker if available
    manifest = None
    if ManifestTracker:
        manifest = ManifestTracker(output_dir)
    
    # Process storyline
    results = process_storyline(storyline, output_dir, args.model, manifest)
    
    # Save manifest
    if manifest:
        manifest_path = output_dir / "manifest.json"
        manifest.save(manifest_path)
        print(f"\n📝 Manifest saved: {manifest_path}")
    
    print("\n✨ Anime generation complete!")
    print(f"📁 Check your generated scenes in: {output_dir.absolute()}")


if __name__ == "__main__":
    main()

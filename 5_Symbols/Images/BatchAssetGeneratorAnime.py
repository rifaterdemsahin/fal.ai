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
from typing import Dict, List, Optional, Union
import re

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
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    try:
        from Utils.asset_utils import generate_filename, extract_scene_number, ManifestTracker
        from Utils.prompt_enhancer import enhance_prompt
    except ImportError:
        print("⚠️  asset_utils or prompt_enhancer not found. Using legacy naming and no enhancement.")
        generate_filename = None
        extract_scene_number = None
        ManifestTracker = None
        enhance_prompt = lambda p, **kwargs: p  # no-op fallback

# Configuration
# Configuration
DEFAULT_OUTPUT_DIR = Path("./generated_anime")
# Directory creation moved to execution time to avoid side effects on import

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
    "flux_anime": "fal-ai/flux/schnell",  # Fast anime image generation
    "flux_dev": "fal-ai/flux/dev",  # High quality anime image generation
    "flux_pro": "fal-ai/flux-pro/v1.1",  # Professional grade image generation
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


def parse_storyboard_markdown(file_path: Path) -> Dict:
    """Parse a markdown storyboard file into a storyline dictionary"""
    if not file_path.exists():
        print(f"⚠️  Storyboard file not found: {file_path}")
        return DEFAULT_STORYLINE

    print(f"📖 Parsing storyboard: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        storyline = {
            "title": "Storyboard Animation",
            "style": "anime",
            "scenes": []
        }
        
        # Regex for frames
        # ### Frame 1: Title (Time)
        frame_pattern = re.compile(r'### Frame (\d+): (.*?)(?:\s*\(.*?\))?\n(.*?)(?=### Frame|\Z)', re.DOTALL)
        
        matches = frame_pattern.findall(content)
        
        for i, (frame_num, title, body) in enumerate(matches, 1):
            # Extract details
            shot_type = re.search(r'\*\*Shot Type:\*\* (.*)', body)
            visuals = re.search(r'\*\*Visual Elements:\*\* (.*)', body)
            mood = re.search(r'\*\*Mood:\*\* (.*)', body)
            camera = re.search(r'\*\*Camera Movement:\*\* (.*)', body)
            
            shot_type_str = shot_type.group(1).strip() if shot_type else ""
            visuals_str = visuals.group(1).strip() if visuals else ""
            mood_str = mood.group(1).strip() if mood else ""
            camera_str = camera.group(1).strip() if camera else ""
            
            # Construct prompt
            # Anime style, [Visuals], [Mood], [Shot Type], [Camera]
            prompt_parts = ["Anime style"]
            if visuals_str: prompt_parts.append(visuals_str)
            if mood_str: prompt_parts.append(mood_str)
            if shot_type_str: prompt_parts.append(shot_type_str)
            if camera_str: prompt_parts.append(camera_str)
            prompt_parts.append("high quality animation, 16:9 aspect ratio")
            
            prompt = ", ".join(prompt_parts)
            
            scene = {
                "id": f"{frame_num}",
                "name": f"frame_{frame_num}_{title.strip().lower().replace(' ', '_')}",
                "priority": "MEDIUM",
                "scene": f"Frame {frame_num}: {title.strip()}",
                "description": f"{visuals_str}. Mood: {mood_str}",
                "prompt": prompt,
                "duration_seconds": 5, # Default
                "characters": [],
                "setting": "Unknown"
            }
            
            storyline["scenes"].append(scene)
            
        print(f"✅ Parsed {len(storyline['scenes'])} scenes from storyboard")
        return storyline
        
    except Exception as e:
        print(f"❌ Error parsing storyboard: {e}")
        return DEFAULT_STORYLINE


def generate_anime_scene(
    scene_config: Dict,
    output_dir: Path,
    model: str = "flux_anime",
    manifest: Optional[object] = None,
    version: int = 1
) -> Dict:
    """Generate a single anime scene using fal.ai (Image Only)"""
    print(f"\n{'='*60}")
    print(f"🎬 Generating Anime Scene: {scene_config['name']}")
    print(f"   Scene: {scene_config['scene']}")
    print(f"   Description: {scene_config['description']}")
    print(f"   Priority: {scene_config.get('priority', 'MEDIUM')}")
    print(f"   Model: {ANIME_MODELS.get(model, ANIME_MODELS['flux_anime'])}")
    print(f"   Characters: {', '.join(scene_config.get('characters', []))}")
    print(f"   Setting: {scene_config.get('setting', 'Unknown')}")
    print(f"{'='*60}")
    
    try:
        # Select the appropriate model
        model_id = ANIME_MODELS.get(model, ANIME_MODELS['flux_anime'])
        
        # Determine asset type for enhancement
        asset_type = 'image'
        
        # Enhance prompt if function is available
        prompt_text = scene_config["prompt"]
        if enhance_prompt:
            print(f"✨ Enhancing prompt with Gemini ({asset_type})...")
            # Create a log file for prompt enhancements in the output directory
            log_path = output_dir / "prompt_enhancements_log.txt"
            enhanced_prompt = enhance_prompt(prompt_text, asset_type=asset_type, log_path=str(log_path))
            if enhanced_prompt != prompt_text:
                print(f"   Original: {prompt_text[:50]}...")
                print(f"   Enhanced: {enhanced_prompt[:50]}...")
                prompt_text = enhanced_prompt
        
        # Prepare arguments based on model type
        arguments = {
            "prompt": prompt_text,
        }
        
        # Add model-specific parameters for image generation
        arguments["image_size"] = scene_config.get("image_size", {"width": 1920, "height": 1080})
        arguments["num_inference_steps"] = scene_config.get("num_inference_steps", 4)
        arguments["num_images"] = 1
        
        # Add seed if consistent generation is desired
        if "seed" in scene_config:
            arguments["seed"] = scene_config["seed"]
        
        # Generate scene
        print("⏳ Generating anime scene (this may take 2-3 minutes)...")
        result = fal_client.subscribe(
            model_id,
            arguments=arguments,
        )
        
        # Extract result URL
        result_url = None
        file_extension = "png"  # Default for image models
        
        if result:
            if "images" in result and len(result["images"]) > 0:
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
                # Add date to filename for organization
                date_str = datetime.now().strftime("%Y%m%d")
                name_with_date = f"{scene_config['name']}_{date_str}"
                
                base_filename = generate_filename(
                    scene_num,
                    'anime',
                    name_with_date,
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
    model: str = "flux_anime",
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
        default="flux_anime",
        choices=["flux_anime", "flux_dev", "flux_pro"],
        help="Model to use for generation (default: flux_anime)"
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
        input_path = Path(args.storyline)
        if input_path.is_dir():
            # Check for source_storyboard.md
            storyboard_path = input_path / "source_storyboard.md"
            if storyboard_path.exists():
                storyline = parse_storyboard_markdown(storyboard_path)
            else:
                # Check for storyline.json
                json_path = input_path / "storyline.json"
                if json_path.exists():
                    storyline = load_storyline_from_file(json_path)
                else:
                    print(f"⚠️  No source_storyboard.md or storyline.json found in {input_path}")
                    storyline = DEFAULT_STORYLINE
        else:
            if input_path.suffix.lower() == '.json':
                storyline = load_storyline_from_file(input_path)
            elif input_path.suffix.lower() == '.md':
                storyline = parse_storyboard_markdown(input_path)
            else:
                print(f"⚠️  Unsupported file format: {input_path.suffix}")
                storyline = DEFAULT_STORYLINE
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
        manifest.save_manifest("manifest.json")
    
    print("\n✨ Anime generation complete!")
    print(f"📁 Check your generated scenes in: {output_dir.absolute()}")


if __name__ == "__main__":
    main()

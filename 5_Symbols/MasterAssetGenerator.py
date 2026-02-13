#!/usr/bin/env python3
"""
fal.ai Master Asset Generator
Project: The Agentic Era
Orchestrates generation of all assets for a given week/video project.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List

try:
    import yaml
except ImportError:
    yaml = None
    print("⚠️  PyYAML not installed. YAML support disabled. Run: pip install PyYAML")

# Add the current directory to path so we can import local modules
sys.path.append(str(Path(__file__).parent))

# Import path configuration for weekly structure
# Import path configuration for weekly structure
from paths_config import get_weekly_paths, ensure_weekly_structure, get_latest_weekly_id

# Import individual generators
from Images import BatchAssetGeneratorImages as gen_images
from Video import BatchAssetGeneratorLowerThirds as gen_lower_thirds
from Images import BatchAssetGeneratorIcons as gen_icons
from Video import BatchAssetGeneratorVideo as gen_video
from Audio import BatchAssetGeneratorMusic as gen_music
from Images import BatchAssetGeneratorGraphics as gen_graphics
from Video import BatchAssetGeneratorChapterMarkers as gen_chapter_markers
from Audio import BatchAssetGeneratorAudio as gen_audio
from Diagrams import BatchAssetGeneratorDiagrams as gen_diagrams
from Images import BatchAssetGeneratorMemoryPalace as gen_memory_palace
from Utils import EstimateWeeklyVideoCost as gen_cost
from Utils.asset_utils import ManifestTracker

# Estimated costs per generation (USD)
COST_ESTIMATES = {
    "fal-ai/flux/schnell": 0.003,
    "fal-ai/flux/dev": 0.025,
    "fal-ai/minimax/video-01": 0.10,  # 5s clip
    "fal-ai/kling-video/v1/standard/text-to-video": 0.15,
    "fal-ai/stable-audio": 0.02,
}
DEFAULT_COST = 0.03

def load_config(config_path: Path) -> Dict:
    """Load the assets configuration from JSON or YAML"""
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return {}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            # Try JSON first
            if config_path.suffix.lower() == '.json':
                return json.load(f)
            # Try YAML
            elif config_path.suffix.lower() in ['.yaml', '.yml']:
                if yaml is None:
                    print("❌ Cannot load YAML file. PyYAML not installed.")
                    return {}
                result = yaml.safe_load(f)
                return result if result is not None else {}
            else:
                # Unknown format, try JSON as default
                return json.load(f)
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return {}

def merge_configs(config_dir: Path) -> Dict:
    """Load and merge all YAML and JSON config files from a directory
    
    Note: If the same asset ID appears in multiple files, all instances will be included.
    This allows for incremental additions, but users should ensure IDs are unique across files
    if duplicates are not desired.
    """
    merged = {}
    
    # Find all YAML and JSON files
    config_files = list(config_dir.glob('*.yaml')) + \
                   list(config_dir.glob('*.yml')) + \
                   list(config_dir.glob('*.json'))
    
    if not config_files:
        return merged
    
    print(f"\n📂 Loading configuration files from: {config_dir}")
    for config_file in sorted(config_files):
        print(f"   • {config_file.name}")
        config = load_config(config_file)
        
        # Merge the config
        for key, value in config.items():
            if key in merged:
                # If key exists, extend the list if it's a list
                if isinstance(merged[key], list) and isinstance(value, list):
                    merged[key].extend(value)
                else:
                    # Otherwise, replace with the new value
                    merged[key] = value
            else:
                merged[key] = value
    
    return merged

def estimate_cost(config: Dict) -> float:
    """Calculate and print estimated cost"""
    total_cost = 0.0
    print("\n💰 COST ESTIMATION")
    print("=" * 60)
    
    # Check all sections
    for category, items in config.items():
        if not isinstance(items, list):
            continue
            
        category_cost = 0.0
        for item in items:
            model = item.get("model", "")
            # Try exact match or substring match
            cost = DEFAULT_COST
            for key, val in COST_ESTIMATES.items():
                if key in model:
                    cost = val
                    break
            
            category_cost += cost
            total_cost += cost
            
        print(f"   • {category.title().ljust(15)}: {len(items)} items (~${category_cost:.2f})")
    
    print("-" * 60)
    print(f"   TOTAL ESTIMATED COST: ${total_cost:.2f}")
    print("=" * 60)
    return total_cost

def main():
    parser = argparse.ArgumentParser(
        description="Master Asset Generator for a video project week",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # New weekly structure (recommended):
  python MasterAssetGenerator.py --week 2026-02-10
  
  # specific week:
  python MasterAssetGenerator.py --week 2026-02-10

  # Latest week (most recent folder):
  python MasterAssetGenerator.py --week latest
  
  # Auto-generate from today's date:
  python MasterAssetGenerator.py --week auto
        """
    )
    
    # Support both legacy and new modes
    parser.add_argument(
        "week_dir", 
        type=str, 
        nargs='?',  # Make it optional
        help="[LEGACY] Path to the weekly video folder (e.g., ../3_Simulation/Feb1Youtube)"
    )
    parser.add_argument(
        "--week", 
        type=str, 
        dest="weekly_id",
        help="Weekly ID for new structure (e.g., '2026-02-10', 'latest', or 'auto')"
    )
    
    args = parser.parse_args()

    # Determine which mode to use
    use_new_structure = False
    
    # Default to "latest" if no arguments provided
    if not args.weekly_id and not args.week_dir:
        args.weekly_id = "latest"

    if args.weekly_id:
        # New mode: Use weekly structure
        if args.weekly_id.lower() == 'auto':
            weekly_id = None  # Will auto-generate from today's date
        elif args.weekly_id.lower() == 'latest':
            weekly_id = get_latest_weekly_id()
            if not weekly_id:
                print("❌ No existing weekly directories found in 3_Simulation.")
                return
            print(f"📅 Found latest week: {weekly_id}")
        else:
            weekly_id = args.weekly_id
        
        paths = ensure_weekly_structure(weekly_id)
        week_dir = paths['base']
        input_dir = paths['input']
        output_dir = paths['output']
        use_new_structure = True
        
        print("\n🎬 MASTER GENERATOR: Weekly Video Production")
        print(f"   Weekly ID: {paths['weekly_id']}")
        print(f"   Base: {week_dir}")
        print(f"   Input: {input_dir}")
        print(f"   Output: {output_dir}")
        
    elif args.week_dir:
        # Legacy mode: Use provided directory
        week_dir = Path(args.week_dir).resolve()
        if not week_dir.exists():
            print(f"❌ Directory not found: {week_dir}")
            return
        
        # In legacy mode, input and output are the same (week_dir)
        input_dir = week_dir
        output_dir = week_dir
        use_new_structure = False
        
        print(f"\n🎬 MASTER GENERATOR: {week_dir.name} [LEGACY MODE]")
        print(f"   Path: {week_dir}")
    
    # Load configuration
    # Try to merge all config files from input directory
    # First check if there are any YAML/JSON files in the input directory
    config_files = list(input_dir.glob('*.yaml')) + \
                   list(input_dir.glob('*.yml')) + \
                   list(input_dir.glob('*.json'))
    
    if not use_new_structure and not config_files:
        # Legacy mode fallback - check week_dir
        config_files = list(week_dir.glob('*.yaml')) + \
                       list(week_dir.glob('*.yml')) + \
                       list(week_dir.glob('*.json'))
        config_dir = week_dir
    else:
        config_dir = input_dir
    
    if not config_files:
        location = "input folder" if use_new_structure else "directory"
        print(f"⚠️  No configuration files (.yaml/.yml/.json) found in {location}: {config_dir}")
        print("   Please create batch_generation_data.yaml or individual asset YAML files.")
        return

    # Load and merge all configuration files
    config = merge_configs(config_dir)
    if not config:
        print("❌ No valid configuration loaded")
        return

    # Check for text marker file (for chapter markers generator)
    # Look in input directory first (new structure), then base (legacy)
    marker_file = input_dir / "source_chapter_markers.txt"
    if not marker_file.exists():
        marker_file = input_dir / "chapter_markers.txt"
    if not marker_file.exists() and not use_new_structure:
        # Legacy fallback
        marker_file = week_dir / "source_chapter_markers.txt"
        if not marker_file.exists():
            marker_file = week_dir / "chapter_markers.txt"

    # Estimate Cost
    # In new structure, config is in input_dir; in legacy mode, it's in week_dir
    cost_dir = input_dir if use_new_structure else week_dir
    gen_cost.generate_report(cost_dir)
    
    # Confirm
    print("\n⚠️  You are about to generate assets which will incur costs.")
    response = input("🤔 Proceed with ALL generations? (yes/no/select): ").strip().lower()
    
    if response not in ['yes', 'y', 'select']:
        print("❌ Cancelled")
        return

    selected_mode = False
    if response == 'select':
        selected_mode = True
        print("\nSelect categories to run (comma separated, e.g. images,video):")
        categories = list(config.keys()) + ["chapter_markers", "audio_markers", "memory_palace"]
        print(f"Available: {', '.join(categories)}")
        selection = input("> ").strip().lower().split(',')
        selection = [s.strip() for s in selection]
    
    # Initialize Manifest Tracker
    # In new structure, save manifest to output folder; in legacy mode, save to week_dir
    manifest_dir = output_dir if use_new_structure else week_dir
    manifest = ManifestTracker(manifest_dir)
    print(f"\n📋 Manifest tracking initialized (will save to: {manifest_dir})")
    
    # Execute Generators
    # 1. Images
    if "images" in config and (not selected_mode or "images" in selection):
        print("\n" + "!"*60)
        print("🖼️  GENERATING IMAGES")
        gen_images.process_queue(config["images"], output_dir / "generated_assets_Images", manifest)

    # 2. Lower Thirds
    if "lower_thirds" in config and (not selected_mode or "lower_thirds" in selection):
        print("\n" + "!"*60)
        print("📺 GENERATING LOWER THIRDS")
        gen_lower_thirds.process_queue(config["lower_thirds"], output_dir / "generated_assets_lowerthirds", manifest)
    
    # 3. Icons
    if "icons" in config and (not selected_mode or "icons" in selection):
        print("\n" + "!"*60)
        print("🔹 GENERATING ICONS")
        gen_icons.process_queue(config["icons"], output_dir / "generated_icons", manifest)
        
    # 4. Video
    if "video" in config and (not selected_mode or "video" in selection):
        print("\n" + "!"*60)
        print("🎥 GENERATING VIDEO CLIPS")
        gen_video.process_queue(config["video"], output_dir / "generated_video", manifest)

    # 5. Music
    if "music" in config and (not selected_mode or "music" in selection):
        print("\n" + "!"*60)
        print("🎵 GENERATING MUSIC")
        gen_music.process_queue(config["music"], output_dir / "generated_music", manifest)
        
    # 6. Graphics
    if "graphics" in config and (not selected_mode or "graphics" in selection):
        print("\n" + "!"*60)
        print("📊 GENERATING GRAPHICS")
        gen_graphics.process_queue(config["graphics"], output_dir / "generated_graphics", manifest)

    # 7. Diagrams
    if "diagrams" in config and (not selected_mode or "diagrams" in selection):
        print("\n" + "!"*60)
        print("📐 GENERATING DIAGRAMS")
        gen_diagrams.process_queue(config["diagrams"], output_dir / "generated_diagrams", manifest)
    
    # 7. Chapter Markers (Visuals)
    if marker_file.exists() and (not selected_mode or "chapter_markers" in selection):
        print("\n" + "!"*60)
        print("🔖 GENERATING CHAPTER MARKER IMAGES")
        gen_chapter_markers.generate_from_file(marker_file, output_dir / "generated_chapter_markers", manifest)
    
    # 8. Audio/Text Markers (from EDL)
    edl_file = input_dir / "source_edl.md"
    if not edl_file.exists() and not use_new_structure:
        # Legacy fallback
        edl_file = week_dir / "source_edl.md"
    
    if edl_file.exists() and (not selected_mode or "audio_markers" in selection):
        print("\n" + "!"*60)
        print("📝 GENERATING TEXT MARKERS FROM EDL")
        gen_audio.generate_chapter_markers(edl_file, output_dir / "generated_audio" / "chapter_markers.txt")

    # 9. Memory Palace
    if "memory_palace" in config and (not selected_mode or "memory_palace" in selection):
        print("\n" + "!"*60)
        print("🧠 GENERATING MEMORY PALACE ASSETS")
        gen_memory_palace.process_queue(config["memory_palace"], output_dir / "generated_memory_palace", manifest)

    # Save the unified manifest
    manifest.save_manifest()
    
    print("\n" + "="*60)
    print("✅ MASTER GENERATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()

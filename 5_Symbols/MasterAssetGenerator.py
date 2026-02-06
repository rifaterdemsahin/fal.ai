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

# Add the current directory to path so we can import local modules
sys.path.append(str(Path(__file__).parent))

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
    """Load the assets configuration from JSON"""
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return {}
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return {}

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
    parser = argparse.ArgumentParser(description="Master Asset Generator for a video project week")
    parser.add_argument("week_dir", type=str, help="Path to the weekly video folder (e.g., ../3_Simulation/Feb1Youtube)")
    args = parser.parse_args()

    # Resolve paths
    week_dir = Path(args.week_dir).resolve()
    if not week_dir.exists():
        print(f"❌ Directory not found: {week_dir}")
        return

    print(f"\n🎬 MASTER GENERATOR: {week_dir.name}")
    print(f"   Path: {week_dir}")
    
    # Check for config
    config_file = week_dir / "assets_config.json"
    if not config_file.exists():
        print(f"⚠️  No 'assets_config.json' found in {week_dir}. Please create it first.")
        # Optional: could check for source_edl.md and propose to generate config, but let's stick to config
        return

    # Load Config
    config = load_config(config_file)
    if not config:
        return

    # Check for text marker file (for chapter markers generator)
    marker_file = week_dir / "source_chapter_markers.txt"
    if not marker_file.exists():
        # fallback
        marker_file = week_dir / "chapter_markers.txt"

    # Estimate Cost
    gen_cost.generate_report(week_dir)
    
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
    manifest = ManifestTracker(week_dir)
    print(f"\n📋 Manifest tracking initialized")
    
    # Execute Generators
    # 1. Images
    if "images" in config and (not selected_mode or "images" in selection):
        print("\n" + "!"*60)
        print("🖼️  GENERATING IMAGES")
        gen_images.process_queue(config["images"], week_dir / "generated_assets_Images", manifest)

    # 2. Lower Thirds
    if "lower_thirds" in config and (not selected_mode or "lower_thirds" in selection):
        print("\n" + "!"*60)
        print("📺 GENERATING LOWER THIRDS")
        gen_lower_thirds.process_queue(config["lower_thirds"], week_dir / "generated_assets_lowerthirds", manifest)
    
    # 3. Icons
    if "icons" in config and (not selected_mode or "icons" in selection):
        print("\n" + "!"*60)
        print("🔹 GENERATING ICONS")
        gen_icons.process_queue(config["icons"], week_dir / "generated_icons", manifest)
        
    # 4. Video
    if "video" in config and (not selected_mode or "video" in selection):
        print("\n" + "!"*60)
        print("🎥 GENERATING VIDEO CLIPS")
        gen_video.process_queue(config["video"], week_dir / "generated_video", manifest)

    # 5. Music
    if "music" in config and (not selected_mode or "music" in selection):
        print("\n" + "!"*60)
        print("🎵 GENERATING MUSIC")
        gen_music.process_queue(config["music"], week_dir / "generated_music", manifest)
        
    # 6. Graphics
    if "graphics" in config and (not selected_mode or "graphics" in selection):
        print("\n" + "!"*60)
        print("📊 GENERATING GRAPHICS")
        gen_graphics.process_queue(config["graphics"], week_dir / "generated_graphics", manifest)

    # 7. Diagrams
    if "diagrams" in config and (not selected_mode or "diagrams" in selection):
        print("\n" + "!"*60)
        print("📐 GENERATING DIAGRAMS")
        gen_diagrams.process_queue(config["diagrams"], week_dir / "generated_diagrams", manifest)
    
    # 7. Chapter Markers (Visuals)
    if marker_file.exists() and (not selected_mode or "chapter_markers" in selection):
        print("\n" + "!"*60)
        print("🔖 GENERATING CHAPTER MARKER IMAGES")
        gen_chapter_markers.generate_from_file(marker_file, week_dir / "generated_chapter_markers", manifest)
    
    # 8. Audio/Text Markers (from EDL)
    edl_file = week_dir / "source_edl.md"
    if edl_file.exists() and (not selected_mode or "audio_markers" in selection):
        print("\n" + "!"*60)
        print("📝 GENERATING TEXT MARKERS FROM EDL")
        gen_audio.generate_chapter_markers(edl_file, week_dir / "generated_audio" / "chapter_markers.txt")

    # 9. Memory Palace
    if "memory_palace" in config and (not selected_mode or "memory_palace" in selection):
        print("\n" + "!"*60)
        print("🧠 GENERATING MEMORY PALACE ASSETS")
        gen_memory_palace.process_queue(config["memory_palace"], week_dir / "generated_memory_palace", manifest)

    # Save the unified manifest
    manifest.save_manifest()
    
    print("\n" + "="*60)
    print("✅ MASTER GENERATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator for Chapter Markers
Project: The Agentic Era - Managing 240+ Workflows
Generates title cards/images for video chapters based on `chapter_markers.txt`
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Install: pip install fal-client
try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

# Configuration
OUTPUT_DIR = Path("./generated_chapter_markers")
OUTPUT_DIR.mkdir(exist_ok=True)
CHAPTER_MARKERS_FILE = Path("./chapter_markers.txt")

# Consistency seeds
SEEDS = {
    "SEED_CHAPTERS": 999001,  # Consistent style for all chapters
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

def read_chapter_markers(file_path: Path) -> List[Tuple[str, str]]:
    """
    Parses the chapter markers file.
    Expected format: "00:00 Hook & Problem Statement"
    Returns a list of (timestamp, title) tuples.
    """
    if not file_path.exists():
        print(f"❌ Chapter markers file not found: {file_path}")
        return []

    markers = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Regex to separate timestamp and title
            # Matches "00:00 Title" or "1:00:00 Title"
            match = re.match(r'^(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)$', line)
            if match:
                timestamp = match.group(1)
                title = match.group(2)
                markers.append((timestamp, title))
            else:
                print(f"⚠️ Could not parse line: {line}")
    return markers

def build_generation_queue(markers: List[Tuple[str, str]]) -> List[Dict]:
    """Builds the asset generation queue from chapter markers."""
    queue = []
    for i, (timestamp, title) in enumerate(markers, 1):
        # Create a safe filename from the title
        safe_title = re.sub(r'[^a-z0-9]', '_', title.lower()).strip('_')
        safe_title = re.sub(r'_+', '_', safe_title)  # Collapse multiple underscores
        
        asset_id = f"CH_{i:02d}"
        
        # Construct the prompt
        # We want a consistent style: Title text, tech background, brand colors
        prompt = (
            f"Cinematic video chapter title card with text '{title}' written in large, bold, futuristic sans-serif font centered. "
            f"Background is a sleek, modern tech abstract design with deep dark blue ({BRAND_COLORS['primary_dark']}) "
            f"and glowing accents in cyan ({BRAND_COLORS['accent_blue']}) and purple ({BRAND_COLORS['accent_purple']}). "
            "High contrast, professional motion graphics style, 8k resolution, highly detailed, "
            "digital interface elements, subtle grid patterns, glassmorphism effects. "
            "Text must be clearly legible and the focal point."
        )

        queue.append({
            "id": asset_id,
            "name": f"chapter_{i:02d}_{safe_title}",
            "priority": "HIGH",
            "scene": f"Chapter {i}: {title} ({timestamp})",
            "seed_key": "SEED_CHAPTERS",
            "prompt": prompt,
            "model": "fal-ai/flux/dev",  # Using dev for better text rendering
            "image_size": {"width": 1920, "height": 1080},
            "num_inference_steps": 28,
            "timestamp": timestamp,
            "original_title": title
        })
    return queue

def generate_asset(asset_config: Dict) -> Dict:
    """Generate a single asset using fal.ai"""
    print(f"\n{'='*60}")
    print(f"🎨 Generating: {asset_config['name']}")
    print(f"   Chapter: {asset_config['scene']}")
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
            
            # Save metadata
            output_path = OUTPUT_DIR / f"{asset_config['name']}.json"
            metadata = {
                **asset_config,
                "result_url": image_url,
                "seed_value": SEEDS[asset_config["seed_key"]],
            }
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Metadata saved: {output_path}")
            
            # Download image
            import urllib.request
            image_path = OUTPUT_DIR / f"{asset_config['name']}.png"
            urllib.request.urlretrieve(image_url, image_path)
            print(f"💾 Image saved: {image_path}")
            
            return {
                "success": True,
                "url": image_url,
                "local_path": str(image_path),
            }
        else:
            print(f"❌ Generation failed: No images in result")
            return {"success": False, "error": "No images returned"}
            
    except Exception as e:
        print(f"❌ Error generating asset: {str(e)}")
        return {"success": False, "error": str(e)}


def main():
    """Main execution"""
    print("\n" + "="*60)
    print("🚀 FAL.AI BATCH CHAPTER MARKER GENERATOR")
    print("   Project: The Agentic Era - Chapter Assets")
    print("="*60)
    
    # Check API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("\n❌ ERROR: FAL_KEY environment variable not set")
        print("   Set it with: export FAL_KEY='your-api-key-here'")
        print("   Get your key from: https://fal.ai/dashboard/keys")
        return
    
    print(f"\n✅ API Key found")
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}")
    print(f"📄 Reading markers from: {CHAPTER_MARKERS_FILE.absolute()}")
    
    markers = read_chapter_markers(CHAPTER_MARKERS_FILE)
    if not markers:
        print("❌ No markers found or file is empty.")
        return

    generation_queue = build_generation_queue(markers)
    print(f"\n📊 Assets to generate: {len(generation_queue)}")
    
    for item in generation_queue:
        print(f"   • {item['timestamp']} - {item['original_title']}")

    # Confirm before proceeding
    print("\n" + "="*60)
    response = input("🤔 Proceed with generation? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled by user")
        return
    
    # Generate assets
    results = []
    for i, asset in enumerate(generation_queue, 1):
        print(f"\n\n{'#'*60}")
        print(f"# Asset {i}/{len(generation_queue)}")
        print(f"{'#'*60}")
        
        result = generate_asset(asset)
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
    summary_path = OUTPUT_DIR / "generation_summary.json"
    with open(summary_path, 'w') as f:
        json.dump({
            "total": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "results": results,
        }, f, indent=2)
    
    print(f"\n💾 Summary saved: {summary_path}")
    print("\n✅ Done!")


if __name__ == "__main__":
    main()

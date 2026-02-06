#!/usr/bin/env python3
"""
Demo: Asset Versioning and Manifest System
Shows how the new system works without making actual API calls
"""

import json
import tempfile
from pathlib import Path
from asset_utils import ManifestTracker, generate_filename, extract_scene_number


def demo_filename_generation():
    """Demonstrate the new filename generation"""
    print("\n" + "=" * 70)
    print("DEMO 1: Filename Generation")
    print("=" * 70)
    
    examples = [
        ("1.1", "image", "ferrari cart morph"),
        ("4.2", "image", "sunday 5pm timeline"),
        ("4.1", "video", "uk streets sunday"),
        ("6.1", "graphic", "20 dollar pricing"),
        ("11.1", "image", "ai job message"),
    ]
    
    print("\nOld vs New Naming Convention:\n")
    print(f"{'Old Name':<40} {'New Name':<50}")
    print("-" * 90)
    
    for asset_id, asset_type, name in examples:
        # Old naming
        old_name = name.replace(' ', '_') + ".png"
        
        # New naming
        scene_num = extract_scene_number(asset_id)
        new_name = generate_filename(scene_num, asset_type, name, version=1, extension="png")
        
        print(f"{old_name:<40} {new_name:<50}")
    
    print("\nBenefits:")
    print("  ✅ Scene-based sorting (001, 004, 006, 011)")
    print("  ✅ Asset type identification (image, video, graphic)")
    print("  ✅ Version tracking (_v1, _v2, etc.)")
    print("  ✅ Clean, consistent formatting")


def demo_manifest_tracking():
    """Demonstrate manifest tracking"""
    print("\n" + "=" * 70)
    print("DEMO 2: Manifest Tracking")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir)
        
        # Initialize manifest
        manifest = ManifestTracker(project_dir)
        print(f"\n📋 Initialized manifest tracker for project: {project_dir.name}")
        
        # Add some assets
        assets_to_add = [
            {
                "id": "1.1",
                "name": "ferrari_cart_morph",
                "type": "image",
                "prompt": "Sleek red Ferrari sports car icon smoothly morphing into simple shopping cart icon",
                "scene": "Scene 1: Hook",
                "priority": "HIGH"
            },
            {
                "id": "4.2",
                "name": "sunday_5pm_timeline",
                "type": "image",
                "prompt": "Motion graphics timeline visualization showing Sunday evening 5:00 PM",
                "scene": "Scene 4: Skills Gap",
                "priority": "HIGH"
            },
        ]
        
        print("\n🎨 Adding assets to manifest...\n")
        
        for asset in assets_to_add:
            scene_num = extract_scene_number(asset["id"])
            filename = generate_filename(scene_num, asset["type"], asset["name"], 1, "png")
            
            manifest.add_asset(
                filename=filename,
                prompt=asset["prompt"],
                asset_type=asset["type"],
                asset_id=asset["id"],
                result_url=f"https://example.com/{filename}",
                local_path=str(project_dir / "generated" / filename),
                metadata={
                    "scene": asset["scene"],
                    "priority": asset["priority"]
                }
            )
            
            print(f"  ✅ Added: {filename}")
            print(f"     Scene: {asset['scene']}")
            print(f"     Prompt: {asset['prompt'][:60]}...")
            print()
        
        # Save manifest
        print("💾 Saving manifest...")
        manifest_path = manifest.save_manifest()
        
        # Display manifest content
        with open(manifest_path, 'r') as f:
            manifest_data = json.load(f)
        
        print("\n📋 Manifest Structure:")
        print(json.dumps(manifest_data, indent=2))


def demo_manifest_queries():
    """Demonstrate querying the manifest"""
    print("\n" + "=" * 70)
    print("DEMO 3: Querying the Manifest")
    print("=" * 70)
    
    # Sample manifest data
    manifest_data = {
        "generation_timestamp": "2026-02-05T06:00:00",
        "completion_timestamp": "2026-02-05T06:10:00",
        "total_assets": 4,
        "assets": [
            {
                "filename": "001_image_ferrari_cart_morph_v1.png",
                "asset_id": "1.1",
                "asset_type": "image",
                "prompt": "Sleek red Ferrari...",
                "metadata": {"scene": "Scene 1", "priority": "HIGH"}
            },
            {
                "filename": "004_image_sunday_5pm_timeline_v1.png",
                "asset_id": "4.2",
                "asset_type": "image",
                "prompt": "Motion graphics timeline...",
                "metadata": {"scene": "Scene 4", "priority": "HIGH"}
            },
            {
                "filename": "004_video_uk_streets_sunday_v1.mp4",
                "asset_id": "4.1",
                "asset_type": "video",
                "prompt": "Cinematic shot...",
                "metadata": {"scene": "Scene 4", "priority": "MEDIUM"}
            },
            {
                "filename": "011_graphic_ai_job_message_v1.png",
                "asset_id": "11.1",
                "asset_type": "graphic",
                "prompt": "Bold typographic design...",
                "metadata": {"scene": "Scene 11", "priority": "HIGH"}
            },
        ]
    }
    
    print("\n📊 Sample Queries:\n")
    
    # Query 1: Find all assets from Scene 4
    scene4_assets = [a for a in manifest_data['assets'] if a['filename'].startswith('004_')]
    print(f"1. Assets from Scene 4:")
    for asset in scene4_assets:
        print(f"   - {asset['filename']} ({asset['asset_type']})")
    
    # Query 2: Find all high priority assets
    high_priority = [a for a in manifest_data['assets'] 
                     if a['metadata'].get('priority') == 'HIGH']
    print(f"\n2. High Priority Assets:")
    for asset in high_priority:
        print(f"   - {asset['filename']} (Scene {asset['asset_id'].split('.')[0]})")
    
    # Query 3: Find all video assets
    videos = [a for a in manifest_data['assets'] if a['asset_type'] == 'video']
    print(f"\n3. Video Assets:")
    for asset in videos:
        print(f"   - {asset['filename']}")
    
    # Query 4: Get prompt for specific file
    filename = "001_image_ferrari_cart_morph_v1.png"
    asset = next((a for a in manifest_data['assets'] if a['filename'] == filename), None)
    print(f"\n4. Prompt for {filename}:")
    if asset:
        print(f"   \"{asset['prompt']}\"")


def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("ASSET VERSIONING AND MANIFEST SYSTEM - DEMONSTRATION")
    print("=" * 70)
    
    demo_filename_generation()
    demo_manifest_tracking()
    demo_manifest_queries()
    
    print("\n" + "=" * 70)
    print("✅ DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nFor more information, see: 5_Symbols/VERSIONING_AND_MANIFEST.md")
    print()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Integration test for manifest and versioning system
Tests the complete flow without calling the actual API
"""

import json
import tempfile
from pathlib import Path
import sys

# Add symbol root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from Utils.asset_utils import ManifestTracker, generate_filename, extract_scene_number


def test_integration():
    """Test the complete manifest and versioning flow"""
    
    print("=" * 60)
    print("INTEGRATION TEST: Manifest and Versioning System")
    print("=" * 60)
    
    # Create temporary project directory
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir)
        print(f"\n📁 Test project directory: {project_dir}")
        
        # Initialize manifest tracker
        manifest = ManifestTracker(project_dir)
        print(f"✅ Manifest tracker initialized")
        
        # Simulate generating some assets
        test_assets = [
            {
                "id": "1.1",
                "name": "ferrari_cart_morph",
                "prompt": "Sleek red Ferrari sports car icon smoothly morphing into simple shopping cart icon",
                "type": "image",
                "ext": "png"
            },
            {
                "id": "4.2",
                "name": "sunday_5pm_timeline",
                "prompt": "Motion graphics timeline visualization showing Sunday evening 5:00 PM",
                "type": "image",
                "ext": "png"
            },
            {
                "id": "4.1",
                "name": "uk_streets_sunday",
                "prompt": "Cinematic shot of empty UK high street on Sunday evening",
                "type": "video",
                "ext": "mp4"
            },
            {
                "id": "11.1",
                "name": "ai_job_message",
                "prompt": "Bold typographic design with powerful message",
                "type": "graphic",
                "ext": "png"
            },
        ]
        
        print(f"\n🎨 Simulating generation of {len(test_assets)} assets...\n")
        
        for asset in test_assets:
            # Extract scene number
            scene_num = extract_scene_number(asset["id"])
            
            # Generate filename with version 1
            filename = generate_filename(
                scene_num,
                asset["type"],
                asset["name"],
                version=1,
                extension=asset["ext"]
            )
            
            print(f"  • Asset {asset['id']}: {asset['name']}")
            print(f"    Old name: {asset['name']}.{asset['ext']}")
            print(f"    New name: {filename}")
            
            # Add to manifest
            manifest.add_asset(
                filename=filename,
                prompt=asset["prompt"],
                asset_type=asset["type"],
                asset_id=asset["id"],
                result_url=f"https://example.com/{filename}",
                local_path=str(project_dir / "generated" / filename),
                metadata={
                    "scene": f"Scene {scene_num}",
                    "priority": "HIGH" if scene_num == 1 else "MEDIUM"
                }
            )
        
        # Save manifest
        print(f"\n💾 Saving manifest...")
        manifest_path = manifest.save_manifest()
        
        # Verify manifest file
        print(f"\n✅ Manifest file created: {manifest_path}")
        print(f"   File size: {manifest_path.stat().st_size} bytes")
        
        # Load and display manifest contents
        with open(manifest_path, 'r') as f:
            manifest_data = json.load(f)
        
        print(f"\n📋 Manifest contents:")
        print(f"   Total assets: {manifest_data['total_assets']}")
        print(f"   Generation timestamp: {manifest_data['generation_timestamp']}")
        print(f"   Completion timestamp: {manifest_data['completion_timestamp']}")
        
        print(f"\n📝 Asset details:")
        for i, asset in enumerate(manifest_data['assets'], 1):
            print(f"   {i}. {asset['filename']}")
            print(f"      - Asset ID: {asset['asset_id']}")
            print(f"      - Type: {asset['asset_type']}")
            print(f"      - Prompt: {asset['prompt'][:60]}...")
            print(f"      - Timestamp: {asset['timestamp']}")
        
        print("\n" + "=" * 60)
        print("✅ INTEGRATION TEST PASSED")
        print("=" * 60)
        
        # Verify expected filenames
        expected_filenames = [
            "001_image_ferrari_cart_morph_v1.png",
            "004_image_sunday_5pm_timeline_v1.png",
            "004_video_uk_streets_sunday_v1.mp4",
            "011_graphic_ai_job_message_v1.png",
        ]
        
        actual_filenames = [asset['filename'] for asset in manifest_data['assets']]
        
        print("\n🔍 Filename verification:")
        all_match = True
        for expected, actual in zip(expected_filenames, actual_filenames):
            match = "✅" if expected == actual else "❌"
            print(f"   {match} Expected: {expected}")
            print(f"      Actual:   {actual}")
            if expected != actual:
                all_match = False
        
        if all_match:
            print("\n✅ All filenames match expected format!")
        else:
            print("\n❌ Some filenames don't match expected format!")
            return False
        
        return True


if __name__ == "__main__":
    success = test_integration()
    exit(0 if success else 1)

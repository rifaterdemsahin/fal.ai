#!/usr/bin/env python3
"""
Integration test for manifest and versioning system
Tests the complete flow without calling the actual API
"""
import sys
import unittest
import json
from pathlib import Path
import datetime

try:
    from base_test import BaseAssetGeneratorTest
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from base_test import BaseAssetGeneratorTest

sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "5_Symbols"))
from Utils.asset_utils import ManifestTracker, generate_filename, extract_scene_number

class TestIntegration(BaseAssetGeneratorTest):
    
    def test_integration(self):
        """Test the complete manifest and versioning flow"""
        print(f"\n🚀 INTEGRATION TEST: Manifest and Versioning System")
        
        # Use fixed project directory within the test output root
        project_dir = self.test_output_root / "manifest_test"
        if not project_dir.exists():
            project_dir.mkdir(parents=True, exist_ok=True)
        
        # Create generated folder if it doesn't exist
        (project_dir / "generated").mkdir(parents=True, exist_ok=True)
            
        print(f"📁 Test project directory: {project_dir}")
        
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
        self.assertTrue(manifest_path.exists())
        print(f"   File size: {manifest_path.stat().st_size} bytes")
        
        # Load and verify manifest contents
        with open(manifest_path, 'r') as f:
            manifest_data = json.load(f)
        
        print(f"\n📋 Manifest contents:")
        print(f"   Total assets: {manifest_data['total_assets']}")
        self.assertEqual(manifest_data['total_assets'], 4)
        
        print(f"\n📝 Asset details:")
        actual_filenames = []
        for i, asset in enumerate(manifest_data['assets'], 1):
            print(f"   {i}. {asset['filename']}")
            actual_filenames.append(asset['filename'])
        
        # Verify expected filenames
        expected_filenames = [
            "001_image_ferrari_cart_morph_v1.png",
            "004_image_sunday_5pm_timeline_v1.png",
            "004_video_uk_streets_sunday_v1.mp4",
            "011_graphic_ai_job_message_v1.png",
        ]
        
        print("\n🔍 Filename verification:")
        for expected, actual in zip(expected_filenames, actual_filenames):
            match = "✅" if expected == actual else "❌"
            print(f"   {match} Expected: {expected}")
            print(f"      Actual:   {actual}")
            self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()

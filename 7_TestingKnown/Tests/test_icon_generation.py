#!/usr/bin/env python3
"""
Test script for Icon Generator with fal.ai integration.

This script validates the BatchAssetGeneratorIcons module by running
a single test icon and verifying the output.
"""
import sys
import unittest
import os
from pathlib import Path
from typing import Dict, List, Any
import datetime

# Add the Tests directory to sys.path to allow importing base_test
sys.path.append(str(Path(__file__).resolve().parent))

try:
    from dotenv import load_dotenv
    # Load .env from 5_Symbols explicitly
    env_path = Path(__file__).resolve().parent.parent.parent / "5_Symbols" / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        print(f"Warning: .env not found at {env_path}")
except ImportError:
    print("Warning: python-dotenv not installed. Skipping .env load.")
    # Attempt to load manually if simple format
    env_path = Path(__file__).resolve().parent.parent.parent / "5_Symbols" / ".env"
    if env_path.exists():
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'): continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        os.environ[key] = value
            print("Loaded .env manually.")
        except Exception as e:
            print(f"Error manually loading .env: {e}")

try:
    from base_test import BaseAssetGeneratorTest
except ImportError:
    # If adding to path didn't work (e.g. if running from a different working dir), 
    # try direct import if possible or fail gracefully
    try:
        from Tests.base_test import BaseAssetGeneratorTest
    except ImportError:
         print("Error: Could not import BaseAssetGeneratorTest. Make sure you are running from the project root or the Tests directory.")
         sys.exit(1)

class TestIconGeneration(BaseAssetGeneratorTest):
    
    def setUp(self):
        super().setUp()
        self.output_dir = self.test_output_root / "icons"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def import_generator(self):
        try:
            # BaseAssetGeneratorTest adds 5_Symbols to sys.path
            from Images import BatchAssetGeneratorIcons
            return BatchAssetGeneratorIcons
        except ImportError as e:
            self.fail(f"Failed to load BatchAssetGeneratorIcons: {e}\nVerify module exists in 5_Symbols/Images/")

    def create_test_batch(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "TEST_ICON_001",
                "name": "test_icon_simple",
                "priority": "HIGH",
                "scene": "Test Scene",
                "seed_key": "SEED_003", # Using a key that exists in SEEDS dict in the generator
                "prompt": (
                    "Simple test icon, minimalist circle, "
                    "blue color, white background, "
                    "vector style"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1024, "height": 1024},
                "num_inference_steps": 20, # Reduced steps for speed if possible, though model might ignore
            }
        ]

    def test_icon_generation(self):
        print(f"\n🚀 Icon Generator Test Suite")
        
        if not self.verify_environment():
            return
        
        generator = self.import_generator()
        test_batch = self.create_test_batch()
        
        # Add timestamp to filenames to avoid collisions
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        for item in test_batch:
            item["name"] = f"{item['name']}_{timestamp}"

        print(f"🧪 Test Batch: {len(test_batch)} icon(s)")
        print(f"📂 Output: {self.output_dir}")
        
        if "GOOGLE_API_KEY" in os.environ and "GEMINI_API_KEY" not in os.environ:
             print("ℹ️  Mapping GOOGLE_API_KEY to GEMINI_API_KEY for test.")
             os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]

        try:
            # Access SEEDS from generator to ensure our seed_key is valid or just pass it
            # The generator's process_queue expects a list of dicts.
            
            print("⏳ Generating assets...")
            # process_queue(queue: List[Dict], output_dir: Path, manifest: Optional[object] = None, provider: str = "auto")
            generator.process_queue(test_batch, self.output_dir, provider="auto")
            
            # Verify output
            generated = self.assertFilesGenerated(self.output_dir, [".png", ".jpg", ".jpeg"], min_count=1)
            
            print("\n" + "=" * 70)
            print("✅ TEST COMPLETE")
            print("=" * 70)
            print(f"\n📄 Generated Files:")
            for f in generated:
                # Check for the specific test file we just generated
                if timestamp in f.name:
                    size_kb = f.stat().st_size / 1024
                    print(f"   • {f.name:<40} ({size_kb:>8.1f} KB)")
                
        except Exception as e:
            self.fail(f"Generation Failed: {e}")

if __name__ == "__main__":
    unittest.main()

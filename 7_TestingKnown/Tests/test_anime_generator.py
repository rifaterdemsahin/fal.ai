#!/usr/bin/env python3
"""
Test script for Anime Generator - Validates functionality without API calls
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "5_Symbols"))

def test_anime_generator():
    """Test the anime generator without making API calls"""
    print("🧪 Testing Anime Generator")
    print("="*60)
    
    # Test 1: Import the module
    print("\n1️⃣ Testing module import...")
    try:
        from Images.BatchAssetGeneratorAnime import (
            load_storyline_from_file,
            DEFAULT_STORYLINE,
            ANIME_MODELS
        )
        print("   ✅ Module imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import: {e}")
        return False
    
    # Test 2: Check default storyline
    print("\n2️⃣ Testing default storyline...")
    try:
        assert "title" in DEFAULT_STORYLINE
        assert "scenes" in DEFAULT_STORYLINE
        assert len(DEFAULT_STORYLINE["scenes"]) > 0
        
        scene = DEFAULT_STORYLINE["scenes"][0]
        required_fields = ["id", "name", "scene", "description", "prompt"]
        for field in required_fields:
            assert field in scene, f"Missing required field: {field}"
        
        print(f"   ✅ Default storyline valid with {len(DEFAULT_STORYLINE['scenes'])} scenes")
        print(f"   📖 Title: {DEFAULT_STORYLINE['title']}")
    except AssertionError as e:
        print(f"   ❌ Default storyline validation failed: {e}")
        return False
    
    # Test 3: Check anime models
    print("\n3️⃣ Testing anime model definitions...")
    try:
        expected_models = ["minimax", "kling", "flux_anime", "flux_dev"]
        for model in expected_models:
            assert model in ANIME_MODELS, f"Missing model: {model}"
            assert ANIME_MODELS[model].startswith("fal-ai/"), f"Invalid model ID: {ANIME_MODELS[model]}"
        
        print(f"   ✅ All {len(ANIME_MODELS)} anime models defined correctly")
        for name, model_id in ANIME_MODELS.items():
            print(f"      • {name}: {model_id}")
    except AssertionError as e:
        print(f"   ❌ Model definitions invalid: {e}")
        return False
    
    # Test 4: Load example storyline
    print("\n4️⃣ Testing storyline loading...")
    try:
        # Check if example exists
        example_path = Path("Images/example_anime_storyline.json")
        if not example_path.exists():
            print("   ⚠️  Example storyline not found (this is OK)")
        else:
            storyline = load_storyline_from_file(example_path)
            assert "title" in storyline
            assert "scenes" in storyline
            print(f"   ✅ Successfully loaded: {storyline['title']}")
            print(f"   📊 Scenes: {len(storyline['scenes'])}")
    except Exception as e:
        print(f"   ❌ Failed to load storyline: {e}")
        return False
    
    # Test 5: Validate anime_storyline.json in 3_Simulation
    print("\n5️⃣ Testing provided anime_storyline.json...")
    try:
        storyline_path = Path("../3_Simulation/Feb1Youtube/anime_storyline.json")
        if storyline_path.exists():
            with open(storyline_path, 'r') as f:
                storyline = json.load(f)
            
            assert "title" in storyline
            assert "scenes" in storyline
            assert len(storyline["scenes"]) > 0
            
            # Validate each scene has required fields
            for i, scene in enumerate(storyline["scenes"]):
                required = ["id", "name", "scene", "description", "prompt"]
                for field in required:
                    assert field in scene, f"Scene {i} missing: {field}"
            
            print(f"   ✅ Storyline validated: {storyline['title']}")
            print(f"   📊 Total scenes: {len(storyline['scenes'])}")
            print(f"   🎬 Estimated runtime: {len(storyline['scenes']) * 5} seconds")
            
            # Count by priority
            high = sum(1 for s in storyline["scenes"] if s.get("priority") == "HIGH")
            medium = sum(1 for s in storyline["scenes"] if s.get("priority") == "MEDIUM")
            low = sum(1 for s in storyline["scenes"] if s.get("priority") == "LOW")
            print(f"   📊 Priorities: HIGH={high}, MEDIUM={medium}, LOW={low}")
        else:
            print("   ⚠️  anime_storyline.json not found in expected location")
    except Exception as e:
        print(f"   ❌ Failed to validate storyline: {e}")
        return False
    
    # Test 6: Check file naming convention
    print("\n6️⃣ Testing filename generation...")
    try:
        from Utils.asset_utils import generate_filename, extract_scene_number
        
        # Test scene number extraction
        scene_num = extract_scene_number("1.1")
        assert scene_num == 1, f"Expected 1, got {scene_num}"
        
        scene_num = extract_scene_number("10.5")
        assert scene_num == 10, f"Expected 10, got {scene_num}"
        
        # Test filename generation
        filename = generate_filename(1, "anime", "hero_awakening", 1)
        assert filename.startswith("001_anime_"), f"Unexpected filename: {filename}"
        assert "hero_awakening" in filename
        assert filename.endswith("_v1")
        
        print(f"   ✅ Filename generation working correctly")
        print(f"   📝 Example: {filename}.mp4")
    except Exception as e:
        print(f"   ❌ Filename generation failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("✅ All tests passed!")
    print("🎌 Anime Generator is ready to use")
    print("\n💡 To generate anime:")
    print("   1. Set your FAL_KEY environment variable")
    print("   2. Run: python Images/BatchAssetGeneratorAnime.py --storyline path/to/storyline.json")
    return True


if __name__ == "__main__":
    success = test_anime_generator()
    sys.exit(0 if success else 1)

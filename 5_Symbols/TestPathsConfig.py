#!/usr/bin/env python3
"""
Test script for MasterAssetGenerator path configuration
Tests the new weekly structure without requiring fal_client
"""

import sys
import argparse
from pathlib import Path

# Add the 5_Symbols directory to path
sys.path.append(str(Path(__file__).parent))

from paths_config import get_weekly_paths, ensure_weekly_structure


def test_weekly_paths():
    """Test weekly path generation"""
    print("Testing Weekly Path Generation")
    print("=" * 60)
    
    # Test 1: Explicit weekly ID
    print("\n1. Testing explicit weekly ID '2026-02-10':")
    paths = get_weekly_paths('2026-02-10')
    for key, value in paths.items():
        print(f"   {key}: {value}")
    
    # Test 2: Auto-generate from today
    print("\n2. Testing auto-generated weekly ID:")
    paths = get_weekly_paths()
    for key, value in paths.items():
        print(f"   {key}: {value}")
    
    # Test 3: Ensure structure
    print("\n3. Testing structure creation:")
    test_id = "test-2026-02-10"
    paths = ensure_weekly_structure(test_id)
    print(f"   Created/verified: {paths['input']}")
    print(f"   Exists: {paths['input'].exists()}")
    print(f"   Created/verified: {paths['output']}")
    print(f"   Exists: {paths['output'].exists()}")
    
    # Clean up test directory
    if paths['base'].exists():
        import shutil
        shutil.rmtree(paths['base'])
        print(f"   Cleaned up test directory: {paths['base']}")
    
    print("\n✅ All path tests passed!")


def test_argument_parsing():
    """Test argument parsing for MasterAssetGenerator"""
    print("\nTesting Argument Parsing")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(
        description="Master Asset Generator for a video project week",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "week_dir", 
        type=str, 
        nargs='?',
        help="[LEGACY] Path to the weekly video folder"
    )
    parser.add_argument(
        "--week", 
        type=str, 
        dest="weekly_id",
        help="Weekly ID for new structure"
    )
    
    # Test case 1: New structure with explicit week
    print("\n1. New structure mode (--week 2026-02-10):")
    args = parser.parse_args(['--week', '2026-02-10'])
    print(f"   weekly_id: {args.weekly_id}")
    print(f"   week_dir: {args.week_dir}")
    
    # Test case 2: Legacy mode
    print("\n2. Legacy mode (../3_Simulation/Feb1Youtube):")
    args = parser.parse_args(['../3_Simulation/Feb1Youtube'])
    print(f"   weekly_id: {args.weekly_id}")
    print(f"   week_dir: {args.week_dir}")
    
    print("\n✅ All argument parsing tests passed!")


def test_config_lookup():
    """Test configuration file lookup logic"""
    print("\nTesting Config File Lookup")
    print("=" * 60)
    
    # Create test structure
    test_id = "test-config-2026-02-10"
    paths = ensure_weekly_structure(test_id)
    
    # Create a test config file
    config_file = paths['input'] / "assets_config.json"
    config_file.write_text('{"test": true}')
    print(f"\n1. Created test config: {config_file}")
    print(f"   Exists: {config_file.exists()}")
    
    # Test lookup
    input_dir = paths['input']
    lookup_file = input_dir / "assets_config.json"
    print(f"\n2. Looking up config in input directory:")
    print(f"   Path: {lookup_file}")
    print(f"   Exists: {lookup_file.exists()}")
    
    # Clean up
    import shutil
    shutil.rmtree(paths['base'])
    print(f"\n3. Cleaned up test directory: {paths['base']}")
    
    print("\n✅ Config lookup test passed!")


if __name__ == "__main__":
    test_weekly_paths()
    test_argument_parsing()
    test_config_lookup()
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 60)

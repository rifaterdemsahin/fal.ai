#!/usr/bin/env python3
"""
Test: Demonstrates automatic cost skipping
Run this to see how expensive generations are automatically skipped
"""

import sys
from pathlib import Path

# Add 5_Symbols/base to path
sys.path.insert(0, str(Path(__file__).parent / "5_Symbols" / "base"))

from generator_config import check_generation_cost

def test_auto_skip():
    """Test the automatic cost skipping behavior"""
    print("=" * 70)
    print("AUTOMATIC COST SKIPPING TEST")
    print("=" * 70)
    print("\nThis test demonstrates automatic skipping of expensive assets (>$0.20).\n")
    
    # Test with an expensive model
    print("Testing with: fal-ai/minimax/video-01 ($0.50)")
    print("-" * 70)
    
    result = check_generation_cost("fal-ai/minimax/video-01")
    
    print("-" * 70)
    if result:
        print("\n✅ Generation would proceed")
    else:
        print("\n❌ Generation automatically skipped")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_auto_skip()

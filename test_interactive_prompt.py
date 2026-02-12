#!/usr/bin/env python3
"""
Manual Test: Demonstrates the interactive cost confirmation prompt
Run this to see how the prompt appears for expensive generations
"""

import sys
from pathlib import Path

# Add 5_Symbols/base to path
sys.path.insert(0, str(Path(__file__).parent / "5_Symbols" / "base"))

from generator_config import check_generation_cost

def test_interactive_prompt():
    """Test the interactive cost confirmation prompt"""
    print("=" * 70)
    print("INTERACTIVE COST CONFIRMATION TEST")
    print("=" * 70)
    print("\nThis test will show you the actual prompt that users see")
    print("when attempting to generate expensive assets (>$0.20).\n")
    
    # Test with an expensive model
    print("Testing with: fal-ai/minimax/video-01 ($0.50)")
    print("-" * 70)
    
    result = check_generation_cost("fal-ai/minimax/video-01")
    
    print("-" * 70)
    if result:
        print("\n✅ User confirmed - generation would proceed")
    else:
        print("\n❌ User cancelled - generation was stopped")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    test_interactive_prompt()

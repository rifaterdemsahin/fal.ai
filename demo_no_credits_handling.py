#!/usr/bin/env python3
"""
Demo: No-Credits Prompt Generation Feature
Shows how the system handles insufficient credits by generating and displaying prompts with costs
"""

import sys
from pathlib import Path

# Add 5_Symbols to path
repo_root = Path(__file__).resolve().parent
symbols_path = repo_root / "5_Symbols"
sys.path.insert(0, str(symbols_path))

from base.base_asset_generator import BaseAssetGenerator
from base.generator_config import SEEDS, BRAND_COLORS


class DemoImageGenerator(BaseAssetGenerator):
    """Demo image generator to showcase no-credits handling"""
    
    def get_generation_queue(self):
        """Return a sample queue of assets"""
        return [
            {
                "id": "1.0",
                "name": "futuristic_city",
                "prompt": "A futuristic cityscape with flying cars and neon lights",
                "scene": "1",
                "priority": "HIGH",
                "model": "fal-ai/flux/dev",
            },
            {
                "id": "2.0",
                "name": "nature_landscape",
                "prompt": "A serene mountain landscape at sunset with reflective lake",
                "scene": "2",
                "priority": "MEDIUM",
                "model": "fal-ai/flux/schnell",
            },
            {
                "id": "3.0",
                "name": "abstract_art",
                "prompt": "Abstract geometric patterns with vibrant colors",
                "scene": "3",
                "priority": "LOW",
                "model": "fal-ai/flux/dev",
            }
        ]


def demo_dry_run_mode():
    """Demonstrate dry-run mode"""
    print("\n" + "="*80)
    print("DEMO 1: DRY-RUN MODE")
    print("="*80)
    print("In this mode, the generator displays prompts and costs WITHOUT making API calls.")
    print("This is useful for:")
    print("  • Planning your generation batch")
    print("  • Estimating costs before running")
    print("  • Reviewing enhanced prompts")
    print()
    
    output_dir = repo_root / "7_TestingKnown" / "TestOutput" / "demo_dry_run"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generator = DemoImageGenerator(
        output_dir=output_dir,
        seeds=SEEDS,
        brand_colors=BRAND_COLORS,
        asset_type="image",
        dry_run=True  # Enable dry-run mode
    )
    
    # Manually process one asset to avoid API key check in process_queue
    asset = {
        "id": "1.0",
        "name": "futuristic_city",
        "prompt": "A futuristic cityscape with flying cars and neon lights",
        "scene": "1",
        "priority": "HIGH",
        "model": "fal-ai/flux/dev",
    }
    
    print("\n🎬 Starting dry-run generation...\n")
    result = generator.generate_asset(asset)
    
    print("\n📋 Result:")
    print(f"  Success: {result['success']}")
    print(f"  Dry-run: {result.get('dry_run', False)}")
    print(f"  Prompt: {result.get('prompt', 'N/A')}")
    print(f"  Cost: ${result.get('estimated_cost', 0):.2f}")
    print(f"  Model: {result.get('model', 'N/A')}")
    
    print("\n" + "="*80)
    print("✅ Dry-run completed!")
    print("Notice that:")
    print("  • Prompts were displayed with full details")
    print("  • Estimated costs were shown")
    print("  • No actual API calls were made")
    print("  • Results marked as 'dry_run: true'")
    print("="*80)


def demo_credits_exhausted():
    """Demonstrate behavior when credits are exhausted"""
    print("\n" + "="*80)
    print("DEMO 2: CREDITS EXHAUSTED SCENARIO")
    print("="*80)
    print("Simulating what happens when fal.ai credits run out during batch generation.")
    print("The system will:")
    print("  • Detect the credit error")
    print("  • Automatically switch to dry-run mode")
    print("  • Display prompts and costs for remaining assets")
    print("  • Provide a link to top up balance")
    print()
    
    output_dir = repo_root / "7_TestingKnown" / "TestOutput" / "demo_no_credits"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generator = DemoImageGenerator(
        output_dir=output_dir,
        seeds=SEEDS,
        brand_colors=BRAND_COLORS,
        asset_type="image"
    )
    
    # Simulate credits exhausted state
    print("🔴 Simulating: Credits exhausted after first asset...")
    generator.credits_exhausted = True
    
    # Process assets manually
    print("\n🎬 Processing queue with no credits...\n")
    
    assets = generator.get_generation_queue()
    for i, asset in enumerate(assets, 1):
        print(f"\n--- Asset {i}/{len(assets)} ---")
        result = generator.generate_asset(asset)
        print(f"\n📋 Result:")
        print(f"  Success: {result['success']}")
        print(f"  Error: {result.get('error', 'N/A')}")
        print(f"  Dry-run: {result.get('dry_run', False)}")
        print(f"  Cost: ${result.get('estimated_cost', 0):.2f}")
    
    print("\n" + "="*80)
    print("✅ Graceful handling completed!")
    print("Notice that:")
    print("  • System detected insufficient credits")
    print("  • Switched to prompt display mode")
    print("  • All prompts and costs were shown")
    print("  • Provided link to billing dashboard")
    print("="*80)


def demo_cost_estimation():
    """Demonstrate cost estimation for different models"""
    print("\n" + "="*80)
    print("DEMO 3: COST ESTIMATION")
    print("="*80)
    print("Shows estimated costs for different fal.ai models.")
    print()
    
    from base.generator_config import MODEL_PRICING
    
    print("💰 Model Pricing Information:")
    print("-" * 80)
    for model, cost in sorted(MODEL_PRICING.items(), key=lambda x: x[1], reverse=True):
        print(f"  {model:<50} ${cost:.2f}")
    print("-" * 80)
    
    print("\n📊 Quick Cost Estimation:")
    print("  • Generating 10 images with flux/dev:     $0.50")
    print("  • Generating 10 images with flux/schnell: $0.10")
    print("  • Generating 1 video with minimax:        $0.50")
    print("  • Generating 1 3D model:                  $0.45")
    print()
    print("💡 Tip: Use dry-run mode first to see exact costs before generation!")
    print("="*80)


def main():
    """Run all demos"""
    print("\n" + "="*80)
    print("🎭 NO-CREDITS HANDLING FEATURE DEMO")
    print("="*80)
    print()
    print("This demo showcases the new feature that handles insufficient fal.ai credits")
    print("by generating and displaying prompts with cost estimates instead of failing.")
    print()
    
    try:
        # Demo 1: Dry-run mode
        demo_dry_run_mode()
        
        input("\nPress Enter to continue to Demo 2...")
        
        # Demo 2: Credits exhausted
        demo_credits_exhausted()
        
        input("\nPress Enter to continue to Demo 3...")
        
        # Demo 3: Cost estimation
        demo_cost_estimation()
        
        print("\n" + "="*80)
        print("✅ ALL DEMOS COMPLETED!")
        print("="*80)
        print()
        print("Key Features:")
        print("  ✅ Automatic credit error detection")
        print("  ✅ Graceful fallback to dry-run mode")
        print("  ✅ Prompt and cost display without API calls")
        print("  ✅ Clear guidance to billing dashboard")
        print()
        print("Benefits:")
        print("  • Never lose track of what you wanted to generate")
        print("  • See enhanced prompts even without credits")
        print("  • Understand costs before topping up")
        print("  • Continue planning your content pipeline")
        print()
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(0)


if __name__ == "__main__":
    main()

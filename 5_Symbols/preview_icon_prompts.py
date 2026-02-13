#!/usr/bin/env python3
"""
Test script to enhance prompts for icons without generating images.
Useful for previewing how Gemini will enhance the prompts.
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Optional

# Add 5_Symbols (current directory) to sys.path
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

symbols_path = current_dir # For logging/reference
project_root = current_dir.parent
    
# Import styles and util
try:
    from Images.BatchAssetGeneratorIcons import BRAND_COLORS
    from Utils.prompt_enhancer import enhance_prompt
except ImportError:
    print("❌ Could not import required modules.")
    print(f"Ensure that {symbols_path} exists and contains Images and Utils packages.")
    sys.exit(1)

# Load environment variables for prompt enhancer
try:
    from dotenv import load_dotenv
    # Load .env from 5_Symbols explicitly
    env_path = current_dir / ".env"
    if env_path.exists():
        # Using string path for compatibility
        load_dotenv(str(env_path))
    else:
        print(f"Warning: .env not found at {env_path}")
        
    # Map GOOGLE_API_KEY to GEMINIKEY if needed by enhancer
    if "GOOGLE_API_KEY" in os.environ and "GEMINIKEY" not in os.environ:
         os.environ["GEMINIKEY"] = os.environ["GOOGLE_API_KEY"]
except ImportError:
    pass

# Fallback: Manual .env loading if GEMINIKEY is still missing
if "GEMINIKEY" not in os.environ and "GOOGLE_API_KEY" not in os.environ:
    env_path = project_root / "5_Symbols" / ".env"
    if env_path.exists():
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'): continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        os.environ[key] = value
        except Exception:
            pass

# Final check mapping
if "GOOGLE_API_KEY" in os.environ and "GEMINIKEY" not in os.environ:
    os.environ["GEMINIKEY"] = os.environ["GOOGLE_API_KEY"]

def load_icons(input_path: Path) -> List[Dict]:
    """Load icons from JSON file"""
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        return []
    
    try:
        with open(input_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading input file: {e}")
        return []

def process_prompts(icons: List[Dict], output_file: Path):
    """Enhance prompts for all icons and save to output file"""
    
    print(f"\n🚀 STARTING PROMPT ENHANCEMENT PREVIEW")
    print(f"   Input Icons: {len(icons)}")
    print(f"   Output File: {output_file}")
    print("="*60)

    # Construct color palette string
    color_palette = ", ".join([f"{k.replace('_', ' ').title()}: {v}" for k, v in BRAND_COLORS.items()])
    color_instruction = f" Use this consistent color palette: {color_palette}."
    
    enhanced_icons = []
    
    # Calculate costs
    total_cost_fal = 0.0
    
    # Try to import pricing
    try:
        from base.generator_config import MODEL_PRICING
    except ImportError:
        # Fallback pricing if import fails
        MODEL_PRICING = {
            "fal-ai/flux/dev": 0.05,
            "fal-ai/flux/schnell": 0.01,
        }

    for i, icon in enumerate(icons, 1):
        print(f"\n[{i}/{len(icons)}] Processing: {icon.get('name', 'Unknown')}")
        
        base_prompt = icon.get("prompt", "")
        model = icon.get("model", "fal-ai/flux/dev")
        cost = MODEL_PRICING.get(model, 0.0)
        total_cost_fal += cost
        
        if not base_prompt:
            print("   ⚠️ No prompt found, skipping")
            continue
            
        print(f"   📝 Original: {base_prompt[:60]}...")
        print(f"   💰 Est. Cost ({model}): ${cost:.3f}")
        
        # Prepare context for enhancer
        prompt_with_colors = base_prompt + color_instruction
        
        try:
            # Enhance prompt
            enhanced_prompt = enhance_prompt(prompt_with_colors, asset_type='icon')
            
            # Store result
            icon_copy = icon.copy()
            icon_copy['original_prompt'] = base_prompt
            icon_copy['enhanced_prompt'] = enhanced_prompt
            
            if enhanced_prompt != prompt_with_colors:
                print(f"   ✨ Enhanced: {enhanced_prompt[:60]}...")
            else:
                print(f"   ⚠️ Enhancement returned same prompt (or failed gracefully)")
                
            enhanced_icons.append(icon_copy)
            
        except Exception as e:
            print(f"   ❌ Error enhancing prompt: {e}")
            icon_copy = icon.copy()
            icon_copy['original_prompt'] = base_prompt
            icon_copy['enhanced_prompt'] = base_prompt + " (Enhancement Failed)"
            icon_copy['enhancement_error'] = str(e)
            enhanced_icons.append(icon_copy)

    # Save results
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(enhanced_icons, f, indent=2)
        
    print("\n" + "="*60)
    print(f"✅ Finished! Saved {len(enhanced_icons)} enhanced prompts to:")
    print(f"   {output_file}")
    print(f"💰 Total Estimated Cost (Fal): ${total_cost_fal:.3f}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Enhance prompts for icons using Gemini.")
    parser.add_argument("--input", "-i", type=Path, required=True, help="Input JSON file path containing icons")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Output JSON file path for enhanced prompts")
    
    args = parser.parse_args()
    
    input_file = args.input
    output_file = args.output
    
    icons = load_icons(input_file)
    if icons:
        process_prompts(icons, output_file)
    else:
        print("No icons to process.")

if __name__ == "__main__":
    main()

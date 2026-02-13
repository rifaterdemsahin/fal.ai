#!/usr/bin/env python3
"""
Script to execute generation of icons using enhanced prompts and Gemini provider.
Source: 7_TestingKnown/TestOutput/generated_icons/enhanced_prompts_preview.json
"""

import sys
import os
import json
from pathlib import Path

# Add project root to sys.path
# Add 5_Symbols (current directory) to sys.path
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

symbols_path = current_dir
project_root = current_dir.parent
# Helper to load .env manually and robustly
def load_env_robustly():
    env_path = symbols_path / ".env"
    if not env_path.exists():
        print(f"Warning: .env not found at {env_path}")
        return

    # Try python-dotenv first
    try:
        from dotenv import load_dotenv
        load_dotenv(str(env_path))
    except ImportError:
        pass

    # Fallback to manual parsing if keys are still missing
    # We specifically need GOOGLE_API_KEY or GEMINIKEY
    if "GOOGLE_API_KEY" not in os.environ and "GEMINIKEY" not in os.environ:
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
        except Exception as e:
            print(f"Error loading .env manually: {e}")

    # Map GOOGLE_API_KEY to GEMINIKEY if needed
    if "GOOGLE_API_KEY" in os.environ and "GEMINIKEY" not in os.environ:
         os.environ["GEMINIKEY"] = os.environ["GOOGLE_API_KEY"]
         # Also map to GEMINI_API_KEY which the generator might use
         os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]

def main():
    load_env_robustly()
    
    # Import Generator
    try:
        from Images import BatchAssetGeneratorIcons
    except ImportError:
        print("❌ Could not import BatchAssetGeneratorIcons.")
        sys.exit(1)

    # Import Prompt Enhancer
    try:
        import preview_icon_prompts
    except ImportError:
        print("❌ Could not import preview_icon_prompts.")
        sys.exit(1)

    # Define paths
    raw_input_path = project_root / "3_Simulation/2026-02-15/input/icons.json"
    enhanced_input_path = project_root / "7_TestingKnown/TestOutput/generated_icons/enhanced_prompts_preview.json"
    output_dir = project_root / "7_TestingKnown/TestOutput/generated_icons/execution_results"

    # Step 1: Run Prompt Enhancement
    print(f"🚀 Step 1: Enhancing prompts from {raw_input_path}")
    if not raw_input_path.exists():
        print(f"❌ Raw input file not found: {raw_input_path}")
        sys.exit(1)

    icons = preview_icon_prompts.load_icons(raw_input_path)
    if not icons:
        print("❌ No icons found in input file.")
        sys.exit(1)
        
    preview_icon_prompts.process_prompts(icons, enhanced_input_path)
    
    # Step 2: Generate from Enhanced Prompts
    print(f"\n🚀 Step 2: Generating icons from enhanced prompts at {enhanced_input_path}")
    
    # Load and Prepare Data
    try:
        with open(enhanced_input_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        sys.exit(1)
        
    generation_queue = []
    print(f"   Preparing to generate {len(data)} icons...")
    
    for item in data:
        # Create a copy to avoid modifying original list in place
        new_item = item.copy()
        
        # Use valid enhanced prompt or fallback to original
        if new_item.get("enhanced_prompt") and "Enhancement Failed" not in new_item["enhanced_prompt"]:
             new_item["prompt"] = new_item["enhanced_prompt"]
             print(f"   • {new_item.get('name', 'Unknown')}: Using enhanced prompt")
        else:
             print(f"   • {new_item.get('name', 'Unknown')}: Using original prompt (enhancement missing/failed)")
        
        generation_queue.append(new_item)

    print("\n" + "="*60)
    
    # Execute
    # Using provider="gemini" as requested
    BatchAssetGeneratorIcons.process_queue(
        generation_queue, 
        output_dir, 
        provider="gemini"
    )

if __name__ == "__main__":
    main()

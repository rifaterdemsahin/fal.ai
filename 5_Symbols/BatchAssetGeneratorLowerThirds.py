#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Lower Thirds
Project: The Agentic Era - Managing 240+ Workflows
Generates lower third graphics for important symbols and concepts derived from:
- source_chapter_markers.txt
- source_edl.md
- source_transcript.md
- assets_config.json (master configuration file)
"""

import os
import json
from pathlib import Path
from typing import Dict, List

# Install: pip install fal-client
try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

# Configuration
OUTPUT_DIR = Path("./generated_assets/lower_thirds")
CONFIG_FILE = Path("../3_Simulation/Feb1Youtube/assets_config.json")

# Consistency seeds
# Using SEED_004 as defined in the main generator for UI overlays/templates
SEEDS = {
    "SEED_004": 345678, 
}

# Brand color palette
BRAND_COLORS = {
    "primary_dark": "#1a1a2e",
    "accent_blue": "#00d4ff",
    "accent_purple": "#7b2cbf",
    "secondary_teal": "#00bfa5",
    "highlight_orange": "#ff6b35",
    "text_white": "#ffffff",
}

# Common Prompt Base
# Ensures all lower thirds have a unified look
PROMPT_BASE = (
    "Professional lower third broadcast graphic for video overlay, "
    "floating on transparent background (alpha channel), "
    "modern tech aesthetic, clean sans-serif typography, "
    "positioned in lower left area, high contrast for readability, "
    "dark glassmorphism background panel (#1a1a2e) with distinct accent borders, "
    "4k resolution, high quality render"
)

# Asset generation queue
# Symbols derived from Chapter Markers, EDL, and Transcript
GENERATION_QUEUE = [
    # HIGH PRIORITY - Core Concepts
    {
        "id": "LT_01",
        "name": "lt_agentic_era",
        "priority": "HIGH",
        "text": "The Agentic Era",
        "subtext": "Managing 240+ Workflows",
        "color_theme": "accent_blue",
        "seed_key": "SEED_004",
        "prompt": (
            f"{PROMPT_BASE}, main text 'THE AGENTIC ERA' in bold white font, "
            "subtext 'Managing 240+ Workflows' in smaller cyan font, "
            "neon blue (#00d4ff) glowing accent line, futuristic interface style."
        ),
    },
    {
        "id": "LT_02",
        "name": "lt_mcp",
        "priority": "HIGH",
        "text": "Model Context Protocol",
        "subtext": "Standardized AI Connections",
        "color_theme": "accent_purple",
        "seed_key": "SEED_004",
        "prompt": (
            f"{PROMPT_BASE}, main text 'MODEL CONTEXT PROTOCOL' in bold white font, "
            "subtext 'Standardized AI Connections' in smaller purple font, "
            "neon purple (#7b2cbf) glowing accent line, technical diagram aesthetic."
        ),
    },
    {
        "id": "LT_03",
        "name": "lt_skills_gap",
        "priority": "HIGH",
        "text": "The Skills Gap",
        "subtext": "Technology vs. Delivery",
        "color_theme": "highlight_orange",
        "seed_key": "SEED_004",
        "prompt": (
            f"{PROMPT_BASE}, main text 'THE SKILLS GAP' in bold white font, "
            "subtext 'Technology vs. Delivery' in smaller orange font, "
            "bright orange (#ff6b35) accent details, alert/warning style UI elements."
        ),
    },
    {
        "id": "LT_04",
        "name": "lt_bounded_contexts",
        "priority": "HIGH",
        "text": "Bounded Contexts",
        "subtext": "Separation of Concerns",
        "color_theme": "secondary_teal",
        "seed_key": "SEED_004",
        "prompt": (
            f"{PROMPT_BASE}, main text 'BOUNDED CONTEXTS' in bold white font, "
            "subtext 'Separation of Concerns' in smaller teal font, "
            "clean teal (#00bfa5) border lines, architectural structure design."
        ),
    },
    {
        "id": "LT_05",
        "name": "lt_para_method",
        "priority": "HIGH",
        "text": "PARA Method",
        "subtext": "Projects Areas Resources Archives",
        "color_theme": "accent_blue",
        "seed_key": "SEED_004",
        "prompt": (
            f"{PROMPT_BASE}, main text 'PARA METHOD' in bold white font, "
            "subtext 'Projects • Areas • Resources • Archives' in smaller grey/blue font, "
            "minimalist organized structure, sharp blue accents."
        ),
    },
    
    # MEDIUM PRIORITY - Technical Terms & Tools
    {
        "id": "LT_06",
        "name": "lt_state_management",
        "priority": "MEDIUM",
        "text": "State Management",
        "subtext": "Persistence in Automation",
        "color_theme": "accent_purple",
        "seed_key": "SEED_004",
        "prompt": (
            f"{PROMPT_BASE}, main text 'STATE MANAGEMENT' in bold white font, "
            "subtext 'Persistence in Automation' in smaller font, "
            "data flow visualization elements, purple accent lighting."
        ),
    },
    {
        "id": "LT_07",
        "name": "lt_deliverpilot",
        "priority": "MEDIUM",
        "text": "DeliverPilot",
        "subtext": "Methodology & Documentation",
        "color_theme": "secondary_teal",
        "seed_key": "SEED_004",
        "prompt": (
            f"{PROMPT_BASE}, main text 'DELIVERPILOT' in bold white font, "
            "subtext 'Methodology & Documentation' in smaller teal font, "
            "navigator/compass interface hints, clean professional look."
        ),
    },
    {
        "id": "LT_08",
        "name": "lt_bottom_up",
        "priority": "MEDIUM",
        "text": "Bottom-Up Revolution",
        "subtext": "Individual AI Adoption",
        "color_theme": "highlight_orange",
        "seed_key": "SEED_004",
        "prompt": (
            f"{PROMPT_BASE}, main text 'BOTTOM-UP REVOLUTION' in bold white font, "
            "subtext 'Individual AI Adoption' in smaller gold/orange font, "
            "dynamic upward motion visuals in background opacity, empowering aesthetic."
        ),
    },
    {
        "id": "LT_09",
        "name": "lt_n8n_workflows",
        "priority": "MEDIUM",
        "text": "240+ Autonomous Workflows",
        "subtext": "Running on n8n",
        "color_theme": "accent_blue",
        "seed_key": "SEED_004",
        "prompt": (
            f"{PROMPT_BASE}, main text '240+ AUTONOMOUS WORKFLOWS' in bold white font, "
            "subtext 'Running on n8n' in smaller font with n8n signature pink/orange hint, "
            "network node background pattern overlays."
        ),
    },
    {
        "id": "LT_10",
        "name": "lt_ai_transformation",
        "priority": "MEDIUM",
        "text": "AI Transformation",
        "subtext": "The Bigger Picture",
        "color_theme": "accent_purple",
        "seed_key": "SEED_004",
        "prompt": (
            f"{PROMPT_BASE}, main text 'AI TRANSFORMATION' in bold white font, "
            "subtext 'The Bigger Picture' in smaller purple font, "
            "digital transformation particle effects in glass panel."
        ),
    }
]

def generate_asset(asset_config: Dict, output_dir: Path) -> Dict:
    """Generate a single asset using fal.ai"""
    print(f"\n{'='*60}")
    print(f"🎨 Generating Lower Third: {asset_config['name']}")
    print(f"   Text: {asset_config['text']}")
    print(f"   Subtext: {asset_config['subtext']}")
    print(f"   Seed: {asset_config['seed_key']} ({SEEDS[asset_config['seed_key']]})")
    print(f"{'='*60}")
    
    try:
        # Prepare arguments
        # Using dev model for better text rendering
        arguments = {
            "prompt": asset_config["prompt"],
            "image_size": {"width": 1920, "height": 1080}, # Full frame, user crops or uses transparent
            "num_inference_steps": 30, # Higher steps for text clarity
            "seed": SEEDS[asset_config["seed_key"]],
            "num_images": 1,
            "enable_safety_checker": False
        }
        
        # Generate image
        print("⏳ Sending request to fal.ai (flux/dev)...")
        result = fal_client.subscribe(
            "fal-ai/flux/dev", 
            arguments=arguments,
        )
        
        # Download and save
        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            print(f"✅ Generated successfully!")
            print(f"   URL: {image_url}")
            
            # Save metadata
            output_path = output_dir / f"{asset_config['name']}.json"
            metadata = {
                **asset_config,
                "result_url": image_url,
                "seed_value": SEEDS[asset_config["seed_key"]],
            }
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Metadata saved: {output_path}")
            
            # Download image
            import urllib.request
            image_path = output_dir / f"{asset_config['name']}.png"
            urllib.request.urlretrieve(image_url, image_path)
            print(f"💾 Image saved: {image_path}")
            
            return {
                "success": True,
                "url": image_url,
                "local_path": str(image_path),
            }
        else:
            print(f"❌ Generation failed: No images in result")
            return {"success": False, "error": "No images returned"}
            
    except Exception as e:
        print(f"❌ Error generating asset: {str(e)}")
        return {"success": False, "error": str(e)}

def process_queue(queue: List[Dict], output_dir: Path) -> List[Dict]:
    """Process a queue of lower thirds to generate"""
    print(f"\n{'='*60}")
    print("🚀 FAL.AI BATCH LOWER THIRDS GENERATOR")
    print("   Project: The Agentic Era")
    print("="*60)
    
    # Check API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("\n❌ ERROR: FAL_KEY environment variable not set")
        print("   Set it with: export FAL_KEY='your-api-key-here'")
        return []
    
    print(f"\n✅ API Key found")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print(f"\n📊 Assets to generate: {len(queue)}")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate assets
    results = []
    for i, asset in enumerate(queue, 1):
        print(f"\n\n{'#'*60}")
        print(f"# Asset {i}/{len(queue)}")
        print(f"{'#'*60}")
        
        result = generate_asset(asset, output_dir)
        results.append({
            "asset_id": asset["id"],
            "name": asset["name"],
            "priority": asset["priority"],
            **result
        })
    
    # Summary
    print("\n\n" + "="*60)
    print("📊 GENERATION SUMMARY")
    print("="*60)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\n✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    # Save summary
    summary_path = output_dir / "generation_summary.json"
    with open(summary_path, 'w') as f:
        json.dump({
            "total": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "results": results,
        }, f, indent=2)
    
    print(f"\n💾 Summary saved: {summary_path}")
    print("\n✅ Done!")
    
    return results

def load_config_from_json(config_path: Path = CONFIG_FILE) -> List[Dict]:
    """Load lower thirds configuration from JSON file"""
    if not config_path.exists():
        print(f"⚠️  Config file not found: {config_path}")
        print(f"   Falling back to hardcoded GENERATION_QUEUE")
        return GENERATION_QUEUE
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if "lower_thirds" not in config:
            print(f"⚠️  No 'lower_thirds' section found in {config_path}")
            print(f"   Falling back to hardcoded GENERATION_QUEUE")
            return GENERATION_QUEUE
        
        lower_thirds_config = config["lower_thirds"]
        
        # Transform config to match expected format with prompt base
        for item in lower_thirds_config:
            # If prompt doesn't exist, build it from text/subtext
            if "prompt" not in item or not item["prompt"]:
                color = BRAND_COLORS.get(item.get("color_theme", "accent_blue"), "#00d4ff")
                item["prompt"] = (
                    f"{PROMPT_BASE}, main text '{item['text'].upper()}' in bold white font, "
                    f"subtext '{item['subtext']}' in smaller font, "
                    f"color theme: {item.get('color_theme', 'accent_blue')}."
                )
        
        print(f"✅ Loaded {len(lower_thirds_config)} lower thirds from {config_path}")
        return lower_thirds_config
        
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        print(f"   Falling back to hardcoded GENERATION_QUEUE")
        return GENERATION_QUEUE

def main():
    """Main execution"""
    # Load configuration from JSON file
    generation_queue = load_config_from_json()
    
    # Confirm before proceeding
    print("\n" + "="*60)
    response = input("🤔 Proceed with generation? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled by user")
        return
        
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    process_queue(generation_queue, OUTPUT_DIR)


if __name__ == "__main__":
    main()

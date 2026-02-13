#!/usr/bin/env python3
"""
fal.ai Batch Icon Generator
Project: The Agentic Era - Managing 240+ Workflows
Generates all required icon assets with consistency controls
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import urllib.request
import urllib.error
import base64
from datetime import datetime


# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Install: pip install fal-client
try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

# Import asset utilities
try:
    from Utils.asset_utils import generate_filename, extract_scene_number, ManifestTracker
except ImportError:
    # Fallback if running standalone
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    try:
        from Utils.asset_utils import generate_filename, extract_scene_number, ManifestTracker
    except ImportError:
        print("⚠️  asset_utils not found. Using legacy naming convention.")
        generate_filename = None
        extract_scene_number = None
        ManifestTracker = None

# Import cost check function
try:
    from Base.generator_config import check_generation_cost, MODEL_PRICING
except ImportError:
    # Fallback if running standalone
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from Base.generator_config import check_generation_cost, MODEL_PRICING

# Configuration
DEFAULT_OUTPUT_DIR = Path("./generated_icons")
# Directory creation moved to execution time to avoid side effects on import

# Consistency seeds for different asset categories
SEEDS = {
    "SEED_001": 42,      # B-roll (can vary)
    "SEED_002": 123456,  # Infographics (MUST match)
    "SEED_003": 789012,  # Motion graphics (brand)
    "SEED_004": 345678,  # UI overlays (template)
}

# Brand color palette (reference for prompts)
BRAND_COLORS = {
    "primary_dark": "#1a1a2e",
    "accent_blue": "#00d4ff",
    "accent_purple": "#7b2cbf",
    "secondary_teal": "#00bfa5",
    "highlight_orange": "#ff6b35",
    "text_white": "#ffffff",
}

# Asset generation queue
GENERATION_QUEUE = [
    # CORE SYMBOLS
    {
        "id": "icon_001",
        "name": "ferrari_icon",
        "priority": "HIGH",
        "scene": "Scene 1: Hook",
        "seed_key": "SEED_003",
        "prompt": (
            "Sleek red Ferrari sports car icon, side view, minimalist flat design, "
            "clean vector style, isolated on white background, "
            "professional tech presentation aesthetic, modern motion graphics style"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    {
        "id": "icon_002",
        "name": "shopping_cart_icon",
        "priority": "HIGH",
        "scene": "Scene 1: Hook",
        "seed_key": "SEED_003",
        "prompt": (
            "Simple shopping cart icon, minimalist flat design, "
            "clean vector style, isolated on white background, "
            "professional tech presentation aesthetic"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    
    # INFOGRAPHIC ICONS
    {
        "id": "icon_003",
        "name": "database_cylinder",
        "priority": "HIGH",
        "scene": "Scene 4: Skills Gap",
        "seed_key": "SEED_002",
        "prompt": (
            "Database cylinder icon, modern UI style, cyan accent #00d4ff, "
            "clean vector graphics, isolated on white background, "
            "tech infographic element"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    {
        "id": "icon_004",
        "name": "brain_processor",
        "priority": "HIGH",
        "scene": "Scene 4: Skills Gap",
        "seed_key": "SEED_002",
        "prompt": (
            "Brain circuit board icon, artificial intelligence symbol, "
            "purple accent #7b2cbf, minimalist vector design, "
            "isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    {
        "id": "icon_005",
        "name": "notification_bell",
        "priority": "MEDIUM",
        "scene": "Scene 4: Skills Gap",
        "seed_key": "SEED_002",
        "prompt": (
            "Notification bell icon with active badge, modern iOS style, "
            "orange accent #ff6b35, clean vector graphics, "
            "isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    
    # BOUNDED CONTEXT ICONS
    {
        "id": "icon_006",
        "name": "family_house",
        "priority": "MEDIUM",
        "scene": "Scene 5: Bounded Contexts",
        "seed_key": "SEED_002",
        "prompt": (
            "Minimalist house icon, home automation symbol, "
            "blue accent #00d4ff, rounded corners, flat design, "
            "vector icon, isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    {
        "id": "icon_007",
        "name": "finance_dollar",
        "priority": "MEDIUM",
        "scene": "Scene 5: Bounded Contexts",
        "seed_key": "SEED_002",
        "prompt": (
            "Dollar sign icon inside circle, financial symbol, "
            "purple accent #7b2cbf, modern clean lines, "
            "vector icon, isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    {
        "id": "icon_008",
        "name": "project_folder",
        "priority": "MEDIUM",
        "scene": "Scene 5: Bounded Contexts",
        "seed_key": "SEED_002",
        "prompt": (
            "Project folder icon, file management symbol, "
            "teal accent #00bfa5, flat minimalist design, "
            "vector icon, isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },

    # STATE MANAGEMENT ICONS
    {
        "id": "icon_009",
        "name": "workflow_branch",
        "priority": "MEDIUM",
        "scene": "Scene 8: State Management",
        "seed_key": "SEED_002",
        "prompt": (
            "Workflow branch icon, fork path symbol, decision point, "
            "modern tech UI style, blue/cyan gradient, "
            "vector graphics, isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
    {
        "id": "icon_010",
        "name": "save_disk",
        "priority": "MEDIUM",
        "scene": "Scene 8: State Management",
        "seed_key": "SEED_002",
        "prompt": (
            "Save state icon, cloud upload symbol or floppy disk stylized, "
            "modern clean UI, teal accent #00bfa5, "
            "vector graphics, isolated on white background"
        ),
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1024, "height": 1024},
        "num_inference_steps": 28,
    },
]





def generate_asset_with_gemini(asset_config: Dict, output_dir: Path, manifest: Optional[object] = None, version: int = 1) -> Dict:
    """
    Generate asset using Gemini (Imagen 3) API as fallback.
    Uses the new google-genai SDK (v1.0+) as recommended.
    """
    api_key = os.environ.get("GOOGLE_IMAGEGENKEY") or os.environ.get("GEMINIKEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ No GEMINI_API_KEY found for fallback.")
        return {"success": False, "error": "No Gemini API Key"}

    print(f"✨ Generating with Gemini (Imagen 3)...")

    # Try using the new google-genai SDK first
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        
        model_name = 'imagen-3.0-generate-001'
        prompt = asset_config.get("prompt", "")
        
        print(f"   Attempting with SDK model: {model_name}")
        
        # Generate image using SDK
        response = client.models.generate_images(
            model=model_name,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        
        if response.generated_images:
            image = response.generated_images[0]
            
            # Generate filename
            if generate_filename and extract_scene_number:
                scene_num = extract_scene_number(asset_config.get('id', '0.0'))
                base_filename = generate_filename(
                    scene_num,
                    'icon',
                    asset_config['name'] + "_gemini",
                    version
                )
                filename_json = base_filename + '.json'
                filename_png = base_filename + '.png'
            else:
                filename_json = f"{asset_config['name']}_gemini.json"
                filename_png = f"{asset_config['name']}_gemini.png"
            
            # Save metadata
            output_path = output_dir / filename_json
            metadata = {
                **asset_config,
                "provider": "gemini",
                "filename": filename_png,
                "model": model_name
            }
            if 'seed_key' in asset_config:
                metadata["seed_value"] = SEEDS.get(asset_config["seed_key"])
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Save image
            image_path = output_dir / filename_png
            image.image.save(image_path)
            print(f"💾 Gemini Image saved: {image_path}")
            
            # Add to manifest
            if manifest:
                manifest.add_asset(
                    filename=filename_png,
                    prompt=prompt,
                    asset_type="icon",
                    asset_id=asset_config.get("id", "unknown"),
                    result_url="gemini-generated",
                    local_path=str(image_path),
                    metadata={
                        "model": model_name,
                        "provider": "gemini"
                    }
                )

            return {
                "success": True,
                "local_path": str(image_path),
                "filename": filename_png,
                "provider": "gemini",
                "cost": 0.0
            }
            
    except ImportError:
        print("⚠️  google-genai SDK not found. Falling back to REST API...")
    except Exception as e:
        print(f"❌ SDK Generation Error: {e}")
        print("   Falling back to REST API...")

    # REST API Fallback (Legacy / Manual)
    models_to_try = [
        "models/imagen-3.0-generate-001",
        "models/image-generation-001",
    ]
    
    headers = {"Content-Type": "application/json"}
    prompt = asset_config.get("prompt", "")
    
    for model_name in models_to_try:
        print(f"   Attempting with REST model: {model_name}")
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:predict?key={api_key}"
        
        payload = {
            "instances": [
                {"prompt": prompt}
            ],
            "parameters": {
                "sampleCount": 1,
            }
        }
        
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers)
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                
                b64_data = None
                if "predictions" in result and len(result["predictions"]) > 0:
                    prediction = result["predictions"][0]
                    if isinstance(prediction, dict):
                            b64_data = prediction.get("bytesBase64Encoded")
                    elif isinstance(prediction, str):
                            b64_data = prediction
                
                if b64_data:
                    image_data = base64.b64decode(b64_data)
                    
                    # (Filename gen duplication omitted for brevity, reusing logic)
                    if generate_filename and extract_scene_number:
                        scene_num = extract_scene_number(asset_config.get('id', '0.0'))
                        base_filename = generate_filename(scene_num, 'icon', asset_config['name'] + "_gemini", version)
                        filename_json = base_filename + '.json'
                        filename_png = base_filename + '.png'
                    else:
                        filename_json = f"{asset_config['name']}_gemini.json"
                        filename_png = f"{asset_config['name']}_gemini.png"
                    
                    output_path = output_dir / filename_json
                    metadata = {**asset_config, "provider": "gemini", "filename": filename_png, "model": model_name}
                    with open(output_path, 'w') as f: json.dump(metadata, f, indent=2)
                    
                    image_path = output_dir / filename_png
                    with open(image_path, "wb") as f: f.write(image_data)
                    print(f"💾 Gemini Image saved: {image_path}")
                    
                    return {"success": True, "local_path": str(image_path), "filename": filename_png, "provider": "gemini", "cost": 0.0}

        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"   ❌ Model {model_name} not found.")
            else:
                 print(f"   ❌ HTTP Error: {e}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue

    return {"success": False, "error": "All Gemini models failed."}


def generate_asset(asset_config: Dict, output_dir: Path, manifest: Optional[object] = None, version: int = 1, provider: str = "auto") -> Dict:
    """Generate a single asset using fal.ai or fallback to Gemini"""
    
    # Force Gemini provider if requested
    if provider == "gemini":
        return generate_asset_with_gemini(asset_config, output_dir, manifest, version)
        
    print(f"\n{'='*60}")
    print(f"🎨 Generating Icon: {asset_config['name']}")
    print(f"   Scene: {asset_config['scene']}")
    print(f"   Priority: {asset_config['priority']}")
    print(f"   Seed: {asset_config['seed_key']} ({SEEDS[asset_config['seed_key']]})")
    print(f"{'='*60}")
    
    try:
        # Check cost before generating (for generations > $0.20)
        if not check_generation_cost(asset_config["model"]):
            return {
                "success": False,
                "error": "Skipped due to cost exceeding threshold",
            }
        
        # Prepare arguments
        arguments = {
            "prompt": asset_config["prompt"],
            "image_size": asset_config["image_size"],
            "num_inference_steps": asset_config["num_inference_steps"],
            "seed": SEEDS[asset_config["seed_key"]],
            "num_images": 1,
        }
        
        # Generate image
        print("⏳ Sending request to fal.ai...")
        try:
            result = fal_client.subscribe(
                asset_config["model"],
                arguments=arguments,
            )
        except Exception as e:
            error_msg = str(e).lower()
            credit_indicators = [
                "exhausted balance",
                "insufficient credits",
                "insufficient balance",
                "user is locked",
                "top up your balance",
                "no credits remaining",
                "credit limit exceeded",
                "402"
            ]
            
            if any(indicator in error_msg for indicator in credit_indicators):
                print(f"\n💳 CREDIT ERROR DETECTED! ({str(e)})")
                print(f"   Attempting fallback to Gemini (Imagen 3)...")
                return generate_asset_with_gemini(asset_config, output_dir, manifest, version)
            else:
                raise e

        
        # Download and save
        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            print(f"✅ Generated successfully!")
            print(f"   URL: {image_url}")
            
            # Generate filename using new convention if available
            if generate_filename and extract_scene_number:
                scene_num = extract_scene_number(asset_config.get('id', '0.0'))
                base_filename = generate_filename(
                    scene_num,
                    'icon',
                    asset_config['name'],
                    version
                )
                filename_json = base_filename + '.json'
                filename_png = base_filename + '.png'
            else:
                # Fallback to legacy naming
                filename_json = f"{asset_config['name']}.json"
                filename_png = f"{asset_config['name']}.png"
            
            # Save metadata
            output_path = output_dir / filename_json
            metadata = {
                **asset_config,
                "result_url": image_url,
                "seed_value": SEEDS[asset_config["seed_key"]],
                "filename": filename_png,
            }
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Metadata saved: {output_path}")
            
            # Download image
            import urllib.request
            image_path = output_dir / filename_png
            urllib.request.urlretrieve(image_url, image_path)
            print(f"💾 Image saved: {image_path}")
            
            # Add to manifest if provided
            if manifest:
                manifest.add_asset(
                    filename=filename_png,
                    prompt=asset_config["prompt"],
                    asset_type="icon",
                    asset_id=asset_config.get("id", "unknown"),
                    result_url=image_url,
                    local_path=str(image_path),
                    metadata={
                        "scene": asset_config.get("scene", ""),
                        "priority": asset_config.get("priority", ""),
                        "model": asset_config.get("model", ""),
                    }
                )
            
            return {
                "success": True,
                "url": image_url,
                "local_path": str(image_path),
                "filename": filename_png,
                "cost": MODEL_PRICING.get(asset_config["model"], 0.0)
            }
        else:
            print(f"❌ Generation failed: No images in result")
            return {"success": False, "error": "No images returned"}
            
    except Exception as e:
        print(f"❌ Error generating asset: {str(e)}")
        return {"success": False, "error": str(e)}

def process_queue(queue: List[Dict], output_dir: Path, manifest: Optional[object] = None, provider: str = "auto") -> List[Dict]:
    """Process a queue of icons to generate"""
    print(f"\n{'='*60}")
    print("🚀 FAL.AI BATCH ICON GENERATOR")
    print("   Project: The Agentic Era - Managing 240+ Workflows")
    print("="*60)
    
    # Check API key if using fal or auto
    if provider in ["fal", "auto"]:
        api_key = os.environ.get("FAL_KEY")
        if not api_key:
            if provider == "fal":
                print("\n❌ ERROR: FAL_KEY environment variable not set")
                return []
            else:
                print("\n⚠️ FAL_KEY not found. Switching to Gemini only.")
                provider = "gemini" 

    
    print(f"\n✅ API Key found")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print(f"\n📊 Icons to generate: {len(queue)}")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Count by priority
    high_priority = [a for a in queue if a["priority"] == "HIGH"]
    medium_priority = [a for a in queue if a["priority"] == "MEDIUM"]
    
    print(f"   • HIGH priority: {len(high_priority)}")
    print(f"   • MEDIUM priority: {len(medium_priority)}")
    
    # Generate assets
    results = []
    for i, asset in enumerate(queue, 1):
        print(f"\n\n{'#'*60}")
        print(f"# Icon {i}/{len(queue)}")
        print(f"{'#'*60}")
        
        result = generate_asset(asset, output_dir, manifest, provider=provider)
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
    
    total_cost = sum(r.get("cost", 0.0) for r in results)
    
    print(f"\n✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    print(f"💰 Total Cost: ${total_cost:.4f}")
    
    if successful:
        print("\n✅ SUCCESSFUL GENERATIONS:")
        for r in successful:
            print(f"   • {r['asset_id']}: {r['name']} ({r['priority']}) - ${r.get('cost', 0.0):.4f}")
    
    if failed:
        print("\n❌ FAILED GENERATIONS:")
        for r in failed:
            print(f"   • {r['asset_id']}: {r['name']} - {r.get('error', 'Unknown error')}")
    
    # Save summary
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path = output_dir / f"generation_summary_{timestamp}.json"
    
    with open(summary_path, 'w') as f:
        json.dump({
            "total": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "total_cost": total_cost,
            "results": results,
            "timestamp": timestamp
        }, f, indent=2)
    
    print(f"\n💾 Summary saved: {summary_path}")
    print("\n✅ Done!")
    
    return results

def main():
    """Main execution"""
    import argparse
    parser = argparse.ArgumentParser(description="Fal.ai Batch Icon Generator")
    parser.add_argument("--input", "-i", type=Path, help="Path to input JSON file containing icon definitions")
    parser.add_argument("--output", "-o", type=Path, help="Path to output directory")
    parser.add_argument("--provider", "-p", choices=["fal", "gemini", "auto"], default="auto", help="Force specific provider")
    args = parser.parse_args()

    # Determine input queue
    queue = GENERATION_QUEUE
    if args.input:
        if not args.input.exists():
            print(f"❌ Input file not found: {args.input}")
            return
        
        try:
            with open(args.input, 'r') as f:
                queue = json.load(f)
            print(f"✅ Loaded {len(queue)} icons from {args.input}")
        except Exception as e:
            print(f"❌ Error loading input file: {e}")
            return

    # Determine output directory
    output_dir = args.output if args.output else DEFAULT_OUTPUT_DIR

    # Confirm before proceeding
    print("\n" + "="*60)
    print(f"🚀 Starting generation for {len(queue)} icons")
    print(f"📁 Output: {output_dir}")
    if args.input:
        print(f"📄 Input: {args.input}")
    print(f"🤖 Provider: {args.provider}")
    
    # Skip confirmation if arguments are provided (assume automation), otherwise ask
    if not args.input and not args.output:
        response = input("🤔 Proceed with generation? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("❌ Cancelled by user")
            return
        
    process_queue(queue, output_dir, provider=args.provider)


if __name__ == "__main__":
    main()

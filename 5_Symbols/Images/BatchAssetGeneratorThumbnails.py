#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator for YouTube Thumbnails
Project: The Delivery Pilot Transformation
Generates 5 compelling thumbnail images that capture key video themes
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Install: pip install fal-client
try:
    import fal_client
    try:
        from dotenv import load_dotenv
        # Load .env from project root (3 levels up: Images -> 5_Symbols -> root)
        load_dotenv(Path(__file__).parent.parent.parent / ".env")
    except ImportError:
        pass # dotenv is optional if env vars are set
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

# Configuration
OUTPUT_DIR = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# fal.ai model for image generation (classical fal.ai code)
MODEL = "fal-ai/flux/schnell"

# Thumbnail specifications (YouTube recommended: 1280x720, 16:9 aspect ratio)
THUMBNAIL_SPECS = {
    "image_size": {
        "width": 1280,
        "height": 720
    },
    "num_inference_steps": 4,  # Fast generation with flux/schnell
    "num_images": 1
}

# 5 compelling thumbnail prompts based on video script themes
THUMBNAIL_PROMPTS = [
    {
        "id": "thumbnail_01",
        "name": "Delivery Pilot Transformation",
        "scene": 1,
        "prompt": (
            "Professional YouTube thumbnail: person holding massive oversized golden microphone, "
            "bold text 'DELIVERY PILOT' in electric blue and gold. Futuristic dark background "
            "with holographic 240+ workflow dashboard floating behind. Text overlay 'BECOME A "
            "DELIVERY PILOT' in modern bold sans-serif. High contrast, cinematic lighting, "
            "tech aesthetic, YouTube optimized 16:9 format, ultra HD."
        ),
        "description": "Main thumbnail - the delivery pilot transformation journey"
    },
    {
        "id": "thumbnail_02",
        "name": "Static vs Dynamic AI",
        "scene": 2,
        "prompt": (
            "Eye-catching YouTube thumbnail split-screen comparison. Left side: grey crumbling "
            "stone statues with chains and text 'OLD RULES' in faded red. Right side: liquid "
            "mercury Terminator-style figure morphing with glowing blue AI neural network, text "
            "'DYNAMIC AI' in vibrant cyan. Dramatic center divide with breaking chains. "
            "Bold text 'BREAK FREE' at top in gold. Dark moody lighting, 16:9 format, ultra sharp."
        ),
        "description": "Static rules vs dynamic AI - breaking the iron chains"
    },
    {
        "id": "thumbnail_03",
        "name": "Zero Capital AI Startup",
        "scene": 3,
        "prompt": (
            "Striking YouTube thumbnail: bold text '$0 TO START' in large neon green letters "
            "at center. Icons for VS Code, GitHub, and Cursor AI floating around. Empty wallet "
            "transforming into a glowing laptop with AI workflows streaming out. Dark gradient "
            "background purple to black. Subtitle 'FREE AI TOOLS' in white. Professional "
            "marketing style, high energy, 16:9 aspect ratio, ultra HD."
        ),
        "description": "Start with zero capital using free AI tools"
    },
    {
        "id": "thumbnail_04",
        "name": "LLM Digital Feast",
        "scene": 4,
        "prompt": (
            "Vibrant YouTube thumbnail: digital banquet table with 100 glowing tablets, each "
            "showing a different AI model logo. Four main dishes highlighted: Claude brain icon "
            "in orange, ChatGPT logo in green, DeepSeek code terminal in blue, Gemini gem in "
            "purple. Bold text 'CHOOSE YOUR AI' at top in white. Warm dramatic lighting, "
            "rich colors, feast aesthetic meets tech, 16:9 format, ultra HD."
        ),
        "description": "The LLM feast - choosing between AI models"
    },
    {
        "id": "thumbnail_05",
        "name": "Internet Kill Switch Parenting",
        "scene": 5,
        "prompt": (
            "Bold YouTube thumbnail: giant red emergency power button with text 'INTERNET KILL "
            "SWITCH' in stark white letters. GitHub and n8n workflow nodes connecting to home "
            "WiFi router. Protective shield icon with family silhouette. Dark cyberpunk "
            "background with red warning glow. Subtitle 'SMART PARENTING' in green. "
            "Dramatic tech-noir style, high contrast, 16:9 format, ultra HD."
        ),
        "description": "The internet kill switch for smart parenting"
    }
]


def generate_thumbnail(thumb_config: Dict, output_dir: Path, manifest: Optional[object] = None, version: int = 1) -> Dict:
    """Generate a single thumbnail using fal.ai"""
    print(f"\n{'='*60}")
    print(f"🎨 Generating Thumbnail: {thumb_config['name']}")
    print(f"   ID: {thumb_config['id']}")
    print(f"   Theme: {thumb_config['description']}")
    print(f"{'='*60}")
    
    try:
        # Prepare arguments for fal.ai
        arguments = {
            "prompt": thumb_config["prompt"],
            "image_size": THUMBNAIL_SPECS["image_size"],
            "num_inference_steps": THUMBNAIL_SPECS["num_inference_steps"],
            "num_images": THUMBNAIL_SPECS["num_images"],
        }
        
        # Generate thumbnail using fal.ai
        print("⏳ Sending request to fal.ai...")
        result = fal_client.subscribe(
            MODEL,
            arguments=arguments,
        )
        
        # Download and save
        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            print(f"✅ Generated successfully!")
            print(f"   URL: {image_url}")
            
            # Generate filename using asset utilities or fallback
            if generate_filename:
                filename = generate_filename(
                    scene_number=thumb_config["scene"],
                    asset_type="thumbnail",
                    description=thumb_config["name"],
                    extension="png",
                    version=version
                )
            else:
                # Fallback naming
                clean_name = thumb_config["name"].lower().replace(" ", "_")
                filename = f"{thumb_config['scene']:03d}_thumbnail_{clean_name}_v{version}.png"
            
            filepath = output_dir / filename
            
            # Download image
            import urllib.request
            print(f"⏳ Downloading to {filepath}...")
            urllib.request.urlretrieve(image_url, filepath)
            print(f"💾 Saved: {filepath}")
            
            # Track in manifest
            result_data = {
                "id": thumb_config["id"],
                "name": thumb_config["name"],
                "filename": filename,
                "filepath": str(filepath.absolute()),
                "url": image_url,
                "prompt": thumb_config["prompt"],
                "description": thumb_config["description"],
                "model": MODEL,
                "image_size": THUMBNAIL_SPECS["image_size"],
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
            
            return result_data
            
        else:
            error_msg = "No image URL in result"
            print(f"❌ Generation failed: {error_msg}")
            return {
                "id": thumb_config["id"],
                "name": thumb_config["name"],
                "success": False,
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error: {error_msg}")
        return {
            "id": thumb_config["id"],
            "name": thumb_config["name"],
            "success": False,
            "error": error_msg,
            "timestamp": datetime.now().isoformat()
        }


def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("🎬 YouTube Thumbnail Generator")
    print("   Using fal.ai flux/schnell model")
    print("="*60)
    
    # Generate all thumbnails
    results = []
    for i, thumb_config in enumerate(THUMBNAIL_PROMPTS, 1):
        print(f"\n📸 Generating thumbnail {i}/{len(THUMBNAIL_PROMPTS)}...")
        result = generate_thumbnail(thumb_config, OUTPUT_DIR, version=1)
        results.append(result)
    
    # Save summary
    summary = {
        "generator": "BatchAssetGeneratorThumbnails",
        "model": MODEL,
        "timestamp": datetime.now().isoformat(),
        "total_thumbnails": len(THUMBNAIL_PROMPTS),
        "successful": sum(1 for r in results if r.get("success")),
        "failed": sum(1 for r in results if not r.get("success")),
        "results": results
    }
    
    summary_path = OUTPUT_DIR / "generation_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 GENERATION SUMMARY")
    print("="*60)
    print(f"✅ Successful: {summary['successful']}/{summary['total_thumbnails']}")
    print(f"❌ Failed: {summary['failed']}/{summary['total_thumbnails']}")
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}")
    print(f"📝 Summary saved: {summary_path}")
    print("="*60)
    
    return summary


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("FAL_KEY"):
        print("❌ Error: FAL_KEY environment variable not set")
        print("   Set it with: export FAL_KEY='your-api-key-here'")
        exit(1)
    
    main()

#!/usr/bin/env python3
"""
Gemini Image Generator
Generates images using Google Gemini API based on storyboard and icon prompts
"""

import os
import json
import base64
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Google Generative AI
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ google-generativeai not installed. Run: pip install google-genai")
    exit(1)

# Configuration
INPUT_DIR = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/input")
OUTPUT_DIR = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Image generation settings
IMAGE_SETTINGS = {
    "model": "imagen-4.0-generate-001",  # Imagen 4 for image generation
    "width": 1024,
    "height": 1024,
}

def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip('"').strip("'")
                    os.environ[key] = value

def get_storyboard_prompts() -> List[Dict]:
    """Parse storyboard markdown and extract image prompts"""
    storyboard_path = INPUT_DIR / "source_storyboard.md"
    prompts = []
    
    if not storyboard_path.exists():
        print(f"⚠️  Storyboard not found: {storyboard_path}")
        return prompts
    
    with open(storyboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse frames from markdown
    frames = content.split("### Frame ")
    for i, frame in enumerate(frames[1:], 1):  # Skip header
        lines = frame.strip().split('\n')
        if not lines:
            continue
            
        # Extract frame title and details
        title_line = lines[0]
        frame_name = title_line.split('(')[0].strip()
        
        # Extract visual elements
        visual_elements = ""
        mood = ""
        shot_type = ""
        
        for line in lines:
            if "Visual Elements:" in line:
                visual_elements = line.split("Visual Elements:")[-1].strip()
            elif "Mood:" in line:
                mood = line.split("Mood:")[-1].strip()
            elif "Shot Type:" in line:
                shot_type = line.split("Shot Type:")[-1].strip()
        
        # Create detailed prompt
        prompt = f"Cinematic {shot_type.lower()} scene showing {visual_elements}. Mood: {mood}. Professional video production quality, 8K, detailed lighting, film grain."
        
        prompts.append({
            "id": f"frame_{i:02d}",
            "name": frame_name.replace(":", "_").replace(" ", "_").lower(),
            "prompt": prompt,
            "scene": f"Frame {i}",
            "category": "storyboard"
        })
    
    return prompts

def get_icon_prompts() -> List[Dict]:
    """Load icon prompts from JSON"""
    icons_path = INPUT_DIR / "icons.json"
    
    if not icons_path.exists():
        print(f"⚠️  Icons file not found: {icons_path}")
        return []
    
    with open(icons_path, 'r', encoding='utf-8') as f:
        icons = json.load(f)
    
    for icon in icons:
        icon["category"] = "icon"
    
    return icons

def generate_image_gemini(client, prompt: str, config: Dict) -> Optional[bytes]:
    """Generate a single image using Imagen 4"""
    try:
        response = client.models.generate_images(
            model=IMAGE_SETTINGS["model"],
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        
        # Extract image from response
        if response.generated_images and len(response.generated_images) > 0:
            return response.generated_images[0].image.image_bytes
        
        return None
        
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return None

def save_image(image_data: bytes, filename: str, output_dir: Path) -> Path:
    """Save image data to file"""
    filepath = output_dir / filename
    with open(filepath, 'wb') as f:
        f.write(image_data)
    return filepath

def generate_all_images(prompts: List[Dict], client, output_dir: Path) -> List[Dict]:
    """Generate all images from prompts"""
    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"\n{'='*60}")
    print("🎨 GEMINI IMAGE GENERATOR")
    print(f"   Total prompts: {len(prompts)}")
    print(f"   Output: {output_dir}")
    print("="*60)
    
    for i, item in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] Generating: {item.get('name', item.get('id'))}")
        print(f"   Category: {item.get('category', 'unknown')}")
        print(f"   Prompt: {item['prompt'][:80]}...")
        
        image_data = generate_image_gemini(client, item['prompt'], IMAGE_SETTINGS)
        
        if image_data:
            # Generate filename
            safe_name = item.get('name', item.get('id', 'image'))
            safe_name = safe_name.replace(' ', '_').replace(':', '').lower()
            filename = f"{item.get('id', i):03d}_{safe_name}_{timestamp}.png" if isinstance(item.get('id'), int) else f"{safe_name}_{timestamp}.png"
            
            # Save image
            filepath = save_image(image_data, filename, output_dir)
            print(f"   ✅ Saved: {filepath.name}")
            
            # Save metadata
            metadata = {
                **item,
                "filename": filename,
                "generated_at": timestamp,
                "model": IMAGE_SETTINGS["model"],
            }
            
            metadata_path = output_dir / f"{filename.replace('.png', '.json')}"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            results.append({
                "success": True,
                "name": item.get('name', item.get('id')),
                "filename": filename,
                "filepath": str(filepath)
            })
        else:
            print(f"   ❌ Failed to generate")
            results.append({
                "success": False,
                "name": item.get('name', item.get('id')),
                "error": "Generation failed"
            })
    
    return results

def main():
    """Main execution"""
    # Load environment
    load_env()
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment")
        return
    
    print(f"✅ API Key loaded")
    
    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    
    # Collect all prompts
    storyboard_prompts = get_storyboard_prompts()
    icon_prompts = get_icon_prompts()
    
    all_prompts = storyboard_prompts + icon_prompts
    
    print(f"\n📊 Found prompts:")
    print(f"   • Storyboard frames: {len(storyboard_prompts)}")
    print(f"   • Icons: {len(icon_prompts)}")
    print(f"   • Total: {len(all_prompts)}")
    
    if not all_prompts:
        print("❌ No prompts found to generate")
        return
    
    # Confirm before proceeding
    response = input("\n🤔 Proceed with generation? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled by user")
        return
    
    # Generate images
    results = generate_all_images(all_prompts, client, OUTPUT_DIR)
    
    # Summary
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\n{'='*60}")
    print("📊 GENERATION SUMMARY")
    print("="*60)
    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    # Save summary
    summary_path = OUTPUT_DIR / f"gemini_generation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_path, 'w') as f:
        json.dump({
            "total": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "results": results,
        }, f, indent=2)
    
    print(f"\n💾 Summary saved: {summary_path}")
    print("\n✅ Done!")

if __name__ == "__main__":
    main()

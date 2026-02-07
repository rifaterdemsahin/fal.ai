#!/usr/bin/env python3
"""
Prerequisites Asset Generator
Generates a sprite sheet for the deployment prerequisites steps.
Steps:
1. Goto n8n.com
2. Open an account
3. Try out online
4. Setup environment
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional

# ensure we can import from parent directories if needed
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Load .env manually to avoid dependency
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    with open(env_path, "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#") and "=" in line:
                key, value = line.strip().split("=", 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")

try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("❌ Pillow (PIL) not installed. Run: pip install Pillow")
    Image = None

# Configuration
OUTPUT_DIR = Path(r"C:\projects\fal.ai\3_Simulation\Feb1Youtube\generated_prerequisites")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VERSION = 1
GROUP_NAME = "n8nsetup"

# Shared Prompt Style
STYLE_PROMPT = "futuristic digital interface, neon glowing accents, dark background, highly detailed, 8k resolution, ui element, minimalist icon style"

# Steps to generate
STEPS = [
    {
        "order": 1,
        "action": "goton8n",
        "prompt": f"Close up view of a web browser address bar with 'n8n.com' being typed, {STYLE_PROMPT}",
        "text": "1. Goto n8n.com"
    },
    {
        "order": 2,
        "action": "openaccount",
        "prompt": f"Digital user profile icon with a 'Sign Up' button being clicked, glowing effect, {STYLE_PROMPT}",
        "text": "2. Open an account"
    },
    {
        "order": 3,
        "action": "tryonline",
        "prompt": f"Node-based workflow editor interface on a screen, connecting dots, {STYLE_PROMPT}",
        "text": "3. Try out online"
    },
    {
        "order": 4,
        "action": "setupenvironment",
        "prompt": f"Computer terminal code screen, green matrix text, setting up local server, {STYLE_PROMPT}",
        "text": "4. Setup environment"
    }
]

def generate_image(step: Dict) -> Optional[Path]:
    """Generate image for a single step with versioned naming"""
    print(f"Generating: {step['text']}...")
    
    # Construct filename: 1_n8nsetup_goton8n_v1.jpg
    filename = f"{step['order']}_{GROUP_NAME}_{step['action']}_v{VERSION}.jpg"
    save_path = OUTPUT_DIR / filename
    
    # Check if exists to avoid re-gen if desired (optional, but good practice. User didn't ask to skip, so we'll overwrite as 'overwrite' implies logic elsewhere or just do it)
    # fal.ai costs money/credits, but user said "generate them here", implying a run.
    
    try:
        result = fal_client.subscribe(
            "fal-ai/flux/schnell", 
            arguments={
                "prompt": step["prompt"],
                "image_size": { "width": 1024, "height": 1024 },
                "num_inference_steps": 4,
                "seed": 42 + step['order'] # Varied seed slightly per step for variety if prompt is same (not case here)
            }
        )
        
        if result and "images" in result and result["images"]:
            image_url = result["images"][0]["url"]
            
            import urllib.request
            urllib.request.urlretrieve(image_url, save_path)
            print(f"saved to {save_path}")
            return save_path
            
    except Exception as e:
        print(f"Error generating {filename}: {e}")
        return None

def create_sprite_sheet(image_paths: List[Path], output_filename: str = "prerequisites_sprite_sheet.jpg"):
    """Combine images into a horizontal sprite sheet"""
    if not Image:
        print("Skipping sprite sheet creation (Pillow not installed)")
        return

    try:
        images = [Image.open(p) for p in image_paths if p]
        if not images:
            return

        # Assuming all images are same size (they should be)
        width, height = images[0].size
        
        # Horizontal strip
        total_width = width * len(images)
        total_height = height
        
        sprite_sheet = Image.new('RGB', (total_width, total_height))
        
        for i, img in enumerate(images):
            sprite_sheet.paste(img, (i * width, 0))
            
        save_path = OUTPUT_DIR / output_filename
        sprite_sheet.save(save_path, quality=95)
        print(f"✅ Sprite sheet saved: {save_path}")
        
    except Exception as e:
        print(f"❌ Error creating sprite sheet: {e}")

def main():
    print("🚀 Starting Prerequisites Generation...")
    
    # Check API Key
    if not os.environ.get("FAL_KEY"):
         print("Warning: FAL_KEY not set. Attempting to run anyway (might fail if not authorized).")

    generated_files = []
    
    # Generate each step
    for step in STEPS:
        path = generate_image(step)
        if path:
            generated_files.append(path)
    
    # Create Sprite Sheet
    if len(generated_files) == len(STEPS):
        create_sprite_sheet(generated_files)
    else:
        print("⚠️ Some steps failed, skipping sprite sheet creation.")
    
    print("Done.")

if __name__ == "__main__":
    main()

"""
Bulk Illustration Generator
This script searches for images using Google Custom Search API and transforms them using fal.ai's image-to-image models.
It falls back to text-to-image generation if the Google search fails or returns no results.
"""
import os
import requests
import fal_client
import yaml
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from ../.env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# 1. Setup Keys
# Keys should be set in environment variables or .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# FAL_KEY is typically picked up by the client from environment
if "FAL_KEY" not in os.environ:
    # Attempt to load from .env or similar if needed, otherwise rely on system env
    pass

# Configuration
OUTPUT_DIR = Path(r"C:\projects\fal.ai\3_Simulation\Feb1Youtube\generated_illustrations")
DATA_PATH = Path(r"C:\projects\fal.ai\3_Simulation\Feb1Youtube\_source\batch_generation_data.yaml")

def load_config() -> list:
    """Load the images section from the batch generation data YAML."""
    if not DATA_PATH.exists():
        print(f"Error: Configuration file not found at {DATA_PATH}")
        return []
    
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('images', [])
    except Exception as e:
        print(f"Error loading YAML: {e}")
        return []

def get_google_image(query: str) -> Optional[str]:
    """
    Search for an image using Google Custom Search API.
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("Warning: Google API keys not set. Skipping search.")
        return None

    print(f"🔍 Searching Google for: '{query}'...")
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': GOOGLE_CSE_ID,
        'key': GOOGLE_API_KEY,
        'searchType': 'image',
        'num': 1,
        'safe': 'active'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            link = data['items'][0]['link']
            print(f"   ✓ Found image: {link}")
            return link
        else:
            print(f"   ✗ No results found for query: {query}")
            return None
    except Exception as e:
        print(f"   ✗ Error searching Google: {e}")
        return None

def illustrate_image(image_url: str, prompt: str, model: str = "fal-ai/flux/dev/image-to-image") -> Optional[str]:
    """
    Transform the image using fal.ai image-to-image model.
    """
    if not image_url:
        return None
        
    print(f"🎨 Transforming image with prompt: {prompt[:50]}...")
    try:
        result = fal_client.subscribe(
            model,
            arguments={
                "image_url": image_url,
                "prompt": prompt,
                "strength": 0.75, # Balanced strength for transformation
                "num_inference_steps": 28,
                "guidance_scale": 3.5
            }
        )
        if result and 'images' in result and len(result['images']) > 0:
            return result['images'][0]['url']
        return None
    except Exception as e:
        print(f"   ✗ Error transforming image: {e}")
        return None

def generate_text_to_image(prompt: str, model: str = "fal-ai/flux/dev") -> Optional[str]:
    """
    Generate an image from scratch using text-to-image (Fallback).
    """
    print(f"🎨 Generating from text (Fallback): {prompt[:50]}...")
    try:
        result = fal_client.subscribe(
            model,
            arguments={
                "prompt": prompt,
                "image_size": {
                    "width": 1920,
                    "height": 1080
                },
                "num_inference_steps": 30,
                "guidance_scale": 3.5
            }
        )
        if result and 'images' in result and len(result['images']) > 0:
            return result['images'][0]['url']
        return None
    except Exception as e:
        print(f"   ✗ Error generating image: {e}")
        return None

def save_image(url: str, filename: str):
    """Download and save the image in both PNG and JPG formats."""
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        filepath = OUTPUT_DIR / filename
        
        # Determine extension if not in filename, though we assume jpg/png
        if not filepath.suffix:
            filepath = filepath.with_suffix(".png")

        print(f"💾 Saving to {filepath}...")
        import urllib.request
        urllib.request.urlretrieve(url, filepath)
        print("   ✓ Saved PNG.")
        
        # Also save as JPG
        jpg_filepath = filepath.with_suffix(".jpg")
        print(f"💾 Converting and saving to {jpg_filepath}...")
        img = Image.open(filepath)
        # Convert RGBA to RGB if necessary (JPG doesn't support transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            rgb_img.save(jpg_filepath, 'JPEG', quality=95)
        else:
            img.save(jpg_filepath, 'JPEG', quality=95)
        print("   ✓ Saved JPG.")
    except Exception as e:
        print(f"   ✗ Error saving image: {e}")

def process_batch():
    items = load_config()
    if not items:
        print("No items to process.")
        return

    print(f"Found {len(items)} items in batch configuration.")
    
    for item in items:
        name = item.get('name', 'unnamed')
        prompt = item.get('prompt', '')
        # Determine search query: explicit 'search_query' > 'name' > None
        search_query = item.get('search_query')
        if not search_query:
            # Simple heuristic: use name logic or skip search if not intended
            # For this requirement, we treat 'name' as a potential query if sensible
            search_query = name.replace('_', ' ')
        
        print(f"\n[{name.upper()}] Processing...")

        final_url = None
        
        # 1. Try Google Search + Image-to-Image
        source_url = get_google_image(search_query)
        
        if source_url:
            # If search succeeded, try to illustrate it
            final_url = illustrate_image(source_url, prompt)
        
        # 2. Fallback: Text-to-Image (Estimate)
        if not final_url:
            if source_url:
                print("   ⚠️ Search succeeded but transformation failed. Fallback to Text-to-Image.")
            else:
                print("   ⚠️ Search failed or no results. Fallback to Text-to-Image.")
            
            final_url = generate_text_to_image(prompt)

        # 3. Save Result
        if final_url:
            filename = f"{name}_illustration.png"
            save_image(final_url, filename)
        else:
            print(f"   ❌ Failed to generate any image for {name}")

if __name__ == "__main__":
    process_batch()

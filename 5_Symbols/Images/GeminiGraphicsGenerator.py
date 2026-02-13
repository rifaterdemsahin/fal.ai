#!/usr/bin/env python3
"""
Gemini Graphics Generator
Generates graphics using Google Gemini API (Imagen 4) based on source_graphics.md
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Google Generative AI
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ google-genai not installed. Run: pip install google-genai")
    exit(1)

# Configuration
INPUT_DIR = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/input")
OUTPUT_DIR = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Image generation settings
IMAGE_SETTINGS = {
    "model": "imagen-4.0-generate-001",
    "width": 1920,
    "height": 1080,
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

def parse_graphics_markdown(file_path: Path) -> List[Dict]:
    """Parse source_graphics.md and extract graphic prompts"""
    prompts = []
    
    if not file_path.exists():
        print(f"⚠️  Graphics file not found: {file_path}")
        return prompts
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse graphics sections by "#### Graphic N:"
    graphic_pattern = re.compile(
        r'#### Graphic (\d+): ([^\n]+)\n(.*?)(?=#### Graphic|\n---\n|\Z)',
        re.DOTALL
    )
    
    matches = graphic_pattern.findall(content)
    
    for num, title, body in matches:
        # Extract details
        graphic_type = ""
        visual = ""
        style = ""
        text_content = ""
        
        for line in body.split('\n'):
            line = line.strip()
            if line.startswith('- **Type:**'):
                graphic_type = line.split('**Type:**')[-1].strip()
            elif line.startswith('- **Visual:**'):
                visual = line.split('**Visual:**')[-1].strip()
            elif line.startswith('- **Style:**'):
                style = line.split('**Style:**')[-1].strip()
            elif line.startswith('- **Text:**'):
                text_content = line.split('**Text:**')[-1].strip()
        
        # Build prompt
        prompt_parts = [
            "Professional video graphic asset",
            f"Title: {title}",
        ]
        
        if graphic_type:
            prompt_parts.append(f"Type: {graphic_type}")
        if visual:
            prompt_parts.append(f"Visual elements: {visual}")
        if style:
            prompt_parts.append(f"Style: {style}")
        if text_content:
            prompt_parts.append(f"Text displayed: {text_content}")
        
        prompt_parts.extend([
            "Modern tech aesthetic",
            "GitHub colors (#24292e black, #0366d6 blue)",
            "Clean minimalist design",
            "Sharp edges, professional look",
            "16:9 aspect ratio for video overlay"
        ])
        
        prompt = ". ".join(prompt_parts)
        
        prompts.append({
            "id": f"graphic_{int(num):02d}",
            "name": title.strip().lower().replace(' ', '_').replace('"', ''),
            "prompt": prompt,
            "scene": f"Graphic {num}",
            "category": "graphic",
            "type": graphic_type,
        })
    
    return prompts

def get_additional_graphics() -> List[Dict]:
    """Additional commonly needed graphics"""
    return [
        {
            "id": "graphic_stat_240",
            "name": "240_workflows_stat",
            "prompt": "Large animated number display showing '240' in bold modern typography. Tech startup style infographic. GitHub blue (#0366d6) accent color. Clean dark background (#24292e). Label: 'Automated Workflows'. Professional video asset. 16:9 aspect ratio.",
            "scene": "Stats Display",
            "category": "graphic",
            "type": "stat_counter"
        },
        {
            "id": "graphic_speed_1000x",
            "name": "speed_1000x_multiplier",
            "prompt": "Dynamic speed multiplier graphic showing '1000x FASTER' in bold typography with motion blur effect. Racing stripes and speed lines. Tech blue accent (#0366d6). Dark professional background. Video overlay asset. 16:9 aspect ratio.",
            "scene": "Speed Display",
            "category": "graphic",
            "type": "stat_display"
        },
        {
            "id": "graphic_vs_comparison",
            "name": "static_vs_dynamic_comparison",
            "prompt": "Split screen comparison graphic. Left side: 'Static Rules' with stone/rigid visual. Right side: 'Dynamic AI' with fluid mercury/adaptive visual. Modern tech design. Clean typography. Contrasting visual styles. 16:9 video overlay.",
            "scene": "Comparison",
            "category": "graphic",
            "type": "comparison"
        },
        {
            "id": "graphic_process_steps",
            "name": "3_step_process_checklist",
            "prompt": "Animated checklist graphic showing 3 steps: '1. Clone Repository ✓', '2. Setup Environment ✓', '3. Run Agent ✓'. Modern tech UI style. GitHub colors. Progress indicator design. Clean sidebar overlay. 16:9 aspect ratio.",
            "scene": "Process Steps",
            "category": "graphic",
            "type": "checklist"
        },
        {
            "id": "graphic_family_badge",
            "name": "family_friendly_badge",
            "prompt": "Warm family-friendly badge icon with shield shape. Text: 'Family-Tested Solution'. Soft rounded edges, warm gold and blue colors. Trust and safety iconography. Professional but approachable. Video overlay asset.",
            "scene": "Badge",
            "category": "graphic",
            "type": "badge"
        },
        {
            "id": "graphic_consistency_quote",
            "name": "consistency_magic_shield_quote",
            "prompt": "Inspirational quote graphic: 'Consistency is Your Magic Shield'. Large elegant typography on dark background. Golden accent effects. Magical sparkle elements. Professional video title card. 16:9 aspect ratio.",
            "scene": "Quote",
            "category": "graphic",
            "type": "quote_card"
        },
    ]

def generate_image_gemini(client, prompt: str) -> Optional[bytes]:
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

def generate_all_graphics(prompts: List[Dict], client, output_dir: Path) -> List[Dict]:
    """Generate all graphics from prompts"""
    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"\n{'='*60}")
    print("🎨 GEMINI GRAPHICS GENERATOR")
    print(f"   Total graphics: {len(prompts)}")
    print(f"   Output: {output_dir}")
    print("="*60)
    
    for i, item in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] Generating: {item.get('name', item.get('id'))}")
        print(f"   Category: {item.get('category', 'graphic')}")
        print(f"   Type: {item.get('type', 'unknown')}")
        print(f"   Prompt: {item['prompt'][:80]}...")
        
        image_data = generate_image_gemini(client, item['prompt'])
        
        if image_data:
            # Generate filename
            safe_name = item.get('name', item.get('id', 'graphic'))
            safe_name = safe_name.replace(' ', '_').replace(':', '').replace('"', '').lower()
            filename = f"gfx_{safe_name}_{timestamp}.png"
            
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
    graphics_file = INPUT_DIR / "source_graphics.md"
    parsed_graphics = parse_graphics_markdown(graphics_file)
    additional_graphics = get_additional_graphics()
    
    all_prompts = parsed_graphics + additional_graphics
    
    print(f"\n📊 Found graphics:")
    print(f"   • From source_graphics.md: {len(parsed_graphics)}")
    print(f"   • Additional graphics: {len(additional_graphics)}")
    print(f"   • Total: {len(all_prompts)}")
    
    if not all_prompts:
        print("❌ No graphics found to generate")
        return
    
    # Confirm before proceeding
    response = input("\n🤔 Proceed with generation? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled by user")
        return
    
    # Generate graphics
    results = generate_all_graphics(all_prompts, client, OUTPUT_DIR)
    
    # Summary
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\n{'='*60}")
    print("📊 GENERATION SUMMARY")
    print("="*60)
    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    # Save summary
    summary_path = OUTPUT_DIR / f"gemini_graphics_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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

#!/usr/bin/env python3
"""
Gemini Green Screen Background Generator
Generates A-roll backgrounds for green screen compositing using Imagen 4.
Each scene has a unique environment that the host stands in front of.
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

IMAGE_SETTINGS = {
    "model": "imagen-4.0-generate-001",
}

# ─── Green Screen Background Definitions ───────────────────────────────────
# Each entry maps a storyboard scene to the background the host will be
# composited onto.  Prompts are tailored for *empty* environments (no people)
# with correct lighting and perspective for medium / wide host shots.

AROLL_BACKGROUNDS = [
    # Scene 1 – The Heavy Mic (00:00:00 – 00:00:10)
    {
        "id": "bg_01_heavy_mic",
        "name": "Heavy Mic Stage",
        "scene": "Scene 1: The Heavy Mic",
        "timecode": "00:00:00 - 00:00:10",
        "prompt": (
            "Empty dramatic stage, single spotlight from above, dark moody atmosphere, "
            "polished black floor with reflections, theatrical fog, volumetric light beams, "
            "wide shot perspective, no people, cinematic lighting, 8K, ultra detailed, "
            "film production background plate, 16:9 aspect ratio"
        ),
    },
    # Scene 2 – The Pivot (00:00:10 – 00:00:35)
    {
        "id": "bg_02_pivot",
        "name": "Pivot Office",
        "scene": "Scene 2: The Pivot",
        "timecode": "00:00:10 - 00:00:35",
        "prompt": (
            "Modern open-plan office, blurred background, warm ambient lighting, "
            "desks with monitors, busy city visible through floor-to-ceiling windows, "
            "soft bokeh, depth of field, no people, corporate startup aesthetic, "
            "cinematic color grading, background plate for green screen, 16:9 aspect ratio"
        ),
    },
    # Scene 3 – Statues vs. Mercury (00:00:35 – 00:00:48)
    {
        "id": "bg_03a_statues",
        "name": "Stone Statue Hall",
        "scene": "Scene 3A: Static Rules",
        "timecode": "00:00:35 - 00:00:48",
        "prompt": (
            "Grand museum hall filled with frozen stone statues, marble columns, "
            "classical architecture, dim moody lighting, dust particles in air, "
            "symmetrical composition, no people, wide shot, ancient Roman aesthetic, "
            "cinematic atmosphere, background plate, 16:9 aspect ratio"
        ),
    },
    {
        "id": "bg_03b_mercury",
        "name": "Mercury Lab",
        "scene": "Scene 3B: Dynamic AI",
        "timecode": "00:00:35 - 00:00:48",
        "prompt": (
            "Futuristic laboratory with liquid mercury flowing in glass tubes, "
            "neon blue and silver reflections, sci-fi aesthetic, clean surfaces, "
            "holographic displays, dark background with electric highlights, no people, "
            "cyberpunk inspired, cinematic lighting, background plate, 16:9 aspect ratio"
        ),
    },
    # Scene 4 – The Clone Lab (00:00:48 – 00:03:52)
    {
        "id": "bg_04_clone_lab",
        "name": "Clone Lab",
        "scene": "Scene 4: The Clone Lab",
        "timecode": "00:00:48 - 00:03:52",
        "prompt": (
            "High-tech developer workspace, multiple large monitors showing code, "
            "dark room with RGB ambient lighting, terminal windows with green text, "
            "server racks in background, GitHub octocat logo on wall screen, "
            "no people, hacker aesthetic, cinematic, background plate, 16:9 aspect ratio"
        ),
    },
    # Scene 5 – The Evolution / 3D Printer (00:03:52 – 00:05:50)
    {
        "id": "bg_05_evolution",
        "name": "Evolution Workshop",
        "scene": "Scene 5: The Evolution",
        "timecode": "00:03:52 - 00:05:50",
        "prompt": (
            "Futuristic workshop with large industrial 3D printer in the center, "
            "glowing blue laser printing a human-shaped form, metallic surfaces, "
            "steam and particles in the air, warm industrial lighting, "
            "no people, sci-fi factory aesthetic, cinematic wide shot, "
            "background plate for green screen, 16:9 aspect ratio"
        ),
    },
    # Scene 6 – The Nursery (00:05:50 – 00:06:36)
    {
        "id": "bg_06_nursery",
        "name": "Nursery Room",
        "scene": "Scene 6: The Nursery",
        "timecode": "00:05:50 - 00:06:36",
        "prompt": (
            "Cozy children's nursery room at night, soft warm lighting, "
            "glowing nightlight shaped like the GitHub octocat logo on bedside table, "
            "comfortable bed with soft blankets, plush toys, stars on ceiling, "
            "no people, family-friendly atmosphere, warm color palette, "
            "intimate cinematic lighting, background plate, 16:9 aspect ratio"
        ),
    },
    # Scene 7 – The Crystal Ball / Tech Companies (00:06:36 – 00:08:26)
    {
        "id": "bg_07_crystal_ball",
        "name": "Crystal Ball Tech Room",
        "scene": "Scene 7: The Crystal Ball",
        "timecode": "00:06:36 - 00:08:26",
        "prompt": (
            "Mystical tech showroom, dark environment with floating holographic logos, "
            "Google, Microsoft, and Amazon logos glowing softly in the air, "
            "crystal ball on pedestal in center emitting soft blue light, "
            "Alexa smart speaker on table, ethereal fog, magical tech atmosphere, "
            "no people, cinematic, background plate, 16:9 aspect ratio"
        ),
    },
    # Scene 8 – The Engine Room / Speed (00:08:26 – 00:09:01)
    {
        "id": "bg_08_engine_room",
        "name": "Engine Room",
        "scene": "Scene 8: The Engine Room",
        "timecode": "00:08:26 - 00:09:01",
        "prompt": (
            "Industrial engine room with massive spinning gears and clockwork mechanisms, "
            "giant clock face on the wall with hands spinning fast, motion blur on gears, "
            "steam pipes, orange and blue industrial lighting, sparks flying, "
            "no people, steampunk meets high-tech aesthetic, dynamic energy, "
            "cinematic wide shot, background plate, 16:9 aspect ratio"
        ),
    },
    # Scene 9 – The Digital Feast / LLM Options (00:09:01 – 00:11:45)
    {
        "id": "bg_09_digital_feast",
        "name": "Digital Feast Table",
        "scene": "Scene 9: The Digital Feast",
        "timecode": "00:09:01 - 00:11:45",
        "prompt": (
            "Grand futuristic banquet hall, long elegant table covered with glowing tablets "
            "and screens displaying AI logos (Claude, ChatGPT, DeepSeek, Gemini), "
            "holographic menus floating above each tablet, ambient blue and purple lighting, "
            "no people, abundant tech feast aesthetic, overhead perspective elements, "
            "cinematic atmosphere, background plate, 16:9 aspect ratio"
        ),
    },
    # Scene 10 – The Power Station / Demo (00:11:45 – 00:13:15)
    {
        "id": "bg_10_power_station",
        "name": "Power Station",
        "scene": "Scene 10: The Power Station",
        "timecode": "00:11:45 - 00:13:15",
        "prompt": (
            "Dark laboratory with a glass bottle containing a captured lightning bolt, "
            "electrical arcs and plasma inside glass container, Tesla coil aesthetic, "
            "n8n workflow diagrams projected on walls, "
            "blue and white electric glow illuminating the room, "
            "no people, powerful contained energy, cinematic close-up environment, "
            "background plate, 16:9 aspect ratio"
        ),
    },
    # Scene 11 – The Tool Shed / GitHub Evolution (00:13:15 – 00:17:24)
    {
        "id": "bg_11_tool_shed",
        "name": "Tool Shed Workshop",
        "scene": "Scene 11: The Tool Shed",
        "timecode": "00:13:15 - 00:17:24",
        "prompt": (
            "Energetic workshop with vibrating toolbox emitting blue GitHub-colored energy, "
            "tools floating in the air surrounded by glowing particles, "
            "workbench with commit history scrolling on monitors, CI/CD pipeline visualization, "
            "green checkmarks floating in the air, no people, "
            "active workshop aesthetic, cinematic lighting, background plate, 16:9 aspect ratio"
        ),
    },
    # Scene 12 – The Balcony / Conclusion (00:17:24 – End)
    {
        "id": "bg_12_balcony",
        "name": "Balcony Cityscape",
        "scene": "Scene 12: The Balcony",
        "timecode": "00:17:24 - End",
        "prompt": (
            "Stunning futuristic cityscape viewed from a high-rise balcony at golden hour, "
            "flying drones building skyscrapers in the distance, gleaming towers, "
            "warm sunset glow, clouds below eye level, glass railing in foreground, "
            "no people, aspirational sci-fi utopia, epic scale, "
            "cinematic wide establishing shot, background plate, 16:9 aspect ratio"
        ),
    },
]


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


def generate_image(client, prompt: str) -> Optional[bytes]:
    """Generate a single background image using Imagen 4"""
    try:
        response = client.models.generate_images(
            model=IMAGE_SETTINGS["model"],
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        if response.generated_images and len(response.generated_images) > 0:
            return response.generated_images[0].image.image_bytes
        return None
    except Exception as e:
        print(f"   ❌ Generation error: {e}")
        return None


def main():
    """Generate all A-roll green screen backgrounds"""
    load_env()

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment")
        return

    client = genai.Client(api_key=api_key)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = []

    print(f"\n{'='*60}")
    print("🟩 GEMINI GREEN SCREEN BACKGROUND GENERATOR")
    print(f"   Backgrounds to generate: {len(AROLL_BACKGROUNDS)}")
    print(f"   Output: {OUTPUT_DIR}")
    print("="*60)

    # Preview
    for i, bg in enumerate(AROLL_BACKGROUNDS, 1):
        print(f"   {i:2d}. [{bg['timecode']}] {bg['name']}")

    response = input("\n🤔 Proceed with generation? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled by user")
        return

    for i, bg in enumerate(AROLL_BACKGROUNDS, 1):
        print(f"\n[{i}/{len(AROLL_BACKGROUNDS)}] Generating: {bg['name']}")
        print(f"   Scene: {bg['scene']} ({bg['timecode']})")
        print(f"   Prompt: {bg['prompt'][:90]}...")

        image_data = generate_image(client, bg['prompt'])

        if image_data:
            safe_name = re.sub(r'[^\w\-]', '_', bg['id'].lower())
            safe_name = re.sub(r'_+', '_', safe_name).strip('_')
            filename = f"{safe_name}_{timestamp}.png"

            filepath = OUTPUT_DIR / filename
            with open(filepath, 'wb') as f:
                f.write(image_data)
            print(f"   ✅ Saved: {filename}")

            # Save metadata
            meta_path = OUTPUT_DIR / filename.replace('.png', '.json')
            with open(meta_path, 'w') as f:
                json.dump({
                    **bg,
                    "filename": filename,
                    "generated_at": timestamp,
                    "model": IMAGE_SETTINGS["model"],
                    "purpose": "green_screen_background",
                }, f, indent=2)

            results.append({"success": True, "name": bg['name'], "filename": filename})
        else:
            print(f"   ❌ Failed")
            results.append({"success": False, "name": bg['name'], "error": "Generation failed"})

    # ── Summary ──
    ok = [r for r in results if r["success"]]
    fail = [r for r in results if not r["success"]]

    print(f"\n{'='*60}")
    print("📊 GENERATION SUMMARY")
    print("="*60)
    print(f"✅ Successful: {len(ok)}/{len(results)}")
    print(f"❌ Failed:     {len(fail)}/{len(results)}")

    if ok:
        print("\n✅ Generated backgrounds:")
        for r in ok:
            print(f"   • {r['name']} → {r['filename']}")
    if fail:
        print("\n❌ Failed backgrounds:")
        for r in fail:
            print(f"   • {r['name']}")

    summary_path = OUTPUT_DIR / f"greenscreen_bg_summary_{timestamp}.json"
    with open(summary_path, 'w') as f:
        json.dump({
            "total": len(results),
            "successful": len(ok),
            "failed": len(fail),
            "results": results,
        }, f, indent=2)

    print(f"\n💾 Summary: {summary_path}")
    print("✅ Done!")


if __name__ == "__main__":
    main()

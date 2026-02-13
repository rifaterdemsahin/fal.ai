#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Memory Palace
Project: The Agentic Era
Generates memory palace imagery for each storyboard scene.
Each image is a surreal, fantastical locus in a memory palace
that visually encodes the key concept of the scene.

Cost: ~$0.01/image × 12 scenes = ~$0.12 total (budget: $1.00)
"""

import os
import json
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# fal.ai client
try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

# Configuration
OUTPUT_DIR = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Model config — flux/schnell is ~$0.01 per image
MODEL = "fal-ai/flux/schnell"
COST_PER_IMAGE = 0.01
BUDGET_LIMIT = 1.00

IMAGE_SIZE = {"width": 1920, "height": 1080}
NUM_INFERENCE_STEPS = 4  # schnell is optimised for 4 steps

# ─── Memory Palace Loci — one per storyboard scene ─────────────────────────

GENERATION_QUEUE = [
    {
        "id": "MP.01",
        "name": "mp_01_heavy_mic",
        "scene": "Scene 1: The Heavy Mic (00:00:00 - 00:00:10)",
        "prompt": (
            "A surreal memory palace room: a colossal golden microphone, taller than a person, "
            "stands on a polished obsidian pedestal in a grand cathedral-like space, dramatic "
            "spotlight from above, swirling golden particle motes, gothic arched ceiling, "
            "volumetric light beams, hyper-detailed, fantasy illustration style, 8K, "
            "cinematic wide shot, no people"
        ),
    },
    {
        "id": "MP.02",
        "name": "mp_02_the_pivot",
        "scene": "Scene 2: The Pivot (00:00:10 - 00:00:35)",
        "prompt": (
            "A surreal memory palace room: a giant compass needle embedded in a marble floor, "
            "spinning in a circular chamber with walls made of flowing water, people-shaped "
            "silhouettes frozen mid-step, warm amber light from a skylight above, ancient "
            "navigational maps carved into the walls, dreamlike atmosphere, fantasy illustration, "
            "8K, cinematic, no people"
        ),
    },
    {
        "id": "MP.03",
        "name": "mp_03_statues_vs_mercury",
        "scene": "Scene 3: Statues vs Mercury (00:00:35 - 00:00:48)",
        "prompt": (
            "A surreal memory palace room split in two: left half has frozen grey stone statues "
            "trapped in a cold, cracked marble hall; right half has a living mercury figure "
            "flowing and shifting in a liquid chrome laboratory, dramatic contrast between "
            "rigid and fluid, split-screen composition, hyper-detailed fantasy illustration, "
            "8K, cinematic lighting, no people"
        ),
    },
    {
        "id": "MP.04",
        "name": "mp_04_clone_lab",
        "scene": "Scene 4: The Clone Lab (00:00:48 - 00:03:52)",
        "prompt": (
            "A surreal memory palace room: a vast futuristic laboratory with rows of glass "
            "cloning pods, glowing green terminal screens showing scrolling code, holographic "
            "DNA helixes floating in the air, dark metallic surfaces with neon reflections, "
            "cyberpunk meets ancient alchemy aesthetic, hyper-detailed, fantasy illustration, "
            "8K, cinematic wide shot, no people"
        ),
    },
    {
        "id": "MP.05",
        "name": "mp_05_evolution",
        "scene": "Scene 5: The Evolution (00:03:52 - 00:05:50)",
        "prompt": (
            "A surreal memory palace room: a giant 3D printer the size of a building, slowly "
            "materializing a glowing humanoid figure layer by layer, surrounded by floating "
            "geometric evolution diagrams, butterfly chrysalis motifs, bioluminescent plants, "
            "futuristic greenhouse atmosphere, hyper-detailed, fantasy illustration, 8K, "
            "cinematic, no people"
        ),
    },
    {
        "id": "MP.06",
        "name": "mp_06_nursery",
        "scene": "Scene 6: The Nursery (00:05:50 - 00:06:36)",
        "prompt": (
            "A surreal memory palace room: a warm, cozy nursery with an enormous glowing "
            "GitHub Octocat nightlight casting soft purple light, floating code-block mobiles "
            "hanging from the ceiling, a cradle made of circuit boards wrapped in soft blankets, "
            "pastel colors, dreamy soft-focus atmosphere, fantasy illustration, 8K, "
            "cinematic, no people"
        ),
    },
    {
        "id": "MP.07",
        "name": "mp_07_crystal_ball",
        "scene": "Scene 7: The Crystal Ball (00:06:36 - 00:08:26)",
        "prompt": (
            "A surreal memory palace room: a massive crystal ball on an ornate bronze stand, "
            "inside the ball swirl miniature floating tech company logos and smart speakers, "
            "mystical purple and blue fog curls around the base, ancient fortune-teller's "
            "chamber with star-mapped ceiling, candles and fiber-optic cables intertwined, "
            "hyper-detailed, fantasy illustration, 8K, cinematic, no people"
        ),
    },
    {
        "id": "MP.08",
        "name": "mp_08_engine_room",
        "scene": "Scene 8: The Engine Room (00:08:26 - 00:09:01)",
        "prompt": (
            "A surreal memory palace room: a steampunk engine room with massive brass gears "
            "and spinning clock mechanisms, a giant clock face showing blurred hands moving "
            "at 1000x speed, steam pipes, pressure gauges, copper boilers, sparks flying, "
            "industrial Victorian aesthetic meets sci-fi, hyper-detailed, fantasy illustration, "
            "8K, cinematic, no people"
        ),
    },
    {
        "id": "MP.09",
        "name": "mp_09_digital_feast",
        "scene": "Scene 9: The Digital Feast (00:09:01 - 00:11:45)",
        "prompt": (
            "A surreal memory palace room: a grand banquet table stretching into infinity, "
            "covered with hundreds of glowing tablets and screens instead of food, each "
            "screen showing different data visualizations, floating holographic fruit and "
            "digital wine glasses, baroque dining hall with chandelier made of circuit boards, "
            "hyper-detailed, fantasy illustration, 8K, cinematic overhead angle, no people"
        ),
    },
    {
        "id": "MP.10",
        "name": "mp_10_power_station",
        "scene": "Scene 10: The Power Station (00:11:45 - 00:13:15)",
        "prompt": (
            "A surreal memory palace room: a single giant glass bottle containing a captured "
            "lightning bolt, arcing with electric blue energy, placed on a Tesla coil pedestal "
            "in a dark industrial power station, copper wires radiating outward, electromagnetic "
            "aurora dancing on the ceiling, hyper-detailed, fantasy illustration, 8K, "
            "cinematic, no people"
        ),
    },
    {
        "id": "MP.11",
        "name": "mp_11_tool_shed",
        "scene": "Scene 11: The Tool Shed (00:13:15 - 00:17:24)",
        "prompt": (
            "A surreal memory palace room: a magical workshop with a vibrating toolbox that "
            "radiates purple energy waves, tools floating in mid-air — wrenches, hammers, "
            "screwdrivers orbiting like planets, walls covered in glowing blueprints, "
            "a workbench made of stacked code repositories, sparks and particles everywhere, "
            "hyper-detailed, fantasy illustration, 8K, cinematic, no people"
        ),
    },
    {
        "id": "MP.12",
        "name": "mp_12_balcony",
        "scene": "Scene 12: The Balcony (00:17:24 - End)",
        "prompt": (
            "A surreal memory palace room: a grand marble balcony overlooking a vast futuristic "
            "city built entirely by drones, towers of light, flying vehicles, holographic "
            "billboards, golden sunset sky, sweeping vista, a telescope on the balcony railing "
            "pointing toward the horizon, sense of infinite possibility, hyper-detailed, "
            "fantasy illustration, 8K, cinematic wide shot, no people"
        ),
    },
]

def generate_asset(asset_config: Dict, idx: int, total: int, cost_so_far: float, timestamp: str) -> Dict:
    """Generate a single memory palace asset using fal.ai"""
    name = asset_config["name"]
    scene = asset_config["scene"]

    print(f"\n[{idx}/{total}] Generating: {name}")
    print(f"   Scene: {scene}")
    print(f"   Cost so far: ${cost_so_far:.2f} / ${BUDGET_LIMIT:.2f}")

    # Budget guard
    if cost_so_far + COST_PER_IMAGE > BUDGET_LIMIT:
        msg = f"Budget exceeded (${cost_so_far:.2f} + ${COST_PER_IMAGE:.2f} > ${BUDGET_LIMIT:.2f})"
        print(f"   ⛔ {msg}")
        return {"success": False, "error": msg}

    try:
        result = fal_client.subscribe(
            MODEL,
            arguments={
                "prompt": asset_config["prompt"],
                "image_size": IMAGE_SIZE,
                "num_inference_steps": NUM_INFERENCE_STEPS,
                "num_images": 1,
            },
        )

        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            filename = f"{name}_{timestamp}.png"
            image_path = OUTPUT_DIR / filename
            urllib.request.urlretrieve(image_url, image_path)
            print(f"   ✅ Saved: {filename}")
            return {
                "success": True,
                "url": image_url,
                "local_path": str(image_path),
                "filename": filename,
            }
        else:
            print("   ❌ No images returned")
            return {"success": False, "error": "No images returned"}

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {"success": False, "error": str(e)}


def main():
    """Main execution — no interactive prompt."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    total = len(GENERATION_QUEUE)
    estimated_cost = total * COST_PER_IMAGE

    print("=" * 60)
    print("🧠 FAL.AI MEMORY PALACE GENERATOR")
    print(f"   Model: {MODEL} (~${COST_PER_IMAGE}/image)")
    print(f"   Scenes: {total}")
    print(f"   Estimated cost: ${estimated_cost:.2f} (budget: ${BUDGET_LIMIT:.2f})")
    print(f"   Output: {OUTPUT_DIR}")
    print("=" * 60)

    # List scenes
    for i, item in enumerate(GENERATION_QUEUE, 1):
        print(f"  {i:>3}. {item['scene']}")

    print(f"\n💰 Total estimated cost: ${estimated_cost:.2f}")

    # Check API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("\n❌ ERROR: FAL_KEY not set. export FAL_KEY='your-key'")
        return

    # Generate
    results = []
    cost_so_far = 0.0

    for i, asset in enumerate(GENERATION_QUEUE, 1):
        result = generate_asset(asset, i, total, cost_so_far, timestamp)
        results.append({"asset_id": asset["id"], "name": asset["name"], **result})
        if result["success"]:
            cost_so_far += COST_PER_IMAGE

    # Summary
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print("\n" + "=" * 60)
    print("📊 GENERATION SUMMARY")
    print("=" * 60)
    print(f"✅ Successful: {len(successful)}/{total}")
    print(f"❌ Failed:     {len(failed)}/{total}")
    print(f"💰 Total cost: ${cost_so_far:.2f} / ${BUDGET_LIMIT:.2f} budget")

    if successful:
        print(f"\n✅ Generated memory palace images:")
        for r in successful:
            print(f"   • {r['name']} → {r['filename']}")

    if failed:
        print(f"\n❌ Failed:")
        for r in failed:
            print(f"   • {r['name']} — {r.get('error', 'unknown')}")

    # Save summary JSON
    summary_path = OUTPUT_DIR / f"memory_palace_summary_{timestamp}.json"
    with open(summary_path, "w") as f:
        json.dump(
            {
                "generator": "BatchAssetGeneratorMemoryPalace",
                "model": MODEL,
                "timestamp": timestamp,
                "total": total,
                "successful": len(successful),
                "failed": len(failed),
                "total_cost_usd": cost_so_far,
                "budget_usd": BUDGET_LIMIT,
                "results": results,
            },
            f,
            indent=2,
        )

    print(f"\n💾 Summary: {summary_path}")
    print("✅ Done!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Infographics
Project: The Agentic Era
Generates data visualization and infographic overlays for each scene.

Derived from: 3_Simulation/2026-02-15/input/source_graphics.md
Cost: ~$0.01/image × ~25 infographics = ~$0.25 (budget: $0.50)
"""

import os
import json
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import Dict, List

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
BUDGET_LIMIT = 0.50

IMAGE_SIZE = {"width": 1920, "height": 1080}
NUM_INFERENCE_STEPS = 4

# ─── Infographic Queue — derived from source_graphics.md ────────────────────

GENERATION_QUEUE = [
    # --- Scene 1-2: Opening & The Pivot ---
    {
        "id": "IG.01",
        "name": "ig_01_240_workflows_stat",
        "scene": "Scene 1-2: Opening (00:00:15)",
        "prompt": (
            "Clean modern infographic stat card on dark background: large bold glowing number '240' "
            "in white with gold accent, subtitle 'Workflows Managed' underneath in sans-serif font, "
            "subtle animated particle trail behind the number, minimal tech aesthetic, "
            "GitHub dark theme colors #24292e background, accent gold #FFD700, 16:9, 8K"
        ),
    },
    {
        "id": "IG.02",
        "name": "ig_02_pivot_title_card",
        "scene": "Scene 2: The Pivot (00:00:20)",
        "prompt": (
            "Professional title card infographic: text 'The Pivot: Building for Everyone' in bold "
            "Montserrat-style sans-serif, clean dark background with subtle gradient, gold underline "
            "accent, futuristic minimal UI design, tech presentation slide aesthetic, "
            "16:9 widescreen, 8K resolution"
        ),
    },
    # --- Scene 3: Static vs Dynamic ---
    {
        "id": "IG.03",
        "name": "ig_03_static_vs_dynamic",
        "scene": "Scene 3: Static vs Dynamic (00:00:38)",
        "prompt": (
            "Split-screen infographic comparison: left side labeled 'Static Rules' with icon of "
            "a locked padlock and rigid grid pattern in grey tones; right side labeled 'Dynamic AI' "
            "with flowing liquid mercury icon and adaptive mesh in blue-gold tones, "
            "clean dividing line, modern data visualization style, dark background, 16:9, 8K"
        ),
    },
    {
        "id": "IG.04",
        "name": "ig_04_breaking_chains",
        "scene": "Scene 3: Breaking Chains (00:00:45)",
        "prompt": (
            "Dramatic infographic visual: iron chains breaking apart into golden particles, "
            "text overlay 'Breaking the Iron Chains' in bold white, dark moody background, "
            "sparks flying, liberation metaphor, cinematic motion graphic style, 16:9, 8K"
        ),
    },
    # --- Scene 4: The Clone Lab ---
    {
        "id": "IG.05",
        "name": "ig_05_clone_steps_checklist",
        "scene": "Scene 4: Clone Lab Steps",
        "prompt": (
            "Clean process infographic checklist on dark background: three steps with checkmarks, "
            "'Step 1: Clone Repository ✓', 'Step 2: Setup Environment ✓', 'Step 3: Run Agent ✓', "
            "green checkmark icons, modern sans-serif font, sidebar layout, "
            "GitHub blue #0366d6 accent color, minimal UI design, 16:9, 8K"
        ),
    },
    {
        "id": "IG.06",
        "name": "ig_06_tool_comparison_table",
        "scene": "Scene 4: Tool Comparison (00:02:30)",
        "prompt": (
            "Clean data comparison table infographic: 'VS Code vs Cursor AI' header, "
            "rows showing features like Free Tier, Local Agent, Git Support with checkmark and "
            "dash icons, modern flat design, dark background, blue and white color scheme, "
            "professional tech presentation table style, 16:9, 8K"
        ),
    },
    # --- Scene 5: The Evolution ---
    {
        "id": "IG.07",
        "name": "ig_07_cloning_flowchart",
        "scene": "Scene 5: Cloning Diagram (00:04:00)",
        "prompt": (
            "Flowchart infographic: 'User → Repository → Clone' with flowing arrow connections, "
            "cloud icon for source, laptop icon for local machine, file copy animation trail, "
            "abstract technical style, glowing blue connections on dark background, "
            "minimal node-based diagram, 16:9, 8K"
        ),
    },
    {
        "id": "IG.08",
        "name": "ig_08_3d_printer_progress",
        "scene": "Scene 5: Progress Bar (00:04:30)",
        "prompt": (
            "Futuristic progress bar infographic: circular progress indicator showing 78% complete, "
            "3D printer silhouette in background, percentage counter in large bold font, "
            "glowing cyan progress arc, dark background, clean modern data visualization, "
            "tech HUD aesthetic, 16:9, 8K"
        ),
    },
    # --- Scene 6: The Nursery ---
    {
        "id": "IG.09",
        "name": "ig_09_consistency_quote",
        "scene": "Scene 6: Consistency Quote (00:06:00)",
        "prompt": (
            "Inspirational quote infographic: 'Consistency is Your Magic Shield' in large bold "
            "white typography, decorative shield icon with golden glow, warm soft gradient "
            "background in purple-to-dark tones, elegant spacing, motivational poster style, "
            "cinematic text layout, 16:9, 8K"
        ),
    },
    {
        "id": "IG.10",
        "name": "ig_10_family_friendly_badge",
        "scene": "Scene 6: Family Badge (00:06:20)",
        "prompt": (
            "Badge infographic overlay: shield-shaped badge icon with text 'Family-Tested Solution', "
            "warm golden and green colors, checkmark inside shield, friendly approachable design, "
            "subtle glow effect, dark background with warm vignette, 16:9, 8K"
        ),
    },
    # --- Scene 7: The Crystal Ball ---
    {
        "id": "IG.11",
        "name": "ig_11_tech_logos_layout",
        "scene": "Scene 7: Tech Platforms (00:06:36)",
        "prompt": (
            "Tech platform comparison infographic: four quadrant layout showing abstract icons "
            "representing major AI platforms, each with a label — 'Search', 'Assistant', "
            "'Reasoning', 'Multi-modal', clean modern card-based design, dark gradient background, "
            "subtle glow around each card, professional data visualization, 16:9, 8K"
        ),
    },
    # --- Scene 8: The Engine Room ---
    {
        "id": "IG.12",
        "name": "ig_12_speed_1000x",
        "scene": "Scene 8: Speed Stat (00:08:35)",
        "prompt": (
            "Bold stat infographic: massive text '1000x' in white with motion blur streaks, "
            "subtitle 'Faster Deployment' below, speed lines radiating from center, "
            "energetic dark background with blue and orange energy trails, "
            "dynamic typography, tech HUD style, 16:9, 8K"
        ),
    },
    {
        "id": "IG.13",
        "name": "ig_13_speed_comparison_bars",
        "scene": "Scene 8: Speed Chart (00:08:50)",
        "prompt": (
            "Horizontal bar chart infographic: 'Traditional' bar in grey at 10%, "
            "'AI-Powered' bar in glowing blue at 95%, clean comparison visualization, "
            "labels on left, percentages on right, dark background, modern flat design, "
            "data dashboard aesthetic, 16:9, 8K"
        ),
    },
    # --- Scene 9: The Digital Feast / LLMs ---
    {
        "id": "IG.14",
        "name": "ig_14_llm_claude_card",
        "scene": "Scene 9: Claude Card (00:09:30)",
        "prompt": (
            "Feature card infographic: 'The Reasoning Layer' headline in bold white, "
            "abstract brain-circuit icon, bullet points 'Sonnet 3.5, 4.5, 4.6', "
            "'Best for: Complex Problems', card design with subtle orange-brown gradient border, "
            "dark background, modern tech card layout, 16:9, 8K"
        ),
    },
    {
        "id": "IG.15",
        "name": "ig_15_llm_chatgpt_card",
        "scene": "Scene 9: ChatGPT Card",
        "prompt": (
            "Feature card infographic: 'The Versatile Leader' headline in bold white, "
            "abstract chat bubble icon with search lens, bullet points 'Search, Browsing, Plugins', "
            "'Best for: General Purpose', card with green gradient border, "
            "dark background, modern tech card layout, 16:9, 8K"
        ),
    },
    {
        "id": "IG.16",
        "name": "ig_16_llm_deepseek_card",
        "scene": "Scene 9: DeepSeek Card",
        "prompt": (
            "Feature card infographic: 'The Coding Disruptor' headline in bold white, "
            "abstract code terminal icon with lightning bolt, bullet points 'Free, Powerful', "
            "'Best for: Development', card with electric blue gradient border, "
            "dark background, modern tech card layout, 16:9, 8K"
        ),
    },
    {
        "id": "IG.17",
        "name": "ig_17_llm_gemini_card",
        "scene": "Scene 9: Gemini Card",
        "prompt": (
            "Feature card infographic: 'The Versatile Platform' headline in bold white, "
            "abstract multi-faceted gem icon, bullet points 'Images, Code, Nano', "
            "'Best for: Multi-modal Tasks', card with purple-blue gradient border, "
            "dark background, modern tech card layout, 16:9, 8K"
        ),
    },
    {
        "id": "IG.18",
        "name": "ig_18_100_tablets_stat",
        "scene": "Scene 9: 100 Tablets (00:09:05)",
        "prompt": (
            "Glowing stat infographic: large text '100+' in digital glitch aesthetic, "
            "flickering neon effect, subtitle 'AI Models Available' below, "
            "dark background with digital noise texture, cyberpunk data visualization, "
            "16:9, 8K"
        ),
    },
    # --- Scene 10: The Power Station ---
    {
        "id": "IG.19",
        "name": "ig_19_n8n_workflow_diagram",
        "scene": "Scene 10: n8n Workflow (00:12:15)",
        "prompt": (
            "Node-based workflow diagram infographic: connected nodes showing "
            "'Telegram/Email → n8n → MAC Filter → Internet Control', "
            "each node is a rounded rectangle with icon, flowing data arrows between nodes, "
            "n8n orange brand color accents, dark background, clean technical diagram, 16:9, 8K"
        ),
    },
    {
        "id": "IG.20",
        "name": "ig_20_internet_kill_switch",
        "scene": "Scene 10: Kill Switch (00:12:00)",
        "prompt": (
            "Bold title infographic: 'The Internet Kill Switch' in stark white text with red "
            "glitch distortion effect, big red power button icon below, tech-noir aesthetic, "
            "dark background with red accent lighting, dramatic and cyberpunk, 16:9, 8K"
        ),
    },
    # --- Scene 11: The Tool Shed ---
    {
        "id": "IG.21",
        "name": "ig_21_37_commits_counter",
        "scene": "Scene 11: Commits Stat (00:14:00)",
        "prompt": (
            "GitHub-style stat box infographic: large number '37+' in bold white, "
            "subtitle 'Commits — Continuous Evolution' below, green contribution graph pattern "
            "in background, GitHub dark theme #24292e, modern developer dashboard aesthetic, "
            "16:9, 8K"
        ),
    },
    {
        "id": "IG.22",
        "name": "ig_22_cicd_pipeline",
        "scene": "Scene 11: CI/CD Pipeline (00:15:30)",
        "prompt": (
            "Linear pipeline infographic: five connected stages 'Code → Test → Build → Deploy → Live', "
            "each stage is a node with green checkmark, arrow connections between them, "
            "horizontal flow left to right, clean flat design, green success color, "
            "dark background, DevOps diagram style, 16:9, 8K"
        ),
    },
    {
        "id": "IG.23",
        "name": "ig_23_success_metrics_dashboard",
        "scene": "Scene 11: Metrics Dashboard (00:16:45)",
        "prompt": (
            "Modern dashboard infographic grid: four metric cards in a 2x2 grid, "
            "'Compliance: 100%' in green, 'Accuracy: 98.5%' in blue, 'Uptime: 99.9%' in cyan, "
            "'Self-growth: ↑37 iterations' in gold, each with a circular progress ring, "
            "dark background, clean data visualization design, 16:9, 8K"
        ),
    },
    # --- Scene 12: The Balcony ---
    {
        "id": "IG.24",
        "name": "ig_24_call_to_action",
        "scene": "Scene 12: CTA Steps (00:17:50)",
        "prompt": (
            "Step-by-step call to action infographic: four numbered steps vertically — "
            "'1. Take Assessment', '2. Watch Simulation', '3. Clone Repository', '4. Build Your Future', "
            "each with a small icon, connecting dotted line between steps, "
            "gold accent numbers, white text, dark gradient background, clean modern design, 16:9, 8K"
        ),
    },
    {
        "id": "IG.25",
        "name": "ig_25_zero_capital_quote",
        "scene": "Scene 5: Zero Capital Quote",
        "prompt": (
            "Inspirational quote infographic: 'Zero Capital, Infinite Potential' in large bold "
            "white serif typography on dark background, subtle gold particle burst behind text, "
            "minimal elegant design, motivational poster aesthetic, 16:9, 8K"
        ),
    },
]


def generate_asset(asset_config: Dict, idx: int, total: int, cost_so_far: float, timestamp: str) -> Dict:
    """Generate a single infographic asset using fal.ai"""
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
    print("📊 FAL.AI INFOGRAPHICS GENERATOR")
    print(f"   Model: {MODEL} (~${COST_PER_IMAGE}/image)")
    print(f"   Infographics: {total}")
    print(f"   Estimated cost: ${estimated_cost:.2f} (budget: ${BUDGET_LIMIT:.2f})")
    print(f"   Output: {OUTPUT_DIR}")
    print("=" * 60)

    for i, item in enumerate(GENERATION_QUEUE, 1):
        print(f"  {i:>3}. [{item['id']}] {item['scene']}")

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
        print(f"\n✅ Generated infographics:")
        for r in successful:
            print(f"   • {r['name']} → {r['filename']}")

    if failed:
        print(f"\n❌ Failed:")
        for r in failed:
            print(f"   • {r['name']} — {r.get('error', 'unknown')}")

    # Save summary JSON
    summary_path = OUTPUT_DIR / f"infographics_summary_{timestamp}.json"
    with open(summary_path, "w") as f:
        json.dump(
            {
                "generator": "BatchAssetGeneratorInfographics",
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

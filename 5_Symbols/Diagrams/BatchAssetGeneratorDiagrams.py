#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Diagrams
Project: The Delivery Pilot Transformation
Generates technical diagrams, flowcharts, and architecture visualizations.

Derived from: 3_Simulation/2026-02-15/input/source_edl.md
Cost: ~$0.01/image × 12 diagrams = ~$0.12 (budget: $0.50)
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

# ─── Diagram Queue — one per scene from the EDL ─────────────────────────────

GENERATION_QUEUE = [
    # Scene 1: The Pivot — Golden Mic
    {
        "id": "DG.01",
        "name": "dg_01_golden_mic_hierarchy",
        "scene": "Scene 1: The Pivot (00:00:00)",
        "prompt": (
            "Clean technical hierarchy diagram on dark background: pyramid chart with three tiers, "
            "top tier labeled 'Enterprise Engineers' with golden crown icon, middle tier 'Mid-Level "
            "Automation' in grey, bottom tier 'Delivery Pilots' highlighted in glowing blue with "
            "upward arrows. Title 'The AI Transformation Hierarchy' in bold white sans-serif. "
            "Connecting lines between tiers, modern flat design, GitHub dark #24292e background, "
            "accent gold #FFD700, 16:9, 8K"
        ),
    },
    # Scene 2: The Delivery Pilot — 240 Workflows
    {
        "id": "DG.02",
        "name": "dg_02_240_workflow_architecture",
        "scene": "Scene 2: Delivery Pilot (00:00:10)",
        "prompt": (
            "Technical architecture diagram: central hub labeled 'Delivery Pilot Engine' connected "
            "to 12 satellite nodes in a radial layout, each labeled with workflow categories like "
            "'Finance', 'Family', 'DevOps', 'Content', 'Health', 'Learning'. Glowing connection "
            "lines in cyan, counter showing '240+' in top-right corner, dark background, "
            "professional network topology style, clean node-based design, 16:9, 8K"
        ),
    },
    # Scene 3: Static vs Dynamic
    {
        "id": "DG.03",
        "name": "dg_03_static_vs_dynamic_flow",
        "scene": "Scene 3: Static vs Dynamic (00:00:35)",
        "prompt": (
            "Side-by-side flowchart comparison diagram: left flowchart labeled 'Static Rules' "
            "with rigid rectangular boxes in grey connected by straight arrows, ending in a "
            "red X dead-end. Right flowchart labeled 'Dynamic AI' with organic rounded nodes "
            "in cyan and blue connected by curved flowing arrows, ending in a green checkmark "
            "with branching paths. Title 'Rules Evolution' at top. Dark background, "
            "clean technical diagram style, 16:9, 8K"
        ),
    },
    # Scene 4: The Clone Lab
    {
        "id": "DG.04",
        "name": "dg_04_git_clone_sequence",
        "scene": "Scene 4: Clone Lab (00:00:48)",
        "prompt": (
            "Technical sequence diagram: vertical swim-lane diagram showing three columns "
            "'GitHub Cloud', 'Terminal', 'Local Machine'. Arrows flowing top to bottom: "
            "'git clone' command from Terminal to GitHub, 'Download repo' response, "
            "'Setup environment' on Local Machine, 'Run agent' final step with green check. "
            "Clean UML sequence diagram style, dark background, blue accent lines, "
            "monospace labels, developer documentation aesthetic, 16:9, 8K"
        ),
    },
    # Scene 5: The Evolution — Free Tier
    {
        "id": "DG.05",
        "name": "dg_05_tool_evolution_timeline",
        "scene": "Scene 5: Evolution (00:03:52)",
        "prompt": (
            "Horizontal timeline evolution diagram: three stages connected by forward arrows. "
            "Stage 1: 'VS Code + GitHub' icon with label 'Free Tier' in green. "
            "Stage 2: 'GitHub Copilot' icon with label 'Pair Pilot' in blue. "
            "Stage 3: 'Cursor AI' icon with label 'Agentic' in purple. "
            "Title 'Developer Tool Evolution' at top. Progress bar underneath showing "
            "increasing capability. Dark background, clean infographic timeline, 16:9, 8K"
        ),
    },
    # Scene 6: The Nursery — Internet Kill Switch
    {
        "id": "DG.06",
        "name": "dg_06_internet_kill_switch_flow",
        "scene": "Scene 6: Nursery (00:05:50)",
        "prompt": (
            "Network architecture diagram: home WiFi router at center connected to multiple "
            "device icons (laptop, tablet, phone). GitHub Actions node connected via API to "
            "the router with a big red toggle switch in the middle labeled 'Kill Switch'. "
            "Green lines for active connections, red dashed lines for blocked connections. "
            "Label 'Per-Device MAC Filtering' at bottom. Dark background, clean network "
            "topology diagram style, 16:9, 8K"
        ),
    },
    # Scene 7: The Crystal Ball — Tech Platforms
    {
        "id": "DG.07",
        "name": "dg_07_tech_platform_comparison",
        "scene": "Scene 7: Crystal Ball (00:06:36)",
        "prompt": (
            "Comparison matrix diagram: 2x2 grid with four quadrant cards. Top-left: 'Google' "
            "with search icon in blue. Top-right: 'Microsoft' with cloud icon in cyan. "
            "Bottom-left: 'Amazon Alexa' with speaker icon in teal. Bottom-right: 'Open Source' "
            "with community icon in green. Overlapping area at center labeled 'AI Convergence'. "
            "Clean Venn-style overlap diagram, dark background, professional tech style, 16:9, 8K"
        ),
    },
    # Scene 8: The Engine Room — Speed
    {
        "id": "DG.08",
        "name": "dg_08_speed_benchmark_chart",
        "scene": "Scene 8: Engine Room (00:08:26)",
        "prompt": (
            "Performance benchmark bar chart diagram: horizontal bars comparing deployment speeds. "
            "'Manual Deploy' bar in grey at 5%, 'CI/CD Pipeline' bar in blue at 60%, "
            "'AI-Powered Deploy' bar in glowing cyan at 100% with '1000x' label and speed lines. "
            "Y-axis labels on left, percentage scale on right. Title 'Deployment Speed Comparison'. "
            "Clean data visualization chart, dark background, modern dashboard style, 16:9, 8K"
        ),
    },
    # Scene 9: The Digital Feast — LLM Comparison
    {
        "id": "DG.09",
        "name": "dg_09_llm_comparison_matrix",
        "scene": "Scene 9: Digital Feast (00:09:01)",
        "prompt": (
            "Feature comparison matrix diagram: table with 4 rows and 5 columns. "
            "Column headers: 'Model', 'Strength', 'Cost', 'Best For', 'Tier'. "
            "Row 1: 'Claude' — 'Reasoning' — '$$' — 'Complex Problems' — orange dot. "
            "Row 2: 'ChatGPT' — 'Versatile' — '$$' — 'General Purpose' — green dot. "
            "Row 3: 'DeepSeek' — 'Coding' — 'Free' — 'Development' — blue dot. "
            "Row 4: 'Gemini' — 'Multi-modal' — 'Free' — 'Images+Code' — purple dot. "
            "Clean spreadsheet-style table, dark background, tech dashboard design, 16:9, 8K"
        ),
    },
    # Scene 10: The Power Station — n8n
    {
        "id": "DG.10",
        "name": "dg_10_n8n_automation_flow",
        "scene": "Scene 10: Power Station (00:11:45)",
        "prompt": (
            "Workflow automation flowchart: node-based diagram showing connected blocks — "
            "'Telegram Trigger' → 'n8n Logic Node' → 'MAC Address Filter' → 'Router API Call' "
            "→ 'GitHub Pages Dashboard'. Each node is a rounded rectangle with a small icon. "
            "Data flow arrows between nodes with labels. Orange n8n brand accents. "
            "Title 'Home Automation Pipeline'. Dark background, clean technical flow, 16:9, 8K"
        ),
    },
    # Scene 11: The Tool Shed — CI/CD
    {
        "id": "DG.11",
        "name": "dg_11_cicd_pipeline_diagram",
        "scene": "Scene 11: Tool Shed (00:13:15)",
        "prompt": (
            "CI/CD pipeline architecture diagram: horizontal pipeline with five connected stages "
            "'Commit' → 'Test' → 'Build' → 'Deploy' → 'Live Site'. GitHub Actions logo at the "
            "top orchestrating all stages. Each stage has a status indicator: green checkmarks. "
            "Counter '37+ commits' badge in corner. Audit trail log scrolling on the side. "
            "Clean DevOps pipeline diagram, dark background, green success theme, 16:9, 8K"
        ),
    },
    # Scene 12: The Balcony — Call to Action
    {
        "id": "DG.12",
        "name": "dg_12_journey_roadmap",
        "scene": "Scene 12: Balcony (00:17:24)",
        "prompt": (
            "Journey roadmap diagram: winding path from bottom-left to top-right with four "
            "milestone markers. Milestone 1: 'Take Assessment' with clipboard icon. "
            "Milestone 2: 'Watch Simulation' with play button icon. Milestone 3: 'Clone Repo' "
            "with terminal icon. Milestone 4: 'Build Your Future' with rocket icon at the top. "
            "Dotted path connecting milestones, golden accent markers, dark gradient background, "
            "inspirational roadmap infographic style, 16:9, 8K"
        ),
    },
]


def generate_asset(asset_config: Dict, idx: int, total: int, cost_so_far: float, timestamp: str) -> Dict:
    """Generate a single diagram asset using fal.ai"""
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
    print("📐 FAL.AI DIAGRAM GENERATOR")
    print(f"   Model: {MODEL} (~${COST_PER_IMAGE}/image)")
    print(f"   Diagrams: {total}")
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
    print("📐 GENERATION SUMMARY")
    print("=" * 60)
    print(f"✅ Successful: {len(successful)}/{total}")
    print(f"❌ Failed:     {len(failed)}/{total}")
    print(f"💰 Total cost: ${cost_so_far:.2f} / ${BUDGET_LIMIT:.2f} budget")

    if successful:
        print(f"\n✅ Generated diagrams:")
        for r in successful:
            print(f"   • {r['name']} → {r['filename']}")

    if failed:
        print(f"\n❌ Failed:")
        for r in failed:
            print(f"   • {r['name']} — {r.get('error', 'unknown')}")

    # Save summary JSON
    summary_path = OUTPUT_DIR / f"diagrams_summary_{timestamp}.json"
    with open(summary_path, "w") as f:
        json.dump(
            {
                "generator": "BatchAssetGeneratorDiagrams",
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

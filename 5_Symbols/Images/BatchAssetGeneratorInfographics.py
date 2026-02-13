#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Infographics
Project: The Agentic Era
Generates data visualization and infographic overlays for each scene.

Derived from: 3_Simulation/2026-02-15/input/source_graphics.md
Cost: ~$0.01/image × ~25 infographics = ~$0.25 (budget: $0.50)
"""

import sys
from pathlib import Path
from typing import Dict, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from base.base_asset_generator import BaseAssetGenerator
from paths_config import get_weekly_paths, get_latest_weekly_id

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

# Model configuration
DEFAULT_MODEL = "fal-ai/flux/schnell"

# ─── Infographic Queue — derived from source_graphics.md ────────────────────

GENERATION_QUEUE = [
    # --- Scene 1-2: Opening & The Pivot ---
    {
        "id": "IG.01",
        "name": "ig_01_240_workflows_stat",
        "scene": "Scene 1-2: Opening (00:00:15)",
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
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
        "seed_key": "SEED_002",
        "model": DEFAULT_MODEL,
        "prompt": (
            "Inspirational quote infographic: 'Zero Capital, Infinite Potential' in large bold "
            "white serif typography on dark background, subtle gold particle burst behind text, "
            "minimal elegant design, motivational poster aesthetic, 16:9, 8K"
        ),
    },
]


class InfographicsGenerator(BaseAssetGenerator):
    """Generator for infographic assets using base class architecture."""

    def __init__(self, output_dir: Path, seeds: Dict[str, int], brand_colors: Dict[str, str]):
        super().__init__(
            output_dir=output_dir,
            seeds=seeds,
            brand_colors=brand_colors,
            asset_type='infographic',
            output_format='png'
        )

    def get_generation_queue(self) -> List[Dict]:
        """Return the infographics generation queue."""
        return GENERATION_QUEUE


def main():
    """Main execution using base class architecture."""
    # Get latest weekly paths or use default
    weekly_id = get_latest_weekly_id() or "2026-02-15"
    paths = get_weekly_paths(weekly_id)
    output_dir = paths['output']
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("📊 FAL.AI INFOGRAPHICS GENERATOR (Base Class Architecture)")
    print(f"   Weekly ID: {weekly_id}")
    print(f"   Output: {output_dir}")
    print("=" * 60)

    # Initialize generator
    generator = InfographicsGenerator(
        output_dir=output_dir,
        seeds=SEEDS,
        brand_colors=BRAND_COLORS
    )

    # Generate all assets
    results = generator.generate_batch()

    # Display results
    generator.display_summary(results)


if __name__ == "__main__":
    main()

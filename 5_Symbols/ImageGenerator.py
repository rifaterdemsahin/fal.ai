#!/usr/bin/env python3
"""
Image Asset Generator
Generates image assets using fal.ai with base class architecture
"""

from pathlib import Path
from typing import Dict, List

from base.base_asset_generator import BaseAssetGenerator
from base.generator_config import SEEDS, BRAND_COLORS


class ImageAssetGenerator(BaseAssetGenerator):
    """Generator for image assets"""
    
    def __init__(self):
        super().__init__(
            output_dir=Path("./generated_assets"),
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="image"
        )
    
    def get_generation_queue(self) -> List[Dict]:
        """Return the list of images to generate"""
        return [
            # HIGH PRIORITY ASSETS
            {
                "id": "1.1",
                "name": "ferrari_cart_morph",
                "priority": "HIGH",
                "scene": "Scene 1: Hook",
                "seed_key": "SEED_003",
                "prompt": (
                    "Sleek red Ferrari sports car icon smoothly morphing into simple shopping cart icon, "
                    "clean vector style, white/transparent background, particle effects during transformation, "
                    "professional tech presentation aesthetic, minimalist flat design, modern motion graphics style, "
                    "16:9 aspect ratio, high quality, sharp details"
                ),
                "model": "fal-ai/flux/schnell",  # Fast generation
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 4,
            },
            {
                "id": "4.2",
                "name": "sunday_5pm_timeline",
                "priority": "HIGH",
                "scene": "Scene 4: Skills Gap",
                "seed_key": "SEED_002",
                "prompt": (
                    "Motion graphics timeline visualization showing Sunday evening 5:00 PM prominently displayed, "
                    "large clock icon showing 17:00, row of 5-6 shop icons with red 'X' or 'CLOSED' indicators overlaid, "
                    "Cambridge location pin subtle in background, clean infographic design, "
                    "dark background (#1a1a2e) with blue/purple accent colors (#00d4ff, #7b2cbf), "
                    "modern minimalist style, professional data visualization, 16:9 format"
                ),
                "model": "fal-ai/flux/dev",  # Higher quality for infographics
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
            {
                "id": "4.3",
                "name": "agent_workflow_diagram",
                "priority": "HIGH",
                "scene": "Scene 4: Skills Gap",
                "seed_key": "SEED_002",
                "prompt": (
                    "Professional workflow diagram showing AI agent process flow in three connected stages from left to right: "
                    "Stage 1 'DATA COLLECTION' with database/cloud storage icons and arrows pointing inward, "
                    "Stage 2 'UNDERSTANDING' with brain/AI processor icon and location symbols (home icon transforming to shopping cart), "
                    "Stage 3 'NOTIFICATION' with mobile phone and notification bell icon, "
                    "connected by flowing arrows with subtle gradient, clean modern infographic style, "
                    "dark background (#1a1a2e) with gradient accent colors (blue #00d4ff to purple #7b2cbf), "
                    "each stage clearly labeled in sans-serif font, professional technical diagram, 16:9 aspect ratio"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
            {
                "id": "4.4",
                "name": "chatbot_vs_realtime",
                "priority": "HIGH",
                "scene": "Scene 4: Skills Gap",
                "seed_key": "SEED_002",
                "prompt": (
                    "Split-screen comparison graphic in 16:9 format, "
                    "LEFT SIDE: traditional chatbot interface showing static conversation bubbles, waiting cursor, inactive state, muted gray colors (#6b6b6b); "
                    "RIGHT SIDE: active real-time AI system showing live notification badges, proactive alert icons, dynamic response indicators, "
                    "vibrant blue/purple colors (#00d4ff, #7b2cbf), visual contrast between passive vs active AI systems, "
                    "modern UI design elements, professional software comparison layout, clean typography, dark background"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
            {
                "id": "6.1",
                "name": "20_dollar_pricing",
                "priority": "HIGH",
                "scene": "Scene 6: PARA Method",
                "seed_key": "SEED_002",
                "prompt": (
                    "Bold pricing graphic with '$20' in very large prominent numbers (72pt+), "
                    "'/month' text below in medium size (36pt), surrounded by circular arrangement of 5 tool icons: "
                    "n8n logo, Telegram icon, Obsidian icon, Gemini sparkle, Claude icon, "
                    "clean modern design with subtle gradient background (dark blue to purple #1a1a2e to #7b2cbf), "
                    "pricing emphasis layout with glowing effect around price, professional infographic style, "
                    "affordability message clear, minimalist design, white/cyan text (#ffffff, #00d4ff), 16:9 aspect ratio"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
            {
                "id": "9.2",
                "name": "silos_vs_agents",
                "priority": "HIGH",
                "scene": "Scene 9: AI Transformation",
                "seed_key": "SEED_002",
                "prompt": (
                    "Split-screen comparison in 16:9 format, "
                    "LEFT SIDE 'SILO APPROACH': 4 isolated figures in separate gray boxes, each with only small ChatGPT icon, "
                    "disconnected units with no connections, muted gray/blue colors (#6b6b6b, #404040), "
                    "text overlay 'ChatGPT only, No automation, Manual work'; "
                    "RIGHT SIDE 'AGENT APPROACH': interconnected network of nodes/circles representing AI agents, "
                    "colorful flowing lines connecting multiple systems, data particle effects, "
                    "vibrant blue/purple/cyan colors (#00d4ff, #7b2cbf, #00bfa5), "
                    "text overlay 'Deployed agents, Data collection, Automated workflows', "
                    "modern infographic design, clear visual contrast, professional comparison graphic"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
            {
                "id": "9.3",
                "name": "bottom_up_revolution",
                "priority": "HIGH",
                "scene": "Scene 9: AI Transformation",
                "seed_key": "SEED_002",
                "prompt": (
                    "Bold motivational graphic showing large upward arrow labeled 'BOTTOM-UP' "
                    "in vibrant gold/orange gradient (#ff6b35, #f7931e) moving from bottom to top, "
                    "crossed-out downward arrow labeled 'TOP-DOWN' faded in background, "
                    "individual empowerment icon (person silhouette with gear/tools) at bottom of upward arrow, "
                    "Microsoft Copilot button icon shown dimmed/crossed out, revolutionary theme with energetic colors, "
                    "grassroots movement aesthetic, strong typographic emphasis with sans-serif bold font, "
                    "motivational infographic style, dark background (#1a1a2e), 16:9 aspect ratio"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
            {
                "id": "11.1",
                "name": "ai_job_message",
                "priority": "HIGH",
                "scene": "Scene 11: Closing",
                "seed_key": "SEED_003",
                "prompt": (
                    "Bold typographic design with powerful message, main text 'AI ISN'T COMING FOR YOUR JOB' "
                    "in very large prominent letters (96pt sans-serif, all caps), positioned in upper two-thirds, "
                    "secondary text below 'YOU MUST TRANSFORM TO KEEP IT' in medium size (48pt), "
                    "dramatic color scheme with dark background (#0a0a0a) and bright white/gold text (#ffffff, #f7931e), "
                    "empowering yet serious tone, professional motivational graphic design, "
                    "clean modern typography, strong visual hierarchy, 16:9 aspect ratio"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
            
            # MEDIUM PRIORITY ASSETS
            {
                "id": "4.1",
                "name": "uk_streets_sunday",
                "priority": "MEDIUM",
                "scene": "Scene 4: Skills Gap",
                "seed_key": "SEED_001",
                "prompt": (
                    "Cinematic shot of empty UK high street on Sunday evening, closed shop fronts with metal shutters down, "
                    "dim streetlights beginning to illuminate, deserted pedestrian area, typical British town center architecture, "
                    "moody atmospheric lighting, golden hour or early dusk, realistic urban photography style, "
                    "slight film grain, 16:9 cinematic aspect ratio, melancholic mood"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
                "note": "Alternative: Use stock footage if generation insufficient",
            },
            {
                "id": "5.1",
                "name": "bounded_contexts_diagram",
                "priority": "MEDIUM",
                "scene": "Scene 5: Bounded Contexts",
                "seed_key": "SEED_002",
                "prompt": (
                    "Technical architecture diagram showing three parallel workflow streams, "
                    "each enclosed in a distinct containment box with rounded corners, "
                    "left workflow labeled 'BOUNDED CONTEXT: FAMILY' with house icon and blue border (#00d4ff), "
                    "middle workflow 'BOUNDED CONTEXT: FINANCE' with dollar icon and purple border (#7b2cbf), "
                    "right workflow 'BOUNDED CONTEXT: PROJECTS' with folder icon and teal border (#00bfa5), "
                    "each box contains simplified workflow nodes ending in Telegram icon, "
                    "clean separation between contexts, professional software architecture visualization, "
                    "dark background, modern tech diagram style, 16:9 format"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
            {
                "id": "7.1",
                "name": "deliverpilot_methodology",
                "priority": "MEDIUM",
                "scene": "Scene 7: GitHub",
                "seed_key": "SEED_002",
                "prompt": (
                    "Horizontal flowchart showing 4 connected stages from left to right: "
                    "'UNKNOWN PROBLEM' box with question mark icon → 'SYMBOL/MODEL' box with diagram icon → "
                    "'n8n SIMULATION' box with workflow icon → 'TESTING/VALIDATION' box with checkmark icon, "
                    "connected by right-pointing arrows, each box has distinct color (red, yellow, blue, green gradients), "
                    "clean process diagram style, dark background (#1a1a2e), modern infographic design, "
                    "professional methodology visualization, sans-serif labels, 16:9 format"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
            {
                "id": "8.1",
                "name": "state_management_flow",
                "priority": "MEDIUM",
                "scene": "Scene 8: State Management",
                "seed_key": "SEED_002",
                "prompt": (
                    "Technical diagram showing state management flow in 5 connected boxes: "
                    "'PREVIOUS STATE' (database cylinder icon) → 'CURRENT INPUT' (arrow icon) → "
                    "'STATE COMPARISON' (equals/not-equals icon) → 'DECISION' (fork/branch icon) → "
                    "'UPDATE STATE' (save icon), connected by arrows with data flow indicators, "
                    "positioned to overlay on workflow nodes, clean technical documentation style, "
                    "cyan/blue color scheme (#00d4ff, #0096c7), dark transparent background, "
                    "professional system architecture diagram, 16:9 format"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
            {
                "id": "10.1",
                "name": "phone_before_after",
                "priority": "MEDIUM",
                "scene": "Scene 10: Call to Action",
                "seed_key": "SEED_002",
                "prompt": (
                    "Side-by-side phone screens in 16:9 layout, "
                    "LEFT 'BEFORE': iPhone home screen cluttered with social media apps - YouTube (red icon), "
                    "Instagram (gradient icon), Reddit (orange icon), TikTok, multiple game apps, notification badges, chaotic layout; "
                    "RIGHT 'AFTER': same iPhone with minimalist clean home screen showing only Google Gemini app icon, "
                    "Claude app icon, Calendar, Notes app, mostly empty screen with clean modern wallpaper, "
                    "visual contrast between distraction vs focus, realistic iOS interface design, modern smartphone mockup"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
        ]


def main():
    """Main execution"""
    generator = ImageAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()

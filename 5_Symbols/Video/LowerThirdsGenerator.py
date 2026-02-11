#!/usr/bin/env python3
"""
Lower Thirds Asset Generator
Generates lower third graphics using fal.ai with base class architecture
"""

from pathlib import Path
from typing import Dict, List

from base.base_asset_generator import BaseAssetGenerator
from base.generator_config import SEEDS, BRAND_COLORS, OUTPUT_FORMATS


class LowerThirdsAssetGenerator(BaseAssetGenerator):
    """Generator for lower third assets"""
    
    def __init__(self):
        super().__init__(
            output_dir=Path("./generated_assets/lower_thirds"),
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="lower_third",
            output_format=OUTPUT_FORMATS.get("lower_third", "png")  # Keep PNG for lower thirds (transparency)
        )
    
    def get_generation_queue(self) -> List[Dict]:
        """Return the list of lower thirds to generate"""
        # Common Prompt Base
        PROMPT_BASE = (
            "Professional lower third broadcast graphic for video overlay, "
            "floating on transparent background (alpha channel), "
            "modern tech aesthetic, clean sans-serif typography, "
            "positioned in lower left area, high contrast for readability, "
            "dark glassmorphism background panel (#1a1a2e) with distinct accent borders, "
            "4k resolution, high quality render"
        )
        
        return [
            # HIGH PRIORITY - Core Concepts
            {
                "id": "LT_01",
                "name": "lt_agentic_era",
                "priority": "HIGH",
                "text": "The Agentic Era",
                "subtext": "Managing 240+ Workflows",
                "color_theme": "accent_blue",
                "seed_key": "SEED_004",
                "prompt": (
                    f"{PROMPT_BASE}, main text 'THE AGENTIC ERA' in bold white font, "
                    "subtext 'Managing 240+ Workflows' in smaller cyan font, "
                    "neon blue (#00d4ff) glowing accent line, futuristic interface style."
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 30,
            },
            {
                "id": "LT_02",
                "name": "lt_mcp",
                "priority": "HIGH",
                "text": "Model Context Protocol",
                "subtext": "Standardized AI Connections",
                "color_theme": "accent_purple",
                "seed_key": "SEED_004",
                "prompt": (
                    f"{PROMPT_BASE}, main text 'MODEL CONTEXT PROTOCOL' in bold white font, "
                    "subtext 'Standardized AI Connections' in smaller purple font, "
                    "neon purple (#7b2cbf) glowing accent line, technical diagram aesthetic."
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 30,
            },
            {
                "id": "LT_03",
                "name": "lt_skills_gap",
                "priority": "HIGH",
                "text": "The Skills Gap",
                "subtext": "Technology vs. Delivery",
                "color_theme": "highlight_orange",
                "seed_key": "SEED_004",
                "prompt": (
                    f"{PROMPT_BASE}, main text 'THE SKILLS GAP' in bold white font, "
                    "subtext 'Technology vs. Delivery' in smaller orange font, "
                    "bright orange (#ff6b35) accent details, alert/warning style UI elements."
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 30,
            },
            {
                "id": "LT_04",
                "name": "lt_bounded_contexts",
                "priority": "HIGH",
                "text": "Bounded Contexts",
                "subtext": "Separation of Concerns",
                "color_theme": "secondary_teal",
                "seed_key": "SEED_004",
                "prompt": (
                    f"{PROMPT_BASE}, main text 'BOUNDED CONTEXTS' in bold white font, "
                    "subtext 'Separation of Concerns' in smaller teal font, "
                    "clean teal (#00bfa5) border lines, architectural structure design."
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 30,
            },
            {
                "id": "LT_05",
                "name": "lt_para_method",
                "priority": "HIGH",
                "text": "PARA Method",
                "subtext": "Projects Areas Resources Archives",
                "color_theme": "accent_blue",
                "seed_key": "SEED_004",
                "prompt": (
                    f"{PROMPT_BASE}, main text 'PARA METHOD' in bold white font, "
                    "subtext 'Projects â€¢ Areas â€¢ Resources â€¢ Archives' in smaller grey/blue font, "
                    "minimalist organized structure, sharp blue accents."
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 30,
            },
            
            # MEDIUM PRIORITY - Technical Terms & Tools
            {
                "id": "LT_06",
                "name": "lt_state_management",
                "priority": "MEDIUM",
                "text": "State Management",
                "subtext": "Persistence in Automation",
                "color_theme": "accent_purple",
                "seed_key": "SEED_004",
                "prompt": (
                    f"{PROMPT_BASE}, main text 'STATE MANAGEMENT' in bold white font, "
                    "subtext 'Persistence in Automation' in smaller font, "
                    "data flow visualization elements, purple accent lighting."
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 30,
            },
            {
                "id": "LT_07",
                "name": "lt_deliverpilot",
                "priority": "MEDIUM",
                "text": "DeliverPilot",
                "subtext": "Methodology & Documentation",
                "color_theme": "secondary_teal",
                "seed_key": "SEED_004",
                "prompt": (
                    f"{PROMPT_BASE}, main text 'DELIVERPILOT' in bold white font, "
                    "subtext 'Methodology & Documentation' in smaller teal font, "
                    "navigator/compass interface hints, clean professional look."
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 30,
            },
            {
                "id": "LT_08",
                "name": "lt_bottom_up",
                "priority": "MEDIUM",
                "text": "Bottom-Up Revolution",
                "subtext": "Individual AI Adoption",
                "color_theme": "highlight_orange",
                "seed_key": "SEED_004",
                "prompt": (
                    f"{PROMPT_BASE}, main text 'BOTTOM-UP REVOLUTION' in bold white font, "
                    "subtext 'Individual AI Adoption' in smaller gold/orange font, "
                    "dynamic upward motion visuals in background opacity, empowering aesthetic."
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 30,
            },
            {
                "id": "LT_09",
                "name": "lt_n8n_workflows",
                "priority": "MEDIUM",
                "text": "240+ Autonomous Workflows",
                "subtext": "Running on n8n",
                "color_theme": "accent_blue",
                "seed_key": "SEED_004",
                "prompt": (
                    f"{PROMPT_BASE}, main text '240+ AUTONOMOUS WORKFLOWS' in bold white font, "
                    "subtext 'Running on n8n' in smaller font with n8n signature pink/orange hint, "
                    "network node background pattern overlays."
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 30,
            },
            {
                "id": "LT_10",
                "name": "lt_ai_transformation",
                "priority": "MEDIUM",
                "text": "AI Transformation",
                "subtext": "The Bigger Picture",
                "color_theme": "accent_purple",
                "seed_key": "SEED_004",
                "prompt": (
                    f"{PROMPT_BASE}, main text 'AI TRANSFORMATION' in bold white font, "
                    "subtext 'The Bigger Picture' in smaller purple font, "
                    "digital transformation particle effects in glass panel."
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 30,
            }
        ]


def main():
    """Main execution"""
    generator = LowerThirdsAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()


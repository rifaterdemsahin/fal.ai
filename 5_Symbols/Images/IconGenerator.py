#!/usr/bin/env python3
"""
Icon Asset Generator
Generates icon assets using fal.ai with base class architecture
"""

from pathlib import Path
from typing import Dict, List

from Base.base_asset_generator import BaseAssetGenerator
from Base.generator_config import SEEDS, BRAND_COLORS, OUTPUT_FORMATS


class IconAssetGenerator(BaseAssetGenerator):
    """Generator for icon assets"""
    
    def __init__(self):
        super().__init__(
            output_dir=Path("./generated_icons"),
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="icon",
            output_format=OUTPUT_FORMATS.get("icon", "png")  # Keep PNG for icons (transparency)
        )
    
    def get_generation_queue(self) -> List[Dict]:
        """Return the list of icons to generate"""
        return [
            # CORE SYMBOLS
            {
                "id": "icon_001",
                "name": "ferrari_icon",
                "priority": "HIGH",
                "scene": "Scene 1: Hook",
                "seed_key": "SEED_003",
                "prompt": (
                    "Sleek red Ferrari sports car icon, side view, minimalist flat design, "
                    "clean vector style, isolated on white background, "
                    "professional tech presentation aesthetic, modern motion graphics style"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1024, "height": 1024},
                "num_inference_steps": 28,
            },
            {
                "id": "icon_002",
                "name": "shopping_cart_icon",
                "priority": "HIGH",
                "scene": "Scene 1: Hook",
                "seed_key": "SEED_003",
                "prompt": (
                    "Simple shopping cart icon, minimalist flat design, "
                    "clean vector style, isolated on white background, "
                    "professional tech presentation aesthetic"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1024, "height": 1024},
                "num_inference_steps": 28,
            },
            
            # INFOGRAPHIC ICONS
            {
                "id": "icon_003",
                "name": "database_cylinder",
                "priority": "HIGH",
                "scene": "Scene 4: Skills Gap",
                "seed_key": "SEED_002",
                "prompt": (
                    "Database cylinder icon, modern UI style, cyan accent #00d4ff, "
                    "clean vector graphics, isolated on white background, "
                    "tech infographic element"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1024, "height": 1024},
                "num_inference_steps": 28,
            },
            {
                "id": "icon_004",
                "name": "brain_processor",
                "priority": "HIGH",
                "scene": "Scene 4: Skills Gap",
                "seed_key": "SEED_002",
                "prompt": (
                    "Brain circuit board icon, artificial intelligence symbol, "
                    "purple accent #7b2cbf, minimalist vector design, "
                    "isolated on white background"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1024, "height": 1024},
                "num_inference_steps": 28,
            },
            {
                "id": "icon_005",
                "name": "notification_bell",
                "priority": "MEDIUM",
                "scene": "Scene 4: Skills Gap",
                "seed_key": "SEED_002",
                "prompt": (
                    "Notification bell icon with active badge, modern iOS style, "
                    "orange accent #ff6b35, clean vector graphics, "
                    "isolated on white background"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1024, "height": 1024},
                "num_inference_steps": 28,
            },
            
            # BOUNDED CONTEXT ICONS
            {
                "id": "icon_006",
                "name": "family_house",
                "priority": "MEDIUM",
                "scene": "Scene 5: Bounded Contexts",
                "seed_key": "SEED_002",
                "prompt": (
                    "Minimalist house icon, home automation symbol, "
                    "blue accent #00d4ff, rounded corners, flat design, "
                    "vector icon, isolated on white background"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1024, "height": 1024},
                "num_inference_steps": 28,
            },
            {
                "id": "icon_007",
                "name": "finance_dollar",
                "priority": "MEDIUM",
                "scene": "Scene 5: Bounded Contexts",
                "seed_key": "SEED_002",
                "prompt": (
                    "Dollar sign icon inside circle, financial symbol, "
                    "purple accent #7b2cbf, modern clean lines, "
                    "vector icon, isolated on white background"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1024, "height": 1024},
                "num_inference_steps": 28,
            },
            {
                "id": "icon_008",
                "name": "project_folder",
                "priority": "MEDIUM",
                "scene": "Scene 5: Bounded Contexts",
                "seed_key": "SEED_002",
                "prompt": (
                    "Project folder icon, file management symbol, "
                    "teal accent #00bfa5, flat minimalist design, "
                    "vector icon, isolated on white background"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1024, "height": 1024},
                "num_inference_steps": 28,
            },

            # STATE MANAGEMENT ICONS
            {
                "id": "icon_009",
                "name": "workflow_branch",
                "priority": "MEDIUM",
                "scene": "Scene 8: State Management",
                "seed_key": "SEED_002",
                "prompt": (
                    "Workflow branch icon, fork path symbol, decision point, "
                    "modern tech UI style, blue/cyan gradient, "
                    "vector graphics, isolated on white background"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1024, "height": 1024},
                "num_inference_steps": 28,
            },
            {
                "id": "icon_010",
                "name": "save_disk",
                "priority": "MEDIUM",
                "scene": "Scene 8: State Management",
                "seed_key": "SEED_002",
                "prompt": (
                    "Save state icon, cloud upload symbol or floppy disk stylized, "
                    "modern clean UI, teal accent #00bfa5, "
                    "vector graphics, isolated on white background"
                ),
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1024, "height": 1024},
                "num_inference_steps": 28,
            },
        ]


def main():
    """Main execution"""
    generator = IconAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()


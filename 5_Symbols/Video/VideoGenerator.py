#!/usr/bin/env python3
"""
Video Asset Generator
Generates video assets using fal.ai with base class architecture
"""

from pathlib import Path
from typing import Dict, List

from Base.base_asset_generator import BaseAssetGenerator
from Base.generator_config import SEEDS, BRAND_COLORS


class VideoAssetGenerator(BaseAssetGenerator):
    """Generator for video assets"""
    
    def __init__(self):
        super().__init__(
            output_dir=Path("./generated_video"),
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="video"
        )
    
    def get_generation_queue(self) -> List[Dict]:
        """Return the list of videos to generate"""
        return [
            {
                "id": "4.1",
                "name": "uk_streets_sunday",
                "priority": "MEDIUM",
                "scene": "Scene 4: Skills Gap",
                "prompt": (
                    "Cinematic shot of empty UK high street on Sunday evening, closed shop fronts with metal shutters down, "
                    "dim streetlights beginning to illuminate, deserted pedestrian area, typical British town center architecture, "
                    "moody atmospheric lighting, golden hour or early dusk, realistic urban photography style, "
                    "slight film grain, 16:9 cinematic aspect ratio, melancholic mood, 4k, high resolution"
                ),
                "model": "fal-ai/minimax/video-01",
                "duration_seconds": 5,
                "aspect_ratio": "16:9"
            },
            {
                "id": "9.1",
                "name": "corporate_meeting",
                "priority": "LOW",
                "scene": "Scene 9: AI Transformation",
                "prompt": (
                    "Cinematic shot of modern corporate meeting room, 4-5 business professionals sitting around conference table "
                    "looking at laptops with frustrated expressions, large monitor on wall displaying generic charts, "
                    "glass walls visible, fluorescent office lighting, professional business environment, "
                    "realistic corporate photography style, slightly desaturated colors for serious tone, "
                    "slow camera movement, 4k"
                ),
                "model": "fal-ai/minimax/video-01",
                "duration_seconds": 5,
                "aspect_ratio": "16:9"
            },
            {
                "id": "1.1",
                "name": "ferrari_cart_morph",
                "priority": "HIGH",
                "scene": "Scene 1: Hook",
                "prompt": (
                    "Sleek red Ferrari sports car icon smoothly morphing into simple shopping cart icon, "
                    "clean vector style, white/transparent background, particle effects during transformation, "
                    "professional tech presentation aesthetic, minimalist flat design, modern motion graphics style"
                ),
                "model": "fal-ai/minimax/video-01",
                "duration_seconds": 5,
                "aspect_ratio": "16:9"
            }
        ]


def main():
    """Main execution"""
    generator = VideoAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()


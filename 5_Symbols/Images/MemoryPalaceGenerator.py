#!/usr/bin/env python3
"""
Memory Palace Asset Generator
Generates memory palace imagery using fal.ai with base class architecture
"""

from pathlib import Path
from typing import Dict, List

from base.base_asset_generator import BaseAssetGenerator
from base.generator_config import SEEDS, BRAND_COLORS, OUTPUT_FORMATS


class MemoryPalaceAssetGenerator(BaseAssetGenerator):
    """Generator for memory palace assets"""
    
    def __init__(self):
        # Custom seeds for memory palace
        memory_palace_seeds = {
            **SEEDS,
            "SEED_001": 555123,  # Ancient/Architectural
            "SEED_002": 555456,  # Surreal/Dreamlike
        }
        
        super().__init__(
            output_dir=Path("./generated_assets/memory_palace"),
            seeds=memory_palace_seeds,
            brand_colors=BRAND_COLORS,
            asset_type="memory_palace",
            output_format=OUTPUT_FORMATS.get("memory_palace", "jpeg")  # Use JPEG for memory palace (solid backgrounds)
        )
    
    def get_generation_queue(self) -> List[Dict]:
        """Return the list of memory palace assets to generate"""
        return [
            {
                "id": "MP.1",
                "name": "memory_palace_entrance",
                "priority": "HIGH",
                "scene": "Intro",
                "seed_key": "SEED_001",
                "prompt": "Grand entrance to a memory palace, classical greek architecture, marble columns, golden light, floating geometric symbols, ethereal atmosphere, cinematic lighting, 8k resolution, wide angle",
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
            {
                "id": "MP.2",
                "name": "locus_hall_of_mirrors",
                "priority": "MEDIUM",
                "scene": "Hallway",
                "seed_key": "SEED_002",
                "prompt": "A long hallway lined with mirrors, each mirror reflecting a different memory or data point, surreal style, infinite depth, glowing blue pathways on the floor, cybernetic architecture mixed with baroque style",
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            }
        ]


def main():
    """Main execution"""
    generator = MemoryPalaceAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
3D Asset Generator
Generates 3D model assets using fal.ai Hunyuan-3D with base class architecture
"""

from pathlib import Path
from typing import Dict, List

from Base.base_asset_generator import BaseAssetGenerator
from Base.generator_config import SEEDS, BRAND_COLORS, OUTPUT_FORMATS


class ThreeDAssetGenerator(BaseAssetGenerator):
    """Generator for 3D model assets using Hunyuan-3D text-to-3D"""
    
    def __init__(self):
        super().__init__(
            output_dir=Path("./generated_assets"),
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="3d",
            output_format=OUTPUT_FORMATS.get("3d", "glb")  # Use GLB for 3D models
        )
    
    def get_generation_queue(self) -> List[Dict]:
        """Return the list of 3D models to generate"""
        return [
            # HIGH PRIORITY 3D ASSETS
            {
                "id": "3d.1",
                "name": "shopping_cart_3d",
                "priority": "HIGH",
                "scene": "Scene 1: Hook",
                "seed_key": "SEED_001",
                "prompt": (
                    "A modern shopping cart, sleek metallic design, detailed wheels, "
                    "professional product visualization, clean geometry, suitable for animation, "
                    "realistic materials with reflective metal surfaces"
                ),
                "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
            },
            {
                "id": "3d.2",
                "name": "ferrari_sports_car_3d",
                "priority": "HIGH",
                "scene": "Scene 1: Hook",
                "seed_key": "SEED_001",
                "prompt": (
                    "A sleek red Ferrari sports car, detailed exterior, "
                    "high-quality 3D model with realistic paint material, "
                    "professional automotive visualization, clean topology"
                ),
                "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
            },
            {
                "id": "3d.3",
                "name": "ai_robot_brain_3d",
                "priority": "MEDIUM",
                "scene": "Scene 4: Skills Gap",
                "seed_key": "SEED_002",
                "prompt": (
                    "An AI robot brain with neural network connections, "
                    "futuristic design, glowing blue accents, holographic elements, "
                    "tech-inspired geometry, suitable for AI visualization"
                ),
                "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
            },
            {
                "id": "3d.4",
                "name": "smartphone_notification_3d",
                "priority": "MEDIUM",
                "scene": "Scene 4: Skills Gap",
                "seed_key": "SEED_002",
                "prompt": (
                    "A modern smartphone with notification badge icon floating above it, "
                    "clean product design, detailed screen, metallic frame, "
                    "professional product visualization"
                ),
                "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
            },
            {
                "id": "3d.5",
                "name": "workflow_node_3d",
                "priority": "MEDIUM",
                "scene": "Scene 5: Bounded Contexts",
                "seed_key": "SEED_002",
                "prompt": (
                    "A geometric node representing a workflow step, "
                    "hexagonal or rounded cube shape, clean edges, "
                    "suitable for technical diagrams, minimalist design"
                ),
                "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
            },
            {
                "id": "3d.6",
                "name": "database_cylinder_3d",
                "priority": "LOW",
                "scene": "Scene 8: State Management",
                "seed_key": "SEED_002",
                "prompt": (
                    "A database cylinder icon in 3D, classic database symbol, "
                    "clean geometric design, metallic or glass material, "
                    "suitable for technical architecture visualization"
                ),
                "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
            },
        ]
    
    def extract_result_url(self, result: Dict, asset_config: Dict) -> str:
        """
        Extract the GLB model URL from the Hunyuan-3D API response.
        
        Args:
            result: Response from fal.ai API
            asset_config: Configuration for the asset
            
        Returns:
            URL of the generated GLB model, or None if not found
        """
        # Hunyuan-3D returns model_urls with glb and obj formats
        if result and "model_urls" in result:
            if "glb" in result["model_urls"]:
                return result["model_urls"]["glb"]["url"]
        
        # Fallback to default extraction
        return super().extract_result_url(result, asset_config)


def main():
    """Main execution"""
    generator = ThreeDAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()


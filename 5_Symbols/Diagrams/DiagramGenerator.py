#!/usr/bin/env python3
"""
Diagram Asset Generator
Generates diagram assets using fal.ai with base class architecture
"""

from pathlib import Path
from typing import Dict, List

from base.base_asset_generator import BaseAssetGenerator
from base.generator_config import SEEDS, BRAND_COLORS, OUTPUT_FORMATS


class DiagramAssetGenerator(BaseAssetGenerator):
    """Generator for diagram assets"""
    
    def __init__(self):
        super().__init__(
            output_dir=Path("./generated_diagrams"),
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="diagram",
            output_format=OUTPUT_FORMATS.get("diagram", "jpeg")  # Use JPEG for diagrams (solid backgrounds)
        )
    
    def get_generation_queue(self) -> List[Dict]:
        """Return the list of diagrams to generate"""
        return [
            {
                "id": "D1.1",
                "name": "agentic_workflow_architecture",
                "priority": "HIGH",
                "scene": "Scene 1",
                "seed_key": "SEED_001",
                "prompt": "High-level technical architecture diagram of an Agentic Workflow system, showing 'User Intent' box -> 'Orchestrator Agent' (central hub) -> connected to multiple specialized Sub-Agents (Research, Coding, Testing, Deployment), connected by data pipelines, clean modern aesthetic, dark background separate distinct nodes, professional software diagram style, 16:9",
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
            {
                "id": "D2.1",
                "name": "data_flow_process",
                "priority": "MEDIUM",
                "scene": "Scene 2",
                "seed_key": "SEED_002",
                "prompt": "Horizontal process flowchart 'Raw Data' -> 'Processing Node' -> 'Structured Output', interconnected with directional arrows, gradients indicating flow, distinct steps, n8n style nodes, modern smooth vector graphics, dark mode UI, blue and purple neon accents, 16:9",
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
             {
                "id": "D3.1",
                "name": "neural_network_concept",
                "priority": "LOW",
                "scene": "Scene 3",
                "seed_key": "SEED_003",
                "prompt": "Abstract concept map of a neural network, nodes connecting in a mesh, glowing connections, highlighting the concept of 'Learning' and 'Adaptation', futuristic tech style, deep blue background, cyber security aesthetic, 16:9",
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
            },
        ]


def main():
    """Main execution"""
    generator = DiagramAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()


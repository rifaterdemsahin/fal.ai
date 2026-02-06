#!/usr/bin/env python3
"""
Music Asset Generator
Generates music assets using fal.ai with base class architecture
"""

from pathlib import Path
from typing import Dict, List, Optional, Any

from base.base_asset_generator import BaseAssetGenerator
from base.generator_config import SEEDS, BRAND_COLORS


class MusicAssetGenerator(BaseAssetGenerator):
    """Generator for music assets"""
    
    def __init__(self):
        super().__init__(
            output_dir=Path("./generated_music"),
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="music"
        )
    
    def prepare_arguments(self, asset_config: Dict) -> Dict[str, Any]:
        """Prepare arguments for music generation"""
        arguments = {
            "prompt": asset_config["prompt"],
        }
        
        if "seconds_total" in asset_config:
            arguments["seconds_total"] = asset_config["seconds_total"]
            
        return arguments
    
    def extract_result_url(self, result: Dict, asset_config: Dict) -> Optional[str]:
        """Extract result URL from music generation response"""
        if result and "audio_file" in result:
            return result["audio_file"]["url"]
        elif result and "url" in result:
            return result["url"]
        return None
    
    def get_generation_queue(self) -> List[Dict]:
        """Return the list of music tracks to generate"""
        return [
            {
                "id": "music_01",
                "name": "tech_innovation_background",
                "priority": "HIGH",
                "prompt": "Upbeat, tech-focused background track, modern synthesizer, rhythmic, innovation, energetic but not distracting, suitable for technology tutorial video, high quality audio",
                "model": "fal-ai/stable-audio",
                "seconds_total": 47,
            },
            {
                "id": "music_02",
                "name": "cta_energy_build",
                "priority": "HIGH",
                "prompt": "High energy, motivational build-up music, cinematic, orchestral hybrid, inspiring, driving rhythm, building tension and release, suitable for call to action, high quality",
                "model": "fal-ai/stable-audio",
                "seconds_total": 47,
            },
            {
                "id": "music_03",
                "name": "screen_recording_bed",
                "priority": "MEDIUM",
                "prompt": "Subtle background music, sweet, calm, lo-fi beats, gentle, non-intrusive, suitable for concentration and screen recording demonstration, high quality",
                "model": "fal-ai/stable-audio",
                "seconds_total": 47,
            }
        ]


def main():
    """Main execution"""
    generator = MusicAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()

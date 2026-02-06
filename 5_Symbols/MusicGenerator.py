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
        """Prepare arguments for music generation using Beatoven"""
        arguments = {
            "prompt": asset_config["prompt"],
        }
        
        # Beatoven-specific parameters
        if "duration" in asset_config:
            arguments["duration"] = asset_config["duration"]
        elif "seconds_total" in asset_config:
            # Support legacy parameter name for backwards compatibility
            arguments["duration"] = asset_config["seconds_total"]
        
        if "negative_prompt" in asset_config:
            arguments["negative_prompt"] = asset_config["negative_prompt"]
        
        if "refinement" in asset_config:
            arguments["refinement"] = asset_config["refinement"]
        
        if "creativity" in asset_config:
            arguments["creativity"] = asset_config["creativity"]
        
        # Add seed support
        if "seed_key" in asset_config and asset_config["seed_key"] in self.seeds:
            arguments["seed"] = self.seeds[asset_config["seed_key"]]
        elif "seed" in asset_config:
            arguments["seed"] = asset_config["seed"]
            
        return arguments
    
    def extract_result_url(self, result: Dict, asset_config: Dict) -> Optional[str]:
        """Extract result URL from Beatoven music generation response"""
        # Beatoven returns: {"audio": {"url": "...", "content_type": "audio/wav", ...}, "prompt": "...", "metadata": {...}}
        if result and "audio" in result and "url" in result["audio"]:
            return result["audio"]["url"]
        # Fallback for other response formats
        elif result and "audio_file" in result:
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
                "model": "beatoven/music-generation",
                "duration": 90,
                "creativity": 14,
                "refinement": 100,
            },
            {
                "id": "music_02",
                "name": "cta_energy_build",
                "priority": "HIGH",
                "prompt": "High energy, motivational build-up music, cinematic, orchestral hybrid, inspiring, driving rhythm, building tension and release, suitable for call to action, high quality",
                "model": "beatoven/music-generation",
                "duration": 60,
                "creativity": 16,
                "refinement": 100,
            },
            {
                "id": "music_03",
                "name": "screen_recording_bed",
                "priority": "MEDIUM",
                "prompt": "Subtle background music, sweet, calm, lo-fi beats, gentle, non-intrusive, suitable for concentration and screen recording demonstration, high quality",
                "model": "beatoven/music-generation",
                "duration": 120,
                "creativity": 12,
                "refinement": 100,
            }
        ]


def main():
    """Main execution"""
    generator = MusicAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()

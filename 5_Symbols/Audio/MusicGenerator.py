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
        
        # Handle duration parameter based on model
        if "duration" in asset_config:
            if "stable-audio" in asset_config.get("model", ""):
                arguments["seconds_total"] = asset_config["duration"]
            else:
                arguments["duration"] = asset_config["duration"]
        elif "seconds_total" in asset_config:
            if "stable-audio" in asset_config.get("model", ""):
                 arguments["seconds_total"] = asset_config["seconds_total"]
            else:
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
        """Extract result URL from API response"""
        # fal-ai/stable-audio returns: {"audio_file": {"url": "...", ...}}
        if result and "audio_file" in result and "url" in result["audio_file"]:
            return result["audio_file"]["url"]
        
        # Beatoven returns: {"audio": {"url": "...", ...}}
        if result and "audio" in result and "url" in result["audio"]:
            return result["audio"]["url"]
            
        # Fallback
        if result and "url" in result:
            return result["url"]
        return None

    def get_file_extension(self, asset_config: Dict) -> str:
        """Get file extension based on model"""
        if "stable-audio" in asset_config.get("model", ""):
            return "mp3"
        return "wav"

    def convert_audio(self, input_path: Path, output_ext: str) -> Optional[Path]:
        """Convert audio file using ffmpeg"""
        import subprocess
        
        output_path = input_path.with_suffix(output_ext)
        if output_path.exists():
            return output_path
            
        print(f"   ðŸ”„ Converting to {output_ext}...")
        try:
            cmd = [
                "ffmpeg", "-y", "-i", str(input_path),
                "-acodec", "libmp3lame" if output_ext == ".mp3" else "pcm_s16le",
                str(output_path)
            ]
            # Suppress output unless error
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print(f"   âœ… Converted: {output_path.name}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"   âŒ Conversion failed: {e}")
            return None
        except FileNotFoundError:
            print("   âŒ ffmpeg not found. Skipping conversion.")
            return None

    def generate_asset(self, asset_config: Dict, version: int = 1) -> Dict:
        """Override to add conversion step"""
        result = super().generate_asset(asset_config, version)
        
        if result["success"] and "local_path" in result:
            local_path = Path(result["local_path"])
            
            # Ensure we have both MP3 and WAV
            if local_path.suffix.lower() == ".wav":
                self.convert_audio(local_path, ".mp3")
            elif local_path.suffix.lower() == ".mp3":
                self.convert_audio(local_path, ".wav")
                
        return result
    
    def get_generation_queue(self) -> List[Dict]:
        """Return the list of music tracks to generate"""
        return [
            {
                "id": "music_01",
                "name": "tech_innovation_stable",
                "priority": "HIGH",
                "prompt": "Upbeat, tech-focused background track, modern synthesizer, rhythmic, innovation",
                "model": "fal-ai/stable-audio", 
                "duration": 47, # Stable Audio max is 47s
            },
            {
                "id": "music_02",
                "name": "cta_energy_beatoven",
                "priority": "HIGH",
                "prompt": "High energy, motivational build-up music, cinematic, orchestral hybrid",
                "model": "beatoven/music-generation",
                "duration": 60,
                "creativity": 16,
                "refinement": 100,
            },
            {
                "id": "music_03",
                "name": "screen_recording_stable",
                "priority": "MEDIUM",
                "prompt": "Subtle background music, sweet, calm, lo-fi beats, gentle",
                "model": "fal-ai/stable-audio",
                "duration": 45,
            }
        ]


def main():
    """Main execution"""
    generator = MusicAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()


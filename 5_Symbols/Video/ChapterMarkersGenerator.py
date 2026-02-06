#!/usr/bin/env python3
"""
Chapter Markers Asset Generator
Generates chapter marker title cards using fal.ai with base class architecture
"""

from pathlib import Path
from typing import Dict, List
import re

from base.base_asset_generator import BaseAssetGenerator
from base.generator_config import SEEDS, BRAND_COLORS, OUTPUT_FORMATS


class ChapterMarkersAssetGenerator(BaseAssetGenerator):
    """Generator for chapter marker assets"""
    
    # Regex pattern for parsing chapter markers
    CHAPTER_MARKER_PATTERN = re.compile(r'^(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)$')
    
    def __init__(self):
        # Custom seeds for chapter markers
        chapter_seeds = {
            **SEEDS,
            "SEED_CHAPTERS": 999001,  # Consistent style for all chapters
        }
        
        super().__init__(
            output_dir=Path("./generated_chapter_markers"),
            seeds=chapter_seeds,
            brand_colors=BRAND_COLORS,
            asset_type="chapter_marker",
            output_format=OUTPUT_FORMATS.get("chapter_marker", "jpeg")  # Use JPEG for chapter markers (solid backgrounds)
        )
        
        self.chapter_markers_file = Path("./chapter_markers.txt")
    
    def read_chapter_markers(self, file_path: Path) -> List[tuple]:
        """Parse the chapter markers file"""
        if not file_path.exists():
            print(f"❌ Chapter markers file not found: {file_path}")
            return []

        markers = []
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                match = self.CHAPTER_MARKER_PATTERN.match(line)
                if match:
                    timestamp = match.group(1)
                    title = match.group(2)
                    markers.append((timestamp, title))
                else:
                    print(f"⚠️ Could not parse line: {line}")
        return markers
    
    def build_generation_queue_from_markers(self, markers: List[tuple]) -> List[Dict]:
        """Build the asset generation queue from chapter markers"""
        queue = []
        for i, (timestamp, title) in enumerate(markers, 1):
            safe_title = re.sub(r'[^a-z0-9]', '_', title.lower()).strip('_')
            safe_title = re.sub(r'_+', '_', safe_title)
            
            asset_id = f"CH_{i:02d}"
            
            prompt = (
                f"Cinematic video chapter title card with text '{title}' written in large, bold, futuristic sans-serif font centered. "
                f"Background is a sleek, modern tech abstract design with deep dark blue ({self.brand_colors['primary_dark']}) "
                f"and glowing accents in cyan ({self.brand_colors['accent_blue']}) and purple ({self.brand_colors['accent_purple']}). "
                "High contrast, professional motion graphics style, 8k resolution, highly detailed, "
                "digital interface elements, subtle grid patterns, glassmorphism effects. "
                "Text must be clearly legible and the focal point."
            )

            queue.append({
                "id": asset_id,
                "name": f"chapter_{i:02d}_{safe_title}",
                "priority": "HIGH",
                "scene": f"Chapter {i}: {title} ({timestamp})",
                "seed_key": "SEED_CHAPTERS",
                "prompt": prompt,
                "model": "fal-ai/flux/dev",
                "image_size": {"width": 1920, "height": 1080},
                "num_inference_steps": 28,
                "timestamp": timestamp,
                "original_title": title
            })
        return queue
    
    def get_generation_queue(self) -> List[Dict]:
        """Return the list of chapter marker assets to generate"""
        if self.chapter_markers_file.exists():
            markers = self.read_chapter_markers(self.chapter_markers_file)
            if markers:
                return self.build_generation_queue_from_markers(markers)
        
        # Fallback to empty queue if file doesn't exist
        print(f"⚠️ No chapter markers file found at {self.chapter_markers_file}")
        return []


def main():
    """Main execution"""
    generator = ChapterMarkersAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()

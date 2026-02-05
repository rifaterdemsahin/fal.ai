#!/usr/bin/env python3
"""
Audio Asset Generator
Generates YouTube chapter markers from EDL
"""

import re
from pathlib import Path
from typing import Dict, List

from base.base_asset_generator import BaseAssetGenerator
from base.generator_config import SEEDS, BRAND_COLORS


class AudioAssetGenerator(BaseAssetGenerator):
    """Generator for audio/chapter marker text files"""
    
    def __init__(self):
        super().__init__(
            output_dir=Path("./generated_audio"),
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="audio"
        )
        
        self.edl_path = Path("../3_Simulation/Feb1Youtube/source_edl.md")
        self.output_file = self.output_dir / "chapter_markers.txt"
    
    def parse_timecode(self, time_str: str) -> str:
        """Normalize timecode (e.g., 0:00 -> 00:00)"""
        parts = time_str.split(':')
        if len(parts) == 2:
            m, s = parts
            return f"{int(m):02d}:{s}"
        return time_str
    
    def format_title(self, text: str) -> str:
        """Convert ALL CAPS to Title Case and fix common acronyms"""
        corrections = {
            "Ai": "AI",
            "Mcp": "MCP",
            "Para": "PARA",
            "N8n": "n8n",
            "Uk": "UK",
            "Vs": "VS",
            "Cli": "CLI",
            "Api": "API"
        }
        
        title_cased = text.title()
        words = title_cased.split()
        fixed_words = [corrections.get(w, w) for w in words]
        return " ".join(fixed_words)
    
    def generate_chapter_markers(self) -> Dict:
        """Parse EDL and generate YouTube chapter markers"""
        print(f"\n{'='*60}")
        print("🔖 GENERATING CHAPTER MARKERS")
        print(f"   Source: {self.edl_path}")
        print(f"{'='*60}")

        if not self.edl_path.exists():
            return {
                "success": False,
                "error": f"EDL file not found: {self.edl_path}"
            }

        content = self.edl_path.read_text(encoding='utf-8')
        lines = content.splitlines()

        markers = []
        current_scene_title = None

        scene_pattern = re.compile(r'^### \*\*SCENE \d+: (.+)\*\*\s*$')
        duration_pattern = re.compile(r'\*\*Duration:\*\* (\d+:\d+)')

        for line in lines:
            line = line.strip()
            
            scene_match = scene_pattern.match(line)
            if scene_match:
                raw_title = scene_match.group(1).strip()
                current_scene_title = self.format_title(raw_title)
                continue

            duration_match = duration_pattern.search(line)
            if duration_match and current_scene_title:
                start_time = duration_match.group(1)
                formatted_time = self.parse_timecode(start_time)
                
                marker_line = f"{formatted_time} {current_scene_title}"
                markers.append(marker_line)
                print(f"   • Found: {marker_line}")
                
                current_scene_title = None

        if markers:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            output_content = "\n".join(markers)
            self.output_file.write_text(output_content, encoding='utf-8')
            
            print(f"\n{'='*60}")
            print(f"✅ Generated {len(markers)} markers")
            print(f"💾 Saved to: {self.output_file}")
            print(f"{'='*60}")
            print("\nCHAPTER MARKERS LIST:")
            print("-" * 20)
            print(output_content)
            print("-" * 20)
            
            return {
                "success": True,
                "local_path": str(self.output_file),
                "markers_count": len(markers)
            }
        else:
            return {
                "success": False,
                "error": "No markers found. Check EDL format."
            }
    
    def get_generation_queue(self) -> List[Dict]:
        """Return empty queue - this generator creates text file directly"""
        return []
    
    def run(self, confirm: bool = True):
        """Main execution method"""
        if confirm:
            print("\n" + "="*60)
            response = input("🤔 Proceed with chapter marker generation? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("❌ Cancelled by user")
                return
        
        result = self.generate_chapter_markers()
        
        if result["success"]:
            print("\n✅ Done!")
        else:
            print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")


def main():
    """Main execution"""
    generator = AudioAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()

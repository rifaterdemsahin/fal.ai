#!/usr/bin/env python3
"""
Audio Asset Generator
Generates YouTube chapter markers from EDL
"""

import re
import sys
from pathlib import Path
from typing import Dict, List

# Add parent directory to path to import base modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from base.base_asset_generator import BaseAssetGenerator
from base.generator_config import SEEDS, BRAND_COLORS, DEFAULT_EDL_PATH


class AudioAssetGenerator(BaseAssetGenerator):
    """Generator for audio/chapter marker text files"""

    # Regex patterns for EDL parsing (table format)
    # Matches: | **01** | 01:00:00 | **The Pivot** | Host holding...
    TABLE_ROW_PATTERN = re.compile(r'\|\s*\*\*(\d+)\*\*\s*\|\s*([\d:]+)\s*\|\s*\*\*(.+?)\*\*\s*\|')
    
    def __init__(self, edl_path: Path = None):
        super().__init__(
            output_dir=Path("./generated_audio"),
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="audio"
        )
        
        # Allow custom EDL path or use default from config
        if edl_path is None:
            self.edl_path = Path(DEFAULT_EDL_PATH)
        else:
            self.edl_path = edl_path
            
        self.output_file = self.output_dir / "chapter_markers.txt"
    
    def parse_timecode(self, time_str: str) -> str:
        """Convert timecode from HH:MM:SS to MM:SS for YouTube chapters"""
        time_str = time_str.strip()
        parts = time_str.split(':')

        if len(parts) == 3:
            # Format: HH:MM:SS -> convert to MM:SS
            h, m, s = parts
            total_minutes = int(h) * 60 + int(m)
            return f"{total_minutes:02d}:{s}"
        elif len(parts) == 2:
            # Format: MM:SS -> ensure 2-digit minutes
            m, s = parts
            return f"{int(m):02d}:{s}"

        return time_str
    
    def format_title(self, text: str) -> str:
        """Convert text to Title Case and fix common acronyms"""
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
        print("ðŸ”– GENERATING CHAPTER MARKERS")
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

        for line in lines:
            line = line.strip()

            # Match table rows like: | **01** | 01:00:00 | **The Pivot** | ...
            table_match = self.TABLE_ROW_PATTERN.search(line)
            if table_match:
                scene_num = table_match.group(1)
                timestamp = table_match.group(2)
                title = table_match.group(3).strip()

                formatted_time = self.parse_timecode(timestamp)
                formatted_title = self.format_title(title)

                marker_line = f"{formatted_time} {formatted_title}"
                markers.append(marker_line)
                print(f"   • Scene {scene_num}: {marker_line}")

        if markers:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            output_content = "\n".join(markers)
            self.output_file.write_text(output_content, encoding='utf-8')
            
            print(f"\n{'='*60}")
            print(f"âœ… Generated {len(markers)} markers")
            print(f"ðŸ’¾ Saved to: {self.output_file}")
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
            response = input("ðŸ¤” Proceed with chapter marker generation? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("âŒ Cancelled by user")
                return
        
        result = self.generate_chapter_markers()
        
        if result["success"]:
            print("\nâœ… Done!")
        else:
            print(f"\nâŒ Failed: {result.get('error', 'Unknown error')}")


def main():
    """Main execution"""
    # Set directories from arguments or use defaults
    input_dir = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/input")
    output_dir = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/output")

    edl_path = input_dir / "source_edl.md"

    print("=" * 60)
    print("🎵 AUDIO CHAPTER MARKERS GENERATOR")
    print("=" * 60)
    print(f"💰 Cost: $0.00 (FREE! Text processing)")
    print(f"📥 Input EDL:  {edl_path}")
    print(f"📤 Output:     {output_dir}")
    print("=" * 60)

    # Override output directory
    generator = AudioAssetGenerator(edl_path=edl_path)
    generator.output_dir = output_dir
    generator.output_file = output_dir / "chapter_markers.txt"

    # Run without confirmation prompt for automation
    generator.run(confirm=False)


if __name__ == "__main__":
    main()


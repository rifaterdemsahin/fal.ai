#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Audio/Markers
Project: The Agentic Era - Managing 240+ Workflows
Generates YouTube chapter markers based on EDL scene breakdown
"""

import os
import re
from pathlib import Path

# Configuration
# Configuration
EDL_PATH = Path("../3_Simulation/Feb1Youtube/source_edl.md") # Default path
DEFAULT_OUTPUT_DIR = Path("./generated_audio")
DEFAULT_OUTPUT_FILE = DEFAULT_OUTPUT_DIR / "chapter_markers.txt"

def parse_timecode(time_str):
    """Normalize timecode (e.g., 0:00 -> 00:00)"""
    parts = time_str.split(':')
    if len(parts) == 2:
        m, s = parts
        return f"{int(m):02d}:{s}"
    return time_str

def format_title(text):
    """Convert ALL CAPS to Title Case and fix common acronyms"""
    # specific overrides
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
    
    # Standard Title Case
    title_cased = text.title()
    
    # Apply corrections
    words = title_cased.split()
    fixed_words = [corrections.get(w, w) for w in words]
    return " ".join(fixed_words)

def generate_chapter_markers(edl_path: Path, output_file: Path):
    """Parse EDL and generate YouTube chapter markers"""
    
    print(f"\n{'='*60}")
    print("🔖 GENERATING CHAPTER MARKERS")
    print(f"   Source: {edl_path}")
    print(f"{'='*60}")

    if not edl_path.exists():
        print(f"❌ Error: {edl_path} not found.")
        return

    content = edl_path.read_text(encoding='utf-8')
    lines = content.splitlines()

    markers = []
    current_scene_title = None

    # Regex patterns
    # Matches: ### **SCENE 1: HOOK & PROBLEM STATEMENT**
    scene_pattern = re.compile(r'^### \*\*SCENE \d+: (.+)\*\*\s*$')
    # Matches: **Duration:** 0:00 - 0:45
    duration_pattern = re.compile(r'\*\*Duration:\*\* (\d+:\d+)')

    for line in lines:
        line = line.strip()
        
        # Check for Scene Header
        scene_match = scene_pattern.match(line)
        if scene_match:
            raw_title = scene_match.group(1).strip()
            current_scene_title = format_title(raw_title)
            continue

        # Check for Duration
        duration_match = duration_pattern.search(line)
        if duration_match and current_scene_title:
            start_time = duration_match.group(1)
            formatted_time = parse_timecode(start_time)
            
            marker_line = f"{formatted_time} {current_scene_title}"
            markers.append(marker_line)
            print(f"   • Found: {marker_line}")
            
            current_scene_title = None # Reset until next scene

    if markers:
        # Ensure parent dir exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        output_content = "\n".join(markers)
        output_file.write_text(output_content, encoding='utf-8')
        
        print(f"\n{'='*60}")
        print(f"✅ Generated {len(markers)} markers")
        print(f"💾 Saved to: {output_file}")
        print(f"{'='*60}")
        print("\nCHAPTER MARKERS LIST:")
        print("-" * 20)
        print(output_content)
        print("-" * 20)
    else:
        print("\n❌ No markers found. Check EDL format.")

def main():
    generate_chapter_markers(EDL_PATH, DEFAULT_OUTPUT_FILE)

if __name__ == "__main__":
    main()

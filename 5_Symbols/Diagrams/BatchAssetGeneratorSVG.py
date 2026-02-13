#!/usr/bin/env python3
"""
SVG Batch Asset Generator
Project: The Delivery Pilot Transformation
Generates SVG diagrams for each scene in the video script.
Cost: $0.00 (SVGs are generated locally, no API calls)
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Import asset utilities from same directory (5_Symbols)
current_dir = Path(__file__).parent
project_root = current_dir.parent

try:
    from asset_utils import generate_filename, extract_scene_number, ManifestTracker, convert_svg_to_jpeg
except ImportError:
    # Fallback if running standalone
    print("⚠️  asset_utils not found. Using legacy naming convention.")
    generate_filename = None
    extract_scene_number = None
    ManifestTracker = None
    convert_svg_to_jpeg = None

# Configuration - output to weekly simulation folder
OUTPUT_DIR = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/output")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Display constants
SEPARATOR_WIDTH = 60
TEXT_LINE_HEIGHT = 25
LABEL_OFFSET = 15

# Brand color palette
BRAND_COLORS = {
    "primary_dark": "#1a1a2e",
    "accent_blue": "#00d4ff",
    "accent_purple": "#7b2cbf",
    "secondary_teal": "#00bfa5",
    "highlight_orange": "#ff6b35",
    "text_white": "#ffffff",
    "box_fill": "#2e2e4e",
    "arrow_color": "#00d4ff",
}

# ─── SVG Generation Queue — one per scene from the script ─────────────────────

GENERATION_QUEUE = [
    # Scene 1: The Heavy Mic — Enterprise vs Delivery Pilot hierarchy
    {
        "id": "SVG1.1",
        "name": "svg_01_enterprise_vs_delivery_pilot",
        "priority": "HIGH",
        "scene": "Scene 1: The Heavy Mic",
        "diagram_type": "comparison",
        "elements": [
            {"type": "box", "text": "Enterprise\nEngineers", "x": 80, "y": 80, "width": 220, "height": 100,
             "fill": "#3a3a3a", "stroke": "#6b6b6b", "text_color": "#cccccc"},
            {"type": "box", "text": "Golden Mic\n(10-Year Race)", "x": 80, "y": 240, "width": 220, "height": 100,
             "fill": "#3a3a3a", "stroke": "#FFD700", "text_color": "#FFD700"},
            {"type": "arrow", "x1": 190, "y1": 180, "x2": 190, "y2": 240, "color": "#6b6b6b", "label": "Gatekeeping"},
            {"type": "box", "text": "Delivery\nPilot", "x": 500, "y": 80, "width": 220, "height": 100,
             "fill": "#2e2e4e", "stroke": "#00d4ff", "text_color": "#ffffff"},
            {"type": "box", "text": "AI Tools\n(No Code)", "x": 500, "y": 240, "width": 220, "height": 100,
             "fill": "#2e2e4e", "stroke": "#00bfa5", "text_color": "#00bfa5"},
            {"type": "arrow", "x1": 610, "y1": 180, "x2": 610, "y2": 240, "color": "#00d4ff", "label": "Accessible"},
        ],
        "canvas_width": 800, "canvas_height": 420, "background": "#1a1a2e",
    },
    # Scene 2: The Pivot — 240 Workflows to No-Code
    {
        "id": "SVG2.1",
        "name": "svg_02_pivot_from_complex_to_simple",
        "priority": "HIGH",
        "scene": "Scene 2: The Pivot",
        "diagram_type": "flow",
        "elements": [
            {"type": "box", "text": "240 Complex\nWorkflows", "x": 50, "y": 160, "width": 200, "height": 100,
             "fill": "#3a3a3a", "stroke": "#ff4444", "text_color": "#ff4444"},
            {"type": "arrow", "x1": 270, "y1": 210, "x2": 370, "y2": 210, "color": "#FFD700", "label": "PIVOT"},
            {"type": "box", "text": "No-Code\nTools", "x": 390, "y": 160, "width": 200, "height": 100,
             "fill": "#2e2e4e", "stroke": "#00d4ff", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 610, "y1": 210, "x2": 710, "y2": 210, "color": "#00bfa5"},
            {"type": "box", "text": "Delivery\nPilot", "x": 730, "y": 160, "width": 200, "height": 100,
             "fill": "#2e2e4e", "stroke": "#00bfa5", "text_color": "#00bfa5"},
        ],
        "canvas_width": 1000, "canvas_height": 420, "background": "#1a1a2e",
    },
    # Scene 3: Statues vs Mercury — Static vs Dynamic
    {
        "id": "SVG3.1",
        "name": "svg_03_static_vs_dynamic_rules",
        "priority": "HIGH",
        "scene": "Scene 3: Statues vs Mercury",
        "diagram_type": "comparison",
        "elements": [
            {"type": "box", "text": "Static Rules", "x": 80, "y": 60, "width": 240, "height": 80,
             "fill": "#3a3a3a", "stroke": "#6b6b6b", "text_color": "#cccccc"},
            {"type": "arrow", "x1": 200, "y1": 140, "x2": 200, "y2": 180, "color": "#6b6b6b"},
            {"type": "box", "text": "Hard-Coded", "x": 80, "y": 180, "width": 240, "height": 70,
             "fill": "#3a3a3a", "stroke": "#6b6b6b", "text_color": "#999999"},
            {"type": "arrow", "x1": 200, "y1": 250, "x2": 200, "y2": 290, "color": "#ff4444"},
            {"type": "box", "text": "BREAKS ✗", "x": 120, "y": 290, "width": 160, "height": 60,
             "fill": "#4a1a1a", "stroke": "#ff4444", "text_color": "#ff4444"},
            # Dynamic side
            {"type": "box", "text": "Dynamic AI", "x": 480, "y": 60, "width": 240, "height": 80,
             "fill": "#2e2e4e", "stroke": "#00d4ff", "text_color": "#00d4ff"},
            {"type": "arrow", "x1": 600, "y1": 140, "x2": 600, "y2": 180, "color": "#00d4ff"},
            {"type": "box", "text": "Adaptive", "x": 480, "y": 180, "width": 240, "height": 70,
             "fill": "#2e2e4e", "stroke": "#7b2cbf", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 600, "y1": 250, "x2": 600, "y2": 290, "color": "#00bfa5"},
            {"type": "box", "text": "ADAPTS ✓", "x": 520, "y": 290, "width": 160, "height": 60,
             "fill": "#1a3a2a", "stroke": "#00bfa5", "text_color": "#00bfa5"},
        ],
        "canvas_width": 800, "canvas_height": 420, "background": "#1a1a2e",
    },
    # Scene 4: The Clone Lab — Git Clone Process
    {
        "id": "SVG4.1",
        "name": "svg_04_git_clone_process",
        "priority": "HIGH",
        "scene": "Scene 4: The Clone Lab",
        "diagram_type": "flow",
        "elements": [
            {"type": "box", "text": "GitHub\nRepository", "x": 50, "y": 160, "width": 180, "height": 100,
             "fill": "#2e2e4e", "stroke": "#00d4ff", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 250, "y1": 210, "x2": 340, "y2": 210, "color": "#00d4ff", "label": "git clone"},
            {"type": "box", "text": "Local\nPowerhouse", "x": 360, "y": 160, "width": 180, "height": 100,
             "fill": "#2e2e4e", "stroke": "#00bfa5", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 560, "y1": 210, "x2": 650, "y2": 210, "color": "#00bfa5", "label": "Run Agent"},
            {"type": "box", "text": "Tooling\nSystem", "x": 670, "y": 160, "width": 180, "height": 100,
             "fill": "#2e2e4e", "stroke": "#7b2cbf", "text_color": "#ffffff"},
        ],
        "canvas_width": 920, "canvas_height": 420, "background": "#1a1a2e",
    },
    # Scene 5: The Free Tier Journey — Tool Evolution
    {
        "id": "SVG5.1",
        "name": "svg_05_tool_evolution_tiers",
        "priority": "HIGH",
        "scene": "Scene 5: Free Tier Journey",
        "diagram_type": "flow",
        "elements": [
            {"type": "box", "text": "VS Code\n+ GitHub\n(FREE)", "x": 50, "y": 130, "width": 180, "height": 120,
             "fill": "#2e2e4e", "stroke": "#00bfa5", "text_color": "#00bfa5"},
            {"type": "arrow", "x1": 250, "y1": 190, "x2": 340, "y2": 190, "color": "#FFD700", "label": "Level Up"},
            {"type": "box", "text": "GitHub\nCopilot\n(Pair Pilot)", "x": 360, "y": 130, "width": 180, "height": 120,
             "fill": "#2e2e4e", "stroke": "#00d4ff", "text_color": "#00d4ff"},
            {"type": "arrow", "x1": 560, "y1": 190, "x2": 650, "y2": 190, "color": "#FFD700", "label": "Level Up"},
            {"type": "box", "text": "Cursor AI\n(Agentic)", "x": 670, "y": 130, "width": 180, "height": 120,
             "fill": "#2e2e4e", "stroke": "#7b2cbf", "text_color": "#7b2cbf"},
        ],
        "canvas_width": 920, "canvas_height": 400, "background": "#1a1a2e",
    },
    # Scene 6: Internet Kill Switch — Network Diagram
    {
        "id": "SVG6.1",
        "name": "svg_06_internet_kill_switch",
        "priority": "HIGH",
        "scene": "Scene 6: Internet Kill Switch",
        "diagram_type": "flow",
        "elements": [
            {"type": "box", "text": "GitHub\nWorkflow", "x": 50, "y": 50, "width": 180, "height": 90,
             "fill": "#2e2e4e", "stroke": "#00d4ff", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 250, "y1": 95, "x2": 340, "y2": 95, "color": "#00d4ff", "label": "Trigger"},
            {"type": "box", "text": "KILL\nSWITCH", "x": 360, "y": 50, "width": 180, "height": 90,
             "fill": "#4a1a1a", "stroke": "#ff4444", "text_color": "#ff4444"},
            {"type": "arrow", "x1": 450, "y1": 140, "x2": 300, "y2": 220, "color": "#00bfa5", "label": "Kid A: ON"},
            {"type": "arrow", "x1": 450, "y1": 140, "x2": 600, "y2": 220, "color": "#ff4444", "label": "Kid B: OFF"},
            {"type": "box", "text": "Device A\n✓ Online", "x": 200, "y": 220, "width": 180, "height": 90,
             "fill": "#1a3a2a", "stroke": "#00bfa5", "text_color": "#00bfa5"},
            {"type": "box", "text": "Device B\n✗ Blocked", "x": 520, "y": 220, "width": 180, "height": 90,
             "fill": "#4a1a1a", "stroke": "#ff4444", "text_color": "#ff4444"},
        ],
        "canvas_width": 780, "canvas_height": 380, "background": "#1a1a2e",
    },
    # Scene 7: The LLM Feast — Model Comparison
    {
        "id": "SVG7.1",
        "name": "svg_07_llm_model_comparison",
        "priority": "HIGH",
        "scene": "Scene 7: The LLM Feast",
        "diagram_type": "comparison",
        "elements": [
            {"type": "box", "text": "Claude\nReasoning\nSonnet 3.5-4.6", "x": 50, "y": 80, "width": 180, "height": 110,
             "fill": "#2e2e4e", "stroke": "#ff6b35", "text_color": "#ff6b35"},
            {"type": "box", "text": "ChatGPT\nVersatile\nSearch Engine", "x": 260, "y": 80, "width": 180, "height": 110,
             "fill": "#2e2e4e", "stroke": "#00bfa5", "text_color": "#00bfa5"},
            {"type": "box", "text": "DeepSeek\nCoding\nFree Alt", "x": 470, "y": 80, "width": 180, "height": 110,
             "fill": "#2e2e4e", "stroke": "#00d4ff", "text_color": "#00d4ff"},
            {"type": "box", "text": "Gemini\nMulti-modal\nFree Tier", "x": 680, "y": 80, "width": 180, "height": 110,
             "fill": "#2e2e4e", "stroke": "#7b2cbf", "text_color": "#7b2cbf"},
            # Connecting to central choice
            {"type": "arrow", "x1": 140, "y1": 190, "x2": 400, "y2": 270, "color": "#ff6b35"},
            {"type": "arrow", "x1": 350, "y1": 190, "x2": 430, "y2": 270, "color": "#00bfa5"},
            {"type": "arrow", "x1": 560, "y1": 190, "x2": 470, "y2": 270, "color": "#00d4ff"},
            {"type": "arrow", "x1": 770, "y1": 190, "x2": 500, "y2": 270, "color": "#7b2cbf"},
            {"type": "box", "text": "Choose\nYour Model", "x": 350, "y": 270, "width": 200, "height": 80,
             "fill": "#2e2e4e", "stroke": "#FFD700", "text_color": "#FFD700"},
        ],
        "canvas_width": 920, "canvas_height": 420, "background": "#1a1a2e",
    },
    # Scene 8: Bespoke Logic — n8n Automation
    {
        "id": "SVG8.1",
        "name": "svg_08_n8n_automation_pipeline",
        "priority": "HIGH",
        "scene": "Scene 8: Bespoke Logic",
        "diagram_type": "flow",
        "elements": [
            {"type": "box", "text": "Telegram\nTrigger", "x": 30, "y": 160, "width": 160, "height": 90,
             "fill": "#2e2e4e", "stroke": "#00d4ff", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 210, "y1": 205, "x2": 270, "y2": 205, "color": "#00d4ff"},
            {"type": "box", "text": "n8n\nLogic", "x": 290, "y": 160, "width": 140, "height": 90,
             "fill": "#2e2e4e", "stroke": "#ff6b35", "text_color": "#ff6b35"},
            {"type": "arrow", "x1": 450, "y1": 205, "x2": 510, "y2": 205, "color": "#ff6b35"},
            {"type": "box", "text": "MAC\nFilter", "x": 530, "y": 160, "width": 140, "height": 90,
             "fill": "#2e2e4e", "stroke": "#7b2cbf", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 690, "y1": 205, "x2": 750, "y2": 205, "color": "#7b2cbf"},
            {"type": "box", "text": "GitHub\nPages UI", "x": 770, "y": 160, "width": 160, "height": 90,
             "fill": "#2e2e4e", "stroke": "#00bfa5", "text_color": "#00bfa5"},
        ],
        "canvas_width": 1000, "canvas_height": 420, "background": "#1a1a2e",
    },
    # Scene 9: Success Metrics — CI/CD Pipeline
    {
        "id": "SVG9.1",
        "name": "svg_09_cicd_success_metrics",
        "priority": "HIGH",
        "scene": "Scene 9: Success Metrics",
        "diagram_type": "flow",
        "elements": [
            {"type": "box", "text": "Commit\n(37+)", "x": 30, "y": 80, "width": 150, "height": 80,
             "fill": "#2e2e4e", "stroke": "#00d4ff", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 200, "y1": 120, "x2": 260, "y2": 120, "color": "#00d4ff"},
            {"type": "box", "text": "GitHub\nActions", "x": 280, "y": 80, "width": 150, "height": 80,
             "fill": "#2e2e4e", "stroke": "#00bfa5", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 450, "y1": 120, "x2": 510, "y2": 120, "color": "#00bfa5"},
            {"type": "box", "text": "CI/CD\nDeploy", "x": 530, "y": 80, "width": 150, "height": 80,
             "fill": "#2e2e4e", "stroke": "#7b2cbf", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 700, "y1": 120, "x2": 760, "y2": 120, "color": "#7b2cbf"},
            {"type": "box", "text": "Live\nSite", "x": 780, "y": 80, "width": 150, "height": 80,
             "fill": "#1a3a2a", "stroke": "#00bfa5", "text_color": "#00bfa5"},
            # Metrics row
            {"type": "box", "text": "Compliance", "x": 130, "y": 250, "width": 180, "height": 70,
             "fill": "#2e2e4e", "stroke": "#00bfa5", "text_color": "#00bfa5"},
            {"type": "box", "text": "Accuracy", "x": 380, "y": 250, "width": 180, "height": 70,
             "fill": "#2e2e4e", "stroke": "#00d4ff", "text_color": "#00d4ff"},
            {"type": "box", "text": "Self-Growth", "x": 630, "y": 250, "width": 180, "height": 70,
             "fill": "#2e2e4e", "stroke": "#FFD700", "text_color": "#FFD700"},
        ],
        "canvas_width": 1000, "canvas_height": 380, "background": "#1a1a2e",
    },
    # Scene 10: Conclusion — Journey Roadmap
    {
        "id": "SVG10.1",
        "name": "svg_10_delivery_pilot_roadmap",
        "priority": "HIGH",
        "scene": "Scene 10: Conclusion",
        "diagram_type": "flow",
        "elements": [
            {"type": "box", "text": "1. Take\nAssessment", "x": 50, "y": 280, "width": 180, "height": 90,
             "fill": "#2e2e4e", "stroke": "#00d4ff", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 230, "y1": 300, "x2": 280, "y2": 250, "color": "#FFD700"},
            {"type": "box", "text": "2. Watch\nSimulation", "x": 280, "y": 190, "width": 180, "height": 90,
             "fill": "#2e2e4e", "stroke": "#00bfa5", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 460, "y1": 210, "x2": 510, "y2": 160, "color": "#FFD700"},
            {"type": "box", "text": "3. Clone\nRepo", "x": 510, "y": 100, "width": 180, "height": 90,
             "fill": "#2e2e4e", "stroke": "#7b2cbf", "text_color": "#ffffff"},
            {"type": "arrow", "x1": 690, "y1": 120, "x2": 740, "y2": 70, "color": "#FFD700"},
            {"type": "box", "text": "4. Build\nYour Future", "x": 740, "y": 20, "width": 180, "height": 90,
             "fill": "#2e2e4e", "stroke": "#FFD700", "text_color": "#FFD700"},
        ],
        "canvas_width": 1000, "canvas_height": 420, "background": "#1a1a2e",
    },
]


def create_svg_element(width: int, height: int, background: str) -> Element:
    """Create the root SVG element"""
    svg = Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": str(width),
            "height": str(height),
            "viewBox": f"0 0 {width} {height}",
        },
    )
    
    # Add background rectangle
    background_rect = SubElement(
        svg,
        "rect",
        {
            "width": str(width),
            "height": str(height),
            "fill": background,
        },
    )
    
    return svg


def add_box(
    svg: Element,
    text: str,
    x: int,
    y: int,
    width: int,
    height: int,
    fill: str,
    stroke: str,
    text_color: str,
) -> None:
    """Add a box with text to the SVG"""
    # Add rectangle
    rect = SubElement(
        svg,
        "rect",
        {
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(height),
            "fill": fill,
            "stroke": stroke,
            "stroke-width": "3",
            "rx": "10",
            "ry": "10",
        },
    )
    
    # Split text by newlines for multi-line support
    lines = text.split("\n")
    
    # Calculate starting y position to center text vertically
    # We add line_height/2 to account for the dominant-baseline="middle" attribute
    total_text_height = len(lines) * TEXT_LINE_HEIGHT
    text_start_y = y + (height - total_text_height) / 2 + TEXT_LINE_HEIGHT / 2
    
    # Add text lines
    for i, line in enumerate(lines):
        text_elem = SubElement(
            svg,
            "text",
            {
                "x": str(x + width / 2),
                "y": str(text_start_y + i * TEXT_LINE_HEIGHT),
                "fill": text_color,
                "font-family": "Arial, sans-serif",
                "font-size": "18",
                "font-weight": "bold",
                "text-anchor": "middle",
                "dominant-baseline": "middle",
            },
        )
        text_elem.text = line.strip()


def add_arrow(
    svg: Element,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color: str,
    label: str = None,
) -> None:
    """Add an arrow to the SVG"""
    # Define arrowhead marker
    defs = svg.find("defs")
    if defs is None:
        defs = SubElement(svg, "defs")
    
    marker_id = f"arrowhead_{color.replace('#', '')}"
    
    # Check if marker already exists
    if svg.find(f".//marker[@id='{marker_id}']") is None:
        marker = SubElement(
            defs,
            "marker",
            {
                "id": marker_id,
                "markerWidth": "10",
                "markerHeight": "10",
                "refX": "9",
                "refY": "3",
                "orient": "auto",
                "markerUnits": "strokeWidth",
            },
        )
        path = SubElement(
            marker,
            "path",
            {
                "d": "M0,0 L0,6 L9,3 z",
                "fill": color,
            },
        )
    
    # Add line
    line = SubElement(
        svg,
        "line",
        {
            "x1": str(x1),
            "y1": str(y1),
            "x2": str(x2),
            "y2": str(y2),
            "stroke": color,
            "stroke-width": "3",
            "marker-end": f"url(#{marker_id})",
        },
    )
    
    # Add label if provided
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 - LABEL_OFFSET
        text_elem = SubElement(
            svg,
            "text",
            {
                "x": str(mid_x),
                "y": str(mid_y),
                "fill": color,
                "font-family": "Arial, sans-serif",
                "font-size": "14",
                "font-style": "italic",
                "text-anchor": "middle",
            },
        )
        text_elem.text = label


def generate_svg(config: Dict, output_dir: Path, manifest: Optional[object] = None, version: int = 1) -> Dict:
    """Generate an SVG diagram based on configuration"""
    print(f"\n{'='*SEPARATOR_WIDTH}")
    print(f"🎨 Generating SVG: {config['name']}")
    print(f"   Scene: {config['scene']}")
    print(f"   Priority: {config['priority']}")
    print(f"   Type: {config['diagram_type']}")
    print(f"{'='*SEPARATOR_WIDTH}")
    
    try:
        # Create SVG root element
        svg = create_svg_element(
            config["canvas_width"],
            config["canvas_height"],
            config["background"],
        )
        
        # Add elements
        for element in config["elements"]:
            if element["type"] == "box":
                add_box(
                    svg,
                    element["text"],
                    element["x"],
                    element["y"],
                    element["width"],
                    element["height"],
                    element["fill"],
                    element["stroke"],
                    element["text_color"],
                )
            elif element["type"] == "arrow":
                add_arrow(
                    svg,
                    element["x1"],
                    element["y1"],
                    element["x2"],
                    element["y2"],
                    element["color"],
                    element.get("label"),
                )
        
        # Convert to pretty XML string
        rough_string = tostring(svg, encoding="unicode")
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # Remove extra blank lines
        pretty_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip()])
        
        # Generate filename using new convention if available
        if generate_filename and extract_scene_number:
            # Extract scene number from SVG ID (e.g., "SVG1.1" -> 1)
            svg_id = config.get('id', '0.0')
            # Remove "SVG" prefix if present
            numeric_id = svg_id.replace('SVG', '') if svg_id.startswith('SVG') else svg_id
            scene_num = extract_scene_number(numeric_id)
            
            base_filename = generate_filename(
                scene_num,
                'svg',
                config['name'],
                version
            )
            filename_json = base_filename + '.json'
            filename_svg = base_filename + '.svg'
        else:
            # Fallback to legacy naming
            filename_json = f"{config['name']}.json"
            filename_svg = f"{config['name']}.svg"
        
        # Save SVG file
        svg_path = output_dir / filename_svg
        with open(svg_path, "w") as f:
            f.write(pretty_xml)
        
        print(f"✅ SVG generated successfully!")
        print(f"💾 Saved to: {svg_path}")
        
        # Also save JPEG version
        if convert_svg_to_jpeg:
            jpeg_path = convert_svg_to_jpeg(svg_path)
            if jpeg_path:
                print(f"📸 JPEG version saved: {jpeg_path.name}")
        
        # Create prompt description for manifest
        prompt_description = f"{config.get('scene', 'Scene')}: {config['diagram_type']} diagram showing {config['name']}"
        
        # Save metadata
        metadata_path = output_dir / filename_json
        metadata = {
            **config,
            "output_file": str(svg_path),
            "filename": filename_svg,
        }
        
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"💾 Metadata saved: {metadata_path}")
        
        # Add to manifest if provided
        if manifest:
            manifest.add_asset(
                filename=filename_svg,
                prompt=prompt_description,
                asset_type="svg",
                asset_id=config.get("id", "unknown"),
                local_path=str(svg_path),
                metadata={
                    "scene": config.get("scene", ""),
                    "priority": config.get("priority", ""),
                    "diagram_type": config.get("diagram_type", ""),
                    "canvas_width": config.get("canvas_width", 0),
                    "canvas_height": config.get("canvas_height", 0),
                }
            )
        
        return {
            "success": True,
            "svg_path": str(svg_path),
            "metadata_path": str(metadata_path),
        }
        
    except Exception as e:
        print(f"❌ Error generating SVG: {str(e)}")
        return {"success": False, "error": str(e)}


def process_queue(queue: List[Dict], output_dir: Path, version: int = 1) -> List[Dict]:
    """Process a queue of SVG diagrams to generate"""
    print(f"\n{'='*SEPARATOR_WIDTH}")
    print("🚀 SVG BATCH ASSET GENERATOR")
    print("   Project: The Agentic Era - Managing 240+ Workflows")
    print("="*SEPARATOR_WIDTH)
    
    print(f"\n📁 Output directory: {output_dir.absolute()}")
    print(f"\n📊 SVGs to generate: {len(queue)}")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize manifest tracker if available
    manifest = None
    if ManifestTracker:
        manifest = ManifestTracker(output_dir)
        print(f"✅ Manifest tracking enabled")
    
    # Count by priority
    high_priority = [a for a in queue if a["priority"] == "HIGH"]
    medium_priority = [a for a in queue if a["priority"] == "MEDIUM"]
    low_priority = [a for a in queue if a["priority"] == "LOW"]
    
    print(f"   • HIGH priority: {len(high_priority)}")
    print(f"   • MEDIUM priority: {len(medium_priority)}")
    print(f"   • LOW priority: {len(low_priority)}")
    
    # Generate SVGs
    results = []
    for i, config in enumerate(queue, 1):
        print(f"\n\n{'#'*SEPARATOR_WIDTH}")
        print(f"# SVG {i}/{len(queue)}")
        print(f"{'#'*SEPARATOR_WIDTH}")
        
        result = generate_svg(config, output_dir, manifest, version)
        results.append({
            "svg_id": config["id"],
            "name": config["name"],
            "priority": config["priority"],
            **result,
        })
    
    # Summary
    print("\n\n" + "="*SEPARATOR_WIDTH)
    print("📊 GENERATION SUMMARY")
    print("="*SEPARATOR_WIDTH)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\n✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    if successful:
        print("\n✅ SUCCESSFUL GENERATIONS:")
        for r in successful:
            print(f"   • {r['svg_id']}: {r['name']} ({r['priority']})")
    
    if failed:
        print("\n❌ FAILED GENERATIONS:")
        for r in failed:
            print(f"   • {r['svg_id']}: {r['name']} - {r.get('error', 'Unknown error')}")
    
    # Save summary
    summary_path = output_dir / "generation_summary.json"
    with open(summary_path, "w") as f:
        json.dump(
            {
                "total": len(results),
                "successful": len(successful),
                "failed": len(failed),
                "results": results,
            },
            f,
            indent=2,
        )
    
    print(f"\n💾 Summary saved: {summary_path}")
    
    # Save manifest if tracker was initialized
    if manifest:
        manifest.save_manifest()
    
    print("\n✅ Done!")
    
    return results


def main():
    """Main execution — no interactive prompt."""
    print("\n" + "="*SEPARATOR_WIDTH)
    print("📐 SVG Batch Asset Generator")
    print("   Project: The Delivery Pilot Transformation")
    print("   Cost: $0.00 (local generation, no API calls)")
    print("="*SEPARATOR_WIDTH)
    
    process_queue(GENERATION_QUEUE, OUTPUT_DIR)


if __name__ == "__main__":
    main()

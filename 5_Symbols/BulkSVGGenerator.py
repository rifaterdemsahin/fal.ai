#!/usr/bin/env python3
"""
Bulk SVG Generator
Project: Weekly Video Creation Pipeline
Generates SVG diagrams for documentation, workflows, and visual explanations
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Import asset utilities for naming and manifest tracking
try:
    from asset_utils import generate_filename, extract_scene_number, ManifestTracker
except ImportError:
    print("⚠️  asset_utils not found. Using legacy naming convention.")
    generate_filename = None
    extract_scene_number = None
    ManifestTracker = None

# Configuration
# Default to weekly folder for GitHub Actions workflow
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent / "3_Simulation" / "Feb1Youtube" / "weekly" / "generated_svgs"
OUTPUT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT_DIR
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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

# SVG Generation Queue
GENERATION_QUEUE = [
    {
        "id": "1.1",
        "scene": "Pipeline Overview",
        "priority": "HIGH",
        "name": "pipeline_overview",
        "diagram_type": "flow",
        "elements": [
            {
                "type": "box",
                "text": "Script Input",
                "x": 100,
                "y": 200,
                "width": 180,
                "height": 80,
                "fill": "#2e2e4e",
                "stroke": "#00d4ff",
                "text_color": "#ffffff",
            },
            {
                "type": "arrow",
                "x1": 290,
                "y1": 240,
                "x2": 370,
                "y2": 240,
                "color": "#00d4ff",
                "label": "Process",
            },
            {
                "type": "box",
                "text": "Asset Gen",
                "x": 390,
                "y": 200,
                "width": 180,
                "height": 80,
                "fill": "#2e2e4e",
                "stroke": "#7b2cbf",
                "text_color": "#ffffff",
            },
            {
                "type": "arrow",
                "x1": 580,
                "y1": 240,
                "x2": 660,
                "y2": 240,
                "color": "#7b2cbf",
            },
            {
                "type": "box",
                "text": "Video Output",
                "x": 680,
                "y": 200,
                "width": 180,
                "height": 80,
                "fill": "#2e2e4e",
                "stroke": "#00bfa5",
                "text_color": "#ffffff",
            },
        ],
        "canvas_width": 960,
        "canvas_height": 480,
        "background": "#1a1a2e",
    },
    {
        "id": "2.1",
        "scene": "Agentic Era Evolution",
        "priority": "HIGH",
        "name": "agentic_era_transition",
        "diagram_type": "flow",
        "elements": [
            {
                "type": "box",
                "text": "Prompts",
                "x": 100,
                "y": 200,
                "width": 200,
                "height": 100,
                "fill": "#2e2e4e",
                "stroke": "#00d4ff",
                "text_color": "#ffffff",
            },
            {
                "type": "arrow",
                "x1": 320,
                "y1": 250,
                "x2": 480,
                "y2": 250,
                "color": "#00d4ff",
                "label": "Evolution",
            },
            {
                "type": "box",
                "text": "Agents",
                "x": 500,
                "y": 200,
                "width": 200,
                "height": 100,
                "fill": "#7b2cbf",
                "stroke": "#00d4ff",
                "text_color": "#ffffff",
            },
        ],
        "canvas_width": 800,
        "canvas_height": 450,
        "background": "#1a1a2e",
    },
    {
        "id": "3.1",
        "scene": "Workflow Process",
        "priority": "MEDIUM",
        "name": "workflow_process_flow",
        "diagram_type": "flow",
        "elements": [
            {
                "type": "box",
                "text": "Input",
                "x": 50,
                "y": 175,
                "width": 150,
                "height": 80,
                "fill": "#2e2e4e",
                "stroke": "#00bfa5",
                "text_color": "#ffffff",
            },
            {
                "type": "arrow",
                "x1": 220,
                "y1": 215,
                "x2": 280,
                "y2": 215,
                "color": "#00bfa5",
            },
            {
                "type": "box",
                "text": "Process",
                "x": 300,
                "y": 175,
                "width": 150,
                "height": 80,
                "fill": "#2e2e4e",
                "stroke": "#00d4ff",
                "text_color": "#ffffff",
            },
            {
                "type": "arrow",
                "x1": 470,
                "y1": 215,
                "x2": 530,
                "y2": 215,
                "color": "#00d4ff",
            },
            {
                "type": "box",
                "text": "Output",
                "x": 550,
                "y": 175,
                "width": 150,
                "height": 80,
                "fill": "#2e2e4e",
                "stroke": "#7b2cbf",
                "text_color": "#ffffff",
            },
        ],
        "canvas_width": 750,
        "canvas_height": 430,
        "background": "#1a1a2e",
    },
    {
        "id": "4.1",
        "scene": "AI Agent Process",
        "priority": "MEDIUM",
        "name": "data_collection_understanding_notification",
        "diagram_type": "flow",
        "elements": [
            {
                "type": "box",
                "text": "Data\nCollection",
                "x": 50,
                "y": 150,
                "width": 180,
                "height": 100,
                "fill": "#2e2e4e",
                "stroke": "#00bfa5",
                "text_color": "#ffffff",
            },
            {
                "type": "arrow",
                "x1": 250,
                "y1": 200,
                "x2": 320,
                "y2": 200,
                "color": "#00bfa5",
            },
            {
                "type": "box",
                "text": "Understanding",
                "x": 340,
                "y": 150,
                "width": 180,
                "height": 100,
                "fill": "#2e2e4e",
                "stroke": "#00d4ff",
                "text_color": "#ffffff",
            },
            {
                "type": "arrow",
                "x1": 540,
                "y1": 200,
                "x2": 610,
                "y2": 200,
                "color": "#00d4ff",
            },
            {
                "type": "box",
                "text": "Notification",
                "x": 630,
                "y": 150,
                "width": 180,
                "height": 100,
                "fill": "#2e2e4e",
                "stroke": "#7b2cbf",
                "text_color": "#ffffff",
            },
        ],
        "canvas_width": 860,
        "canvas_height": 400,
        "background": "#1a1a2e",
    },
    {
        "id": "5.1",
        "scene": "Traditional vs Agentic Comparison",
        "priority": "LOW",
        "name": "traditional_vs_agentic",
        "diagram_type": "comparison",
        "elements": [
            # Traditional side
            {
                "type": "box",
                "text": "Traditional\nWorkflow",
                "x": 100,
                "y": 100,
                "width": 200,
                "height": 100,
                "fill": "#3a3a3a",
                "stroke": "#6b6b6b",
                "text_color": "#cccccc",
            },
            {
                "type": "arrow",
                "x1": 200,
                "y1": 220,
                "x2": 200,
                "y2": 280,
                "color": "#6b6b6b",
            },
            {
                "type": "box",
                "text": "Manual\nProcessing",
                "x": 100,
                "y": 300,
                "width": 200,
                "height": 100,
                "fill": "#3a3a3a",
                "stroke": "#6b6b6b",
                "text_color": "#cccccc",
            },
            # Agentic side
            {
                "type": "box",
                "text": "Agentic\nWorkflow",
                "x": 500,
                "y": 100,
                "width": 200,
                "height": 100,
                "fill": "#2e2e4e",
                "stroke": "#00d4ff",
                "text_color": "#ffffff",
            },
            {
                "type": "arrow",
                "x1": 600,
                "y1": 220,
                "x2": 600,
                "y2": 280,
                "color": "#00d4ff",
            },
            {
                "type": "box",
                "text": "Automated\nIntelligence",
                "x": 500,
                "y": 300,
                "width": 200,
                "height": 100,
                "fill": "#2e2e4e",
                "stroke": "#7b2cbf",
                "text_color": "#ffffff",
            },
        ],
        "canvas_width": 800,
        "canvas_height": 500,
        "background": "#1a1a2e",
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


def generate_svg(config: Dict, metadata: Optional[Dict] = None) -> Dict:
    """
    Generate an SVG diagram based on configuration
    
    Args:
        config: SVG configuration with elements and properties
        metadata: Additional metadata for tracking
    
    Returns:
        Dictionary with SVG text and metadata
    """
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
        
        result = {
            "svg_text": pretty_xml,
            "type": config["diagram_type"],
            "name": config["name"],
            "success": True,
            "timestamp": datetime.now().isoformat()
        }
        
        if metadata:
            result["metadata"] = metadata
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "name": config.get("name", "unknown")
        }


def save_svg_to_file(svg_result: Dict, asset_id: str, filename: str) -> str:
    """Save SVG to file"""
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_result['svg_text'])
    
    return str(filepath)


def main():
    """Main execution function"""
    print("🎨 Bulk SVG Generator")
    print("=" * 60)
    print(f"Output Directory: {OUTPUT_DIR.absolute()}")
    print(f"Total SVGs to Generate: {len(GENERATION_QUEUE)}")
    print("=" * 60)
    
    # Initialize manifest tracker if available
    manifest = ManifestTracker(OUTPUT_DIR) if ManifestTracker else None
    
    successful = 0
    failed = 0
    results = []
    
    for item in GENERATION_QUEUE:
        asset_id = item["id"]
        scene = item["scene"]
        priority = item["priority"]
        name = item["name"]
        
        print(f"\n🎨 Generating: {scene} (ID: {asset_id}, Priority: {priority})")
        
        # Generate the SVG
        result = generate_svg(
            config=item,
            metadata={
                "scene": scene,
                "priority": priority,
                "asset_id": asset_id
            }
        )
        
        if result["success"]:
            # Generate filename using asset_utils if available
            if generate_filename:
                scene_number = extract_scene_number(asset_id) if extract_scene_number else 1
                filename = generate_filename(
                    scene_number=scene_number,
                    asset_type="svg",
                    description=name,
                    version=1,
                    extension="svg"
                )
            else:
                # Fallback naming
                filename = f"svg_{asset_id.replace('.', '_')}_{name}.svg"
            
            # Save to file
            filepath = save_svg_to_file(result, asset_id, filename)
            
            print(f"✅ Success: {filename}")
            successful += 1
            
            # Track in manifest
            if manifest:
                manifest.add_asset(
                    filename=filename,
                    prompt=f"SVG {item['diagram_type']} diagram for {scene}",
                    asset_type="svg",
                    asset_id=asset_id,
                    result_url=f"file://{filepath}",
                    local_path=filepath,
                    metadata={
                        "scene": scene,
                        "priority": priority,
                        "diagram_type": item["diagram_type"],
                        "name": name,
                        "canvas_width": item["canvas_width"],
                        "canvas_height": item["canvas_height"]
                    }
                )
            
            results.append({
                "asset_id": asset_id,
                "filename": filename,
                "filepath": filepath,
                "status": "success"
            })
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
            failed += 1
            results.append({
                "asset_id": asset_id,
                "status": "failed",
                "error": result.get("error")
            })
    
    # Save manifest
    if manifest:
        manifest.save_manifest("manifest.json")
        manifest_path = OUTPUT_DIR / "manifest.json"
        print(f"\n📝 Manifest saved: {manifest_path}")
    
    # Save summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total": len(GENERATION_QUEUE),
        "successful": successful,
        "failed": failed,
        "output_directory": str(OUTPUT_DIR.absolute()),
        "results": results
    }
    
    summary_path = OUTPUT_DIR / "generation_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 GENERATION SUMMARY")
    print("=" * 60)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Output Directory: {OUTPUT_DIR.absolute()}")
    print(f"📝 Summary saved: {summary_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()

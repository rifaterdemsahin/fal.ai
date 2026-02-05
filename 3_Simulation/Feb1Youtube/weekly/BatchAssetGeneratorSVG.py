#!/usr/bin/env python3
"""
SVG Batch Asset Generator
Project: The Agentic Era - Managing 240+ Workflows
Generates SVG diagrams to showcase processes in video scripts
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Configuration
OUTPUT_DIR = Path("./generated_svgs")
OUTPUT_DIR.mkdir(exist_ok=True)

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
        "id": "SVG1.1",
        "name": "agentic_era_transition",
        "priority": "HIGH",
        "scene": "Agentic Era Explanation",
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
        "id": "SVG2.1",
        "name": "workflow_process",
        "priority": "HIGH",
        "scene": "Workflow Process Flow",
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
        "id": "SVG3.1",
        "name": "data_collection_understanding_notification",
        "priority": "MEDIUM",
        "scene": "AI Agent Process",
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
        "id": "SVG4.1",
        "name": "traditional_vs_agentic",
        "priority": "MEDIUM",
        "scene": "Comparison: Traditional vs Agentic",
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
    line_height = 25
    
    # Calculate starting y position to center text vertically
    total_text_height = len(lines) * line_height
    text_start_y = y + (height - total_text_height) / 2 + line_height / 2
    
    # Add text lines
    for i, line in enumerate(lines):
        text_elem = SubElement(
            svg,
            "text",
            {
                "x": str(x + width / 2),
                "y": str(text_start_y + i * line_height),
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
        mid_y = (y1 + y2) / 2 - 15
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


def generate_svg(config: Dict, output_dir: Path) -> Dict:
    """Generate an SVG diagram based on configuration"""
    print(f"\n{'='*60}")
    print(f"🎨 Generating SVG: {config['name']}")
    print(f"   Scene: {config['scene']}")
    print(f"   Priority: {config['priority']}")
    print(f"   Type: {config['diagram_type']}")
    print(f"{'='*60}")
    
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
        
        # Save SVG file
        svg_path = output_dir / f"{config['name']}.svg"
        with open(svg_path, "w") as f:
            f.write(pretty_xml)
        
        print(f"✅ SVG generated successfully!")
        print(f"💾 Saved to: {svg_path}")
        
        # Save metadata
        metadata_path = output_dir / f"{config['name']}.json"
        metadata = {
            **config,
            "output_file": str(svg_path),
        }
        
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"💾 Metadata saved: {metadata_path}")
        
        return {
            "success": True,
            "svg_path": str(svg_path),
            "metadata_path": str(metadata_path),
        }
        
    except Exception as e:
        print(f"❌ Error generating SVG: {str(e)}")
        return {"success": False, "error": str(e)}


def process_queue(queue: List[Dict], output_dir: Path) -> List[Dict]:
    """Process a queue of SVG diagrams to generate"""
    print(f"\n{'='*60}")
    print("🚀 SVG BATCH ASSET GENERATOR")
    print("   Project: The Agentic Era - Managing 240+ Workflows")
    print("="*60)
    
    print(f"\n📁 Output directory: {output_dir.absolute()}")
    print(f"\n📊 SVGs to generate: {len(queue)}")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
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
        print(f"\n\n{'#'*60}")
        print(f"# SVG {i}/{len(queue)}")
        print(f"{'#'*60}")
        
        result = generate_svg(config, output_dir)
        results.append({
            "svg_id": config["id"],
            "name": config["name"],
            "priority": config["priority"],
            **result,
        })
    
    # Summary
    print("\n\n" + "="*60)
    print("📊 GENERATION SUMMARY")
    print("="*60)
    
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
    print("\n✅ Done!")
    
    return results


def main():
    """Main execution"""
    print("\n" + "="*60)
    print("SVG Batch Asset Generator")
    print("Generates process flow diagrams for video scripts")
    print("="*60)
    
    response = input("\n🤔 Proceed with SVG generation? (yes/no): ").strip().lower()
    if response not in ["yes", "y"]:
        print("❌ Cancelled by user")
        return
    
    process_queue(GENERATION_QUEUE, OUTPUT_DIR)


if __name__ == "__main__":
    main()

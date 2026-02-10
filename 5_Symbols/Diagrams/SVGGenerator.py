#!/usr/bin/env python3
"""
SVG Asset Generator
Generates SVG diagram assets with base class architecture
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Add parent directory to path to allow imports from base and Utils
sys.path.append(str(Path(__file__).resolve().parent.parent))

from Base.base_asset_generator import BaseAssetGenerator
from Base.generator_config import SEEDS, BRAND_COLORS
from Utils.asset_utils import generate_filename, extract_scene_number, convert_svg_to_jpeg


# Display constants
SEPARATOR_WIDTH = 60
TEXT_LINE_HEIGHT = 25
LABEL_OFFSET = 15


class SVGAssetGenerator(BaseAssetGenerator):
    """Generator for SVG diagram assets"""
    
    def __init__(self):
        super().__init__(
            output_dir=Path("./generated_svg"),
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="svg"
        )
    
    def create_svg_element(self, width: int, height: int, background: str) -> Element:
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
        self,
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
        
        lines = text.split("\n")
        total_text_height = len(lines) * TEXT_LINE_HEIGHT
        text_start_y = y + (height - total_text_height) / 2 + TEXT_LINE_HEIGHT / 2
        
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
        self,
        svg: Element,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: str,
        label: str = None,
    ) -> None:
        """Add an arrow to the SVG"""
        defs = svg.find("defs")
        if defs is None:
            defs = SubElement(svg, "defs")
        
        marker_id = f"arrowhead_{color.replace('#', '')}"
        
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
    
    def generate_asset(
        self,
        asset_config: Dict,
        version: int = 1
    ) -> Dict:
        """Generate a single SVG diagram"""
        print(f"\n{'='*60}")
        print(f"ðŸŽ¨ Generating {self.asset_type}: {asset_config['name']}")
        print(f"   Scene: {asset_config.get('scene', 'Unknown')}")
        print(f"   Priority: {asset_config.get('priority', 'MEDIUM')}")
        print(f"   Type: {asset_config.get('diagram_type', 'flow')}")
        print(f"{'='*60}")
        
        try:
            svg = self.create_svg_element(
                asset_config["canvas_width"],
                asset_config["canvas_height"],
                asset_config["background"],
            )
            
            for element in asset_config["elements"]:
                if element["type"] == "box":
                    self.add_box(
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
                    self.add_arrow(
                        svg,
                        element["x1"],
                        element["y1"],
                        element["x2"],
                        element["y2"],
                        element["color"],
                        element.get("label"),
                    )
            
            rough_string = tostring(svg, encoding="unicode")
            reparsed = minidom.parseString(rough_string)
            pretty_xml = reparsed.toprettyxml(indent="  ")
            # Remove extra blank lines while keeping the pretty formatting structure
            pretty_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip() or line == ""])
            
            svg_id = asset_config.get('id', '0.0')
            numeric_id = svg_id.replace('SVG', '') if svg_id.startswith('SVG') else svg_id
            scene_num = extract_scene_number(numeric_id)
            
            base_filename = generate_filename(
                scene_num,
                self.asset_type,
                asset_config['name'],
                version
            )
            filename_json = base_filename + '.json'
            filename_svg = base_filename + '.svg'
            
            svg_path = self.output_dir / filename_svg
            with open(svg_path, "w") as f:
                f.write(pretty_xml)
            
            print(f"âœ… Generated successfully!")
            print(f"ðŸ’¾ Saved to: {svg_path}")
            
            # Also save JPEG version
            jpeg_path = convert_svg_to_jpeg(svg_path)
            if jpeg_path:
                print(f"ðŸ“¸ JPEG version saved: {jpeg_path.name}")
            
            prompt_description = f"{asset_config.get('scene', 'Scene')}: {asset_config.get('diagram_type', 'flow')} diagram showing {asset_config['name']}"
            
            metadata_path = self.output_dir / filename_json
            metadata = {
                **asset_config,
                "output_file": str(svg_path),
                "filename": filename_svg,
                "prompt": prompt_description,
            }
            
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            
            print(f"ðŸ’¾ Metadata saved: {metadata_path}")
            
            if self.manifest:
                self.manifest.add_asset(
                    filename=filename_svg,
                    prompt=prompt_description,
                    asset_type=self.asset_type,
                    asset_id=asset_config.get("id", "unknown"),
                    local_path=str(svg_path),
                    metadata={
                        "scene": asset_config.get("scene", ""),
                        "priority": asset_config.get("priority", ""),
                        "diagram_type": asset_config.get("diagram_type", ""),
                        "canvas_width": asset_config.get("canvas_width", 0),
                        "canvas_height": asset_config.get("canvas_height", 0),
                    }
                )
            
            return {
                "success": True,
                "local_path": str(svg_path),
            }
            
        except Exception as e:
            print(f"âŒ Error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }
    
    def get_generation_queue(self) -> List[Dict]:
        """Return the list of SVG diagrams to generate"""
        return [
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


def main():
    """Main execution"""
    generator = SVGAssetGenerator()
    generator.run()


if __name__ == "__main__":
    main()


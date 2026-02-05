#!/usr/bin/env python3
"""
Bulk Mermaid Diagram Generator
Project: Weekly Video Creation Pipeline
Generates Mermaid diagrams for documentation, workflows, and visual explanations
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Import asset utilities for naming and manifest tracking
try:
    from asset_utils import generate_filename, extract_scene_number, ManifestTracker
except ImportError:
    print("⚠️  asset_utils not found. Using legacy naming convention.")
    generate_filename = None
    extract_scene_number = None
    ManifestTracker = None

# Configuration
OUTPUT_DIR = Path("./generated_mermaid_diagrams")
OUTPUT_DIR.mkdir(exist_ok=True)

# Mermaid diagram templates
DIAGRAM_TEMPLATES = {
    "flowchart": """```mermaid
flowchart {direction}
{content}
```""",
    "sequence": """```mermaid
sequenceDiagram
{content}
```""",
    "gantt": """```mermaid
gantt
    title {title}
    dateFormat YYYY-MM-DD
{content}
```""",
    "class": """```mermaid
classDiagram
{content}
```""",
    "state": """```mermaid
stateDiagram-v2
{content}
```""",
    "er": """```mermaid
erDiagram
{content}
```""",
    "journey": """```mermaid
journey
    title {title}
{content}
```""",
    "pie": """```mermaid
pie title {title}
{content}
```"""
}

# Generation queue for diagrams
GENERATION_QUEUE = [
    {
        "id": "1.1",
        "scene": "Pipeline Overview",
        "priority": "HIGH",
        "type": "flowchart",
        "direction": "TB",
        "title": "Weekly Video Creation Pipeline",
        "content": """    A[📝 Script Input] --> B[🤖 Gemini Analysis]
    B --> C[📋 Requirements]
    C --> D[🎨 Asset Generation]
    D --> E[📊 Manifest]
    E --> F[🎞️ DaVinci Resolve]
    
    style A fill:#e1f5ff
    style F fill:#d4edda"""
    },
    {
        "id": "2.1",
        "scene": "Asset Generation Flow",
        "priority": "HIGH",
        "type": "sequence",
        "title": "Asset Generation Sequence",
        "content": """    participant User
    participant Master
    participant Generators
    participant Storage
    
    User->>Master: Run Pipeline
    Master->>Generators: Trigger Batch
    Generators->>Storage: Save Assets
    Storage->>Master: Return Paths
    Master->>User: Generate Report"""
    },
    {
        "id": "3.1",
        "scene": "Weekly Production Timeline",
        "priority": "MEDIUM",
        "type": "gantt",
        "title": "Weekly Video Production",
        "content": """    section Planning
    Script Writing           :a1, 2026-02-05, 1d
    Gemini Analysis         :a2, after a1, 1d
    
    section Generation
    Asset Generation        :a3, after a2, 2d
    Quality Check           :a4, after a3, 1d
    
    section Post-Production
    DaVinci Resolve Edit    :a5, after a4, 2d
    Final Export            :a6, after a5, 1d"""
    },
    {
        "id": "4.1",
        "scene": "Asset Type Distribution",
        "priority": "MEDIUM",
        "type": "pie",
        "title": "Asset Distribution by Type",
        "content": """    "Video Assets" : 30
    "Audio Assets" : 20
    "Images" : 25
    "Diagrams" : 15
    "Icons" : 10"""
    },
    {
        "id": "5.1",
        "scene": "Platform Support",
        "priority": "LOW",
        "type": "flowchart",
        "direction": "LR",
        "title": "Environment Support",
        "content": """    A[Pipeline] --> B[Codespaces]
    A --> C[Windows]
    A --> D[macOS]
    
    style B fill:#e1f5ff
    style C fill:#fff3cd
    style D fill:#d4edda"""
    },
    {
        "id": "6.1",
        "scene": "Generator State Machine",
        "priority": "LOW",
        "type": "state",
        "title": "Asset Generation States",
        "content": """    [*] --> Queued
    Queued --> Generating
    Generating --> Success
    Generating --> Failed
    Success --> [*]
    Failed --> Retry
    Retry --> Generating
    Retry --> [*]"""
    }
]

def generate_mermaid_diagram(
    diagram_type: str,
    content: str,
    title: str = "",
    direction: str = "TB",
    metadata: Optional[Dict] = None
) -> Dict:
    """
    Generate a Mermaid diagram
    
    Args:
        diagram_type: Type of diagram (flowchart, sequence, gantt, etc.)
        content: Diagram content
        title: Optional title for the diagram
        direction: Flow direction for flowcharts (TB, LR, etc.)
        metadata: Additional metadata for tracking
    
    Returns:
        Dictionary with diagram text and metadata
    """
    try:
        template = DIAGRAM_TEMPLATES.get(diagram_type, DIAGRAM_TEMPLATES["flowchart"])
        
        # Format the diagram
        if diagram_type == "flowchart":
            diagram_text = template.format(direction=direction, content=content)
        elif diagram_type in ["gantt", "pie", "journey"]:
            diagram_text = template.format(title=title, content=content)
        else:
            diagram_text = template.format(content=content)
        
        result = {
            "diagram_text": diagram_text,
            "type": diagram_type,
            "title": title,
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
            "type": diagram_type
        }

def save_diagram_to_file(diagram: Dict, asset_id: str, filename: str) -> str:
    """Save diagram to markdown file"""
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {diagram.get('title', 'Mermaid Diagram')}\n\n")
        f.write(f"**Type:** {diagram['type']}\n")
        f.write(f"**Generated:** {diagram['timestamp']}\n\n")
        f.write(diagram['diagram_text'])
        f.write("\n")
    
    return str(filepath)

def main():
    """Main execution function"""
    print("🗺️  Bulk Mermaid Diagram Generator")
    print("=" * 60)
    print(f"Output Directory: {OUTPUT_DIR.absolute()}")
    print(f"Total Diagrams to Generate: {len(GENERATION_QUEUE)}")
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
        diagram_type = item["type"]
        
        print(f"\n📊 Generating: {scene} (ID: {asset_id}, Priority: {priority})")
        
        # Generate the diagram
        result = generate_mermaid_diagram(
            diagram_type=diagram_type,
            content=item["content"],
            title=item.get("title", scene),
            direction=item.get("direction", "TB"),
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
                clean_desc = scene.lower().replace(" ", "_").replace("-", "_")
                filename = generate_filename(
                    scene_number=scene_number,
                    asset_type="diagram",
                    description=clean_desc,
                    version=1,
                    extension="md"
                )
            else:
                # Fallback naming
                filename = f"diagram_{asset_id.replace('.', '_')}_{scene.replace(' ', '_').lower()}.md"
            
            # Save to file
            filepath = save_diagram_to_file(result, asset_id, filename)
            
            print(f"✅ Success: {filename}")
            successful += 1
            
            # Track in manifest
            if manifest:
                manifest.add_asset(
                    filename=filename,
                    prompt=f"Mermaid {diagram_type} diagram for {scene}",
                    asset_type="diagram",
                    asset_id=asset_id,
                    result_url=f"file://{filepath}",
                    local_path=filepath,
                    metadata={
                        "scene": scene,
                        "priority": priority,
                        "diagram_type": diagram_type,
                        "title": item.get("title", scene)
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

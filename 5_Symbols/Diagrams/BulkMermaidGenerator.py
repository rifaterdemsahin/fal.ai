#!/usr/bin/env python3
"""
Bulk Mermaid Diagram Generator
Project: Weekly Video Creation Pipeline
Generates Mermaid diagrams for documentation, workflows, and visual explanations
"""

import os
import json
import subprocess
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
OUTPUT_DIR = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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

# Generation queue for diagrams — The Delivery Pilot Transformation (10 scenes)
GENERATION_QUEUE = [
    {
        "id": "MM.01",
        "scene": "Scene 1 - The Heavy Mic",
        "priority": "HIGH",
        "type": "flowchart",
        "direction": "TB",
        "title": "Enterprise AI Transformation Bottleneck",
        "content": """    A[🏢 Enterprise AI Goal] --> B{Decision Makers}
    B -->|Zombie Snails| C[🐌 10-Year Roadmap]
    B -->|Delivery Pilots| D[🚀 Rapid Iteration]
    C --> E[❌ Too Slow]
    D --> F[✅ Ship Weekly]

    style A fill:#e1f5ff
    style E fill:#f8d7da
    style F fill:#d4edda"""
    },
    {
        "id": "MM.02",
        "scene": "Scene 2 - The Pivot",
        "priority": "HIGH",
        "type": "journey",
        "title": "The Delivery Pilot Pivot",
        "content": """    section Before Pivot
      Complex 240 workflows: 2: Engineer
      Scaring people off: 1: Audience
    section After Pivot
      No-code tools: 5: Everyone
      Delivery Pilot identity: 5: Creator
      Accessible AI building: 4: Audience"""
    },
    {
        "id": "MM.03",
        "scene": "Scene 3 - Statues vs Mercury",
        "priority": "HIGH",
        "type": "flowchart",
        "direction": "LR",
        "title": "Static Rules vs Dynamic AI",
        "content": """    subgraph Old[🗿 Static Systems]
        A[Hard-Coded Rules] --> B[Rigid Logic]
        B --> C[Breaks on Change]
    end
    subgraph New[💧 Dynamic AI]
        D[AI-Driven Rules] --> E[Adaptive Logic]
        E --> F[Self-Healing]
    end
    Old -->|Transform| New

    style A fill:#f8d7da
    style C fill:#f8d7da
    style D fill:#d4edda
    style F fill:#d4edda"""
    },
    {
        "id": "MM.04",
        "scene": "Scene 4 - The Clone Lab",
        "priority": "HIGH",
        "type": "sequence",
        "title": "Git Clone to Local Powerhouse",
        "content": """    participant Dev as Developer
    participant GH as GitHub
    participant Local as Local Machine
    participant Agent as AI Agent

    Dev->>GH: Browse delivery pilot template
    Dev->>Local: git clone repo
    Local->>Agent: Start AI agent
    Agent->>Local: Execute commands
    Agent->>Local: Build tooling system
    Local->>Dev: Ready to develop"""
    },
    {
        "id": "MM.05",
        "scene": "Scene 5 - The Free Tier Journey",
        "priority": "HIGH",
        "type": "flowchart",
        "direction": "TB",
        "title": "Zero Capital AI Starter Kit",
        "content": """    A[💰 Zero Capital] --> B[VS Code - Free]
    A --> C[GitHub - Free]
    B --> D{Need AI Pair?}
    D -->|Cloud Co-pilot| E[GitHub Copilot]
    D -->|Local Agentic| F[Cursor AI]
    E --> G[🔄 Swap Between All Three]
    F --> G

    style A fill:#fff3cd
    style G fill:#d4edda"""
    },
    {
        "id": "MM.06",
        "scene": "Scene 6 - Internet Kill Switch",
        "priority": "MEDIUM",
        "type": "flowchart",
        "direction": "TB",
        "title": "Parental Internet Kill Switch Workflow",
        "content": """    A[👨‍👩‍👧‍👦 Parent] --> B[GitHub Pages UI]
    B --> C{Select Child}
    C -->|Kid A| D[MAC Address A]
    C -->|Kid B| E[MAC Address B]
    D --> F[n8n Workflow]
    E --> F
    F --> G[🔴 Drop Traffic]
    F --> H[🟢 Allow Traffic]

    style A fill:#e1f5ff
    style G fill:#f8d7da
    style H fill:#d4edda"""
    },
    {
        "id": "MM.07",
        "scene": "Scene 7 - The LLM Feast",
        "priority": "HIGH",
        "type": "pie",
        "title": "LLM Model Strengths",
        "content": """    "Claude - Reasoning" : 30
    "ChatGPT - Search" : 25
    "DeepSeek - Coding" : 20
    "Gemini - Versatile Free" : 25"""
    },
    {
        "id": "MM.08",
        "scene": "Scene 8 - Bespoke Logic n8n",
        "priority": "MEDIUM",
        "type": "sequence",
        "title": "n8n Bespoke Automation Flow",
        "content": """    participant Wife as Wife
    participant UI as GitHub Pages UI
    participant N8N as n8n Workflow
    participant Router as Home Router

    Wife->>UI: Toggle internet off for Kid
    UI->>N8N: Trigger webhook
    N8N->>N8N: Lookup MAC address
    N8N->>Router: Apply firewall rule
    Router->>N8N: Confirm block
    N8N->>UI: Status updated"""
    },
    {
        "id": "MM.09",
        "scene": "Scene 9 - Success Metrics CICD",
        "priority": "MEDIUM",
        "type": "gantt",
        "title": "CI/CD Pipeline & Success Metrics",
        "content": """    section Development
    Feature Branch           :a1, 2026-02-10, 1d
    Code Changes             :a2, after a1, 1d

    section CI/CD Pipeline
    GitHub Actions Build     :a3, after a2, 1d
    Automated Tests          :a4, after a3, 1d
    Deploy to Production     :a5, after a4, 1d

    section Metrics
    Compliance Audit         :a6, after a5, 1d
    Accuracy Check           :a7, after a6, 1d"""
    },
    {
        "id": "MM.10",
        "scene": "Scene 10 - Conclusion Call to Action",
        "priority": "HIGH",
        "type": "flowchart",
        "direction": "TB",
        "title": "Your Delivery Pilot Journey",
        "content": """    A[📝 Take Assessment] --> B[🔍 Identify Gaps]
    B --> C[🎬 Watch Simulation]
    C --> D[📂 Clone the Repo]
    D --> E[⚙️ Configure Environment]
    E --> F[🚀 Build the Future]

    style A fill:#e1f5ff
    style F fill:#d4edda"""
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

def convert_to_jpeg(md_filepath: str) -> Optional[str]:
    """
    Convert Mermaid markdown file to JPEG using mermaid-cli (via PNG intermediate)
    
    Args:
        md_filepath: Path to the markdown file
    
    Returns:
        Path to the generated JPEG file or None if conversion failed
    """
    # Maximum number of suffix attempts when mmdc adds -N to output files
    MAX_SUFFIX_ATTEMPTS = 10
    
    try:
        # Get the base path without extension
        base_path = Path(md_filepath).with_suffix('')
        png_path = f"{base_path}.png"
        jpeg_path = f"{base_path}.jpeg"
        
        # Check if mmdc (mermaid-cli) is available
        mmdc_path = Path(__file__).parent / "node_modules" / ".bin" / "mmdc"
        puppeteer_config = Path(__file__).parent / "puppeteer-config.json"
        
        # Remove existing PNG if it exists (to avoid -1 suffix)
        if Path(png_path).exists():
            Path(png_path).unlink()
        
        # Step 1: Convert to PNG using mermaid-cli
        cmd = [
            str(mmdc_path) if mmdc_path.exists() else "mmdc",
            "-i", md_filepath,
            "-o", png_path,
            "-b", "white",  # White background
            "-t", "default"  # Default theme
        ]
        
        # Add puppeteer config if it exists
        if puppeteer_config.exists():
            cmd.extend(["-p", str(puppeteer_config)])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # mmdc might add a suffix like -1.png, check for that
        actual_png_path = png_path
        if not Path(png_path).exists():
            # Look for files with -1, -2, etc. suffix
            for i in range(1, MAX_SUFFIX_ATTEMPTS + 1):
                candidate = f"{base_path}-{i}.png"
                if Path(candidate).exists():
                    actual_png_path = candidate
                    break
        
        if result.returncode != 0 or not Path(actual_png_path).exists():
            if result.stderr:
                print(f"⚠️  PNG conversion warning: {result.stderr}")
            return None
        
        # Step 2: Convert PNG to JPEG using Pillow
        try:
            from PIL import Image
            
            # Open PNG and convert to RGB (JPEG doesn't support transparency)
            img = Image.open(actual_png_path)
            
            # Handle images with alpha channel (RGBA, LA) or palette mode (P)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Palette mode needs conversion to RGBA first
                if img.mode == 'P':
                    img = img.convert('RGBA')
                
                # Create a white background and paste with alpha channel as mask
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            else:
                # Simple RGB conversion for other modes
                img = img.convert('RGB')
            
            # Save as JPEG
            img.save(jpeg_path, 'JPEG', quality=95)
            
            # Clean up the intermediate PNG file
            Path(actual_png_path).unlink()
            
            return jpeg_path
            
        except ImportError:
            print("⚠️  Pillow not installed. PNG created but JPEG conversion skipped.\n"
                  "⚠️  Install Pillow to enable JPEG export: pip install Pillow")
            # Keep the PNG file since we can't convert to JPEG
            return actual_png_path
            
    except Exception as e:
        print(f"⚠️  JPEG conversion failed: {str(e)}")
        return None

def save_diagram_to_file(diagram: Dict, asset_id: str, filename: str) -> str:
    """Save diagram to markdown file and optionally to JPEG"""
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {diagram.get('title', 'Mermaid Diagram')}\n\n")
        f.write(f"**Type:** {diagram['type']}\n")
        f.write(f"**Generated:** {diagram['timestamp']}\n\n")
        f.write(diagram['diagram_text'])
        f.write("\n")
    
    # Also generate JPEG version
    jpeg_path = convert_to_jpeg(str(filepath))
    if jpeg_path:
        print(f"   📸 JPEG: {Path(jpeg_path).name}")
    
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

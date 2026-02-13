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

# Import paths configuration
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from paths_config import get_weekly_paths, get_latest_weekly_id
    USE_PATHS_CONFIG = True
except ImportError:
    USE_PATHS_CONFIG = False
    print("⚠️  paths_config not found. Using fallback directory.")

# Configuration - will be updated in main() if paths_config is available
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

# Generation queue v2 — The Delivery Pilot Transformation (10 scenes) — EMOJI ENHANCED
GENERATION_QUEUE = [
    {
        "id": "MM.01",
        "scene": "Scene 1 - The Heavy Mic",
        "priority": "HIGH",
        "type": "flowchart",
        "direction": "TB",
        "title": "Enterprise AI Transformation Bottleneck",
        "content": """    A["\U0001F3E2 Enterprise AI Goal"] --> B{"\U0001F914 Decision Makers"}
    B -->|"\U0001F40C Zombie Snails"| C["\U0001F4C5 10-Year Roadmap"]
    B -->|"\U0001F680 Delivery Pilots"| D["\u26A1 Rapid Iteration"]
    C --> E["\u274C Too Slow - Obsolete"]
    D --> F["\u2705 Ship Weekly"]
    E --> G["\U0001F480 Project Dead"]
    F --> H["\U0001F3C6 Market Leader"]

    style A fill:#4a90d9,color:#fff
    style B fill:#f5a623,color:#fff
    style C fill:#e74c3c,color:#fff
    style D fill:#2ecc71,color:#fff
    style E fill:#c0392b,color:#fff
    style F fill:#27ae60,color:#fff
    style G fill:#7f8c8d,color:#fff
    style H fill:#f1c40f,color:#333"""
    },
    {
        "id": "MM.02",
        "scene": "Scene 2 - The Pivot",
        "priority": "HIGH",
        "type": "journey",
        "title": "\U0001F504 The Delivery Pilot Pivot Journey",
        "content": """    section \U0001F6AB Before Pivot
      \U0001F62B Complex 240 workflows: 2: Engineer
      \U0001F631 Scaring people off: 1: Audience
      \U0001F4C9 Low engagement: 1: Creator
    section \u2705 After Pivot
      \U0001F6E0 No-code tools: 5: Everyone
      \U0001F3AF Delivery Pilot identity: 5: Creator
      \U0001F91D Accessible AI building: 4: Audience
      \U0001F4C8 Growing community: 5: Creator"""
    },
    {
        "id": "MM.03",
        "scene": "Scene 3 - Statues vs Mercury",
        "priority": "HIGH",
        "type": "flowchart",
        "direction": "LR",
        "title": "Static Rules vs Dynamic AI",
        "content": """    subgraph OLD["\U0001F5FF OLD WORLD - Static Systems"]
        direction TB
        A["\U0001F4DC Hard-Coded Rules"] --> B["\U0001F512 Rigid Logic"]
        B --> C["\U0001F4A5 Breaks on Change"]
        C --> D["\U0001F6D1 System Down"]
    end
    subgraph NEW["\U0001F4A7 NEW WORLD - Dynamic AI"]
        direction TB
        E["\U0001F916 AI-Driven Rules"] --> F["\U0001F300 Adaptive Logic"]
        F --> G["\U0001F504 Self-Healing"]
        G --> H["\U0001F680 Always Running"]
    end
    OLD -->|"\u26A1 Transform"| NEW

    style A fill:#e74c3c,color:#fff
    style D fill:#c0392b,color:#fff
    style E fill:#2ecc71,color:#fff
    style H fill:#27ae60,color:#fff"""
    },
    {
        "id": "MM.04",
        "scene": "Scene 4 - The Clone Lab",
        "priority": "HIGH",
        "type": "sequence",
        "title": "Git Clone to Local Powerhouse",
        "content": """    participant Dev as \U0001F468\u200D\U0001F4BB Developer
    participant GH as \U0001F431 GitHub
    participant Local as \U0001F4BB Local Machine
    participant Agent as \U0001F916 AI Agent

    Dev->>GH: \U0001F50D Browse delivery pilot template
    GH-->>Dev: \U0001F4E6 Template found
    Dev->>Local: \U0001F4E5 git clone repo
    Local->>Local: \U0001F4C2 Repository ready
    Local->>Agent: \u26A1 Start AI agent
    Agent->>Local: \U0001F528 Execute commands
    Agent->>Local: \U0001F3D7 Build tooling system
    Local-->>Dev: \u2705 Ready to develop!"""
    },
    {
        "id": "MM.05",
        "scene": "Scene 5 - The Free Tier Journey",
        "priority": "HIGH",
        "type": "flowchart",
        "direction": "TB",
        "title": "Zero Capital AI Starter Kit",
        "content": """    A["\U0001F4B0 Zero Capital Start"] --> B["\U0001F4DD VS Code - FREE"]
    A --> C["\U0001F431 GitHub - FREE"]
    A --> D["\U0001F310 Browser - FREE"]
    B --> E{"\U0001F916 Need AI Pair?"}
    E -->|"\u2601 Cloud"| F["\U0001F9D1\u200D\u2708 GitHub Copilot"]
    E -->|"\U0001F4BB Local"| G["\U0001F5B1 Cursor AI"]
    E -->|"\U0001F310 Web"| H["\U0001F4AC ChatGPT Free"]
    F --> I["\U0001F504 Swap Between All"]
    G --> I
    H --> I
    I --> J["\U0001F680 Start Building!"]

    style A fill:#f1c40f,color:#333
    style J fill:#27ae60,color:#fff
    style F fill:#6c5ce7,color:#fff
    style G fill:#00b894,color:#fff
    style H fill:#0984e3,color:#fff"""
    },
    {
        "id": "MM.06",
        "scene": "Scene 6 - Internet Kill Switch",
        "priority": "MEDIUM",
        "type": "flowchart",
        "direction": "TB",
        "title": "Parental Internet Kill Switch",
        "content": """    A["\U0001F468\u200D\U0001F469\u200D\U0001F467\u200D\U0001F466 Parent"] --> B["\U0001F310 GitHub Pages UI"]
    B --> C{"\U0001F476 Select Child"}
    C -->|"\U0001F466 Kid A"| D["\U0001F4F1 MAC Address A"]
    C -->|"\U0001F467 Kid B"| E["\U0001F4F1 MAC Address B"]
    D --> F["\u2699 n8n Workflow"]
    E --> F
    F --> G{"\U0001F6A6 Action"}
    G -->|"Block"| H["\U0001F534 Drop Traffic"]
    G -->|"Allow"| I["\U0001F7E2 Allow Traffic"]
    H --> J["\U0001F634 Bedtime Enforced"]
    I --> K["\U0001F3AE Internet Active"]

    style A fill:#3498db,color:#fff
    style H fill:#e74c3c,color:#fff
    style I fill:#2ecc71,color:#fff
    style J fill:#9b59b6,color:#fff
    style K fill:#1abc9c,color:#fff"""
    },
    {
        "id": "MM.07",
        "scene": "Scene 7 - The LLM Feast",
        "priority": "HIGH",
        "type": "pie",
        "title": "\U0001F37D The LLM Feast - Model Strengths",
        "content": """    "\U0001F9E0 Claude - Reasoning" : 30
    "\U0001F50D ChatGPT - Search" : 25
    "\U0001F4BB DeepSeek - Coding" : 20
    "\U0001F48E Gemini - Versatile Free" : 25"""
    },
    {
        "id": "MM.08",
        "scene": "Scene 8 - Bespoke Logic n8n",
        "priority": "MEDIUM",
        "type": "sequence",
        "title": "n8n Bespoke Automation Flow",
        "content": """    participant Wife as \U0001F469 Wife
    participant UI as \U0001F310 GitHub Pages
    participant N8N as \u2699 n8n Engine
    participant Router as \U0001F4E1 Home Router

    Wife->>UI: \U0001F446 Toggle internet off
    UI->>N8N: \U0001F514 Trigger webhook
    N8N->>N8N: \U0001F50D Lookup MAC address
    N8N->>Router: \U0001F6E1 Apply firewall rule
    Router-->>N8N: \u2705 Rule confirmed
    N8N-->>UI: \U0001F4CA Status updated
    UI-->>Wife: \U0001F44D Done!"""
    },
    {
        "id": "MM.09",
        "scene": "Scene 9 - Success Metrics CICD",
        "priority": "MEDIUM",
        "type": "gantt",
        "title": "\U0001F3AF CI-CD Pipeline and Success Metrics",
        "content": """    section \U0001F4BB Development
    \U0001F33F Feature Branch        :a1, 2026-02-10, 1d
    \u270D Code Changes            :a2, after a1, 1d

    section \u2699 CI-CD Pipeline
    \U0001F3D7 GitHub Actions Build  :a3, after a2, 1d
    \U0001F9EA Automated Tests       :a4, after a3, 1d
    \U0001F680 Deploy to Production  :a5, after a4, 1d

    section \U0001F4CA Metrics
    \U0001F6E1 Compliance Audit     :a6, after a5, 1d
    \U0001F3AF Accuracy Check       :a7, after a6, 1d
    \U0001F4C8 Self Growth          :a8, after a7, 1d"""
    },
    {
        "id": "MM.10",
        "scene": "Scene 10 - Conclusion Call to Action",
        "priority": "HIGH",
        "type": "flowchart",
        "direction": "TB",
        "title": "Your Delivery Pilot Journey",
        "content": """    A["\U0001F4CB Take Assessment"] --> B["\U0001F50D Identify Gaps"]
    B --> C["\U0001F3AC Watch Simulation"]
    C --> D["\U0001F4E5 Clone the Repo"]
    D --> E["\u2699 Configure Environment"]
    E --> F["\U0001F528 Build Your Tools"]
    F --> G["\U0001F680 Launch as Delivery Pilot"]
    G --> H["\U0001F3C6 Build the Future!"]

    style A fill:#3498db,color:#fff
    style B fill:#9b59b6,color:#fff
    style C fill:#e67e22,color:#fff
    style D fill:#2ecc71,color:#fff
    style E fill:#1abc9c,color:#fff
    style F fill:#f39c12,color:#fff
    style G fill:#e74c3c,color:#fff
    style H fill:#f1c40f,color:#333"""
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
        # Look in current dir, parent dir (5_Symbols), and global
        mmdc_path = Path(__file__).parent / "node_modules" / ".bin" / "mmdc"
        if not mmdc_path.exists():
            mmdc_path = Path(__file__).parent.parent / "node_modules" / ".bin" / "mmdc"
        puppeteer_config = Path(__file__).parent / "puppeteer-config.json"
        
        # Remove existing PNG if it exists (to avoid -1 suffix)
        if Path(png_path).exists():
            Path(png_path).unlink()
        
        # Step 1: Convert to PNG using mermaid-cli with enhanced quality
        cmd = [
            str(mmdc_path) if mmdc_path.exists() else "mmdc",
            "-i", md_filepath,
            "-o", png_path,
            "-b", "white",  # White background
            "-t", "default",  # Default theme
            "-s", "2",  # Scale factor for higher resolution (2x)
            "-w", "1920",  # Width in pixels (HD)
            "-H", "1080"  # Height in pixels (HD)
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
            
            # Save as JPEG with high quality and optimization
            img.save(jpeg_path, 'JPEG', quality=95, optimize=True, progressive=True)

            print(f"   ✅ Converted to JPEG: {Path(jpeg_path).name}")

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

def save_diagram_to_file(diagram: Dict, asset_id: str, filename: str) -> tuple[str, Optional[str]]:
    """
    Save diagram to markdown file and convert to JPEG

    Returns:
        Tuple of (markdown_path, jpeg_path)
    """
    filepath = OUTPUT_DIR / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {diagram.get('title', 'Mermaid Diagram')}\n\n")
        f.write(f"**Type:** {diagram['type']}\n")
        f.write(f"**Asset ID:** {asset_id}\n")
        f.write(f"**Generated:** {diagram['timestamp']}\n\n")
        f.write(diagram['diagram_text'])
        f.write("\n\n---\n\n")
        f.write("*Generated by BulkMermaidGenerator.py*\n")
        f.write("*To render: paste the mermaid code into https://mermaid.live*\n")

    print(f"   📄 Markdown saved: {filename}")

    # Also generate JPEG version
    jpeg_path = convert_to_jpeg(str(filepath))
    if jpeg_path:
        print(f"   📸 JPEG exported: {Path(jpeg_path).name}")
    else:
        print(f"   ⚠️  JPEG export failed (install mermaid-cli: npm install -g @mermaid-js/mermaid-cli)")

    return str(filepath), jpeg_path

def main():
    """Main execution function"""
    # Update OUTPUT_DIR if paths_config is available
    global OUTPUT_DIR
    if USE_PATHS_CONFIG and get_weekly_paths and get_latest_weekly_id:
        weekly_id = get_latest_weekly_id() or datetime.now().strftime("%Y-%m-%d")
        paths = get_weekly_paths(weekly_id)
        OUTPUT_DIR = paths['output']
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        print(f"✅ Using paths_config for weekly ID: {weekly_id}")
    else:
        print("⚠️  Using hardcoded output directory")

    print("🗺️  Bulk Mermaid Diagram Generator (Enhanced)")
    print("=" * 70)
    print(f"📁 Output Directory: {OUTPUT_DIR.absolute()}")
    print(f"📊 Total Diagrams: {len(GENERATION_QUEUE)}")
    print("🎨 Features: Subgraphs, Styling, High-Quality JPEG Export")
    print("=" * 70)
    
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
            
            # Save to file (returns markdown and JPEG paths)
            filepath, jpeg_path = save_diagram_to_file(result, asset_id, filename)

            print("   ✅ Generation complete")
            successful += 1
            
            # Track in manifest
            if manifest:
                # Track both markdown and JPEG if available
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
                        "title": item.get("title", scene),
                        "has_jpeg": jpeg_path is not None,
                        "jpeg_path": jpeg_path if jpeg_path else None
                    }
                )

            results.append({
                "asset_id": asset_id,
                "filename": filename,
                "markdown_path": filepath,
                "jpeg_path": jpeg_path,
                "has_jpeg": jpeg_path is not None,
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
    
    # Count JPEG exports
    jpeg_count = sum(1 for r in results if r.get("has_jpeg", False))

    # Save summary
    summary = {
        "generator": "BulkMermaidGenerator",
        "version": "2.0-enhanced",
        "timestamp": datetime.now().isoformat(),
        "total": len(GENERATION_QUEUE),
        "successful": successful,
        "failed": failed,
        "jpeg_exported": jpeg_count,
        "output_directory": str(OUTPUT_DIR.absolute()),
        "features": [
            "Subgraph support",
            "Custom styling per node",
            "High-quality JPEG export (2x scale)",
            "Progressive JPEG optimization",
            "HD resolution (1920x1080)",
            "Manifest tracking"
        ],
        "results": results
    }

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path = OUTPUT_DIR / f"mermaid_summary_{timestamp_str}.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print("\n" + "=" * 70)
    print("📊 GENERATION SUMMARY")
    print("=" * 70)
    print(f"✅ Successful: {successful}/{len(GENERATION_QUEUE)}")
    print(f"❌ Failed: {failed}/{len(GENERATION_QUEUE)}")
    print(f"📸 JPEG Exported: {jpeg_count}/{successful}")
    print(f"📁 Output Directory: {OUTPUT_DIR.absolute()}")
    print(f"📝 Summary: {summary_path.name}")
    print("=" * 70)

    # Installation tips if JPEG export failed
    if jpeg_count < successful:
        print("\n💡 TIP: Install mermaid-cli for automatic JPEG export:")
        print("   npm install -g @mermaid-js/mermaid-cli")
        print("   Requires Node.js: https://nodejs.org/")

    print("\n✅ Done! Check the output directory for your diagrams.")

if __name__ == "__main__":
    main()

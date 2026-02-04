#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Diagrams
Project: The Agentic Era - Managing 240+ Workflows
Generates technical diagrams, flowcharts, and architecture visualizations
"""

import os
import json
from pathlib import Path
from typing import Dict, List

# Install: pip install fal-client
try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

# Configuration
OUTPUT_DIR = Path("./generated_diagrams")
OUTPUT_DIR.mkdir(exist_ok=True)

# Consistency seeds for different diagram styles
SEEDS = {
    "SEED_001": 555123,  # Technical Architecture
    "SEED_002": 555456,  # Process Flows
    "SEED_003": 555789,  # Concept Maps
    "SEED_004": 555000,  # Data Visualization
}

# Brand color palette (reference for prompts)
BRAND_COLORS = {
    "primary_dark": "#1a1a2e",
    "accent_blue": "#00d4ff",
    "accent_purple": "#7b2cbf",
    "secondary_teal": "#00bfa5",
    "highlight_orange": "#ff6b35",
    "text_white": "#ffffff",
}

# Asset generation queue
# Populated based on concepts from EDL - Diagrams specific
GENERATION_QUEUE = [
    {
        "id": "D1.1",
        "name": "agentic_workflow_architecture",
        "priority": "HIGH",
        "scene": "Scene 1",
        "seed_key": "SEED_001",
        "prompt": "High-level technical architecture diagram of an Agentic Workflow system, showing 'User Intent' box -> 'Orchestrator Agent' (central hub) -> connected to multiple specialized Sub-Agents (Research, Coding, Testing, Deployment), connected by data pipelines, clean modern aesthetic, dark background separate distinct nodes, professional software diagram style, 16:9",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "D2.1",
        "name": "data_flow_process",
        "priority": "MEDIUM",
        "scene": "Scene 2",
        "seed_key": "SEED_002",
        "prompt": "Horizontal process flowchart 'Raw Data' -> 'Processing Node' -> 'Structured Output', interconnected with directional arrows, gradients indicating flow, distinct steps, n8n style nodes, modern smooth vector graphics, dark mode UI, blue and purple neon accents, 16:9",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
     {
        "id": "D3.1",
        "name": "neural_network_concept",
        "priority": "LOW",
        "scene": "Scene 3",
        "seed_key": "SEED_003",
        "prompt": "Abstract concept map of a neural network, nodes connecting in a mesh, glowing connections, highlighting the concept of 'Learning' and 'Adaptation', futuristic tech style, deep blue background, cyber security aesthetic, 16:9",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
]


def generate_asset(asset_config: Dict, output_dir: Path) -> Dict:
    """Generate a single asset using fal.ai"""
    print(f"\n{'='*60}")
    print(f"📊 Generating Diagram: {asset_config['name']}")
    print(f"   Scene: {asset_config.get('scene', 'Unknown')}")
    print(f"   Priority: {asset_config.get('priority', 'MEDIUM')}")
    print(f"   Seed: {asset_config['seed_key']} ({SEEDS[asset_config['seed_key']]})")
    print(f"{'='*60}")
    
    try:
        # Prepare arguments
        arguments = {
            "prompt": asset_config["prompt"],
            "image_size": asset_config["image_size"],
            "num_inference_steps": asset_config["num_inference_steps"],
            "seed": SEEDS[asset_config["seed_key"]],
            "num_images": 1,
        }
        
        # Generate image
        print("⏳ Sending request to fal.ai...")
        result = fal_client.subscribe(
            asset_config["model"],
            arguments=arguments,
        )
        
        # Download and save
        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            print(f"✅ Generated successfully!")
            print(f"   URL: {image_url}")
            
            # Save metadata
            output_path = output_dir / f"{asset_config['name']}.json"
            metadata = {
                **asset_config,
                "result_url": image_url,
                "seed_value": SEEDS[asset_config["seed_key"]],
            }
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Metadata saved: {output_path}")
            
            # Download image
            import urllib.request
            image_path = output_dir / f"{asset_config['name']}.png"
            urllib.request.urlretrieve(image_url, image_path)
            print(f"💾 Image saved: {image_path}")
            
            return {
                "success": True,
                "url": image_url,
                "local_path": str(image_path),
            }
        else:
            print(f"❌ Generation failed: No images in result")
            return {"success": False, "error": "No images returned"}
            
    except Exception as e:
        print(f"❌ Error generating asset: {str(e)}")
        return {"success": False, "error": str(e)}

def process_queue(queue: List[Dict], output_dir: Path) -> List[Dict]:
    """Process a queue of diagrams to generate"""
    print(f"\n{'='*60}")
    print("🚀 FAL.AI BATCH ASSET GENERATOR - DIAGRAMS")
    print("   Project: The Agentic Era - Managing 240+ Workflows")
    print("="*60)
    
    # Check API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("\n❌ ERROR: FAL_KEY environment variable not set")
        print("   Set it with: export FAL_KEY='your-api-key-here'")
        print("   Get your key from: https://fal.ai/dashboard/keys")
        return []
    
    print(f"\n✅ API Key found")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print(f"\n📊 Assets to generate: {len(queue)}")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    if not queue:
        print("\n⚠️  QUEUE IS EMPTY. Please populate GENERATION_QUEUE with concepts from EDL.")
        return []

    # Count by priority
    high_priority = [a for a in queue if a.get("priority") == "HIGH"]
    medium_priority = [a for a in queue if a.get("priority") == "MEDIUM"]
    
    print(f"   • HIGH priority: {len(high_priority)}")
    print(f"   • MEDIUM priority: {len(medium_priority)}")
    
    # Generate assets
    results = []
    for i, asset in enumerate(queue, 1):
        print(f"\n\n{'#'*60}")
        print(f"# Asset {i}/{len(queue)}")
        print(f"{'#'*60}")
        
        result = generate_asset(asset, output_dir)
        results.append({
            "asset_id": asset.get("id", f"auto_{i}"),
            "name": asset["name"],
            "priority": asset.get("priority", "MEDIUM"),
            **result
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
            print(f"   • {r['asset_id']}: {r['name']} ({r['priority']})")
    
    if failed:
        print("\n❌ FAILED GENERATIONS:")
        for r in failed:
            print(f"   • {r['asset_id']}: {r['name']} - {r.get('error', 'Unknown error')}")
    
    # Save summary
    summary_path = output_dir / "generation_summary.json"
    with open(summary_path, 'w') as f:
        json.dump({
            "total": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "results": results,
        }, f, indent=2)
    
    print(f"\n💾 Summary saved: {summary_path}")
    print("\n✅ Done!")
    
    return results

def main():
    """Main execution"""
    # Confirm before proceeding
    print("\n" + "="*60)
    response = input("🤔 Proceed with generation? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled by user")
        return
        
    process_queue(GENERATION_QUEUE, OUTPUT_DIR)


if __name__ == "__main__":
    main()

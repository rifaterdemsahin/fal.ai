#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator - Graphics
Project: The Agentic Era - Managing 240+ Workflows
Generates all required graphic assets based on EDL concepts
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional

# Install: pip install fal-client
try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

# Import asset utilities
try:
    from Utils.asset_utils import generate_filename, extract_scene_number, ManifestTracker
except ImportError:
    # Fallback if running standalone
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    try:
        from Utils.asset_utils import generate_filename, extract_scene_number, ManifestTracker
    except ImportError:
        print("⚠️  asset_utils not found. Using legacy naming convention.")
        generate_filename = None
        extract_scene_number = None
        ManifestTracker = None

# Configuration
OUTPUT_DIR = Path("./generated_graphics")
OUTPUT_DIR.mkdir(exist_ok=True)

# Consistency seeds for different asset categories
SEEDS = {
    "SEED_001": 987654,  # B-roll establishing shots
    "SEED_002": 123456,  # Infographics (MUST match)
    "SEED_003": 789012,  # Motion graphics (brand)
    "SEED_004": 345678,  # UI overlays (template)
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
# Populated based on concepts from EDL
GENERATION_QUEUE = [
    {
        "id": "1.1",
        "name": "ferrari_cart_morph",
        "priority": "HIGH",
        "scene": "Scene 1",
        "seed_key": "SEED_003",
        "prompt": "Sleek red Ferrari sports car icon smoothly morphing into simple shopping cart icon, clean vector style, white/transparent background, particle effects during transformation, professional tech presentation aesthetic, minimalist flat design, modern motion graphics style, 16:9",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "4.1",
        "name": "uk_streets_sunday_evening",
        "priority": "MEDIUM",
        "scene": "Scene 4",
        "seed_key": "SEED_001",
        "prompt": "Cinematic shot of empty UK high street on Sunday evening, closed shop fronts with metal shutters down, dim streetlights beginning to illuminate, deserted pedestrian area, typical British town center architecture, moody atmospheric lighting, golden hour or early dusk, realistic urban photography style, slight film grain, 16:9 cinematic aspect ratio, melancholic mood",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "4.2",
        "name": "sunday_5pm_timeline",
        "priority": "HIGH",
        "scene": "Scene 4",
        "seed_key": "SEED_002",
        "prompt": "Motion graphics timeline visualization showing Sunday evening 5:00 PM prominently displayed, large clock icon showing 17:00, row of 5-6 shop icons with red 'X' or 'CLOSED' indicators overlaid, Cambridge location pin subtle in background, clean infographic design, dark background (#1a1a2e) with blue/purple accent colors (#00d4ff, #7b2cbf), modern minimalist style, professional data visualization, 16:9 format",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "4.3",
        "name": "agent_workflow_diagram",
        "priority": "HIGH",
        "scene": "Scene 4",
        "seed_key": "SEED_002",
        "prompt": "Professional workflow diagram showing AI agent process flow in three connected stages from left to right: Stage 1 'DATA COLLECTION' with database/cloud storage icons and arrows pointing inward, Stage 2 'UNDERSTANDING' with brain/AI processor icon and location symbols (home icon transforming to shopping cart), Stage 3 'NOTIFICATION' with mobile phone and notification bell icon, connected by flowing arrows with subtle gradient, clean modern infographic style, dark background (#1a1a2e) with gradient accent colors (blue #00d4ff to purple #7b2cbf), each stage clearly labeled in sans-serif font, professional technical diagram, 16:9 aspect ratio",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "4.4",
        "name": "chatbot_vs_realtime",
        "priority": "HIGH",
        "scene": "Scene 4",
        "seed_key": "SEED_002",
        "prompt": "Split-screen comparison graphic in 16:9 format, LEFT SIDE: traditional chatbot interface showing static conversation bubbles, waiting cursor, inactive state, muted gray colors (#6b6b6b); RIGHT SIDE: active real-time AI system showing live notification badges, proactive alert icons, dynamic response indicators, vibrant blue/purple colors (#00d4ff, #7b2cbf), visual contrast between passive vs active AI systems, modern UI design elements, professional software comparison layout, clean typography, dark background",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "5.1",
        "name": "bounded_contexts_diagram",
        "priority": "MEDIUM",
        "scene": "Scene 5",
        "seed_key": "SEED_002",
        "prompt": "Technical architecture diagram showing three parallel workflow streams, each enclosed in a distinct containment box with rounded corners, left workflow labeled 'BOUNDED CONTEXT: FAMILY' with house icon and blue border (#00d4ff), middle workflow 'BOUNDED CONTEXT: FINANCE' with dollar icon and purple border (#7b2cbf), right workflow 'BOUNDED CONTEXT: PROJECTS' with folder icon and teal border (#00bfa5), each box contains simplified workflow nodes ending in Telegram icon, clean separation between contexts, professional software architecture visualization, dark background, modern tech diagram style, 16:9 format",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "6.1",
        "name": "20_dollar_pricing",
        "priority": "HIGH",
        "scene": "Scene 6",
        "seed_key": "SEED_002",
        "prompt": "Bold pricing graphic with '$20' in very large prominent numbers (72pt+), '/month' text below in medium size (36pt), surrounded by circular arrangement of 5 tool icons: n8n logo, Telegram icon, Obsidian icon, Gemini sparkle, Claude icon, clean modern design with subtle gradient background (dark blue to purple #1a1a2e to #7b2cbf), pricing emphasis layout with glowing effect around price, professional infographic style, affordability message clear, minimalist design, white/cyan text (#ffffff, #00d4ff), 16:9 aspect ratio",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "7.1",
        "name": "deliverpilot_methodology",
        "priority": "MEDIUM",
        "scene": "Scene 7",
        "seed_key": "SEED_002",
        "prompt": "Horizontal flowchart showing 4 connected stages from left to right: 'UNKNOWN PROBLEM' box with question mark icon → 'SYMBOL/MODEL' box with diagram icon → 'n8n SIMULATION' box with workflow icon → 'TESTING/VALIDATION' box with checkmark icon, connected by right-pointing arrows, each box has distinct color (red, yellow, blue, green gradients), clean process diagram style, dark background (#1a1a2e), modern infographic design, professional methodology visualization, sans-serif labels, 16:9 format",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "8.1",
        "name": "state_management_flow",
        "priority": "MEDIUM",
        "scene": "Scene 8",
        "seed_key": "SEED_002",
        "prompt": "Technical diagram showing state management flow in 5 connected boxes: 'PREVIOUS STATE' (database cylinder icon) → 'CURRENT INPUT' (arrow icon) → 'STATE COMPARISON' (equals/not-equals icon) → 'DECISION' (fork/branch icon) → 'UPDATE STATE' (save icon), connected by arrows with data flow indicators, positioned to overlay on workflow nodes, clean technical documentation style, cyan/blue color scheme (#00d4ff, #0096c7), dark transparent background, professional system architecture diagram, 16:9 format",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "9.1",
        "name": "corporate_meeting",
        "priority": "LOW",
        "scene": "Scene 9",
        "seed_key": "SEED_001",
        "prompt": "Cinematic shot of modern corporate meeting room, 4-5 business professionals sitting around conference table looking at laptops with frustrated expressions, large monitor on wall displaying generic charts, glass walls visible, fluorescent office lighting, professional business environment, realistic corporate photography style, slightly desaturated colors for serious tone, 16:9 cinematic aspect ratio",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "9.2",
        "name": "silos_vs_agents",
        "priority": "HIGH",
        "scene": "Scene 9",
        "seed_key": "SEED_002",
        "prompt": "Split-screen comparison in 16:9 format, LEFT SIDE 'SILO APPROACH': 4 isolated figures in separate gray boxes, each with only small ChatGPT icon, disconnected units with no connections, muted gray/blue colors (#6b6b6b, #404040), text overlay 'ChatGPT only, No automation, Manual work'; RIGHT SIDE 'AGENT APPROACH': interconnected network of nodes/circles representing AI agents, colorful flowing lines connecting multiple systems, data particle effects, vibrant blue/purple/cyan colors (#00d4ff, #7b2cbf, #00bfa5), text overlay 'Deployed agents, Data collection, Automated workflows', modern infographic design, clear visual contrast, professional comparison graphic",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "9.3",
        "name": "bottom_up_revolution",
        "priority": "HIGH",
        "scene": "Scene 9",
        "seed_key": "SEED_002",
        "prompt": "Bold motivational graphic showing large upward arrow labeled 'BOTTOM-UP' in vibrant gold/orange gradient (#ff6b35, #f7931e) moving from bottom to top, crossed-out downward arrow labeled 'TOP-DOWN' faded in background, individual empowerment icon (person silhouette with gear/tools) at bottom of upward arrow, Microsoft Copilot button icon shown dimmed/crossed out, revolutionary theme with energetic colors, grassroots movement aesthetic, strong typographic emphasis with sans-serif bold font, motivational infographic style, dark background (#1a1a2e), 16:9 aspect ratio",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "10.1",
        "name": "phone_before_after",
        "priority": "MEDIUM",
        "scene": "Scene 10",
        "seed_key": "SEED_002",
        "prompt": "Side-by-side phone screens in 16:9 layout, LEFT 'BEFORE': iPhone home screen cluttered with social media apps - YouTube (red icon), Instagram (gradient icon), Reddit (orange icon), TikTok, multiple game apps, notification badges, chaotic layout; RIGHT 'AFTER': same iPhone with minimalist clean home screen showing only Google Gemini app icon, Claude app icon, Calendar, Notes app, mostly empty screen with clean modern wallpaper, visual contrast between distraction vs focus, realistic iOS interface design, modern smartphone mockup",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
    {
        "id": "11.1",
        "name": "ai_job_message",
        "priority": "HIGH",
        "scene": "Scene 11",
        "seed_key": "SEED_003",
        "prompt": "Bold typographic design with powerful message, main text 'AI ISN'T COMING FOR YOUR JOB' in very large prominent letters (96pt sans-serif, all caps), positioned in upper two-thirds, secondary text below 'YOU MUST TRANSFORM TO KEEP IT' in medium size (48pt), dramatic color scheme with dark background (#0a0a0a) and bright white/gold text (#ffffff, #f7931e), empowering yet serious tone, professional motivational graphic design, clean modern typography, strong visual hierarchy, 16:9 aspect ratio",
        "model": "fal-ai/flux/dev",
        "image_size": {"width": 1920, "height": 1080},
        "num_inference_steps": 28,
    },
]


def generate_asset(asset_config: Dict, output_dir: Path, manifest: Optional[object] = None, version: int = 1) -> Dict:
    """Generate a single asset using fal.ai"""
    print(f"\n{'='*60}")
    print(f"🎨 Generating: {asset_config['name']}")
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
            
            # Generate filename using new convention if available
            if generate_filename and extract_scene_number:
                scene_num = extract_scene_number(asset_config.get('id', '0.0'))
                base_filename = generate_filename(
                    scene_num,
                    'graphic',
                    asset_config['name'],
                    version
                )
                filename_json = base_filename + '.json'
                filename_png = base_filename + '.png'
            else:
                # Fallback to legacy naming
                filename_json = f"{asset_config['name']}.json"
                filename_png = f"{asset_config['name']}.png"
            
            # Save metadata
            output_path = output_dir / filename_json
            metadata = {
                **asset_config,
                "result_url": image_url,
                "seed_value": SEEDS[asset_config["seed_key"]],
                "filename": filename_png,
            }
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Metadata saved: {output_path}")
            
            # Download image
            import urllib.request
            image_path = output_dir / filename_png
            urllib.request.urlretrieve(image_url, image_path)
            print(f"💾 Image saved: {image_path}")
            
            # Add to manifest if provided
            if manifest:
                manifest.add_asset(
                    filename=filename_png,
                    prompt=asset_config["prompt"],
                    asset_type="graphic",
                    asset_id=asset_config.get("id", "unknown"),
                    result_url=image_url,
                    local_path=str(image_path),
                    metadata={
                        "scene": asset_config.get("scene", ""),
                        "priority": asset_config.get("priority", ""),
                        "model": asset_config.get("model", ""),
                    }
                )
            
            return {
                "success": True,
                "url": image_url,
                "local_path": str(image_path),
                "filename": filename_png,
            }
        else:
            print(f"❌ Generation failed: No images in result")
            return {"success": False, "error": "No images returned"}
            
    except Exception as e:
        print(f"❌ Error generating asset: {str(e)}")
        return {"success": False, "error": str(e)}

def process_queue(queue: List[Dict], output_dir: Path, manifest: Optional[object] = None) -> List[Dict]:
    """Process a queue of graphics to generate"""
    print(f"\n{'='*60}")
    print("🚀 FAL.AI BATCH ASSET GENERATOR - GRAPHICS")
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
        
        result = generate_asset(asset, output_dir, manifest)
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

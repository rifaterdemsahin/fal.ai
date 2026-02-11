#!/usr/bin/env python3
"""
Test script for Infographics Generator with fal.ai integration.

This script validates the BatchAssetGeneratorInfographics module by running
a small test batch and verifying the output.
"""
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
import traceback


def setup_paths() -> tuple[Path, Path]:
    """Configure project paths and add to sys.path."""
    project_root = Path(__file__).resolve().parent.parent.parent
    symbols_path = project_root / "5_Symbols"
    sys.path.append(str(symbols_path))
    return project_root, symbols_path


def import_generator():
    """Import the BatchAssetGeneratorInfographics module with error handling."""
    try:
        from Images import BatchAssetGeneratorInfographics
        return BatchAssetGeneratorInfographics
    except ImportError as e:
        print(f"❌ Import Error: Failed to load BatchAssetGeneratorInfographics")
        print(f"   Details: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   - Verify the module exists in 5_Symbols/Images/")
        print(f"   - Check for missing dependencies")
        sys.exit(1)


def verify_environment() -> bool:
    """Check required environment variables."""
    if not os.environ.get("FAL_KEY"):
        print("❌ Environment Error: FAL_KEY not set")
        print("\n💡 Setup Instructions:")
        print("   export FAL_KEY='your-api-key-here'")
        print("   Or add to your .env file")
        return False
    return True


def create_test_batch() -> List[Dict[str, Any]]:
    """Define test infographic configurations for Kubernetes concepts."""
    return [
        {
            "id": "K8S_PODS_01",
            "name": "kubernetes_pods",
            "priority": "HIGH",
            "scene": "Kubernetes Architecture",
            "seed_key": "SEED_K8S_01",
            "prompt": "Infographic explaining Kubernetes Pods: The smallest deployable units of computing that you can create and manage in Kubernetes. Visualizing a pod wrapping a container.",
            "image_size": {"width": 1920, "height": 1080},
            "num_inference_steps": 28,
            "model": "fal-ai/flux/dev"
        },
        {
            "id": "K8S_CONTAINERS_01",
            "name": "kubernetes_containers",
            "priority": "HIGH",
            "scene": "Kubernetes Architecture",
            "seed_key": "SEED_K8S_02",
            "prompt": "Infographic showing Kubernetes Containers: Lightweight, standalone, executable packages of software that include everything needed to run an application.",
            "image_size": {"width": 1920, "height": 1080},
            "num_inference_steps": 28,
            "model": "fal-ai/flux/dev"
        },
        {
            "id": "K8S_ROUTES_01",
            "name": "kubernetes_routes",
            "priority": "HIGH",
            "scene": "Kubernetes Architecture",
            "seed_key": "SEED_K8S_03",
            "prompt": "Infographic illustrating Kubernetes Routes and Ingress: Managing external access to the services in a cluster, typically HTTP.",
            "image_size": {"width": 1920, "height": 1080},
            "num_inference_steps": 28,
            "model": "fal-ai/flux/dev"
        },
        {
            "id": "K8S_SERVICES_01",
            "name": "kubernetes_services",
            "priority": "HIGH",
            "scene": "Kubernetes Architecture",
            "seed_key": "SEED_K8S_04",
            "prompt": "Infographic defining Kubernetes Services: An abstract way to expose an application running on a set of Pods as a network service.",
            "image_size": {"width": 1920, "height": 1080},
            "num_inference_steps": 28,
            "model": "fal-ai/flux/dev"
        },
        {
            "id": "K8S_CONFIGMAP_01",
            "name": "kubernetes_configmaps",
            "priority": "HIGH",
            "scene": "Kubernetes Architecture",
            "seed_key": "SEED_K8S_05",
            "prompt": "Infographic about Kubernetes ConfigMaps: An API object used to store non-confidential data in key-value pairs.",
            "image_size": {"width": 1920, "height": 1080},
            "num_inference_steps": 28,
            "model": "fal-ai/flux/dev"
        },
        {
            "id": "K8S_SECRETS_01",
            "name": "kubernetes_secrets",
            "priority": "HIGH",
            "scene": "Kubernetes Architecture",
            "seed_key": "SEED_K8S_06",
            "prompt": "Infographic explaining Kubernetes Secrets: An object that contains a small amount of sensitive data such as a password, a token, or a key.",
            "image_size": {"width": 1920, "height": 1080},
            "num_inference_steps": 28,
            "model": "fal-ai/flux/dev"
        }
    ]


def print_results(output_dir: Path) -> None:
    """Display generation results and file listing."""
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE")
    print("=" * 70)
    
    # Count generated files
    png_files = list(output_dir.glob("*.png"))
    json_files = list(output_dir.glob("*.json"))
    
    print(f"\n📊 Results Summary:")
    print(f"   Images:   {len(png_files)}")
    print(f"   Metadata: {len(json_files)}")
    print(f"   Total:    {len(png_files) + len(json_files)}")
    
    if png_files or json_files:
        print(f"\n📂 Output Location:")
        print(f"   {output_dir}")
        print(f"\n📄 Generated Files:")
        for f in sorted(png_files + json_files):
            size_kb = f.stat().st_size / 1024
            print(f"   • {f.name:<40} ({size_kb:>8.1f} KB)")
    else:
        print("\n⚠️  No files were generated")
    
    print("=" * 70)


def test_infographics_generation() -> None:
    """Main test execution function."""
    print("🚀 Infographics Generator Test Suite")
    print("=" * 70)
    
    # Setup
    project_root, _ = setup_paths()
    output_dir = (
        project_root / "7_TestingKnown" / "TestOutput" / 
        "generated_assets" / "infographics"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Output: {output_dir}")
    
    # Verify environment
    if not verify_environment():
        sys.exit(1)
    
    # Import module
    generator = import_generator()
    
    # Prepare test data
    test_batch = create_test_batch()
    
    # Add timestamp to filenames to prevent overwriting
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for item in test_batch:
        item["name"] = f"{item['name']}_{timestamp}"

    print(f"\n🧪 Test Batch: {len(test_batch)} infographic(s)")
    
    # Execute generation
    try:
        print("\n⏳ Generating assets...")
        generator.process_queue(test_batch, output_dir)
        print_results(output_dir)
        
    except Exception as e:
        print(f"\n❌ Generation Failed")
        print(f"   Error: {e}")
        print(f"\n🔍 Full Traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    test_infographics_generation()
#!/usr/bin/env python3
"""
Base Asset Generator
Common functionality for all asset generators
"""

import os
import json
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

# Import from parent directory
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from asset_utils import generate_filename, extract_scene_number, ManifestTracker


class BaseAssetGenerator(ABC):
    """
    Abstract base class for all asset generators.
    Provides common functionality for generating assets using fal.ai.
    """
    
    def __init__(
        self,
        output_dir: Path,
        seeds: Dict[str, int],
        brand_colors: Dict[str, str],
        asset_type: str
    ):
        """
        Initialize the base generator.
        
        Args:
            output_dir: Directory for output files
            seeds: Dictionary of seed values for consistency
            brand_colors: Brand color palette
            asset_type: Type of asset (e.g., 'image', 'video', 'music')
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.seeds = seeds
        self.brand_colors = brand_colors
        self.asset_type = asset_type
        self.manifest = None
        
    @abstractmethod
    def get_generation_queue(self) -> List[Dict]:
        """
        Return the list of assets to generate.
        Must be implemented by subclasses.
        """
        pass
    
    def check_api_key(self) -> str:
        """Check and return FAL_KEY from environment."""
        api_key = os.environ.get("FAL_KEY")
        if not api_key:
            print("\n❌ ERROR: FAL_KEY environment variable not set")
            print("   Set it with: export FAL_KEY='your-api-key-here'")
            raise ValueError("FAL_KEY not set")
        return api_key
    
    def prepare_arguments(self, asset_config: Dict) -> Dict[str, Any]:
        """
        Prepare arguments for fal.ai API call.
        Can be overridden by subclasses for custom behavior.
        
        Args:
            asset_config: Configuration for the asset
            
        Returns:
            Dictionary of arguments for fal_client.subscribe()
        """
        arguments = {
            "prompt": asset_config["prompt"],
        }
        
        # Add common image parameters if present
        if "image_size" in asset_config:
            arguments["image_size"] = asset_config["image_size"]
        if "num_inference_steps" in asset_config:
            arguments["num_inference_steps"] = asset_config["num_inference_steps"]
        if "seed_key" in asset_config and asset_config["seed_key"] in self.seeds:
            arguments["seed"] = self.seeds[asset_config["seed_key"]]
        if "num_images" in asset_config:
            arguments["num_images"] = asset_config["num_images"]
            
        return arguments
    
    def extract_result_url(self, result: Dict, asset_config: Dict) -> Optional[str]:
        """
        Extract the result URL from the API response.
        Can be overridden by subclasses for different result structures.
        
        Args:
            result: Response from fal.ai API
            asset_config: Configuration for the asset
            
        Returns:
            URL of the generated asset, or None if not found
        """
        # Default: look for images array
        if result and "images" in result and len(result["images"]) > 0:
            return result["images"][0]["url"]
        # Alternative: direct URL field
        elif result and "url" in result:
            return result["url"]
        # Video response
        elif result and "video" in result and "url" in result["video"]:
            return result["video"]["url"]
        return None
    
    def get_file_extension(self, asset_config: Dict) -> str:
        """
        Get the file extension for this asset type.
        Can be overridden by subclasses.
        
        Args:
            asset_config: Configuration for the asset
            
        Returns:
            File extension (e.g., 'png', 'mp4', 'mp3')
        """
        if self.asset_type in ['image', 'graphic', 'icon', 'lower_third', 'svg', 'diagram', 'memory_palace']:
            return 'png'
        elif self.asset_type == 'video':
            return 'mp4'
        elif self.asset_type == 'music':
            return 'mp3'
        else:
            return 'bin'
    
    def generate_asset(
        self,
        asset_config: Dict,
        version: int = 1
    ) -> Dict:
        """
        Generate a single asset using fal.ai.
        Common implementation used by all generators.
        
        Args:
            asset_config: Configuration dictionary for the asset
            version: Version number for the asset
            
        Returns:
            Dictionary with success status and metadata
        """
        print(f"\n{'='*60}")
        print(f"🎨 Generating {self.asset_type}: {asset_config['name']}")
        print(f"   Scene: {asset_config.get('scene', 'Unknown')}")
        print(f"   Priority: {asset_config.get('priority', 'MEDIUM')}")
        if 'seed_key' in asset_config:
            print(f"   Seed: {asset_config['seed_key']} ({self.seeds.get(asset_config['seed_key'], 'N/A')})")
        print(f"{'='*60}")
        
        try:
            # Prepare arguments
            arguments = self.prepare_arguments(asset_config)
            
            # Generate asset
            print("⏳ Sending request to fal.ai...")
            result = fal_client.subscribe(
                asset_config["model"],
                arguments=arguments,
            )
            
            # Extract result URL
            result_url = self.extract_result_url(result, asset_config)
            
            if not result_url:
                return {
                    "success": False,
                    "error": "No URL in result",
                }
            
            print(f"✅ Generated successfully!")
            print(f"   URL: {result_url}")
            
            # Generate filename
            scene_num = extract_scene_number(asset_config.get('id', '0.0'))
            extension = self.get_file_extension(asset_config)
            base_filename = generate_filename(
                scene_num,
                self.asset_type,
                asset_config['name'],
                version
            )
            filename_json = base_filename + '.json'
            filename_asset = base_filename + '.' + extension
            
            # Save metadata
            metadata = {
                **asset_config,
                "result_url": result_url,
                "filename": filename_asset,
            }
            if 'seed_key' in asset_config:
                metadata["seed_value"] = self.seeds.get(asset_config["seed_key"])
            
            metadata_path = self.output_dir / filename_json
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"💾 Metadata saved: {metadata_path}")
            
            # Download asset
            asset_path = self.output_dir / filename_asset
            urllib.request.urlretrieve(result_url, asset_path)
            print(f"💾 Asset saved: {asset_path}")
            
            # Add to manifest if available
            if self.manifest:
                self.manifest.add_asset(
                    filename=filename_asset,
                    prompt=asset_config["prompt"],
                    asset_type=self.asset_type,
                    asset_id=asset_config.get("id", "unknown"),
                    result_url=result_url,
                    local_path=str(asset_path),
                    metadata={
                        "scene": asset_config.get("scene", ""),
                        "priority": asset_config.get("priority", ""),
                        "model": asset_config.get("model", ""),
                    }
                )
            
            return {
                "success": True,
                "url": result_url,
                "local_path": str(asset_path),
            }
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }
    
    def process_queue(
        self,
        queue: Optional[List[Dict]] = None
    ) -> List[Dict]:
        """
        Process the entire generation queue.
        
        Args:
            queue: Optional queue to process (uses get_generation_queue() if None)
            
        Returns:
            List of results for each asset
        """
        if queue is None:
            queue = self.get_generation_queue()
            
        print("="*60)
        print(f"   🎨 fal.ai {self.asset_type.title()} Generator")
        print("   Project: The Agentic Era - Managing 240+ Workflows")
        print("="*60)
        
        # Check API key
        try:
            self.check_api_key()
        except ValueError:
            return []
        
        print(f"\n✅ API Key found")
        print(f"📁 Output directory: {self.output_dir.absolute()}")
        print(f"\n📊 Assets to generate: {len(queue)}")
        
        if not queue:
            print("\n⚠️  QUEUE IS EMPTY.")
            return []
        
        # Count by priority
        high_priority = [a for a in queue if a.get("priority") == "HIGH"]
        medium_priority = [a for a in queue if a.get("priority") == "MEDIUM"]
        low_priority = [a for a in queue if a.get("priority") == "LOW"]
        
        print(f"   • HIGH priority: {len(high_priority)}")
        print(f"   • MEDIUM priority: {len(medium_priority)}")
        print(f"   • LOW priority: {len(low_priority)}")
        
        # Generate assets
        results = []
        for i, asset in enumerate(queue, 1):
            print(f"\n\n{'#'*60}")
            print(f"# Asset {i}/{len(queue)}")
            print(f"{'#'*60}")
            
            result = self.generate_asset(asset)
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
        summary_path = self.output_dir / "generation_summary.json"
        with open(summary_path, 'w') as f:
            json.dump({
                "asset_type": self.asset_type,
                "total": len(results),
                "successful": len(successful),
                "failed": len(failed),
                "results": results,
            }, f, indent=2)
        
        print(f"\n💾 Summary saved: {summary_path}")
        print("\n✅ Done!")
        
        return results
    
    def run(self, confirm: bool = True):
        """
        Main execution method.
        
        Args:
            confirm: Whether to ask for confirmation before proceeding
        """
        if confirm:
            print("\n" + "="*60)
            response = input("🤔 Proceed with generation? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("❌ Cancelled by user")
                return
        
        self.process_queue()

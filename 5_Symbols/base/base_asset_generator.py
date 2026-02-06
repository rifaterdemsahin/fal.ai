#!/usr/bin/env python3
"""
Base Asset Generator
Common functionality for all asset generators
"""

import os
import json
import urllib.request
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

try:
    from PIL import Image
except ImportError:
    print("❌ Pillow not installed. Run: pip install Pillow")
    exit(1)

# Import from parent directory
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from asset_utils import generate_filename, extract_scene_number, ManifestTracker

# Import configuration (relative import from same package)
from .generator_config import OUTPUT_FORMATS

# Pre-compute image asset types that support conversion (computed once at module level)
IMAGE_ASSET_TYPES = [k for k, v in OUTPUT_FORMATS.items() 
                     if v in ('jpeg', 'png') and k != 'svg']


class BaseAssetGenerator(ABC):
    """
    Abstract base class for all asset generators.
    Provides common functionality for generating assets using fal.ai.
    """
    
    # File extension mapping for asset types
    ASSET_TYPE_EXTENSIONS = {
        'image': 'png',
        'graphic': 'png',
        'icon': 'png',
        'lower_third': 'png',
        'svg': 'svg',
        'diagram': 'png',
        'memory_palace': 'png',
        'chapter_marker': 'png',
        'video': 'mp4',
        'music': 'mp3',
        'audio': 'mp3',
    }
    
    def __init__(
        self,
        output_dir: Path,
        seeds: Dict[str, int],
        brand_colors: Dict[str, str],
        asset_type: str,
        output_format: Optional[str] = None
    ):
        """
        Initialize the base generator.
        
        Args:
            output_dir: Directory for output files
            seeds: Dictionary of seed values for consistency
            brand_colors: Brand color palette
            asset_type: Type of asset (e.g., 'image', 'video', 'music')
            output_format: Override output format (e.g., 'jpeg', 'png'). 
                          If None, uses OUTPUT_FORMATS from config
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.seeds = seeds
        self.brand_colors = brand_colors
        self.asset_type = asset_type
        self.manifest = None
        self.output_format = output_format  # Store the desired output format
        
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
            print("   Set it in your shell with: export FAL_KEY='your-api-key-here'  (bash/zsh)")
            print("   Or for Windows: set FAL_KEY=your-api-key-here  (cmd)")
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
            File extension (e.g., 'png', 'jpeg', 'mp4', 'mp3')
        """
        # Use output_format if specified, otherwise use default
        if self.output_format:
            return self.output_format
        return self.ASSET_TYPE_EXTENSIONS.get(self.asset_type, 'bin')
    
    def convert_to_jpeg(self, png_path: Path, jpeg_path: Path, quality: int = 95) -> bool:
        """
        Convert a PNG image to JPEG format.
        
        Transparency handling:
        - RGBA (RGB with alpha): Alpha channel is used as mask, transparent areas become white
        - LA (grayscale with alpha): Alpha channel is used as mask, transparent areas become white
        - P (palette mode): Converted to RGBA first, then transparency becomes white
        - RGB: Direct conversion to JPEG (no transparency handling needed)
        
        Args:
            png_path: Path to the source PNG file
            jpeg_path: Path to save the JPEG file
            quality: JPEG quality (1-100, default 95 for high quality)
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            # Open PNG image
            with Image.open(png_path) as img:
                # Convert RGBA to RGB if necessary (JPEG doesn't support transparency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create a white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    # Convert palette mode to RGBA first
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    # Extract alpha channel for mask (handles both RGBA and LA modes)
                    # After P->RGBA conversion, img.mode will be 'RGBA', 'LA', or original mode
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Save as JPEG
                img.save(jpeg_path, 'JPEG', quality=quality, optimize=True)
                
            return True
        except Exception as e:
            print(f"⚠️  Warning: Failed to convert to JPEG: {e}")
            return False
    
    def optimize_png_for_resolve(self, png_path: Path) -> bool:
        """
        Optimize PNG file for DaVinci Resolve compatibility.
        
        Ensures:
        - 32-bit format (RGBA with 8-bit per channel) - standard RGB + Alpha
        - Not indexed color mode (mode 'P')
        - No metadata (removes EXIF, XMP, and other metadata)
        
        This prevents DaVinci Resolve issues with:
        - Auto-detect or 8-bit indexed colors
        - Hidden metadata that might confuse Resolve
        
        Args:
            png_path: Path to the PNG file to optimize
            
        Returns:
            True if optimization successful, False otherwise
        """
        try:
            # Open PNG image
            with Image.open(png_path) as img:
                # Get original mode for logging
                original_mode = img.mode
                
                # Convert to RGBA (32-bit: 8-bit per channel RGB + Alpha)
                # This ensures we never have indexed colors (mode 'P') or other problematic modes
                if img.mode != 'RGBA':
                    # Preserve transparency if present
                    if img.mode in ('P', 'PA', 'LA'):
                        # These modes have transparency/alpha that we want to keep
                        img = img.convert('RGBA')
                    elif img.mode == 'RGB':
                        # Add full opacity alpha channel to RGB images
                        img = img.convert('RGBA')
                    elif img.mode in ('L', '1'):
                        # Grayscale or binary - convert to RGBA
                        img = img.convert('RGBA')
                    else:
                        # For any other mode, convert to RGBA
                        img = img.convert('RGBA')
                    
                    print(f"   🔄 Converted PNG mode: {original_mode} → RGBA (32-bit)")
                
                # Save with optimized settings for DaVinci Resolve
                # - No metadata (exif=None removes EXIF, XMP, and other metadata)
                # - RGBA mode ensures 32-bit format
                # - optimize=True for better compression
                img.save(png_path, 'PNG', optimize=True, exif=b'')
                
            return True
        except Exception as e:
            print(f"⚠️  Warning: Failed to optimize PNG for Resolve: {e}")
            return False
    
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
            
            # Download asset from fal.ai (always downloads as PNG for images)
            # Use UUID to ensure unique temporary filename for guaranteed thread safety
            unique_id = uuid.uuid4().hex[:8]  # First 8 hexadecimal characters (4 bytes)
            temp_path = self.output_dir / f"{base_filename}_temp_{unique_id}.png"
            asset_path = self.output_dir / filename_asset
            
            # Determine if we need conversion
            # Only convert to JPEG if:
            # 1. The output format is 'jpeg'
            # 2. The asset type is one that supports conversion (image-based assets)
            needs_conversion = (
                extension == 'jpeg' and 
                self.asset_type in IMAGE_ASSET_TYPES
            )
            
            if needs_conversion:
                # Download as temporary PNG first
                urllib.request.urlretrieve(result_url, temp_path)
                print(f"💾 Downloaded temporary PNG: {temp_path}")
                
                # Convert to JPEG
                if self.convert_to_jpeg(temp_path, asset_path, quality=95):
                    print(f"🔄 Converted to JPEG: {asset_path}")
                    # Get file size comparison
                    png_size = temp_path.stat().st_size / 1024  # KB
                    jpeg_size = asset_path.stat().st_size / 1024  # KB
                    savings = ((png_size - jpeg_size) / png_size) * 100
                    print(f"   📦 Size: {png_size:.1f}KB (PNG) → {jpeg_size:.1f}KB (JPEG) - {savings:.1f}% smaller")
                    # Clean up temporary PNG
                    temp_path.unlink()
                else:
                    # Conversion failed, use PNG instead
                    print(f"⚠️  Using PNG format instead")
                    temp_path.rename(asset_path)
                    # Optimize the PNG for DaVinci Resolve since we're keeping it
                    print(f"🔧 Optimizing PNG for DaVinci Resolve...")
                    self.optimize_png_for_resolve(asset_path)
            else:
                # Direct download without conversion
                urllib.request.urlretrieve(result_url, asset_path)
                print(f"💾 Asset saved: {asset_path}")
                
                # Optimize PNG files for DaVinci Resolve compatibility
                if extension == 'png':
                    print(f"🔧 Optimizing PNG for DaVinci Resolve...")
                    self.optimize_png_for_resolve(asset_path)
            
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

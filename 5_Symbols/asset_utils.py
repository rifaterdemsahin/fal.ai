#!/usr/bin/env python3
"""
Asset Utilities
Common utilities for asset generation including file naming and manifest tracking
"""

import json
import re
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# Optional imports for SVG to JPEG conversion
try:
    import cairosvg
    from PIL import Image
    import io
    SVG_CONVERSION_AVAILABLE = True
except (ImportError, OSError):
    SVG_CONVERSION_AVAILABLE = False


def clean_description(description: str) -> str:
    """
    Clean a description for use in filenames.
    Removes special characters, converts to lowercase, replaces spaces with underscores.
    
    Args:
        description: The description to clean
        
    Returns:
        Cleaned description suitable for filename
    """
    # Convert to lowercase
    clean = description.lower()
    # Replace spaces and hyphens with underscores
    clean = clean.replace(' ', '_').replace('-', '_')
    # Remove any character that's not alphanumeric or underscore
    clean = re.sub(r'[^a-z0-9_]', '', clean)
    # Replace multiple underscores with single underscore
    clean = re.sub(r'_+', '_', clean)
    # Remove leading/trailing underscores
    clean = clean.strip('_')
    return clean


def generate_filename(
    scene_number: int,
    asset_type: str,
    description: str,
    version: Optional[int] = None,
    extension: Optional[str] = None
) -> str:
    """
    Generate a standardized filename following the format:
    {scene_number:03d}_{asset_type}_{clean_desc}_v{version}.{extension}
    
    Args:
        scene_number: Scene number (will be zero-padded to 3 digits)
        asset_type: Type of asset (e.g., 'image', 'video', 'music', 'icon')
        description: Description of the asset
        version: Optional version number (if None, no version suffix is added)
        extension: Optional file extension (without dot)
        
    Returns:
        Formatted filename
        
    Examples:
        >>> generate_filename(1, 'image', 'ferrari cart morph', 1, 'png')
        '001_image_ferrari_cart_morph_v1.png'
        >>> generate_filename(4, 'video', 'uk streets sunday', 2)
        '004_video_uk_streets_sunday_v2'
    """
    clean_desc = clean_description(description)
    
    # Format: {scene_number:03d}_{asset_type}_{clean_desc}
    filename = f"{scene_number:03d}_{asset_type}_{clean_desc}"
    
    # Add version if provided
    if version is not None:
        filename += f"_v{version}"
    
    # Add extension if provided
    if extension:
        filename += f".{extension}"
    
    return filename


def extract_scene_number(asset_id: str) -> int:
    """
    Extract scene number from asset ID (e.g., "1.1" -> 1, "4.2" -> 4)
    
    Args:
        asset_id: Asset ID in format "scene.number"
        
    Returns:
        Scene number as integer
    """
    try:
        return int(asset_id.split('.')[0])
    except (ValueError, IndexError, AttributeError):
        return 0


class ManifestTracker:
    """
    Tracks all generated assets and creates a unified manifest.json
    """
    
    def __init__(self, project_dir: Path):
        """
        Initialize the manifest tracker
        
        Args:
            project_dir: Root directory of the project (e.g., 3_Simulation/Feb1Youtube)
        """
        self.project_dir = Path(project_dir)
        self.assets = []
        self.start_time = datetime.now()
        
    def add_asset(
        self,
        filename: str,
        prompt: str,
        asset_type: str,
        asset_id: str,
        result_url: Optional[str] = None,
        local_path: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Add an asset to the manifest
        
        Args:
            filename: The filename of the generated asset
            prompt: The prompt used to generate the asset
            asset_type: Type of asset (image, video, music, etc.)
            asset_id: Unique asset ID
            result_url: URL of the generated asset (if available)
            local_path: Local path where the asset is saved
            metadata: Additional metadata to store
        """
        timestamp = datetime.now().isoformat()
        
        asset_entry = {
            "filename": filename,
            "prompt": prompt,
            "timestamp": timestamp,
            "asset_type": asset_type,
            "asset_id": asset_id,
        }
        
        if result_url:
            asset_entry["result_url"] = result_url
        
        if local_path:
            asset_entry["local_path"] = str(local_path)
            
        if metadata:
            asset_entry["metadata"] = metadata
            
        self.assets.append(asset_entry)
    
    def save_manifest(self, filename: str = "manifest.json"):
        """
        Save the manifest to a JSON file
        
        Args:
            filename: Name of the manifest file (default: manifest.json)
        """
        manifest_path = self.project_dir / filename
        
        manifest_data = {
            "generation_timestamp": self.start_time.isoformat(),
            "completion_timestamp": datetime.now().isoformat(),
            "total_assets": len(self.assets),
            "assets": self.assets
        }
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest_data, f, indent=2)
        
        print(f"\n📋 Manifest saved: {manifest_path}")
        print(f"   Total assets tracked: {len(self.assets)}")
        
        return manifest_path


def convert_svg_to_jpeg(svg_path: Path, jpeg_path: Optional[Path] = None, quality: int = 95) -> Optional[Path]:
    """
    Convert an SVG file to JPEG format.
    
    Process:
    1. Read SVG file
    2. Render SVG to PNG using cairosvg
    3. Convert PNG to JPEG using Pillow
    
    Args:
        svg_path: Path to the source SVG file
        jpeg_path: Path to save the JPEG file (if None, uses same name with .jpeg extension)
        quality: JPEG quality (1-100, default 95 for high quality)
        
    Returns:
        Path to the saved JPEG file if successful, None otherwise
    """
    if not SVG_CONVERSION_AVAILABLE:
        print(f"⚠️  Warning: SVG to JPEG conversion not available. Install cairosvg and Pillow.")
        return None
    
    try:
        # Generate JPEG path if not provided
        if jpeg_path is None:
            jpeg_path = svg_path.with_suffix('.jpeg')
        
        # Read SVG file
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        # Convert SVG to PNG in memory
        png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'))
        
        # Open PNG with Pillow
        with Image.open(io.BytesIO(png_data)) as img:
            # Convert RGBA to RGB if necessary (JPEG doesn't support transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                # Convert palette mode to RGBA first
                if img.mode == 'P':
                    img = img.convert('RGBA')
                # Paste with alpha channel as mask
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save as JPEG
            img.save(jpeg_path, 'JPEG', quality=quality, optimize=True)
        
        return jpeg_path
        
    except Exception as e:
        print(f"⚠️  Warning: Failed to convert SVG to JPEG: {e}")
        return None

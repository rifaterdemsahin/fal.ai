"""
Convert existing PNG illustrations to JPG format
This is a utility script to add JPG versions for existing PNG illustrations.
"""
import os
from pathlib import Path
from PIL import Image

# Configuration
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
ILLUSTRATIONS_DIR = REPO_ROOT / "3_Simulation" / "Feb1Youtube" / "generated_illustrations"

def convert_png_to_jpg(png_path: Path):
    """Convert a PNG file to JPG format with high quality."""
    try:
        jpg_path = png_path.with_suffix(".jpg")
        
        # Skip if JPG already exists
        if jpg_path.exists():
            print(f"   ⚠️ JPG already exists: {jpg_path.name}")
            return
        
        print(f"💾 Converting {png_path.name} to JPG...")
        img = Image.open(png_path)
        
        # Convert to RGB if necessary (JPG doesn't support transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Convert all non-RGB modes to RGBA first for consistent handling
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            # Create RGB image with white background
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1])
            rgb_img.save(jpg_path, 'JPEG', quality=95)
        else:
            img.save(jpg_path, 'JPEG', quality=95)
        
        print(f"   ✓ Saved: {jpg_path.name}")
        return jpg_path
    except Exception as e:
        print(f"   ✗ Error converting {png_path.name}: {e}")
        return None

def main():
    """Convert all PNG files in the illustrations directory to JPG."""
    if not ILLUSTRATIONS_DIR.exists():
        print(f"Error: Illustrations directory not found at {ILLUSTRATIONS_DIR}")
        return
    
    # Find all PNG files (excluding README)
    png_files = [f for f in ILLUSTRATIONS_DIR.glob("*.png")]
    
    if not png_files:
        print("No PNG files found to convert.")
        return
    
    print(f"Found {len(png_files)} PNG files to convert.\n")
    
    converted = 0
    for png_file in sorted(png_files):
        result = convert_png_to_jpg(png_file)
        if result:
            converted += 1
    
    print(f"\n✅ Conversion complete! {converted}/{len(png_files)} files converted to JPG.")

if __name__ == "__main__":
    main()

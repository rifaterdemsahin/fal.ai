# 📄 Output Format Configuration

## Overview

This project now supports automatic conversion of generated images to JPEG format when transparency is not needed, significantly reducing file sizes while maintaining quality.

## Key Features

- **Automatic Format Selection**: Each asset type automatically uses the optimal format
- **Transparency Preservation**: Assets requiring transparency (icons, lower thirds) remain in PNG format
- **File Size Optimization**: Images with solid backgrounds are converted to JPEG (typically 40-60% smaller)
- **High Quality**: JPEG conversion uses quality=95 for minimal quality loss

## Format Configuration

The output format for each asset type is configured in `base/generator_config.py`:

```python
OUTPUT_FORMATS = {
    "image": "jpeg",          # Images with solid backgrounds
    "graphic": "png",         # Graphics may need transparency
    "icon": "png",            # Icons need transparency
    "lower_third": "png",     # Lower thirds need transparency for overlays
    "diagram": "jpeg",        # Diagrams typically have solid backgrounds
    "memory_palace": "jpeg",  # Memory palace images have solid backgrounds
    "chapter_marker": "jpeg", # Chapter markers have solid backgrounds
    # ... other formats
}
```

## Assets Requiring Transparency (PNG)

These assets **MUST** use PNG format to preserve transparency:

### PNG Optimization for DaVinci Resolve

**All PNG files are automatically optimized for DaVinci Resolve compatibility:**

- **32-bit Format**: Converted to RGBA (8-bit per channel RGB + Alpha)
- **No Indexed Colors**: Mode 'P' (palette/indexed) is converted to RGBA
- **No Metadata**: EXIF, XMP, and other metadata removed
- **Automatic**: Happens during the generation process

This ensures PNG files work seamlessly in DaVinci Resolve without "Media Offline" errors.

### Lower Thirds (10 assets)

- All lower thirds are broadcast overlays
- Require transparent backgrounds for video compositing
- Examples: `lt_agentic_era`, `lt_mcp`, `lt_skills_gap`, etc.

### Icons (10 assets)

- Generated with "isolated on white background"
- Need transparency for flexible use in presentations
- Examples: `ferrari_icon`, `shopping_cart_icon`, `database_cylinder`, etc.

### Graphics with Transparency (2 assets)

- `ferrari_cart_morph` - Morphing animation requires transparency
- `state_management_flow` - Overlay graphic with transparent background

## Assets Using JPEG (20+ assets)

These assets use JPEG format for smaller file sizes:

### Images (11+ assets)

- All have solid dark backgrounds
- Examples: `sunday_5pm_timeline`, `agent_workflow_diagram`, `20_dollar_pricing`, etc.
- Typical savings: 40-60% file size reduction

### Diagrams (3+ assets)

- All have solid backgrounds
- Examples: `agentic_workflow_architecture`, `data_flow_process`, etc.

### Memory Palace & Chapter Markers

- Photorealistic or stylized scenes with solid backgrounds
- No transparency requirements

## How It Works

### JPEG Conversion (for non-transparent assets)

1. **Generation**: fal.ai generates images (always returns PNG format initially)
2. **Download**: Image is downloaded from fal.ai
3. **Conversion** (if needed):
   - If `output_format` is "jpeg" and asset type supports it
   - PNG is converted to JPEG with quality=95
   - Transparent pixels are replaced with white background
   - Original PNG is deleted after successful conversion
4. **File Size Reporting**: Console output shows size comparison and savings percentage

### PNG Optimization (for transparent assets)

1. **Generation**: fal.ai generates images in PNG format
2. **Download**: Image is downloaded from fal.ai
3. **Optimization** (automatic for all PNGs):
   - Convert to RGBA mode (32-bit: 8-bit per channel)
   - Remove indexed colors (mode 'P' → RGBA)
   - Strip all metadata (EXIF, XMP, etc.)
   - Ensure DaVinci Resolve compatibility
4. **Console Output**: Shows mode conversion if applied

## Example Output

### JPEG Conversion

```
💾 Downloaded temporary PNG: 001_image_timeline_v1_temp.png
🔄 Converted to JPEG: 001_image_timeline_v1.jpeg
   📦 Size: 1840.2KB (PNG) → 845.3KB (JPEG) - 54.1% smaller
```

### PNG Optimization

```
💾 Asset saved: 001_icon_ferrari_v1.png
🔧 Optimizing PNG for DaVinci Resolve...
   🔄 Converted PNG mode: RGB → RGBA (32-bit)
```

## Usage in Generators

Each generator class specifies its output format during initialization:

```python
class ImageAssetGenerator(BaseAssetGenerator):
    def __init__(self):
        super().__init__(
            output_dir=Path("./generated_assets"),
            seeds=SEEDS,
            brand_colors=BRAND_COLORS,
            asset_type="image",
            output_format=OUTPUT_FORMATS.get("image", "jpeg")  # JPEG for images
        )
```

## Testing

Run the test suite to verify format configuration:

```bash
cd 5_Symbols
python3 test_output_format.py      # Verify format configuration
python3 test_jpeg_conversion.py    # Test JPEG conversion logic
python3 test_png_optimization.py   # Test PNG optimization for DaVinci Resolve
```

## Benefits

1. **Reduced Storage**: 40-60% smaller file sizes for JPEG assets
2. **Faster Downloads**: Smaller files transfer faster
3. **Better Performance**: Video editing software loads smaller files faster
4. **Preserved Quality**: High-quality JPEG (quality=95) maintains visual fidelity
5. **Automatic**: No manual intervention required
6. **DaVinci Resolve Compatible**: All PNG files optimized with 32-bit format and no metadata
7. **No Indexed Colors**: Prevents "Media Offline" errors in DaVinci Resolve

## Transparency Requirements Summary

| Asset Type | Format | Optimization | Reason |
|------------|--------|--------------|--------|
| Lower Thirds | PNG | 32-bit RGBA | Video overlay transparency |
| Icons | PNG | 32-bit RGBA | Flexible use with transparency |
| Graphics (some) | PNG | 32-bit RGBA | Specific transparency needs |
| Images | JPEG | Quality 95 | Solid backgrounds |
| Diagrams | JPEG | Quality 95 | Solid backgrounds |
| Memory Palace | JPEG | Quality 95 | Solid backgrounds |
| Chapter Markers | JPEG | Quality 95 | Solid backgrounds |

**PNG Optimization Details:**

- All PNG files converted to RGBA (32-bit: 8-bit per channel)
- Indexed colors (mode 'P') automatically converted to RGBA
- All metadata stripped for DaVinci Resolve compatibility

## Dependencies

- **Pillow (PIL)**: Required for PNG to JPEG conversion
- Install: `pip install Pillow`

## Configuration Override

To override the format for a specific generator:

```python
generator = ImageAssetGenerator()
generator.output_format = "png"  # Force PNG if needed
```

## Notes

- **JPEG Conversion**:
  - JPEG does not support transparency (alpha channel)
  - Transparent areas in PNG are replaced with white background during conversion
  - For assets requiring transparency, PNG is always used regardless of configuration
  - The conversion is automatic and happens during the generation process

- **PNG Optimization**:
  - All PNG files are automatically converted to 32-bit RGBA format
  - Bit depth is standardized to 8-bit per channel (never auto-detect or indexed)
  - Metadata is completely removed to prevent DaVinci Resolve issues
  - Optimization happens automatically for all PNG files
  - No manual intervention or post-processing required

## 🎬 Usecase in Weekly Artifact Generation

This formula acts as the "Standard Operating Procedure" for file formats delivered to the editor.

- **Role**: format standardization.
- **Input**: Generated assets in memory.
- **Output**: Files saved with the correct extension (.jpg vs .png) and settings (compression, metadata).
- **Benefit**: Balances file quality with storage size (using JPEGs where possible) while preserving necessary technical features (transparency in PNGs), optimizing the "Weekly Inputs" folder for both quality and manageability.

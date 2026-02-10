# 🖼️ SVG to JPEG Conversion

## Overview

All SVG generators in this project now automatically create JPEG versions alongside SVG files. This provides both vector (SVG) and raster (JPEG) formats for maximum compatibility.

## How It Works

When an SVG file is saved, the system automatically:

1. **Renders** the SVG to PNG format using cairosvg
2. **Converts** the PNG to high-quality JPEG using Pillow (quality=95)
3. **Handles transparency** by compositing onto a white background
4. **Saves** the JPEG with the same filename (different extension)

## Example Output

```
generated_svgs/
├── 001_svg_pipeline_overview_v1.svg    (1.8 KB - vector)
├── 001_svg_pipeline_overview_v1.jpeg   (20 KB - raster)
├── 002_svg_workflow_process_v1.svg     (1.7 KB - vector)
└── 002_svg_workflow_process_v1.jpeg    (15 KB - raster)
```

## Dependencies

The conversion requires two additional Python packages:

- **cairosvg** (≥2.7.0) - For SVG to PNG rendering
- **Pillow** (≥10.0.0) - For PNG to JPEG conversion

Both are included in `requirements.txt`.

## Installation

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install cairosvg Pillow
```

## Usage

The conversion happens automatically in all SVG generators:

### BulkSVGGenerator.py

```python
python3 BulkSVGGenerator.py
```

### BatchAssetGeneratorSVG.py

```python
python3 BatchAssetGeneratorSVG.py
```

### SVGGenerator.py

```python
from SVGGenerator import SVGAssetGenerator
generator = SVGAssetGenerator()
generator.run()
```

## Testing

Run the test script to verify conversion:

```bash
cd 5_Symbols
python3 test_svg_jpeg_conversion.py
```

Expected output:

```
🧪 Testing SVG to JPEG Conversion
============================================================
✅ cairosvg and Pillow are installed

Found 10 SVG file(s)

Testing with: 001_svg_pipeline_overview_v1.svg
SVG size: 1821 bytes
✅ JPEG created: 001_svg_pipeline_overview_v1.jpeg
JPEG size: 19604 bytes

📊 Comparison:
   SVG:      1821 bytes (vector)
   JPEG:    19604 bytes (raster)
   Format: JPEG
   Size: (960, 480)
   Mode: RGB

✅ Test passed!
```

## Technical Details

### Conversion Function

The `convert_svg_to_jpeg()` function in `asset_utils.py`:

```python
def convert_svg_to_jpeg(
    svg_path: Path,
    jpeg_path: Optional[Path] = None,
    quality: int = 95
) -> Optional[Path]:
    """
    Convert an SVG file to JPEG format.
    
    Args:
        svg_path: Path to source SVG file
        jpeg_path: Path to save JPEG (defaults to same name, .jpeg extension)
        quality: JPEG quality 1-100 (default: 95)
    
    Returns:
        Path to saved JPEG file, or None if conversion failed
    """
```

### Transparency Handling

SVG files may have transparent backgrounds. During JPEG conversion:

1. **Detect transparency**: Check for RGBA, LA, or P (palette) image modes
2. **Create white background**: Generate solid white RGB image
3. **Composite**: Paste SVG content onto white background using alpha channel as mask
4. **Save**: Export as RGB JPEG (no alpha channel)

### Quality Settings

- **JPEG Quality**: 95 (high quality, minimal compression artifacts)
- **Optimize**: Enabled for better compression without quality loss
- **Mode**: RGB (no transparency support in JPEG)

## Error Handling

If `cairosvg` or `Pillow` are not installed:

- A warning is printed: `⚠️ Warning: SVG to JPEG conversion not available`
- SVG generation continues normally
- No JPEG files are created

This graceful degradation ensures the system works even without the optional conversion feature.

## Benefits

### For Users

- **Compatibility**: JPEG works everywhere (browsers, editors, viewers)
- **Preview**: Easier to preview without SVG support
- **Thumbnails**: Better for thumbnail generation

### For Developers

- **Vector + Raster**: Best of both worlds - scalable SVG + universal JPEG
- **Automation**: No manual conversion needed
- **Consistency**: Same naming convention for both formats

## File Sizes

Typical file sizes for generated diagrams:

| File Type | Size Range | Use Case |
|-----------|-----------|----------|
| SVG | 1-3 KB | Vector editing, scaling, web display |
| JPEG | 13-26 KB | Raster preview, thumbnails, compatibility |

**Note**: JPEG files are larger because they're rasterized at specific dimensions (e.g., 960×480), while SVG files are compact vector definitions.

## Integration with Manifest

Both SVG and JPEG files can be tracked in the manifest system. Currently, only the SVG file is added to the manifest, but you can modify the generators to track both if needed.

## Troubleshooting

### Conversion Not Working

**Problem**: Warning message appears, no JPEG created

**Solution**: Install dependencies

```bash
pip install cairosvg Pillow
```

### Invalid JPEG Files

**Problem**: JPEG files created but won't open

**Solution**: Check cairosvg installation

```bash
python3 -c "import cairosvg; print(cairosvg.__version__)"
```

### Large File Sizes

**Problem**: JPEG files are very large

**Solution**: Adjust quality setting in `asset_utils.py`:

```python
convert_svg_to_jpeg(svg_path, quality=85)  # Lower quality = smaller file
```

## Future Enhancements

Potential improvements:

- [ ] Configurable JPEG quality per generator
- [ ] Optional PNG output (with transparency)
- [ ] Batch conversion of existing SVG files
- [ ] Multiple resolution outputs (thumbnail, standard, high-res)
- [ ] Add JPEG files to manifest tracking
- [ ] WebP format support for modern browsers

## 🎬 Usecase in Weekly Artifact Generation

This formula ensures improved compatibility for vector assets.

- **Role**: Compatibility bridge for vector graphics.
- **Input**: SVG files.
- **Output**: High-quality JPEG rasters.
- **Benefit**: Video editors (like DaVinci Resolve) sometimes struggle with complex SVGs or render them slowly. Converting to high-res JPEGs ensures smooth playback and instant "media online" status during editing, preventing technical slowdowns.

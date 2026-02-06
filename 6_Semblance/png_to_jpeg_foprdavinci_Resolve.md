This is a "settings" problem, not a "text prompt" problem. You cannot fix this by writing "make this DaVinci compatible" in your image description.

To stop this from happening during your bulk generation, you need to change the **API parameters** or **Settings** in `fal.ai`, not the text prompt.

Here is exactly what you need to change in your generation configuration.

### 1. The Fix: Change `output_format` to JPEG (Safest)

DaVinci Resolve loves JPEGs. If you **do not need transparency** (i.e., you don't need a clear background), force the system to generate JPEGs.

**If you are using the fal.ai API (Python/JS):**
Look for the `output_format` parameter in your payload and set it to `jpeg`.

```json
{
  "prompt": "your cool image prompt here",
  "output_format": "jpeg" 
}

```

*Note: Many fal.ai models default to `png` or `webp`. Explicitly setting this to `jpeg` fixes the "Media Offline" issue 100% of the time for opaque images.*

### 2. If You NEED Transparency (PNG)

If you need transparency, you must use PNG, but `fal.ai` sometimes generates PNGs with color profiles (like sRGB chunks or 16-bit depth) that Resolve hates.

**✅ AUTOMATIC SOLUTION (Now Implemented):**
As of the latest update, the pipeline **automatically optimizes all PNG files** for DaVinci Resolve compatibility. Every PNG file is now:

* **Converted to 32-bit format** (RGBA with 8-bit per channel RGB + Alpha)
* **Never uses indexed colors** (mode 'P' which causes issues)
* **Stripped of all metadata** (EXIF, XMP, and other hidden data removed)

This happens automatically when you generate PNG assets (graphics, icons, lower thirds). No manual intervention needed!

**How it works:**
The `optimize_png_for_resolve()` method in `base_asset_generator.py` ensures:

```python
# Automatically applied to all PNG files:
# 1. Converts any mode (P, RGB, L, etc.) to RGBA (32-bit)
# 2. Removes all metadata
# 3. Ensures 8-bit per channel (standard)
```

**If you are using the API/Script manually:**
There is no "DaVinci Mode" in the API, so you have two options for your bulk script:

* **Option A (Prevention):** Ensure your script is not saving the file as `.png` if the URL ends in `.webp`. (Fal.ai often generates WebP files for speed; if you save a WebP file with a `.png` extension, Paint.NET will fix it, but DaVinci will reject it).
* **Option B (Post-Process - NOW BUILT-IN):** The pipeline now includes automatic "washing" of PNG images using the `Pillow` library before they reach DaVinci.

**Python "Washing" Script (Now Automatic in Pipeline):**
This is now handled automatically by the base generator. For reference, here's what it does:

```python
from PIL import Image

# Opens the downloaded PNG
image = Image.open(png_path)

# Force convert to Standard RGBA (32-bit: 8-bit per channel)
# This removes indexed colors, ensures alpha channel, and standardizes format
if image.mode != 'RGBA':
    image = image.convert("RGBA")

# Save cleanly without metadata
image.save(png_path, "PNG", optimize=True, exif=b'')
```

### Summary Check

1. **Don't write** "compatible with video" in your text prompt (it does nothing).
2. **Set `output_format`: "jpeg"`** in your API settings if you don't need transparency.
3. **Check your file extensions:** Ensure you aren't accidentally downloading `image.webp` and naming it `image.png`. DaVinci *hates* that.
4. **✅ PNG files are now automatically optimized** with 32-bit format (RGBA), no indexed colors, and no metadata for DaVinci Resolve compatibility.

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

**If you are using the API/Script:**
There is no "DaVinci Mode" in the API, so you have two options for your bulk script:

* **Option A (Prevention):** Ensure your script is not saving the file as `.png` if the URL ends in `.webp`. (Fal.ai often generates WebP files for speed; if you save a WebP file with a `.png` extension, Paint.NET will fix it, but DaVinci will reject it).
* **Option B (Post-Process):** Since you are bulk generating, add a tiny Python step to your script to "wash" the images using the `Pillow` library before they ever reach DaVinci.

**Python "Washing" Script for your bulk generator:**
Add this to your code. It opens the raw generation and re-saves it as a "dumb" standard PNG that DaVinci accepts.

```python
from PIL import Image
import io

# Assume 'image_data' is the bytes you got from fal.ai
image = Image.open(io.BytesIO(image_data))

# Force convert to Standard RGB (removes weird color profiles/CMYK)
image = image.convert("RGBA") 

# Save cleanly
image.save("clean_for_davinci.png", "PNG")

```

### Summary Check

1. **Don't write** "compatible with video" in your text prompt (it does nothing).
2. **Set `output_format`: "jpeg"`** in your API settings if you don't need transparency.
3. **Check your file extensions:** Ensure you aren't accidentally downloading `image.webp` and naming it `image.png`. DaVinci *hates* that.

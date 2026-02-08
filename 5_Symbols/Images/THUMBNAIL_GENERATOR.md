# 📸 YouTube Thumbnail Generator

## Overview

The `BatchAssetGeneratorThumbnails.py` script generates 3 compelling YouTube thumbnail images based on your video script content. Each thumbnail is designed to capture key themes and appeal to your target audience.

## Features

- ✅ **3 Pre-Designed Thumbnail Variations** - Automatically generates 3 different compelling thumbnails
- ✅ **Script-Based Prompts** - Thumbnail designs are based on actual video script themes
- ✅ **YouTube Optimized** - 1280x720 resolution (16:9 aspect ratio) as recommended by YouTube
- ✅ **Fast Generation** - Uses fal.ai's flux/schnell model for quick results
- ✅ **Professional Quality** - High contrast, eye-catching designs with text overlays
- ✅ **Standardized Naming** - Follows project naming conventions for easy organization

## 3 Thumbnail Themes

### 1. Workflow Automation Dashboard
**Theme:** Managing 240+ autonomous workflows  
**Visual:** Futuristic dashboard with workflow connections, bold text "240+ WORKFLOWS", tech aesthetic

### 2. AI Agent Ecosystem
**Theme:** Bridging the AI skills gap with autonomous agents  
**Visual:** Interconnected AI agent network, vibrant colors, "AI SKILLS GAP" crossed out

### 3. Ferrari vs Grocery Store Metaphor
**Theme:** Using AI properly vs. underutilizing it  
**Visual:** Split-screen comparison, Ferrari at grocery store vs. racing with automation, bold "STOP WASTING AI!"

## Usage

### Quick Start

```bash
# Navigate to the Images directory
cd 5_Symbols/Images

# Run the thumbnail generator
python3 BatchAssetGeneratorThumbnails.py
```

### Prerequisites

1. **API Key**: Set your fal.ai API key
   ```bash
   export FAL_KEY='your-api-key-here'
   ```

2. **Dependencies**: Install required packages
   ```bash
   pip install fal-client python-dotenv
   ```

### Output

The script generates:
- 📸 **3 thumbnail images** (PNG format, 1280x720)
- 📝 **manifest.json** - Complete asset tracking
- 📊 **generation_summary.json** - Generation metrics and results

Files are saved to: `5_Symbols/Images/generated_thumbnails/`

### File Naming Convention

```
001_thumbnail_workflow_automation_dashboard_v1.png
002_thumbnail_ai_agent_ecosystem_v1.png
003_thumbnail_ferrari_vs_grocery_store_metaphor_v1.png
```

## Customization

To customize thumbnails for your video:

1. Open `BatchAssetGeneratorThumbnails.py`
2. Edit the `THUMBNAIL_PROMPTS` list
3. Modify the prompts to match your video themes
4. Run the script

Example prompt structure:
```python
{
    "id": "thumbnail_01",
    "name": "Your Thumbnail Name",
    "scene": 1,
    "prompt": "Detailed visual description with colors, text, style...",
    "description": "Short theme description"
}
```

## Technical Details

- **Model**: `fal-ai/flux/schnell` (fast, high-quality image generation)
- **Resolution**: 1280x720 (YouTube standard)
- **Inference Steps**: 4 (fast generation)
- **Format**: PNG with transparency support

## Integration

The thumbnail generator follows the same patterns as other batch asset generators:

- ✅ Uses `asset_utils.py` for standardized naming
- ✅ Tracks all assets in `manifest.json`
- ✅ Compatible with DaVinci Resolve workflows
- ✅ Can be integrated into `MasterAssetGenerator.py`

## Tips for Great Thumbnails

1. **High Contrast** - Use bold colors and clear text
2. **Emotion** - Show faces or evoke curiosity
3. **Text Overlay** - Keep it short (3-5 words max)
4. **Brand Colors** - Use consistent color palette
5. **Visual Hierarchy** - Make the main point obvious
6. **Test Variations** - Generate multiple options and A/B test

## Example Output

After running the generator:

```
📸 Generating Thumbnail: Workflow Automation Dashboard
   ID: thumbnail_01
   Theme: Captures the core theme of managing 240+ autonomous workflows
⏳ Sending request to fal.ai...
✅ Generated successfully!
💾 Saved: generated_thumbnails/001_thumbnail_workflow_automation_dashboard_v1.png

... (2 more thumbnails) ...

📊 GENERATION SUMMARY
✅ Successful: 3/3
📁 Output directory: /path/to/generated_thumbnails
```

## Troubleshooting

### Missing API Key
```
❌ Error: FAL_KEY environment variable not set
```
**Solution**: Set your API key with `export FAL_KEY='your-key'`

### Import Errors
```
❌ fal_client not installed
```
**Solution**: Run `pip install fal-client python-dotenv`

## Related Files

- `BatchAssetGeneratorImages.py` - General image generation
- `BatchAssetGeneratorGraphics.py` - Graphics and artwork
- `Utils/asset_utils.py` - Naming and manifest utilities

---

**Made with ❤️ using [fal.ai](https://fal.ai) generative AI models**

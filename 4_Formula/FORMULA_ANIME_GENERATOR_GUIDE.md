# 🎬 Bulk Anime Image Generator with Storyline

## Overview

The **Bulk Anime Image Generator** is a specialized asset generator that creates anime-style image scenes based on a structured storyline or script. It's designed to generate multiple anime images in bulk, following a narrative structure with characters, settings, and scene progression.

## Features

- 📖 **Storyline-Based Generation**: Define your entire anime story in a JSON file
- 🎬 **Scene Management**: Automatically generates scenes in sequence with proper naming
- 🎨 **Multiple Model Support**: Choose from fal.ai Flux models (Flux Schnell, Flux Dev, Flux Pro)
- 👥 **Character Tracking**: Keep track of characters appearing in each scene
- 🏞️ **Setting Management**: Define and track different locations/settings
- 📊 **Priority System**: Mark important scenes as HIGH priority
- 📝 **Comprehensive Metadata**: Each scene includes description, mood, camera angle
- 🎞️ **DaVinci Resolve Ready**: Generated files use standardized naming for video editing

## Installation

```bash
# Install required dependencies
pip install fal-client

# Set your fal.ai API key
export FAL_KEY='your-api-key-here'
```

## Quick Start

### 1. Create an Example Storyline

```bash
cd 5_Symbols/Images
python BatchAssetGeneratorAnime.py --create-example
```

This creates `example_anime_storyline.json` with a default story structure.

### 2. Customize Your Storyline

Edit `example_anime_storyline.json` or create your own:

```json
{
  "title": "Your Anime Title",
  "style": "anime",
  "scenes": [
    {
      "id": "1.1",
      "name": "opening_scene",
      "priority": "HIGH",
      "scene": "Scene 1: The Beginning",
      "description": "Your scene description",
      "prompt": "Anime style, detailed prompt for the scene...",
      "characters": ["Hero"],
      "setting": "Starting Location",
      "mood": "excited",
      "camera_angle": "wide shot",
      "image_size": {
        "width": 1920,
        "height": 1080
      }
    }
  ]
}
```

### 3. Generate Your Anime Images

```bash
# Generate with default model (Flux Schnell)
python BatchAssetGeneratorAnime.py --storyline anime_storyline.json

# Generate with high quality model
python BatchAssetGeneratorAnime.py --storyline anime_storyline.json --model flux_dev

# Specify output directory
python BatchAssetGeneratorAnime.py --storyline anime_storyline.json --output ../generated_my_anime
```

## Available Models

| Model | Type | Best For | ID |
|-------|------|----------|-----|
| **Flux Schnell** | Image | Fast anime still images (Default) | `flux_anime` |
| **Flux Dev** | Image | High-quality anime stills | `flux_dev` |
| **Flux Pro** | Image | Professional grade anime art | `flux_pro` |

## Cost Estimation

Anime generation costs vary by model (pricing as of February 2026, subject to change):

- **Flux Schnell**: ~$0.01-0.03 per image
- **Flux Dev**: ~$0.03-0.05 per image
- **Flux Pro**: ~$0.05-0.10 per image

**Example**: A 22-scene storyline with Flux Schnell would cost approximately $0.22-0.66

**Note**: Please verify current pricing at [fal.ai/pricing](https://fal.ai/pricing) as rates may change.

Use the cost estimator:

```bash
cd 5_Symbols/Utils
python EstimateWeeklyVideoCost.py
```

## Advanced Usage

### Custom Scene Types

Extend the generator for specific anime genres:

```python
# Mecha battle scene
{
  "prompt": "Anime mecha battle, giant robot with laser sword fighting enemy mech, explosive combat, city destruction, dynamic camera angles, detailed mechanical design, cinematic action, 16:9",
  "characters": ["Hero Mecha", "Enemy Mecha"],
  "setting": "Destroyed City",
  "scene_type": "mecha_battle"
}

# Magical girl transformation
{
  "prompt": "Magical girl transformation sequence, spinning ribbons of light, costume change, sparkles and stars, pastel colors, detailed transformation animation, elegant poses, 16:9",
  "characters": ["Magical Hero"],
  "setting": "Transformation Space",
  "scene_type": "transformation"
}
```

### Batch Processing Multiple Stories

```bash
# Create a script to process multiple storylines
for story in storylines/*.json; do
  python BatchAssetGeneratorAnime.py --storyline "$story" --output "output/$(basename $story .json)"
done
```

### Integration with DaVinci Resolve

1. Generate your anime scenes
2. Import the entire output folder into DaVinci Resolve
3. Files are pre-sorted by scene number (001, 002, 003...)
4. Reference `manifest.json` for scene descriptions and metadata

## Examples Gallery

See `/3_Simulation/Feb1Youtube/anime_storyline.json` for a complete example with:

- 22 fully-defined scenes
- Character development arc
- Multiple settings and moods
- Detailed prompts and metadata

## Future Enhancements

Potential features for future versions:

- [ ] Character consistency across scenes (face/style matching)
- [ ] Automatic dialogue generation
- [ ] Scene transition effects
- [ ] Music/sound effect integration
- [ ] Multi-language support for prompts
- [ ] Style transfer between scenes
- [ ] Interactive storyline editor

## Support

For issues or questions:

1. Check the main [README.md](../../README.md)
2. Review [Troubleshooting Guide](../../6_Semblance/README.md)
3. Open an issue on GitHub

## 🎬 Usecase in Weekly Artifact Generation

This formula is a key component of the weekly video production pipeline, specifically for creating narrative-driven anime segments.

- **Role**: Generates consistent anime-style scenes from a structured `storyline.json` file.
- **Input**: `anime_storyline.json` located in the weekly input folder (e.g., `3_Simulation/YYYY-MM-DD/input/`).
- **Output**: A series of video or image files in the `generated_anime` output folder, ready for editing.
- **Benefit**: Automates the visualization of complex scripts, ensuring style consistency and reducing manual effort in asset creation.
- **Weekly Workflow**:
    1. Draft the anime script/storyline in the weekly planning phase.
    2. Save as `anime_storyline.json` in the weekly input directory.
    3. Run the generator as part of the `MasterAssetGenerator` pipeline or independently.
    4. Import generated assets into DaVinci Resolve using the provided `manifest.json`.

## License

Part of the fal.ai Weekly Video Creation Pipeline project.

---

**Happy anime creation! 🎌✨**

# Bulk Anime Generator with Storyline

## Overview

The **Bulk Anime Generator** is a specialized asset generator that creates anime-style scenes based on a structured storyline or script. It's designed to generate multiple anime scenes in bulk, following a narrative structure with characters, settings, and scene progression.

## Features

- 📖 **Storyline-Based Generation**: Define your entire anime story in a JSON file
- 🎬 **Scene Management**: Automatically generates scenes in sequence with proper naming
- 🎨 **Multiple Model Support**: Choose from various fal.ai models (Minimax, Kling, Flux)
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
cd 5_Symbols/Video
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
      "duration_seconds": 5,
      "characters": ["Hero"],
      "setting": "Starting Location",
      "mood": "excited",
      "camera_angle": "wide shot"
    }
  ]
}
```

### 3. Generate Your Anime

```bash
# Generate with default model (Minimax video)
python BatchAssetGeneratorAnime.py --storyline anime_storyline.json

# Generate with specific model
python BatchAssetGeneratorAnime.py --storyline anime_storyline.json --model kling

# Specify output directory
python BatchAssetGeneratorAnime.py --storyline anime_storyline.json --output ../generated_my_anime
```

## Storyline Structure

### Required Fields

Each scene in your storyline must include:

- **id**: Unique identifier (e.g., "1.1", "2.1")
- **name**: Scene name for file generation
- **scene**: Scene title/description
- **description**: What happens in this scene
- **prompt**: Detailed prompt for AI generation

### Optional Fields

- **priority**: "HIGH", "MEDIUM", or "LOW" (default: "MEDIUM")
- **duration_seconds**: Video length in seconds (default: 5)
- **characters**: Array of character names appearing in the scene
- **setting**: Location where scene takes place
- **mood**: Emotional tone (e.g., "dramatic", "happy", "tense")
- **camera_angle**: Cinematography note (e.g., "wide shot", "close-up")
- **aspect_ratio**: Video aspect ratio (default: "16:9")
- **image_size**: For image models, e.g., `{"width": 1920, "height": 1080}`
- **num_inference_steps**: For image models (default: 4 for Flux)

## Available Models

| Model | Type | Best For | ID |
|-------|------|----------|-----|
| **Minimax** | Video | General anime video generation | `minimax` |
| **Kling** | Video | High-quality anime video | `kling` |
| **Flux Schnell** | Image | Fast anime still images | `flux_anime` |
| **Flux Dev** | Image | High-quality anime stills | `flux_dev` |

### Model Selection

```bash
# Minimax (default) - Best for video generation
python BatchAssetGeneratorAnime.py --model minimax

# Kling - Higher quality video
python BatchAssetGeneratorAnime.py --model kling

# Flux for still images/storyboards
python BatchAssetGeneratorAnime.py --model flux_anime
```

## Example Storylines

### Action Adventure (Included)

The default storyline `anime_storyline.json` includes:
- **22 scenes** covering a complete hero's journey
- Character development from ordinary person to hero
- Training arc with mentor
- Epic battle with villain
- Emotional resolution

### Custom Story Types

You can create storylines for:

- **Slice of Life**: Daily life, school, relationships
- **Mecha**: Giant robots, sci-fi battles
- **Fantasy**: Magic, monsters, quests
- **Romance**: Character relationships, drama
- **Horror**: Suspense, supernatural elements
- **Sports**: Competition, training, teamwork

## Output Structure

```
generated_anime/
├── 001_anime_opening_scene_v1.mp4
├── 001_anime_opening_scene_v1.json
├── 002_anime_hero_awakening_v1.mp4
├── 002_anime_hero_awakening_v1.json
├── ...
├── generation_summary.json
└── manifest.json
```

### Generated Files

- **Video/Image Files**: The actual generated anime scenes
- **JSON Metadata**: Complete information about each scene
- **generation_summary.json**: Overview of the generation session
- **manifest.json**: DaVinci Resolve import manifest

## Command Line Options

```bash
python BatchAssetGeneratorAnime.py [options]

Options:
  --storyline PATH       Path to storyline JSON file
  --output PATH          Output directory (default: ./generated_anime)
  --model MODEL          Model to use: minimax, kling, flux_anime, flux_dev
  --create-example       Create an example storyline JSON file
  -h, --help            Show help message
```

## Integration with Existing Pipeline

### Using with MasterAssetGenerator

The anime generator can be integrated into the existing asset generation pipeline:

```python
# In your asset generation script
from Video.BatchAssetGeneratorAnime import process_storyline, load_storyline_from_file

# Load your storyline
storyline = load_storyline_from_file("path/to/storyline.json")

# Generate all scenes
results = process_storyline(storyline, output_dir, model="minimax", manifest=manifest_tracker)
```

### Adding to assets_config.json

You can also define anime scenes directly in your `assets_config.json`:

```json
{
  "anime": [
    {
      "id": "1.1",
      "name": "hero_awakening",
      "priority": "HIGH",
      "scene": "Scene 1: Awakening",
      "prompt": "Anime style, hero discovering powers...",
      "model": "fal-ai/minimax/video-01"
    }
  ]
}
```

## Tips for Better Results

### 1. Write Detailed Prompts

```json
// Bad
"prompt": "anime character fighting"

// Good
"prompt": "Anime style, teenage protagonist with blue hair executing dynamic martial arts combo, speed lines, impact effects, urban rooftop setting, sunset lighting, detailed character animation, 16:9 aspect ratio"
```

### 2. Maintain Visual Consistency

- Use consistent character descriptions across scenes
- Reference the same art style (e.g., "studio quality animation")
- Keep color palettes consistent per character/setting

### 3. Scene Composition

- Include camera angle notes: "wide shot", "close-up", "low angle"
- Specify mood/atmosphere: "dramatic lighting", "cheerful atmosphere"
- Add cinematography terms: "depth of field", "motion blur"

### 4. Story Structure

Follow classic anime narrative beats:
1. **Introduction** (1-2 scenes): Establish world and character
2. **Inciting Incident** (2-3 scenes): Problem/conflict appears
3. **Rising Action** (5-8 scenes): Training, preparation, small battles
4. **Climax** (3-5 scenes): Main confrontation/battle
5. **Resolution** (2-3 scenes): Aftermath, character growth
6. **Conclusion** (1-2 scenes): New status quo, teaser

## Troubleshooting

### API Key Issues

```bash
# Verify your API key is set
echo $FAL_KEY

# If not set
export FAL_KEY='your-api-key-here'
```

### Generation Failures

- Check `generation_summary.json` for error details
- Failed scenes can be regenerated individually
- Reduce `num_inference_steps` if generation times out
- Try a different model if one consistently fails

### Quality Issues

- Increase `num_inference_steps` for image models (4 → 28)
- Use more detailed and specific prompts
- Try different models (flux_dev for quality, flux_anime for speed)
- Add specific art style references (e.g., "Studio Ghibli style")

## Cost Estimation

Anime generation costs vary by model (pricing as of February 2026, subject to change):

- **Minimax Video**: ~$0.10-0.20 per 5-second clip
- **Kling Video**: ~$0.15-0.30 per 5-second clip  
- **Flux Image**: ~$0.01-0.05 per image

**Example**: A 22-scene storyline with Minimax would cost approximately $2.20-4.40

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

## License

Part of the fal.ai Weekly Video Creation Pipeline project.

---

**Happy anime creation! 🎌✨**

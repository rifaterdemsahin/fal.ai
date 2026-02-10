# Anime Generator Quick Reference

## Quick Start

```bash
# 1. Install dependencies
pip install fal-client

# 2. Set API key
export FAL_KEY='your-api-key-here'

# 3. Create example storyline
python 5_Symbols/Images/BatchAssetGeneratorAnime.py --create-example

# 4. Generate anime scenes
python 5_Symbols/Images/BatchAssetGeneratorAnime.py --storyline example_anime_storyline.json
```

## Command Line Options

```bash
# Use specific model
python BatchAssetGeneratorAnime.py --storyline story.json --model kling

# Custom output directory
python BatchAssetGeneratorAnime.py --storyline story.json --output /path/to/output

# All options
python BatchAssetGeneratorAnime.py \
  --storyline my_anime.json \
  --output ./my_anime_output \
  --model minimax
```

## Storyline JSON Structure

```json
{
  "title": "Your Anime Title",
  "style": "anime",
  "scenes": [
    {
      "id": "1.1",
      "name": "scene_name",
      "priority": "HIGH",
      "scene": "Scene 1: Description",
      "description": "What happens",
      "prompt": "Detailed prompt for AI generation",
      "duration_seconds": 5,
      "characters": ["Character1", "Character2"],
      "setting": "Location",
      "mood": "dramatic",
      "camera_angle": "wide shot"
    }
  ]
}
```

## Available Models

| Model | Command | Best For |
|-------|---------|----------|
| Minimax (default) | `--model minimax` | General anime video |
| Kling | `--model kling` | High-quality anime video |
| Flux Schnell | `--model flux_anime` | Fast anime stills |
| Flux Dev | `--model flux_dev` | Quality anime stills |

## Output Files

- `001_anime_scene_name_v1.mp4` - Generated video/image
- `001_anime_scene_name_v1.json` - Scene metadata
- `generation_summary.json` - Generation report
- `manifest.json` - DaVinci Resolve manifest

## Examples

### Minimal Scene
```json
{
  "id": "1.1",
  "name": "opening",
  "scene": "Opening Scene",
  "description": "Hero appears",
  "prompt": "Anime style, hero character standing on hill, sunset background"
}
```

### Detailed Scene
```json
{
  "id": "1.1",
  "name": "epic_battle",
  "priority": "HIGH",
  "scene": "Scene 5: Epic Battle",
  "description": "Final showdown between hero and villain",
  "prompt": "Anime style, dynamic battle scene with energy attacks, speed lines, dramatic lighting, cinematic wide shot, 16:9",
  "duration_seconds": 5,
  "characters": ["Hero", "Villain"],
  "setting": "Destroyed City",
  "mood": "intense",
  "camera_angle": "wide action shot",
  "aspect_ratio": "16:9"
}
```

## Tips

1. **Write detailed prompts** - More detail = better results
2. **Mark priorities** - Use HIGH for key scenes
3. **Consistent characters** - Describe characters the same way across scenes
4. **Camera angles** - Specify shots for better composition
5. **Scene flow** - Order scenes logically for story progression

## Testing

```bash
# Run tests
cd 5_Symbols
python Tests/test_anime_generator.py

# Dry run (no API calls)
python Video/BatchAssetGeneratorAnime.py --help
```

## Full Documentation

See [ANIME_GENERATOR_GUIDE.md](./ANIME_GENERATOR_GUIDE.md) for complete documentation.

## Example Storylines

1. **Simple Demo** (5 scenes) - Built-in default
2. **Full Adventure** (22 scenes) - `3_Simulation/Feb1Youtube/anime_storyline.json`

## Troubleshooting

**No API key:**
```bash
export FAL_KEY='your-key-here'
```

**Generation fails:**
- Check `generation_summary.json` for errors
- Try different model with `--model` flag
- Simplify prompt if too complex

**Import errors:**
```bash
pip install fal-client
```

For more help, see the [Troubleshooting Guide](../../6_Semblance/README.md).

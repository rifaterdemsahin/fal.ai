# Weekly Video Production Structure

This document describes the new weekly video production workflow using a clean folder structure.

## Overview

The refactored system uses a standardized weekly folder structure under `3_Simulation/` for organizing inputs and outputs:

```
3_Simulation/
├── 2026-02-10/              # Weekly folder (YYYY-MM-DD format)
│   ├── input/               # Source assets for this week
│   │   ├── assets_config.json    # Configuration for asset generation
│   │   ├── source_edl.md         # Edit decision list
│   │   ├── source_chapter_markers.txt
│   │   └── ...                   # Other source files
│   └── output/              # Generated assets for this week
│       ├── generated_assets_Images/
│       ├── generated_video/
│       ├── generated_music/
│       └── ...
```

## Quick Start

### 1. New Weekly Structure (Recommended)

Use the new structure with explicit weekly ID:

```bash
# Generate assets for a specific week (date-based ID)
python 5_Symbols/MasterAssetGenerator.py --week 2026-02-10
```

Or auto-generate weekly ID from today's date:

```bash
# Use today's date as weekly ID (automatically generates YYYY-MM-DD)
python 5_Symbols/MasterAssetGenerator.py --week auto
# This will use today's date, e.g., if run on Feb 10, 2026, it creates:
# 3_Simulation/2026-02-10/input and 3_Simulation/2026-02-10/output
```

### 2. Legacy Mode (Backward Compatible)

The old way still works for existing projects:

```bash
# Use existing folder structure
python 5_Symbols/MasterAssetGenerator.py ../3_Simulation/Feb1Youtube
```

## Weekly Workflow

### Step 1: Set Up Weekly Folder

Choose your weekly ID (typically the date: `YYYY-MM-DD`):

```bash
# Automatically create the structure
python 5_Symbols/MasterAssetGenerator.py --week 2026-02-10
```

This creates:
- `3_Simulation/2026-02-10/input/`
- `3_Simulation/2026-02-10/output/`

### Step 2: Add Source Assets

Place your source files in the `input/` folder:

```
3_Simulation/2026-02-10/input/
├── assets_config.json           # Required: Asset generation configuration
├── source_edl.md               # Optional: Edit decision list
├── source_chapter_markers.txt  # Optional: Chapter markers
├── clip1.mp4                   # Optional: Source video clips
├── prompts.json                # Optional: Generation prompts
└── ...
```

#### Example `assets_config.json`:

```json
{
  "images": [
    {
      "id": "hero_image_001",
      "prompt": "A futuristic cityscape at sunset, cyberpunk style",
      "model": "fal-ai/flux/dev",
      "seed": 42
    }
  ],
  "video": [
    {
      "id": "broll_city_001",
      "prompt": "Empty city streets, golden hour lighting",
      "model": "fal-ai/minimax/video-01",
      "duration": 5
    }
  ],
  "music": [
    {
      "id": "intro_music",
      "prompt": "Upbeat electronic music, energetic and modern",
      "model": "fal-ai/stable-audio",
      "duration": 30
    }
  ]
}
```

### Step 3: Generate Assets

Run the generator:

```bash
cd 5_Symbols
python MasterAssetGenerator.py --week 2026-02-10
```

The script will:
1. Read configuration from `input/assets_config.json`
2. Show cost estimation
3. Ask for confirmation
4. Generate all assets
5. Save outputs to `output/` folder

### Step 4: Access Generated Assets

All outputs are organized in the `output/` folder:

```
3_Simulation/2026-02-10/output/
├── generated_assets_Images/
│   ├── hero_image_001.jpg
│   └── ...
├── generated_video/
│   ├── broll_city_001.mp4
│   └── ...
├── generated_music/
│   ├── intro_music.wav
│   └── ...
├── generated_chapter_markers/
├── generated_audio/
└── manifest.json              # Complete manifest of all generated assets
```

## Path Configuration Module

The new `paths_config.py` module provides centralized path management:

### Basic Usage

```python
from paths_config import get_weekly_paths

# Get paths for a specific week
paths = get_weekly_paths('2026-02-10')
print(paths['input'])   # 3_Simulation/2026-02-10/input
print(paths['output'])  # 3_Simulation/2026-02-10/output

# Auto-generate from today's date
paths = get_weekly_paths()  # Uses today's date
```

### Creating Structure

```python
from paths_config import ensure_weekly_structure

# Create input/output directories if they don't exist
paths = ensure_weekly_structure('2026-02-10')
# Now paths['input'] and paths['output'] exist
```

### Using in Your Scripts

Update your scripts to use the new paths:

```python
from paths_config import get_weekly_paths
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--week", help="Weekly ID (e.g., 2026-02-10)")
args = parser.parse_args()

# Get paths
paths = get_weekly_paths(args.week)

# Read inputs
input_file = paths['input'] / 'source_data.json'
with open(input_file) as f:
    data = json.load(f)

# Write outputs
output_file = paths['output'] / 'result.mp4'
# ... generate and save to output_file
```

## Benefits of New Structure

1. **Clean Organization**: Separate input sources from generated outputs
2. **Weekly Isolation**: Each week's assets are completely isolated
3. **Easy Archival**: Archive entire weekly folders when done
4. **Clear Workflow**: Input → Process → Output
5. **Version Control**: Easy to track what changed week-to-week
6. **Automation Ready**: Scripts can easily iterate over weeks
7. **Backward Compatible**: Legacy mode still works

## Advanced Usage

### Selective Generation

Generate only specific asset types:

```bash
# The script will prompt for selection
python MasterAssetGenerator.py --week 2026-02-10
# Choose: select
# Enter: images,video
```

### Multiple Weeks

Process multiple weeks in batch:

```bash
for week in 2026-02-10 2026-02-17 2026-02-24; do
  python MasterAssetGenerator.py --week $week
done
```

### Custom Weekly IDs

While `YYYY-MM-DD` is recommended, you can use any ID:

```bash
python MasterAssetGenerator.py --week week_07_2026
python MasterAssetGenerator.py --week Q1_2026_video_01
```

## Troubleshooting

### Config Not Found

```
⚠️ No 'assets_config.json' found in input folder
```

**Solution**: Create `3_Simulation/<weekly_id>/input/assets_config.json`

### Directory Not Found (Legacy Mode)

```
❌ Directory not found: ../3_Simulation/Feb1Youtube
```

**Solution**: Check the path exists or use new mode with `--week`

### Missing Dependencies

```
❌ fal_client not installed
```

**Solution**: Install dependencies:

```bash
pip install -r requirements.txt
```

## Migration Guide

### From Legacy to New Structure

To migrate an existing project:

1. Create new weekly folder:
   ```bash
   mkdir -p 3_Simulation/2026-02-10/input
   mkdir -p 3_Simulation/2026-02-10/output
   ```

2. Copy config to input:
   ```bash
   cp 3_Simulation/Feb1Youtube/assets_config.json \
      3_Simulation/2026-02-10/input/
   ```

3. Copy any source files:
   ```bash
   cp 3_Simulation/Feb1Youtube/_source/* \
      3_Simulation/2026-02-10/input/
   ```

4. Run with new structure:
   ```bash
   python MasterAssetGenerator.py --week 2026-02-10
   ```

## Testing

Run the test suite to verify the setup:

```bash
cd 5_Symbols
python test_path_config.py
```

This validates:
- Path generation
- Directory creation
- Argument parsing
- Config file lookup

## Summary

The refactored weekly structure provides:
- ✅ Clean separation of inputs and outputs
- ✅ Date-based organization
- ✅ Backward compatibility
- ✅ Easy automation
- ✅ Clear workflow

Start using it today with:
```bash
python 5_Symbols/MasterAssetGenerator.py --week auto
```

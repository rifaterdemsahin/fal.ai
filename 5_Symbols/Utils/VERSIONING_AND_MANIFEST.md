# Asset Versioning and Manifest System

## Overview

This document describes the new versioning system and manifest tracking implemented for the fal.ai batch asset generators.

## Features

### 1. Standardized File Naming Convention

All generated assets now follow a consistent naming pattern:

```
{scene_number:03d}_{asset_type}_{clean_description}_v{version}.{extension}
```

**Examples:**
- `001_image_ferrari_cart_morph_v1.png`
- `004_video_uk_streets_sunday_v1.mp4`
- `011_graphic_ai_job_message_v1.png`

**Benefits:**
- Easy to find assets by scene number (zero-padded to 3 digits)
- Clear asset type identification
- Version tracking built into filename
- Clean, alphanumeric descriptions (no special characters)

### 2. Unified Manifest System

Every time the Master Controller runs, it generates a `manifest.json` file that maps:
- Filename → Prompt
- Filename → Timestamp
- Filename → Additional metadata (scene, priority, model, etc.)

**Example manifest.json:**
```json
{
  "generation_timestamp": "2026-02-05T06:18:33.350747",
  "completion_timestamp": "2026-02-05T06:18:33.351119",
  "total_assets": 4,
  "assets": [
    {
      "filename": "001_image_ferrari_cart_morph_v1.png",
      "prompt": "Sleek red Ferrari sports car icon...",
      "timestamp": "2026-02-05T06:18:33.350947",
      "asset_type": "image",
      "asset_id": "1.1",
      "result_url": "https://v3b.fal.media/files/...",
      "local_path": "/path/to/generated_assets_Images/001_image_ferrari_cart_morph_v1.png",
      "metadata": {
        "scene": "Scene 1: Hook",
        "priority": "HIGH",
        "model": "fal-ai/flux/schnell",
        "seed_key": "SEED_003"
      }
    }
  ]
}
```

## Implementation Details

### Core Module: `asset_utils.py`

#### Functions

**`clean_description(description: str) -> str`**
- Cleans a description for use in filenames
- Converts to lowercase, replaces spaces with underscores
- Removes special characters
- Example: `"Ferrari Cart Morph"` → `"ferrari_cart_morph"`

**`generate_filename(scene_number, asset_type, description, version, extension) -> str`**
- Generates standardized filenames
- Zero-pads scene numbers to 3 digits
- Applies clean description rules
- Adds version suffix if provided

**`extract_scene_number(asset_id: str) -> int`**
- Extracts scene number from asset ID (e.g., "1.1" → 1)

#### ManifestTracker Class

**`__init__(project_dir: Path)`**
- Initializes tracker for a specific project directory

**`add_asset(...)`**
- Adds an asset entry to the manifest
- Captures filename, prompt, timestamp, and metadata

**`save_manifest(filename="manifest.json")`**
- Saves the manifest to JSON file
- Includes generation and completion timestamps
- Tracks total asset count

### Updated Batch Generators

All 10 batch generators have been updated:
1. BatchAssetGeneratorImages.py
2. BatchAssetGeneratorLowerThirds.py
3. BatchAssetGeneratorIcons.py
4. BatchAssetGeneratorVideo.py
5. BatchAssetGeneratorMusic.py
6. BatchAssetGeneratorGraphics.py
7. BatchAssetGeneratorDiagrams.py
8. BatchAssetGeneratorMemoryPalace.py
9. BatchAssetGeneratorChapterMarkers.py
10. BatchAssetGeneratorAudio.py (no changes needed - text only)

**Key changes:**
- Accept optional `manifest` parameter in `process_queue()` / `generate_from_file()`
- Accept optional `version` parameter in `generate_asset()`
- Import asset_utils with fallback for standalone operation
- Generate new filenames using standardized convention
- Track each asset in manifest before returning

### Master Controller Integration

**MasterAssetGenerator.py** has been updated to:
1. Import `ManifestTracker` from `asset_utils`
2. Initialize manifest tracker at start of generation
3. Pass manifest to all batch generators
4. Save unified manifest at completion

## Usage

### Running the Master Controller

```bash
cd 5_Symbols
python MasterAssetGenerator.py ../3_Simulation/Feb1Youtube
```

The system will:
1. Load `assets_config.json`
2. Estimate costs
3. Prompt for confirmation
4. Generate all assets with new naming convention
5. Track all assets in manifest
6. Save `manifest.json` in project directory

### Finding Assets

**By Scene Number:**
- All assets from Scene 1: `001_*`
- All assets from Scene 4: `004_*`

**By Asset Type:**
- All images: `*_image_*`
- All videos: `*_video_*`
- All graphics: `*_graphic_*`

**By Version:**
- Version 1: `*_v1.*`
- Version 2: `*_v2.*`

### Querying the Manifest

```python
import json

# Load manifest
with open('manifest.json', 'r') as f:
    manifest = json.load(f)

# Find all assets from Scene 1
scene1_assets = [a for a in manifest['assets'] if a['filename'].startswith('001_')]

# Find all high priority assets
high_priority = [a for a in manifest['assets'] 
                 if a['metadata'].get('priority') == 'HIGH']

# Get prompt for specific file
filename = '001_image_ferrari_cart_morph_v1.png'
asset = next((a for a in manifest['assets'] if a['filename'] == filename), None)
if asset:
    print(f"Prompt: {asset['prompt']}")
```

## Backward Compatibility

The system includes fallback mechanisms:
- If `asset_utils` cannot be imported, generators use legacy naming
- Existing assets with old names remain valid
- Per-directory `generation_summary.json` files are still created

## Testing

### Unit Tests
```bash
cd 5_Symbols
python test_asset_utils.py -v
```

Tests cover:
- Description cleaning
- Filename generation
- Scene number extraction
- Manifest tracking

### Integration Test
```bash
cd 5_Symbols
python test_integration.py
```

Validates:
- Complete workflow from asset definition to manifest
- Filename format verification
- Manifest structure and content

## Benefits

1. **Better Organization**: Scene-based numbering makes assets easy to find
2. **Version Control**: Built-in versioning for asset iterations
3. **Traceability**: Manifest maps every asset to its prompt and metadata
4. **Consistency**: Standardized naming across all asset types
5. **Automation**: No manual tracking needed

## Future Enhancements

Potential improvements:
- Automatic version increment when regenerating existing assets
- Search tool for querying manifest
- Diff tool for comparing manifest versions
- Integration with video editing software via manifest

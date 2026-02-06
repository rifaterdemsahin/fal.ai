# Music Generator for Feb 1 Video

## Overview

This document explains how to run the music generator for the Feb 1 video project. The music generator creates background music tracks using fal.ai's stable-audio model.

## Problem Fixed

The previous music generation attempts failed because the configuration requested tracks of 60-180 seconds, but the fal.ai stable-audio API has a maximum duration limit of **47 seconds** per track.

### Changes Made

1. **Updated MusicGenerator.py** - Changed all `seconds_total` values from 180/60/180 to 47 seconds
2. **Updated BatchAssetGeneratorMusic.py** - Changed all `seconds_total` values from 180/60/180 to 47 seconds
3. **Created run_music_generator_feb1.py** - Convenience script to run the generator with the correct output directory

## Music Tracks to Generate

The generator will create 3 music tracks for the Feb 1 video:

1. **tech_innovation_background** (47 seconds, HIGH priority)
   - Upbeat, tech-focused background track
   - Modern synthesizer, rhythmic, energetic
   - Suitable for technology tutorial video

2. **cta_energy_build** (47 seconds, HIGH priority)
   - High energy, motivational build-up music
   - Cinematic, orchestral hybrid
   - Suitable for call to action

3. **screen_recording_bed** (47 seconds, MEDIUM priority)
   - Subtle background music
   - Sweet, calm, lo-fi beats
   - Suitable for concentration and screen recording demonstration

## Prerequisites

1. **Python 3.8+** installed
2. **fal-client** package installed:
   ```bash
   pip install -r requirements.txt
   ```
3. **FAL_KEY environment variable** set with a valid fal.ai API key

## Getting Your fal.ai API Key

1. Go to [https://fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)
2. Sign up or log in to your account
3. Create a new API key
4. Copy the key for use in the next step

## How to Run

### Option 1: Using the Convenience Script (Recommended)

```bash
# Set your fal.ai API key
export FAL_KEY='your-api-key-here'

# Run the music generator for Feb1Youtube
python3 run_music_generator_feb1.py
```

This will:
- Generate all 3 music tracks
- Save them to `3_Simulation/Feb1Youtube/generated_music/`
- Create a `generation_summary.json` with results

### Option 2: Using the Batch Generator Directly

```bash
# Set your fal.ai API key
export FAL_KEY='your-api-key-here'

# Navigate to the 5_Symbols directory
cd 5_Symbols

# Run the batch generator (will prompt for confirmation)
python3 BatchAssetGeneratorMusic.py
```

**Note:** This will save to `5_Symbols/generated_music/` by default, not the Feb1Youtube folder.

### Option 3: Using the Base Class Generator

```bash
# Set your fal.ai API key
export FAL_KEY='your-api-key-here'

# Navigate to the 5_Symbols directory
cd 5_Symbols

# Run the music generator
python3 MusicGenerator.py
```

## Output

Generated files will be saved to:
```
3_Simulation/Feb1Youtube/generated_music/
├── tech_innovation_background.mp3
├── tech_innovation_background.json
├── cta_energy_build.mp3
├── cta_energy_build.json
├── screen_recording_bed.mp3
├── screen_recording_bed.json
└── generation_summary.json
```

Each `.json` file contains metadata about the generation:
- Prompt used
- Model used
- Duration
- Result URL
- Priority level

## Estimated Cost

Based on fal.ai pricing:
- Stable Audio: ~$0.02 per generation
- **Total for 3 tracks: ~$0.06 USD**

## Troubleshooting

### Error: "FAL_KEY environment variable not set"

**Solution:** Export your API key:
```bash
export FAL_KEY='your-api-key-here'
```

### Error: "Input should be less than or equal to 47"

**Solution:** This error has been fixed in the updated code. The duration is now set to 47 seconds (the maximum allowed).

### Error: "No module named 'fal_client'"

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Music tracks are too short for my video

**Solution:** The 47-second limit is a constraint of the fal.ai stable-audio API. For longer tracks, you have a few options:
1. Generate multiple 47-second tracks and concatenate them in your video editor
2. Loop the generated tracks in your video editor
3. Use a different audio generation service that supports longer durations
4. Use the generated tracks as background loops

## Integration with Video Project

Once generated, the music tracks can be imported into DaVinci Resolve along with other assets from the Feb1Youtube project:

1. Open DaVinci Resolve
2. Navigate to Media Pool → Import Media
3. Select: `3_Simulation/Feb1Youtube/generated_music/`
4. Drag the music tracks to your timeline
5. Adjust volume and timing as needed

## Additional Information

- **Model Used:** `fal-ai/stable-audio`
- **Output Format:** MP3
- **Sample Rate:** Determined by the fal.ai API (typically 44.1kHz)
- **Channels:** Stereo

## See Also

- [Main README](README.md) - Complete project documentation
- [4_Formula/README.md](4_Formula/README.md) - Setup and best practices
- [5_Symbols/README.md](5_Symbols/README.md) - Generator documentation
- [.github/workflows/batch-asset-generator-music.yml](.github/workflows/batch-asset-generator-music.yml) - GitHub Actions workflow

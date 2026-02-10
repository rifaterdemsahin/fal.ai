# Weekly Video Inputs - Quick Start Guide

This guide shows you how to use the new weekly video inputs system with YAML templates and memory palace support.

## Overview

The system now supports:
- ✅ Modular YAML files for each asset type
- ✅ Memory palace visualizations for complex topics
- ✅ Automatic merging of multiple input files
- ✅ Weekly folder structure (YYYY-MM-DD)
- ✅ Backward compatibility with JSON

## Quick Start (5 Minutes)

### 1. Create Your Weekly Folder

```bash
# Navigate to the project root
cd /home/runner/work/fal.ai/fal.ai

# Create this week's folder
WEEK_ID=$(date +%Y-%m-%d)
mkdir -p 3_Simulation/${WEEK_ID}/input
mkdir -p 3_Simulation/${WEEK_ID}/output
```

### 2. Copy Templates

Choose one of these approaches:

#### Option A: Use Master Template (Easiest)
```bash
# Copy the all-in-one template
cp 4_Formula/templates/batch_generation_data.yaml \
   3_Simulation/${WEEK_ID}/input/

# Edit the file with your content
# All asset types are in one file
```

#### Option B: Use Modular Templates (Recommended)
```bash
# Copy only what you need
cp 4_Formula/templates/video_inputs.yaml \
   3_Simulation/${WEEK_ID}/input/

cp 4_Formula/templates/memory_palace_inputs.yaml \
   3_Simulation/${WEEK_ID}/input/

cp 4_Formula/templates/images_inputs.yaml \
   3_Simulation/${WEEK_ID}/input/

# Files will be automatically merged when you run the generator
```

### 3. Customize Your Templates

Edit the YAML files with your specific requirements:

```yaml
# Example: video_inputs.yaml
video:
  - id: "V1.1"
    name: "my_intro_video"
    priority: "HIGH"
    scene: "Scene 1"
    seed_key: "SEED_001"
    prompt: "YOUR CUSTOM PROMPT HERE"
    model: "fal-ai/minimax/video-01"
    duration_seconds: 5
    aspect_ratio: "16:9"
```

### 4. Generate Assets

```bash
cd 5_Symbols

# Generate all assets for your week
python MasterAssetGenerator.py --week ${WEEK_ID}

# Or use 'auto' to automatically use today's date
python MasterAssetGenerator.py --week auto
```

### 5. Review Output

```bash
# Check generated assets
ls -la ../3_Simulation/${WEEK_ID}/output/

# View the manifest
cat ../3_Simulation/${WEEK_ID}/output/manifest.json
```

## Example: Creating a Memory Palace Video

Let's create a video about "Understanding Cloud Computing" with memory palace visualization.

### Step 1: Create the Folder
```bash
WEEK_ID="2026-02-17"
mkdir -p 3_Simulation/${WEEK_ID}/input
mkdir -p 3_Simulation/${WEEK_ID}/output
```

### Step 2: Create Memory Palace YAML

Create `3_Simulation/2026-02-17/input/memory_palace_cloud.yaml`:

```yaml
memory_palace:
  - id: "MP.1"
    name: "cloud_entrance"
    priority: "HIGH"
    scene: "Scene 1"
    seed_key: "SEED_MEMORY"
    prompt: "Grand entrance to a floating palace in the clouds, ethereal bridges connecting sky islands, soft golden light, architectural photography, 8k"
    model: "fal-ai/flux/dev"
    image_size:
      width: 1920
      height: 1080
    num_inference_steps: 30
    memory_location: "entrance"
    concept: "Introduction to Cloud Computing"
    
  - id: "MP.2"
    name: "data_center_hall"
    priority: "HIGH"
    scene: "Scene 2"
    seed_key: "SEED_MEMORY"
    prompt: "Vast hall filled with glowing server racks floating in space, holographic data streams flowing between them, futuristic data center"
    model: "fal-ai/flux/dev"
    image_size:
      width: 1920
      height: 1080
    num_inference_steps: 30
    memory_location: "main_hall"
    concept: "Infrastructure and Data Centers"
    
  - id: "MP.3"
    name: "service_library"
    priority: "HIGH"
    scene: "Scene 3"
    seed_key: "SEED_MEMORY"
    prompt: "Library with shelves containing glowing service cubes labeled AWS, Azure, GCP, floating icons of different cloud services"
    model: "fal-ai/flux/dev"
    image_size:
      width: 1920
      height: 1080
    num_inference_steps: 30
    memory_location: "library"
    concept: "Cloud Service Providers"
```

### Step 3: Create Video B-roll YAML

Create `3_Simulation/2026-02-17/input/video_cloud.yaml`:

```yaml
video:
  - id: "V1.1"
    name: "cloud_intro"
    priority: "HIGH"
    scene: "Scene 1"
    seed_key: "SEED_001"
    prompt: "Cinematic aerial view of server farm facility, modern architecture, twilight sky, high tech"
    model: "fal-ai/minimax/video-01"
    duration_seconds: 5
    aspect_ratio: "16:9"
    
  - id: "V2.1"
    name: "data_flow"
    priority: "HIGH"
    scene: "Scene 2"
    seed_key: "SEED_001"
    prompt: "Abstract visualization of data packets flowing through networks, particles of light, dark background"
    model: "fal-ai/minimax/video-01"
    duration_seconds: 5
    aspect_ratio: "16:9"
```

### Step 4: Generate

```bash
cd 5_Symbols
python MasterAssetGenerator.py --week 2026-02-17
```

The generator will:
1. Load both YAML files
2. Merge them into one configuration
3. Show cost estimate
4. Ask for confirmation
5. Generate all assets
6. Save to `output/` folder

### Step 5: Use in Your Video

The generated memory palace images serve as:
- Visual anchors for each concept
- Transitions between topics
- Memorable reference points for viewers

## Advanced Features

### Selective Generation

Generate only specific asset types:

```bash
# Generate only memory palace
python MasterAssetGenerator.py --week 2026-02-17 --types memory_palace

# Generate video and images only
python MasterAssetGenerator.py --week 2026-02-17 --types video,images
```

### Visual Consistency with Seeds

Use the same seed for related assets:

```yaml
# All memory palace locations use SEED_MEMORY
memory_palace:
  - seed_key: "SEED_MEMORY"  # = 888001
  # ...

# All chapter markers use SEED_CHAPTERS  
chapters:
  - seed_key: "SEED_CHAPTERS"  # = 777001
  # ...
```

### Priority-Based Generation

The system respects priority levels:

```yaml
# HIGH priority assets are generated first
- priority: "HIGH"    # Must have

# MEDIUM priority if you have time/budget
- priority: "MEDIUM"  # Nice to have

# LOW priority can be skipped
- priority: "LOW"     # Optional
```

## File Structure Example

Here's what a complete weekly setup looks like:

```
3_Simulation/2026-02-17/
├── input/
│   ├── video_inputs.yaml           # 3 video clips
│   ├── memory_palace_inputs.yaml   # 6 memory palace locations
│   ├── chapters_inputs.yaml        # 5 chapter markers
│   └── images_inputs.yaml          # 8 supporting images
└── output/
    ├── generated_video/
    │   ├── 01_cloud_intro_V1.1.mp4
    │   └── 02_data_flow_V2.1.mp4
    ├── generated_memory_palace/
    │   ├── 00_cloud_entrance_MP.1.jpg
    │   ├── 00_data_center_hall_MP.2.jpg
    │   └── 00_service_library_MP.3.jpg
    ├── generated_chapter_markers/
    │   └── ...
    ├── generated_assets_Images/
    │   └── ...
    └── manifest.json
```

## Troubleshooting

### No Configuration Files Found

**Error:** `⚠️  No configuration files (.yaml/.yml/.json) found`

**Solution:** 
```bash
# Make sure you have at least one config file
ls 3_Simulation/2026-02-17/input/*.yaml
# Should show your YAML files

# If empty, copy a template
cp 4_Formula/templates/batch_generation_data.yaml \
   3_Simulation/2026-02-17/input/
```

### YAML Syntax Error

**Error:** `❌ Error reading config: ...`

**Solution:** Validate your YAML syntax
```bash
# Test YAML syntax
python3 -c "import yaml; yaml.safe_load(open('3_Simulation/2026-02-17/input/video_inputs.yaml'))"

# Common issues:
# - Wrong indentation (use 2 spaces)
# - Missing colons after keys
# - Unquoted strings with special characters
```

### PyYAML Not Installed

**Error:** `⚠️  PyYAML not installed`

**Solution:**
```bash
pip install PyYAML
# or
pip install -r requirements.txt
```

## Best Practices

1. **Start Small**: Begin with one or two asset types
2. **Use Descriptive Names**: `cloud_intro` not `video1`
3. **Test First**: Generate a few assets before creating a large batch
4. **Consistent Seeds**: Same seed = same visual style
5. **Document Concepts**: Use the `concept` field in memory palace
6. **Version Control**: Keep your input YAMLs in git
7. **Review Manifest**: Check `manifest.json` after generation

## Resources

- **Formula Guide**: `4_Formula/WEEKLY_VIDEO_INPUTS_FORMULA.md`
- **Template Reference**: `4_Formula/templates/README.md`
- **All Templates**: `4_Formula/templates/*.yaml`

## Next Steps

1. ✅ Copy templates to your weekly input folder
2. ✅ Customize prompts for your video topic
3. ✅ Run the generator
4. ✅ Review generated assets
5. ✅ Import to DaVinci Resolve
6. ✅ Create your video!

---

**Questions?** Check the documentation in `4_Formula/` or review the template examples.

**Ready to start?** Run this:
```bash
cd /home/runner/work/fal.ai/fal.ai
cp 4_Formula/templates/batch_generation_data.yaml 3_Simulation/$(date +%Y-%m-%d)/input/
```

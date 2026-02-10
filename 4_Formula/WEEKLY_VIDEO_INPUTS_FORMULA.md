# Weekly Video Inputs Formula

## Overview

This document defines the formula and structure for organizing weekly video production inputs. The system supports modular YAML files for different asset types to enable flexible, scalable video content creation.

## Weekly Structure

Each week follows a standardized directory structure:

```
3_Simulation/
├── YYYY-MM-DD/              # Weekly folder (e.g., 2026-02-10)
│   ├── input/               # All input YAML files
│   │   ├── batch_generation_data.yaml    # Master file (all assets)
│   │   ├── video_inputs.yaml             # Video-specific inputs
│   │   ├── images_inputs.yaml            # Image-specific inputs
│   │   ├── diagrams_inputs.yaml          # Diagram-specific inputs
│   │   ├── memory_palace_inputs.yaml     # Memory palace inputs
│   │   ├── audio_inputs.yaml             # Audio/music inputs
│   │   ├── graphics_inputs.yaml          # Graphics inputs
│   │   └── chapters_inputs.yaml          # Chapter markers inputs
│   └── output/              # Generated assets
│       ├── generated_video/
│       ├── generated_assets_Images/
│       ├── generated_diagrams/
│       ├── generated_memory_palace/
│       ├── generated_audio/
│       └── manifest.json
```

## Asset Types and Their Inputs

### 1. Video Inputs (`video_inputs.yaml`)

Video inputs define B-roll clips, motion graphics, and video content.

**Structure:**
```yaml
video:
  - id: "V1.1"                    # Unique identifier
    name: "intro_broll"           # Descriptive name
    priority: "HIGH"              # HIGH, MEDIUM, LOW
    scene: "Scene 1"              # Associated scene
    seed_key: "SEED_001"          # Consistency seed
    prompt: "..."                 # Generation prompt
    model: "fal-ai/minimax/video-01"  # Model to use
    duration_seconds: 5           # Video duration
    aspect_ratio: "16:9"          # Aspect ratio
    search_query: ""              # Optional search query
```

**Formula Fields:**
- `id`: Pattern `V{scene}.{index}` (e.g., V1.1, V2.3)
- `name`: snake_case descriptive name
- `priority`: HIGH (must have), MEDIUM (nice to have), LOW (optional)
- `seed_key`: References consistency seed for visual coherence
- `duration_seconds`: Standard durations: 3, 5, 10, 15, 30
- `aspect_ratio`: Common ratios: "16:9", "9:16", "1:1", "4:3"

### 2. Memory Palace Inputs (`memory_palace_inputs.yaml`)

Memory palace visualization helps with complex information retention and visual storytelling.

**Structure:**
```yaml
memory_palace:
  - id: "MP.1"                    # Unique identifier
    name: "memory_palace_entrance" # Descriptive name
    priority: "HIGH"              # Priority level
    scene: "Scene 1"              # Associated scene
    seed_key: "SEED_001"          # Consistency seed
    prompt: "..."                 # Generation prompt
    model: "fal-ai/flux/dev"      # Model to use
    image_size:
      width: 1920
      height: 1080
    num_inference_steps: 30
    memory_location: "entrance"   # Location in memory palace
    concept: "Introduction"       # Concept being visualized
```

**Formula Fields:**
- `id`: Pattern `MP.{index}` (e.g., MP.1, MP.2)
- `memory_location`: Position in memory palace (entrance, hallway, room1, etc.)
- `concept`: The idea/topic this location represents
- `seed_key`: Use consistent seeds for architectural coherence

**Memory Palace Principles:**
1. **Sequential Flow**: Locations follow a logical path
2. **Visual Distinctiveness**: Each location is visually unique
3. **Emotional Anchoring**: Strong visual metaphors aid memory
4. **Spatial Consistency**: Maintain architectural logic

### 3. Image Inputs (`images_inputs.yaml`)

**Structure:**
```yaml
images:
  - id: "I1.1"
    name: "hero_image"
    priority: "HIGH"
    scene: "Scene 1"
    seed_key: "SEED_001"
    prompt: "..."
    search_query: ""              # Optional
    model: "fal-ai/flux/schnell"  # or fal-ai/flux/dev
    image_size:
      width: 1920
      height: 1080
    num_inference_steps: 4        # schnell: 4, dev: 28-50
```

### 4. Diagram Inputs (`diagrams_inputs.yaml`)

**Structure:**
```yaml
diagrams:
  - id: "D1.1"
    name: "workflow_diagram"
    priority: "HIGH"
    scene: "Scene 1"
    seed_key: "SEED_001"
    mermaid_content: |
      graph TD
          A[Start] --> B[Process]
          B --> C[End]
    prompt: "..."                 # AI enhancement prompt
    model: "fal-ai/flux/dev"
    image_size:
      width: 1920
      height: 1080
    num_inference_steps: 30
```

### 5. Audio Inputs (`audio_inputs.yaml`)

**Structure:**
```yaml
audio:
  - id: "A1.1"
    name: "background_music"
    priority: "HIGH"
    scene: "Scene 1"
    prompt: "..."
    model: "fal-ai/stable-audio"
    duration_seconds: 30
    
music:
  - id: "M1.1"
    name: "intro_theme"
    priority: "HIGH"
    scene: "Scene 1"
    prompt: "..."
    model: "fal-ai/stable-audio"
    duration_seconds: 15
```

### 6. Graphics Inputs (`graphics_inputs.yaml`)

**Structure:**
```yaml
graphics:
  - id: "G1.1"
    name: "lower_third"
    priority: "HIGH"
    scene: "Scene 1"
    seed_key: "SEED_001"
    prompt: "..."
    model: "fal-ai/flux/dev"
    image_size:
      width: 1920
      height: 1080
    num_inference_steps: 30
```

### 7. Chapter Marker Inputs (`chapters_inputs.yaml`)

**Structure:**
```yaml
chapters:
  - id: "CH_1"
    name: "chapter_1_intro"
    priority: "HIGH"
    scene: "Scene 1"
    seed_key: "SEED_CHAPTERS"
    timestamp: "00:00"            # Timestamp in video
    prompt: "..."
    model: "fal-ai/flux/dev"
    image_size:
      width: 1920
      height: 1080
    num_inference_steps: 28
```

## Master Configuration File

The `batch_generation_data.yaml` can contain all asset types in one file:

```yaml
# Master batch generation configuration
# Includes all asset types for the week

diagrams:
  - id: "D1.1"
    # ... diagram config

images:
  - id: "I1.1"
    # ... image config

video:
  - id: "V1.1"
    # ... video config

memory_palace:
  - id: "MP.1"
    # ... memory palace config

graphics:
  - id: "G1.1"
    # ... graphics config

chapters:
  - id: "CH_1"
    # ... chapter config

audio:
  - id: "A1.1"
    # ... audio config

music:
  - id: "M1.1"
    # ... music config
```

## Naming Conventions

### File Naming
- Weekly folders: `YYYY-MM-DD` (ISO 8601 date format)
- Input files: `{type}_inputs.yaml` (e.g., `video_inputs.yaml`)
- Master file: `batch_generation_data.yaml`

### Asset ID Patterns
- Videos: `V{scene}.{index}` (e.g., V1.1, V2.5)
- Images: `I{scene}.{index}` (e.g., I1.1, I3.2)
- Diagrams: `D{scene}.{index}` (e.g., D1.1, D2.1)
- Memory Palace: `MP.{index}` (e.g., MP.1, MP.10)
- Graphics: `G{scene}.{index}` (e.g., G1.1, G2.3)
- Chapters: `CH_{number}` (e.g., CH_1, CH_10)
- Audio: `A{scene}.{index}` (e.g., A1.1, A2.2)
- Music: `M{scene}.{index}` (e.g., M1.1, M3.1)

### Output File Naming
Generated files follow the pattern:
```
{scene_number:02d}_{name}_{id}.{extension}
```
Examples:
- `01_intro_broll_V1.1.mp4`
- `02_workflow_diagram_D2.1.jpg`
- `00_memory_palace_entrance_MP.1.jpg`

## Seed Key Management

Consistency seeds ensure visual coherence across related assets.

**Seed Categories:**
```yaml
# Define in each input file or globally
SEEDS:
  SEED_001: 555123    # Primary visual style
  SEED_002: 555456    # Secondary visual style
  SEED_CHAPTERS: 777001  # Chapter markers
  SEED_MEMORY: 888001    # Memory palace locations
  SEED_DIAGRAMS: 999001  # Technical diagrams
```

**Usage Patterns:**
- Same scene assets: Use same seed_key for consistency
- Different scenes: Use different seeds for variety
- Special categories: Use dedicated seeds (chapters, memory palace)

## Priority System

**HIGH Priority:**
- Essential for video narrative
- Cannot be omitted
- Generated first

**MEDIUM Priority:**
- Enhances the video
- Can be substituted
- Generated second

**LOW Priority:**
- Nice to have
- Can be skipped if time/budget limited
- Generated last

## Weekly Workflow Formula

### 1. Planning Phase
```bash
# Create weekly folder structure
mkdir -p 3_Simulation/2026-02-17/input
mkdir -p 3_Simulation/2026-02-17/output
```

### 2. Input Creation Phase
- Create `batch_generation_data.yaml` with all assets, OR
- Create separate YAML files per asset type
- Define priorities
- Assign seed keys for consistency
- Write generation prompts

### 3. Generation Phase
```bash
# Generate all assets
cd 5_Symbols
python MasterAssetGenerator.py --week 2026-02-17

# Or generate specific types
python MasterAssetGenerator.py --week 2026-02-17 --types video,memory_palace
```

### 4. Review Phase
- Check `output/manifest.json` for generation summary
- Review generated assets
- Regenerate low-quality assets if needed

### 5. Integration Phase
- Import assets into DaVinci Resolve
- Use standardized naming for timeline organization
- Follow scene numbers for ordering

## Memory Palace Integration Example

**Weekly Video Topic:** "Understanding AI Agents"

**Memory Palace Journey:**
```yaml
memory_palace:
  - id: "MP.1"
    name: "entrance_gate"
    memory_location: "entrance"
    concept: "Introduction to AI"
    prompt: "Grand entrance gate to a futuristic palace..."
    
  - id: "MP.2"
    name: "hallway_of_history"
    memory_location: "hallway"
    concept: "History of AI"
    prompt: "Long hallway with holographic displays of AI history..."
    
  - id: "MP.3"
    name: "room_of_algorithms"
    memory_location: "room1"
    concept: "Core Algorithms"
    prompt: "Circular room with floating mathematical equations..."
    
  - id: "MP.4"
    name: "garden_of_applications"
    memory_location: "garden"
    concept: "Real-world Applications"
    prompt: "Lush garden with AI applications as plants..."
    
  - id: "MP.5"
    name: "observatory_of_future"
    memory_location: "observatory"
    concept: "Future of AI"
    prompt: "Glass observatory overlooking a futuristic cityscape..."
```

Each location visually represents a key concept, creating a memorable journey through the topic.

## Best Practices

### 1. Consistency
- Use the same models for related assets
- Apply consistent seed keys within scenes
- Maintain visual style throughout the week

### 2. Efficiency
- Start with HIGH priority assets
- Use `fal-ai/flux/schnell` for faster iterations
- Batch similar asset types together

### 3. Quality
- Use `fal-ai/flux/dev` for final high-quality outputs
- Increase `num_inference_steps` for better results (28-50)
- Write detailed, specific prompts

### 4. Organization
- Use clear, descriptive names
- Follow ID patterns consistently
- Document special requirements in YAML comments

### 5. Memory Palace Design
- Create a logical spatial flow
- Use strong visual metaphors
- Make each location distinctive
- Connect concepts to locations meaningfully

## Troubleshooting

**Issue: Assets lack visual consistency**
- Solution: Use same `seed_key` for related assets

**Issue: Generation too slow**
- Solution: Start with `fal-ai/flux/schnell`, upgrade to `dev` for finals

**Issue: Memory palace locations feel disconnected**
- Solution: Use consistent architectural seeds and create transition locations

**Issue: Too many assets to manage**
- Solution: Use separate YAML files per type, focus on HIGH priority first

## Summary

This formula provides a structured approach to weekly video production:
- ✅ Organized by week (YYYY-MM-DD)
- ✅ Modular YAML files for each asset type
- ✅ Memory palace integration for complex topics
- ✅ Consistent naming and ID patterns
- ✅ Priority-based generation
- ✅ Visual consistency through seed management

Start creating your weekly video inputs today:
```bash
python 5_Symbols/MasterAssetGenerator.py --week auto
```

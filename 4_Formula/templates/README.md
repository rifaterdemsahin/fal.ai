# YAML Templates for Weekly Video Production

This folder contains templates for organizing and generating weekly video assets.

## Available Templates

### 1. Master Template
**File:** `batch_generation_data.yaml`

A complete template containing all asset types in one file. Use this for:
- Small projects with few assets
- Getting started quickly
- Overview of all asset types

### 2. Individual Asset Type Templates

Use these for modular, organized workflows:

| Template File | Asset Type | Use Case |
|--------------|------------|----------|
| `video_inputs.yaml` | Video clips, B-roll | Video content generation |
| `memory_palace_inputs.yaml` | Memory palace visualizations | Complex topic visualization |
| `images_inputs.yaml` | Photos, illustrations | Static visual content |
| `diagrams_inputs.yaml` | Technical diagrams | System architecture, workflows |
| `graphics_inputs.yaml` | Lower thirds, overlays | Visual elements and graphics |
| `chapters_inputs.yaml` | Chapter markers | Video segmentation |
| `audio_inputs.yaml` | Audio, music | Sound effects and background music |

## How to Use

### Option 1: Use the Master Template

1. Copy `batch_generation_data.yaml` to your weekly input folder:
   ```bash
   cp 4_Formula/templates/batch_generation_data.yaml \
      3_Simulation/2026-02-17/input/
   ```

2. Fill in your asset requirements in all sections

3. Generate assets:
   ```bash
   cd 5_Symbols
   python MasterAssetGenerator.py --week 2026-02-17
   ```

### Option 2: Use Individual Templates (Recommended for Large Projects)

1. Copy only the templates you need:
   ```bash
   # Example: Copy video and memory palace templates
   cp 4_Formula/templates/video_inputs.yaml \
      3_Simulation/2026-02-17/input/
   cp 4_Formula/templates/memory_palace_inputs.yaml \
      3_Simulation/2026-02-17/input/
   ```

2. Fill in each template with your requirements

3. Generate assets for specific types:
   ```bash
   cd 5_Symbols
   python MasterAssetGenerator.py --week 2026-02-17 --types video,memory_palace
   ```

### Option 3: Mix and Match

You can combine approaches:
- Use the master `batch_generation_data.yaml` for most assets
- Create separate files for complex asset types (e.g., `memory_palace_inputs.yaml`)
- The generator will merge all YAML files in the input folder

## Weekly Workflow

### Step 1: Create Weekly Folder
```bash
# Create folder structure for the week
mkdir -p 3_Simulation/2026-02-17/input
mkdir -p 3_Simulation/2026-02-17/output
```

### Step 2: Copy Templates
```bash
# Copy master template OR individual templates
cp 4_Formula/templates/batch_generation_data.yaml \
   3_Simulation/2026-02-17/input/
```

### Step 3: Customize
Edit the YAML file(s) with your specific requirements:
- Update IDs, names, scenes
- Write generation prompts
- Set priorities
- Configure seeds for consistency

### Step 4: Generate
```bash
cd 5_Symbols
python MasterAssetGenerator.py --week 2026-02-17
```

### Step 5: Review
Check generated assets in `3_Simulation/2026-02-17/output/`

## Template Customization

### Seed Keys
Define consistent seeds for visual coherence:
```yaml
# Add at the top of your YAML file
# Seed Key Definitions:
# SEED_001: 555123 (Primary visual style)
# SEED_002: 555456 (Secondary visual style)
# SEED_CHAPTERS: 777001 (Chapter markers)
# SEED_MEMORY: 888001 (Memory palace locations)
# SEED_DIAGRAMS: 999001 (Technical diagrams)
# SEED_GRAPHICS: 666001 (Graphics and overlays)
```

### Priority System
- **HIGH**: Essential, must generate
- **MEDIUM**: Nice to have, generate if time/budget allows
- **LOW**: Optional, skip if constrained

### Model Selection
- `fal-ai/flux/schnell`: Fast (4 steps), good for iterations
- `fal-ai/flux/dev`: High quality (28-50 steps), use for finals
- `fal-ai/minimax/video-01`: Video generation

## Advanced Usage

### Merging Multiple YAML Files

The generator automatically merges multiple YAML files from the input folder:

```bash
# Your input folder structure
3_Simulation/2026-02-17/input/
├── video_inputs.yaml          # Video assets
├── memory_palace_inputs.yaml  # Memory palace
└── chapters_inputs.yaml       # Chapter markers

# All three files will be processed together
```

**Important:** Ensure asset IDs are unique across all files. If the same ID appears in multiple files, both instances will be included in the generation queue. This is useful for adding assets incrementally, but avoid unintended duplicates by using unique IDs (e.g., `V1.1`, `V2.1`, etc.).

### Separate Weekly Configurations

Organize by topic or team:
```
3_Simulation/2026-02-17/input/
├── team_a_assets.yaml
├── team_b_assets.yaml
└── shared_assets.yaml
```

### Version Control

Track changes to your input configurations:
```bash
# Create a new week's config based on previous week
cp 3_Simulation/2026-02-10/input/batch_generation_data.yaml \
   3_Simulation/2026-02-17/input/
# Edit for new week's content
```

## Best Practices

1. **Start with Templates**: Don't start from scratch
2. **Use Descriptive Names**: Clear asset names help in post-production
3. **Consistent Seed Keys**: Same seed = visual consistency
4. **Priority Tagging**: Mark must-haves as HIGH
5. **Document Prompts**: Good prompts = better results
6. **Incremental Generation**: Test with a few assets first
7. **Organize by Scene**: Group related assets together

## Troubleshooting

### Template Not Found
```bash
# Ensure you're in the right directory
cd /home/runner/work/fal.ai/fal.ai
ls 4_Formula/templates/
```

### YAML Syntax Errors
- Use proper indentation (2 spaces)
- Quote strings with special characters
- Validate with: `python -c "import yaml; yaml.safe_load(open('file.yaml'))"`

### Missing Sections
- Not all sections are required
- Include only the asset types you need
- Empty sections will be skipped

## Resources

- **Formula Documentation**: `../WEEKLY_VIDEO_INPUTS_FORMULA.md`
- **Weekly Structure Guide**: `../WEEKLY_STRUCTURE.md`
- **MasterAssetGenerator**: `../../5_Symbols/MasterAssetGenerator.py`

## Quick Reference

| Task | Command |
|------|---------|
| Copy master template | `cp 4_Formula/templates/batch_generation_data.yaml 3_Simulation/YYYY-MM-DD/input/` |
| Copy specific template | `cp 4_Formula/templates/video_inputs.yaml 3_Simulation/YYYY-MM-DD/input/` |
| Generate all assets | `python 5_Symbols/MasterAssetGenerator.py --week YYYY-MM-DD` |
| Generate specific types | `python 5_Symbols/MasterAssetGenerator.py --week YYYY-MM-DD --types video,images` |
| View generated assets | `ls 3_Simulation/YYYY-MM-DD/output/` |

## Examples

See the `../WEEKLY_VIDEO_INPUTS_FORMULA.md` for detailed examples of:
- Memory palace journey design
- Video asset planning
- Chapter marker creation
- Multi-week workflows

---

**Ready to start?** Copy a template and begin creating your weekly video assets!

```bash
# From the project root (e.g., /path/to/your/fal.ai)
cp 4_Formula/templates/batch_generation_data.yaml \
   3_Simulation/$(date +%Y-%m-%d)/input/
```

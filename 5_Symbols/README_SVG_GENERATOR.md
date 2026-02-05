# SVG Batch Asset Generator

This tool generates SVG diagrams programmatically to showcase processes in video scripts. Unlike the other batch asset generators that use fal.ai API, this generator creates pure SVG files using Python's XML capabilities.

## Features

- **Process Flow Diagrams**: Creates flowcharts with boxes and arrows
- **Custom Styling**: Uses brand colors and consistent design
- **Multiple Diagram Types**: Supports flow diagrams, comparisons, and more
- **Metadata Export**: Saves configuration and metadata for each diagram
- **No External APIs**: Generates SVG files locally without API calls
- **New Versioning System**: Follows standardized file naming convention from main branch
- **Manifest Tracking**: Generates manifest.json with all asset metadata

## File Naming Convention

Generated SVG files follow the standardized naming pattern:

```
{scene_number:03d}_svg_{clean_description}_v{version}.svg
```

**Examples:**
- `001_svg_agentic_era_transition_v1.svg`
- `002_svg_workflow_process_v1.svg`
- `003_svg_data_collection_understanding_notification_v1.svg`

The naming convention ensures:
- Easy scene-based organization (zero-padded 3-digit scene numbers)
- Clear asset type identification (`svg`)
- Version tracking built into filename
- Clean, alphanumeric descriptions

## Manifest System

Every generation run creates a `manifest.json` file that maps:
- Filename → Description
- Filename → Timestamp
- Filename → Additional metadata (scene, priority, diagram type, dimensions)

This makes it easy to track and manage all generated SVG assets.

## Usage

```bash
cd /path/to/fal.ai/5_Symbols
python3 BatchAssetGeneratorSVG.py
```

When prompted, type `yes` to proceed with generation.

Generated files will be saved to `../3_Simulation/Feb1Youtube/generated_svgs/`.

## Example Diagrams Included

1. **Agentic Era Transition** - Shows evolution from "Prompts" to "Agents"
2. **Workflow Process** - Basic Input → Process → Output flow
3. **Data Collection → Understanding → Notification** - AI agent process stages
4. **Traditional vs Agentic** - Side-by-side comparison diagram

## Configuration

Edit the `GENERATION_QUEUE` in the script to add or modify diagrams. Each diagram configuration includes:

- `id`: Unique identifier
- `name`: Output filename (without extension)
- `priority`: HIGH, MEDIUM, or LOW
- `scene`: Description of where it's used
- `diagram_type`: flow, comparison, etc.
- `elements`: List of boxes and arrows
- `canvas_width` and `canvas_height`: SVG dimensions
- `background`: Background color

## Element Types

### Box Element
```python
{
    "type": "box",
    "text": "Box Text",  # Use \n for multi-line
    "x": 100,           # X position
    "y": 200,           # Y position
    "width": 200,       # Box width
    "height": 100,      # Box height
    "fill": "#2e2e4e",  # Fill color
    "stroke": "#00d4ff", # Border color
    "text_color": "#ffffff", # Text color
}
```

### Arrow Element
```python
{
    "type": "arrow",
    "x1": 300,          # Start X
    "y1": 250,          # Start Y
    "x2": 500,          # End X
    "y2": 250,          # End Y
    "color": "#00d4ff", # Arrow color
    "label": "Optional Label", # Optional arrow label
}
```

## Output

Generated files are saved to `../3_Simulation/Feb1Youtube/generated_svgs/`:
- `.svg` files - The actual SVG diagrams (with new naming convention)
- `.json` files - Metadata for each diagram
- `generation_summary.json` - Overall generation report
- `manifest.json` - Unified manifest tracking all assets

## Brand Colors

The script uses consistent brand colors defined in `BRAND_COLORS`:

- `primary_dark`: #1a1a2e (Background)
- `accent_blue`: #00d4ff (Primary accent)
- `accent_purple`: #7b2cbf (Secondary accent)
- `secondary_teal`: #00bfa5 (Tertiary accent)
- `highlight_orange`: #ff6b35 (Highlights)
- `text_white`: #ffffff (Text)

## Requirements

- Python 3.6+
- No external dependencies (uses standard library only)

## Example: Creating a New Diagram

Add to `GENERATION_QUEUE`:

```python
{
    "id": "SVG5.1",
    "name": "my_custom_diagram",
    "priority": "HIGH",
    "scene": "My Scene",
    "diagram_type": "flow",
    "elements": [
        {
            "type": "box",
            "text": "Start",
            "x": 50, "y": 100,
            "width": 150, "height": 80,
            "fill": "#2e2e4e",
            "stroke": "#00d4ff",
            "text_color": "#ffffff",
        },
        {
            "type": "arrow",
            "x1": 200, "y1": 140,
            "x2": 300, "y2": 140,
            "color": "#00d4ff",
        },
        {
            "type": "box",
            "text": "End",
            "x": 320, "y": 100,
            "width": 150, "height": 80,
            "fill": "#7b2cbf",
            "stroke": "#00d4ff",
            "text_color": "#ffffff",
        },
    ],
    "canvas_width": 500,
    "canvas_height": 250,
    "background": "#1a1a2e",
}
```

## Similar Tools

This generator follows the same pattern as other generators in the project:
- `5_Symbols/BatchAssetGeneratorImages.py` - Image generation via fal.ai
- `5_Symbols/BatchAssetGeneratorDiagrams.py` - Diagram generation via fal.ai
- `5_Symbols/BatchAssetGeneratorGraphics.py` - Graphics generation via fal.ai

The key difference is that this SVG generator creates vector graphics programmatically without requiring external API calls or credits.

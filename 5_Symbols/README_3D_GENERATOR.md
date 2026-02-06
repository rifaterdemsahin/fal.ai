# 3D Asset Generator - Usage Guide

## Overview

The 3D Asset Generator uses fal.ai's Hunyuan-3D API to generate high-quality 3D models from text descriptions. Models are exported in GLB format (glTF binary), which is widely supported by 3D software, game engines, and web applications.

## Quick Start

### Prerequisites

1. Install dependencies:
   ```bash
   pip install fal-client Pillow
   ```

2. Set up your fal.ai API key:
   ```bash
   export FAL_KEY='your-api-key-here'
   ```

### Generate 3D Models

**Using the Batch Generator:**
```bash
cd 5_Symbols
python3 BatchAssetGenerator3D.py
```

**Using the Individual Generator:**
```bash
cd 5_Symbols
python3 ThreeDGenerator.py
```

## API Details

### Model Information

- **Model Name**: `fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d`
- **API Documentation**: https://fal.ai/models/fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d
- **Output Format**: GLB (glTF Binary)
- **Estimated Cost**: ~$0.10 per 3D model (verify current pricing)

### Response Format

The API returns the 3D model in the following structure:
```json
{
  "model_urls": {
    "glb": {
      "url": "https://..../model.glb",
      "content_type": "model/gltf-binary",
      "file_name": "model.glb"
    },
    "obj": {
      "url": "https://..../model.obj",
      "content_type": "text/plain",
      "file_name": "model.obj"
    }
  }
}
```

## Included 3D Assets

The default generation queue includes:

### High Priority
1. **Shopping Cart** - Modern metallic shopping cart with detailed wheels
2. **Ferrari Sports Car** - Sleek red Ferrari with realistic materials

### Medium Priority
3. **AI Robot Brain** - Futuristic AI brain with neural network connections
4. **Smartphone** - Modern smartphone with notification badge
5. **Workflow Node** - Geometric node for technical diagrams

### Low Priority
6. **Database Cylinder** - Classic database symbol in 3D

## Customization

### Adding New 3D Models

Edit the `GENERATION_QUEUE` in `BatchAssetGenerator3D.py`:

```python
{
    "id": "3d.7",
    "name": "custom_model_name",
    "priority": "HIGH",
    "scene": "Scene X: Description",
    "seed_key": "SEED_001",
    "prompt": (
        "Your detailed 3D model description here. "
        "Include materials, style, and any specific details."
    ),
    "model": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
}
```

### Seed Configuration

Seeds control consistency across generations:

- **SEED_001 (42)**: For B-roll style models that can vary
- **SEED_002 (123456)**: For technical objects requiring consistency
- **SEED_003 (789012)**: For decorative elements with brand consistency

## File Naming Convention

Generated files follow the standardized naming pattern:

```
{scene_number:03d}_3d_{clean_description}_v{version}.glb
```

Examples:
- `001_3d_shopping_cart_v1.glb`
- `001_3d_ferrari_sports_car_v2.glb`
- `003_3d_ai_robot_brain_v1.glb`

## Output Files

Each generation creates:

1. **GLB Model** - `{name}.glb` - The 3D model file
2. **Metadata JSON** - `{name}.json` - Generation metadata including prompt
3. **Manifest** - `manifest_3d.json` - Complete asset tracking

## Using Generated 3D Models

### In Blender
1. File → Import → glTF 2.0 (.glb/.gltf)
2. Select your `.glb` file
3. Model imports with materials and textures

### In Unity
1. Drag `.glb` file into Assets folder
2. Unity automatically imports the model
3. Ready to use in scenes

### In Three.js (Web)
```javascript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('path/to/model.glb', (gltf) => {
  scene.add(gltf.scene);
});
```

### In DaVinci Resolve Fusion

DaVinci Resolve's Fusion page supports direct 3D model import. Use the **3D Model Optimizer** to prepare models:

```bash
# Optimize generated 3D models for Fusion
cd 5_Symbols
python3 Batch3DModelOptimizer.py
```

The optimizer will:
- ✅ Validate 3D model files (GLB, FBX, OBJ, DAE)
- 🔧 Optimize models for Fusion integration
- 📊 Generate metadata and analysis reports
- 💡 Provide Fusion integration tips

**Manual Import in Fusion:**
1. Open DaVinci Resolve → Fusion page
2. File → Import → 3D Model
3. Select optimized model file
4. Add lights and camera nodes
5. Use Merge3D to combine with other elements

**Supported Formats:**
- **FBX**: Best compatibility with animations
- **OBJ**: Basic geometry, limited animation
- **DAE**: COLLADA format with animation support
- **GLB**: Exported from text-to-3D generator

See `Batch3DModelOptimizer.py` for validation and optimization details.

## Testing

Run the test suite to verify everything works:

```bash
cd 5_Symbols

# Test 3D model generation
python3 test_3d_generator.py

# Test 3D model optimization
python3 test_3d_optimizer.py
```

Expected output:
```
# 3D Generator Tests
Ran 10 tests in 0.003s
OK

# 3D Optimizer Tests  
Ran 13 tests in 0.004s
OK
```

## Cost Estimation

Before generation, the batch generator shows:
- Total number of models to generate
- Breakdown by priority (HIGH/MEDIUM/LOW)
- Estimated total cost
- Confirmation prompt

Example:
```
📊 Generation Queue Summary:
   Total 3D models to generate: 6
   • HIGH priority: 2
   • MEDIUM priority: 3
   • LOW priority: 1

⚠️  Estimated cost: ~$0.60 (approx $0.10 per 3D model)

Proceed with generation? (yes/no):
```

## Troubleshooting

### API Key Not Found
```
❌ ERROR: FAL_KEY environment variable not set
```
**Solution**: Set your API key with `export FAL_KEY='your-api-key-here'`

### No GLB URL in Result
```
❌ Error: No GLB model URL in result
```
**Solution**: Check API status and verify your prompt is valid

### Module Not Found
```
❌ fal_client not installed
```
**Solution**: Run `pip install fal-client`

## Best Practices

### Writing Prompts
- Be specific about materials (metallic, glass, wood, etc.)
- Describe the style (realistic, low-poly, stylized)
- Mention any special features (reflective surfaces, transparency)
- Include lighting preferences if needed
- Keep prompts focused and clear

### Model Organization
- Use scene numbers to organize assets
- Set appropriate priorities for generation order
- Use consistent seeds for matching asset sets
- Document custom prompts in comments

### Performance
- The "rapid" version is optimized for speed
- Generation typically takes 30-60 seconds per model
- Process multiple models in batch for efficiency
- Review generated models before committing to large batches

## Additional Resources

- **fal.ai Documentation**: https://fal.ai/docs
- **Hunyuan-3D Model Page**: https://fal.ai/models/fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d
- **GLB Format Specification**: https://www.khronos.org/gltf/
- **Project Documentation**: See `README.md` and `5_Symbols/README.md`

## Support

For issues or questions:
1. Check the [Troubleshooting Guide](../6_Semblance/README.md)
2. Review [API Key Setup](../4_Formula/api_key_setup.md)
3. Open an issue on GitHub

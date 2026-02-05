### 4_Formula - Guides and Best Practices

**Setup Guide**:
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    # OR individual install
    pip install fal-client
    ```
2.  **Configuration**:
    - Ensure your `FAL_KEY` is set in your environment:
      ```bash
      export FAL_KEY="your-api-key-here"
      ```
    - Or add to `.env` file if using `dotenv` loading.

**Running Generators**:
Navigate to the project root and run specific modules:
```bash
# Individual generators
python 5_Symbols/BatchAssetGeneratorVideo.py
python 5_Symbols/BatchAssetGeneratorMusic.py

# Master controller (runs all generators)
cd 5_Symbols
python MasterAssetGenerator.py ../3_Simulation/Feb1Youtube
```

**Versioning System**:
All generated assets follow a standardized naming convention:
```
{scene_number:03d}_{asset_type}_{clean_desc}_v{version}.{ext}

Examples:
- 001_image_ferrari_cart_morph_v1.png
- 004_video_empty_uk_streets_v2.mp4
- 011_icon_ai_brain_network_v1.svg
```

**Manifest Tracking**:
The `manifest.json` file provides complete asset traceability:
```python
import json

# Load manifest
with open('3_Simulation/Feb1Youtube/manifest.json', 'r') as f:
    manifest = json.load(f)

# Find all Scene 1 assets
scene1_assets = [a for a in manifest['assets'] if a['filename'].startswith('001_')]

# Get prompt for specific file
filename = '001_image_ferrari_cart_morph_v1.png'
asset = next(a for a in manifest['assets'] if a['filename'] == filename)
print(f"Prompt: {asset['prompt']}")
print(f"Generated: {asset['timestamp']}")
```

**Best Practices**:
- **Prioritization**: Use the `priority` flag (HIGH, MEDIUM, LOW) in generation queues to manage API costs and time.
- **Metadata**: Check `manifest.json` for complete asset tracking and prompt references.
- **Versioning**: Asset versions are tracked automatically; regenerating an asset should increment the version number.
- **Cool-down**: Scripts include automatic delays to avoid rate limiting; do not remove these for large batches.
- **Testing**: Run unit tests (`test_asset_utils.py`) and integration tests (`test_integration.py`) to verify functionality.
- **Cost Estimation**: Use `EstimateWeeklyVideoCost.py` to calculate expected API costs before generation.

# fal.ai
Generate Video Artifacts

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your fal.ai API key
   # Get your key from: https://fal.ai/dashboard/keys
   ```

3. **Run the batch asset generator**
   ```bash
   # Set the environment variable
   export FAL_KEY="your-api-key-here"
   
   # Run the script
   python BatchAssetGenerator.py
   ```

## What it does

The `BatchAssetGenerator.py` script generates visual assets for "The Agentic Era" project using fal.ai's API. It creates:
- B-roll footage
- Infographics
- Motion graphics
- UI overlays

All assets are saved to the `generated_assets/` directory.

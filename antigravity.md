# Antigravity Master Overview

This file serves as the central documentation for the project structure, configuration, and generation workflows.

## 🔐 Environment & Credentials

The project relies on a `.env` file located at `c:\projects\fal.ai\5_Symbols\.env` for API keys.

**Required Keys:**

- `FAL_KEY`: For image/video generation.
- `GOOGLE_API_KEY`: For Google Custom Search (fallback logic).
- `GOOGLE_CSE_ID`: For Google Custom Search Engine ID.

## 📂 Key Directories

- **Root**: `c:\projects\fal.ai`
- **Simulation Source**: `c:\projects\fal.ai\3_Simulation\Feb1Youtube\_source` (Contains YAML configs)
- **Output Directory**: `c:\projects\fal.ai\3_Simulation\Feb1Youtube`

## ⚙️ Configuration Files

- **Master Config**: `c:\projects\fal.ai\3_Simulation\Feb1Youtube\_source\batch_generation_data.yaml`
  - Defines `images`, `chapters`, `infographics`, etc.

## 🚀 Generation Scripts

These scripts are located in `c:\projects\fal.ai\5_Symbols`:

1. **Images (Illustrations)**:
    - Script: `c:\projects\fal.ai\5_Symbols\Images\BulkIllustrationGenerator.py`
    - Description: Generates illustrations using Google Search -> Image-to-Image (fal-ai/flux/dev), with fallback to Text-to-Image.
    - Output: `c:\projects\fal.ai\3_Simulation\Feb1Youtube`

2. **Chapter Markers**:
    - Script: `c:\projects\fal.ai\5_Symbols\Video\BatchAssetGeneratorChapterMarkers.py`
    - Description: Generates video chapter title cards.

3. **Infographics**:
    - Script: `c:\projects\fal.ai\5_Symbols\Infographics\BatchAssetGeneratorInfographics.py`
    - Description: Generates data visualizations and infographics.

## 📝 Usage Guide

To run a generation cycle:

1. Ensure `.env` in `5_Symbols` is populated.
2. Update `batch_generation_data.yaml` with new prompts/items.
3. Run the appropriate python script.

Example for Illustrations:

```powershell
cd c:\projects\fal.ai\5_Symbols\Images
python BulkIllustrationGenerator.py
```

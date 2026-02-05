# Fal.ai Asset Generator for "The Agentic Era"

This project allows for the batch generation of visual and audio assets for YouTube video production using the [fal.ai](https://fal.ai) API. It specifically targets assets for "The Agentic Era" project.

## 📂 Project Organization

The project is structured into 7 core layers:

*   [**1_Real_Unknown**](./1_Real_Unknown/README.md): Objectives (OKRs) and problem definitions.
*   [**2_Environment**](./2_Environment/README.md): Roadmap and high-level use cases.
*   [**3_Simulation**](./3_Simulation/README.md): Workspace for generated assets and UI interactions.
*   [**4_Formula**](./4_Formula/README.md): Guides, setup instructions, and best practices.
*   [**5_Symbols**](./5_Symbols/README.md): **Core Source Code** - Contains all batch generator Python scripts.
*   [**6_Semblance**](./6_Semblance/README.md): Troubleshooting and error logging.
*   [**7_Testing_known**](./7_Testing_known/README.md): QA validation plans and acceptance criteria.

## 🔧 Core Generators (Files in `5_Symbols/`)

*   **`MasterAssetGenerator.py`**: **Master Controller** - Orchestrates all generators and creates unified manifest.
*   **`BatchAssetGeneratorVideo.py`**: Generates B-roll video clips.
*   **`BatchAssetGeneratorAudio.py`**: Generates background music and sound effects.
*   **`BatchAssetGeneratorImages.py`**: Generates photorealistic images.
*   **`BatchAssetGeneratorIcons.py`**: Generates vector-style icon sets.
*   **`BatchAssetGeneratorLowerThirds.py`**: Generates text overlay graphics.
*   **`BatchAssetGeneratorChapterMarkers.py`**: Generates chapter title cards.
*   **`asset_utils.py`**: Utilities for standardized naming and manifest tracking.

## 📋 Asset Versioning and Manifest System

All batch processes now include:
- **Standardized file naming**: `{scene_number:03d}_{asset_type}_{clean_desc}_v{version}.ext`
- **Unified manifest.json**: Maps filenames to prompts, timestamps, and metadata

For detailed documentation, see [5_Symbols/VERSIONING_AND_MANIFEST.md](./5_Symbols/VERSIONING_AND_MANIFEST.md).

## 🚀 Quick Start

1.  **Install Dependencies**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install fal-client
    ```

2.  **Set API Key**:
    ```bash
    export FAL_KEY="your-api-key-here"
    ```

3.  **Run a Generator**:
    ```bash
    python3 5_Symbols/BatchAssetGeneratorVideo.py
    ```

For detailed instructions, see [4_Formula/README.md](./4_Formula/README.md).

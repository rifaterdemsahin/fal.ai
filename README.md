# Fal.ai Asset Generator for "The Agentic Era"

This project allows for the batch generation of visual and audio assets for YouTube video production using the [fal.ai](https://fal.ai) API. It specifically targets assets for "The Agentic Era" project but can be adapted for other video productions.

## Project Structure

The core generation scripts are located in the `Feb1Youtube/` directory:

*   **`Feb1Youtube/BatchAssetGeneratorGraphics.py`**: Generates high-quality graphic assets, diagrams, and infographics.
*   **`Feb1Youtube/BatchAssetGeneratorImages.py`**: Generates B-roll footage frames and general imagery.
*   **`Feb1Youtube/BatchAssetGeneratorIcons.py`**: Generates consistent icon sets for UI and overlays.
*   **`Feb1Youtube/BatchAssetGeneratorLowerThirds.py`**: Generates lower thirds textual/graphic elements.
*   **`Feb1Youtube/BatchAssetGeneratorChapterMarkers.py`**: Generates still images for video chapter markers.
*   **`Feb1Youtube/BatchAssetGeneratorAudio.py`**: Generates sound effects and audio assets.

Generated assets are saved in respected subdirectories within `Feb1Youtube/` (e.g., `generated_graphics/`, `generated_icons/`).

## Setup

1.  **Prerequisites**:
    *   Python 3 installed.
    *   A fal.ai API Key.

2.  **Environment Setup**:
    It is recommended to use a virtual environment.

    ```bash
    # Create virtual environment
    python3 -m venv .venv

    # Activate it
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install fal-client
    ```

4.  **Configuration**:
    Set your fal.ai API key as an environment variable. You can do this in your session or add it to a `.env` file (if using a tool that loads it).

    ```bash
    export FAL_KEY="your-api-key-here"
    ```

## Usage

Navigate to the `Feb1Youtube` directory (or run from root with adjusted paths) and execute the desired generator script.

**Example: Generating Graphics**

```bash
cd Feb1Youtube
export FAL_KEY="your-api-key-here"
python3 BatchAssetGeneratorGraphics.py
```

Each script contains a `GENERATION_QUEUE` list that defines the assets to be created, including prompts, seeds, and models. Configure these lists within the scripts to customize the output.

## Workflow

For a detailed workflow on how to run and rerun these scripts efficiently, refer to [formula.md](./formula.md).

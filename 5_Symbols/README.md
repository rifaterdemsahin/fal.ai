### 5_Symbols - Core Source Code

This directory contains the operational source code for the project. The scripts are modular agents designed for specific asset generation tasks.

**Core Scripts**:

*   **Video & Animation**:
    *   `BatchAssetGeneratorVideo.py`: Generates video clips using models like `fal-ai/minimax/video-01`. Handles aspect ratios and duration.

*   **Audio**:
    *   `BatchAssetGeneratorAudio.py` / `BatchAssetGeneratorMusic.py`: Generates audio tracks, sound effects, and background music.

*   **Static Graphics**:
    *   `BatchAssetGeneratorImages.py`: General purpose image generation (photorealistic or stylized).
    *   `BatchAssetGeneratorIcons.py`: specialized for vector-style, minimalist icons (often checks for transparency).
    *   `BatchAssetGeneratorGraphics.py`: General graphics utility.

*   **Video Elements**:
    *   `BatchAssetGeneratorLowerThirds.py`: Creates overlay graphics for titling.
    *   `BatchAssetGeneratorChapterMarkers.py`: Creates title cards for video chapters.

**Structure**:
Each script typically follows a standard pattern:
1.  Configuration & Imports.
2.  `GENERATION_QUEUE`: A list of dictionaries defining the assets to build.
3.  `generate_*()` function: Handles the API call to fal.ai.
4.  `main()`: Orchestrates the batch process, error handling, and summary reporting.

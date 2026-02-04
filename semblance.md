# Semblance: Missing Batch Jobs

## Missing: Video Production / B-Roll Generation

Upon scanning the `Feb1Youtube` project modules, the following batch job is missing to complete the video production pipeline:

### 1. **BatchAssetGeneratorVideo.py** (Missing)
The current pipeline generates static assets (Images, Icons, Graphics, Lower Thirds) and Music. However, the EDL calls for **B-roll footage** (e.g., "Empty UK Streets", "Corporate Meeting").

- **Current State**: These assets are handled by `BatchAssetGeneratorImages.py` (producing .png) or marked for "Stock Footage".
- **Recommendation**: Create `BatchAssetGeneratorVideo.py` to utilize fal.ai's video generation models (e.g., `fal-ai/minimax/video-01`, `fal-ai/kling-video`, or `fal-ai/hunyuan-video`) to generate actual video clips (.mp4) instead of static images.

## Pipeline Anomalies

- **`BatchAssetGeneratorAudio.py`**: This file is misnamed. Its current logic parses the EDL to generate **text-based Chapter Markers**, not audio/sound effects. It should be renamed to `BatchAssetGeneratorMarkersExtractor.py` or similar, and a true Audio/SFX generator should be created if needed.
- **`BatchAssetGeneratorMusic.py`**: Exists in the codebase but is missing from `README.md`.

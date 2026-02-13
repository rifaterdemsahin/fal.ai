# Gemini Image Generation Formula

This document outlines the successful formula used to enable and run Google Gemini (Imagen) for image generation within the `BatchAssetGeneratorIcons` system.

## 1. Prerequisites & Environment

The system relies on a valid Google Cloud API key with access to the Generative Language API.

*   **Source**: `.env` file in `5_Symbols/`
*   **Key Name**: `GOOGLE_API_KEY` (or `GEMINIKEY`)
*   **Mapping**: The test script automatically maps `GOOGLE_API_KEY` to `GEMINI_API_KEY` if the latter is missing, as the scripts may look for either.

## 2. Model Discovery

To determine which models were actually available for the provided API key, we used a discovery script.

**Script**: `list_gemini_models.py`

```python
import os
import urllib.request
import json
from pathlib import Path

# ... (Loads .env manually to get key) ...

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        for model in data.get('models', []):
            if 'image' in model['name'] or 'imagen' in model['name']:
                print(f"  Found Image Model: {model['name']}")
except Exception as e:
    print(f"Error: {e}")
```

**Result**: We identified that `models/imagen-3.0-generate-001` (default in code) was NOT available, but **`models/imagen-4.0-generate-001`** WAS available.

## 3. Code Configuration

We updated `5_Symbols/Images/BatchAssetGeneratorIcons.py` to include the verified models in the fallback list.

**File**: `5_Symbols/Images/BatchAssetGeneratorIcons.py`
**Function**: `generate_asset_with_gemini`

```python
    # REST API Fallback (Legacy / Manual)
    models_to_try = [
        "models/imagen-4.0-generate-001",      # <--- ADDED (Newest)
        "models/imagen-4.0-fast-generate-001", # <--- ADDED (Fast)
        "models/imagen-3.0-generate-001",
        "models/image-generation-001",
    ]
```

## 4. Execution Formula

To force generation using Gemini instead of the default provider (fal.ai), you use the `provider` argument.

### A. Via Python Script (Programmatic)

```python
from Images import BatchAssetGeneratorIcons

# ... setup asset_config ...

# Force "gemini" provider
BatchAssetGeneratorIcons.generate_asset(
    asset_config, 
    output_dir, 
    provider="gemini"
)
```

### B. Via Command Line (CLI)

The generator script supports a `--provider` flag.

```bash
python3 5_Symbols/Images/BatchAssetGeneratorIcons.py --provider gemini
```

### C. Via Test Suite

In `7_TestingKnown/Tests/test_icon_generation.py`, we modified the `process_queue` call:

```python
generator.process_queue(
    test_batch, 
    self.output_dir, 
    provider="gemini"  # <--- Forces Gemini generation
)
```

## 5. Validation

The generation was verified by checking the output directory:
*   **File**: `000_icon_test_icon_simple_[timestamp]_gemini_v1.png`
*   **Metadata**: `..._gemini_v1.json` (contains `"provider": "gemini"` and `"model": "models/imagen-4.0-generate-001"`)

## Summary

**Formula = (Valid API Key) + (Correct Model Name in Code) + (Provider Flag = "gemini")**

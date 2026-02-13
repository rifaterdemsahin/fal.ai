# Semblance: Troubleshooting Gemini Icon Generation Failure

## Problem Description
The user attempted to generate icons using the Gemini API as the primary provider (`--provider gemini`). However, the generation failed for all 9 icons.

## Observed Error
The process reported:
```
❌ FAILED GENERATIONS:
   • icon_github: github_logo - All Gemini models failed.
   • ... (for all icons)
```

Within the logs, we saw:
```
   Attempting with REST model: models/image-generation-001
   ❌ Model models/image-generation-001 not found.
```
and
```
   Attempting with REST model: models/imagen-3.0-generate-001
   ❌ Model models/imagen-3.0-generate-001 not found.
```

## Root Cause Analysis
1. **Missing SDK**: The `google-genai` Python SDK (v1.0+) was not installed or importable, causing the code to fall back to the raw REST API implementation.
   `ModuleNotFoundError: No module named 'google.genai'` (implied by the fallback code execution path)

2. **REST API Endpoint/Model Name Mismatch**: The REST fallback attempted to access models via:
   `https://generativelanguage.googleapis.com/v1beta/models/image-generation-001:predict`
   `https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict`

   These specific model endpoints are either:
   - Not accessible with the provided API key (permissions scope).
   - Deprecated or incorrect names for the public `generativelanguage` API. The public API often exposes text models (gemini-pro) more readily than image generation endpoints without specific allowlisting or project configuration in Google Cloud Console.

3. **Fallback Logic**: The script correctly identified the `google-genai` import failure and attempted the REST fallback, but the fallback URLs/Methods were not successful.

## Verification of Fix (Workaround)
We switched the provider to `fal` (`--provider fal`) while keeping the Gemini API strictly for **prompt enhancement** and **color injection**.

Command used:
```bash
python3 5_Symbols/Images/BatchAssetGeneratorIcons.py --input 3_Simulation/2026-02-15/input/icons.json --output 7_TestingKnown/TestOutput/generated_icons --provider fal
```

This approach:
1. Uses Gemini (via `enhance_prompt` which relies on the working text-generation model `gemini-2.0-flash`) to rewrite prompts and inject the color palette.
2. Uses Fal.ai (`flux/dev`) to generate the actual high-quality images.

## Solution Implemented
- Updated `BatchAssetGeneratorIcons.py` to import `enhance_prompt` correctly.
- Updated `generate_asset` to inject `BRAND_COLORS` into the prompt *before* enhancement.
- Switched execution to use Fal.ai for image generation, leveraging Gemini for improved prompt adherence to brand guidelines.

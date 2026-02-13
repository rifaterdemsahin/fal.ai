# No-Credits Handling Feature

## Overview

This feature ensures that when your fal.ai credits are exhausted during batch generation, the system gracefully handles the situation by automatically switching to a "dry-run" mode. Instead of stopping completely, it continues to display enhanced prompts and estimated costs for the remaining assets, giving you valuable information even without credits.

## Problem Statement

Previously, when fal.ai credits were exhausted during batch asset generation:
- The generation process would fail with an error
- Users would lose track of what assets they wanted to generate
- No information about prompts or costs was provided for remaining items
- Users had to manually track which assets were generated

## Solution

The new no-credits handling feature provides:

1. **Automatic Credit Error Detection**: Recognizes when the fal.ai API returns credit/balance errors
2. **Graceful Degradation**: Automatically switches to dry-run mode for remaining assets
3. **Prompt Display**: Shows enhanced prompts for all remaining items
4. **Cost Estimation**: Displays estimated costs for each asset
5. **Clear Guidance**: Provides links to the billing dashboard to top up

## Key Features

### 1. Credit Error Detection

The system automatically detects various credit-related error messages:
- "exhausted balance"
- "insufficient credits"
- "user is locked"
- "top up your balance"
- And other similar messages

### 2. Dry-Run Mode

A new mode that allows you to:
- Preview what will be generated without making API calls
- See enhanced prompts (if Gemini API is available)
- Estimate total costs before generation
- Plan your generation strategy

### 3. Automatic Fallback

When credits are exhausted:
1. The error is detected during API call
2. System automatically sets `credits_exhausted` flag
3. Remaining assets are processed in dry-run mode
4. Prompts and costs are displayed for each asset
5. Summary includes both successful generations and dry-run items

## Usage

### Using Dry-Run Mode Explicitly

```python
from base.base_asset_generator import BaseAssetGenerator
from base.generator_config import SEEDS, BRAND_COLORS

# Initialize generator with dry_run=True
generator = YourGenerator(
    output_dir=output_path,
    seeds=SEEDS,
    brand_colors=BRAND_COLORS,
    asset_type="image",
    dry_run=True  # Enable dry-run mode
)

# Process queue - no API calls will be made
results = generator.process_queue()
```

### Automatic Credit Handling

The system automatically handles credit errors:

```python
# Normal initialization
generator = YourGenerator(
    output_dir=output_path,
    seeds=SEEDS,
    brand_colors=BRAND_COLORS,
    asset_type="image"
)

# Process queue
results = generator.process_queue()

# If credits run out during processing:
# 1. Error is caught and detected
# 2. Remaining assets are processed in dry-run mode
# 3. All prompts and costs are displayed
```

## Output

### When Credits Are Available

```
============================================================
🎨 Generating image: futuristic_city
   Scene: 1
   Priority: HIGH
============================================================

📝 Prompt: A futuristic cityscape with flying cars and neon lights
💰 Estimated Cost: $0.05
🔧 Model: fal-ai/flux/dev
⏳ Sending request to fal.ai...
✅ Generated successfully!
   URL: https://fal.ai/...
```

### When Credits Are Exhausted

```
============================================================
🎨 Generating image: futuristic_city
   Scene: 1
   Priority: HIGH
============================================================

📝 Prompt: A futuristic cityscape with flying cars and neon lights
💰 Estimated Cost: $0.05
🔧 Model: fal-ai/flux/dev

💳 NO CREDITS AVAILABLE - Displaying prompt and cost only
   Top up your balance at: https://fal.ai/dashboard/billing
```

### Summary Output

```
================================================================================
📊 GENERATION SUMMARY
================================================================================

✅ Successful: 2/5
❌ Failed: 3/5

✅ SUCCESSFUL GENERATIONS:
   • 1.0: asset_one (HIGH)
   • 2.0: asset_two (MEDIUM)

📝 DRY-RUN / NO CREDITS (Prompt & Cost Displayed):
   • 3.0: asset_three - $0.05
     Prompt: A beautiful mountain landscape at sunset with reflective lake...
   • 4.0: asset_four - $0.01
     Prompt: Abstract geometric patterns with vibrant colors and dynamic...
   • 5.0: asset_five - $0.05
     Prompt: Futuristic robot assistant with holographic display panels...
```

## Benefits

1. **Never Lose Progress**: Even without credits, you can see what was planned
2. **Cost Awareness**: Understand how much you need to top up
3. **Enhanced Prompts**: View Gemini-enhanced prompts without spending credits
4. **Planning**: Use dry-run mode to plan before spending any credits
5. **Graceful UX**: No abrupt failures or lost information

## Implementation Details

### Core Changes

**File: `5_Symbols/base/base_asset_generator.py`**

1. Added `dry_run` parameter to `__init__` method
2. Added `credits_exhausted` flag to track credit state
3. Added `is_credit_error()` method to detect credit errors
4. Updated `generate_asset()` to:
   - Display prompt and cost information
   - Skip API calls in dry-run mode
   - Detect credit errors and switch to dry-run
5. Updated `process_queue()` to:
   - Categorize dry-run items separately
   - Include dry-run stats in summary

### Test Coverage

**File: `7_TestingKnown/Tests/test_no_credits_handling.py`**

- Test credit error detection
- Test dry-run mode functionality
- Test credits exhausted behavior
- Test cost information in results
- Test automatic switching to dry-run on credit error

All tests passing ✅

## Examples

### Example 1: Planning a Batch

```bash
# Run in dry-run mode first to see all prompts and costs
python3 demo_no_credits_handling.py

# Review the output
# Decide if you want to proceed
# Top up credits if needed
# Run actual generation
```

### Example 2: Recovery from Credit Exhaustion

```python
# Batch generation starts normally
# After 5 assets, credits run out
# System detects error automatically
# Remaining 10 assets display prompts and costs
# User sees everything that was planned
# User tops up credits
# User can re-run just the failed assets
```

## Configuration

### Model Pricing

Costs are defined in `5_Symbols/base/generator_config.py`:

```python
MODEL_PRICING = {
    "fal-ai/minimax/video-01": 0.50,
    "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d": 0.45,
    "fal-ai/flux/dev": 0.05,
    "fal-ai/flux/schnell": 0.01,
    "beatoven/music-generation": 0.05,
    "fal-ai/aura-sr": 0.02,
}
```

### Cost Threshold

Expensive generations (>$0.20) are automatically skipped:

```python
COST_THRESHOLD = 0.20
```

## Testing

### Run Unit Tests

```bash
cd /home/runner/work/fal.ai/fal.ai
python3 7_TestingKnown/Tests/test_no_credits_handling.py
```

### Run Demo

```bash
cd /home/runner/work/fal.ai/fal.ai
python3 demo_no_credits_handling.py
```

## Future Enhancements

Potential improvements for future versions:

1. **Batch Cost Estimation**: Show total estimated cost before starting
2. **Credit Balance Check**: Query current balance before generation
3. **Resume Capability**: Automatically resume from where it stopped
4. **Budget Limits**: Set per-batch budget limits
5. **Email Notifications**: Alert when credits are low
6. **Cost Tracking**: Track cumulative costs across sessions

## Related Documentation

- [Cost Confirmation Implementation](./COST_CONFIRMATION_IMPLEMENTATION.md)
- [Base Asset Generator](./5_Symbols/base/base_asset_generator.py)
- [Generator Configuration](./5_Symbols/base/generator_config.py)

## Support

If you encounter issues:
1. Check that you have the latest code
2. Verify your fal.ai API key is set correctly
3. Review the test cases for examples
4. Run the demo script to see expected behavior

For questions or issues, please open a GitHub issue.

# Video Generation - 2026-02-15

## Overview
This directory contains video generation configuration with a **$2.00 budget limit**.

## Directory Structure
```
2026-02-15/
├── input/
│   └── batch_generation_data.yaml    # Video generation queue
└── output/
    └── generated_video/               # Generated videos will be saved here
```

## Setup Instructions

### 1. Install Dependencies
```bash
# Install required Python packages
pip3 install --user PyYAML fal-client python-dotenv Pillow
```

### 2. Set API Key
```bash
# Set your fal.ai API key
export FAL_KEY='your-api-key-here'

# Or add to .env file in project root
echo "FAL_KEY=your-api-key-here" >> /Users/rifaterdemsahin/projects/fal.ai/.env
```

### 3. Configure Videos
Edit `input/batch_generation_data.yaml` to add/modify videos:
- Each video costs approximately $0.25
- Budget limit: $2.00 (max ~8 videos)
- The script will warn if cost exceeds budget

## Running Video Generation

```bash
cd /Users/rifaterdemsahin/projects/fal.ai/5_Symbols/Video
python3 BatchAssetGeneratorVideo.py
```

## Budget Controls

The script includes automatic budget protection:
- **Maximum Total Cost**: $2.00
- **Estimated Cost Per Video**: $0.25
- **Pre-generation Warning**: If queue exceeds budget
- **Runtime Tracking**: Monitors spending during generation
- **Auto-stop Option**: Can halt before exceeding budget

## Current Configuration

**Videos in Queue**: 3
- V_01: agentic_workflows_overview (HIGH)
- V_02: automation_in_action (HIGH)
- V_03: cloud_infrastructure (MEDIUM)

**Estimated Cost**: $0.75 (well within $2.00 budget)

## Output Files

After generation:
```
output/generated_video/
├── 001_0_video_agentic_workflows_overview_v1.mp4
├── 001_0_video_agentic_workflows_overview_v1.json
├── 002_0_video_automation_in_action_v1.mp4
├── 002_0_video_automation_in_action_v1.json
├── 003_0_video_cloud_infrastructure_v1.mp4
├── 003_0_video_cloud_infrastructure_v1.json
└── generation_summary.json
```

## Notes

- Video generation takes 2-3 minutes per clip
- 5-second cooldown between requests
- All costs are estimates; actual costs may vary
- Check fal.ai dashboard for actual usage

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
- **Simulation Source**: `c:\projects\fal.ai\3_Simulation\2026-02-15\_source` (Contains YAML configs)
- **Output Directory**: `c:\projects\fal.ai\3_Simulation\2026-02-15\output` (Latest exact date folder)

## ⚙️ Configuration Files

- **Master Config**: `c:\projects\fal.ai\3_Simulation\2026-02-15\input\batch_generation_data.yaml`
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

## 📂 Naming Conventions

- **Top-Level Directories**: `Number_PascalCase` (e.g., `5_Symbols`)
- **Sub-Directories**: `PascalCase` (e.g., `Audio`, `Images`)
- **Python Scripts (Entry Points)**: `PascalCase.py` (e.g., `MasterAssetGenerator.py`)
- **Python Modules/Utils**: `snake_case.py` (e.g., `paths_config.py`)
- **Configuration/Data**: `snake_case` (e.g., `batch_generation_data.yaml`)
- **Documentation**: `snake_case.md` (except `README.md` and `SCREAMING_SNAKE_CASE.md` for major protocols)

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


---

# Deliver Pilot Structure

📁 fal.ai/
├── 🎯 1_Real_Unknown/        Objectives (OKRs) and problem definitions
├── 🌍 2_Environment/          Roadmap, tech stack, and use cases
├── 🎨 3_Simulation/           Workspace for generated assets and CLI interactions
├── 📖 4_Formula/              Setup guides, best practices, and documentation
├── 💻 5_Symbols/              Core source code - All batch generators live here
├── 🔧 6_Semblance/            Troubleshooting guides and error solutions
└── ✅ 7_Testing_known/        QA validation plans and acceptance criteria

## Delivery Pilot Folder Structure Rationale

The 7-layer architecture provides clear separation of concerns:

### 1_Real_Unknown (🎯 Objectives)
- **Purpose**: Defines the problem space and project objectives
- **Why**: Captures the "unknown" requirements we're solving for
- **Path Example**: `c:\projects\fal.ai\1_RealUnknown\README.md`
- **Usage**: Start here to understand project goals and KPIs

### 2_Environment (🌍 Technical Stack)
- **Purpose**: Documents technical environment, setup procedures, and roadmap
- **Why**: Central hub for all environment configurations and platform-specific setup
- **Path Example**: `c:\projects\fal.ai\2_Environment\SETUP_LINUX.md`
- **Usage**: Reference when setting up development environments

### 3_Simulation (🎨 Workspace)
- **Purpose**: Active workspace for asset generation and outputs
- **Why**: Isolates generated content from source code
- **Path Example**: `c:\projects\fal.ai\3_Simulation\2026-02-15\output`
- **Usage**: All generated assets are stored here with date-based folders

### 4_Formula (📖 Documentation)
- **Purpose**: Complete documentation of workflows, formulas, and best practices
- **Why**: Single source of truth for how to use the system
- **Path Example**: `c:\projects\fal.ai\4_Formula\FORMULA_QUICK_START_GUIDE.md`
- **Usage**: Read before implementing new features or workflows

### 5_Symbols (💻 Core Code)
- **Purpose**: All executable source code and generators
- **Why**: Separates implementation from documentation and data
- **Path Example**: `c:\projects\fal.ai\5_Symbols\MasterAssetGenerator.py`
- **Usage**: Main codebase - all Python generators live here

### 6_Semblance (🔧 Troubleshooting)
- **Purpose**: Error solutions, debugging guides, and known issues
- **Why**: Captures tribal knowledge about common problems
- **Path Example**: `c:\projects\fal.ai\6_Semblance\README.md`
- **Usage**: First stop when encountering errors or unexpected behavior

### 7_Testing_Known (✅ QA)
- **Purpose**: Test suites, validation scripts, and acceptance criteria
- **Why**: Ensures quality and validates that known requirements work
- **Path Example**: `c:\projects\fal.ai\7_TestingKnown\Tests\test_asset_utils.py`
- **Usage**: Run tests before committing changes

This structure mirrors the software development lifecycle: Unknown → Environment → Simulation → Formula → Symbols (Code) → Semblance (Debug) → Testing (Validate)

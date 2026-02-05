# 🎬 Fal.ai Asset Generator for "The Agentic Era"

> 🤖 **Automated multimedia asset generation for YouTube video production using AI**

This project provides a comprehensive suite of Python batch generators that leverage the [fal.ai](https://fal.ai) API to create high-quality visual and audio assets for "The Agentic Era" video project. Generate everything from B-roll footage to icons, music, and chapter markers—all automated and production-ready.

---

## 📂 Project Organization

The project follows a 7-layer architecture for clear separation of concerns:

```
📁 fal.ai/
├── 🎯 1_Real_Unknown/        Objectives (OKRs) and problem definitions
├── 🌍 2_Environment/          Roadmap, tech stack, and use cases
├── 🎨 3_Simulation/           Workspace for generated assets and CLI interactions
├── 📖 4_Formula/              Setup guides, best practices, and documentation
├── 💻 5_Symbols/              Core source code - All batch generators live here
├── 🔧 6_Semblance/            Troubleshooting guides and error solutions
└── ✅ 7_Testing_known/        QA validation plans and acceptance criteria
```

### 📚 Directory Details

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| **[1_Real_Unknown](./1_Real_Unknown/README.md)** | 🎯 Objectives and Key Results | `README.md` - Project goals and KPIs |
| **[2_Environment](./2_Environment/README.md)** | 🌍 Technical Environment | `README.md` - Roadmap, tech stack, Python 3.x |
| **[3_Simulation](./3_Simulation/README.md)** | 🎨 Asset Workspace | `Feb1Youtube/` - Generated assets output |
| **[4_Formula](./4_Formula/README.md)** | 📖 Setup & Best Practices | `formula.md`, `README.md` - Usage guides |
| **[5_Symbols](./5_Symbols/README.md)** | 💻 **Core Generators** | All `.py` scripts - Main codebase |
| **[6_Semblance](./6_Semblance/README.md)** | 🔧 Troubleshooting | `README.md` - Common errors and fixes |
| **[7_Testing_known](./7_Testing_known/README.md)** | ✅ Quality Assurance | `README.md` - Validation strategies |

---

## 🎨 Core Asset Generators

All generators are located in the `5_Symbols/` directory and follow a consistent batch-processing pattern.

### 🎮 Master Controller

| Generator | Description | Output |
|-----------|-------------|--------|
| 🎛️ **`MasterAssetGenerator.py`** | Orchestrates all generators, creates unified manifest | `manifest.json` with complete asset tracking |

### 🎥 Video & Animation

| Generator | Description | Models Used |
|-----------|-------------|-------------|
| 🎬 **`BatchAssetGeneratorVideo.py`** | B-roll video clips (1080p/4k) | `fal-ai/minimax/video-01` |
| 🎞️ **`BatchAssetGeneratorChapterMarkers.py`** | Chapter title cards | Image generation models |

### 🎵 Audio Assets

| Generator | Description | Models Used |
|-----------|-------------|-------------|
| 🎵 **`BatchAssetGeneratorMusic.py`** | Background music tracks | Audio generation models |
| 🔊 **`BatchAssetGeneratorAudio.py`** | Sound effects and audio clips | Audio generation models |

### 🖼️ Visual Assets

| Generator | Description | Models Used |
|-----------|-------------|-------------|
| 🖼️ **`BatchAssetGeneratorImages.py`** | Photorealistic images | `fal-ai/flux/schnell` |
| 🎨 **`BatchAssetGeneratorGraphics.py`** | General graphics and artwork | Image generation models |
| 🧩 **`BatchAssetGeneratorIcons.py`** | Vector-style minimalist icons | Image generation models |
| 📊 **`BatchAssetGeneratorDiagrams.py`** | Technical diagrams and charts | Image generation models |
| 🏛️ **`BatchAssetGeneratorMemoryPalace.py`** | Memory palace visualizations | Image generation models |
| 📺 **`BatchAssetGeneratorLowerThirds.py`** | Text overlay graphics for video | Image generation models |

### 🛠️ Utilities & Testing

| File | Purpose |
|------|---------|
| 🔧 **`asset_utils.py`** | Utilities for standardized naming and manifest tracking |
| 💰 **`EstimateWeeklyVideoCost.py`** | Calculate API costs for batch generation |
| 🎭 **`demo_versioning_system.py`** | Demonstration of versioning and manifest features |
| ✅ **`test_asset_utils.py`** | Unit tests for asset utilities (13 tests) |
| ✅ **`test_integration.py`** | End-to-end integration tests |

---

## 📋 Asset Versioning & Manifest System

✨ **Smart Asset Management** - Every generated asset is automatically tracked and versioned.

### 🏷️ Standardized Naming Convention

All assets follow a consistent naming pattern:
```
{scene_number:03d}_{asset_type}_{clean_desc}_v{version}.{ext}
```

**Examples:**
- `001_image_ferrari_cart_morph_v1.png` - Scene 1, Image, version 1
- `004_video_empty_uk_streets_v2.mp4` - Scene 4, Video, version 2
- `011_icon_ai_brain_network_v1.svg` - Scene 11, Icon, version 1

### 📝 Unified Manifest Tracking

The `MasterAssetGenerator.py` creates a comprehensive `manifest.json` that maps:
- 📁 **Filename** → Full file path
- 📝 **Prompt** → Complete generation prompt used
- ⏰ **Timestamp** → When the asset was created
- 🔗 **Result URL** → Original fal.ai result URL
- 📊 **Metadata** → Scene info, priority, model used, etc.

**Benefits:**
- 🔍 Easily find assets by scene number or type
- 📜 Complete traceability from prompt to final file
- 🔄 Version control for asset iterations
- 🤖 Automated tracking—no manual logging needed

For comprehensive documentation, see **[VERSIONING_AND_MANIFEST.md](./5_Symbols/VERSIONING_AND_MANIFEST.md)**.

---

## 🚀 Quick Start Guide

### 1️⃣ Install Dependencies

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
# OR install directly:
pip install fal-client
```

### 2️⃣ Configure API Key

```bash
# Set your fal.ai API key
export FAL_KEY="your-api-key-here"

# Or add to .env file:
echo 'FAL_KEY=your-api-key-here' > .env
```

### 3️⃣ Run Generators

**Run Individual Generators:**
```bash
# Generate video assets
python3 5_Symbols/BatchAssetGeneratorVideo.py

# Generate image assets
python3 5_Symbols/BatchAssetGeneratorImages.py

# Generate music tracks
python3 5_Symbols/BatchAssetGeneratorMusic.py
```

**Run Master Controller (All Generators):**
```bash
# Navigate to 5_Symbols directory
cd 5_Symbols

# Run master generator with project directory
python MasterAssetGenerator.py ../3_Simulation/Feb1Youtube
```

The Master Controller will:
1. 📊 Load configuration
2. 💰 Estimate API costs
3. ❓ Prompt for confirmation
4. 🚀 Generate all assets with standardized naming
5. 📝 Track everything in manifest.json
6. ✅ Save complete manifest in project directory

---

## 📖 Detailed Documentation

- **[Setup & Best Practices](./4_Formula/README.md)** - Installation, configuration, and usage tips
- **[Versioning System](./5_Symbols/VERSIONING_AND_MANIFEST.md)** - Complete guide to asset naming and manifest
- **[Implementation Summary](./IMPLEMENTATION_SUMMARY.md)** - Technical details of recent improvements
- **[Troubleshooting Guide](./6_Semblance/README.md)** - Common issues and solutions
- **[Testing Strategy](./7_Testing_known/README.md)** - QA validation and acceptance criteria

---

## 💡 Key Features

✨ **Automated Asset Generation**
- 🎬 Video clips (B-roll, animations)
- 🎵 Audio tracks (music, sound effects)
- 🖼️ Images (photorealistic, stylized)
- 🧩 Icons & graphics (vector-style)
- 📺 Video elements (lower thirds, chapter markers)

🎯 **Smart Asset Management**
- 🏷️ Standardized naming with scene numbers
- 📝 Automatic manifest generation
- 🔄 Built-in version control
- 📊 Complete metadata tracking

🔧 **Developer-Friendly**
- 🐍 Pure Python 3.x
- 📦 Minimal dependencies (fal-client)
- 🧪 Comprehensive test suite
- 📚 Well-documented codebase

---

## 🧪 Testing

Run the test suite to verify everything works:

```bash
cd 5_Symbols

# Run unit tests
python test_asset_utils.py

# Run integration tests
python test_integration.py

# Demo versioning system
python demo_versioning_system.py
```

**Test Coverage:**
- ✅ 13 unit tests for asset utilities
- ✅ Integration tests for end-to-end workflows
- ✅ Demo scripts for feature demonstration

---

## 🛠️ Troubleshooting

### Common Issues

**🔑 Missing API Key**
```
Error: "FAL_KEY environment variable not set"
Solution: export FAL_KEY='your-key-here'
```

**📦 Module Not Found**
```
Error: ModuleNotFoundError: No module named 'fal_client'
Solution: pip install fal-client
```

**⏱️ API Timeouts**
```
Error: "Generation failed: No video URL"
Solution: Check generation_summary.json for failed assets, then retry
```

For more troubleshooting help, see **[6_Semblance/README.md](./6_Semblance/README.md)**.

---

## 📊 Project Status

| Component | Status | Tests |
|-----------|--------|-------|
| 🎬 Video Generation | ✅ Complete | Passing |
| 🎵 Audio Generation | ✅ Complete | Passing |
| 🖼️ Image Generation | ✅ Complete | Passing |
| 🧩 Icon Generation | ✅ Complete | Passing |
| 📝 Manifest System | ✅ Complete | Passing |
| 🏷️ Versioning System | ✅ Complete | Passing |
| 🧪 Test Suite | ✅ Complete | 13/13 Passing |
| 📚 Documentation | ✅ Complete | N/A |

---

## 🎯 Use Cases

- **🎬 YouTube Video Production** - Generate all multimedia assets for "The Agentic Era" video
- **🎨 Content Creation** - Batch-generate visual assets for presentations and marketing
- **🎵 Audio Production** - Create background music and sound effects libraries
- **🧩 Icon Libraries** - Generate consistent icon sets for UIs and documentation
- **📺 Video Elements** - Create professional lower thirds and chapter markers

---

## 📜 License

This project is part of "The Agentic Era" initiative. See individual files for specific licensing information.

---

## 🤝 Contributing

Contributions are welcome! Please ensure:
- ✅ All tests pass (`python test_asset_utils.py`)
- 📝 Code follows existing patterns and conventions
- 📚 Documentation is updated for new features
- 🔒 No API keys are committed to the repository

---

## 📞 Support

For issues, questions, or suggestions:
1. 📖 Check the [Troubleshooting Guide](./6_Semblance/README.md)
2. 📚 Review the [Documentation](./4_Formula/README.md)
3. 🐛 Open an issue on GitHub

---

**Made with ❤️ using [fal.ai](https://fal.ai) generative AI models**

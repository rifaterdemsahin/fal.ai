# 🎨 Simulation Workspace

This directory serves as the **active production environment** for the weekly video pipeline. While the core logic lives in `5_Symbols`, the `3_Simulation` folder is where data input meets automated execution to produce final media artifacts.

## 🔄 The Input-Output Loop

The simulation follows a straightforward "Black Box" model powered by Gemini and fal.ai:

1. **Input**: You provide a structured script, storyline JSON, or prompt list.
2. **Process**: The `MasterAssetGenerator` (and specialized batch scripts) processes these inputs.
3. **Output**: A structured project folder containing versioned media, a `manifest.json`, and performance reports.

### 📥 User Inputs

To trigger a simulation, you typically provide:

* **Storyline JSONs**: Defined sequences for Anime or Video generation (e.g., `anime_storyline.json`).
* **Prompt Lists**: CSV or TXT files with descriptions for bulk image/icon generation.
* **CLI Arguments**: Direct instructions passed to the generators regarding scene counts and quality.

### 📤 Generated Outputs

Every simulation run populates a sub-directory (e.g., `Feb1Youtube/`) with:

* **Media Assets**: `.mp4`, `.png`, `.wav`, and `.glb` files ready for DaVinci Resolve.
* **Metadata**: A `manifest.json` file that acts as the "brain" of the folder, linking prompts to filenames.
* **Insights**: Markdown reports detailing costs, generation success rates, and time logs.

---

## 📂 Directory Structure

```
📁 3_Simulation/
├── 📁 2026-02-15/             # Example: Specific weekly project folder
│   ├── 📁 input             
│   ├── 📁 output 
│   └── 📄 manifest.json        # The master map for DaVinci Resolve import
└── 📄 README.md                # This documentation

```

---

## 🚀 Running a Weekly Simulation

To start the creation process, navigate to the root and run the Master Controller, pointing it to this simulation workspace:

```bash
# Example: Running the Feb 1st Video Production
python 5_Symbols/MasterAssetGenerator.py 3_Simulation/Feb1Youtube

```

### Simulation Checklist

* [ ] **Verify API Key**: Ensure `FAL_KEY` is active.
* [ ] **Check Inputs**: Ensure your script or JSON is placed in the target simulation folder.
* [ ] **Review Cost**: Look at the `cost_report.md` generated in the `weekly/` sub-folder after the run.
* [ ] **Validate Manifest**: Open `manifest.json` to ensure all assets are correctly mapped to their scenes.

---

## 🎞️ Workflow Integration

The assets produced here are designed for immediate consumption by the **DaVinci Resolve** pipeline.

| Asset Type | Primary Use Case | Resolution/Format |
| --- | --- | --- |
| **Video** | B-Roll & Visual Narrative | 1080p / 4k MP4 |
| **Audio** | Background Scores & SFX | High-bitrate WAV |
| **Images** | Contextual stills & Thumbnails | PNG / JPG |
| **3D** | Fusion-ready motion graphics | GLB / OBJ |

> **Note:** Always use the `manifest.json` generated in this folder to verify asset integrity before importing into your NLE (Non-Linear Editor).

Classic Prompt to ask to generate
@2026-02-15 generate the icons this week and use the source @input > and place it to the output @output

---

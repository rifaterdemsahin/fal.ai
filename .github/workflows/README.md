# GitHub Actions Workflows for Bulk Generators

This directory contains GitHub Actions workflows for running bulk asset generators. These workflows can be triggered manually from GitHub Actions UI or automatically when generator files are updated.

## 🚀 Available Workflows

### 1. Bulk SVG Generator (`bulk-svg-generator.yml`)
Generates SVG diagrams for documentation and visual explanations.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `BulkSVGGenerator.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- Generated SVG files in `3_Simulation/Feb1Youtube/weekly/generated_svgs/`
- Manifest and summary JSON files
- Artifacts uploaded for 30 days

### 2. Bulk Mermaid Generator (`bulk-mermaid-generator.yml`)
Generates Mermaid diagrams in Markdown format.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `BulkMermaidGenerator.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- Generated Mermaid diagrams in `5_Symbols/generated_mermaid_diagrams/`
- Manifest and summary JSON files
- Artifacts uploaded for 30 days

### 3. Batch Asset Generator - Audio (`batch-asset-generator-audio.yml`)
Generates audio assets and chapter markers.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `BatchAssetGeneratorAudio.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- Generated audio files in `5_Symbols/generated_audio/`
- Summary JSON file
- Artifacts uploaded for 30 days

### 4. Batch Asset Generator - Chapter Markers (`batch-asset-generator-chapter-markers.yml`)
Generates YouTube chapter markers based on EDL scene breakdown.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `BatchAssetGeneratorChapterMarkers.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- Generated chapter markers in `5_Symbols/generated_chapter_markers/`
- Summary JSON file
- Artifacts uploaded for 30 days

### 5. Batch Asset Generator - Diagrams (`batch-asset-generator-diagrams.yml`)
Generates diagram assets for video content.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `BatchAssetGeneratorDiagrams.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- Generated diagrams in `5_Symbols/generated_diagrams/`
- Summary JSON file
- Artifacts uploaded for 30 days

### 6. Batch Asset Generator - Graphics (`batch-asset-generator-graphics.yml`)
Generates motion graphics and brand assets.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `BatchAssetGeneratorGraphics.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- Generated graphics in `5_Symbols/generated_graphics/`
- Summary JSON file
- Artifacts uploaded for 30 days

### 7. Batch Asset Generator - Icons (`batch-asset-generator-icons.yml`)
Generates icon assets for UI overlays.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `BatchAssetGeneratorIcons.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- Generated icons in `5_Symbols/generated_icons/`
- Summary JSON file
- Artifacts uploaded for 30 days

### 8. Batch Asset Generator - Images (`batch-asset-generator-images.yml`)
Generates image assets including B-roll and infographics.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `BatchAssetGeneratorImages.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- Generated images in `5_Symbols/generated_assets/`
- Summary JSON file
- Artifacts uploaded for 30 days

### 9. Batch Asset Generator - Lower Thirds (`batch-asset-generator-lower-thirds.yml`)
Generates lower thirds overlays for video.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `BatchAssetGeneratorLowerThirds.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- Generated lower thirds in `5_Symbols/generated_assets/lower_thirds/`
- Summary JSON file
- Artifacts uploaded for 30 days

### 10. Batch Asset Generator - Memory Palace (`batch-asset-generator-memory-palace.yml`)
Generates memory palace visualization assets.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `BatchAssetGeneratorMemoryPalace.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- Generated memory palace assets in `5_Symbols/generated_memory_palace/`
- Summary JSON file
- Artifacts uploaded for 30 days

### 11. Batch Asset Generator - Music (`batch-asset-generator-music.yml`)
Generates music and audio background assets.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `BatchAssetGeneratorMusic.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- Generated music in `5_Symbols/generated_music/`
- Summary JSON file
- Artifacts uploaded for 30 days

### 12. Batch Asset Generator - Video (`batch-asset-generator-video.yml`)
Generates video clip assets.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `BatchAssetGeneratorVideo.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- Generated video clips in `5_Symbols/generated_video/`
- Summary JSON file
- Artifacts uploaded for 30 days

### 13. Master Asset Generator (`master-asset-generator.yml`)
Orchestrates generation of all assets for a given week/video project.

**Triggers:**
- Manual via workflow_dispatch
- Automatic on push to main when `MasterAssetGenerator.py` is modified

**Inputs:**
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- All generated assets from all generators
- Combined summary files
- Artifacts uploaded for 30 days

### 14. All Bulk Generators (`all-bulk-generators.yml`)
Master workflow that can run multiple generators at once.

**Triggers:**
- Manual via workflow_dispatch only

**Inputs:**
- `generators`: Select which generators to run (all, svg, mermaid, audio, chapter-markers, diagrams, graphics, icons, images, lower-thirds, memory-palace, music, video, master)
- `commit_and_push`: Whether to commit and push generated files (default: true)

**Outputs:**
- All generated assets from selected generators
- Combined artifacts uploaded for 30 days

## 📖 How to Run Workflows

### From GitHub Actions UI:
1. Go to the repository on GitHub
2. Click on "Actions" tab
3. Select the workflow you want to run from the left sidebar
4. Click "Run workflow" button
5. Select options if prompted (branch, inputs, etc.)
6. Click "Run workflow" to start

### From GitHub Codespaces:
These workflows are designed to work in GitHub Codespaces with commit/push capabilities:

1. Open the repository in Codespaces
2. Navigate to the Actions tab in the GitHub UI
3. Run workflows as described above
4. The workflows will automatically commit and push generated files (unless disabled)

Alternatively, you can trigger workflows using GitHub CLI in Codespaces:

```bash
# Run SVG generator
gh workflow run bulk-svg-generator.yml

# Run Mermaid generator
gh workflow run bulk-mermaid-generator.yml

# Run all generators
gh workflow run all-bulk-generators.yml -f generators=all

# Run with custom options
gh workflow run bulk-svg-generator.yml -f commit_and_push=false
```

## 🔐 Permissions

All workflows have `contents: write` permission to commit and push generated files back to the repository.

## 📦 Artifacts

Each workflow uploads generated files as artifacts that are retained for 30 days. You can download these artifacts from the workflow run page.

## 🔄 Auto-triggers

Workflows are configured to run automatically when their corresponding generator files are modified:
- Modifying `5_Symbols/BulkSVGGenerator.py` triggers the SVG generator workflow
- Modifying `5_Symbols/BulkMermaidGenerator.py` triggers the Mermaid generator workflow
- Modifying `5_Symbols/BatchAssetGeneratorAudio.py` triggers the audio generator workflow
- Modifying `5_Symbols/BatchAssetGeneratorChapterMarkers.py` triggers the chapter markers generator workflow
- Modifying `5_Symbols/BatchAssetGeneratorDiagrams.py` triggers the diagrams generator workflow
- Modifying `5_Symbols/BatchAssetGeneratorGraphics.py` triggers the graphics generator workflow
- Modifying `5_Symbols/BatchAssetGeneratorIcons.py` triggers the icons generator workflow
- Modifying `5_Symbols/BatchAssetGeneratorImages.py` triggers the images generator workflow
- Modifying `5_Symbols/BatchAssetGeneratorLowerThirds.py` triggers the lower thirds generator workflow
- Modifying `5_Symbols/BatchAssetGeneratorMemoryPalace.py` triggers the memory palace generator workflow
- Modifying `5_Symbols/BatchAssetGeneratorMusic.py` triggers the music generator workflow
- Modifying `5_Symbols/BatchAssetGeneratorVideo.py` triggers the video generator workflow
- Modifying `5_Symbols/MasterAssetGenerator.py` triggers the master asset generator workflow

## 🛠️ Adding New Bulk Generators

To add a new bulk generator workflow:

1. Create a new Python generator in `5_Symbols/` following the existing pattern
2. Copy one of the existing workflow files
3. Update the workflow name, file paths, and generator script name
4. Add it to the master `all-bulk-generators.yml` workflow
5. Update this README with the new generator information

## 📝 Notes

- All generators use Python 3.x
- Dependencies are installed from `requirements.txt` if present
- Generated files are placed in subdirectories under `5_Symbols/`
- The `.gitignore` file excludes generated directories by default, but workflows can still commit them if needed

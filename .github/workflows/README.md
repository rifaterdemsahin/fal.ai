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
- Generated SVG files in `5_Symbols/generated_svgs/`
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

### 3. All Bulk Generators (`all-bulk-generators.yml`)
Master workflow that can run multiple generators at once.

**Triggers:**
- Manual via workflow_dispatch only

**Inputs:**
- `generators`: Select which generators to run (all, svg, mermaid)
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

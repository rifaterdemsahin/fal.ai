### 3_Simulation - UI and Assets

**Workspace**:
This folder contains the `Feb1Youtube` directory, which acts as the primary workspace for simulation data and generated asset output.

**User Interface (UI)**:
- Currently, the "UI" is a **Command Line Interface (CLI)**.
- Users interact with the system by running Python scripts from the `5_Symbols` directory.
- Feedback is provided via console logs (formatted with emojis for readability), JSON summary files, and comprehensive manifest tracking.

**Asset Management**:
- Generated assets are organized into type-specific output directories (e.g., `generated_video`, `generated_icons`, `generated_assets_Images`) created at runtime.
- Each generation run produces a metadata JSON file linking the prompt, settings, and result URL for traceability.
- **Unified Manifest System**: The `manifest.json` file (created by MasterAssetGenerator) provides complete tracking of all assets with:
  - Standardized filenames with scene numbers and versioning
  - Full prompt text for each asset
  - Generation timestamps
  - Asset metadata (scene info, priority, model used, result URL, local path)

**Weekly Reports**:
- Generated reports are saved in the `Feb1Youtube/weekly/` directory:
  - `generation_report_YYYY-MM-DD.md` - Detailed generation summary
  - `cost_report_YYYY-MM-DD.md` - API cost analysis
  - Summary JSON files with metrics and asset counts

### 3_Simulation - UI and Assets

**Workspace**:
This folder contains the `Feb1Youtube` directory, which acts as the primary workspace for simulation data and potentially the raw output of generation tasks.

**User Interface (UI)**:
- Currently, the "UI" is a **Command Line Interface (CLI)**.
- Users interact with the system by running Python scripts from the `5_Symbols` directory.
- Feedback is provided via console logs (formatted with emojis for readability) and JSON summary files.

**Asset Management**:
- Generated assets are organized into type-specific output directories (e.g., `generated_video`, `generated_icons`) created at runtime.
- Each generation run produces a metadata JSON file linking the prompt, settings, and result URL for traceability.

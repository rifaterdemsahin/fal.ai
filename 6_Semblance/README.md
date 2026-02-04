### 6_Semblance - Error Logs and Solutions

**Common Issues**:

1.  **Missing API Key**:
    *   *Error*: "FAL_KEY environment variable not set"
    *   *Solution*: Run `export FAL_KEY='key'` or add it to your `.env` file.

2.  **Dependency Errors**:
    *   *Error*: `ModuleNotFoundError: No module named 'fal_client'`
    *   *Solution*: Ensure you are in the correct virtual environment and run `pip install fal-client`.

3.  **API Timeouts / Server Errors**:
    *   *Error*: "Generation failed: No video URL" or HTTP 5xx codes.
    *   *Solution*: The fal.ai service might be busy. The scripts save a `generation_summary.json`—check this to identify which specific asset failed. Retry the script; logically designed scripts should handle re-runs (checking for existing files, though currently overwrite might be default).

4.  **Model Availability**:
    *   *Issue*: Specific models (e.g., minimax) might change names or availability.
    *   *Solution*: Update the `model` key in the `GENERATION_QUEUE` within the Python scripts.

# Batch Asset Generator Usage Formula

This document outlines the steps to set up, run, and rerun the `BatchAssetGenerator.py` script using a Python virtual environment.

## Prerequisites

- Python 3 installed
- `fal.ai` API Key (Found in your `.env` file or dashboard)

## 1. Setup Virtual Environment (First Time Only)

Create a virtual environment to manage dependencies locally without affecting your system Python.

```bash
# Create the virtual environment in a folder named .venv
python3 -m venv .venv
```

## 2. Install Dependencies

Install the required `fal-client` library into the virtual environment.

```bash
# Install directly using the virtual environment's pip
.venv/bin/pip install fal-client

# OR activate the environment first and then install
source .venv/bin/activate
pip install fal-client
```

## 3. Run the Generator

To run the script, you need to provide your API key and use the python executable from the virtual environment.

### Option A: One-line command (recommended for quick runs)
This sets the key and runs the script using the venv python.

```bash
export FAL_KEY="your-api-key-here" && .venv/bin/python3 BatchAssetGenerator.py
```
*Note: Replace "your-api-key-here" with your actual key if it's not already set in your environment.*

### Option B: Activated Environment
If you are working in the terminal for a while:

```bash
# 1. Activate the environment
source .venv/bin/activate

# 2. Export Key (if not already set)
export FAL_KEY="your-api-key-here"

# 3. Run the script
python3 BatchAssetGenerator.py
```

## 4. Rerunning the Script

If you need to generate assets again (e.g., after modifying the prompt or adding new assets):

1.  **Modify the script**: Edit `BatchAssetGenerator.py` as needed.
2.  **Run again**: Use the same command as before.

```bash
# Rerun
export FAL_KEY="your-api-key-here" && .venv/bin/python3 BatchAssetGenerator.py
```

The script will ask for confirmation before generating assets.

## Common Issues

*   **`ModuleNotFoundError: No module named 'fal_client'`**: This means you are not using the virtual environment python or haven't installed the package in it. Ensure you use `.venv/bin/python3` or have activated the environment.
*   **API Key Error**: Ensure `FAL_KEY` is exported correctly in your terminal session.

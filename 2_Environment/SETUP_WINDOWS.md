# 🪟 Windows 10/11 Setup Guide

> Full Python 3.8+ support for the fal.ai Weekly Video Production Pipeline

---

## 📋 Overview

This guide covers setting up the fal.ai pipeline on Windows 10 or Windows 11 using PowerShell or Command Prompt.

---

## 🚀 Prerequisites

### Install Python 3.8+

1. **Download Python**:
   - Visit: https://www.python.org/downloads/
   - Download Python 3.8 or higher (recommend 3.11+)

2. **Run Installer**:
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"
   - Click "Install Now"

3. **Verify Installation**:
   ```powershell
   python --version
   # Should show: Python 3.8.x or higher
   
   pip --version
   # Should show pip version
   ```

### Install Git (if not already installed)

1. Download from: https://git-scm.com/download/win
2. Run installer with default settings
3. Verify: `git --version`

---

## 📥 Clone Repository

Open PowerShell or Command Prompt:

```powershell
# Navigate to your projects directory
cd C:\Users\YourUsername\Documents

# Clone the repository
git clone https://github.com/rifaterdemsahin/fal.ai.git

# Navigate into the project
cd fal.ai
```

---

## 🐍 Set Up Python Environment

### Create Virtual Environment

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Your prompt should now show (.venv) at the beginning
```

**Note**: If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Install Dependencies

```powershell
# Make sure virtual environment is activated
# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

---

## ⚙️ Configure API Key

### Method 1: Using .env File (Recommended)

1. **Copy the sample file**:
   ```powershell
   copy 4_Formula\.env.sample .env
   ```

2. **Edit .env file**:
   ```powershell
   # Open in Notepad
   notepad .env
   
   # OR use VS Code if installed
   code .env
   ```

3. **Add your API keys**:
   ```env
   FAL_KEY=your-fal-ai-key-here
   GOOGLE_API_KEY=your-google-key-here
   GOOGLE_CSE_ID=your-search-engine-id-here
   ```

4. **Save and close** the file

### Method 2: Set Environment Variable (Session-based)

For PowerShell:
```powershell
$env:FAL_KEY="your-fal-ai-key-here"
```

For Command Prompt:
```cmd
set FAL_KEY=your-fal-ai-key-here
```

**Note**: This method only lasts for the current session.

### Method 3: System Environment Variable (Permanent)

1. Press `Win + X` → Select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Variable name: `FAL_KEY`
6. Variable value: `your-fal-ai-key-here`
7. Click OK on all dialogs

---

## 🎬 Running Generators

### Navigate to Symbols Directory

```powershell
# Make sure you're in the project root
cd C:\path\to\fal.ai

# Navigate to generators
cd 5_Symbols
```

### Run Individual Generator

```powershell
# Example: Video generator
python Video\BatchAssetGeneratorVideo.py

# Example: Image generator
python Images\BatchAssetGeneratorImages.py

# Example: Music generator
python Audio\BatchAssetGeneratorMusic.py
```

### Run Master Generator

```powershell
cd 5_Symbols
python MasterAssetGenerator.py ..\3_Simulation\2026-02-10
```

---

## 💻 Using PowerShell ISE or VS Code

### Visual Studio Code (Recommended)

1. **Install VS Code**: https://code.visualstudio.com/
2. **Install Python Extension**:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search "Python" and install

3. **Open Project**:
   ```powershell
   cd C:\path\to\fal.ai
   code .
   ```

4. **Select Python Interpreter**:
   - Press Ctrl+Shift+P
   - Type "Python: Select Interpreter"
   - Choose the `.venv` interpreter

5. **Run Scripts**:
   - Open any `.py` file
   - Press F5 to run
   - Or right-click → "Run Python File in Terminal"

### PowerShell ISE

1. Open PowerShell ISE
2. Navigate to project: `cd C:\path\to\fal.ai`
3. Activate virtual environment: `.\.venv\Scripts\activate`
4. Open and run Python files

---

## 🔧 Troubleshooting

### Python Not Found

```powershell
# Verify Python is in PATH
$env:Path -split ";" | Select-String -Pattern "Python"

# If not found, add manually or reinstall Python with "Add to PATH" checked
```

### pip Not Working

```powershell
# Use python -m pip instead
python -m pip install -r requirements.txt
```

### Virtual Environment Won't Activate

```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Try activating again
.venv\Scripts\activate
```

### ModuleNotFoundError: No module named 'fal_client'

```powershell
# Make sure virtual environment is activated
.venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Permission Denied Errors

```powershell
# Run PowerShell as Administrator
# Right-click PowerShell → "Run as Administrator"
```

### File Path Issues

Windows uses backslashes (`\`) while Python often uses forward slashes (`/`). The scripts handle this automatically, but if you encounter issues:

```python
# Use pathlib in Python scripts (already done in project)
from pathlib import Path
path = Path("5_Symbols/Video")
```

---

## 📂 Windows-Specific Paths

```powershell
# Project root
C:\Users\YourUsername\Documents\fal.ai

# Generators
C:\Users\YourUsername\Documents\fal.ai\5_Symbols

# Output directory
C:\Users\YourUsername\Documents\fal.ai\3_Simulation
```

---

## 🔗 Additional Resources

- **Python for Windows**: https://docs.python.org/3/using/windows.html
- **Project Main README**: [../README.md](../README.md)
- **API Key Setup Guide**: [../4_Formula/SETUP_API_Key.md](../4_Formula/SETUP_API_Key.md)
- **Troubleshooting Guide**: [../6_Semblance/README.md](../6_Semblance/README.md)

---

## ✅ Verification Checklist

Before running generators, verify:

- [ ] Python 3.8+ is installed (`python --version`)
- [ ] Virtual environment is created and activated (`.venv\Scripts\activate`)
- [ ] Dependencies are installed (`pip list | grep fal-client` or `pip list | findstr fal-client`)
- [ ] `.env` file exists and contains `FAL_KEY`
- [ ] Can navigate to `5_Symbols` directory
- [ ] Test with a simple generator run

---

**Ready to Generate Assets on Windows!** 🎉

Once everything is verified, you can start generating assets using any of the batch generators in the `5_Symbols` directory.

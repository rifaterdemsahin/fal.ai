# 🍎 macOS Setup Guide

> Native Python 3.8+ support for the fal.ai Weekly Video Production Pipeline

---

## 📋 Overview

This guide covers setting up the fal.ai pipeline on macOS using Terminal and native tools.

---

## 🚀 Prerequisites

### Install Homebrew (Package Manager)

If not already installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the on-screen instructions to add Homebrew to your PATH.

### Install Python 3.8+

macOS comes with Python, but it's often outdated. Install a modern version:

```bash
# Install Python 3.11 (recommended)
brew install python@3.11

# Verify installation
python3 --version
# Should show: Python 3.8.x or higher

# Verify pip
pip3 --version
```

### Install Git

```bash
# Git should be pre-installed, but verify
git --version

# If not installed, install via Homebrew
brew install git
```

---

## 📥 Clone Repository

```bash
# Navigate to your projects directory
cd ~/Documents

# Clone the repository
git clone https://github.com/rifaterdemsahin/fal.ai.git

# Navigate into the project
cd fal.ai
```

---

## 🐍 Set Up Python Environment

### Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Your prompt should now show (.venv) at the beginning
```

### Install Dependencies

```bash
# Make sure virtual environment is activated
# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fal-client
```

---

## ⚙️ Configure API Key

### Method 1: Using .env File (Recommended)

```bash
# Copy the sample file
cp 4_Formula/.env.sample .env

# Edit the file with your preferred editor
nano .env
# OR
vim .env
# OR
code .env  # if VS Code is installed
# OR
open -a TextEdit .env
```

Add your API keys:
```env
FAL_KEY=your-fal-ai-key-here
GOOGLE_API_KEY=your-google-key-here
GOOGLE_CSE_ID=your-search-engine-id-here
```

Save and close the file:
- **nano**: Press `Ctrl+X`, then `Y`, then `Enter`
- **vim**: Press `Esc`, type `:wq`, press `Enter`
- **TextEdit/VS Code**: Save normally (Cmd+S)

### Method 2: Set Environment Variable (Session-based)

For the current terminal session:
```bash
export FAL_KEY="your-fal-ai-key-here"
```

### Method 3: Add to Shell Profile (Permanent)

For **zsh** (default on macOS Catalina and later):
```bash
# Add to .zshrc
echo 'export FAL_KEY="your-fal-ai-key-here"' >> ~/.zshrc

# Reload configuration
source ~/.zshrc
```

For **bash**:
```bash
# Add to .bash_profile or .bashrc
echo 'export FAL_KEY="your-fal-ai-key-here"' >> ~/.bash_profile

# Reload configuration
source ~/.bash_profile
```

---

## 🎬 Running Generators

### Navigate to Symbols Directory

```bash
# Make sure you're in the project root
cd ~/Documents/fal.ai

# Navigate to generators
cd 5_Symbols
```

### Run Individual Generator

```bash
# Example: Video generator
python3 Video/BatchAssetGeneratorVideo.py

# Example: Image generator
python3 Images/BatchAssetGeneratorImages.py

# Example: Music generator
python3 Audio/BatchAssetGeneratorMusic.py
```

### Run Master Generator

```bash
cd 5_Symbols
python3 MasterAssetGenerator.py ../3_Simulation/$(date +%Y-%m-%d)
```

---

## 💻 Using macOS Terminal Features

### Terminal Preferences

1. Open Terminal → Preferences
2. Choose your preferred theme
3. Set font size for readability
4. Enable "Use Option as Meta key" for better navigation

### Useful Aliases

Add to your `~/.zshrc` or `~/.bash_profile`:

```bash
# Navigate to project
alias falai='cd ~/Documents/fal.ai'

# Activate virtual environment
alias venv='source .venv/bin/activate'

# Run generators
alias falrun='cd ~/Documents/fal.ai/5_Symbols && source ../.venv/bin/activate'
```

Reload: `source ~/.zshrc` or `source ~/.bash_profile`

### VS Code Integration

```bash
# Install VS Code command line tools
# Open VS Code → Command Palette (Cmd+Shift+P)
# Type "Shell Command: Install 'code' command in PATH"

# Then you can open project from terminal
cd ~/Documents/fal.ai
code .
```

---

## 🔧 Troubleshooting

### Command Not Found: python3

```bash
# Check Python installation
which python3

# If not found, install via Homebrew
brew install python@3.11

# Add to PATH (if needed)
echo 'export PATH="/usr/local/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### pip Not Working

```bash
# Use python3 -m pip instead
python3 -m pip install -r requirements.txt
```

### Virtual Environment Issues

```bash
# Remove and recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### ModuleNotFoundError: No module named 'fal_client'

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Verify activation (prompt should show .venv)
which python3
# Should show: /path/to/fal.ai/.venv/bin/python3

# Reinstall dependencies
pip install -r requirements.txt
```

### SSL Certificate Errors

```bash
# Update certificates via Homebrew
brew install ca-certificates

# Or use Python's certificate installer
/Applications/Python\ 3.11/Install\ Certificates.command
```

### Permission Denied

```bash
# Make scripts executable
chmod +x 5_Symbols/*.py

# Or run with python3 explicitly
python3 5_Symbols/Video/BatchAssetGeneratorVideo.py
```

### macOS Gatekeeper Blocking Scripts

If macOS blocks execution:
1. System Preferences → Security & Privacy
2. Click "Allow" for the blocked script
3. Or disable Gatekeeper temporarily:
   ```bash
   sudo spctl --master-disable
   # Run your script
   sudo spctl --master-enable
   ```

---

## 🎨 macOS-Specific Features

### Using Spotlight to Navigate

Press `Cmd+Space` and type:
- "Terminal" to open Terminal
- Your project folder name to navigate

### Quick Look for Files

```bash
# Preview a Python file
qlmanage -p 5_Symbols/Video/BatchAssetGeneratorVideo.py
```

### Finder Integration

```bash
# Open current directory in Finder
open .

# Open specific folder
open 3_Simulation
```

---

## 📂 macOS-Specific Paths

```bash
# Project root
~/Documents/fal.ai

# Generators
~/Documents/fal.ai/5_Symbols

# Output directory
~/Documents/fal.ai/3_Simulation
```

---

## 🔗 Additional Resources

- **Python for macOS**: https://docs.python.org/3/using/mac.html
- **Homebrew Documentation**: https://docs.brew.sh
- **Project Main README**: [../README.md](../README.md)
- **API Key Setup Guide**: [../4_Formula/SETUP_API_Key.md](../4_Formula/SETUP_API_Key.md)
- **Troubleshooting Guide**: [../6_Semblance/README.md](../6_Semblance/README.md)

---

## ✅ Verification Checklist

Before running generators, verify:

- [ ] Python 3.8+ is installed (`python3 --version`)
- [ ] Homebrew is installed (`brew --version`)
- [ ] Virtual environment is created and activated (`source .venv/bin/activate`)
- [ ] Dependencies are installed (`pip list | grep fal-client`)
- [ ] `.env` file exists and contains `FAL_KEY`
- [ ] Can navigate to `5_Symbols` directory
- [ ] Test with a simple generator run

---

**Ready to Generate Assets on macOS!** 🎉

Once everything is verified, you can start generating assets using any of the batch generators in the `5_Symbols` directory.

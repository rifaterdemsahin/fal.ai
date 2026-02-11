# 🐧 Linux Setup Guide

> Full Python 3.8+ support for the fal.ai Weekly Video Production Pipeline

---

## 📋 Overview

This guide covers setting up the fal.ai pipeline on Linux distributions (Ubuntu, Debian, Fedora, Arch, etc.) using the terminal.

---

## 🚀 Prerequisites

### Install Python 3.8+

#### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Python 3.8 or higher
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

#### Fedora

```bash
# Install Python 3
sudo dnf install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

#### Arch Linux

```bash
# Install Python 3
sudo pacman -S python python-pip

# Verify installation
python --version
pip --version
```

### Install Git

Most Linux distributions have Git pre-installed, but if not:

```bash
# Ubuntu/Debian
sudo apt install git

# Fedora
sudo dnf install git

# Arch Linux
sudo pacman -S git

# Verify
git --version
```

---

## 📥 Clone Repository

```bash
# Navigate to your projects directory
cd ~/projects
# OR
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
- **VS Code**: Save normally (Ctrl+S)

### Method 2: Set Environment Variable (Session-based)

For the current terminal session:
```bash
export FAL_KEY="your-fal-ai-key-here"
```

### Method 3: Add to Shell Profile (Permanent)

For **bash** (most common):
```bash
# Add to .bashrc
echo 'export FAL_KEY="your-fal-ai-key-here"' >> ~/.bashrc

# Reload configuration
source ~/.bashrc
```

For **zsh**:
```bash
# Add to .zshrc
echo 'export FAL_KEY="your-fal-ai-key-here"' >> ~/.zshrc

# Reload configuration
source ~/.zshrc
```

For **fish**:
```bash
# Add to config.fish
echo 'set -x FAL_KEY "your-fal-ai-key-here"' >> ~/.config/fish/config.fish

# Reload configuration
source ~/.config/fish/config.fish
```

---

## 🎬 Running Generators

### Navigate to Symbols Directory

```bash
# Make sure you're in the project root
cd ~/projects/fal.ai
# OR
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

## 💻 Using Linux Terminal Features

### Useful Aliases

Add to your `~/.bashrc`, `~/.zshrc`, or shell config:

```bash
# Navigate to project
alias falai='cd ~/projects/fal.ai'

# Activate virtual environment
alias venv='source .venv/bin/activate'

# Combined: navigate and activate
alias falrun='cd ~/projects/fal.ai && source .venv/bin/activate'

# Run master generator
alias falmaster='cd ~/projects/fal.ai/5_Symbols && python3 MasterAssetGenerator.py'
```

Reload: `source ~/.bashrc` or `source ~/.zshrc`

### VS Code Integration

```bash
# Install VS Code on Ubuntu/Debian
sudo snap install code --classic
# OR
sudo apt install code

# Open project from terminal
cd ~/projects/fal.ai
code .
```

---

## 🔧 Troubleshooting

### Python3 Command Not Found

```bash
# Check if python (without 3) works
python --version

# If so, create an alias
echo 'alias python3=python' >> ~/.bashrc
source ~/.bashrc
```

### pip3 Not Working

```bash
# Use python3 -m pip instead
python3 -m pip install -r requirements.txt

# Or install pip separately
sudo apt install python3-pip  # Ubuntu/Debian
sudo dnf install python3-pip  # Fedora
```

### Virtual Environment Issues

```bash
# Install venv module if missing
sudo apt install python3-venv  # Ubuntu/Debian

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

### Permission Denied

```bash
# Make scripts executable
chmod +x 5_Symbols/*.py

# Or run with python3 explicitly (no need for +x)
python3 5_Symbols/Video/BatchAssetGeneratorVideo.py
```

### SSL Certificate Errors

```bash
# Ubuntu/Debian
sudo apt install ca-certificates
sudo update-ca-certificates

# Fedora
sudo dnf install ca-certificates
```

### Missing System Dependencies

Some Python packages may require system libraries:

```bash
# Ubuntu/Debian
sudo apt install python3-dev build-essential libssl-dev libffi-dev

# Fedora
sudo dnf install python3-devel gcc openssl-devel libffi-devel

# For image processing (Pillow, cairosvg)
sudo apt install libjpeg-dev libpng-dev libcairo2-dev  # Ubuntu/Debian
sudo dnf install libjpeg-turbo-devel libpng-devel cairo-devel  # Fedora
```

---

## 🖥️ Distribution-Specific Notes

### Ubuntu/Debian

- Uses `apt` package manager
- Python 3 is typically pre-installed
- May need to install `python3-venv` separately

### Fedora

- Uses `dnf` package manager
- Python 3 is the default Python
- Most dependencies available in repos

### Arch Linux

- Uses `pacman` package manager
- Python 3 is the default (command is just `python`)
- AUR has additional Python packages

### openSUSE

```bash
# Install Python and dependencies
sudo zypper install python3 python3-pip python3-virtualenv
```

### CentOS/RHEL

```bash
# Enable EPEL repository first
sudo yum install epel-release

# Install Python 3
sudo yum install python3 python3-pip
```

---

## 📂 Linux-Specific Paths

```bash
# Project root (adjust based on where you cloned)
~/projects/fal.ai
# OR
~/Documents/fal.ai

# Generators
~/projects/fal.ai/5_Symbols

# Output directory
~/projects/fal.ai/3_Simulation
```

---

## 🤖 GitHub Actions Integration

This Linux setup is also used by **GitHub Actions workflows** for automated asset generation in CI/CD pipelines.

### How GitHub Actions Uses This Setup

GitHub Actions workflows use a similar approach to set up the Python environment:

```yaml
# Example from .github/workflows/*.yml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.x'

- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt

- name: Set environment variables
  env:
    FAL_KEY: ${{ secrets.FAL_API_KEY }}
```

### Key Differences from Local Setup

1. **Virtual Environment**: GitHub Actions doesn't require explicit venv activation
2. **API Keys**: Uses GitHub Secrets instead of .env files
3. **Python Command**: Uses `python` instead of `python3`
4. **Automated**: Runs on push/workflow_dispatch triggers

### Related Workflows

See `.github/workflows/` directory for 14+ automated workflows that use this setup:
- Video generation: `batch-asset-generator-video.yml`
- Image generation: `batch-asset-generator-images.yml`
- Audio generation: `batch-asset-generator-music.yml`
- Master orchestration: `master-asset-generator.yml`

For detailed workflow documentation, see: [.github/workflows/README.md](../.github/workflows/README.md)

---

## 🎯 Running as a Service (Optional)

For automated generation, you can set up a systemd service:

```bash
# Create service file
sudo nano /etc/systemd/system/fal-generator.service
```

Add:
```ini
[Unit]
Description=fal.ai Asset Generator
After=network.target

[Service]
Type=oneshot
User=yourusername
WorkingDirectory=/home/yourusername/projects/fal.ai/5_Symbols
Environment="FAL_KEY=your-key-here"
ExecStart=/home/yourusername/projects/fal.ai/.venv/bin/python3 MasterAssetGenerator.py ../3_Simulation/$(date +%Y-%m-%d)

[Install]
WantedBy=multi-user.target
```

Enable and run:
```bash
sudo systemctl daemon-reload
sudo systemctl enable fal-generator.service
sudo systemctl start fal-generator.service
```

---

## 🔗 Additional Resources

- **Python for Linux**: https://docs.python.org/3/using/unix.html
- **Project Main README**: [../README.md](../README.md)
- **API Key Setup Guide**: [../4_Formula/SETUP_API_Key.md](../4_Formula/SETUP_API_Key.md)
- **Troubleshooting Guide**: [../6_Semblance/README.md](../6_Semblance/README.md)

---

## ✅ Verification Checklist

Before running generators, verify:

- [ ] Python 3.8+ is installed (`python3 --version`)
- [ ] Virtual environment is created and activated (`source .venv/bin/activate`)
- [ ] Dependencies are installed (`pip list | grep fal-client`)
- [ ] `.env` file exists and contains `FAL_KEY`
- [ ] Can navigate to `5_Symbols` directory
- [ ] Test with a simple generator run

---

**Ready to Generate Assets on Linux!** 🎉

Once everything is verified, you can start generating assets using any of the batch generators in the `5_Symbols` directory.

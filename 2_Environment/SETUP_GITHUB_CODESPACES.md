# ☁️ GitHub Codespaces Setup Guide

> **Recommended for teams** - Pre-configured development environment with all dependencies

---

## 📋 Overview

GitHub Codespaces provides a cloud-based development environment that's pre-configured with all necessary dependencies for the fal.ai Weekly Video Production Pipeline. This is the easiest way to get started, especially for teams.

---

## 🚀 Quick Start

### 1️⃣ Open in Codespaces

1. Navigate to the repository on GitHub: `https://github.com/rifaterdemsahin/fal.ai`
2. Click the green **Code** button
3. Select the **Codespaces** tab
4. Click **Create codespace on main** (or select your branch)

GitHub will create and configure your development environment automatically.

### 2️⃣ Wait for Environment Setup

The Codespace will:
- ✅ Clone the repository
- ✅ Install Python 3.8+
- ✅ Install all dependencies from `requirements.txt`
- ✅ Configure the development environment

This typically takes 2-3 minutes.

---

## ⚙️ Configuration

### Set Up API Key

1. **Open Terminal** in Codespaces (Terminal → New Terminal)

2. **Create .env file**:
   ```bash
   cd /workspaces/fal.ai
   cp 4_Formula/.env.sample .env
   ```

3. **Edit the .env file**:
   ```bash
   # Open in Codespaces editor
   code .env
   ```

4. **Add your API keys**:
   ```env
   FAL_KEY=your-fal-ai-key-here
   GOOGLE_API_KEY=your-google-key-here
   GOOGLE_CSE_ID=your-search-engine-id-here
   ```

5. **Save the file** (Ctrl+S or Cmd+S)

### Verify Installation

```bash
# Check Python version
python3 --version

# Verify dependencies
pip list | grep fal-client

# Check environment variables
python3 -c "import os; print('FAL_KEY is set:', bool(os.getenv('FAL_KEY')))"
```

---

## 🎬 Running Generators

### Individual Generator

```bash
# Navigate to the Symbols directory
cd /workspaces/fal.ai/5_Symbols

# Run a specific generator
python3 Video/BatchAssetGeneratorVideo.py
```

### Master Generator (All Assets)

```bash
cd /workspaces/fal.ai/5_Symbols
python3 MasterAssetGenerator.py ../3_Simulation/$(date +%Y-%m-%d)
```

---

## 💡 Tips for Codespaces

### Terminal Navigation

```bash
# Repository root
cd /workspaces/fal.ai

# Generators directory
cd /workspaces/fal.ai/5_Symbols

# Output directory
cd /workspaces/fal.ai/3_Simulation
```

### File Editing

- Use the built-in VS Code editor
- Files are automatically saved to the cloud
- Changes persist between sessions

### Port Forwarding

If you run a web server or API:
```bash
# Codespaces automatically forwards ports
# Access via the "Ports" tab in the bottom panel
```

### Persistent Storage

- Your Codespace persists for 30 days of inactivity
- Changes are saved automatically
- You can have multiple Codespaces for different branches

---

## 🔧 Troubleshooting

### Codespace Won't Start

1. Check your GitHub Codespaces quota
2. Try creating a new Codespace
3. Contact GitHub support if issues persist

### Dependencies Not Installed

```bash
# Reinstall dependencies manually
pip install -r requirements.txt
```

### Environment Variables Not Loading

```bash
# Verify .env file exists
ls -la /workspaces/fal.ai/.env

# Check file contents (safely)
python3 -c "from dotenv import load_dotenv; load_dotenv(); import os; print('Keys loaded:', bool(os.getenv('FAL_KEY')))"
```

### Permission Issues

Codespaces typically don't have permission issues, but if you encounter them:
```bash
# Check file permissions
ls -la /workspaces/fal.ai/

# Fix if needed (usually not required)
chmod +x 5_Symbols/*.py
```

---

## 🔗 Additional Resources

- **GitHub Codespaces Documentation**: https://docs.github.com/en/codespaces
- **Project Main README**: [../README.md](../README.md)
- **API Key Setup Guide**: [../4_Formula/SETUP_API_Key.md](../4_Formula/SETUP_API_Key.md)
- **Troubleshooting Guide**: [../6_Semblance/README.md](../6_Semblance/README.md)

---

## ✅ Verification Checklist

Before running generators, verify:

- [ ] Python 3.8+ is installed (`python3 --version`)
- [ ] Dependencies are installed (`pip list | grep fal-client`)
- [ ] `.env` file exists and contains `FAL_KEY`
- [ ] Can navigate to `/workspaces/fal.ai/5_Symbols`
- [ ] Test with a simple generator run

---

**Ready to Generate Assets!** 🎉

Once everything is verified, you can start generating assets using any of the batch generators in the `5_Symbols` directory.

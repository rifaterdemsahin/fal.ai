# 🔑 fal.ai API Key Setup Guide

This guide explains how to obtain, save, and use your fal.ai API key for the weekly video creation pipeline.

---

## 📋 Table of Contents

1. [Getting Your API Key](#getting-your-api-key)
2. [Saving Your API Key](#saving-your-api-key)
3. [Using the API Key](#using-the-api-key)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)

---

## 🎯 Getting Your API Key

### Step 1: Create a fal.ai Account

1. Visit [fal.ai](https://fal.ai) in your web browser
2. Click **"Sign Up"** or **"Get Started"** 
3. Create an account using:
   - GitHub account (recommended)
   - Google account
   - Email and password

### Step 2: Access Your Dashboard

1. Once logged in, navigate to your **Dashboard**
2. Look for the **API Keys** or **Keys** section in the navigation menu
3. You should see your existing API keys or an option to create a new one

### Step 3: Generate an API Key

1. Click **"Create New API Key"** or **"Generate Key"**
2. Give your key a descriptive name (e.g., "Weekly Video Pipeline")
3. Set permissions if prompted (typically "Full Access" for this project)
4. Click **"Create"** or **"Generate"**
5. **Important**: Copy the key immediately - it will only be shown once!

```
Example API Key Format:
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### 🚨 Security Best Practices

- **Never share** your API key publicly
- **Never commit** your API key to version control (GitHub, GitLab, etc.)
- **Use environment variables** instead of hardcoding keys in scripts
- **Rotate keys regularly** for enhanced security
- **Use separate keys** for development and production environments

---

## 💾 Saving Your API Key

You have three options to save your API key. Choose the method that works best for your workflow:

### Option 1: Environment Variable (Recommended for Quick Sessions)

Set the API key as an environment variable in your terminal session.

#### On macOS/Linux/GitHub Codespaces:
```bash
export FAL_KEY="your-api-key-here"
```

#### On Windows (PowerShell):
```powershell
$env:FAL_KEY="your-api-key-here"
```

#### On Windows (Command Prompt):
```cmd
set FAL_KEY=your-api-key-here
```

**Note**: This method requires setting the key each time you open a new terminal session.

---

### Option 2: .env File (Recommended for Development)

Create a `.env` file in the project root directory to persist your API key across sessions.

#### Steps:

1. **Create the .env file** in the project root:
   ```bash
   cd /home/runner/work/fal.ai/fal.ai
   touch .env
   ```

2. **Add your API key** to the file:
   ```bash
   echo 'FAL_KEY=your-api-key-here' > .env
   ```

   Or manually edit `.env`:
   ```env
   FAL_KEY=your-api-key-here
   ```

3. **Verify .gitignore** includes `.env` to prevent accidental commits:
   ```bash
   grep ".env" .gitignore
   ```

   If not present, add it:
   ```bash
   echo ".env" >> .gitignore
   ```

#### Using .env with Python scripts:

If your scripts use `python-dotenv`, the key will be loaded automatically:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file
api_key = os.environ.get("FAL_KEY")
```

**Note**: Check if `python-dotenv` is installed:
```bash
pip list | grep python-dotenv
```

If not installed:
```bash
pip install python-dotenv
```

---

### Option 3: Shell Configuration File (Permanent)

Add the API key to your shell configuration file for permanent availability.

#### For bash users (~/.bashrc or ~/.bash_profile):
```bash
echo 'export FAL_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### For zsh users (~/.zshrc):
```bash
echo 'export FAL_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

#### For fish shell users (~/.config/fish/config.fish):
```bash
echo 'set -gx FAL_KEY "your-api-key-here"' >> ~/.config/fish/config.fish
source ~/.config/fish/config.fish
```

**Note**: This makes the key available in all terminal sessions permanently.

---

## 🚀 Using the API Key

Once your API key is configured, the generators will automatically use it from the environment.

### Running Individual Generators

```bash
# Navigate to project root
cd /home/runner/work/fal.ai/fal.ai

# Run video generator
python3 5_Symbols/BatchAssetGeneratorVideo.py

# Run image generator
python3 5_Symbols/BatchAssetGeneratorImages.py

# Run music generator
python3 5_Symbols/BatchAssetGeneratorMusic.py
```

### Running the Master Controller

The Master Controller orchestrates all generators:

```bash
# Navigate to 5_Symbols directory
cd 5_Symbols

# Run master generator
python MasterAssetGenerator.py ../3_Simulation/Feb1Youtube
```

### Using with Virtual Environment

If you're using a Python virtual environment:

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Set API key (if not using .env)
export FAL_KEY="your-api-key-here"

# Run generators
python3 5_Symbols/BatchAssetGeneratorVideo.py
```

### Quick One-Line Command

Combine setting the key and running a script:

```bash
# Export key and run in one command
export FAL_KEY="your-api-key-here" && python3 5_Symbols/BatchAssetGeneratorImages.py
```

---

## ✅ Verification

### Method 1: Echo the Variable

Check if your API key is set:

```bash
# macOS/Linux/Codespaces
echo $FAL_KEY

# Windows PowerShell
echo $env:FAL_KEY

# Windows CMD
echo %FAL_KEY%
```

**Expected output**: Your API key string (not empty)

### Method 2: Python Test Script

Create a quick test script to verify:

```bash
python3 -c "import os; print('API Key Set:', 'FAL_KEY' in os.environ and len(os.environ.get('FAL_KEY', '')) > 0)"
```

**Expected output**: `API Key Set: True`

### Method 3: Run a Simple Generator Test

Try running a generator - it will fail immediately if the key is not set:

```bash
python3 5_Symbols/BatchAssetGeneratorImages.py
```

**If the key is set correctly**, you'll see:
```
🎨 Batch Image Generator
=========================
API Key: ✓ Found
...
```

**If the key is NOT set**, you'll see:
```
❌ ERROR: FAL_KEY environment variable not set
   Set it with: export FAL_KEY='your-api-key-here'
```

---

## 🛠️ Troubleshooting

### Issue 1: "FAL_KEY environment variable not set"

**Problem**: The API key is not available to the Python script.

**Solutions**:

1. **Check if the key is set**:
   ```bash
   echo $FAL_KEY
   ```

2. **Set the key in your current session**:
   ```bash
   export FAL_KEY="your-actual-key-here"
   ```

3. **If using .env file**, ensure:
   - The file exists in the project root
   - The file contains `FAL_KEY=your-key`
   - Your script loads the .env file (using `python-dotenv`)

4. **If using shell config file**, ensure:
   - You've sourced the config file: `source ~/.bashrc` or `source ~/.zshrc`
   - You've opened a new terminal session after editing the config

---

### Issue 2: "Invalid API Key" or Authentication Errors

**Problem**: The API key is set but fal.ai rejects it.

**Solutions**:

1. **Verify key format**: fal.ai keys are typically UUID format
   ```
   xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```

2. **Check for extra spaces or quotes**:
   ```bash
   # Wrong:
   export FAL_KEY=" your-key-here "  # Has spaces
   export FAL_KEY="'your-key-here'"  # Has extra quotes
   
   # Correct:
   export FAL_KEY="your-key-here"
   ```

3. **Regenerate key**: Go to fal.ai dashboard and create a new API key

4. **Check key permissions**: Ensure the key has the necessary permissions for generation

---

### Issue 3: Key Works in Terminal but Not in Scripts

**Problem**: `echo $FAL_KEY` shows the key, but scripts can't find it.

**Solutions**:

1. **Check subprocess environment**: If running scripts with `python3`, ensure the key is exported:
   ```bash
   export FAL_KEY="your-key"  # Not just 'FAL_KEY="your-key"'
   ```

2. **Use absolute path for .env**:
   ```python
   from dotenv import load_dotenv
   load_dotenv('/absolute/path/to/.env')
   ```

3. **Check virtual environment**: Ensure you're using the correct Python interpreter:
   ```bash
   which python3  # Should point to .venv/bin/python3 if using venv
   ```

---

### Issue 4: Key Lost After Closing Terminal

**Problem**: API key disappears when you close and reopen the terminal.

**Solutions**:

1. **Use .env file** (recommended for development)
2. **Add to shell config** (~/.bashrc, ~/.zshrc, etc.) for permanent availability
3. **Set key in each session** (least convenient but most secure)

---

### Issue 5: API Key Committed to Git (Security Risk!)

**Problem**: You accidentally committed your API key to version control.

**Immediate Actions**:

1. **Revoke the key immediately** on fal.ai dashboard
2. **Generate a new key**
3. **Remove from Git history**:
   ```bash
   # Remove the file from Git history
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/file-with-key" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (dangerous - coordinate with team first)
   git push origin --force --all
   ```

4. **Add to .gitignore** to prevent future accidents:
   ```bash
   echo ".env" >> .gitignore
   echo "*.key" >> .gitignore
   git add .gitignore
   git commit -m "Add API key files to .gitignore"
   ```

---

### Issue 6: Multiple API Keys for Different Environments

**Problem**: Need separate keys for development, staging, and production.

**Solution**:

Use different .env files:

```bash
# Development
.env.dev
FAL_KEY=dev-key-here

# Production
.env.prod
FAL_KEY=prod-key-here
```

Load the appropriate file:

```python
import os
from dotenv import load_dotenv

env = os.getenv('ENVIRONMENT', 'dev')
load_dotenv(f'.env.{env}')
```

Or use shell scripts to switch:

```bash
# Switch to dev
export FAL_KEY=$(grep FAL_KEY .env.dev | cut -d '=' -f2)

# Switch to prod
export FAL_KEY=$(grep FAL_KEY .env.prod | cut -d '=' -f2)
```

---

## 📚 Additional Resources

- **fal.ai Documentation**: [https://fal.ai/docs](https://fal.ai/docs)
- **API Reference**: Check the fal.ai dashboard for detailed API documentation
- **Project Documentation**: See [4_Formula/README.md](./README.md) for generator usage
- **Troubleshooting Guide**: See [6_Semblance/README.md](../6_Semblance/README.md) for common issues

---

## 🔐 Security Checklist

Before running generators in production, verify:

- [ ] API key is stored securely (environment variable or .env file)
- [ ] .env file is in .gitignore
- [ ] No API keys are hardcoded in Python scripts
- [ ] Shell config files with keys have appropriate permissions (chmod 600)
- [ ] Team members use separate API keys (not shared)
- [ ] Keys are rotated periodically
- [ ] Old/unused keys are revoked on fal.ai dashboard

---

## 💡 Quick Reference Card

```bash
# Get API Key
1. Visit https://fal.ai
2. Sign up/Log in
3. Dashboard → API Keys → Create New Key
4. Copy key (shown only once!)

# Set Key (choose one method)
export FAL_KEY="your-key"           # Session only
echo 'FAL_KEY=your-key' > .env      # .env file (recommended)
echo 'export FAL_KEY="your-key"' >> ~/.bashrc  # Permanent

# Verify
echo $FAL_KEY                       # Should show your key

# Use
python3 5_Symbols/BatchAssetGeneratorVideo.py
```

---

**Made with ❤️ for the fal.ai Weekly Video Creation Pipeline**

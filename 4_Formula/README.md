# 🧪 Batch Asset Generator Formulas

This directory contains standard procedures, workflows, and configurations for the project.

## 📚 Formula References

### ⚙️ Setup & Configuration

* [**🔑 API Key Setup**](./SETUP_API_Key.md) - Standard method using `.env`.
* [**🔒 GitHub Secrets**](./SETUP_GitHub_Secrets.md) - For CI/CD automation.

### ⚡ Workflows

* [**🛡️ Safe PNG Guide**](./WORKFLOW_Safe_PNG.md) - Ensuring DaVinci Resolve compatibility.
* [**🔍 Dynamic Zoom**](./WORKFLOW_Dynamic_Zoom_PNG.md) - How to handle zoom effects.
* [**🎵 Music Generator**](./WORKFLOW_Run_Music_Generator.md) - Generating MP3/WAV assets.
* [**📥 Download MP3**](./WORKFLOW_Download_MP3.md) - Helper guide.

### 🛠️ Development Specs

* [**Music Generator Spec**](./DEV_Music_Generator_Spec.md)
* [**PNG Optimization Spec**](./DEV_PNG_Optimization_Spec.md)

---

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -r ../requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
FAL_KEY=your_key_here
```

### 3. Run a Generator

```bash
python 5_Symbols/BatchAssetGeneratorMusic.py
```

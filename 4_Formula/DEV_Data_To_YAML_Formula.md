# 🏗️ Formula: Externalizing Configuration Data to YAML

## Summary

This formula outlines the standard pattern for moving hardcoded configuration data (such as asset lists, prompt queues, and generation settings) out of Python scripts and into centralized YAML files. This separation of concerns improves maintainability, allows for non-code updates, and ensures a single source of truth.

## Problem Identified

Hardcoding large lists of dictionaries (like generation queues) directly into Python scripts leads to:

1. **Code Bloat:** Scripts become long and difficult to read.
2. **Maintenance Risk:** Changing a prompt requires editing executable code, increasing the risk of syntax errors.
3. **Duplication:** Shared data (like brand colors or seeds) might be defined in multiple places.
4. **Inflexibility:** Changing configuration requires a "deployment" or code commit rather than just a config update.

## The Solution: YAML Configuration Pattern

### 1. Centralized Data File

Create a `.yaml` file in a dedicated `_source` or `config` directory.

**Example Structure (`batch_generation_data.yaml`):**

```yaml
diagrams:
  - id: "D1.1"
    name: "architecture_overview"
    prompt: "A complex diagram..."
    model: "fal-ai/flux/dev"

images:
  - id: "1.2"
    name: "hero_image"
    prompt: "A futuristic city..."
```

### 2. Python Loading Pattern

Use `PyYAML` to load this data dynamically.

**Implementation wrapper:**

```python
import yaml
from pathlib import Path

# Define path to config
DATA_PATH = Path("path/to/your/config.yaml")

def load_config():
    if not DATA_PATH.exists():
        print(f"⚠️ Config not found: {DATA_PATH}")
        return {}
    
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return {}

# Usage
config = load_config()
GENERATION_QUEUE = config.get("diagrams", [])
```

## Benefits

1. **Clean Code:** Python scripts focus purely on logic (API calling, file handling).
2. **Safe Editing:** YAML is human-readable and safer to edit than Python code.
3. **Scalability:** Easy to add hundreds of items without affecting script performance or readability.
4. **Interoperability:** YAML files can be generated or read by other tools (e.g., n8n, dashboards).

## Applied Checklists

### ✅ Migration Checklist

- [ ] Identify hardcoded lists in `.py` files.
- [ ] Create a target `.yaml` file.
- [ ] Convert Python dictionaries to YAML format.
- [ ] Install `PyYAML` (`pip install PyYAML`).
- [ ] Implement the `load_queue` function in the Python script.
- [ ] Test the script to ensure it correctly reads the external data.

### ✅ Best Practices

- **Paths:** Use `pathlib` for robust path handling across OS versions.
- **Validation:** Add basic checks (e.g., `if not queue: print("Empty")`) after loading.
- **Fallbacks:** Handle missing files gracefully (don't crash, just warn).
- **Encoding:** Always use `encoding='utf-8'` when opening text files.

## Case Study: Batch Asset Generators

*Refactored Feb 2026*

We successfully migrated the hardcoded `GENERATION_QUEUE` lists from:

- `BatchAssetGeneratorDiagrams.py`
- `BatchAssetGeneratorImages.py`
- `BatchAssetGeneratorVideo.py`
- `BatchAssetGeneratorGraphics.py`

Into a single source of truth:
`c:\projects\fal.ai\3_Simulation\Feb1Youtube\_source\batch_generation_data.yaml`

This reduced code size significantly and centralized the "Creative Direction" (prompts/scenes) into one readable document.

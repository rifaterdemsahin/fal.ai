# Code Duplicates Analysis - 6_Semblance

## Overview
This document identifies code duplicates in the `5_Symbols` folder and provides refactoring recommendations to reduce redundancy and improve maintainability.

---

## Critical Code Duplicates Identified

### 1. **Generate Asset Function** (HIGHEST PRIORITY)
**Location**: All `BatchAssetGenerator*.py` files  
**Duplication Count**: 7+ files  
**Lines Duplicated**: ~100 lines per file

#### Files Affected:
- `BatchAssetGeneratorImages.py` (lines 297-380)
- `BatchAssetGeneratorGraphics.py` (lines 212-295)
- `BatchAssetGeneratorIcons.py` (lines 214-297)
- `BatchAssetGeneratorLowerThirds.py` (lines 213-296)
- `BatchAssetGeneratorDiagrams.py` (lines 91-174)
- `BatchAssetGeneratorMemoryPalace.py` (lines 66-149)
- `BatchAssetGeneratorChapterMarkers.py` (lines 114-197)

#### Duplicate Code Pattern:
```python
def generate_asset(asset_config: Dict, output_dir: Path, manifest: Optional[object] = None, version: int = 1) -> Dict:
    """Generate a single asset using fal.ai"""
    print(f"\n{'='*60}")
    print(f"🎨 Generating: {asset_config['name']}")
    print(f"   Scene: {asset_config['scene']}")
    print(f"   Priority: {asset_config['priority']}")
    print(f"   Seed: {asset_config['seed_key']} ({SEEDS[asset_config['seed_key']]})")
    print(f"{'='*60}")
    
    try:
        # Prepare arguments
        arguments = {
            "prompt": asset_config["prompt"],
            "image_size": asset_config["image_size"],
            "num_inference_steps": asset_config["num_inference_steps"],
            "seed": SEEDS[asset_config["seed_key"]],
            "num_images": 1,
        }
        
        # Generate image
        print("⏳ Sending request to fal.ai...")
        result = fal_client.subscribe(
            asset_config["model"],
            arguments=arguments,
        )
        
        # Download and save (nearly identical across all files)
        # ... (60+ more lines of duplicate code)
```

**Estimated Duplicate Lines**: ~700 lines across 7 files

---

### 2. **Process Queue Function** (HIGH PRIORITY)
**Location**: All `BatchAssetGenerator*.py` files  
**Duplication Count**: 8+ files  
**Lines Duplicated**: ~80 lines per file

#### Files Affected:
- All `BatchAssetGenerator*.py` files contain nearly identical `process_queue()` functions

#### Duplicate Code Pattern:
```python
def process_queue(queue: List[Dict], output_dir: Path, manifest: Optional[object] = None):
    """Process the entire generation queue"""
    print("="*60)
    print("   🎨 fal.ai Batch Asset Generator")
    print("   Project: The Agentic Era - Managing 240+ Workflows")
    print("="*60)
    
    # Check API key
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("\n❌ ERROR: FAL_KEY environment variable not set")
        print("   Set it with: export FAL_KEY='your-api-key-here'")
        return []
    
    print(f"\n✅ API Key found")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print(f"\n📊 Assets to generate: {len(queue)}")
    
    # ... (60+ more lines of duplicate code for processing)
```

**Estimated Duplicate Lines**: ~640 lines across 8 files

---

### 3. **Main Function** (MEDIUM PRIORITY)
**Location**: All `BatchAssetGenerator*.py` files  
**Duplication Count**: 11 files  
**Lines Duplicated**: ~10 lines per file

#### Duplicate Code Pattern:
```python
def main():
    """Main execution"""
    # Confirm before proceeding
    print("\n" + "="*60)
    response = input("🤔 Proceed with generation? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Cancelled by user")
        return
        
    process_queue(GENERATION_QUEUE, OUTPUT_DIR)

if __name__ == "__main__":
    main()
```

**Estimated Duplicate Lines**: ~110 lines across 11 files

---

### 4. **Configuration Boilerplate** (MEDIUM PRIORITY)
**Location**: All `BatchAssetGenerator*.py` files  
**Duplication Count**: 11 files  
**Lines Duplicated**: ~50 lines per file

#### Files Affected:
All `BatchAssetGenerator*.py` files contain identical:
- Import statements (lines 1-28)
- SEEDS dictionary definitions
- BRAND_COLORS dictionary
- Output directory setup

#### Duplicate Code Pattern:
```python
#!/usr/bin/env python3
"""
fal.ai Batch Asset Generator
...
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional

# Install: pip install fal-client
try:
    import fal_client
except ImportError:
    print("❌ fal_client not installed. Run: pip install fal-client")
    exit(1)

# Import asset utilities
try:
    from asset_utils import generate_filename, extract_scene_number, ManifestTracker
except ImportError:
    # Fallback if running standalone
    print("⚠️  asset_utils not found. Using legacy naming convention.")
    generate_filename = None
    extract_scene_number = None
    ManifestTracker = None

# Configuration
OUTPUT_DIR = Path("./generated_assets")  # Slightly different per file
OUTPUT_DIR.mkdir(exist_ok=True)

# Consistency seeds for different asset categories
SEEDS = {
    "SEED_001": 42,      # B-roll (can vary)
    "SEED_002": 123456,  # Infographics (MUST match)
    "SEED_003": 789012,  # Motion graphics (brand)
    "SEED_004": 345678,  # UI overlays (template)
}

# Brand color palette (reference for prompts)
BRAND_COLORS = {
    "primary_dark": "#1a1a2e",
    "accent_blue": "#00d4ff",
    "accent_purple": "#7b2cbf",
    "secondary_teal": "#00bfa5",
    "highlight_orange": "#ff6b35",
    "text_white": "#ffffff",
}
```

**Estimated Duplicate Lines**: ~550 lines across 11 files

---

## Total Duplicate Code Statistics

| Category | Files Affected | Lines per File | Total Duplicate Lines |
|----------|---------------|----------------|---------------------|
| Generate Asset Function | 7 | ~100 | ~700 |
| Process Queue Function | 8 | ~80 | ~640 |
| Main Function | 11 | ~10 | ~110 |
| Configuration Boilerplate | 11 | ~50 | ~550 |
| **TOTAL** | **11 unique files** | **~240** | **~2,000 lines** |

---

## Refactoring Opportunities

### Opportunity 1: Create Base Asset Generator Class (RECOMMENDED)
**Impact**: Eliminates ~1,500 lines of duplicate code  
**Effort**: Medium (2-3 hours)

#### Proposed Structure:
```python
# base_asset_generator.py

class BaseAssetGenerator:
    """Base class for all asset generators"""
    
    def __init__(self, output_dir: Path, seeds: Dict, brand_colors: Dict):
        self.output_dir = output_dir
        self.seeds = seeds
        self.brand_colors = brand_colors
        self.manifest = None
        
    def generate_asset(self, asset_config: Dict, version: int = 1) -> Dict:
        """Common asset generation logic"""
        # Unified implementation replacing 700 lines of duplicates
        pass
        
    def process_queue(self, queue: List[Dict]) -> List[Dict]:
        """Common queue processing logic"""
        # Unified implementation replacing 640 lines of duplicates
        pass
        
    def run(self):
        """Common main execution logic"""
        # Unified implementation replacing 110 lines of duplicates
        pass
```

#### Then Each Generator Becomes:
```python
# BatchAssetGeneratorImages.py

from base_asset_generator import BaseAssetGenerator

class ImageAssetGenerator(BaseAssetGenerator):
    def __init__(self):
        super().__init__(
            output_dir=Path("./generated_assets"),
            seeds=SEEDS,
            brand_colors=BRAND_COLORS
        )
        self.asset_type = "image"
        
    # Only define GENERATION_QUEUE - everything else inherited!
    
GENERATION_QUEUE = [
    # Asset definitions only
]

if __name__ == "__main__":
    generator = ImageAssetGenerator()
    generator.run()
```

**Benefits**:
- Reduces 11 files from ~300-500 lines each to ~100-150 lines each
- Single place to fix bugs
- Easier to add new features
- Better testing capabilities
- Consistent behavior across all generators

---

### Opportunity 2: Consolidate Configuration (RECOMMENDED)
**Impact**: Eliminates ~550 lines of duplicate code  
**Effort**: Low (1 hour)

#### Create Shared Configuration Module:
```python
# generator_config.py

"""Shared configuration for all asset generators"""

from pathlib import Path

# Consistency seeds for different asset categories
SEEDS = {
    "SEED_001": 42,      # B-roll (can vary)
    "SEED_002": 123456,  # Infographics (MUST match)
    "SEED_003": 789012,  # Motion graphics (brand)
    "SEED_004": 345678,  # UI overlays (template)
}

# Brand color palette (reference for prompts)
BRAND_COLORS = {
    "primary_dark": "#1a1a2e",
    "accent_blue": "#00d4ff",
    "accent_purple": "#7b2cbf",
    "secondary_teal": "#00bfa5",
    "highlight_orange": "#ff6b35",
    "text_white": "#ffffff",
}

# Common imports
def check_fal_client():
    """Check if fal_client is installed"""
    try:
        import fal_client
        return True
    except ImportError:
        print("❌ fal_client not installed. Run: pip install fal-client")
        return False
```

**Benefits**:
- Single source of truth for configuration
- Easy to update colors/seeds across all generators
- Reduces risk of inconsistencies

---

### Opportunity 3: Extract Common Utilities (RECOMMENDED)
**Impact**: Better code organization  
**Effort**: Low (1-2 hours)

#### Enhance `asset_utils.py` with common functions:
```python
# asset_utils.py (additions)

def download_image(url: str, save_path: Path) -> bool:
    """Common image download logic"""
    import urllib.request
    try:
        urllib.request.urlretrieve(url, save_path)
        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def save_metadata(metadata: Dict, path: Path):
    """Common metadata saving logic"""
    with open(path, 'w') as f:
        json.dump(metadata, f, indent=2)

def check_api_key() -> str:
    """Check and return API key"""
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        print("\n❌ ERROR: FAL_KEY environment variable not set")
        print("   Set it with: export FAL_KEY='your-api-key-here'")
        raise ValueError("FAL_KEY not set")
    return api_key
```

---

## Additional Issues Identified

### Issue 1: Inconsistent Asset Type Naming
**Files**: `BatchAssetGeneratorGraphics.py`, `BatchAssetGeneratorImages.py`, `BatchAssetGeneratorIcons.py`

In `generate_asset()` function, the asset_type varies:
- Images: `asset_type="image"` (line 249)
- Graphics: `asset_type="graphic"` (line 285)  
- Icons: `asset_type="icon"` (line 287)

**Recommendation**: Use consistent plural forms: `"images"`, `"graphics"`, `"icons"`

---

### Issue 2: Video Generator Uses Different Pattern
**File**: `BatchAssetGeneratorVideo.py`

Uses `generate_video()` instead of `generate_asset()`, breaking the pattern.

**Recommendation**: Rename to `generate_asset()` for consistency, or have base class support both image and video generation.

---

### Issue 3: Missing Error Handling Consistency
Some generators check for empty queue:
```python
if not queue:
    print("\n⚠️  QUEUE IS EMPTY...")
    return []
```

Others don't.

**Recommendation**: Add consistent validation in base class.

---

## Migration Strategy (If Implementing Refactoring)

### Phase 1: Create Base Infrastructure (No Breaking Changes)
1. Create `base_asset_generator.py` with common logic
2. Create `generator_config.py` with shared configuration
3. Add tests for base functionality

### Phase 2: Migrate One Generator (Proof of Concept)
1. Start with simplest: `BatchAssetGeneratorIcons.py`
2. Refactor to use base class
3. Verify functionality
4. Document learnings

### Phase 3: Migrate Remaining Generators
1. Migrate in order of complexity
2. Test each migration
3. Keep old files as backup until fully verified

### Phase 4: Cleanup
1. Remove old duplicate code
2. Update documentation
3. Add integration tests

---

## Testing Recommendations

After any refactoring:
1. Test each generator independently
2. Verify output files are identical to originals
3. Test with actual FAL_KEY and API calls
4. Verify manifest generation
5. Test error scenarios (missing API key, failed generation, etc.)

---

## Estimated Impact of Full Refactoring

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total Lines of Code | ~4,000 | ~2,000 | 50% reduction |
| Duplicate Code | ~2,000 lines | ~0 lines | 100% elimination |
| Files to Modify for Bug Fix | 11 files | 1 file | 91% reduction |
| Maintainability Score | Low | High | Significant |
| Test Coverage Potential | Limited | Excellent | Major improvement |

---

## Conclusion

The codebase has **significant code duplication** (~2,000 lines across 11 files) that can be eliminated through object-oriented refactoring. The recommended approach is to:

1. ✅ **Create a base class** to consolidate common logic
2. ✅ **Extract shared configuration** to a separate module  
3. ✅ **Enhance utility functions** in `asset_utils.py`

This refactoring would reduce maintenance burden, improve code quality, and make it easier to add new generators in the future.

---

**Priority**: HIGH  
**Estimated Effort**: 6-8 hours for complete refactoring  
**Risk**: Low (can be done incrementally with parallel testing)  
**ROI**: Very High (50% code reduction, much easier maintenance)

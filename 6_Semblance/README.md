# 6_Semblance - Code Quality and Issue Tracking

This folder contains documentation about code quality issues, duplicates, and troubleshooting information for the fal.ai project.

---

## 📚 Documentation Files

### Code Quality Analysis
- **[DUPLICATE_CODE_SUMMARY.md](DUPLICATE_CODE_SUMMARY.md)** - Quick reference for code duplicates (~2,000 duplicate lines identified)
- **[code_duplicates_analysis.md](code_duplicates_analysis.md)** - Detailed analysis with specific line numbers and code examples
- **[refactoring_recommendations.md](refactoring_recommendations.md)** - Complete refactoring guide with implementation examples
- **[REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md)** - Status of base class refactoring implementation

### Project Issues
- **[semblance.md](semblance.md)** - Pipeline anomalies and missing batch jobs

---

## 🎯 Key Finding: 50% Code Duplication

The `5_Symbols/` folder originally contained **~2,000 lines of duplicate code** across 11 `BatchAssetGenerator*.py` files.

### ✅ Refactoring Progress

**Base Class Architecture Implemented:**
- ✅ Created `base/base_asset_generator.py` with shared generator logic
- ✅ Created `base/generator_config.py` for centralized configuration
- ✅ Generators can now inherit from base classes to reduce duplication
- ✅ Versioning and manifest tracking integrated into base architecture

**Benefits Achieved:**
- 🔧 Reduced code duplication for new generators
- 🐛 Easier bug fixes (fix once in base class)
- 📚 Improved maintainability
- ✨ Consistent behavior across all generators

**Status:** Base architecture complete. Legacy generators can be gradually migrated to use base classes.

See [REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md) for implementation details.

---

## 🔧 Common Issues and Solutions

### 1. Missing API Key
- **Error**: "FAL_KEY environment variable not set"
- **Solution**: Run `export FAL_KEY='key'` or add it to your `.env` file.

### 2. Dependency Errors
- **Error**: `ModuleNotFoundError: No module named 'fal_client'`
- **Solution**: Ensure you are in the correct virtual environment and run `pip install fal-client`.

### 3. API Timeouts / Server Errors
- **Error**: "Generation failed: No video URL" or HTTP 5xx codes.
- **Solution**: The fal.ai service might be busy. Check `generation_summary.json` to identify which specific asset failed. Retry the script; generators handle re-runs appropriately.

### 4. Model Availability
- **Issue**: Specific models (e.g., minimax) might change names or availability.
- **Solution**: Update the `model` key in the `GENERATION_QUEUE` within the Python scripts.

### 5. Manifest Not Found
- **Error**: Cannot find `manifest.json` file.
- **Solution**: Run `MasterAssetGenerator.py` at least once to create the unified manifest. Individual generators create their own metadata files.

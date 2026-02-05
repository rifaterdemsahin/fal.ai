# 6_Semblance - Code Quality and Issue Tracking

This folder contains documentation about code quality issues, duplicates, and troubleshooting information for the fal.ai project.

---

## 📚 Documentation Files

### Code Quality Analysis
- **[DUPLICATE_CODE_SUMMARY.md](DUPLICATE_CODE_SUMMARY.md)** - Quick reference for code duplicates (~2,000 duplicate lines identified)
- **[code_duplicates_analysis.md](code_duplicates_analysis.md)** - Detailed analysis with specific line numbers and code examples
- **[refactoring_recommendations.md](refactoring_recommendations.md)** - Complete refactoring guide with implementation examples

### Project Issues
- **[semblance.md](semblance.md)** - Pipeline anomalies and missing batch jobs

---

## 🎯 Key Finding: 50% Code Duplication

The `5_Symbols/` folder contains **~2,000 lines of duplicate code** across 11 `BatchAssetGenerator*.py` files. Refactoring to use a base class pattern would:
- Reduce codebase by 67%
- Cut bug fix effort by 91%
- Improve maintainability significantly

See [DUPLICATE_CODE_SUMMARY.md](DUPLICATE_CODE_SUMMARY.md) for quick overview.

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
- **Solution**: The fal.ai service might be busy. The scripts save a `generation_summary.json`—check this to identify which specific asset failed. Retry the script; logically designed scripts should handle re-runs (checking for existing files, though currently overwrite might be default).

### 4. Model Availability
- **Issue**: Specific models (e.g., minimax) might change names or availability.
- **Solution**: Update the `model` key in the `GENERATION_QUEUE` within the Python scripts.

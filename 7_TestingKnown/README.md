### 7_Testing - Validation

**Validation Strategy**:

1.  **Automated Unit Tests**:
    *   **`test_asset_utils.py`**: 13 unit tests for asset utilities
        - Tests for filename generation and standardization
        - Scene number extraction
        - Description cleaning and sanitization
        - Manifest tracking functionality
    *   **Test Status**: ✅ 13/13 tests passing
    *   **Run Command**: `python 5_Symbols/test_asset_utils.py`

2.  **Integration Tests**:
    *   **`test_integration.py`**: End-to-end workflow validation
        - Tests complete asset generation pipeline
        - Validates filename format compliance
        - Verifies manifest structure and content
        - Ensures cross-generator consistency
    *   **Test Status**: ✅ All integration tests passing
    *   **Run Command**: `python 5_Symbols/test_integration.py`

3.  **Runtime Checks**:
    *   Scripts report `✅ Successful` or `❌ Failed` counts at the end of execution.
    *   A `generation_summary.json` is created in the output directory detailing every attempt.
    *   Manifest tracking provides complete asset audit trail.

4.  **Manual Verification** (The "Reasonable Unknown"):
    *   **Visual Check**: Open generated MP4/PNG files. Verify they match the prompt's intent (e.g., "Empty UK Streets" should look like UK streets).
    *   **Technical Check**: Ensure files are not 0 bytes. Check resolution (e.g., 1080p, 4k) and aspect ratio (16:9).
    *   **Audio Check**: Listen for glitches or hallucinations in generated audio.
    *   **Naming Check**: Verify standardized naming convention is followed (`{scene:03d}_{type}_{desc}_v{version}.{ext}`).

5.  **Integration Test with Video Editor**:
    *   Import a sample generated asset into the target video editor (DaVinci Resolve/Premiere) to ensure codec compatibility.
    *   Verify scene-based organization works correctly.
    *   Test manifest.json for prompt reference during editing.

**Test Coverage Summary**:
- ✅ Unit Tests: 13/13 passing
- ✅ Integration Tests: All passing
- ✅ Filename Convention: Validated
- ✅ Manifest Tracking: Validated
- ✅ Base Class Architecture: Validated
- 📊 Code Quality: Documented in `6_Semblance/`

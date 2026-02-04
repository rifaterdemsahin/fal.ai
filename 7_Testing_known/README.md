### 7_Testing - Validation

**Validation Strategy**:

1.  **Automated Checks**:
    *   Scripts report `✅ Successful` or `❌ Failed` counts at the end of execution.
    *   A `generation_summary.json` is created in the output directory detailing every attempt.

2.  **Manual Verification** (The "Reasonable Unknown"):
    *   **Visual Check**: Open generated MP4/PNG files. Verify they match the prompt's intent (e.g., "Empty UK Streets" should look like UK streets).
    *   **Technical Check**: Ensure files are not 0 bytes. Check resolution (e.g., 1080p, 4k) and aspect ratio (16:9).
    *   **Audio Check**: Listen for glitches or hallucinations in generated audio.

3.  **Integration Test**:
    *   Import a sample generated asset into the target video editor (Premiere/Davinci/Remotion) to ensure codec compatibility.

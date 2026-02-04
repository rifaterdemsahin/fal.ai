### 4_Formula - Guides and Best Practices

**Setup Guide**:
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    # OR individual install
    pip install fal-client
    ```
2.  **Configuration**:
    - Ensure your `FAL_KEY` is set in your environment:
      ```bash
      export FAL_KEY="your-api-key-here"
      ```
    - Verify `.env` file exists if using `dotenv` loading.

**Running Generators**:
Navigate to the project root and run specific modules:
```bash
python 5_Symbols/BatchAssetGeneratorVideo.py
python 5_Symbols/BatchAssetGeneratorMusic.py
```

**Best Practices**:
- **Prioritization**: Use the `priority` flag (HIGH, MEDIUM, LOW) in generation queues to manage API costs and time.
- **Metadata**: Always check the generated JSON metadata files to audit the prompts used for each asset.
- **Cool-down**: Scripts include automatic delays (cool-down) to avoid rate limiting; do not remove these for large batches.

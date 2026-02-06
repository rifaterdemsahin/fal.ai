# 🔒 GitHub Repository Secrets Formula

To automate the Bulk Illustration Generator workflow using GitHub Actions, you must securely store your API keys as repository secrets.

## 🔗 Quick Link

[**Manage Repository Secrets**](https://github.com/rifaterdemsahin/fal.ai/settings/secrets/actions)

## 🔑 Required Secrets

| Secret Name | Description | Required For |
| :--- | :--- | :--- |
| `FAL_KEY` | Your fal.ai API key. | `illustrate_image` (fal.ai transformation) |
| `GOOGLE_API_KEY` | Google Custom Search JSON API Key. | `get_google_image` (Image search) |
| `GOOGLE_CSE_ID` | Google Custom Search Engine ID (CX). | `get_google_image` (Image search) |

## 🛠️ Steps to Add Secrets

1. **Click the Link**: Go to [GitHub Secrets Settings](https://github.com/rifaterdemsahin/fal.ai/settings/secrets/actions).
2. **New Secret**: Click on the **New repository secret** button.
3. **Enter Details**:
    * **Name**: Enter the name (e.g., `FAL_KEY`).
    * **Secret**: Paste your API key value.
4. **Save**: Click **Add secret**.

## 🏗️ Using Secrets in GitHub Actions

Reference these in your YAML workflows:

```yaml
- name: Run Bulk Illustration Generator
  env:
    FAL_KEY: ${{ secrets.FAL_KEY }}
  run: |
    python 5_Symbols/BulkIllustrationGenerator.py
```

## 💻 Local Development vs. Remote Secrets

* **Remote (GitHub Actions)**: Uses **Secrets**.
* **Local (Your Computer)**: Uses `.env` file.

**⚠️ IMPORTANT:**

* **NEVER** push your `.env` file to GitHub.
* The `.env` file is in your `.gitignore` by default.
* For local runs, create a `.env` file in the root directory:

    ```env
    FAL_KEY=your_key_here
    ```

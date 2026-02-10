# 🔑 Setting Up FAL_API_KEY for Music Generation

This guide explains how to set up your fal.ai API key to enable actual MP3 music generation.

## Quick Start (Local Execution)

### 1. Get Your API Key

1. Visit [https://fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)
2. Sign up or log in to your fal.ai account
3. Create a new API key
4. Copy the key (it looks like: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### 2. Run the Music Generator Locally

```bash
# Set your API key (replace with your actual key)
export FAL_API_KEY='your-api-key-here'

# Run the music generator for Feb 1 video
python3 run_music_generator_feb1.py
```

This will:

- ✅ Connect to fal.ai API
- ✅ Generate 3 music tracks (47 seconds each)
- ✅ Download MP3 files to `3_Simulation/Feb1Youtube/generated_music/`
- ✅ Create metadata JSON files
- ✅ Generate summary report

**Cost:** ~$0.06 USD (3 tracks × $0.02/track)

## GitHub Actions Setup (Automated Execution)

To run music generation automatically via GitHub Actions:

### 1. Add FAL_API_KEY as a GitHub Secret

1. Go to your repository: `https://github.com/rifaterdemsahin/fal.ai`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `FAL_API_KEY`
5. Value: Your fal.ai API key
6. Click **Add secret**

### 2. Run the Workflow

#### Option A: Manual Trigger

1. Go to **Actions** tab
2. Select **"Batch Asset Generator - Music"** workflow
3. Click **"Run workflow"**
4. Choose branch and options
5. Click **"Run workflow"**

#### Option B: Automatic Trigger

The workflow runs automatically when you:

- Push changes to `5_Symbols/BatchAssetGeneratorMusic.py`
- Push changes to `.github/workflows/batch-asset-generator-music.yml`

### 3. Download Generated Files

After the workflow completes:

**Option A: From Artifacts**

1. Go to the workflow run page
2. Scroll to **Artifacts** section
3. Download **generated-music.zip**
4. Extract to get your MP3 files

**Option B: From Git (if commit_and_push enabled)**

```bash
git pull origin main
cd 5_Symbols/generated_music/
ls *.mp3
```

## Output Files

Once generated, you'll have:

```
3_Simulation/Feb1Youtube/generated_music/
├── tech_innovation_background.mp3      # 47 seconds, HIGH priority
├── tech_innovation_background.json     # Metadata
├── cta_energy_build.mp3                # 47 seconds, HIGH priority
├── cta_energy_build.json               # Metadata
├── screen_recording_bed.mp3            # 47 seconds, MEDIUM priority
├── screen_recording_bed.json           # Metadata
└── generation_summary.json             # Complete summary
```

## Troubleshooting

### Error: "FAL_API_KEY environment variable not set"

**Local Execution:**

```bash
# Make sure you exported the key
echo $FAL_API_KEY
# Should show your key, if empty, export it again
export FAL_API_KEY='your-actual-key-here'
```

**GitHub Actions:**

- Verify the secret is set in repository settings
- Secret name must be exactly `FAL_API_KEY` (case-sensitive)
- Re-run the workflow after adding the secret

### Error: "Authentication failed" or "Invalid API key"

- Check that you copied the complete API key
- Verify the key is still active at [https://fal.ai/dashboard/keys](https://fal.ai/dashboard/keys)
- Try generating a new key if the old one expired

### Error: "Input should be less than or equal to 47"

- This issue has been fixed in the current code
- All tracks are now set to 47 seconds (API maximum)
- Update to the latest code: `git pull origin copilot/run-music-generator-feb-1-video`

### MP3 Files Not Downloaded

Check that:

1. The generation completed successfully (check `generation_summary.json`)
2. You have write permissions to the output directory
3. Your internet connection is stable for downloading

## Validation Before Running

Test your configuration without using API credits:

```bash
# Validate configuration (no API calls)
python3 validate_music_config.py

# Run dry-run simulation (no API calls)
python3 run_music_generator_dryrun.py
```

Both commands will verify your setup without incurring any costs.

## Security Notes

⚠️ **Never commit your FAL_API_KEY to git!**

- Don't add it to `.env` files that are tracked
- Don't hardcode it in Python scripts
- Use environment variables or GitHub secrets only
- The `.gitignore` should exclude any files with secrets

## Cost Estimation

| Item | Cost per Track | Total for 3 Tracks |
|------|----------------|-------------------|
| stable-audio generation | $0.02 | $0.06 |

Total estimated cost: **$0.06 USD**

## Next Steps

After successful generation:

1. **Verify the files:**

   ```bash
   ls -lh 3_Simulation/Feb1Youtube/generated_music/*.mp3
   ```

2. **Test the audio:**
   - Play the MP3 files to ensure quality
   - Check they're 47 seconds long
   - Verify they match the prompts

3. **Import to DaVinci Resolve:**
   - See `RUN_MUSIC_GENERATOR.md` for integration guide
   - Use the generated tracks in your Feb 1 video project

## Support

- For fal.ai API issues: [https://fal.ai/docs](https://fal.ai/docs)
- For repository issues: Open an issue on GitHub
- Documentation: See `RUN_MUSIC_GENERATOR.md` for detailed usage

---

**Last Updated:** 2026-02-06  
**Status:** Ready to generate with valid FAL_API_KEY

**Note:** The scripts also support `FAL_KEY` for backwards compatibility, but `FAL_API_KEY` is the preferred variable name to match the repository secret.

## 🎬 Usecase in Weekly Artifact Generation

This formula ensures the environment is correctly authenticated to generate assets.

- **Role**: Authentication setup guide.
- **Input**: User's FAL.AI API key.
- **Output**: configured `.env` file or environment variable.
- **Benefit**: Enables all other generators to function; without this, no assets can be created. Required step for any new team member or environment.

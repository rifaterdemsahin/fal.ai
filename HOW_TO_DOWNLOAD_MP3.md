# Downloading MP3 Files: Complete Guide

This guide specifically addresses how to generate and download actual MP3 music files (not just JSON metadata).

## The Problem

The dry-run mode only creates JSON metadata files. To get actual MP3 audio files, you need to:
1. Have a valid fal.ai API key
2. Run the generator with the API key set
3. The generator will call the fal.ai API and download the MP3s

## Solution: 3 Ways to Get MP3 Files

### Option 1: Quick Start Script (Easiest) ⭐

```bash
# Run the interactive setup script
./generate_music_with_api.sh
```

This script will:
- ✅ Check for dependencies
- ✅ Guide you through API key setup
- ✅ Validate configuration
- ✅ Run generation with confirmation
- ✅ Download MP3 files automatically
- ✅ Show you where the files are saved

**No FAL_KEY?** The script will help you get one and set it up.

### Option 2: Manual Execution

```bash
# 1. Get your API key from https://fal.ai/dashboard/keys

# 2. Set the environment variable
export FAL_KEY='your-actual-api-key-here'

# 3. Install dependencies (if not already done)
pip install -r requirements.txt

# 4. Run the music generator
python3 run_music_generator_feb1.py
```

This will:
- Connect to fal.ai API
- Generate 3 music tracks (47 seconds each)
- Download MP3 files to `3_Simulation/Feb1Youtube/generated_music/`
- Create JSON metadata alongside each MP3

### Option 3: GitHub Actions (Automated)

For automated generation without local execution:

1. **Set up the secret:**
   - Go to repository Settings → Secrets → Actions
   - Add new secret: `FAL_KEY` with your fal.ai API key

2. **Run the workflow:**
   - Go to Actions tab
   - Select "Batch Asset Generator - Music"
   - Click "Run workflow"
   - Wait for completion

3. **Download the MP3s:**
   - From workflow run page, download the "generated-music" artifact
   - OR if committed to git: `git pull` to get the files

## What You'll Get

After successful generation:

```
3_Simulation/Feb1Youtube/generated_music/
├── 🎵 tech_innovation_background.mp3      (47 seconds) ← ACTUAL MP3
├── 📄 tech_innovation_background.json     (metadata)
├── 🎵 cta_energy_build.mp3                (47 seconds) ← ACTUAL MP3  
├── 📄 cta_energy_build.json               (metadata)
├── 🎵 screen_recording_bed.mp3            (47 seconds) ← ACTUAL MP3
├── 📄 screen_recording_bed.json           (metadata)
└── 📊 generation_summary.json             (summary)
```

**File sizes:** Each MP3 is approximately 750 KB - 1.5 MB (depends on audio complexity)

## Verification

Check that MP3s were actually downloaded:

```bash
# List MP3 files with sizes
ls -lh 3_Simulation/Feb1Youtube/generated_music/*.mp3

# Count MP3 files (should show 3)
ls 3_Simulation/Feb1Youtube/generated_music/*.mp3 | wc -l

# Play a track to test (on Linux with mpg123)
mpg123 3_Simulation/Feb1Youtube/generated_music/tech_innovation_background.mp3

# Check audio file properties (on Linux with ffprobe)
ffprobe -hide_banner 3_Simulation/Feb1Youtube/generated_music/tech_innovation_background.mp3
```

## Common Issues

### Issue: Only JSON files, no MP3s

**Cause:** Generator ran in dry-run mode or generation failed

**Solutions:**
1. Check `generation_summary.json` for errors:
   ```bash
   cat 3_Simulation/Feb1Youtube/generated_music/generation_summary.json
   ```

2. Verify FAL_KEY is set:
   ```bash
   echo $FAL_KEY
   # Should show your key, not empty
   ```

3. Re-run with verbose output:
   ```bash
   python3 run_music_generator_feb1.py 2>&1 | tee generation.log
   ```

### Issue: "FAL_KEY environment variable not set"

**Solution:** You must set the API key before running:

```bash
# This is required - replace with your actual key
export FAL_KEY='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'

# Verify it's set
echo $FAL_KEY

# Now run the generator
python3 run_music_generator_feb1.py
```

### Issue: Generation succeeds but files are 0 bytes

**Cause:** Network issue during download or API returned invalid data

**Solutions:**
1. Check your internet connection
2. Re-run the generation
3. Check the JSON metadata for the download URL and try manual download

### Issue: "Authentication failed" 

**Cause:** Invalid or expired API key

**Solutions:**
1. Verify your key at https://fal.ai/dashboard/keys
2. Generate a new key if needed
3. Make sure you copied the complete key (no spaces/truncation)

## Testing Without Using API Credits

Before making actual API calls:

```bash
# Validate configuration (free, no API calls)
python3 validate_music_config.py

# Run simulation (free, no API calls, creates JSON only)
python3 run_music_generator_dryrun.py
```

Both commands verify your setup without costing anything.

## Cost & Limits

- **Cost per track:** $0.02 USD
- **Total cost for 3 tracks:** $0.06 USD
- **Duration limit:** Maximum 47 seconds per track (API constraint)
- **File format:** MP3
- **Quality:** High quality audio (determined by fal.ai API)

## Security Reminder

🔒 **Protect your API key:**
- Never commit it to git
- Don't share it publicly
- Use environment variables only
- Rotate keys if exposed

## What Happens During Generation

1. **Validation:** Checks configuration (duration ≤ 47s, required fields)
2. **API Request:** Sends prompt to fal.ai stable-audio model
3. **Processing:** fal.ai generates the audio (takes 30-60 seconds per track)
4. **Download:** Fetches the MP3 file from fal.ai's CDN
5. **Save:** Writes MP3 and metadata JSON to output directory
6. **Summary:** Creates generation_summary.json with results

Total time: **2-4 minutes for 3 tracks**

## Next Steps After Getting MP3s

1. **Quality Check:**
   - Play each track
   - Verify it's 47 seconds
   - Check audio matches the prompt description

2. **Import to Video Editor:**
   - DaVinci Resolve: See `RUN_MUSIC_GENERATOR.md`
   - Other editors: Import from `3_Simulation/Feb1Youtube/generated_music/`

3. **Use in Feb 1 Video:**
   - Background music: `tech_innovation_background.mp3`
   - Call to action: `cta_energy_build.mp3`
   - Screen recording: `screen_recording_bed.mp3`

## Getting Help

If you're still having issues:

1. **Check the logs:**
   ```bash
   python3 run_music_generator_feb1.py 2>&1 | tee generation.log
   cat generation.log
   ```

2. **Review documentation:**
   - `SETUP_FAL_KEY.md` - API key setup
   - `RUN_MUSIC_GENERATOR.md` - Complete usage guide
   - `MUSIC_GENERATOR_STATUS.md` - Current status

3. **Check fal.ai status:**
   - Visit https://status.fal.ai/
   - Check for any API outages

4. **Open an issue:**
   - Include the generation.log
   - Include generation_summary.json
   - Describe what you tried

---

**Remember:** The dry-run creates JSON only. For MP3s, you MUST use a valid FAL_KEY.

**Quick command to verify you have MP3s:**
```bash
file 3_Simulation/Feb1Youtube/generated_music/*.mp3
# Should show: "Audio file with ID3 version..." or similar
```

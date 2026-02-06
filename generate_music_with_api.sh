#!/bin/bash
#
# Easy Music Generator Runner for Feb 1 Video
# This script guides you through running the music generator and downloading MP3 files
#

set -e

echo "════════════════════════════════════════════════════════════════════"
echo "  🎵 Music Generator Setup & Execution for Feb 1 Video"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Check if FAL_KEY is set
if [ -z "$FAL_KEY" ]; then
    echo "⚠️  FAL_KEY environment variable is not set"
    echo ""
    echo "To generate actual MP3 files, you need a fal.ai API key."
    echo ""
    echo "Steps to get your API key:"
    echo "  1. Visit: https://fal.ai/dashboard/keys"
    echo "  2. Sign up or log in"
    echo "  3. Create a new API key"
    echo "  4. Copy the key"
    echo ""
    echo "Then run this script with:"
    echo "  export FAL_KEY='your-api-key-here'"
    echo "  ./generate_music_with_api.sh"
    echo ""
    echo "────────────────────────────────────────────────────────────────────"
    echo "Would you like to:"
    echo "  1) Enter your API key now (it will only be used for this session)"
    echo "  2) Run validation/dry-run without API key"
    echo "  3) Exit and set FAL_KEY manually"
    echo ""
    read -p "Choose an option (1/2/3): " choice
    
    case $choice in
        1)
            echo ""
            read -sp "Enter your FAL_KEY: " user_key
            echo ""
            export FAL_KEY="$user_key"
            echo "✅ API key set for this session"
            ;;
        2)
            echo ""
            echo "Running validation and dry-run simulation..."
            echo ""
            python3 validate_music_config.py
            echo ""
            python3 run_music_generator_dryrun.py
            echo ""
            echo "════════════════════════════════════════════════════════════════════"
            echo "✅ Validation and dry-run completed!"
            echo ""
            echo "To generate actual MP3 files, set FAL_KEY and run this script again."
            echo "════════════════════════════════════════════════════════════════════"
            exit 0
            ;;
        3)
            echo ""
            echo "To set FAL_KEY manually, run:"
            echo "  export FAL_KEY='your-api-key-here'"
            echo ""
            exit 0
            ;;
        *)
            echo "Invalid option. Exiting."
            exit 1
            ;;
    esac
fi

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  ✅ FAL_KEY detected"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Check if Python dependencies are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import fal_client" 2>/dev/null; then
    echo "⚠️  fal_client not installed"
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi
echo ""

# Run validation first
echo "════════════════════════════════════════════════════════════════════"
echo "  🔍 Step 1: Validating Configuration"
echo "════════════════════════════════════════════════════════════════════"
echo ""
python3 validate_music_config.py
echo ""

# Ask for confirmation
echo "════════════════════════════════════════════════════════════════════"
echo "  💰 Cost Estimation"
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "  3 tracks × 47 seconds each"
echo "  Estimated cost: \$0.06 USD"
echo ""
echo "────────────────────────────────────────────────────────────────────"
read -p "Proceed with music generation? (yes/no): " confirm

if [ "$confirm" != "yes" ] && [ "$confirm" != "y" ]; then
    echo ""
    echo "❌ Cancelled by user"
    exit 0
fi

# Run the music generator
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  🎵 Step 2: Generating Music (This may take a few minutes)"
echo "════════════════════════════════════════════════════════════════════"
echo ""
python3 run_music_generator_feb1.py

# Check results
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  📊 Step 3: Checking Results"
echo "════════════════════════════════════════════════════════════════════"
echo ""

OUTPUT_DIR="3_Simulation/Feb1Youtube/generated_music"

if [ -f "$OUTPUT_DIR/generation_summary.json" ]; then
    echo "✅ Generation summary found"
    
    # Check for MP3 files
    mp3_count=$(ls -1 "$OUTPUT_DIR"/*.mp3 2>/dev/null | wc -l)
    json_count=$(ls -1 "$OUTPUT_DIR"/*.json 2>/dev/null | wc -l)
    
    echo ""
    echo "📁 Output directory: $OUTPUT_DIR"
    echo "  • MP3 files: $mp3_count"
    echo "  • JSON metadata files: $json_count"
    echo ""
    
    if [ "$mp3_count" -gt 0 ]; then
        echo "🎵 Generated MP3 files:"
        ls -lh "$OUTPUT_DIR"/*.mp3
        echo ""
        echo "════════════════════════════════════════════════════════════════════"
        echo "  ✅ SUCCESS! Music generation complete!"
        echo "════════════════════════════════════════════════════════════════════"
        echo ""
        echo "Your music tracks are ready in:"
        echo "  $OUTPUT_DIR"
        echo ""
        echo "Next steps:"
        echo "  1. Listen to the tracks to verify quality"
        echo "  2. Import into DaVinci Resolve (see RUN_MUSIC_GENERATOR.md)"
        echo "  3. Use in your Feb 1 video project"
        echo ""
    else
        echo "⚠️  No MP3 files found. Check generation_summary.json for errors."
        echo ""
        cat "$OUTPUT_DIR/generation_summary.json"
    fi
else
    echo "❌ Generation summary not found. Something went wrong."
    echo "Check the output above for errors."
fi

echo "════════════════════════════════════════════════════════════════════"

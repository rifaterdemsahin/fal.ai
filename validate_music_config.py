#!/usr/bin/env python3
"""
Music Generator Validation Script
Validates the music generator configuration without making API calls
"""

import sys
from pathlib import Path

# Add 5_Symbols to path
sys.path.insert(0, str(Path(__file__).parent / "5_Symbols"))

# Import the music generator configuration
import BatchAssetGeneratorMusic as music_gen

def validate_configuration():
    """Validate the music generation configuration"""
    print("\n" + "="*60)
    print("🔍 MUSIC GENERATOR CONFIGURATION VALIDATION")
    print("="*60)
    
    issues = []
    warnings = []
    
    # Check the generation queue
    queue = music_gen.GENERATION_QUEUE
    print(f"\n✅ Found {len(queue)} tracks in generation queue")
    
    # Validate each track
    for i, track in enumerate(queue, 1):
        print(f"\n📝 Track {i}: {track.get('name', 'UNNAMED')}")
        print(f"   Priority: {track.get('priority', 'NOT SET')}")
        print(f"   Model: {track.get('model', 'NOT SET')}")
        print(f"   Duration: {track.get('seconds_total', 'NOT SET')}s")
        
        # Check required fields
        required_fields = ['id', 'name', 'prompt', 'model', 'seconds_total']
        for field in required_fields:
            if field not in track:
                issues.append(f"Track {i} ({track.get('name', 'UNNAMED')}): Missing required field '{field}'")
        
        # Check duration limit
        duration = track.get('seconds_total', 0)
        if duration > 47:
            issues.append(f"Track {i} ({track.get('name', 'UNNAMED')}): Duration {duration}s exceeds API limit of 47s")
        elif duration <= 0:
            issues.append(f"Track {i} ({track.get('name', 'UNNAMED')}): Duration must be greater than 0")
        else:
            print(f"   ✅ Duration {duration}s is within API limit (≤47s)")
        
        # Check model
        model = track.get('model', '')
        if 'stable-audio' not in model:
            warnings.append(f"Track {i} ({track.get('name', 'UNNAMED')}): Model '{model}' may not be compatible")
        
        # Check prompt length
        prompt = track.get('prompt', '')
        if len(prompt) < 10:
            warnings.append(f"Track {i} ({track.get('name', 'UNNAMED')}): Prompt is very short ({len(prompt)} chars)")
        elif len(prompt) > 500:
            warnings.append(f"Track {i} ({track.get('name', 'UNNAMED')}): Prompt is very long ({len(prompt)} chars)")
        else:
            print(f"   ✅ Prompt length: {len(prompt)} characters")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 VALIDATION SUMMARY")
    print("="*60)
    
    if not issues and not warnings:
        print("✅ All checks passed! Configuration is valid.")
        print("\nℹ️  Ready to run music generation with:")
        print("   python3 run_music_generator_feb1.py")
        return 0
    
    if warnings:
        print(f"\n⚠️  Found {len(warnings)} warning(s):")
        for warning in warnings:
            print(f"   • {warning}")
    
    if issues:
        print(f"\n❌ Found {len(issues)} critical issue(s):")
        for issue in issues:
            print(f"   • {issue}")
        print("\n❌ Configuration has errors. Please fix before running.")
        return 1
    
    print("\n⚠️  Configuration has warnings but should work.")
    return 0

def main():
    """Main execution"""
    return validate_configuration()

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Test script for Chapter Markers (Audio Generator)
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
symbols_path = project_root / "5_Symbols"
sys.path.append(str(symbols_path))

try:
    from Audio import BatchAssetGeneratorAudio
except ImportError as e:
    print(f"❌ Failed to import BatchAssetGeneratorAudio: {e}")
    sys.exit(1)

def test_marker_generation():
    # Setup paths
    output_dir = project_root / "7_TestingKnown" / "TestOutput" / "generated_assets" / "markers"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a dummy EDL file
    dummy_edl = output_dir / "test_edl.md"
    dummy_edl.write_text("""
### **SCENE 1: HOOK & PROBLEM STATEMENT**
**Duration:** 0:00 - 0:45

### **SCENE 2: THE SOLUTION**
**Duration:** 0:45 - 2:00
""", encoding="utf-8")
    
    output_file = output_dir / "test_markers.txt"

    print(f"📂 Output directory: {output_dir}")
    print("🧪 Starting Chapter Marker Test...")

    # Run the generator
    try:
        BatchAssetGeneratorAudio.generate_chapter_markers(dummy_edl, output_file)
        
        print("\n" + "="*60)
        print("✅ Test Batch Complete")
        print(f"📂 Check results in: {output_file}")
        print("="*60)
        
        if output_file.exists():
             print(f"📄 Markers generated:\n{output_file.read_text()}")
        else:
             print("❌ Failed: Output file not created")
            
    except Exception as e:
        print(f"❌ Error running generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_marker_generation()

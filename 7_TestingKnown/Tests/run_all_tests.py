#!/usr/bin/env python3
import sys
import os
import subprocess
import glob
from pathlib import Path
from datetime import datetime

def run_all_tests():
    # Setup paths
    tests_dir = Path(__file__).resolve().parent
    project_root = tests_dir.parent.parent
    results_file = project_root / "7_TestingKnown" / "TestResults.md"
    
    # helper to check if file is a test
    test_files = sorted([f for f in tests_dir.glob("test_*.py") if f.name != "run_all_tests.py"])
    
    print(f"🚀 Found {len(test_files)} tests to run.")
    print(f"📂 Results will be written to: {results_file}")
    
    results = []
    
    # Environment with FAL_KEY
    env = os.environ.copy()
    
    # We might need to source .env if FAL_KEY is missing, but simpler to assume it's in env
    # or let the user run this script with the env loaded.
    
    total_start_time = datetime.now()
    
    for test_file in test_files:
        print(f"\n🏃 Running {test_file.name}...")
        start_time = datetime.now()
        
        try:
            # Run the test file as a separate process
            # We use the same python interpreter
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                env=env,
                check=False # Don't raise exception on failure, just check return code
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            status = "✅ PASS" if result.returncode == 0 else "❌ FAIL"
            
            # Extract summary (last few lines)
            output_lines = result.stdout.strip().split('\n')
            
            # Try to find meaningful output lines (e.g. "Ran X tests", "OK", "FAILED")
            summary_info = "No output"
            if output_lines:
                # Get last non-empty line
                summary_info = output_lines[-1]
                # If it's just empty or "OK", maybe get the one before
                if len(output_lines) > 1 and (summary_info == "OK" or summary_info == ""):
                    summary_info = output_lines[-2]
            
            if result.returncode != 0:
                 # usage stderr for errors
                 err_lines = result.stderr.strip().split('\n')
                 if err_lines:
                     summary_info = f"Error: {err_lines[-1]}"

            results.append({
                "name": test_file.name,
                "status": status,
                "duration": f"{duration:.2f}s",
                "summary": summary_info
            })
            
            print(f"   result: {status} ({duration:.2f}s)")
            
        except Exception as e:
            print(f"   ❌ Error running {test_file.name}: {e}")
            results.append({
                "name": test_file.name,
                "status": "❌ ERROR",
                "duration": "0.00s",
                "summary": str(e)
            })

    total_duration = (datetime.now() - total_start_time).total_seconds()
    
    # Generate Markdown Table
    print("\n📝 Generiating report...")
    
    md_content = f"# Test Results\n\n"
    md_content += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    md_content += f"**Total Duration:** {total_duration:.2f}s\n\n"
    
    md_content += "| Test File | Status | Duration | Summary |\n"
    md_content += "|-----------|--------|----------|---------|\n"
    
    for res in results:
        # Escape pipes in summary to avoid breaking table
        summary_clean = res['summary'].replace("|", "\\|").replace("\n", " ")
        # Truncate summary if too long
        if len(summary_clean) > 100:
            summary_clean = summary_clean[:97] + "..."
            
        md_content += f"| {res['name']} | {res['status']} | {res['duration']} | {summary_clean} |\n"
    
    md_content += "\n\n## Details\n"
    md_content += "Run specific tests for more details:\n"
    md_content += "```bash\n"
    md_content += "python 7_TestingKnown/Tests/<test_file.py>\n"
    md_content += "```\n"

    with open(results_file, "w") as f:
        f.write(md_content)
        
    print(f"✅ Report saved to {results_file}")

if __name__ == "__main__":
    run_all_tests()

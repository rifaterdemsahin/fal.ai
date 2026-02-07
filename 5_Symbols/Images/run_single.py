
import sys
import os
from pathlib import Path

# Add parent directory to path to find Utils if needed
sys.path.append(str(Path(__file__).resolve().parent))

# Load .env manually from parent directory
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    with open(env_path, "r") as f:
        for line in f:
            if line.strip().startswith("FAL_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
                os.environ["FAL_KEY"] = key
                print("Loaded FAL_KEY")

try:
    from BatchAssetGeneratorImages import generate_asset, load_queue, OUTPUT_DIR
except ImportError:
    print("Error importing BatchAssetGeneratorImages")
    sys.exit(1)

def run():
    if len(sys.argv) < 2:
        print("Usage: python run_single.py <asset_id>")
        print("Example: python run_single.py 12.1")
        
        # List available IDs for convenience
        print("\nAvailable IDs in queue:")
        queue = load_queue()
        for item in queue:
            print(f" - {item.get('id')}: {item.get('name')}")
        return

    target_id = sys.argv[1]
    print(f"Loading queue to find {target_id}...")
    queue = load_queue()
    target = next((x for x in queue if x['id'] == target_id), None)
    
    if target:
        print(f"Found target: {target['name']}")
        # Ask for version optional override? Default to 1 for now or maybe auto-increment logic is in the other script?
        # The generate_asset function takes a version, default 1.
        result = generate_asset(target, OUTPUT_DIR, version=1)
        print("Result:", result)
    else:
        print(f"❌ Target ID {target_id} not found in queue.")

if __name__ == "__main__":
    run()

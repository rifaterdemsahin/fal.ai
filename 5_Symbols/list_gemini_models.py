
import os
import urllib.request
import json
from pathlib import Path

# Load .env manually to get key
env_path = Path(__file__).resolve().parent / "5_Symbols" / ".env"
api_key = None
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            if 'GOOGLE_API_KEY=' in line:
                key, value = line.split('=', 1)
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                api_key = value
                break

if not api_key:
    print("No GOOGLE_API_KEY found in .env")
    exit(1)

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        print(f"Found {len(data.get('models', []))} models:")
        for model in data.get('models', []):
            print(f"- {model['name']}")
            if 'image' in model['name'] or 'imagen' in model['name']:
                print(f"  ^^ Potential Image Model ^^")
except Exception as e:
    print(f"Error listing models: {e}")

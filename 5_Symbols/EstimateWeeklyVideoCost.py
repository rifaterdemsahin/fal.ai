import json
import os
import argparse
from collections import defaultdict

# Pricing Estimates (USD per generation)
PRICING = {
    "fal-ai/flux/schnell": 0.003,
    "fal-ai/flux/dev": 0.03,
    "fal-ai/minimax/video-01": 0.70,
    "fal-ai/stable-audio": 0.05,
    "fal-ai/luma-dream-machine": 0.80,  # Estimated
    "fal-ai/fast-sdxl": 0.002,
    "fal-ai/hyper-sd": 0.002,
}

DEFAULT_PRICE = 0.05 # Fallback price if model not found

def estimate_cost(folder_path):
    config_path = os.path.join(folder_path, 'assets_config.json')
    
    if not os.path.exists(config_path):
        print(f"Error: assets_config.json not found in {folder_path}")
        return

    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    total_cost = 0.0
    category_costs = defaultdict(float)
    model_counts = defaultdict(int)

    print(f"\n--- Cost Estimate for: {config_path} ---\n")

    for category, items in data.items():
        if not isinstance(items, list):
            continue
            
        print(f"Processing Category: {category} ({len(items)} items)")
        
        for item in items:
            model = item.get('model', 'unknown')
            price = PRICING.get(model, DEFAULT_PRICE)
            
            # Special logic for video duration if pricing depended on it (assuming flat rate per generation for now for simplicity, or per 5s)
            # Minimax is often priced per second or per generation. Let's assume the pricing constant is for a standard huge generation.
            
            cost = price
            total_cost += cost
            category_costs[category] += cost
            model_counts[model] += 1
            
            # Optional: Print detail for expensive items
            if cost > 0.10:
               print(f"  - {item.get('name', 'Unnamed')}: ${cost:.3f} ({model})")

    print("\n--- Breakdown by Category ---")
    for category, cost in category_costs.items():
        print(f"{category.ljust(15)}: ${cost:.2f}")

    print("\n--- Breakdown by Model ---")
    for model, count in model_counts.items():
        price = PRICING.get(model, DEFAULT_PRICE)
        print(f"{model.ljust(30)}: {count} x ${price:.3f} = ${count * price:.2f}")

    print(f"\n===========================================")
    print(f"TOTAL ESTIMATED WEEKLY COST: ${total_cost:.2f}")
    print(f"===========================================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate weekly video production costs based on assets_config.json")
    parser.add_argument("folder", nargs="?", default=".", help="Folder containing assets_config.json")
    
    args = parser.parse_args()
    estimate_cost(args.folder)

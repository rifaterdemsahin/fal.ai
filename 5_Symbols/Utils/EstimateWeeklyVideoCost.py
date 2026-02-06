
import json
import os
import argparse
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Pricing Estimates (USD per generation)
PRICING = {
    "fal-ai/flux/schnell": 0.003,
    "fal-ai/flux/dev": 0.03,
    "fal-ai/minimax/video-01": 0.70,
    "fal-ai/stable-audio": 0.05,
    "fal-ai/luma-dream-machine": 0.80,
    "fal-ai/fast-sdxl": 0.002,
    "fal-ai/hyper-sd": 0.002,
}

DEFAULT_PRICE = 0.05  # Fallback price if model not found

def generate_report(folder_path: str) -> None:
    """
    Generates a cost estimation report for the assets in the given folder.
    Saves the report to a 'weekly_reports' subdirectory.
    """
    folder_path = Path(folder_path).resolve()
    config_path = folder_path / 'assets_config.json'
    
    if not config_path.exists():
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
    
    # Store detailed line items for the report
    details = []

    print(f"\n--- Cost Estimate for: {config_path.name} ---\n")

    for category, items in data.items():
        if not isinstance(items, list):
            continue
            
        # print(f"Processing Category: {category} ({len(items)} items)")
        
        for item in items:
            model = item.get('model', 'unknown')
            # specific model override logic if needed, or fuzzy matching
            price = DEFAULT_PRICE
            if model in PRICING:
                price = PRICING[model]
            else:
                # Fuzzy match for things like 'fal-ai/flux/dev' vs just 'flux' if keys were simpler, 
                # but valid keys are full strings. Let's try to match known keys.
                for k, v in PRICING.items():
                    if k in model:
                        price = v
                        break
            
            cost = price
            total_cost += cost
            category_costs[category] += cost
            model_counts[model] += 1
            
            details.append({
                "category": category,
                "name": item.get('name', 'Unnamed'),
                "model": model,
                "cost": cost
            })

    # Prepare Markdown Content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    md_lines = []
    md_lines.append(f"# Weekly Video Cost Estimate")
    md_lines.append(f"**Generated:** {timestamp}")
    md_lines.append(f"**Source:** `{config_path}`")
    md_lines.append("")
    md_lines.append(f"## Total Estimated Cost: **${total_cost:.2f}**")
    md_lines.append("")
    
    md_lines.append("## Breakdown by Category")
    md_lines.append("| Category | Count | Cost |")
    md_lines.append("| :--- | :--- | :--- |")
    for category, cost in category_costs.items():
        count = sum(1 for d in details if d['category'] == category)
        md_lines.append(f"| {category} | {count} | ${cost:.2f} |")
    md_lines.append("")

    md_lines.append("## Breakdown by Model")
    md_lines.append("| Model | Count | Unit Price | Total |")
    md_lines.append("| :--- | :--- | :--- | :--- |")
    for model, count in model_counts.items():
        # find price used (may vary if logic changed, but here it's static per model key)
        # We'll just re-lookup or assume consistent.
        price = DEFAULT_PRICE
        if model in PRICING:
            price = PRICING[model]
        else:
             for k, v in PRICING.items():
                    if k in model:
                        price = v
                        break
        md_lines.append(f"| `{model}` | {count} | ${price:.3f} | ${count * price:.2f} |")
    md_lines.append("")
    
    # Save Report
    reports_dir = folder_path / "weekly"
    reports_dir.mkdir(exist_ok=True)
    report_file = reports_dir / f"cost_report_{date_str}.md"
    
    with open(report_file, "w") as f:
        f.write("\n".join(md_lines))
        
    print(f"✅ Report saved to: {report_file}")
    print(f"💰 Total Estimated Cost: ${total_cost:.2f}")
    
    # Output for Master Generator consistency (optional)
    return total_cost

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate weekly video production costs")
    parser.add_argument("folder", nargs="?", default=".", help="Folder containing assets_config.json")
    
    args = parser.parse_args()
    generate_report(args.folder)

#!/usr/bin/env python3
"""
Markdown Presentation to Image Converter
Converts markdown slides to individual chapter marker images
"""

import os
import re
from pathlib import Path
from typing import List, Dict

def parse_markdown_slides(markdown_file: Path) -> List[Dict]:
    """Parse markdown file into individual slides"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by slide separator (---)
    slides = content.split('\n---\n')

    parsed_slides = []
    chapter_num = 0

    for slide in slides:
        slide = slide.strip()
        if not slide or slide.startswith('#') and 'Chapter Markers' in slide:
            continue

        # Extract chapter information
        timestamp_match = re.search(r'\*\*Timestamp:\*\*\s*(\d{2}:\d{2})', slide)
        chapter_match = re.search(r'##\s+Chapter\s+(\d+):\s+(.+)', slide)

        if chapter_match:
            chapter_num = int(chapter_match.group(1))
            chapter_title = chapter_match.group(2).strip()
            timestamp = timestamp_match.group(1) if timestamp_match else "00:00"

            # Extract subtitle lines (everything after the first heading)
            lines = slide.split('\n')
            subtitle = ""
            for i, line in enumerate(lines):
                if line.startswith('**Timestamp:**'):
                    continue
                if i > 0 and not line.startswith('#') and not line.startswith('**'):
                    if subtitle:
                        subtitle += " | "
                    subtitle += line.strip()

            parsed_slides.append({
                'chapter_num': chapter_num,
                'title': chapter_title,
                'subtitle': subtitle.strip(),
                'timestamp': timestamp,
                'full_text': f"Chapter {chapter_num}: {chapter_title}"
            })

    return parsed_slides

def generate_html_slide(slide: Dict, output_dir: Path, theme: str = "dark") -> str:
    """Generate HTML file for a single slide"""
    chapter_num = slide['chapter_num']
    title = slide['title']
    subtitle = slide['subtitle']
    timestamp = slide['timestamp']

    # Color schemes
    if theme == "dark":
        bg_color = "#0f0f23"
        primary_color = "#00d9ff"
        secondary_color = "#a855f7"
        text_color = "#ffffff"
        subtitle_color = "#9ca3af"
    else:
        bg_color = "#ffffff"
        primary_color = "#2563eb"
        secondary_color = "#7c3aed"
        text_color = "#1f2937"
        subtitle_color = "#6b7280"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080">
    <title>Chapter {chapter_num}: {title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            width: 1920px;
            height: 1080px;
            background: linear-gradient(135deg, {bg_color} 0%, {bg_color}dd 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            position: relative;
            overflow: hidden;
        }}

        /* Decorative background elements */
        .bg-decoration {{
            position: absolute;
            width: 100%;
            height: 100%;
            z-index: 0;
        }}

        .circle {{
            position: absolute;
            border-radius: 50%;
            opacity: 0.1;
        }}

        .circle-1 {{
            width: 600px;
            height: 600px;
            background: {primary_color};
            top: -300px;
            right: -200px;
            filter: blur(100px);
        }}

        .circle-2 {{
            width: 800px;
            height: 800px;
            background: {secondary_color};
            bottom: -400px;
            left: -300px;
            filter: blur(120px);
        }}

        .content {{
            position: relative;
            z-index: 1;
            text-align: center;
            padding: 80px;
            max-width: 1600px;
        }}

        .chapter-label {{
            font-size: 48px;
            font-weight: 600;
            color: {primary_color};
            letter-spacing: 4px;
            margin-bottom: 40px;
            text-transform: uppercase;
        }}

        .chapter-title {{
            font-size: 120px;
            font-weight: 900;
            color: {text_color};
            line-height: 1.2;
            margin-bottom: 40px;
            text-shadow: 0 0 40px rgba(0, 217, 255, 0.3);
        }}

        .chapter-subtitle {{
            font-size: 42px;
            font-weight: 400;
            color: {subtitle_color};
            line-height: 1.6;
            margin-bottom: 60px;
        }}

        .timestamp {{
            position: absolute;
            bottom: 60px;
            left: 80px;
            font-size: 36px;
            font-weight: 600;
            color: {primary_color};
            padding: 20px 40px;
            background: rgba(0, 217, 255, 0.1);
            border: 2px solid {primary_color};
            border-radius: 12px;
        }}

        .chapter-number {{
            position: absolute;
            top: 60px;
            right: 80px;
            font-size: 200px;
            font-weight: 900;
            color: {primary_color};
            opacity: 0.15;
        }}
    </style>
</head>
<body>
    <div class="bg-decoration">
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
    </div>

    <div class="content">
        <div class="chapter-label">Chapter {chapter_num}</div>
        <h1 class="chapter-title">{title}</h1>
        {f'<p class="chapter-subtitle">{subtitle}</p>' if subtitle else ''}
    </div>

    <div class="timestamp">{timestamp}</div>
    <div class="chapter-number">{chapter_num:02d}</div>
</body>
</html>
"""

    filename = f"chapter_{chapter_num:02d}_{title.lower().replace(' ', '_')}.html"
    output_path = output_dir / filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return str(output_path)

def convert_html_to_image(html_path: str, output_path: str):
    """Convert HTML to PNG using available tools"""
    html_file = Path(html_path)
    output_file = Path(output_path)

    try:
        # Try using playwright/selenium/pyppeteer
        print(f"Converting {html_file.name} to image...")

        # Method 1: Try Playwright (recommended)
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport={'width': 1920, 'height': 1080})
                page.goto(f'file://{html_file.absolute()}')
                page.screenshot(path=output_path, full_page=False)
                browser.close()
                print(f"✅ Created: {output_file.name}")
                return True
        except ImportError:
            print("⚠️  Playwright not installed. Trying alternative...")

        # Method 2: Try imgkit (wkhtmltoimage wrapper)
        try:
            import imgkit
            options = {
                'width': 1920,
                'height': 1080,
                'quality': 100,
            }
            imgkit.from_file(str(html_file), str(output_file), options=options)
            print(f"✅ Created: {output_file.name}")
            return True
        except (ImportError, OSError):
            print("⚠️  imgkit not available. Trying alternative...")

        # Method 3: Display instructions for manual conversion
        print(f"\n⚠️  No automatic converter available.")
        print(f"Please install one of these tools:")
        print(f"  1. Playwright: pip install playwright && playwright install chromium")
        print(f"  2. imgkit: pip install imgkit (requires wkhtmltoimage)")
        print(f"\nHTML file saved at: {html_file}")
        print(f"Expected output: {output_file}\n")
        return False

    except Exception as e:
        print(f"❌ Error converting {html_file.name}: {e}")
        return False

def main():
    """Main execution"""
    script_dir = Path(__file__).parent
    markdown_file = script_dir / "chapter_markers.md"
    output_dir = script_dir / "generated_chapter_markers_md"

    # Create output directory
    output_dir.mkdir(exist_ok=True)
    html_dir = output_dir / "html"
    html_dir.mkdir(exist_ok=True)
    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True)

    print("="*60)
    print("🎨 MARKDOWN CHAPTER MARKERS TO IMAGE CONVERTER")
    print("="*60)
    print(f"\n📄 Input: {markdown_file}")
    print(f"📁 Output: {output_dir}")

    # Parse markdown
    print(f"\n🔍 Parsing markdown slides...")
    slides = parse_markdown_slides(markdown_file)
    print(f"✅ Found {len(slides)} chapter markers")

    # Generate HTML files
    print(f"\n🎨 Generating HTML slides...")
    html_files = []
    for slide in slides:
        html_path = generate_html_slide(slide, html_dir, theme="dark")
        html_files.append(html_path)
        print(f"  ✓ Chapter {slide['chapter_num']}: {slide['title']}")

    # Convert to images
    print(f"\n🖼️  Converting HTML to images...")
    successful = 0
    failed = 0

    for i, html_path in enumerate(html_files):
        slide = slides[i]
        image_filename = f"chapter_{slide['chapter_num']:02d}_{slide['title'].lower().replace(' ', '_')}.png"
        image_path = images_dir / image_filename

        if convert_html_to_image(html_path, str(image_path)):
            successful += 1
        else:
            failed += 1

    # Summary
    print("\n" + "="*60)
    print("📊 CONVERSION SUMMARY")
    print("="*60)
    print(f"✅ Successful: {successful}/{len(slides)}")
    print(f"❌ Failed: {failed}/{len(slides)}")
    print(f"\n📁 HTML files: {html_dir}")
    print(f"📁 Images: {images_dir}")
    print("\n✅ Done!")

if __name__ == "__main__":
    main()

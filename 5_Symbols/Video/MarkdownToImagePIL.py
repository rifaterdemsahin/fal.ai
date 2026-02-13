#!/usr/bin/env python3
"""
Markdown Presentation to Image Converter using PIL
Converts markdown slides to individual chapter marker images using Pillow
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("❌ Pillow not installed. Run: pip3 install --user Pillow")
    exit(1)

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
            subtitle_lines = []
            for i, line in enumerate(lines):
                if line.startswith('**Timestamp:**'):
                    continue
                if i > 0 and not line.startswith('#') and not line.startswith('**'):
                    line = line.strip()
                    if line:
                        subtitle_lines.append(line)

            subtitle = ' | '.join(subtitle_lines)

            parsed_slides.append({
                'chapter_num': chapter_num,
                'title': chapter_title,
                'subtitle': subtitle.strip(),
                'timestamp': timestamp,
                'full_text': f"Chapter {chapter_num}: {chapter_title}"
            })

    return parsed_slides

def create_gradient_background(width: int, height: int, color1: Tuple, color2: Tuple) -> Image:
    """Create a gradient background"""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (y / height)))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def add_glow_effect(image: Image, position: Tuple, text: str, font, color: Tuple, blur_radius: int = 10) -> Image:
    """Add a glow effect to text"""
    # Create a larger temporary image for the glow
    glow = Image.new('RGBA', (image.width + 100, image.height + 100), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    # Adjust position for the larger canvas
    glow_pos = (position[0] + 50, position[1] + 50)

    # Draw text multiple times with decreasing opacity for glow effect
    for i in range(blur_radius):
        alpha = int(255 * (1 - i / blur_radius) * 0.3)
        glow_color = (*color, alpha)
        offset = blur_radius - i
        glow_draw.text((glow_pos[0] - offset, glow_pos[1]), text, font=font, fill=glow_color, anchor="mm")
        glow_draw.text((glow_pos[0] + offset, glow_pos[1]), text, font=font, fill=glow_color, anchor="mm")
        glow_draw.text((glow_pos[0], glow_pos[1] - offset), text, font=font, fill=glow_color, anchor="mm")
        glow_draw.text((glow_pos[0], glow_pos[1] + offset), text, font=font, fill=glow_color, anchor="mm")

    # Apply blur
    glow = glow.filter(ImageFilter.GaussianBlur(blur_radius))

    # Paste glow onto original image
    image.paste(glow, (-50, -50), glow)

    return image

def generate_chapter_image(slide: Dict, output_path: Path, theme: str = "dark") -> bool:
    """Generate chapter marker image using PIL"""
    # Image dimensions (1920x1080 - Full HD)
    width, height = 1920, 1080

    chapter_num = slide['chapter_num']
    title = slide['title']
    subtitle = slide['subtitle']
    timestamp = slide['timestamp']

    # Color schemes
    if theme == "dark":
        bg_color1 = (15, 15, 35)      # Dark blue-black
        bg_color2 = (25, 15, 45)      # Slightly lighter purple-black
        primary_color = (0, 217, 255)  # Cyan
        secondary_color = (168, 85, 247)  # Purple
        text_color = (255, 255, 255)   # White
        subtitle_color = (156, 163, 175)  # Gray
    else:
        bg_color1 = (255, 255, 255)
        bg_color2 = (240, 240, 250)
        primary_color = (37, 99, 235)
        secondary_color = (124, 58, 237)
        text_color = (31, 41, 55)
        subtitle_color = (107, 114, 128)

    # Create base image with gradient
    image = create_gradient_background(width, height, bg_color1, bg_color2)
    draw = ImageDraw.Draw(image, 'RGBA')

    # Add decorative circles with gradient and blur
    circle_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    circle_draw = ImageDraw.Draw(circle_layer)

    # Top right circle (cyan)
    circle_draw.ellipse([1520, -300, 2120, 300], fill=(*primary_color, 25))
    # Bottom left circle (purple)
    circle_draw.ellipse([-300, 680, 500, 1480], fill=(*secondary_color, 25))

    # Blur the circles
    circle_layer = circle_layer.filter(ImageFilter.GaussianBlur(60))
    image = Image.alpha_composite(image.convert('RGBA'), circle_layer).convert('RGB')
    draw = ImageDraw.Draw(image, 'RGBA')

    # Try to load fonts (fallback to default if not available)
    try:
        # Try common system fonts
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
        ]

        font_title = None
        font_label = None
        font_subtitle = None
        font_timestamp = None
        font_number = None

        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font_title = ImageFont.truetype(font_path, 100)
                    font_label = ImageFont.truetype(font_path, 40)
                    font_subtitle = ImageFont.truetype(font_path, 36)
                    font_timestamp = ImageFont.truetype(font_path, 32)
                    font_number = ImageFont.truetype(font_path, 150)
                    break
                except:
                    continue

        if not font_title:
            # Fallback to default
            font_title = ImageFont.load_default()
            font_label = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
            font_timestamp = ImageFont.load_default()
            font_number = ImageFont.load_default()

    except Exception as e:
        print(f"⚠️  Could not load custom fonts, using default: {e}")
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_timestamp = ImageFont.load_default()
        font_number = ImageFont.load_default()

    # Draw chapter number watermark (top right)
    number_text = f"{chapter_num:02d}"
    number_bbox = draw.textbbox((0, 0), number_text, font=font_number)
    number_width = number_bbox[2] - number_bbox[0]
    number_height = number_bbox[3] - number_bbox[1]
    draw.text((width - number_width - 80, 60), number_text,
              fill=(*primary_color, 40), font=font_number)

    # Draw chapter label
    label_text = f"CHAPTER {chapter_num}"
    label_bbox = draw.textbbox((0, 0), label_text, font=font_label)
    label_width = label_bbox[2] - label_bbox[0]
    draw.text(((width - label_width) // 2, 320), label_text,
              fill=primary_color, font=font_label)

    # Draw chapter title (with glow effect)
    title_y = 450

    # Wrap title if too long
    title_lines = []
    max_title_width = width - 200

    if len(title) > 20:
        words = title.split()
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font_title)
            if bbox[2] - bbox[0] <= max_title_width:
                current_line.append(word)
            else:
                if current_line:
                    title_lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            title_lines.append(' '.join(current_line))
    else:
        title_lines = [title]

    # Draw each title line
    for i, line in enumerate(title_lines):
        line_bbox = draw.textbbox((0, 0), line, font=font_title)
        line_width = line_bbox[2] - line_bbox[0]
        line_y = title_y + (i * 110)

        # Add glow effect
        for offset in range(3):
            alpha = int(100 - offset * 30)
            glow_color = (*primary_color, alpha)
            for dx, dy in [(-offset-1, 0), (offset+1, 0), (0, -offset-1), (0, offset+1)]:
                draw.text(((width - line_width) // 2 + dx, line_y + dy), line,
                         fill=glow_color, font=font_title)

        # Draw main text
        draw.text(((width - line_width) // 2, line_y), line,
                 fill=text_color, font=font_title)

    # Draw subtitle
    if subtitle:
        subtitle_y = title_y + len(title_lines) * 110 + 50

        # Wrap subtitle
        subtitle_lines = []
        max_subtitle_width = width - 400

        words = subtitle.split()
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font_subtitle)
            if bbox[2] - bbox[0] <= max_subtitle_width:
                current_line.append(word)
            else:
                if current_line:
                    subtitle_lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            subtitle_lines.append(' '.join(current_line))

        for i, line in enumerate(subtitle_lines[:3]):  # Limit to 3 lines
            line_bbox = draw.textbbox((0, 0), line, font=font_subtitle)
            line_width = line_bbox[2] - line_bbox[0]
            draw.text(((width - line_width) // 2, subtitle_y + i * 45), line,
                     fill=subtitle_color, font=font_subtitle)

    # Draw timestamp badge (bottom left)
    timestamp_text = timestamp
    timestamp_bbox = draw.textbbox((0, 0), timestamp_text, font=font_timestamp)
    timestamp_width = timestamp_bbox[2] - timestamp_bbox[0]
    timestamp_height = timestamp_bbox[3] - timestamp_bbox[1]

    # Badge background
    badge_x, badge_y = 80, height - 100
    badge_padding = 20
    badge_rect = [
        badge_x - badge_padding,
        badge_y - badge_padding,
        badge_x + timestamp_width + badge_padding,
        badge_y + timestamp_height + badge_padding
    ]

    # Draw badge with border
    draw.rounded_rectangle(badge_rect, radius=12,
                          fill=(*primary_color, 25),
                          outline=primary_color, width=2)

    draw.text((badge_x, badge_y), timestamp_text,
             fill=primary_color, font=font_timestamp)

    # Save image
    try:
        image.save(output_path, 'PNG', quality=95)
        return True
    except Exception as e:
        print(f"❌ Error saving image: {e}")
        return False

def main():
    """Main execution"""
    script_dir = Path(__file__).parent
    markdown_file = script_dir / "chapter_markers.md"
    output_dir = script_dir / "generated_chapter_markers_md"
    images_dir = output_dir / "images"

    # Create output directory
    images_dir.mkdir(parents=True, exist_ok=True)

    print("="*60)
    print("🎨 MARKDOWN CHAPTER MARKERS TO IMAGE CONVERTER (PIL)")
    print("="*60)
    print(f"\n📄 Input: {markdown_file}")
    print(f"📁 Output: {images_dir}")

    # Parse markdown
    print(f"\n🔍 Parsing markdown slides...")
    slides = parse_markdown_slides(markdown_file)
    print(f"✅ Found {len(slides)} chapter markers")

    # Generate images
    print(f"\n🎨 Generating images...")
    successful = 0
    failed = 0

    for slide in slides:
        image_filename = f"chapter_{slide['chapter_num']:02d}_{slide['title'].lower().replace(' ', '_').replace('&', 'and')}.png"
        image_path = images_dir / image_filename

        print(f"  Creating: {image_filename}...", end=' ')

        if generate_chapter_image(slide, image_path, theme="dark"):
            print("✅")
            successful += 1
        else:
            print("❌")
            failed += 1

    # Summary
    print("\n" + "="*60)
    print("📊 CONVERSION SUMMARY")
    print("="*60)
    print(f"✅ Successful: {successful}/{len(slides)}")
    print(f"❌ Failed: {failed}/{len(slides)}")
    print(f"\n📁 Images saved to: {images_dir}")
    print("\n✅ Done!")

if __name__ == "__main__":
    main()

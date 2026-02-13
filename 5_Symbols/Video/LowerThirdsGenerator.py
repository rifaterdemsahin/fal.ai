#!/usr/bin/env python3
"""
Lower Thirds Generator - Cost-Effective Edition
Generates professional lower third graphics using PIL/Pillow (FREE!)
Perfect for DaVinci Resolve with transparent backgrounds
"""

import sys
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import json

class LowerThirdsGenerator:
    """Generates professional lower thirds graphics for DaVinci Resolve"""

    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Design specifications for DaVinci Resolve
        self.width = 1920
        self.height = 1080

        # Professional color palette
        self.colors = {
            'bg_dark': (26, 26, 46, 220),  # #1a1a2e with transparency
            'accent_blue': (0, 212, 255, 255),  # #00d4ff
            'accent_purple': (123, 44, 191, 255),  # #7b2cbf
            'highlight_orange': (255, 107, 53, 255),  # #ff6b35
            'secondary_teal': (0, 191, 165, 255),  # #00bfa5
            'text_white': (255, 255, 255, 255),
            'text_gray': (180, 180, 180, 255),
        }

    def create_lower_third(self, main_text: str, subtext: str,
                          accent_color: str = 'accent_blue',
                          filename: str = None) -> Path:
        """
        Create a lower third graphic with transparent background

        Args:
            main_text: Primary text (e.g., "The Agentic Era")
            subtext: Secondary text (e.g., "Managing 240+ Workflows")
            accent_color: Color key from self.colors
            filename: Output filename (auto-generated if None)

        Returns:
            Path to generated PNG file
        """
        # Create transparent image (RGBA mode)
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Position in lower-left area (typical lower third placement)
        margin_x = 60
        margin_y = 840  # Start lower third at 840px from top

        # Load fonts (try to use system fonts, fallback to default)
        try:
            font_main = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 48)
            font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 32)
        except (OSError, IOError):
            try:
                # macOS alternative
                font_main = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
                font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
            except (OSError, IOError):
                # Fallback to default
                font_main = ImageFont.load_default()
                font_sub = ImageFont.load_default()

        # Draw background panel (glassmorphism style)
        panel_width = 700
        panel_height = 140
        panel_x = margin_x
        panel_y = margin_y

        # Background rectangle with rounded corners
        draw.rounded_rectangle(
            [panel_x, panel_y, panel_x + panel_width, panel_y + panel_height],
            radius=8,
            fill=self.colors['bg_dark']
        )

        # Accent line (left side)
        accent_width = 6
        draw.rectangle(
            [panel_x, panel_y, panel_x + accent_width, panel_y + panel_height],
            fill=self.colors[accent_color]
        )

        # Draw main text
        text_x = panel_x + 25
        text_y = panel_y + 20
        draw.text(
            (text_x, text_y),
            main_text.upper(),
            font=font_main,
            fill=self.colors['text_white']
        )

        # Draw subtext
        subtext_y = panel_y + 80
        draw.text(
            (text_x, subtext_y),
            subtext,
            font=font_sub,
            fill=self.colors['text_gray']
        )

        # Generate filename if not provided
        if filename is None:
            safe_name = main_text.lower().replace(' ', '_').replace('-', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"lt_{safe_name}_{timestamp}.png"

        # Save with transparency
        output_path = self.output_dir / filename
        img.save(output_path, 'PNG', optimize=True)

        print(f"✅ Generated: {filename}")
        return output_path

    def generate_from_config(self, config_path: Path = None) -> dict:
        """
        Generate multiple lower thirds from a JSON configuration file

        Returns:
            Dictionary with generation summary
        """
        if config_path is None:
            config_path = self.input_dir / "lower_thirds_config.json"

        # Default configuration if file doesn't exist
        if not config_path.exists():
            print(f"⚠️  Config file not found: {config_path}")
            print("📝 Using default lower thirds configuration")
            config = self.get_default_config()
        else:
            with open(config_path, 'r') as f:
                config = json.load(f)

        generated_files = []
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_generated': 0,
            'files': []
        }

        for item in config['lower_thirds']:
            output_path = self.create_lower_third(
                main_text=item['text'],
                subtext=item['subtext'],
                accent_color=item.get('accent_color', 'accent_blue'),
                filename=item.get('filename')
            )

            file_info = {
                'filename': output_path.name,
                'path': str(output_path),
                'text': item['text'],
                'subtext': item['subtext']
            }

            generated_files.append(output_path)
            summary['files'].append(file_info)

        summary['total_generated'] = len(generated_files)

        # Save summary JSON
        summary_path = self.output_dir / f"lower_thirds_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"\n🎉 Generated {len(generated_files)} lower thirds!")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📊 Summary saved to: {summary_path}")

        return summary

    def get_default_config(self) -> dict:
        """Return default lower thirds configuration"""
        return {
            "lower_thirds": [
                {
                    "text": "The Agentic Era",
                    "subtext": "Managing 240+ Workflows",
                    "accent_color": "accent_blue",
                    "filename": "lt_01_agentic_era.png"
                },
                {
                    "text": "Model Context Protocol",
                    "subtext": "Standardized AI Connections",
                    "accent_color": "accent_purple",
                    "filename": "lt_02_mcp.png"
                },
                {
                    "text": "The Skills Gap",
                    "subtext": "Technology vs. Delivery",
                    "accent_color": "highlight_orange",
                    "filename": "lt_03_skills_gap.png"
                },
                {
                    "text": "Bounded Contexts",
                    "subtext": "Separation of Concerns",
                    "accent_color": "secondary_teal",
                    "filename": "lt_04_bounded_contexts.png"
                },
                {
                    "text": "PARA Method",
                    "subtext": "Projects • Areas • Resources • Archives",
                    "accent_color": "accent_blue",
                    "filename": "lt_05_para_method.png"
                },
                {
                    "text": "State Management",
                    "subtext": "Persistence in Automation",
                    "accent_color": "accent_purple",
                    "filename": "lt_06_state_management.png"
                },
                {
                    "text": "DeliverPilot",
                    "subtext": "Methodology & Documentation",
                    "accent_color": "secondary_teal",
                    "filename": "lt_07_deliverpilot.png"
                },
                {
                    "text": "Bottom-Up Revolution",
                    "subtext": "Individual AI Adoption",
                    "accent_color": "highlight_orange",
                    "filename": "lt_08_bottom_up.png"
                },
                {
                    "text": "240+ Autonomous Workflows",
                    "subtext": "Running on n8n",
                    "accent_color": "accent_blue",
                    "filename": "lt_09_n8n_workflows.png"
                },
                {
                    "text": "AI Transformation",
                    "subtext": "The Bigger Picture",
                    "accent_color": "accent_purple",
                    "filename": "lt_10_ai_transformation.png"
                }
            ]
        }


def main():
    """Main execution"""
    # Set directories from arguments or use defaults
    input_dir = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/input")
    output_dir = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/output")

    print("=" * 60)
    print("🎬 LOWER THIRDS GENERATOR - Cost-Effective Edition")
    print("=" * 60)
    print("💰 Cost: $0.00 (FREE! Using PIL/Pillow)")
    print(f"📥 Input:  {input_dir}")
    print(f"📤 Output: {output_dir}")
    print("=" * 60)
    print()

    generator = LowerThirdsGenerator(input_dir=input_dir, output_dir=output_dir)
    generator.generate_from_config()

    print("\n" + "=" * 60)
    print("✨ BENEFITS FOR DAVINCI RESOLVE:")
    print("=" * 60)
    print("✅ PNG format with alpha channel (transparency)")
    print("✅ 1920x1080 resolution (Full HD)")
    print("✅ Professional glassmorphism design")
    print("✅ Positioned in lower-left (broadcast standard)")
    print("✅ Optimized file size")
    print("✅ Ready to drag-and-drop into timeline")
    print("=" * 60)


if __name__ == "__main__":
    main()

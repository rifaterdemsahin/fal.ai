#!/usr/bin/env python3
"""
Shared Configuration for Asset Generators
Single source of truth for seeds, colors, and common settings
"""

from pathlib import Path

# Consistency seeds for different asset categories
SEEDS = {
    "SEED_001": 42,      # B-roll (can vary)
    "SEED_002": 123456,  # Infographics (MUST match)
    "SEED_003": 789012,  # Motion graphics (brand)
    "SEED_004": 345678,  # UI overlays (template)
}

# Brand color palette (reference for prompts)
BRAND_COLORS = {
    "primary_dark": "#1a1a2e",
    "accent_blue": "#00d4ff",
    "accent_purple": "#7b2cbf",
    "secondary_teal": "#00bfa5",
    "highlight_orange": "#ff6b35",
    "text_white": "#ffffff",
}

# Default models for different asset types
DEFAULT_MODELS = {
    "image": "fal-ai/flux/dev",
    "image_fast": "fal-ai/flux/schnell",
    "video": "fal-ai/minimax/video-01",
    "music": "fal-ai/stable-audio",
}

# Common image sizes
IMAGE_SIZES = {
    "hd": {"width": 1920, "height": 1080},
    "square": {"width": 1024, "height": 1024},
    "portrait": {"width": 1080, "height": 1920},
}

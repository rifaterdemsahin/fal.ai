"""
Shared Configuration for Asset Generators
Single source of truth for seeds, colors, and common settings
"""

from pathlib import Path

# Default EDL path for chapter marker generation
DEFAULT_EDL_PATH = "../3_Simulation/Feb1Youtube/source_edl.md"

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
    "music": "beatoven/music-generation",
    "3d": "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d",
}

# Common image sizes
IMAGE_SIZES = {
    "hd": {"width": 1920, "height": 1080},
    "square": {"width": 1024, "height": 1024},
    "portrait": {"width": 1080, "height": 1920},
}

# Output format configuration
# Use "jpeg" for assets without transparency needs (smaller file size)
# Use "png" for assets requiring transparency (icons, lower thirds, overlays)
OUTPUT_FORMATS = {
    "image": "jpeg",          # Images with solid backgrounds
    "graphic": "png",         # Graphics may need transparency
    "icon": "png",            # Icons need transparency
    "lower_third": "png",     # Lower thirds need transparency for overlays
    "svg": "svg",             # SVG is vector format
    "diagram": "jpeg",        # Diagrams typically have solid backgrounds
    "memory_palace": "jpeg",  # Memory palace images have solid backgrounds
    "chapter_marker": "jpeg", # Chapter markers have solid backgrounds
    "video": "mp4",           # Video format
    "music": "wav",           # Audio format (Beatoven outputs WAV)
    "audio": "mp3",           # Audio format
    "3d": "glb",              # 3D models in GLB format (glTF binary)
}

# Estimated pricing per generation (in USD)
# Used for cost warnings
MODEL_PRICING = {
    # Video
    "fal-ai/minimax/video-01": 0.50,
    
    # 3D
    "fal-ai/hunyuan-3d/v3.1/rapid/text-to-3d": 0.45, # Conservative estimate
    
    # Images (approximate cost per output)
    "fal-ai/flux/dev": 0.05,        # Approx for standard HD/Square
    "fal-ai/flux/schnell": 0.01,    # Cheaper variant
    
    # Audio
    "beatoven/music-generation": 0.05,
    
    # Upscaling
    "fal-ai/aura-sr": 0.02,         # Upscaling cost
}

# Cost threshold for automatic skipping (in USD)
COST_THRESHOLD = 0.20

def check_generation_cost(model: str) -> bool:
    """
    Check if the estimated cost exceeds the threshold ($0.20) and skip automatically.
    
    Args:
        model: The model identifier (e.g., "fal-ai/flux/dev")
        
    Returns:
        True to proceed with generation, False to skip
    """
    # Default to 0.0 if model not found in pricing dict
    estimated_cost = MODEL_PRICING.get(model, 0.0)
    
    # If cost > threshold, skip and log
    if estimated_cost > COST_THRESHOLD:
        print(f"⚠️  SKIPPED: Generation cost ${estimated_cost:.2f} exceeds threshold ${COST_THRESHOLD:.2f}")
        print(f"   Model: {model}")
        return False
            
    return True

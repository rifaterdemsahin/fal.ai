import os
import json
import urllib.request
import urllib.error
from typing import Optional
from datetime import datetime

def get_gemini_key() -> Optional[str]:
    """Retrieve the Gemini API key from environment variables."""
    return os.environ.get("GEMINIKEY") or os.environ.get("GEMINI_API_KEY")


def get_enhancement_context(asset_type: str) -> str:
    """Get specific enhancement instructions based on asset type."""
    
    # Common visual elements
    base_visual = "Make it more descriptive, detailed, and visually evocative. Focus on lighting, texture, composition, and style."
    
    contexts = {
        'image': f"Enhance this prompt for a high-quality AI image generator. {base_visual}",
        'graphic': f"Enhance this prompt for a professional graphic design asset. {base_visual} Focus on clean aesthetics.",
        'icon': "Enhance this prompt for an icon generator. Focus on simplicity, clarity, distinctive shapes, and vector-like qualities. Ensure it reads well at small sizes.",
        'lower_third': "Enhance this prompt for a video lower-third overlay. Focus on identifying text positioning, alpha transparency requirements, and broadcast-style aesthetics.",
        'svg': "Enhance this prompt for an SVG vector generator. Focus on flat colors, clean lines, geometric shapes, and scalable vector aesthetics.",
        'diagram': "Enhance this prompt for a diagram generator. Focus on structural clarity, logical flow, schematic look, and informational density.",
        'memory_palace': "Enhance this prompt for a memory palace visualization. Focus on distinct loci, vivid and memorable imagery, spatial reasoning, and mnemonic devices.",
        'chapter_marker': f"Enhance this prompt for a video chapter title card. {base_visual} Focus on cinematic composition and potential text placement areas.",
        'video': "Enhance this prompt for an AI video generator. Focus on motion, camera movement (pan, tilt, zoom), pacing, dynamic action, and temporal consistency.",
        'music': "Enhance this prompt for an AI music generator. Focus on instrumentation, genre, mood, tempo (BPM), rhythm, musical structure, and specific sonic emotion.",
        'audio': "Enhance this prompt for an AI sound effect or audio generator. Focus on sonic texture, duration, exact sound characteristics, and audio fidelity.",
        '3d': "Enhance this prompt for a 3D model generator. Focus on 3D geometry, spatial structure, material properties (PBR), and object volume. Do not describe background surroundings.",
    }
    
    default_context = (
        "Enhance the following prompt for an AI generator. "
        "Make it more descriptive and detailed while keeping the core meaning. "
        "Output ONLY the enhanced prompt."
    )
    
    return contexts.get(asset_type, default_context)

def enhance_prompt(prompt: str, context: Optional[str] = None, asset_type: Optional[str] = None, log_path: Optional[str] = None) -> str:
    """
    Enhance a prompt using Google Gemini API.
    
    Args:
        prompt: The original prompt to enhance.
        context: Optional context/instruction for enhancement. 
                 If None, uses specific context based on asset_type.
        asset_type: The type of asset (e.g., 'image', 'video', 'music').
                 Used to determine the enhancement strategy if context is not provided.
                 
    Returns:
        The enhanced prompt, or the original prompt if enhancement fails.
    """
    api_key = get_gemini_key()
    
    if not api_key:
        print("⚠️  GEMINIKEY not found in environment. Skipping prompt enhancement.")
        return prompt
        
    if not prompt:
        return prompt

    # Determine context strategy
    if not context:
        if asset_type:
            context = get_enhancement_context(asset_type)
        else:
            # Fallback default
            context = (
                "Enhance the following prompt for an AI image generator. "
                "Make it more descriptive, detailed, and visually evocative. "
                "Focus on lighting, texture, composition, and style. "
                "Keep the core subject and meaning intact. "
                "Output ONLY the enhanced prompt, no other text."
            )
    
    # Append the instruction to output only the prompt if not already explicit in custom context
    if "Output ONLY" not in context:
        context += " Output ONLY the enhanced prompt, no other text."
    
    # Construct the request payload
    # Using gemini-2.0-flash as it is available in the environment
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"{context}\n\nOriginal prompt: {prompt}"
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1000,
        }
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            
            # Extract text from response
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    enhanced_text = candidate["content"]["parts"][0]["text"].strip()
                    
                    if log_path:
                        with open(log_path, 'a', encoding='utf-8') as f:
                            f.write(f"\n--- Prompt Enhancement ({datetime.now().isoformat()}) ---\n")
                            f.write(f"Original: {prompt}\n")
                            f.write(f"Enhanced: {enhanced_text}\n")
                            f.write("-" * 50 + "\n")
                            
                    return enhanced_text
            
            print(f"⚠️  Gemini response format unexpected: {result}")
            return prompt
            
    except urllib.error.HTTPError as e:
        print(f"⚠️  Gemini API error: {e.code} {e.reason}")
        try:
            print(e.read().decode('utf-8')) # specific error details
        except:
            pass
        return prompt
    except Exception as e:
        print(f"⚠️  Error enhancing prompt: {str(e)}")
        return prompt

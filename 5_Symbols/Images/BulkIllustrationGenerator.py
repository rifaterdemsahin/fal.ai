"""
Bulk Illustration Generator
This script searches for images using Google Custom Search API and transforms them using fal.ai's image-to-image models.
"""
import os
import requests
import fal_client

# 1. Setup Keys
# Keys should be set in environment variables or .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "your_google_key")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "your_search_engine_id")

# FAL_KEY is typically picked up by the client from environment, 
# ensuring it is set if provided explicitly.
if "FAL_KEY" not in os.environ and "your_fal_ai_key" != "your_fal_ai_key":
     os.environ["FAL_KEY"] = "your_fal_ai_key"

def get_google_image(query):
    """
    Search for an image using Google Custom Search API.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': GOOGLE_CSE_ID,
        'key': GOOGLE_API_KEY,
        'searchType': 'image',
        'num': 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['link'] # The direct image URL
        else:
            print(f"No results found for query: {query}")
            # print(f"Debug: {data}")
            return None
    except Exception as e:
        print(f"Error searching Google: {e}")
        return None

def illustrate_image(image_url):
    """
    Transform the image using fal.ai image-to-image model.
    """
    if not image_url:
        return None
        
    print(f"Transforming image: {image_url}")
    try:
        # Using fal-ai/flux/dev/image-to-image as requested
        result = fal_client.subscribe(
            "fal-ai/flux/dev/image-to-image",
            arguments={
                "image_url": image_url,
                "prompt": "A beautiful, highly detailed digital illustration in a Studio Ghibli style, vibrant colors",
                "strength": 0.65  # Adjust: 0.1 stays close to photo, 0.9 becomes very abstract
            }
        )
        if result and 'images' in result and len(result['images']) > 0:
            return result['images'][0]['url']
        return None
    except Exception as e:
        print(f"Error transforming image: {e}")
        return None

# Execution
if __name__ == "__main__":
    # Example query
    query = "Cyberpunk Tokyo Street"
    print(f"Starting process for: {query}")
    
    source_img = get_google_image(query)
    
    if source_img:
        final_img = illustrate_image(source_img)
        print("-" * 30)
        print(f"Original: {source_img}")
        print(f"Illustrated: {final_img}")
        print("-" * 30)
    else:
        print("Process failed: Could not retrieve source image.")

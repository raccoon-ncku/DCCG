"""
Lecture 10: AI in Design
Example 02: Semantic Search (CLIP)

This script demonstrates how to use "Discriminative AI" (CLIP) to understand 
the content of images. We can use this to search through a collection of 
architectural images using text descriptions.

Requirements:
    pip install torch transformers pillow requests

"""

import torch
from PIL import Image
import requests
from transformers import CLIPProcessor, CLIPModel

def semantic_search():
    print("--- AI Semantic Search (CLIP) ---")

    # 1. Load Model
    print("Loading CLIP Model (openai/clip-vit-base-patch32)...")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32", use_safetensors=True)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    # 2. Prepare "Database" of Images
    # In a real project, these would be files in your 'assets' folder.
    print("Loading sample images...")
    urls = [
        "https://images.unsplash.com/photo-1511818966892-d7d671e672a2?w=600", # Modern glass building
        "https://images.unsplash.com/photo-1546414701-81cc6963c67f?w=600", # concrete building
        "https://images.unsplash.com/photo-1761194412110-9998acafc0ec?w=600", # Traditional brick house
        "https://images.unsplash.com/photo-1448375240586-882707db888b?w=600", # Forest/Nature
    ]
    
    images = []
    for url in urls:
        try:
            images.append(Image.open(requests.get(url, stream=True).raw))
        except:
            print(f"Failed to load {url}")

    if not images:
        print("No images loaded. Exiting.")
        return

    # 3. Define Search Queries
    # What are we looking for?
    search_queries = [
        "a modern glass skyscraper",
        "a cozy brick house",
        "concrete brutalist architecture",
        "nature and trees"
    ]

    print(f"Analyzing {len(images)} images against {len(search_queries)} queries...")

    # 4. Process Inputs
    inputs = processor(text=search_queries, images=images, return_tensors="pt", padding=True)

    # 5. Run Model
    outputs = model(**inputs)
    
    # The model returns "logits_per_image" (how well each image matches each text)
    logits_per_image = outputs.logits_per_image 
    probs = logits_per_image.softmax(dim=1) # Convert to probabilities

    # 6. Display Results
    print("\n--- Search Results ---")
    for i, image_url in enumerate(urls):
        print(f"\nImage {i+1}: {image_url[:40]}...")
        
        # Find the best matching text for this image
        best_match_idx = probs[i].argmax().item()
        best_score = probs[i][best_match_idx].item()
        
        print(f"  Best Match: '{search_queries[best_match_idx]}' ({best_score:.2%})")
        
        # Show all scores
        for j, query in enumerate(search_queries):
            score = probs[i][j].item()
            print(f"    - '{query}': {score:.2%}")

if __name__ == "__main__":
    semantic_search()

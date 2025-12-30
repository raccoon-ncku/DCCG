"""
Lecture 10: AI in Design
Example 01: Neural Rendering (Sketch-to-Render)

This script demonstrates how to use Generative AI (Stable Diffusion + ControlNet)
to transform a simple architectural sketch (or COMPAS wireframe) into a 
photorealistic rendering.

Requirements:
    pip install torch diffusers transformers accelerate opencv-python

Note: This script requires a significant amount of RAM and preferably a GPU (CUDA or MPS).
"""

import torch
import numpy as np
from PIL import Image
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from diffusers.utils import load_image
import os
import pathlib

# Enable MPS Fallback for Mac compatibility
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

def neural_rendering():
    print("--- AI Neural Rendering (ControlNet) ---")

    # 1. Setup Device (MPS for Mac, CUDA for Nvidia, CPU otherwise)
    if torch.backends.mps.is_available():
        device = "mps"
        dtype = torch.float16
        print("Using Apple Metal (MPS) acceleration.")
    elif torch.cuda.is_available():
        device = "cuda"
        dtype = torch.float16
        print("Using NVIDIA CUDA acceleration.")
    else:
        device = "cpu"
        dtype = torch.float32
        print("Using CPU (Warning: This will be slow).")

    # 2. Load ControlNet (The "Eye" that understands lines)
    # We use a "Scribble" model that is good at interpreting rough sketches
    print("Loading ControlNet Model...")
    controlnet = ControlNetModel.from_pretrained(
        "lllyasviel/sd-controlnet-scribble", 
        torch_dtype=dtype
    )

    # 3. Load Stable Diffusion (The "Brain" that generates images)
    print("Loading Stable Diffusion Pipeline...")
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", 
        controlnet=controlnet, 
        torch_dtype=dtype,
        safety_checker=None
    )

    # Optimize scheduler for speed
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    
    # Enable memory savings
    pipe.to(device)
    if device == "cuda":
        pipe.enable_model_cpu_offload()

    # 4. Load or Create Input Image
    # For this example, we'll download a sample scribble if you don't have one.
    # In a real workflow, this would be your COMPAS viewport screenshot.

    image_path = pathlib.Path(__file__).parent / "input.jpg"
    print(f"Loading input sketch... {image_path}")
    image = load_image(str(image_path))


    # 5. Generate Image
    prompt = "architecture, concrete and glass, photorealistic, 8k, detailed"
    negative_prompt = "low quality, blurry, distorted, cartoon"

    print(f"Generating with prompt: '{prompt}'...")
    
    output = pipe(
        prompt, 
        image, 
        negative_prompt=negative_prompt, 
        num_inference_steps=20
    ).images[0]

    # 6. Save Result
    output_path = pathlib.Path(__file__).parent / "render_output.png"
    output.save(output_path)
    print(f"Rendering saved to '{output_path}'")

if __name__ == "__main__":
    neural_rendering()

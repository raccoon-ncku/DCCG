# Lecture 10: AI in Design

This lecture introduces **Artificial Intelligence** and **Machine Learning** workflows for architectural design. We explore two main categories: **Generative AI** (creating new data) and **Discriminative AI** (understanding existing data).

## 1. Concepts

### Generative AI (Diffusion Models)
Models like Stable Diffusion learn to generate images by reversing a noise process. By using **ControlNet**, we can guide this generation with precise geometry (edges, depth maps, segmentation), making it a powerful tool for architectural visualization.

### Discriminative AI (Transformers/CLIP)
Models like CLIP (Contrastive Language-Image Pre-training) learn to associate images with text. This allows us to "search" our design assets using natural language, or categorize images automatically.

## 2. Examples

### Example 01: Neural Rendering
**File:** `01_neural_rendering.py`

Takes a simple sketch or wireframe and turns it into a high-quality rendering using a text prompt.
*   **Model**: Stable Diffusion v1.5 + ControlNet (Scribble)
*   **Library**: `diffusers` (Hugging Face)

### Example 02: Semantic Search
**File:** `02_semantic_search.py`

Demonstrates how to search through a collection of images using text queries like "modern glass facade" or "brick house".
*   **Model**: CLIP (OpenAI)
*   **Library**: `transformers` (Hugging Face)

> caveat: These models are large, try it with a good and unlimited internet connection. 

## 3. Data Analysis (Legacy)
The `clustering/` and `regression/` folders contain examples of traditional Machine Learning techniques (K-Means, Linear Regression) applied to design data.

## 4. Installation

For the easiest setup, create the dedicated AI environment from the root of the repository. This handles PyTorch and other complex dependencies automatically.

```bash
conda env create -f environment_ai.yml
conda activate DCCG_AI
```



## Clean Up
Pretrained models can take up significant disk space. To remove cached models, you can delete the `~/.cache/huggingface/` folder:

on macOS/Linux:

```bash
rm -rf ~/.cache/huggingface/
```

on Windows (PowerShell):

```powershell
Remove-Item -Recurse -Force $env:USERPROFILE\.cache\huggingface\
```

or navigate to the folder in your file explorer and delete it manually, which is typically located at:

```C:\Users\<YourUsername>\.cache\huggingface\
```

or `/home/<YourUsername>/.cache/huggingface/` on macOS/Linux.


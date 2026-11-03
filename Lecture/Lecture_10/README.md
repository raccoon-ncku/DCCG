# AI models as design ingredients (optional, Week 15)

> Optional, and the heaviest material in the course to install. A trained model is one
> **component** inside a design tool you still architect the same way: a core that calls
> it, an artifact, an adapter.

## 1. Two kinds of model

**Generative** — makes new data. Diffusion models (Stable Diffusion) turn noise
into images; with **ControlNet** you steer that generation with real geometry
(edges, depth, a scribble), so your wireframe drives the render instead of a
text prompt alone.

**Discriminative** — understands existing data. **CLIP** links images and text
in the same space, so you can search a folder of references with a phrase like
"modern glass facade", or sort images automatically.

A model is a function that was trained rather than written, and it belongs behind a clean
boundary: your core calls `render(sketch, prompt)` or `search(query, images)`, whatever is
inside them.

## 2. Examples

```bash
uv run Lecture/Lecture_10/01_neural_rendering.py
uv run Lecture/Lecture_10/02_semantic_search.py
```

### `01_neural_rendering.py` — sketch to render

A wireframe or scribble plus a text prompt becomes a high-quality image.

- **Model**: Stable Diffusion v1.5 + ControlNet (Scribble)
- **Library**: `diffusers` (Hugging Face)

### `02_semantic_search.py` — search by meaning

Search a collection of images with natural-language queries instead of
filenames.

- **Model**: CLIP (OpenAI)
- **Library**: `transformers` (Hugging Face)

> ⚠️ These models are large (gigabytes) and download on first run. Use a fast,
> unlimited connection, and expect the first run to be slow.

### Classic machine learning

Clustering and regression, written from scratch on design data, are in the
Week 12 [learning tutorials](/Lecture/Algorithms/learning/README.md). They are
lighter to run, and often more appropriate than a giant model when the problem
is small.

## 3. Setup

Because of PyTorch and its GPU dependencies, **conda is the reliable path** here:

```bash
conda env create -f environment_neural.yml
conda activate DCCG_NEURAL
python Lecture/Lecture_10/01_neural_rendering.py
```

Do not add these packages to the shared `uv.lock`.

## 4. Clean up

The downloaded models are cached and take real disk space. To reclaim it:

```bash
# macOS / Linux
rm -rf ~/.cache/huggingface/

# Windows (PowerShell)
Remove-Item -Recurse -Force $env:USERPROFILE\.cache\huggingface\
```

## Using it in a final project

Wrap the model call in a core function, run it headlessly to produce an artifact (an image,
a ranked list), and keep the model behind that boundary, so the rest of your tool stays
testable. "Verify, don't trust" applies to a diffusion model as it does to a coding agent.

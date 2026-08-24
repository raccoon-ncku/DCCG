# Week 15 (Lecture 10) — AI models as design ingredients

> Optional, and the heaviest material in the course to install. The point is
> not to make you an ML engineer — it is to see how a trained model becomes one
> **component** inside a design tool you still architect the same way as
> everything else: a core that calls the model, an artifact, an adapter.

## 1. Two kinds of model

**Generative** — makes new data. Diffusion models (Stable Diffusion) turn noise
into images; with **ControlNet** you steer that generation with real geometry
(edges, depth, a scribble), so your wireframe drives the render instead of a
text prompt alone.

**Discriminative** — understands existing data. **CLIP** links images and text
in the same space, so you can search a folder of references with a phrase like
"modern glass facade", or sort images automatically.

The lesson for *you* is architectural, not statistical: a model is a function
that happens to have been trained rather than written. It still belongs behind
a clean boundary. Your core calls `render(sketch, prompt)` or
`search(query, images)`; whether that function is 10 lines of maths or a
2 GB neural network does not change how the rest of your program is shaped.

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

### Traditional ML (legacy)

`clustering/` (K-Means) and `regression/` (linear regression) apply classic
machine learning to design data — lighter to run, and often more appropriate
than a giant model when your problem is small.

## 3. Setup

Because of PyTorch, diffusers and their CUDA/Metal dependencies, the
**conda environment is the reliable path** here — this is the one place in the
course where conda earns its keep:

```bash
conda env create -f environment_neural.yml
conda activate DCCG_NEURAL
python Lecture/Lecture_10/01_neural_rendering.py
```

You *can* add the packages to the uv project (`uv add torch torchvision
transformers diffusers`), but the heavy binary wheels resolve more predictably
through conda. Do not add them to the shared `uv.lock` — keep this optional
stack out of everyone else's environment.

## 4. Clean up

The downloaded models are cached and take real disk space. To reclaim it:

```bash
# macOS / Linux
rm -rf ~/.cache/huggingface/

# Windows (PowerShell)
Remove-Item -Recurse -Force $env:USERPROFILE\.cache\huggingface\
```

## Using it in a final project

A strong project pattern: wrap the model call in a pure-ish core function, run
it headlessly to produce an artifact (a rendered image, a ranked list of
matches), and keep the model itself behind that boundary. The heavy,
non-deterministic part stays in one place; the rest of your tool stays testable.

Be honest in your reflection about what the model got right and wrong — the same
"verify, don't trust" rule from Week 11 applies to a diffusion model exactly as
it does to a coding agent.

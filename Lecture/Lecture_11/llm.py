"""
Shared helper for Lecture 11.

Every script in this lecture talks to the same course LLM node.
This module keeps the connection details in ONE place, so the
example scripts can focus on the *workflow*, not the plumbing.

The API key is read from a `.env` file next to this script
(copy `.env.example` to `.env` and paste your key).
"""

import os
from pathlib import Path

from openai import OpenAI

# Our self-hosted node speaks the OpenAI wire protocol, so the official
# `openai` client works with it -- we only change the base_url.
BASE_URL = "https://llm-api.rccn.dev/v1"
MODEL = "gemma-4-26B-A4B-it-AWQ-4bit"


def _load_dotenv():
    """A minimal .env reader (no extra dependency needed).

    Reads KEY=VALUE lines from Lecture_11/.env into os.environ.
    """
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"'))


def get_client():
    """Return an OpenAI client connected to the course node."""
    _load_dotenv()
    api_key = os.environ.get("DCCG_LLM_KEY")
    if not api_key:
        raise SystemExit(
            "No API key found.\n"
            "Copy Lecture_11/.env.example to Lecture_11/.env and fill in DCCG_LLM_KEY."
        )
    return OpenAI(base_url=BASE_URL, api_key=api_key)


def chat(client, messages, **kwargs):
    """One round-trip to the model. Returns the assistant message object.

    We default temperature to 0: small quantized models drift and start
    hallucinating at higher temperatures, and for *tool-like* usage we
    want reproducible answers, not creativity.
    """
    kwargs.setdefault("temperature", 0)
    kwargs.setdefault("timeout", 120)
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        **kwargs,
    )
    return response.choices[0].message

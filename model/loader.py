"""
model/loader.py

Loads a HuggingFace causal LM either from HuggingFace Hub or a local path,
wraps it with langchain-huggingface HuggingFacePipeline, and exposes a
get_llm() function for use across all agents.

Supports optional 4-bit quantization via bitsandbytes when a GPU is available.

Usage:
    from model.loader import get_llm
    llm = get_llm()
"""

import os
import logging
from functools import lru_cache

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    pipeline,
)
from langchain_huggingface import HuggingFacePipeline

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration (read from .env via python-dotenv in main.py)
# ---------------------------------------------------------------------------

# HuggingFace Hub model ID or absolute local path
# Example Hub:   "mistralai/Mistral-7B-Instruct-v0.2"
# Example local: "/home/user/models/mistral-finetuned"
MODEL_NAME: str = os.getenv("HF_MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.2")

# Optional HuggingFace token (needed for gated/private models)
HF_TOKEN: str | None = os.getenv("HUGGINGFACE_TOKEN") or None

# Generation defaults (can be overridden by callers)
MAX_NEW_TOKENS: int = int(os.getenv("HF_MAX_NEW_TOKENS", "512"))
TEMPERATURE: float = float(os.getenv("HF_TEMPERATURE", "0.7"))


# ---------------------------------------------------------------------------
# Device detection
# ---------------------------------------------------------------------------

def _get_device() -> str:
    """Returns 'cuda', 'mps', or 'cpu' based on available hardware."""
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def _use_quantization(device: str) -> bool:
    """4-bit quantization is only supported on CUDA."""
    return device == "cuda"


# ---------------------------------------------------------------------------
# Model + tokenizer loading
# ---------------------------------------------------------------------------

def _load_pipeline(model_name: str, device: str) -> pipeline:
    """
    Loads the tokenizer and model, applies 4-bit quantization on GPU,
    and returns a HuggingFace text-generation pipeline.
    """
    logger.info("Loading model: %s  |  device: %s", model_name, device)

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        token=HF_TOKEN,
        trust_remote_code=True,
    )

    # Ensure pad token exists (required for batched generation)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Build quantization config for GPU
    quantization_config = None
    if _use_quantization(device):
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )
        logger.info("4-bit quantization enabled (bitsandbytes)")

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        token=HF_TOKEN,
        quantization_config=quantization_config,
        device_map="auto" if device == "cuda" else None,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        trust_remote_code=True,
    )

    if device != "cuda":
        model = model.to(device)

    hf_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        return_full_text=False,   # return only the generated part, not the prompt
    )

    logger.info("Model loaded successfully.")
    return hf_pipeline


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_llm() -> HuggingFacePipeline:
    """
    Returns a cached LangChain-compatible LLM backed by the local HuggingFace model.

    The model is loaded once and reused across all agents.
    Subsequent calls return the same instance (lru_cache).

    Returns:
        HuggingFacePipeline: A LangChain LLM ready for .invoke() calls.

    Raises:
        RuntimeError: If the model cannot be loaded.
    """
    device = _get_device()

    try:
        hf_pipeline = _load_pipeline(MODEL_NAME, device)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to load model '{MODEL_NAME}' on device '{device}'. "
            f"Check HF_MODEL_NAME and HUGGINGFACE_TOKEN in your .env file.\n"
            f"Original error: {exc}"
        ) from exc

    return HuggingFacePipeline(pipeline=hf_pipeline)
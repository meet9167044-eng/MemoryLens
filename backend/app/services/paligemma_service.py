"""
backend/app/services/paligemma_service.py

PaliGemma 2 Visual Inference Service — Phase: Trained Model Integration

Modes (auto-detected from config):
  1. Colab Proxy (default for demo): Forwards image + question to the
     live ngrok URL of the Colab backend running the fine-tuned model.
  2. Local GPU: Loads LoRA adapter weights directly into the FastAPI
     process (requires CUDA + transformers/peft installed).

Usage:
    from app.services.paligemma_service import ask_visual
    answer = await ask_visual(image_bytes=b"...", question="Where are my keys?")
"""

from __future__ import annotations

import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Public interface
# ─────────────────────────────────────────────────────────────────────────────

async def ask_visual(
    image_bytes: bytes,
    filename: str,
    question: str,
    content_type: str = "image/jpeg",
    timeout: float = 60.0,
) -> dict:
    """
    Route an image + question to PaliGemma 2.

    Returns:
        {
            "question": str,
            "answer": str,
            "model": str,
            "backend": "colab_proxy" | "local_gpu" | "unavailable"
        }
    """
    from app.config import settings

    url = settings.PALIGEMMA_BACKEND_URL.strip()

    if url:
        return await _ask_via_colab_proxy(
            url=url,
            image_bytes=image_bytes,
            filename=filename,
            question=question,
            content_type=content_type,
            timeout=timeout,
        )

    # Fallback: try local GPU
    return _ask_via_local_gpu(image_bytes=image_bytes, question=question)


# ─────────────────────────────────────────────────────────────────────────────
# Mode A — Colab ngrok proxy
# ─────────────────────────────────────────────────────────────────────────────

async def _ask_via_colab_proxy(
    url: str,
    image_bytes: bytes,
    filename: str,
    question: str,
    content_type: str,
    timeout: float,
) -> dict:
    """Forward multipart request to the Colab FastAPI server."""
    endpoint = url.rstrip("/") + "/api/ask"

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                endpoint,
                files={"file": (filename, image_bytes, content_type)},
                data={"question": question},
                # ngrok free tier requires this header to skip the browser warning page
                headers={"ngrok-skip-browser-warning": "true"},
            )
            response.raise_for_status()
            data = response.json()

        return {
            "question": question,
            "answer": data.get("answer", "No answer returned."),
            "model": "PaliGemma 2 (LoRA fine-tuned)",
            "backend": "colab_proxy",
        }

    except httpx.TimeoutException:
        logger.error("Colab proxy timed out after %.1fs", timeout)
        return _error_response(question, "Request to the Colab model server timed out. Is your Colab notebook still running?")
    except httpx.HTTPStatusError as exc:
        logger.error("Colab proxy returned HTTP %s: %s", exc.response.status_code, exc.response.text)
        return _error_response(question, f"Colab server returned HTTP {exc.response.status_code}.")
    except Exception as exc:
        logger.error("Colab proxy error: %s", exc)
        return _error_response(question, f"Could not reach the Colab backend: {exc}")


# ─────────────────────────────────────────────────────────────────────────────
# Mode B — Local GPU (optional, requires transformers + peft + CUDA)
# ─────────────────────────────────────────────────────────────────────────────

_local_model = None
_local_processor = None


def _ask_via_local_gpu(image_bytes: bytes, question: str) -> dict:
    """Load LoRA adapter locally and run inference (GPU required)."""
    global _local_model, _local_processor

    try:
        import io
        import torch
        from PIL import Image
        from transformers import PaliGemmaProcessor, PaliGemmaForConditionalGeneration, BitsAndBytesConfig
        from peft import PeftModel

        if _local_model is None or _local_processor is None:
            logger.info("Loading PaliGemma 2 LoRA weights locally...")
            adapter_path = "./memorylens_paligemma_adapter"
            base_model_id = "google/paligemma2-3b-pt-224"

            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
            _local_processor = PaliGemmaProcessor.from_pretrained(base_model_id)
            base = PaliGemmaForConditionalGeneration.from_pretrained(
                base_model_id,
                quantization_config=bnb_config,
                device_map="auto",
            )
            _local_model = PeftModel.from_pretrained(base, adapter_path)
            _local_model.eval()
            logger.info("PaliGemma 2 loaded successfully.")

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        prompt = f"<image>answer en {question}"
        inputs = _local_processor(text=prompt, images=image, return_tensors="pt").to("cuda")

        with torch.no_grad():
            output = _local_model.generate(**inputs, max_new_tokens=60, do_sample=False, repetition_penalty=1.1)

        generated = output[0][inputs["input_ids"].shape[1]:]
        answer = _local_processor.decode(generated, skip_special_tokens=True).strip()

        return {
            "question": question,
            "answer": answer or "I couldn't generate an answer.",
            "model": "PaliGemma 2 (LoRA — local GPU)",
            "backend": "local_gpu",
        }

    except ImportError:
        return _error_response(
            question,
            "PaliGemma backend is not configured. Set PALIGEMMA_BACKEND_URL in your .env to point to your running Colab session.",
        )
    except Exception as exc:
        logger.error("Local GPU inference failed: %s", exc)
        return _error_response(question, f"Local model inference error: {exc}")


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _error_response(question: str, message: str) -> dict:
    return {
        "question": question,
        "answer": message,
        "model": "none",
        "backend": "unavailable",
    }

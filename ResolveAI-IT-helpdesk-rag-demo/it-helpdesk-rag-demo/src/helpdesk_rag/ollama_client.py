"""Thin HTTP client for a local Ollama server (no extra SDK needed).

Endpoints used:
  POST /api/embed  -> text  -> vector
  POST /api/chat   -> prompt -> streamed answer
  GET  /api/tags   -> list installed models (for the UI dropdown / health check)
"""

from __future__ import annotations

import json
import re
from typing import Iterable, Iterator, Protocol

import requests

from .config import settings


class OllamaError(RuntimeError):
    pass


class Embedder(Protocol):
    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...
    def embed_query(self, text: str) -> list[float]: ...


def _post(path: str, payload: dict, stream: bool = False) -> requests.Response:
    url = f"{settings.ollama_url.rstrip('/')}{path}"
    try:
        resp = requests.post(url, json=payload, stream=stream, timeout=settings.request_timeout)
    except requests.ConnectionError as e:
        raise OllamaError(
            f"Cannot reach Ollama at {settings.ollama_url}. Is it running? (`ollama serve`)"
        ) from e
    if resp.status_code != 200:
        raise OllamaError(f"Ollama {path} returned {resp.status_code}: {resp.text[:300]}")
    return resp


def list_models() -> list[str]:
    try:
        r = requests.get(f"{settings.ollama_url.rstrip('/')}/api/tags", timeout=5)
        r.raise_for_status()
        return sorted(m["name"] for m in r.json().get("models", []))
    except requests.RequestException:
        return []


# --------------------------------------------------------------------------- embeddings
class OllamaEmbedder:
    """Embeds text with an Ollama embedding model (default: nomic-embed-text).

    nomic-embed-text is trained with task prefixes; using them noticeably
    improves retrieval quality, so we add them automatically for that model.
    """

    def __init__(self, model: str | None = None, batch_size: int = 32):
        self.model = model or settings.embed_model
        self.batch_size = batch_size
        self._use_prefix = "nomic" in self.model

    def _embed(self, texts: list[str]) -> list[list[float]]:
        out: list[list[float]] = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            data = _post("/api/embed", {"model": self.model, "input": batch}).json()
            if "embeddings" not in data:
                raise OllamaError(f"Unexpected embed response: {str(data)[:200]}")
            out.extend(data["embeddings"])
        return out

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if self._use_prefix:
            texts = [f"search_document: {t}" for t in texts]
        return self._embed(texts)

    def embed_query(self, text: str) -> list[float]:
        if self._use_prefix:
            text = f"search_query: {text}"
        return self._embed([text])[0]


# --------------------------------------------------------------------------- chat
_THINK_BLOCK = re.compile(r"<think>.*?</think>", re.DOTALL)


def _supports_think_flag(model: str) -> bool:
    # Reasoning models (qwen3.x, deepseek-r1...) "think" before answering, which
    # is slow for a helpdesk demo. We ask Ollama to skip it for those families.
    name = model.lower()
    return name.startswith(("qwen3", "deepseek-r1", "gpt-oss"))


def chat_stream(messages: list[dict], model: str | None = None,
                temperature: float | None = None) -> Iterator[str]:
    """Yield answer tokens as they are generated."""
    model = model or settings.chat_model
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {"temperature": settings.temperature if temperature is None else temperature},
    }
    if _supports_think_flag(model):
        payload["think"] = False

    try:
        resp = _post("/api/chat", payload, stream=True)
    except OllamaError as e:
        if "think" in payload and "think" in str(e).lower():
            payload.pop("think")  # older Ollama / model without the flag -> retry plainly
            resp = _post("/api/chat", payload, stream=True)
        else:
            raise

    in_think = False
    for line in resp.iter_lines():
        if not line:
            continue
        chunk = json.loads(line)
        if "error" in chunk:
            raise OllamaError(chunk["error"])
        token = chunk.get("message", {}).get("content", "")
        # Strip any inline <think>...</think> the model still emits.
        if "<think>" in token:
            in_think = True
        if in_think:
            if "</think>" in token:
                in_think = False
                token = token.split("</think>", 1)[1]
            else:
                continue
        if token:
            yield token
        if chunk.get("done"):
            break


def chat(messages: list[dict], model: str | None = None) -> str:
    return _THINK_BLOCK.sub("", "".join(chat_stream(messages, model))).strip()

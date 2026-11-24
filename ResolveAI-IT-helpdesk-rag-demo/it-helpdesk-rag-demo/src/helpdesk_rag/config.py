"""Central configuration. Every value can be overridden with an environment
variable or a `.env` file in the project root (see `.env.example`)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

try:  # optional dependency
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


@dataclass(frozen=True)
class Settings:
    # --- Ollama ---------------------------------------------------------
    ollama_url: str = field(default_factory=lambda: _env("OLLAMA_URL", "http://localhost:11434"))
    chat_model: str = field(default_factory=lambda: _env("CHAT_MODEL", "llama3.2"))
    embed_model: str = field(default_factory=lambda: _env("EMBED_MODEL", "nomic-embed-text"))
    temperature: float = field(default_factory=lambda: float(_env("TEMPERATURE", "0.1")))
    request_timeout: int = field(default_factory=lambda: int(_env("REQUEST_TIMEOUT", "300")))

    # --- Data & vector DB -------------------------------------------------
    data_dir: Path = field(default_factory=lambda: Path(_env("DATA_DIR", str(PROJECT_ROOT / "data"))))
    chroma_dir: Path = field(default_factory=lambda: Path(_env("CHROMA_DIR", str(PROJECT_ROOT / "chroma_db"))))
    collection_name: str = field(default_factory=lambda: _env("COLLECTION_NAME", "helpdesk_knowledge"))

    # --- Retrieval --------------------------------------------------------
    top_k: int = field(default_factory=lambda: int(_env("TOP_K", "5")))
    # Chunks with cosine similarity below this are dropped before reaching the LLM.
    min_similarity: float = field(default_factory=lambda: float(_env("MIN_SIMILARITY", "0.40")))

    @property
    def tickets_file(self) -> Path:
        return self.data_dir / "tickets.json"

    @property
    def kb_dir(self) -> Path:
        return self.data_dir / "kb_articles"


settings = Settings()

"""Build (or rebuild) the vector index from data/tickets.json and data/kb_articles/.

Usage:
    python scripts/ingest.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from helpdesk_rag.config import settings  # noqa: E402
from helpdesk_rag.ollama_client import OllamaError  # noqa: E402
from helpdesk_rag.rag import HelpdeskRAG  # noqa: E402


def main() -> int:
    print(f"Embedding model : {settings.embed_model} @ {settings.ollama_url}")
    print(f"Data            : {settings.data_dir}")
    print(f"Vector DB       : {settings.chroma_dir} (collection '{settings.collection_name}')")
    try:
        stats = HelpdeskRAG().ingest(reset=True)
    except OllamaError as e:
        print(f"\nERROR: {e}")
        print(f"Tip: run `ollama pull {settings.embed_model}` and make sure Ollama is running.")
        return 1
    print(
        f"\nIndexed {stats['chunks']} chunks "
        f"({stats['tickets']} resolved tickets + {stats['article_sections']} KB article sections) "
        f"in {stats['seconds']}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

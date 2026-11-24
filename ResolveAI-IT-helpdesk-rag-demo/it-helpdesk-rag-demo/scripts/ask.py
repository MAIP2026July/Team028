"""Quick command-line check of the pipeline (handy for debugging without the UI).

Usage:
    python scripts/ask.py "My VPN keeps disconnecting"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from helpdesk_rag.rag import HelpdeskRAG  # noqa: E402


def main() -> None:
    question = " ".join(sys.argv[1:]) or "My VPN keeps disconnecting every few minutes"
    result = HelpdeskRAG().ask(question)
    print(f"Q: {question}\n\nRetrieved in {result.retrieval_ms:.0f} ms:")
    for c in result.chunks:
        print(f"  {c.similarity:.3f}  [{c.citation}] {c.metadata.get('title')}")
    print("\nA: ", end="", flush=True)
    for token in result.answer_stream:
        print(token, end="", flush=True)
    print()


if __name__ == "__main__":
    main()

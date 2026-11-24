"""The RAG pipeline: query -> embed -> KNN in Chroma -> prompt -> LLM -> answer."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Iterator

from . import ollama_client
from .config import settings
from .loaders import load_all
from .ollama_client import Embedder, OllamaEmbedder
from .prompts import NO_CONTEXT_ANSWER, build_messages
from .vector_store import RetrievedChunk, VectorStore

ChatFn = Callable[[list[dict], str | None], Iterator[str]]


@dataclass
class RAGResult:
    question: str
    chunks: list[RetrievedChunk]
    messages: list[dict]
    retrieval_ms: float
    answer_stream: Iterator[str]
    timings: dict = field(default_factory=dict)


class HelpdeskRAG:
    def __init__(self, embedder: Embedder | None = None, chat_fn: ChatFn | None = None,
                 store: VectorStore | None = None):
        self.embedder = embedder or OllamaEmbedder()
        self.chat_fn = chat_fn or ollama_client.chat_stream
        self.store = store or VectorStore(
            settings.chroma_dir, settings.collection_name, self.embedder,
            embed_model_name=getattr(self.embedder, "model", "custom"),
        )

    # ---------------------------------------------------------------- ingest
    def ingest(self, reset: bool = True) -> dict:
        docs = load_all(settings.tickets_file, settings.kb_dir)
        if reset:
            self.store.reset()
        t0 = time.perf_counter()
        self.store.add_documents(docs)
        return {
            "chunks": len(docs),
            "tickets": sum(d.metadata["source_type"] == "ticket" for d in docs),
            "article_sections": sum(d.metadata["source_type"] == "article" for d in docs),
            "seconds": round(time.perf_counter() - t0, 2),
        }

    # ---------------------------------------------------------------- query
    def retrieve(self, question: str, k: int | None = None, source_type: str | None = None,
                 min_similarity: float | None = None) -> tuple[list[RetrievedChunk], float]:
        t0 = time.perf_counter()
        chunks = self.store.search(
            question,
            k=k or settings.top_k,
            source_type=source_type,
            min_similarity=settings.min_similarity if min_similarity is None else min_similarity,
        )
        return chunks, (time.perf_counter() - t0) * 1000

    def ask(self, question: str, k: int | None = None, source_type: str | None = None,
            min_similarity: float | None = None, model: str | None = None) -> RAGResult:
        chunks, ms = self.retrieve(question, k, source_type, min_similarity)
        messages = build_messages(question, chunks)
        if not chunks:
            stream: Iterator[str] = iter([NO_CONTEXT_ANSWER])
        else:
            stream = self.chat_fn(messages, model)
        return RAGResult(question, chunks, messages, ms, stream)

    def ask_text(self, question: str, **kwargs) -> tuple[str, list[RetrievedChunk]]:
        r = self.ask(question, **kwargs)
        return "".join(r.answer_stream).strip(), r.chunks

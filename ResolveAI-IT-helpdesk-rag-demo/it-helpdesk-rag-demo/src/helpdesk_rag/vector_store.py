"""ChromaDB wrapper.

We compute embeddings ourselves (via Ollama) and hand Chroma the raw vectors,
so it is obvious where each step of the pipeline happens. The collection uses
cosine distance; Chroma's HNSW index performs the (approximate) K-nearest-
neighbour search.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import chromadb

from .loaders import Document
from .ollama_client import Embedder


@dataclass
class RetrievedChunk:
    id: str
    text: str
    metadata: dict
    similarity: float  # cosine similarity, 1.0 = identical direction

    @property
    def citation(self) -> str:
        return self.metadata.get("source_id", self.id)


class VectorStore:
    def __init__(self, persist_dir: Path, collection_name: str, embedder: Embedder,
                 embed_model_name: str = "unknown"):
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(persist_dir))
        self.collection_name = collection_name
        self.embedder = embedder
        self.embed_model_name = embed_model_name
        self.collection = self._get_collection()

    def _get_collection(self):
        return self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=None,  # we supply vectors ourselves
            metadata={"hnsw:space": "cosine", "embed_model": self.embed_model_name},
        )

    # ------------------------------------------------------------------ write
    def reset(self) -> None:
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:  # collection may not exist yet
            pass
        self.collection = self._get_collection()

    def add_documents(self, docs: list[Document], batch_size: int = 64) -> int:
        for i in range(0, len(docs), batch_size):
            batch = docs[i : i + batch_size]
            vectors = self.embedder.embed_documents([d.text for d in batch])
            self.collection.upsert(
                ids=[d.id for d in batch],
                documents=[d.text for d in batch],
                metadatas=[d.metadata for d in batch],
                embeddings=vectors,
            )
        return len(docs)

    # ------------------------------------------------------------------ read
    def count(self) -> int:
        return self.collection.count()

    def indexed_embed_model(self) -> str | None:
        return (self.collection.metadata or {}).get("embed_model")

    def search(self, query: str, k: int = 5, source_type: str | None = None,
               min_similarity: float = 0.0) -> list[RetrievedChunk]:
        """Embed the query and return the k nearest chunks (KNN)."""
        if self.count() == 0:
            return []
        query_vec = self.embedder.embed_query(query)
        where = {"source_type": source_type} if source_type else None
        res = self.collection.query(
            query_embeddings=[query_vec],
            n_results=min(k, self.count()),
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        chunks = [
            RetrievedChunk(id=i, text=doc, metadata=meta, similarity=round(1.0 - dist, 4))
            for i, doc, meta, dist in zip(
                res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]
            )
        ]
        return [c for c in chunks if c.similarity >= min_similarity]

"""Offline tests: no Ollama needed. A tiny bag-of-words "embedder" stands in for
the real model so we can check loading, indexing, KNN retrieval and prompting."""

import hashlib
import math
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from helpdesk_rag.config import settings  # noqa: E402
from helpdesk_rag.loaders import load_articles, load_tickets  # noqa: E402
from helpdesk_rag.prompts import NO_CONTEXT_ANSWER  # noqa: E402
from helpdesk_rag.rag import HelpdeskRAG  # noqa: E402
from helpdesk_rag.vector_store import VectorStore  # noqa: E402

DIM = 512
STOP = {"the", "a", "to", "and", "is", "my", "i", "of", "in", "on", "it", "for", "with", "not"}


class HashingEmbedder:
    model = "test-hashing"

    def _vec(self, text: str) -> list[float]:
        v = [0.0] * DIM
        for w in re.findall(r"[a-z0-9]+", text.lower()):
            if w in STOP:
                continue
            v[int(hashlib.md5(w.encode()).hexdigest(), 16) % DIM] += 1.0
        n = math.sqrt(sum(x * x for x in v)) or 1.0
        return [x / n for x in v]

    def embed_documents(self, texts):
        return [self._vec(t) for t in texts]

    def embed_query(self, text):
        return self._vec(text)


def fake_chat(messages, model=None):
    yield "stub answer"


@pytest.fixture(scope="module")
def rag(tmp_path_factory):
    emb = HashingEmbedder()
    store = VectorStore(tmp_path_factory.mktemp("chroma"), "test", emb, emb.model)
    r = HelpdeskRAG(embedder=emb, chat_fn=fake_chat, store=store)
    r.ingest()
    return r


def test_open_tickets_are_not_indexed():
    ids = {d.metadata["source_id"] for d in load_tickets(settings.tickets_file)}
    assert "INC-1035" not in ids  # status Open
    assert "INC-1001" in ids


def test_articles_are_split_into_sections():
    docs = load_articles(settings.kb_dir)
    vpn = [d for d in docs if d.metadata["source_id"] == "KB-001"]
    assert len(vpn) >= 4
    assert all(d.text.startswith("Article KB-001") for d in vpn)


def test_ingest_counts(rag):
    assert rag.store.count() > 40


@pytest.mark.parametrize("question, expected", [
    ("VPN keeps disconnecting every 10 minutes", {"KB-001", "INC-1001"}),
    ("new phone MFA authenticator old phone", {"KB-003", "INC-1006"}),
    ("outlook loading profile hangs", {"KB-004", "INC-1008"}),
    ("restore deleted folder shared drive", {"KB-008", "INC-1025"}),
])
def test_knn_finds_relevant_sources(rag, question, expected):
    chunks, _ = rag.retrieve(question, k=5, min_similarity=0.0)
    found = {c.citation for c in chunks}
    assert found & expected, f"{question!r} -> {found}"
    sims = [c.similarity for c in chunks]
    assert sims == sorted(sims, reverse=True)


def test_source_filter(rag):
    chunks, _ = rag.retrieve("vpn", k=5, source_type="ticket", min_similarity=0.0)
    assert chunks and all(c.metadata["source_type"] == "ticket" for c in chunks)


def test_prompt_contains_context_and_question(rag):
    r = rag.ask("printer offline", min_similarity=0.0)
    prompt = r.messages[1]["content"]
    assert "printer offline" in prompt and "[" in prompt
    assert "".join(r.answer_stream) == "stub answer"


def test_irrelevant_question_skips_llm(rag):
    r = rag.ask("zzqx blorf wibble", min_similarity=0.5)
    assert r.chunks == []
    assert "".join(r.answer_stream) == NO_CONTEXT_ANSWER

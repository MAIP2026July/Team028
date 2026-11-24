"""Streamlit UI for the IT Helpdesk RAG demo.

Run:  streamlit run app.py
"""

import sys
import time
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from helpdesk_rag import ollama_client  # noqa: E402
from helpdesk_rag.config import settings  # noqa: E402
from helpdesk_rag.ollama_client import OllamaError  # noqa: E402
from helpdesk_rag.rag import HelpdeskRAG  # noqa: E402

st.set_page_config(page_title="ResolveAI (RAG demo)", page_icon="🛠️", layout="wide")

SAMPLE_QUESTIONS = [
    "My VPN keeps disconnecting every few minutes",
    "I got a new phone and MFA still goes to my old one",
    "Outlook is stuck on loading profile",
    "I deleted a folder on the shared drive by mistake",
    "How do I add the office printer?",
    "I clicked a link in a suspicious email",
]
EMBED_HINTS = ("embed", "nomic", "bge", "minilm", "e5")


@st.cache_resource(show_spinner=False)
def get_rag() -> HelpdeskRAG:
    return HelpdeskRAG()


def render_sources(chunks, retrieval_ms: float | None = None, messages=None):
    label = f"🔎 Retrieved context — {len(chunks)} nearest neighbours"
    if retrieval_ms is not None:
        label += f" ({retrieval_ms:.0f} ms)"
    with st.expander(label, expanded=False):
        if not chunks:
            st.info("Nothing passed the similarity threshold, so the LLM was not called.")
        for rank, c in enumerate(chunks, 1):
            is_article = c.metadata.get("source_type") == "article"
            badge = "📘 KB article" if is_article else "🎫 Resolved ticket"
            sub = f" › {c.metadata.get('section')}" if is_article else ""
            st.markdown(f"**#{rank} · {badge} · `{c.citation}`** — {c.metadata.get('title')}{sub}")
            st.progress(max(0.0, min(1.0, c.similarity)), text=f"cosine similarity {c.similarity:.3f}")
            st.code(c.text, language=None, wrap_lines=True)
    if messages:
        with st.expander("🧾 Prompt sent to the LLM"):
            for m in messages:
                st.markdown(f"**{m['role']}**")
                st.code(m["content"], language=None, wrap_lines=True)


# ----------------------------------------------------------------------------- sidebar
rag = get_rag()
models = ollama_client.list_models()
chat_models = [m for m in models if not any(h in m.lower() for h in EMBED_HINTS)]
embed_installed = any(m.split(":")[0] == settings.embed_model.split(":")[0] for m in models)

with st.sidebar:
    st.header("⚙️ Settings")
    if models:
        st.success(f"Ollama running · {len(models)} models")
    else:
        st.error(f"Ollama not reachable at {settings.ollama_url}. Start it with `ollama serve`.")
    if models and not embed_installed:
        st.warning(f"Embedding model missing. Run:\n\n`ollama pull {settings.embed_model}`")

    default_idx = next((i for i, m in enumerate(chat_models)
                        if m.split(":")[0] == settings.chat_model.split(":")[0]), 0)
    model = st.selectbox("Answer model (LLM)", chat_models or [settings.chat_model], index=default_idx)
    top_k = st.slider("K (nearest neighbours)", 1, 10, settings.top_k)
    min_sim = st.slider("Min. similarity", 0.0, 1.0, settings.min_similarity, 0.05,
                        help="Chunks less similar than this are not sent to the LLM.")
    source = st.radio("Search in", ["Everything", "KB articles only", "Past tickets only"])
    source_type = {"KB articles only": "article", "Past tickets only": "ticket"}.get(source)

    st.divider()
    st.caption(f"Vector DB: **{rag.store.count()}** chunks · embeddings: `{settings.embed_model}`")
    if st.button("🔄 Rebuild index", use_container_width=True):
        with st.spinner("Embedding tickets and articles…"):
            try:
                stats = rag.ingest(reset=True)
                st.success(f"Indexed {stats['chunks']} chunks in {stats['seconds']}s")
                time.sleep(1)
                st.rerun()
            except OllamaError as e:
                st.error(str(e))
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    with st.expander("How it works"):
        st.markdown(
            "1. Tickets & KB articles are split into chunks and **embedded** into vectors.\n"
            "2. Vectors are stored in **ChromaDB**.\n"
            "3. Your question is embedded with the same model.\n"
            "4. **KNN** (cosine) finds the K most similar chunks.\n"
            "5. Those chunks + your question go to the **LLM**, which answers with citations."
        )

# ----------------------------------------------------------------------------- main
st.title("🛠️ ResolveAI")
st.caption("Retrieval-Augmented Generation over past tickets and knowledge-base articles · runs 100% locally")

if "history" not in st.session_state:
    st.session_state.history = []

if rag.store.count() == 0:
    st.warning("The vector index is empty. Click **🔄 Rebuild index** in the sidebar "
               "(or run `python scripts/ingest.py`) before asking questions.")

for turn in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(turn["question"])
    with st.chat_message("assistant"):
        st.markdown(turn["answer"])
        st.caption(turn["meta"])
        render_sources(turn["chunks"], turn["retrieval_ms"])

clicked = None
if not st.session_state.history:
    st.markdown("**Try one of these:**")
    cols = st.columns(3)
    for i, q in enumerate(SAMPLE_QUESTIONS):
        if cols[i % 3].button(q, key=f"sample{i}", use_container_width=True):
            clicked = q

question = st.chat_input("Describe your IT problem…") or clicked

if question:
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching tickets and articles…"):
                result = rag.ask(question, k=top_k, source_type=source_type,
                                 min_similarity=min_sim, model=model)
            t0 = time.perf_counter()
            answer = st.write_stream(result.answer_stream)
            gen_s = time.perf_counter() - t0
            meta = (f"model `{model}` · retrieval {result.retrieval_ms:.0f} ms · "
                    f"generation {gen_s:.1f} s · {len(result.chunks)} sources")
            st.caption(meta)
            render_sources(result.chunks, result.retrieval_ms, result.messages)
            st.session_state.history.append({
                "question": question, "answer": answer, "chunks": result.chunks,
                "retrieval_ms": result.retrieval_ms, "meta": meta,
            })
        except OllamaError as e:
            st.error(str(e))

"""Prompt templates. Kept separate so they are easy to tweak and review."""

from __future__ import annotations

SYSTEM_PROMPT = """You are an IT Service Desk assistant for Acme Corp.
Answer the user's IT question using ONLY the context provided below, which contains
knowledge-base articles and previously resolved support tickets.

Rules:
- Give clear, numbered troubleshooting steps when steps are relevant.
- Cite every source you use in square brackets, e.g. [KB-001] or [INC-1002].
- Prefer official KB articles for procedures; use past tickets as supporting evidence
  ("A similar issue was fixed by ...").
- If the context does not contain the answer, say you could not find it in the
  knowledge base and recommend raising a ticket with the Service Desk. Do not invent
  URLs, commands, or policies.
- Never ask the user to share their password.
- Keep the answer concise (under ~200 words)."""

NO_CONTEXT_ANSWER = (
    "I couldn't find anything relevant to that in the knowledge base or past tickets. "
    "Please raise a ticket with the Service Desk and include any error message you see, "
    "when the problem started, and what you have already tried."
)


def format_context(chunks) -> str:
    blocks = []
    for c in chunks:
        kind = "KB ARTICLE" if c.metadata.get("source_type") == "article" else "RESOLVED TICKET"
        blocks.append(f"[{c.citation}] ({kind}, similarity {c.similarity:.2f})\n{c.text}")
    return "\n\n---\n\n".join(blocks)


def build_messages(question: str, chunks) -> list[dict]:
    user_msg = (
        f"Context:\n{format_context(chunks)}\n\n"
        f"=====\nUser question: {question}\n\n"
        "Answer using only the context above, with citations."
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

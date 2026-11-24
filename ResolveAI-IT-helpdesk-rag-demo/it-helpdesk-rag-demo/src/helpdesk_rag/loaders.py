"""Turn raw tickets and KB articles into `Document` chunks ready for embedding.

Chunking strategy
-----------------
* Ticket  -> 1 chunk (title + description + resolution). Tickets are short and
  self-contained, so splitting them would lose the problem/solution link.
* Article -> 1 chunk per `## section`, each prefixed with the article title so
  the chunk still makes sense on its own when retrieved.
* Only Resolved/Closed tickets are indexed: an open ticket has no answer to offer.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

INDEXABLE_TICKET_STATUSES = {"resolved", "closed"}


@dataclass
class Document:
    id: str
    text: str
    metadata: dict = field(default_factory=dict)


# --------------------------------------------------------------------------- tickets
def load_tickets(path: Path) -> list[Document]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    docs: list[Document] = []
    for t in raw:
        if str(t.get("status", "")).lower() not in INDEXABLE_TICKET_STATUSES:
            continue
        if not t.get("resolution"):
            continue
        text = (
            f"Ticket {t['ticket_id']}: {t['title']}\n"
            f"Category: {t.get('category', '')}\n"
            f"Problem: {t['description']}\n"
            f"Resolution: {t['resolution']}"
        )
        docs.append(
            Document(
                id=f"ticket::{t['ticket_id']}",
                text=text,
                metadata={
                    "source_type": "ticket",
                    "source_id": t["ticket_id"],
                    "title": t["title"],
                    "category": t.get("category", ""),
                    "priority": t.get("priority", ""),
                    "resolved_at": t.get("resolved_at") or "",
                    "tags": ", ".join(t.get("tags", [])),
                },
            )
        )
    return docs


# --------------------------------------------------------------------------- articles
_FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_front_matter(md: str) -> tuple[dict, str]:
    """Minimal `key: value` front-matter parser (avoids a YAML dependency)."""
    m = _FRONT_MATTER.match(md)
    if not m:
        return {}, md
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, md[m.end():]


def _split_sections(body: str) -> list[tuple[str, str]]:
    """Split markdown on `## ` headings -> [(heading, content), ...]."""
    sections: list[tuple[str, str]] = []
    current_heading, buf = "Introduction", []
    for line in body.splitlines():
        if line.startswith("## "):
            if "".join(buf).strip():
                sections.append((current_heading, "\n".join(buf).strip()))
            current_heading, buf = line[3:].strip(), []
        else:
            buf.append(line)
    if "".join(buf).strip():
        sections.append((current_heading, "\n".join(buf).strip()))
    return sections


def load_articles(kb_dir: Path) -> list[Document]:
    docs: list[Document] = []
    for path in sorted(Path(kb_dir).glob("*.md")):
        meta, body = _parse_front_matter(path.read_text(encoding="utf-8"))
        article_id = meta.get("id", path.stem)
        title = meta.get("title", path.stem)
        for i, (heading, content) in enumerate(_split_sections(body)):
            docs.append(
                Document(
                    id=f"article::{article_id}::{i}",
                    text=f"Article {article_id}: {title}\nSection: {heading}\n{content}",
                    metadata={
                        "source_type": "article",
                        "source_id": article_id,
                        "title": title,
                        "section": heading,
                        "category": meta.get("category", ""),
                        "last_updated": meta.get("last_updated", ""),
                        "file": path.name,
                    },
                )
            )
    return docs


def load_all(tickets_file: Path, kb_dir: Path) -> list[Document]:
    return load_tickets(tickets_file) + load_articles(kb_dir)

#!/usr/bin/env python3
"""Import authoritative EHDS articles from local Official Journal HTML.

Default source: data/raw/32025R0327_oj_en.html
Default output: ehds_index/
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW_PATH = PROJECT_ROOT / "data" / "raw" / "32025R0327_oj_en.html"
INDEX_ROOT = PROJECT_ROOT / "ehds_index"
CELEX = "32025R0327"
REGULATION = "Reg. (EU) 2025/327"
DATE_ENACTED = "2025-03-11"

SECONDARY_USE_ARTICLES = set(range(50, 80))
PRIMARY_USE_ARTICLES = set(range(14, 49))
GOVERNANCE_ARTICLES = set(range(80, 106))


@dataclass(frozen=True)
class EHDSArticle:
    article: int
    article_id: str
    title: str
    text: str
    paragraphs: List[str]
    source_path: str = "data/raw/32025R0327_oj_en.html"
    celex: str = CELEX

    @property
    def stable_id(self) -> str:
        return f"EHDS-2025-327-A{self.article:03d}"

    @property
    def filename(self) -> str:
        return f"EHDS-2025-327_Art-{self.article:03d}.md"


class TextHTMLParser(HTMLParser):
    """Extract visible text tokens from EUR-Lex/OJ XHTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: List[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[no-untyped-def]
        if tag.lower() in {"script", "style", "noscript"}:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript"} and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = normalize_ws(data)
        if text:
            self.items.append(text)


def normalize_ws(text: str) -> str:
    text = unescape(text).replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _is_article_heading(text: str) -> Optional[int]:
    match = re.fullmatch(r"Article\s+([1-9][0-9]{0,2})", normalize_ws(text))
    if not match:
        return None
    number = int(match.group(1))
    if 1 <= number <= 105:
        return number
    return None


def _is_noise_token(text: str) -> bool:
    if not text:
        return True
    if re.fullmatch(r"\(?\d{1,3}\)?", text):
        return True
    if text in {"(", ")", ",", ";"}:
        return True
    return False


def _join_body_tokens(tokens: Iterable[str]) -> str:
    paragraphs: List[str] = []
    pending_label: Optional[str] = None
    footnote_buffer: List[str] = []

    for raw in tokens:
        token = normalize_ws(raw)
        if _is_noise_token(token):
            # Footnote markers are not useful as standalone paragraphs.
            continue
        if re.fullmatch(r"\([a-z]{1,3}\)|\([ivxlcdm]+\)", token, flags=re.IGNORECASE):
            pending_label = token
            continue
        if pending_label:
            token = f"{pending_label} {token}"
            pending_label = None
        if token.startswith("OJ ") or re.match(r"^ELI:\s", token):
            footnote_buffer.append(token)
            continue
        paragraphs.append(token)

    if footnote_buffer:
        paragraphs.extend(footnote_buffer)
    return "\n\n".join(paragraphs)


def _split_paragraphs(text: str) -> List[str]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return paras


def parse_oj_html(path: Path = DEFAULT_RAW_PATH) -> List[EHDSArticle]:
    """Parse local EUR-Lex/OJ HTML and return official EHDS Article records."""
    html = path.read_text(encoding="utf-8", errors="replace")
    parser = TextHTMLParser()
    parser.feed(html)
    tokens = parser.items

    heading_positions: List[tuple[int, int]] = []
    for idx, token in enumerate(tokens):
        number = _is_article_heading(token)
        if number is None:
            continue
        # Keep real article headings: followed by a title, not merely prose mention.
        if idx + 1 < len(tokens) and not re.match(r"^\d+\.\s", tokens[idx + 1]):
            heading_positions.append((idx, number))

    # Deduplicate repeated table-of-contents/legal references by requiring a monotonic
    # article sequence. The OJ body contains exactly Article 1..105 in order.
    selected: List[tuple[int, int]] = []
    expected = 1
    for idx, number in heading_positions:
        if number == expected:
            selected.append((idx, number))
            expected += 1
            if expected == 106:
                break

    if len(selected) != 105:
        raise ValueError(f"Expected 105 official article headings, found {len(selected)}")

    articles: List[EHDSArticle] = []
    for pos, (idx, number) in enumerate(selected):
        end = selected[pos + 1][0] if pos + 1 < len(selected) else len(tokens)
        title = normalize_ws(tokens[idx + 1]) if idx + 1 < end else ""
        body_tokens = tokens[idx + 2 : end]
        text = _join_body_tokens(body_tokens)
        paragraphs = _split_paragraphs(text)
        if not title or not paragraphs:
            raise ValueError(f"Article {number} parsed without title/body")
        articles.append(
            EHDSArticle(
                article=number,
                article_id=f"Art.{number}",
                title=title,
                text=text,
                paragraphs=paragraphs,
                source_path=str(path.relative_to(PROJECT_ROOT)) if path.is_relative_to(PROJECT_ROOT) else str(path),
            )
        )
    return articles


def category_for_article(number: int) -> str:
    if number in SECONDARY_USE_ARTICLES:
        return "secondary_use"
    if number in PRIMARY_USE_ARTICLES:
        return "primary_use"
    if number in GOVERNANCE_ARTICLES:
        return "governance"
    return "general"


def chapter_for_article(number: int) -> str:
    if 1 <= number <= 13:
        return "I-II"
    if number in PRIMARY_USE_ARTICLES:
        return "III-IV"
    if number in SECONDARY_USE_ARTICLES:
        return "V"
    return "VI+"


def yaml_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def render_article(article: EHDSArticle) -> str:
    blocks: List[str] = []
    anchors: List[str] = []
    for idx, para in enumerate(article.paragraphs, start=1):
        anchor = f"A{article.article:03d}-P{idx}"
        anchors.append(anchor)
        blocks.append(f"## Para {idx}\n[[{anchor}]]\n\n{para}")

    anchors_block = "\n".join(f"- [[{anchor}]] :: paragraph {i}" for i, anchor in enumerate(anchors, start=1))
    return f"""---
regulation: {yaml_quote(REGULATION)}
article: {article.article}
title: {yaml_quote(article.title)}
chapter: {yaml_quote(chapter_for_article(article.article))}
stable_id: {yaml_quote(article.stable_id)}
category: {yaml_quote(category_for_article(article.article))}
date_enacted: {yaml_quote(DATE_ENACTED)}
celex: {yaml_quote(article.celex)}
source_path: {yaml_quote(article.source_path)}
source_type: "official_journal_html"
---

# Art. {article.article} — {article.title}

## Index Summary
> **Stable ID:** `{article.stable_id}`  
> **Regulation:** {REGULATION}  
> **Article:** {article.article}  
> **Category:** {category_for_article(article.article)}  
> **Source:** `{article.source_path}`

{chr(10).join(blocks)}

## Audit Anchors
{anchors_block}
"""


def backup_existing_index(index_root: Path) -> Optional[Path]:
    if not index_root.exists() or not any(index_root.glob("*.md")):
        return None
    backup_root = PROJECT_ROOT / "data" / "backups" / "ehds_index_pre_raw_rebuild"
    if backup_root.exists():
        shutil.rmtree(backup_root)
    backup_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(index_root, backup_root)
    return backup_root


def rebuild_index(raw_path: Path = DEFAULT_RAW_PATH, index_root: Path = INDEX_ROOT, *, backup: bool = True) -> List[Path]:
    articles = parse_oj_html(raw_path)
    if len(articles) != 105:
        raise ValueError(f"Refusing to rebuild: expected 105 articles, got {len(articles)}")
    if backup:
        backup_existing_index(index_root)
    index_root.mkdir(parents=True, exist_ok=True)
    for old in index_root.glob("*.md"):
        old.unlink()
    written: List[Path] = []
    for article in articles:
        out = index_root / article.filename
        out.write_text(render_article(article), encoding="utf-8")
        written.append(out)
    return written


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Rebuild EHDS Index from local official OJ HTML")
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW_PATH, help="Path to 32025R0327 OJ HTML")
    parser.add_argument("--index-root", type=Path, default=INDEX_ROOT, help="Output ehds_index directory")
    parser.add_argument("--check", action="store_true", help="Parse and report article count without writing")
    parser.add_argument("--rebuild-index", action="store_true", help="Write authoritative Index Markdown files")
    parser.add_argument("--no-backup", action="store_true", help="Do not backup existing ehds_index before rebuild")
    args = parser.parse_args(argv)

    if args.check or not args.rebuild_index:
        articles = parse_oj_html(args.raw)
        print(f"Parsed {len(articles)} articles from {args.raw}")
        for article in articles[:3] + articles[-3:]:
            print(f"Art.{article.article:03d}: {article.title} ({len(article.text)} chars)")
        if not args.rebuild_index:
            return 0

    written = rebuild_index(args.raw, args.index_root, backup=not args.no_backup)
    print(f"Wrote {len(written)} Index files to {args.index_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

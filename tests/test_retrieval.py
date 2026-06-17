#!/usr/bin/env python3
"""Tests for the BM25-based retrieval engine."""

from src.ehds_embedding import get_engine


def test_ethical_governance_finds_d82():
    engine = get_engine()
    results = engine.semantic_search("ethical governance recommendations", top_k=5)
    assert any("d8.2" in r["source_path"].lower() for r in results)


def test_art68_identifier_search():
    engine = get_engine()
    results = engine.semantic_search("Art.68 data permit", top_k=5)
    assert len(results) > 0
    sources = " ".join(r["source_path"] for r in results)
    assert "art" in sources.lower() or "68" in sources or "data permit" in " ".join(r["text"] for r in results).lower()


def test_data_chunk_merge():
    """Data layer chunks should contain multiple paragraphs."""
    engine = get_engine()
    results = engine.semantic_search("ethical governance recommendations", top_k=5)
    data_results = [r for r in results if r["layer"] == "data"]
    assert len(data_results) > 0
    # With 5-paragraph merge, each data chunk should be > 500 chars
    assert any(len(r["text"]) > 500 for r in data_results), "merged chunk too short"


def test_d82_metadata_filtered():
    """D8.2 chunks should contain substantive content, not frontmatter metadata."""
    engine = get_engine()
    results = engine.semantic_search("ethical governance recommendations", top_k=10)
    d82_texts = [r["text"] for r in results if "d8.2" in r["source_path"].lower()]
    assert len(d82_texts) > 0, "D8.2 must be in top-10 results"
    # Verify D8.2 chunk is substantive (not frontmatter like "Document info", "Disclaimer")
    for t in d82_texts:
        assert "disclaimer" not in t.lower(), "D8.2 chunk should not contain disclaimer metadata"
        assert "document info" not in t.lower()[:200], \
            "D8.2 chunk should not start with frontmatter"

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
    assert "art" in sources.lower() or "68" in sources or "data permit" in " ".join(r["text"] for r in results)

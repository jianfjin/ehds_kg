#!/usr/bin/env python3
"""Tests for the BM25-based retrieval engine."""

from src.ehds_embedding import get_engine


def test_ethical_governance_finds_d82():
    engine = get_engine()
    results = engine.semantic_search("ethical governance recommendations", top_k=10)
    assert any("d8.2" in r["source_path"].lower() for r in results)


def test_art68_identifier_search():
    engine = get_engine()
    results = engine.semantic_search("Art.68 data permit", top_k=10)
    assert len(results) > 0
    sources = " ".join(r["source_path"] for r in results)
    assert "art" in sources.lower() or "68" in sources or "data permit" in " ".join(r["text"] for r in results).lower()


def test_heading_aware_chunks_have_metadata():
    """Data layer chunks should carry document_id and section_id."""
    engine = get_engine()
    results = engine.semantic_search("ethical governance recommendations", top_k=10)
    data_results = [r for r in results if r["layer"] == "data"]
    assert len(data_results) > 0
    for r in data_results:
        assert r["metadata"].get("document_id"), f"missing document_id in {r['source_path']}"
        assert "section_id" in r["metadata"], f"missing section_id in {r['source_path']}"


def test_d82_chunks_are_substantive():
    """D8.2 chunks should contain substantive content, not frontmatter metadata."""
    engine = get_engine()
    results = engine.semantic_search("ethical governance recommendations", top_k=10)
    d82_texts = [r["text"] for r in results if "d8.2" in r["source_path"].lower()]
    assert len(d82_texts) > 0, "D8.2 must be in top-10 results"
    for t in d82_texts:
        assert "disclaimer" not in t.lower(), "D8.2 chunk should not contain disclaimer metadata"
        assert "document info" not in t.lower()[:200], \
            "D8.2 chunk should not start with frontmatter"


def test_diversity_rerank_limits_per_document():
    """No single document should dominate the top-10 results."""
    engine = get_engine()
    results = engine.semantic_search("collaboration challenges in EHDS", top_k=10)
    assert len(results) == 10
    doc_counts = {}
    for r in results:
        doc_id = r["metadata"].get("document_id") or r["source_path"]
        doc_counts[doc_id] = doc_counts.get(doc_id, 0) + 1
    max_count = max(doc_counts.values())
    assert max_count <= 4, f"single document appears {max_count} times in top-10"


def test_results_sorted_by_document_then_section():
    """Final ordering should group by document_id and sort by section_id."""
    engine = get_engine()
    results = engine.semantic_search("ethical governance recommendations", top_k=10)
    data_results = [r for r in results if r["layer"] == "data"]
    if len(data_results) >= 2:
        keys = [
            (r["metadata"].get("document_id", ""), r["metadata"].get("section_id", ""))
            for r in data_results
        ]
        def _section_key(s):
            try:
                return tuple(int(p) for p in s.split(".") if p)
            except (ValueError, AttributeError):
                return (999,)
        sorted_keys = sorted(keys, key=lambda k: (k[0], _section_key(k[1])))
        assert keys == sorted_keys, "results not ordered by (document_id, section_id)"

# EHDS KG Retrieval: First-Principles Architecture Analysis

**Analyst:** CVO (Elon Musk persona)
**Date:** 2026-05-12
**Subject:** Is full-file-read the optimal retrieval fix? What would I build from scratch?

---

## 1. The System as It Stands

### Data Scale
- 20 Wiki entries (avg 6KB each, max 13KB — Penalties/Fees)
- 37 Index articles (avg 2KB each)
- 4 KB rules
- Total: 604 chunks across 57 source files
- TF-IDF cache: 463KB pickle + 15MB SQLite (15.5MB total)

### The Pipeline (current, post-fix)

```
QUERY ─► TF-IDF semantic_search(top_k=5)
     ─► deduplicate by source_path (keep first chunk per file)
     ─► for each unique source_path:
          ─► read FULL file from disk
          ─► strip YAML frontmatter
          ─► take body[:2000]
     ─► return results
```

### The Original Bug

For query "data linkage", `semantic_search(top_k=5)` returned 5 chunks — all from
Data_Linkage.md. The first chunk (chunk #663) was just the title + first heading:

    "Data Linkage in EHDS\n# Data Linkage in EHDS"

The old `_add_result` deduplication killed all subsequent chunks from the same file,
leaving only this heading. The LLM saw "cannot explain — only saw a heading."

### The Fix

Two changes applied:
1. Path migration: `~/.hermes/docs/` → `~/projects/ehds_kg/`
2. Instead of returning chunk text, read the full file body and return body[:2000]

---

## 2. Full-File-Read: Performance Analysis

### Latency

| Operation | Cost |
|-----------|------|
| TF-IDF transform (5000-dim × 604 chunks) | ~0.5ms |
| SQLite load (604 rows) | ~1ms |
| File read (1 file, 6KB avg) | ~0.1ms |
| **Total per query, 5 unique files** | **~7ms** |

At this scale, file I/O is negligible. Even reading all 20 Wiki files at once
(120KB total) takes ~0.3ms on an SSD. The bottleneck is SQLite, not file I/O.

### Memory

- TF-IDF matrix in memory: ~604 × 5000 floats ≈ 12MB (sparse — actual ~500KB)
- Chunks loaded from DB per query: ~600 dicts ≈ 500KB (allocated and GC'd each call)
- File read: strings allocated, then GC'd

**Current VM (2 CPU, 1.9GB RAM) handles this comfortably.**

### Scalability Projections

| Growth | Files | Chunks | File I/O (5 files) | DB Load | Verdict |
|--------|-------|--------|---------------------|---------|---------|
| 10× wiki | 200 | ~5,000 | ~1ms | ~10ms | Fine |
| 100× wiki | 2,000 | ~50,000 | ~10ms | ~150ms | DB read becoming bottleneck |
| 1000× wiki | 20,000 | ~500,000 | ~100ms | ~1.5s | Unacceptable, need DB cache |

Bottom line: **flush caching the entire chunks table into memory** would eliminate
the SQLite bottleneck and buy 10× headroom. The file I/O itself isn't the problem
at any reasonable scale for this domain.

---

## 3. The Real Problem: Context Quality, Not Performance

The full-file-read fix is a **correctness fix**, not an optimization. It's a
sledgehammer that ensures the LLM sees *something* useful by dumping the whole
document. But it throws away all the semantic granularity the TF-IDF search
provides.

### Concrete Example

For "data linkage", the current code returns `Data_Linkage.md[:2000]`, which gives:

```
# Data Linkage in EHDS
## Definition (ISO 5127:2017)
> Data linkage is the process of combining datasets...
Source: TEHDAS2 M5.4 Draft Guideline...
## Data Linkage vs. Data Enrichment
| Aspect | Data Linkage | Data Enrichment |
...
```

This is *good* — it starts with the definition and the core distinction table.

But the TF-IDF search's top-matched chunks (the ones we throw away) are:

| Rank | Chunk | Similarity |
|------|-------|------------|
| 1 | Data Linkage vs. Data Enrichment table | 0.7590 |
| 2 | # Data Linkage in EHDS (heading) | 0.7306 |
| 3 | ## Example of Data Linkage | 0.7062 |
| 4 | ## Pitfall: Enrichment That Becomes Linkage | 0.5331 |
| 5 | Definition paragraph | 0.5144 |

The most semantically relevant chunk is the comparison TABLE, not the heading.
With the current fix, we get the heading → definition → table flow anyway
because the document happens to be structured that way. But this is **accidental
correctness**, not engineered correctness.

### When Full-File-Read Fails

Imagine a 50KB Wiki entry structured like:

```
# Broad Topic X
## Introduction (500 words, low relevance)
## Background (2000 words, medium relevance)
## Historical Context (3000 words, zero relevance)
...
## Specific Subtopic Y (800 words, HIGH relevance — this is what the query matches)
...
## References (1000 words)
```

The TF-IDF search correctly identifies Specific Subtopic Y chunks. But the
full-file-read dumps Introduction and Background into the LLM's context,
wasting 2/3 of the context window on irrelevant content. Meanwhile, the
highly relevant Subtopic Y is at char position 5000+ and gets truncated.

**This is the fundamental failure mode: the fix trades semantic precision for
completeness, and completeness without precision is noise.**

---

## 4. Architectural Alternatives (Evaluated)

### A. Chunk Merging (Merge top-K chunks from same file)

```
For each unique source_path:
  - Collect ALL chunks from that file that appeared in top_k=20
  - Concatenate them with "\n---\n" separators
  - Truncate to 2000 chars, preferring higher-ranked chunks
```

**Pros:** Uses semantic ranking. No file I/O. Preserves relevance ordering.
**Cons:** Chunks may overlap or have gaps. Only gets content from matched chunks.
**Verdict:** Better than full-file-read for relevance. Simple to implement.

### B. Sliding Window Around Best Chunk

```
For each unique source_path:
  - Find the highest-ranked chunk
  - Read the file, but center the 2000-char window around that chunk's position
  - Include ±1000 chars of context
```

**Pros:** Contextual coherence. Surrounds the best content with context.
**Cons:** Requires file read (same I/O cost as current fix) PLUS position tracking.
**Verdict:** Better quality than full-file-read, same I/O cost. Implementation
requires storing byte offsets at index time (not currently tracked).

### C. Two-Pass: TF-IDF Discovery + Embedding Extraction

```
Pass 1: TF-IDF semantic_search(top_k=20) → identify source files
Pass 2: For each file, compute sentence-transformer embedding similarity
        between query and every paragraph → extract top paragraph + context
```

**Pros:** Best semantic precision. Uses dense embeddings for extraction.
**Cons:** Requires sentence-transformers model (~90MB). No GPU on this VM.
CPU inference of 20 files × 20 paragraphs ≈ 5-10 seconds. Unacceptable.
**Verdict:** Ideal quality, but infeasible on current hardware without GPU.

### D. Pre-Built File Summaries (Index-Time)

```
At index time, for each file:
  - Extract frontmatter metadata
  - Generate a summary: title + first 3 paragraphs + all section headings
  - Store in SQLite as a "file_summaries" table
  
At query time:
  - TF-IDF → identify files
  - Return pre-built summary (no file I/O)
```

**Pros:** Zero I/O at query time. Fastest possible. Consistent.
**Cons:** Static — summaries don't adapt to query. May miss relevant deep content.
**Verdict:** Excellent for "what is X?" queries. Poor for targeted sub-topic queries.
Not a replacement, but a good complementary layer.

### E. Multi-Chunk Retrieval with Content-Aware Dedup

```
semantic_search(top_k=20) → group by source_path
For each source_path:
  - Take top 3 chunks
  - Sort by chunk index (preserve document flow)
  - Merge adjacent chunks (chunk 3 + chunk 4 + chunk 5 → one block)
  - Truncate to 2000 chars
```

**Pros:** Content-aware. Preserves document structure. No file I/O.
**Cons:** Adjacent chunks may have semantic gaps (chunks 3 and 7 aren't merged).
**Verdict:** Best balance of quality, performance, and simplicity.

---

## 5. What I Would Build From Scratch

### First Principles

1. **The job of retrieval is to maximize P(relevant | query) per token delivered to the LLM.**
   Context windows are scarce. Every irrelevant byte is wasted compute.

2. **TF-IDF is a discovery mechanism, not an extraction mechanism.**
   It tells you *which file* and *which region* is relevant. Using it only for
   file discovery is under-utilizing it.

3. **The data is small enough that we can afford richer per-query processing.**
   604 chunks × 500 bytes average = 300KB of text. We can load the entire chunk
   table into memory at startup and never touch disk again.

4. **The VM constraints (2-core, 1.9GB, no GPU) rule out dense embeddings.**
   TF-IDF is the right choice for discovery. But we can be smarter about extraction.

### Proposed Architecture: "Discovery + Intelligent Excerpt"

```
INDEX TIME (unchanged, but add one thing):
  1. Build TF-IDF index from paragraphs (as current)
  2. ALSO store each chunk's:
     - chunk_index (position in file, 1-indexed)
     - byte_offset and byte_length in source file
  3. Load all chunks into an in-memory dict at engine init
     (604 chunks × ~1KB each = ~600KB — trivial)

QUERY TIME:
  1. TF-IDF search with top_k=30 (not 5 — cast a wider net)
  2. Group by source_path, keep top 5 chunks per file
  3. For each source_path:
     a. Sort chunks by chunk_index (restore document order)
     b. Merge adjacent chunks into "blocks" (gap ≤ 2 between indices)
     c. Score each block: sum(similarity) / sqrt(block_size)
     d. Select the highest-scoring block
     e. Extract block text + 100 chars of surrounding context
     f. Truncate to 2000 chars
  4. Rank files by max(block_score), return top 5

CACHING:
  - LRU cache (TTL=300s) for file bodies
  - If cache hit, use exact byte-range extraction (faster + precise context)
  - If cache miss, read file and populate cache
```

### Why This Is Better

| Aspect | Current Fix | Proposed |
|--------|-------------|----------|
| Relevance | Gets file header (luck-dependent) | Gets the region the query actually matches |
| I/O | 1 read per unique file, every query | Cache hit: 0 I/O. Cache miss: 1 read per file |
| Context quality | First 2000 chars of file | 2000 chars centered on best semantic match |
| Scalability | Degrades linearly with file count | Degrades with chunk count only (DB in memory) |
| Memory | Chunks from DB every query | Chunks in memory (~600KB permanent) |
| Implementation complexity | Trivial | Moderate (~100 lines of new code) |

### What I'd Do Differently for Production Scale

If this were going to 10,000+ Wiki entries:

1. **Move TF-IDF to a proper sparse matrix library** (scipy.sparse CSR format
   is already used under the hood by sklearn, but we'd manage it explicitly)

2. **Add a BM25 layer** — TF-IDF with document-length normalization.
   Current TF-IDF doesn't normalize for document length, so long files have
   artificially low per-chunk scores.

3. **Two-tier retrieval:**
   - **Fast path:** Pre-built summaries (none of this "first 2000 chars" nonsense —
     actually generate a summary using extractive methods: first paragraph + all
     section headings + key sentences identified by TF-IDF importance)
   - **Precision path:** The block-based extraction described above

4. **Add a reranker** — even a tiny cross-encoder (e.g., `cross-encoder/ms-marco-MiniLM-L-2-v2`
   at 17MB) can run on CPU and significantly improve precision. At 604 chunks,
   reranking the top 20 takes ~100ms on 2 cores.

5. **Replace the `seen_ids` dedup with a proper scoring model.**
   The current `_add_result` dedup is a binary filter (first file wins).
   Replace with: per-file relevance = max(chunk_similarity) × boost(metadata_match).
   Then sort by relevance score.

---

## 6. Concrete Recommendation (For This Scale)

Given the current constraints (57 files, 604 chunks, 2-core VM, no GPU), I recommend:

### Short-term (today):
**Replace full-file-read with chunk-merging.** No I/O, better relevance, trivial change:

```python
# Instead of reading the full file:
# Collect top 5 matching chunks for each source_path, merge, truncate
for sp in seen_paths:
    sp_chunks = [(sr['similarity'], sr) for sr in semantic_results if sr['source_path'] == sp]
    sp_chunks.sort(key=lambda x: x[0], reverse=True)
    merged = "\n\n".join(c[1]['text'] for c in sp_chunks[:5])
    _add_result({..., "text": merged[:2000], ...})
```

This eliminates file I/O entirely, uses the semantic ranking the TF-IDF search
already computed, and is a 5-line change.

### Medium-term (this sprint):
1. Cache `_load_chunks()` in memory (avoid SQLite on every query)
2. Add chunk_index to schema for position-aware merging
3. Implement the block-merging algorithm described in Section 5

### Long-term (if data grows 10×):
1. Add BM25 normalization
2. Add lightweight cross-encoder reranker
3. Two-tier retrieval with pre-built summaries

---

## 7. The Bottom Line

The full-file-read fix is **correct but not optimal**. It solves the immediate
bug (empty headings) by brute force — dumping entire documents into context.
This works at 20 Wiki entries but is architecturally lazy.

The right fix at this scale is **chunk-aware merging**: use the TF-IDF scores
to identify not just *which file* but *which content* within the file is relevant,
then assemble a context window that maximizes semantic density.

The fact that the TF-IDF search already computed per-chunk relevance scores and
we throw them away to re-read files from disk is a design smell. The information
we need is already in memory. Use it.

---

*"The best part is no part. The best process is no process."*
— The best I/O is no I/O. The chunks are already loaded. Stop reading files.

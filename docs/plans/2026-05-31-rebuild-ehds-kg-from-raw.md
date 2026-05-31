# Rebuild EHDS KG From Official Raw OJ HTML Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Rebuild the authoritative EHDS Index layer from the local raw Official Journal HTML at `data/raw/32025R0327_oj_en.html` and eliminate stale synthetic article numbering.

**Architecture:** Layer 1 (`ehds_index/`) becomes generated authoritative legal text from the local raw source. Existing Layer 2 (`ehds_wiki/`) and Layer 3 (`ehds_kb/`) are preserved initially, then audited for stale citations. A rebuild command parses the raw HTML, writes one Markdown file per Article with provenance metadata and paragraph anchors, and invalidates/rebuilds TF-IDF caches.

**Tech Stack:** Python stdlib + existing project utilities, pytest-compatible script tests, existing TF-IDF engine.

---

## Acceptance Criteria

1. `data/raw/32025R0327_oj_en.html` is the default source path for rebuilds.
2. The parser extracts 105 official articles from CELEX `32025R0327`.
3. Generated Index files contain official titles and text, not synthetic placeholders.
4. Official secondary-use mappings hold:
   - Art.33 = Obligations of distributors
   - Art.50 = Applicability to health data holders
   - Art.51 = Minimum categories of electronic health data for secondary use
   - Art.53 = Purposes for which electronic health data can be processed for secondary use
   - Art.60 = Duties of health data holders
   - Art.61 = Duties of health data users
   - Art.68 = Data permit
   - Art.73 = Secure processing environment
5. Stable IDs and filenames are consistently zero-padded: `EHDS-2025-327-A050`, `EHDS-2025-327_Art-050.md`.
6. Rebuild does not modify `ehds_wiki/` or `ehds_kb/` in the first pass.
7. Cache rebuild succeeds after Index regeneration.

## Task 1: Add RED official article parser/rebuild test

**Objective:** Prove current KG is stale and the expected source path/mappings are not satisfied.

**Files:**
- Create: `scripts/test_official_raw_rebuild.py`
- Read: `data/raw/32025R0327_oj_en.html`
- Read: `ehds_index/*.md`

**Step 1:** Write tests that assert raw file exists, parser extracts official mappings, and index files match official mappings.

**Step 2:** Run:

```bash
python3 scripts/test_official_raw_rebuild.py
```

Expected before implementation: FAIL because parser/rebuild tooling is missing and/or current Index maps Art.33/50/53 incorrectly.

## Task 2: Implement raw HTML article parser

**Objective:** Extract article number, title, and full text from the local OJ HTML.

**Files:**
- Create: `src/ehds_raw_import.py`

**Implementation notes:**
- Use stdlib HTMLParser or regex over EUR-Lex/OJ HTML structure.
- Support fallback extraction from paragraph text if tags are noisy.
- Return structured article records: `{article, article_id, title, text, paragraphs, source_path, celex}`.
- Validate exactly 105 articles.

**Verification:** Parser test passes for article count and title mappings.

## Task 3: Implement Index writer and rebuild command

**Objective:** Generate canonical Markdown files into `ehds_index/`.

**Files:**
- Modify/Create: `src/ehds_raw_import.py`
- Possibly modify: `src/batch_import.py` only if CLI reuse is cleaner.

**Implementation notes:**
- Backup stale generated files only if needed; do not delete wiki/kb.
- Write frontmatter with `stable_id`, `regulation`, `article`, `title`, `chapter`, `category`, `source_path`, `celex`, `date_enacted`.
- Body format: `# Art. N — Title`, `## Para N`, anchor `[[A###-P#]]`.
- Include `## Audit Anchors` generated from paragraphs.

**Verification:** `python3 src/ehds_raw_import.py --rebuild-index` writes 105 files.

## Task 4: Update E2E validation to official mappings

**Objective:** Prevent reintroducing stale synthetic article numbers.

**Files:**
- Modify: `scripts/test_e2e.py`

**Implementation notes:**
- Replace weak `len(index) >= 7` checks with official Article count and mapping checks.
- Ensure citation resolver handles zero-padded and non-padded stable IDs or document intentional behavior.

**Verification:** `python3 scripts/test_e2e.py` passes.

## Task 5: Rebuild TF-IDF cache and verify retrieval

**Objective:** Ensure search layer reflects the rebuilt Index.

**Commands:**

```bash
rm -f cache/ehds_tfidf.pkl cache/ehds_embeddings.db
python3 src/ehds_embedding.py --build
python3 src/ehds_embedding.py --search "secure processing environment data permit" --top-k 5
```

**Verification:** Results include Art.68/Art.73 or their Wiki overlays.

## Task 6: Review git diff and commit

**Objective:** Leave a clean feature branch ready for review.

**Commands:**

```bash
git status --short
git diff --stat
git diff -- scripts/test_official_raw_rebuild.py src/ehds_raw_import.py scripts/test_e2e.py
python3 scripts/test_official_raw_rebuild.py
python3 scripts/test_e2e.py
git add data/raw/32025R0327_oj_en.html docs/plans/2026-05-31-rebuild-ehds-kg-from-raw.md scripts/test_official_raw_rebuild.py src/ehds_raw_import.py scripts/test_e2e.py ehds_index cache
git commit -m "feat: rebuild EHDS index from official raw source"
```


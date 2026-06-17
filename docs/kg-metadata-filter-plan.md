# KG Context — Metadata Filter 方案

## 问题

D8.2 的 BM25 chunk 被 metadata（disclaimer, authors, document history, keywords, document info）占满。
LLM context 中 D8.2 chunk 是 metadata 而非 ethical governance 正文（章节 5-6）。

## 解法

### Step 1: 在 `_extract_chunks()` 中过滤 metadata 段落

文件: `src/ehds_embedding.py`，data layer 分支。

Metadata 段落特征识别：

```python
_METADATA_HEADINGS = {
    "document info", "disclaimer", "authors", "document history",
    "keywords", "version", "document info", "0 document info",
    "0.1 authors", "0.2 keywords", "0.3 document history",
}
```

在 data layer 的段落循环中：

```python
for i in range(0, len(paragraphs), 5):
    chunk_text = "\n\n".join(paragraphs[i:i+5])
    if not chunk_text:
        continue
    # Skip metadata chunk: if first line of first paragraph matches
    first_line = paragraphs[i].split("\n")[0].strip().lower()
    if any(mkw in first_line for mkw in _METADATA_HEADINGS):
        continue  # skip this chunk (metadata only)
    chunks.append({...})
```

### Step 2: 重建 BM25 索引

```bash
cd ~/projects/ehds_kg && uv run python3 src/ehds_embedding.py --build
```

### Step 3: 测试

在 `tests/test_retrieval.py` 中加：

```python
def test_d82_ethical_governance_found():
    engine = get_engine()
    results = engine.semantic_search("ethical governance recommendations", top_k=10)
    data_texts = [r["text"] for r in results if "d8.2" in r["source_path"].lower()]
    assert len(data_texts) > 0
    # At least one D8.2 chunk should contain ethical governance content (not just metadata)
    assert any("ethical" in t.lower() or "governance" in t.lower() for t in data_texts), \
        "D8.2 chunk should contain ethical governance content, not just metadata"
```

### 风险

1. `first_line` 匹配 `authors` — 如果正文段落首行出现 "The authors recommend..." 会被误杀？不会——正文首行 "the authors" 小写，"The authors" 大写首字母，且 `_METADATA_HEADINGS` 中的 "authors" 指的是 section heading 格式。但为了安全，检查段落前加 heading pattern 判断（如 `^## |^[A-Z][a-z]+ ` 等）。
2. `document info` 只在文档开头出现一次，不会误杀正文。
3. `0.1 authors` / `0.2 keywords` 这些编号前缀只在 TEHDAS2 文档中出现，不会误杀。

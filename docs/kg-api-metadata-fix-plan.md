# API Server ↔ Embedding Engine Metadata 断链修复方案

**日期**: 2026-06-17
**作者**: Allen
**状态**: 待实施

---

## 1. 问题根因

`ehds_api_server.py` 的 `/api/retrieve` depth>=1 路径（第 214-244 行）存在数据流断裂：

```
semantic_search() 返回 → API 丢弃 text + metadata → 重新读文件全文 → 截断 [:2000]
```

`ehds_embedding.py` 的 `semantic_search()` 返回的每条 result 已经包含：
- `text`: chunk 文本（engine 已切好的 section-level chunk）
- `metadata.document_id`: 文档 ID
- `metadata.section_id`: section 编号（如 "3.1.2"）
- `metadata.section`: section 标题
- `layer`, `source_path`, `similarity`

但 API server 在拿到 `sr` 后做了三件错误的事：
1. 从 `sr["source_path"]` 重新 `read_text()` 读全文件
2. 调用 `_parse_frontmatter` 拿 `body`（忽略 engine 已切好的 chunk）
3. 用 `meta.get("title", sp)` 替代 `section`，丢了真正的 section 标题

结果：每次 API 返回的是**全文前 2000 字符**，不是跟查询真正相关的 chunk 文本。metadata（document_id, section_id, section）也丢失或错位。

## 2. 受影响代码

**文件**: `src/ehds_api_server.py`
**行号**: 214-244 (depth>=1 块)

当前代码（问题段）：

```python
# --- depth>=1: BM25 semantic search ---
if depth >= 1:
    try:
        engine = _get_embedding_engine()
        semantic = engine.semantic_search(query, top_k=max_results)
        kg_path = PROJECT_ROOT
        for sr in semantic:
            sp = sr.get("source_path", "")
            if sp in seen_paths:
                continue
            seen_paths.add(sp)
            # Read full file body for rich context    ← 重新读文件
            try:
                full_path = kg_path / sp
                full_text = full_path.read_text(encoding="utf-8", errors="replace")
                _, body = _parse_frontmatter(full_text)
            except Exception:
                body = sr.get("text", "")
            meta = sr.get("metadata", {})
            document_id = meta.get("document_id") or f"EHDS-{sr.get('layer', 'kg').title()}"
            section_label = meta.get("section") or meta.get("title") or sp   ← 回退链不对
            results.append({
                "layer": sr.get("layer", ""),
                "document": document_id,
                "section": section_label,
                "section_id": meta.get("section_id", ""),
                "similarity": sr.get("similarity"),
                "text": body.strip()[:2000],          ← 全文截断
                "source_path": sp,
                "article": meta.get("article", ""),
            })
    except Exception as e:
        print(f"[KG] BM25 search unavailable: {e}")
```

## 3. 修复方案

**直接用 engine 返回的 chunk text 和 metadata**，删除重新读文件的逻辑。

修复后代码：

```python
# --- depth>=1: BM25 semantic search ---
if depth >= 1:
    try:
        engine = _get_embedding_engine()
        semantic = engine.semantic_search(query, top_k=max_results)
        for sr in semantic:
            sp = sr.get("source_path", "")
            if sp in seen_paths:
                continue
            seen_paths.add(sp)
            meta = sr.get("metadata", {})
            document_id = meta.get("document_id") or f"EHDS-{sr.get('layer', 'kg').title()}"
            section_label = sr.get("section") or meta.get("section") or meta.get("title") or ""
            results.append({
                "layer": sr.get("layer", ""),
                "document": document_id,
                "section": section_label,
                "section_id": sr.get("section_id") or meta.get("section_id", ""),
                "similarity": sr.get("similarity"),
                "text": sr.get("text", "")[:2000],  # engine 的 chunk 文本
                "source_path": sp,
                "article": meta.get("article", ""),
            })
    except Exception as e:
        print(f"[KG] BM25 search unavailable: {e}")
```

## 4. 变更清单

| 变更项 | 说明 |
|--------|------|
| 删除 `kg_path = PROJECT_ROOT` | 不再需要文件系统路径 |
| 删除 `full_path.read_text()` + `_parse_frontmatter()` | 不再重新读文件 |
| 删除 `except Exception: body = sr.get("text")` 回退 | 直接用 engine text |
| `section_label` | 改为 `sr.get("section")` 优先，引擎 metadata.section 才是真正的 section 标题；回退链去掉 `sp`（filepath 不宜做 label） |
| `text` | 从 `body.strip()[:2000]` 改为 `sr.get("text", "")[:2000]` |
| `section_id` | 增加 `sr.get("section_id")` 优先（注意：engine 返回的 result 顶层**不**直接带 section_id，在 metadata 里；但需要确认是否要在 engine 返回中也展平。当前 metadata 里有 `section_id`，留着 `meta.get("section_id", "")` 即可） |

### 关于 engine 返回的 `section` 字段

分析 `semantic_search()` 的返回结构（第 337-343 行）：

```python
candidates.append({
    "similarity": ...,
    "source_path": chunk["source_path"],
    "layer": chunk["layer"],
    "text": chunk["text"][:2000] + "..." if len(chunk["text"]) > 2000 else chunk["text"],
    "metadata": chunk.get("metadata", {}),
})
```

**注意**: engine 返回的 result **顶层没有** `section` / `section_id` / `document_id` 字段——这些都在 `result["metadata"]` 里。所以修复代码中 `sr.get("section")` 实际不会命中，应该简化为只用 `meta`：

```python
section_label = meta.get("section") or meta.get("title") or ""
```

## 5. 影响评估

- **API 响应体变化**: `text` 字段从"全文前 2000 字符"变为"与查询最相关的 chunk 文本"。这是**预期的正确行为**。
- **向后兼容**: `layer`, `document`, `section`, `section_id`, `similarity`, `source_path` 字段名不变，仅值更准确。
- **性能提升**: 省去每次查询重新读取文件 + frontmatter 解析的 I/O。
- **去重逻辑**: `seen_paths` 仍然有效（同一个 source_path 的不同 chunk 只取第一条）。
- **风险**: 如果 engine 的 chunk text 被截断到 2000 字符（第 341 行），API 再截一次 `[:2000]` 无影响；如果 chunk text < 2000，API 返回的就是完整 chunk。

## 6. 修复后验证

```bash
cd ~/projects/ehds_kg
curl -s "http://localhost:8000/api/retrieve?q=data+quality&depth=1" | python3 -m json.tool | head -80
```

预期：`text` 字段应包含与 "data quality" 相关的 chunk 内容，而非某个文件的开头 2000 字符。

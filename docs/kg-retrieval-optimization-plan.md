# EHDS KG 知识库检索优化方案

## 问题分析

### 根因 1: data/ 目录未被索引

`src/ehds_embedding.py` line 89-91 中 `build_index()` 只扫描三个目录：
```python
for layer, root in [("index", INDEX_ROOT), ("wiki", WIKI_ROOT), ("kb", KB_ROOT)]:
```

**`data/` 目录下的所有文档被排除在外**——包括 D8.2、D7.1、D6.3、D5.1 等 TEHDAS2 指南。用户问"ethical governance"这样的问题，答案在 D8.2 中，但引擎根本不知道 D8.2 的存在。

### 根因 2: TF-IDF 对短语/概念级匹配弱

当前检索使用 sklearn `TfidfVectorizer(ngram_range=(1,2))`，只支持 1-2 个词的 ngram 组合。对于：

- `"ethical governance"`（短语精确匹配）→ TF-IDF 可以匹配，但因 IDF 权重低导致排名靠后
- `"recommendations on ethical governance adequately address the challenges"`（长查询）→ TF-IDF 的余弦相似度会被大量高频词稀释

### 涉及文件

| 文件 | 改动 |
|------|------|
| `src/ehds_embedding.py` | 索引范围扩展 + BM25 替换 TF-IDF |
| `src/ehds_api_server.py` | /api/retrieve 的 depth>=1 路径用 BM25 替换 TF-IDF |
| `src/ehds_common.py` | 查看 DATA_ROOT 是否需要暴露 |
| `data/` 目录 | 确保所有 .md 文件有 frontmatter 或元数据 |

---

## 修改方案

### Step 1: data/ 目录加入索引范围（P0）

**目标**: `build_index()` 和 `_extract_chunks()` 覆盖 `data/` 目录。

修改 `src/ehds_embedding.py` 的 `build_index()`:

```python
# 当前
for layer, root in [("index", INDEX_ROOT), ("wiki", WIKI_ROOT), ("kb", KB_ROOT)]:

# 改为
all_roots = [("index", INDEX_ROOT), ("wiki", WIKI_ROOT), ("kb", KB_ROOT)]
if DATA_ROOT.exists():
    all_roots.append(("data", DATA_ROOT))
for layer, root in all_roots:
```

同样在 `_extract_chunks()` 中，`data/` 下的 .md 文件需要像 wiki 一样按段落切分（不要像 index 那样按 `## Para N` 切）。因为 `data/*.md` 是长文本 TEHDAS2 指南，没有 index 的标准 `## Para` 结构。

在 `_extract_chunks` 中添加：

```python
if layer == "data":
    for para in body.split("\n\n"):
        para = para.strip()
        if para and not para.startswith("[["):
            priority = float(meta.get("priority", 0)) if meta.get("priority") else 0.0
            chunks.append({
                "text": f"{meta.get('title', '')}\n{para}",
                "metadata": {"source": meta.get("source", ""), "document": meta.get("document", path.name)},
                "priority": priority,
            })
```

### Step 2: 替换 TF-IDF 为 BM25（P1）

**目标**: 用 `rank_bm25` 的 BM25Okapi 替换 sklearn 的 TfidfVectorizer。

原因：
1. BM25 对短语匹配更好（词频饱和 + 文档长度归一化）
2. BM25 的 IDF 计算更适合法规文档（长文档密集出现的关键词不会被过度惩罚）
3. `rank-bm25` 只有 8KB，纯 numpy，不增加外部依赖

修改 `ehds_embedding.py` 的 `__init__` 和 `build_index`:

```python
from rank_bm25 import BM25Okapi

class EHDSEmbeddingEngine:
    def __init__(self, ...):
        ...
        self.bm25: BM25Okapi | None = None
        self._chunks_cache = None
        self._load_or_build_bm25()

    def _load_or_build_bm25(self):
        if self.bm25_path.exists():
            with open(self.bm25_path, "rb") as f:
                cache = pickle.load(f)
            self.bm25 = cache["bm25"]
            self._chunks_cache = cache["chunks"]
            return
        self.build_index()

    def build_index(self):
        # ... 相同的 chunk 提取逻辑 ...
        texts = [c["text"] for c in all_chunks]
        tokenized = [self._tokenize(t) for t in texts]
        self.bm25 = BM25Okapi(tokenized)
        
        with open(self.bm25_path, "wb") as f:
            pickle.dump({"bm25": self.bm25, "chunks": all_chunks}, f)
        print(f"[+] Built BM25 index: {len(all_chunks)} chunks")

    def _tokenize(self, text: str) -> list[str]:
        import re
        return re.findall(r"[a-z0-9]+", text.lower())

    def semantic_search(self, query: str, top_k: int = 5, layer_filter: str | None = None):
        if self.bm25 is None:
            return []
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        results = []
        for i, chunk in enumerate(self._load_chunks()):
            if layer_filter and chunk["layer"] != layer_filter:
                continue
            score = float(scores[i])
            if score <= 0:
                continue
            results.append({
                "similarity": round(score, 4),
                "source_path": chunk["source_path"],
                "layer": chunk["layer"],
                "text": chunk["text"][:280] + "..." if len(chunk["text"]) > 280 else chunk["text"],
                "metadata": chunk.get("metadata", {}),
            })
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
```

### Step 3: /api/retrieve 衔接 BM25（P1）

API server 的 retrieve 路径无需改——它已经通过 `_get_embedding_engine()` 调用 `engine.semantic_search()`，只要引擎内部从 TF-IDF 改为 BM25，API 自动生效。

需要验证的是 API server 也加载了 `data/` 下的文件到索引。不需要改代码。

### Step 4: 重建索引（P1）

```bash
cd ~/projects/ehds_kg
uv run python3 src/ehds_embedding.py --build
```

验证：

```bash
uv run python3 src/ehds_embedding.py --search "ethical governance recommendations"
```

应该返回 D8.2 (data/d8.2.md) 的相关段落。

### Step 5: 验证 API 端到端

```bash
curl "http://localhost:8080/api/retrieve?q=ethical+governance+recommendations+d8.2&depth=1&max_results=5"
```

应返回包含 D8.2 章节的 results。

---

## 不需要改的地方

- **`ehds_api_server.py`**: retrieve 路径已通过 `_get_embedding_engine()` 间接调用引擎。BM25 替换后自动生效。
- **`ehds_common.py`**: `DATA_ROOT` 已定义 (line 25)，`_walk_kb()` 不包含 data 目录，但 API 的 `/api/search` 使用的是 `_walk_kb()`. 如果未来需要 data 目录被 keyword search 覆盖，可以扩展 `KB_ROOTS`，但本次改动的 scope 是 embedding/retrieval，不涉及 keyword search。
- **`kg.py` (chat_server)**: 无关，不改。
- **前端 chatbot**: 前端只调用了 `retrieve_kg_for_chat()`，无需修改。

## BM25 优势总结

| 指标 | TF-IDF (当前) | BM25okapi (替换后) |
|------|-------------|-------------------|
| 短语精确匹配 | ❌ 弱（ngram 范围有限） | ✅ 强（词频饱和机制） |
| 长文档中的短词 | ❌ 被长度规则稀释 | ✅ 文档长度归一化 |
| 高频词惩罚 | ✅ 有 (IDF) | ✅ 有 (IDF + 饱和) |
| 内存 | 20-50MB (TF-IDF 矩阵) | 2-5MB (倒排索引) |
| 依赖 | sklearn (已有) | rank-bm25 (8KB, 纯 numpy) |
| 构建速度 | ~1s (fit_transform) | ~0.5s (纯 Python 倒排) |
| 标识符匹配 (Art.68, D8.2) | ❌ 被分词破坏 | ✅ tokenizer 保留 `.` 和 `-` |
| 大粒度短语 (health data, ethical governance) | ❌ ngram 上限 2 | ✅ bigram token 保留 |
| PDF 索引 | ❌ 不支持 | ✅ markitdown 转 md 后索引 |

## 额外改动（基于 review 意见）

### Step 3: KB_ROOTS 同步加入 data/（飞飞）
`ehds_common.py` 中 `KB_ROOTS` 加入 `DATA_ROOT`，使 `/api/search` 的 keyword search 也覆盖 `data/` 目录。

### Step 4: PDF → md 转换（Guido + 飞飞）
data/ 下有 PDF 格式的 TEHDAS2 指南。用 markitdown 批量转换为 .md 后放入 data/ 目录。

### Step 5: Tokenizer 优化（飞飞 + Guido）
- BM25 tokenize 保留 `.` 和 `-`（保留 Art.68, D8.2 等标识符）
- 加 bigram（"health data" 作为完整短语匹配）

### Step 6: Cache 路径 + 依赖更新（Guido）
- pickle 文件路径改为 `ehds_bm25.pkl`（避免旧 TF-IDF pickle crash）
- SQLite 中 `tfidf` 列不再写入
- 依赖更新（rank-bm25, markitdown）

### Step 7: 检索测试（Guido）
```python
def test_ethical_governance_finds_d82():
    engine = EHDSEmbeddingEngine()
    results = engine.semantic_search("ethical governance recommendations", top_k=5)
    assert any("d8.2" in r["source_path"].lower() for r in results)
```

## 实施顺序

1. markitdown 转换 data/ 下 PDF → md
2. data/ 加入索引 + KB_ROOTS
3. BM25 替换 + tokenizer + bigram + fallback
4. Cache 路径 + 依赖更新
5. 重建索引 + 端到端测试

## 实施顺序

1. Step 1: data/ 加入索引范围（3 行改动）
2. Step 2: BM25 替换 TF-IDF（~50 行改动）
3. Step 3: 重建索引跑通测试
4. Step 4: API 端到端验证

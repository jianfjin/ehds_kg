# Diversity Rerank 修复方案

## 问题

`src/ehds_embedding.py::semantic_search()` 的 diversity rerank 逻辑导致低相关文档被强行补位进入 top-k，稀释真正相关文档（如 D8.2 Annex 5）的信号。

当前行为：

1. 取 `candidate_pool = candidates[:max(top_k * 3, 20)]`。
2. 按 `document_id` 聚类，每个文档取 top-2 chunk。
3. 如果聚类后不足 `top_k`，从剩余候选中按分数补位；即使分数远低于最高分，也会通过 "gap threshold" 后再无条件补足。

结果：D6.2 / GUID / DRAF 等文档的 chunks 因多样性规则被塞入 top-10，即使它们与查询的相似度显著低于 D8.2 Annex 5 的相关 chunks。

## 修复目标

- 保持 BM25 检索链路不变。
- 不改 API server。
- 只修改 `src/ehds_embedding.py` 中 `semantic_search()` 的 diversity rerank 部分。
- 让多样性选择只在**高相关候选池**内进行，不再硬塞低分文档凑数。

## 方案 A：在 diversity rerank 中加入 score gap threshold（推荐）

### 改动点

1. 在模块级新增常量：

```python
# Diversity rerank: only consider candidates within this relative score gap
# of the best BM25 score. 0.5 means candidates must be within 50% of the top.
DIVERSITY_GAP_THRESHOLD = 0.5
```

2. 在 `semantic_search()` 中，计算 `best_score` 后先过滤 eligible pool：

```python
best_score = candidate_pool[0]["similarity"]
gap_floor = best_score * (1.0 - DIVERSITY_GAP_THRESHOLD)
eligible = [r for r in candidate_pool if r["similarity"] >= gap_floor]
```

3. 多样性聚类只针对 `eligible` 进行：

```python
by_doc = defaultdict(list)
for r in eligible:
    doc_id = self._extract_doc_id_from_result(r)
    by_doc[doc_id].append(r)

diverse = []
for items in by_doc.values():
    diverse.extend(items[:2])
```

4. **不再补位**：如果 diversity 选择后不足 `top_k`，直接返回当前数量，不再从低分候选中填充。

```python
diverse.sort(key=lambda x: x["similarity"], reverse=True)
results = diverse[:top_k]
```

5. 保持最终按 `document_id` + `section_id` 的排序逻辑不变。

### 预期效果

- D8.2 Annex 5 的高分 chunks 优先进入结果。
- 只有分数落在 top score 50% 范围内的文档才参与多样性竞争。
- 如果某查询的相关文档集中，返回结果可能少于 10 条，但每条都更相关。

## 方案 B：将默认 top_k 从 10 降到 5

### 改动点

1. 修改 `semantic_search()` 默认参数：

```python
def semantic_search(
    self, query: str, top_k: int = 5, layer_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
```

2. 与方案 A 同时使用效果更佳；若单独使用，候选池 `max(top_k * 3, 20) = 20` 不变， diversity 选择范围不变，但返回结果更少，自然减少低分文档进入最终 context 的概率。

### 风险

- API 现有调用者若依赖默认 10 条，可能收到更少结果。但本约束范围内未修改 API server，调用者显式传入 `top_k=10` 仍可得到旧行为数量。

## 建议组合

**实施方案 A + 方案 B**：既用 score gap 过滤低相关文档，又将默认 top_k 降到 5，从质量和数量两方面避免 context 稀释。

## 测试验证

1. 使用查询 "D8.2 Annex 5 data quality" 调用 `semantic_search()`，检查返回结果中是否不再出现 D6.2 / GUID / DRAF 等低分文档。
2. 打印 `best_score`、`gap_floor`、`eligible` 数量，确认过滤逻辑生效。
3. 对比修改前后 top-10 / top-5 的 source_path 分布。
4. 运行现有 CLI：`python src/ehds_embedding.py --search "D8.2 Annex 5" --top-k 10`。

## 不改动的范围

- `BM25_PATH`、`_tokenize`、`get_scores` 等检索链路保持原样。
- API server 代码不修改。
- `build_index`、chunking、embedding 生成逻辑不修改。

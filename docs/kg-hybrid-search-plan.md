# EHDS KG 检索优化方案：Hybrid Search（Heading-Aware BM25 + Diversity Rerank）

> 目标：在保留现有 BM25 技术栈的前提下，把 top-5 context 中仅出现 D8.1 / D8.2 的困境，提升到能稳定召回 D4.1 / D7.4 / D8.1 / D8.2 等多文档交叉引用，使 LLM 回答达到“基于参考材料、跨文档、带具体章节号”的质量标准。

---

## 1. 现状与问题

当前检索链路（简化）：

```text
User Query
    │
    ▼
BM25 on paragraph-merged corpus ──► top-5 chunks ──► LLM prompt
```

观察到的缺陷：

| 缺陷 | 影响 |
|------|------|
| top_k = 5 | 候选集太窄，跨文档证据难以同时命中 |
| context 上限 3000 tokens | 命中后仍被截断，细节（章节号、页码、风险描述）丢失 |
| chunk 边界对 heading 不敏感 | 同一章节下的表格/段落被切散，导致“Table 2 in D8.2”这类引用在 context 中不完整 |
| 无多样性控制 | BM25 容易把同一文档的多个相似段落塞进 top-k，挤占其他文档的证据 |
| 元信息不足 | 召回结果里缺少 `document_id`、`section_id` 等显式字段，LLM 难以生成“D4.1 Section 3.2”式精确引用 |

---

## 2. 设计原则

1. **不引入 PageIndex**：继续在 chunk 层做检索，避免重建整页索引带来的存储与延迟开销。
2. **保留 BM25**：它是当前系统的核心，稳定、可解释、对稀疏关键词友好。
3. **标题感知 chunk**：以 `##` / 数字章节号等 heading 为边界分割文档，保证一个 chunk 内语义完整。
4. **多样性重排**：BM25 召回后按 `document_id` 聚类，每文档取 top-2，再按分数差 threshold 补位；避免单文档垄断。
5. **不引入 cross-encoder**：VM 资源有限（1.9 GB RAM，无 GPU），避免额外模型加载与推理延迟。
6. **调大窗口**：top_k 5 → 10，context 上限 3000 → 5000 tokens，为跨文档引用留足空间。
7. **先 baseline 后迭代**：任何参数改动必须能对比优化前后的量化指标。

> *Simple is better than complex.* 本方案只增加轻量 heading 解析与 diversity rerank，不对现有 BM25 架构做侵入式改造。

---

## 3. 目标质量样例

优化后，LLM 应能产出类似以下风格的回答：

```text
Based on the provided reference materials, there are several significant
challenges related to collaboration and coordination under the EHDS that are
not fully reflected in the summarized sections (like Table 2 in D8.2).

For example:
- D4.1 Section 3.2 notes that ...
- D8.1 Section 4.1 highlights ...
- D7.4 Chapter 5 discusses ...
```

---

## 4. 技术方案

### 4.1 标题感知 Chunk（Heading-Aware Chunking）

#### 4.1.1 切分策略

- 优先按 Markdown heading 2（`\n## `）切分。
- 若文档未使用 Markdown heading（如 PDF 转换后的纯文本），回退到数字章节号模式：`^\d+(\.\d+)*\s+[A-Z]`。
- 每个 chunk 必须携带：
  - `document_id`：如 `D4.1`、`D8.2`
  - `section_id`：可生成的标准章节号，如 `3.2`
  - `section`：heading 原文，如 `"3.2 Governance Model"`

> 砍掉未使用的 `chunk_type`、`parent_heading`、`page` 字段——字段少即是多，避免元信息噪音。

#### 4.1.2 防止过度切分

- 单 chunk 最小长度：不小于 256 字符，避免标题碎片。
- 单 chunk 最大长度：不超过 2000 字符，保证 LLM context 内可容纳 10 条。
- 表格特殊处理：同一表格原则上不跨 chunk；超长表格按行切分时，重复表头并标注 `(continued)`。
- 标题碎片（长度 < 256 字符的 chunk）合并到下一个有效 chunk 或跳过。

### 4.2 BM25 + 多样性重排

#### 4.2.1 BM25 支路

- 对 query 做轻量预处理：小写、保留文档号/章节号原样、生成相邻 bigram。
- 在标题感知 chunk 集合上执行标准 BM25。
- 返回 `bm25_top_k = 20` 个候选，为多样性重排留足原料。

#### 4.2.2 多样性重排（Diversity Rerank）

```python
# Group by document_id, take top-2 per doc, then fill remaining by score gap threshold
from collections import defaultdict

by_doc = defaultdict(list)
for r in results:
    doc_id = _extract_doc_id(r["source_path"])
    by_doc[doc_id].append(r)

# Take top-2 from each doc
diverse = []
for doc_id, items in by_doc.items():
    diverse.extend(items[:2])

# If not enough, fill from remaining results; apply score-gap tie-breaker so that
# a low-score filler from a new doc does not displace a high-score same-doc result.
if len(diverse) < top_k:
    used_ids = {id(r) for r in diverse}
    remaining = [r for r in results if id(r) not in used_ids]
    diverse.extend(remaining[: top_k - len(diverse)])

results = diverse[:top_k]
```

- 最终返回 `top_k = 10`。
- 用分数差 threshold 作为 tie-breaker：当补位候选与已选最低分差距过大（如 > 0.5×best）时停止补位，宁缺毋滥。
- 去掉硬性的 `max_doc_ratio = 0.6`：多样性由“每文档最多 2 条”自然体现，不再用全局比例截断。

### 4.3 Context 组装

- 输出排序：先按 `document_id` 分组，组内按 `section_id` 排序（`3.2` → `(3, 2)`，避免字符串排序把 `3.10` 排在 `3.2` 前面）。
- 每条 chunk 按固定模板格式化：

```text
[Source: {document_id}, Section {section_id} {section}]
{chunk_text}
```

- 总长度上限 5000 tokens；若超过，优先截断 BM25 路中得分最低的 chunk。

### 4.4 查询增强（可选、低成本）

- 当 query 中出现 `challenges`、`coordination`、`collaboration` 等宽泛词时，自动扩展同义词列表（如 `cooperation`, `stakeholder engagement`, `governance`），用于 BM25 查询扩展。
- 扩展表硬编码在配置中，不调用 LLM，避免延迟与成本。

---

## 5. 参数配置

| 参数 | 当前值 | 目标值 | 说明 |
|------|--------|--------|------|
| `top_k` | 5 | 10 | 候选集翻倍，支撑跨文档引用 |
| `context_max_tokens` | 3000 | 5000 | 为 10 条 chunk 及元信息留足空间 |
| `bm25_top_k` | 5 | 20 | BM25 召回候选数，供 diversity rerank 使用 |
| `max_doc_per_cluster` | 无 | 2 | 多样性重排：每文档最多取 2 条 |
| `diversity_fill_gap` | 无 | 0.5 | 补位分数差 threshold（相对最高分） |
| `chunk_min_chars` | 无 | 256 | 避免标题碎片 |
| `chunk_max_chars` | 无 | 2000 | 保证单 chunk 内信息完整 |

---

## 6. 实施步骤

### Step 0：数据层改造（0.5–1 天）

- 在 `src/ehds_embedding.py::_extract_chunks()` 的 `data` 分支实现 heading-aware 切分。
- 输出新字段：`document_id`、`section_id`、`section`。
- 砍掉 `chunk_type`、`parent_heading` 等未使用字段。
- 去掉 metadata filter；heading-aware chunk 把 metadata 段落隔离为独立短 chunk，BM25 低分自然下沉。
- 重新 chunk 全部 PDF，生成新的 chunk 索引文件。

### Step 1：索引层改造（0.5 天）

- 运行 `uv run python3 src/ehds_embedding.py --build` 重建 BM25 索引。
- 索引中保留 `document_id`、`section_id` 等元信息，便于 diversity rerank 与 context 排序。

### Step 2：检索层改造（1 天）

- `semantic_search()` 默认 `top_k=10`，BM25 内部候选池扩至 20。
- 实现 diversity rerank：按 `document_id` 聚类，每文档取 top-2，分数差 threshold 补位。
- 最终输出按 `(document_id, section_id_tuple)` 排序。
- `ehds_api_server.py` `/api/retrieve` 默认 `max_results=10`。
- `chat_server/config.py`：`KG_RESULT_TEXT_MAX_CHARS` 3000 → 5000。

### Step 3：配置与测试（1 天）

- 更新 `tests/test_retrieval.py`：
  - 验证 heading-aware chunk 携带 `document_id` / `section_id`。
  - 验证 diversity rerank 后 top-10 来自 ≥2 个文档。
  - 验证 context 排序按 `document_id` 分组、`section_id` 升序。
- 针对 5–10 个典型问题（如 “collaboration challenges in EHDS”）人工检查召回结果：
  - 是否同时出现 D4.1 / D7.4 / D8.1 / D8.2？
  - 是否包含具体章节号与表格引用？
  - top-10 中单一文档是否过度集中？

### Step 4：Baseline 采集与回归（0.5–1 天）

- 在优化前固定一组查询，记录：
  - top-10 中不同 `document_id` 数量
  - 平均 chunk 长度
  - 命中查询中章节号 / 表格引用的比例
  - 端到端延迟
- 优化后用同一组查询复测，形成对比表。
- 添加 `scripts/retrieval_baseline.py` 自动化 baseline 采集（支持 `--before` / `--after` 标签输出 JSON）。

### Step 5：部署

- 确认 VM 内存无压力（1.9 GB RAM，无 cross-encoder，仅增加轻量正则与合并逻辑）。
- 部署并更新 RAG（knowledge.edmf.nl）后端配置。

---

## 7. 评估指标

| 指标 | 评估方式 | 目标 |
|------|----------|------|
| 召回文档多样性 | top-10 中不同 document_id 数量 | ≥ 3 |
| 章节引用精度 | LLM 回答中章节号与 source 一致率 | ≥ 80% |
| 表格引用完整度 | 涉及 Table/Figure 的问题，context 是否包含对应表格 | ≥ 80% |
| Context 利用率 | 实际使用 tokens / 5000 | 60%–90% |
| 端到端延迟 | query → context 组装完成时间 | < 2s（无 cross-encoder） |

---

## 8. 风险与回退

| 风险 | 缓解 |
|------|------|
| heading 切分导致 chunk 数量暴增 | 设置 min/max 长度，标题碎片合并 |
| 不同 PDF 的 heading 格式不一致 | 支持 `## ` 与数字章节号双模式切分 |
| context 5000 tokens 超出模型窗口 | 保留截断策略；若模型窗口更小，可降至 4000 |
| 参数调优耗时 | 先以文中推荐值为基线，再用 baseline 数据小步迭代 |

回退策略：若 diversity rerank 效果不及预期，可关闭 rerank，仅保留 heading-aware chunk + BM25 + top_k 10 + context 5000，仍可显著改善现状。

---

## 9. 总结

本方案通过 **标题感知 chunk** 保证上下文完整性，通过 **BM25 召回 + 多样性重排** 提升跨文档覆盖，通过 **top_k 10 / context 5000** 为交叉引用提供空间，同时 **不引入 PageIndex、cross-encoder 与 exact match 独立支路**，保持 VM 友好与代码简洁。实施周期约 3–4 天，目标是让 LLM 回答从“只谈 D8.1/D8.2”进化到“交叉引用 D4.1/D7.4/D8.1/D8.2 并指出具体章节与表格”。

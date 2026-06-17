# KG Hybrid/Agentic RAG — 提升推理水平方案

> "好的产品是用完即走的。好的 context 是 LLM 看完就能回答的。"
> — Allen

---

## 0. 问题诊断

### 0.1 检索没问题，推理有问题

当前链路：

```
User Query
  → BM25 (top_k=20 candidate pool)
    → Diversity Rerank (top-2 per doc, score-gap fill)
      → top-10 chunks with [D8.2 · 3.2] citation headers
        → _format_context_for_chat() concatenates chunks
          → Injected as system prompt: "Answer using the provided context."
            → DeepSeek
```

实测：对于 "Do the recommendations on ethical governance adequately address the challenges identified?"，BM25+diversity rerank **能正确召回** D8.2 Annex 5（包含 "ethical governance" 引用 D4.2 的表格行），但 LLM 回答依然是 "no information available"。

**这不是检索失败。这是推理失败。**

### 0.2 根因分析

LLM 拿到的是 **10 个扁平 chunk 片段**，格式如下：

```
[EHDS-DATA] D8.2 · 5
D8.2 Guideline...
Annex 5 – Overview of deliverables in TEHDAS2
| Deliverable | Topic | Lead |
| D4.2 | Ethical governance | ... |
...

[EHDS-DATA] D4.1 · 3.2
D4.1 Guideline on fees and penalties...
3.2 Governance Model
...
```

问题有三个层面：

| 层面 | 问题 | 后果 |
|------|------|------|
| **结构** | Chunks 是平的，没有"这个 chunk 引用那个 chunk"的关系标注 | LLM 看到的是一堆独立片段，不是文档网络 |
| **指令** | System prompt 只说 "Answer using the provided context" | LLM 缺少跨 chunk 推理的明确指令 |
| **规模** | 10 chunks × 500-2000 chars/chunk ≈ 8000 chars 挤在一个 system message 里 | LLM 注意力分散，关键引用关系被稀释 |

### 0.3 为什么 ima.qq.com 能做到

ima 知识库的做法：
1. 更强的 LLM（更大的 reasoning 能力）
2. 更好的 prompt 工程（显式要求 cross-reference）
3. 可能做了 chunk 级别的 rerank/summarization

我们不换模型。我们改进 LLM 接收 context 的方式和推理指令。

---

## 1. 方案总览

四个层级，按复杂度递增。**先做 L1，80% 的收益来自这里。**

```
L1: Prompt Engineering         ← 零成本，立即部署
L2: Context Restructuring      ← 预处理 chunk，构建关系图
L3: Two-Pass Summarization     ← 一次额外 LLM 调用
L4: Agentic Tool-Use           ← 多次 LLM 调用，完全自治
```

约束检查：
- [x] 2GB VM，无 GPU — 所有 LLM 调用走 DeepSeek API
- [x] 不引入 PageIndex 或 cross-encoder — 不改检索链路
- [x] 不改 BM25 — diversity rerank 保持原样
- [x] top_k=10, context=5000-8000 chars — 在现有窗口内操作

---

## 2. L1: Prompt Engineering（零成本，立即）

### 2.1 当前 system prompt（chat.py L101-105）

```python
"You are the EDM Master Assistant. Answer using the provided context. "
"For EHDS-KG, cite articles.\n\n"
f"CONTEXT:\n[EHDS KNOWLEDGE GRAPH]\n{kg_context}"
```

问题：
- "Answer using the provided context" — 这是给搜索引擎用的指令，不是给推理引擎用的
- 没有告诉 LLM 如何利用多个 chunk 做综合判断
- 没有给出评估性问题的回答框架

### 2.2 新 system prompt

```python
SYSTEM_PROMPT = """You are an EHDS regulatory analyst. You are given reference fragments
from EHDS deliverables (D4.1, D8.2, etc.) and the EHDS Regulation.

When answering, follow this reasoning framework:

1. IDENTIFY: Which deliverables are represented in the context? List them.
2. CROSS-REFERENCE: Which documents cite or reference others? (e.g., "D8.2 Annex 5
   lists D4.2 as covering ethical governance")
3. GAP-ANALYZE: For evaluative questions — does the context contain BOTH the problem
   description AND the solution/recommendation? If only one side is present,
   state what is found and what is missing.
4. SYNTHESIZE: Answer the question using all available fragments. If information is
   spread across multiple chunks, integrate them. If the context is insufficient
   for a definitive answer, explain WHY — don't just say "no information."

CRITICAL RULES:
- NEVER say "no information is available" without first examining ALL chunks.
- If D8.2 references D4.2 (e.g., in a table), explicitly note this cross-reference.
- Cite using [D8.2 · Section X] format for every claim.
- For evaluative questions: give a judgment based on the evidence present,
  not a refusal to answer.

CONTEXT:
[EHDS KNOWLEDGE GRAPH]
{kg_context}"""
```

### 2.3 为什么这样改

| 变更 | 原因 |
|------|------|
| 角色从 "Assistant" 变为 "regulatory analyst" | 设定专业预期，激活领域知识 |
| 四步推理框架 (IDENTIFY → CROSS-REFERENCE → GAP-ANALYZE → SYNTHESIZE) | 给 LLM 一个结构化的工作流，引导它逐层处理 |
| "NEVER say no information" 规则 | 直接对抗当前的 "I cannot answer" 默认行为 |
| 显式要求 cross-reference | 让 LLM 主动寻找跨 chunk 关系 |
| 评估性问题的特殊处理 | 区分"信息检索"和"分析判断"两类问题 |

### 2.4 实施

改动文件：`~/projects/edm_home/back-end/chat_server/routes/chat.py`
改动量：~30 行，替换 system prompt 字符串

---

## 3. L2: Context Restructuring（结构化 context）

### 3.1 问题

当前 context 是 10 个 chunk 的平铺拼接。一个 D8.2 Annex 5 里的表格引用 D4.2——这个引用关系藏在表格文本里，LLM 可能注意不到。

### 3.2 方案：Context 重组为三段式

```
=== DOCUMENT MAP ===
D8.2 → references D4.1, D4.2, D4.3, D7.4 (see Annex 5)
D4.1 → Fees and penalties for non-compliance
D4.2 → Ethical governance (referenced by D8.2)
...

=== RETRIEVED CHUNKS ===
[D8.2 · 5] ...（完整文本）
[D4.1 · 3.2] ...
[D4.2 · 2.1] ...

=== CROSS-REFERENCE INDEX ===
D8.2 ──references──▶ D4.2 (ethical governance)
D8.2 ──references──▶ D4.1 (fees/penalties)
...
```

### 3.3 实现方式

在 `_format_context_for_chat()` 中增加预处理步骤：

1. **提取 document map**: 扫描所有 chunk，从 metadata 中收集 `document_id` 列表
2. **检测交叉引用**: 用 regex 匹配 chunk 文本中的 `D\d+\.\d+` 引用模式
3. **构建三段 context**: 先放 map，再放 chunks，最后放引用索引

不增加 LLM 调用，纯文本处理。成本为零。

### 3.4 实施

改动文件：`~/projects/edm_home/back-end/chat_server/kg.py` 的 `_format_context_for_chat()`
改动量：~60 行

---

## 4. L3: Two-Pass Summarization（一次额外 LLM 调用）

### 4.1 思路

在把 context 送进 system prompt 之前，先用一次 LLM 调用把 10 个 chunk 压缩成结构化摘要。

```
Pass 1 (summarize):
  Input: 10 raw chunks
  Output: Structured synthesis — "Here's what the documents say..."

Pass 2 (answer):
  Input: Structured synthesis + user question
  Output: Final answer
```

### 4.2 实现

```python
async def _summarize_context(chunks: list[str]) -> str:
    """Use DeepSeek to synthesize chunks into a coherent briefing."""
    prompt = """Synthesize the following EHDS document fragments into a structured briefing.

For each document, extract:
- Document ID and topic
- Key findings or recommendations
- Cross-references to other documents
- Any gaps or limitations noted

FRAGMENTS:
""" + "\n\n---\n\n".join(chunks)

    # Single DeepSeek call, no tool loop
    return await _call_deepseek(client, [
        {"role": "system", "content": "You are an EHDS document analyst. Be concise and structured."},
        {"role": "user", "content": prompt},
    ])
```

### 4.3 成本

- 一次额外 API 调用（~1-2s 延迟）
- Context 从 8000 chars 压缩到 ~2000 chars 的结构化摘要
- Answer LLM 拿到的是清晰的摘要而非碎片
- 适合复杂评估性问题，简单事实类问题可跳过

### 4.4 触发条件（可选优化）

不是所有问题都需要 two-pass。简单问题（"What is D8.2 about?"）直接用 chunk context 即可。复杂问题（含 "evaluate", "assess", "adequately", "challenges", "gaps" 等关键词）触发 two-pass。

```python
COMPLEX_QUESTION_SIGNALS = [
    "evaluate", "assess", "adequate", "sufficient",
    "challenge", "gap", "compare", "contrast",
    "to what extent", "how well", "recommend",
]
```

### 4.5 实施

改动文件：
- `chat_server/routes/chat.py` — 增加 two-pass 逻辑
- `chat_server/kg.py` — 增加 `_summarize_context()` 辅助函数
改动量：~100 行

---

## 5. L4: Agentic Tool-Use（多次 LLM 调用，完全自治）

### 5.1 思路

给 LLM 一个工具：`search_kg(query: str) → chunks`。LLM 拿到初始 context 后，可以主动调用工具获取更多信息。

```
User: "Do the recommendations on ethical governance adequately address the challenges?"

LLM round 1:
  → reads initial context (D8.2 chunks)
  → "I see D8.2 references D4.2 for ethical governance.
     Let me search for D4.2 details."
  → tool_call: search_kg("D4.2 ethical governance challenges")

LLM round 2:
  → receives D4.2 chunks
  → "D4.2 identifies challenges X, Y, Z. But D8.2 only addresses X and Y."
  → final answer with gap analysis
```

### 5.2 实现方案

用 DeepSeek 的 tool-calling API（`deepseek-chat` 支持 function calling）：

```python
TOOLS = [{
    "type": "function",
    "function": {
        "name": "search_ehds_kg",
        "description": "Search the EHDS Knowledge Graph for specific document sections. "
                       "Use this when you need more detail on a referenced deliverable.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query, e.g. 'D4.2 ethical governance' or 'challenges in TEHDAS2'"
                }
            },
            "required": ["query"]
        }
    }
}]
```

Agent loop（最多 3 轮）：

```python
async def agentic_rag(user_query: str, initial_context: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\n" + initial_context},
        {"role": "user", "content": user_query},
    ]

    for round in range(3):  # Max 3 rounds
        response = await _call_deepseek_with_tools(client, messages, TOOLS)

        if has_tool_calls(response):
            for tc in response.tool_calls:
                if tc.function.name == "search_ehds_kg":
                    query = json.loads(tc.function.arguments)["query"]
                    new_chunks = await retrieve_kg_raw(query, depth=1, max_results=5)
                    new_context = _format_context_for_chat(new_chunks)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": new_context,
                    })
            continue  # Another round

        return response.content  # Final answer
```

### 5.3 成本与风险

| 指标 | L1 | L2 | L3 | L4 |
|------|----|----|----|-----|
| LLM 调用次数 | 1 | 1 | 2 | 2-4 |
| 延迟增加 | 0 | ~0.01s | ~1-2s | ~3-8s |
| 实现复杂度 | 低 | 低 | 中 | 高 |
| 失败模式 | 无 | 无 | Summary 质量差 | Tool loop 无限循环 |
| 调试难度 | 低 | 低 | 中 | 高 |

### 5.4 L4 的前提条件

- DeepSeek function calling API 稳定可用
- Tool loop 有严格的 max rounds 和 timeout
- Fallback：如果 tool calling 不可用，降级到 L3

### 5.5 实施

改动文件：
- `chat_server/routes/chat.py` — agent loop
- `chat_server/kg.py` — `search_ehds_kg` tool implementation
改动量：~200 行

---

## 6. 推荐实施路径

```
Phase 1 (今天): L1 Prompt Engineering
  → 预期: 80% 的评估性问题得到正确回答
  → 评估: 用 5 个测试问题验证

Phase 2 (本周): L2 Context Restructuring
  → 预期: 跨文档引用被 LLM 明确识别
  → 评估: 检查 LLM 回答是否显式引用 D4.2 等

Phase 3 (下周): L3 Two-Pass Summarization（仅在 L1+L2 不满足时）
  → 预期: 复杂多文档推理问题得到解决
  → 评估: 对比 L1+L2 vs L1+L2+L3 的答案质量

Phase 4 (按需): L4 Agentic（仅在需要主动 drill-down 的场景）
  → 触发条件: 用户明确要求深入某个文档的具体章节
```

---

## 7. 评估测试集

对 "Do the recommendations on ethical governance adequately address the challenges identified?" 这个问题：

### 7.1 期望回答标准

LLM 应该做到：
1. [x] 识别 D8.2 引用了 D4.2（D8.2 Annex 5 表格里明确列出 D4.2 负责 "Ethical governance"）
2. [x] 识别 "ethical governance" 是 D4.2 的主题
3. [x] 从 context 中提取 D4.1（fees/penalties）、D4.3 等协同工作组的描述
4. [x] **综合给出评估性判断**——例如：
   - "D8.2 确实提到了 ethical governance（引用 D4.2），但 D8.2 自身的推荐主要聚焦于 notification obligations，而非伦理治理本身的挑战。要全面评估，需要检查 D4.2 正文内容。"
   - 或更具体的基于 context 的判断

### 7.2 反模式（当前行为，需消除）

- [ ] "I cannot answer this question because the provided context does not contain specific information about..."
- [ ] "No information is available..."
- [ ] 只回答 D8.2 的内容，忽略对 D4.2 的引用

---

## 8. 改动文件清单

| Phase | 文件 | 改动 |
|-------|------|------|
| L1 | `edm_home/back-end/chat_server/routes/chat.py` | 替换 system prompt |
| L2 | `edm_home/back-end/chat_server/kg.py` | `_format_context_for_chat()` 增加 document map + cross-reference index |
| L3 | `edm_home/back-end/chat_server/kg.py` | 新增 `_summarize_context()` |
| L3 | `edm_home/back-end/chat_server/routes/chat.py` | 增加 two-pass 逻辑 + 触发条件 |
| L4 | `edm_home/back-end/chat_server/routes/chat.py` | Agent loop + tool definitions |
| L4 | `edm_home/back-end/chat_server/kg.py` | `search_ehds_kg` tool |

不改的文件：
- `ehds_kg/src/ehds_embedding.py` — BM25 检索保持不变
- `ehds_kg/src/ehds_api_server.py` — API server 保持不变
- `edm_home/back-end/rag/retrieval/ehds_kg.py` — HTTP client 保持不变

---

## 9. 回退策略

所有改动都是增量的——在现有 system prompt 基础上叠加。如果 L1 的新 prompt 效果不如预期，回退到旧 prompt 只需 revert 一个字符串。

L3 的 two-pass 在 L1+L2 效果不好时启用，不影响基础路径。L4 的 agent loop 有明确的 max rounds=3 硬限制，不会无限循环。

---

— Allen

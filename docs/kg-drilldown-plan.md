# KG Context — Full-Text Drill-Down 方案

## 问题

当前 LLM context 只包含 chunk 文本（≤2000 chars/chunk）。当 chunk 截断了关键内容（如 D8.2 Annex 5 表格的后半部分），LLM 无法获取完整信息。

答案在原文中，但 chunk 只展示了片段。

## 方案

### Step 1: Context 中附加 citation 信息

每个 chunk 的 header 改为:

```
[EHDS-DATA] D8.2 — Annex 5 – An overview of deliverables in TEHDAS2
Source: data/d8.2.md, section 57
```

这样 LLM 知道具体在哪个文档的哪个章节。

### Step 2: 在 chat_server 中加全文检索回路

当 LLM 返回的回答中出现了 "I would need the full text of..." 或类似信号，或者当用户的 follow-up query 包含文档名称（如 "D4.2"），自动触发全文 drill-down：

1. 检测用户消息中包含 `D4.2`、`section 57` 等文档引用
2. 从 `data/` 目录直接 grep 提取包含该文档名的段落（不是 BM25）
3. 把全文段落作为 {{context}} 注入下一轮对话

### Step 3: 在 context 结尾加 3 轮 roundtrip 控制

```python
KG_RETRIEVAL_SIGNAL = """
If you need more detailed content from a specific document or section, 
include "NEED_FULL_TEXT: <document_id> [section]" in your response.
I will retrieve the full section for you.
"""
```

### 改动文件

- `src/ehds_api_server.py` — section 字段包含文档名+章节
- `chat_server/routes/chat.py` — 检测 NEED_FULL_TEXT 信号，触发全文提取
- 不需要改 embedding engine

### 复杂度

3 个文件，~50 行改动。

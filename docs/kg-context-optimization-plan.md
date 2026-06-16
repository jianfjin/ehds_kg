# KG Context 输出优化方案 v2

基于 张小龙 review + 线上 config 确认。

## 线上确认值

| 参数 | 计划猜测值 | 线上实际值 |
|------|-----------|-----------|
| `KG_RESULT_TEXT_MAX_CHARS` (kg.py) | 600 | **3000** (瓶颈不在此) |
| API server depth=0 text 截断 | 800 | 800 (真瓶颈) |
| API server depth=1 text 截断 | 800 | 800 (真瓶颈) |
| embedding `semantic_search` text 截断 | 280 | 280 (CLI 输出，非瓶颈) |

## 修改方案

### 改动 1: API server 两处截断 800 → 2000

`ehds_api_server.py` 中 depth=0 (line 210) 和 depth=1 (line 238) 各有一处 `[:800]` 截断，改为 `[:2000]`。

### 改动 2: embedding engine 截断 280 → 1000

`ehds_embedding.py` 的 `semantic_search()` 中 `text[:280]` 改为 `text[:1000]`。影响 CLI `--search` 输出，不影响主链路但是顺手改。

### 改动 3: data layer chunk 合并为 5 段落

`ehds_embedding.py` 的 `_extract_chunks()` 中，data layer 从单段落切分改为 5 段落合并。同时下调 BM25 `b` 参数到 0.4 以补偿长文档惩罚。给 data layer 统一加 0.15 priority boost。

### 改动 4: 重建 BM25 索引

```bash
cd ~/projects/ehds_kg && uv run python3 src/ehds_embedding.py --build
```

## 不修改

- `KG_RESULT_TEXT_MAX_CHARS` (kg.py): 已是 3000，足够
- `chat_server/` 其他文件: 无关
- 前端 ChatBot: 无关

## 不修改的理由

- `b=0.4` 降低 BM25 长度归一化强度，避免 data layer 长 chunk 系统性低分
- `priority=0.15` 在所有 data layer chunk 上叠加，进一步确保 data 内容不被 wiki/index 的短 chunk 压制
- 不需要在额外地方加截断——kg.py 的 3000 已经是最终防线

## 验证

```bash
# 1. 语义搜索
cd ~/projects/ehds_kg && uv run src/ehds_embedding.py --search "ethical governance recommendations"
# 预期: text 长度 > 500 chars, 至少 2 个 data layer chunk

# 2. API server 端到端
curl "http://localhost:8080/api/retrieve?q=ethical+governance+recommendations&depth=1&max_results=5"
# 预期: text 字段 > 1000 chars

# 3. Chat server context
cd ~/projects/edm_home/back-end && uv run python3 -c "
from chat_server.kg import retrieve_kg_for_chat; import asyncio
ctx, sources = asyncio.run(retrieve_kg_for_chat('ethical governance recommendations'))
print('Context chars:', len(ctx))
print('Contains ethical:', 'ethical' in ctx.lower())
"
# 预期: Context chars > 6000, Contains ethical = True
```

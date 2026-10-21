# Batch 29 · T08-03 第三轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色 / 范围 | 同一独立审阅者；只核对 C05 剩余的两个固定源码链接与取证 L21 同步，不编写或修订正文 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| turn_context 核验方法 | 读取本地当前会话 JSONL 最新 `turn_context` 的 `model`、`effort`、`cwd`，并比对 `collaboration_mode.settings` |
| 核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；settings 中模型/档位一致，未调用其他模型或子代理 |
| 核验记录 | `/Users/ywang2397/.codex/sessions/2026/10/21/rollout-2026-10-21T19-22-05-01a15e32-6cde-73e0-aaeb-c0b856434851.jsonl`；最新 `turn_context.timestamp=2026-10-21T11:54:30.222Z` |
| 会话 ID | `01a15e32-6cde-73e0-aaeb-c0b856434851`；与初审及前两轮复核相同 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 正文 | `knowledge/08-reliability/mitigation-and-recovery-principles.md`，145 行 |
| 正文 SHA-256 | `c3dea4fb4974e92d7d0df32a6063dad425583d4c57fb5abe5cf5d4b155bd09b6`；独立计算，与请求一致 |
| 第二轮复核依据 | `docs/research/batch-29-t08-03-codex-recheck-2.md`；SHA-256 `382dc730ea486cace0f3247cbdf74568437651d1abd221510ceb5d33e2b3ed37` |
| 同步取证记录 | `docs/research/batch-29-t08-03-sources.md`；SHA-256 `c69d7f388ba66c35dc6aaa3343a214f6be776a2d5913864d9b9c09326ad96ce1` |
| 写入范围 | 仅新增 `docs/research/batch-29-t08-03-codex-recheck-3.md`；不修改其他文件，不运行任何 make 目标 |
| 本轮结果 | **C05 CLOSED；新增发现 0 项** |
| 总体结论 | **通过本轮定向复核；累计 11 项 CLOSED、0 项 OPEN** |

以下正文行号均以上述 SHA-256 为基准。复核依据为[第二轮报告](batch-29-t08-03-codex-recheck-2.md)列出的剩余条件；本轮只读取[正文 L85 所在文件](../../knowledge/08-reliability/mitigation-and-recovery-principles.md)与[取证 L21 所在文件](batch-29-t08-03-sources.md)的对应主张、链接及来源登记的 commit 身份，不重审 C10、N01 或此前已关闭八项。

## C05 复核表

| 发现 | 状态 | 核对结果与理由 | 剩余关闭条件 |
|---|---|---|---|
| C05 · 原 P2 | **CLOSED** | 正文 L85 已在文档概括与实现分支的主张附近加入 `run.py#L157-L165`、`api.py#L887-L917` 两个固定 commit 链接，URL 与第二轮要求逐字一致，commit 与 `src.pytorch.elastic-2.6` 登记一致。取证 L21 同时补齐两链接、文档示例合并概括成员变化与失败的说明，以及 UNHEALTHY/FAILED 剩余预算大于零时扣减、HEALTHY 等待新节点不扣的实现分支，并保留按实现表述与未核离开/故障组合 unknown。两项剩余条件均已满足 | 无 |

证据定位：

- [固定 run.py L157–165](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/run.py#L157-L165)：示例标题合并概括成员变化与失败，并配置 `--max-restarts=3`。正文与取证将其作为文档概括，未改作所有成员变化均扣预算的实现结论。
- [固定 api.py L887–917](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/elastic/agent/server/api.py#L887-L917)：UNHEALTHY/FAILED 分支在剩余预算大于零时扣减后重启；HEALTHY 且有等待节点的分支重建 worker 组，不扣该预算。正文与取证的有限分支表述一致。

本轮 GitHub 页面抽取返回缓存未命中，随后直接读取同一 commit 的 [run.py 原始文件](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/run.py)与 [api.py 原始文件](https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/elastic/agent/server/api.py)，均返回 HTTP 200，按原文件行号核对上述区间。原始文件分别为 922 行、957 行，两个锚点区间均存在且支持对应转述；没有据此扩大到未核组合。

## 新增发现

无。本轮补充的链接与取证说明没有引入新的结论或超出已核实现分支的适用范围。正文及取证仍明确保留未逐路径核对的离开/故障组合 unknown，不影响本项关闭。

## 总体结论

**C05 CLOSED，通过第三轮定向复核。** 沿用前轮已关闭的 C01–C04、C06–C10 与 N01，累计 C01–C10 加 N01 共 11 项全部 CLOSED，OPEN 0 项；这些已关闭项本轮未重新审阅，无新增 N 编号发现。

本结论仅表示 T08-03 已记录的审阅发现全部关闭，不代表 Batch 29 全批验收或真实环境验证。未执行任何 make 目标、现场操作或硬件实验，未修改正文、取证、来源登记、历史报告或其他文件。

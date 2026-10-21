# Batch 31 · T00-04 定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 初审的同一独立审阅者；C01–C02 修订后的第一轮定向复核；不承担正文编写或修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 核验方法 | 首先以 `CODEX_SESSION_ID` / `CODEX_THREAD_ID` 定位本会话 rollout JSONL，读取最新 `turn_context` 的 model、effort、cwd 与 collaboration_mode.settings，并与 `session_meta.id` 核对 |
| 最新 turn_context | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；`collaboration_mode.mode=default`；`settings={model: gpt-6.1-sol, reasoning_effort: xhigh, developer_instructions: null}` |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T01-13-11-01a15f73-dd74-7880-b830-bb528c222620.jsonl` L220；时间戳 `2026-10-21T17:21:40.313Z`；`session_meta` 在 L1 |
| 会话 ID / turn ID | `01a15f73-dd74-7880-b830-bb528c222620` / `01a15f7b-903b-7861-8038-1e05f8c3cc0f` |
| 身份结论 | 模型与档位符合本轮要求；本地 Codex CLI 会话直接审阅，未另启子代理或其他模型。引用内容中的 `[frontier_llm]` 不作为回退依据，以本轮 turn_context 为准 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai |
| 写入范围 | 仅新增 `docs/research/batch-31-t00-04-codex-recheck.md`；其他文件不修改 |

**复核结论：C01 CLOSED，C02 CLOSED；开放项 0，新增余项 0（无 R01 等新编号）。T00-04 在初审及本轮定向复核的有限编辑验收范围内通过。** 该结论不代表硬件验证、平台组合支持或恢复演练成功。

## 范围与基准

只对照[初审报告](batch-31-t00-04-codex-review.md) C01、C02 的关闭条件，读取修订后的[推理文](../../knowledge/00-overview/inference-lifecycle.md)及其关联段落、[取证记录](batch-31-t00-04-sources.md) L28–31，并定向回读容量、发布恢复、路由、引擎交集与 MindIE 执行正文的承载位置。初审对训练侧及其他未改段落的结论沿用；不扩大为整批或兄弟篇重审。

| 本轮读取基准 | 行数 | SHA-256 |
|---|---:|---|
| `knowledge/00-overview/inference-lifecycle.md` | 153 | `5f694892073ee46ac24f9861dbbf73d55756d48ab32868d96b91a49d2a22c658` |
| `knowledge/00-overview/training-lifecycle.md` | 151 | `07681ebe62e5eb1d055bc271f2615a24975d3575b16cbd9fc7b03e8a82f4a1ea` |
| `docs/research/batch-31-t00-04-sources.md` | 31 | `17cae5b25c599131710b6f77bfcafca277e0d4edb1e986cd0c322eb5cbbda41d` |

初审报告本轮读取 SHA-256 为 `6988e06f78be480bdb6ff3a89babd5ff329d1c8aa7ed872618b65aba88a36950`。正文行号均按上表版本。本轮不重新打开上游网页或源码；外部固定证据的独立读取记录见初审，本次核对修订是否准确收回初审指出的边界，并与现存承载正文一致。

## 逐项关闭判断

### C01 · P2 · CLOSED

**关闭条件**：明确新请求与在途流的不同去向；不暗示自动迁移/续传，不以端点摘除代替排空完成；失败、取消与未知终态仍按承载正文对账，并与推理文 L86/L90 一致。

**修订证据**：推理文 L84 现分别说明新请求“经实际路由收敛转向其他可服务副本”，在途流“按 drain 契约完成/取消”；超期或终态不明按重试边界处理，并明确不承诺已输出流透明续传或 KV 自动迁移。该行没有把终态不明直接判作成功，也没有要求自动重试。

**承载与关联复核**：

- [容量与扩缩容](../../knowledge/07-inference/capacity-and-autoscaling.md) L67 区分路由/端点摘除、在途流排空和进程退出；本地 KV/prefix cache 不自动保留。
- [发布与恢复](../../knowledge/07-inference/release-and-recovery.md) L57 保留实际路由收敛、已接纳流完成/取消计数、超期终态不确定和自动排空 unknown；L76–77 限制透明续传与本地 KV 继承；L87–90 保留逻辑请求×attempt 对账及恢复闭环。
- [路由与流控](../../knowledge/07-inference/routing-and-flow-control.md) L96–98 区分幂等证据、送达未见响应、响应已提交和取消后的资源释放。推理文 L86 的重试入口、L90 的请求恢复判据及 L105 的终态/分母表述均未改变，与修订一致。

**判断**：满足全部关闭条件。这里的“按 drain 契约”指需由目标部署落实并验证的处理规则，没有升级为引擎自动排空、无损迁移或已完成演练的保证。

### C02 · P3 · CLOSED

**关闭条件**：每个版本标签对应实际承载档案；b17039bc 不覆盖 Ascend 独立证据；3.1.0 不被写成产品、源码和站点全集已核同版。

**修订证据**：推理文 L94 明确三线分立：上游 vLLM 执行/计时细节限 b17039bc；vLLM Ascend 限 52d4acf，保留其构建变量指向 v0.14.1 的差异并指回文末说明；MindIE 为开源仓 69e5a5dd 快照内文档自述的 3.1.0，产品包/latest 支持表映射仍 unknown，并新增就近的 MindIE 执行档案链接。

**承载与关联复核**：[引擎交集](../../knowledge/07-inference/engine-backend-boundaries.md) L24、L46、L74 保留独立快照、开源/产品包区分和 latest 支持表未核同版；[MindIE 执行档案](../../knowledge/07-inference/mindie-execution-profile.md) L38–41 明确 3.1.0 为文档线自述，保留同快照数值差异及产品/源码映射 unknown。推理文 L147 原有的 Ascend 0.14.1 差异和“不拼成 NPU 部署组合”说明未改；L95 仍要求未列交集组合保持 unknown。

**判断**：满足全部关闭条件。版本标签已对应其证据身份，没有以该修订消除配套冲突或建立新的产品支持承诺。

## 回归检查与新增余项

为避免仅凭编写者列出的修改范围作判断，在内存中将当前推理文 L84、L94 还原为初审时留存的两行，再计算 SHA-256，所得 `8ca211d0aec866ede7047664d3ce6f74627cd6eacea32cdb55f48c2fb1b79938` 与初审正文基准完全一致。该过程未写回文件，证明与初审版本相比仅这两行发生变化，其余字节均保持。

| 检查项 | 结果 |
|---|---|
| 原有阶段、观察点和计时 | 导航图、问题入口表、请求阶段表、三类状态、计时序列图、时钟/分母、失败过滤与末尾适用边界均保持初审版本；两处修订未引入冲突 |
| 元数据与来源 | frontmatter 全部字节未变；Draft 2020-12 schema 与日期格式检查通过；source_refs、evidence_refs、related_ids、draft/source_checked、generic 及 updated_at 均保留；外链 URL 序列未变 |
| 本地链接 | 推理文 24 处本地相对链接目标均存在；比初审新增 1 处 MindIE 执行档案链接，实际承载 C02 所需限定 |
| 训练侧 | 151 行及 SHA-256 与初审完全相同，未发生正文变化 |
| 取证回填 | 来源记录 L30–31 对 C01/C02 的修订描述与实文一致，unknown 清单和未运行实验说明保留；其回填不代替本报告的独立关闭判断 |
| 新余项 R01… | 本轮两项关闭条件及相关回归检查范围内未发现新增余项，不另建编号 |

## 写入核对与最终结论

本轮仅做只读文本、摘要、schema 与链接检查；未执行正文命令或硬件/服务实验。未运行 `make check`、`make build`、`make test`，未重建 `build/`；本轮只新增审阅报告。

写入前对 Git tracked＋非忽略 untracked 文件（排除本复核报告）记录清单：688 个文件，按路径及文件 SHA-256 汇总的清单 SHA-256 为 `0defed51e9a2ef092b4ed5261093eedf611c7644cb6f4841fe4a15b41b40a1da`。交付时重新计算得到同一数量与摘要，两文仍保持上表行数及 SHA-256，确认报告之外文件未变；本报告相对链接与空白检查通过。再次读取最新 turn_context，仍为 L220 的同一模型、档位、cwd 与嵌套 settings。

**C01、C02 均 CLOSED，无 OPEN 项，无新增 R 项；T00-04 在原初审及本轮定向复核范围内通过。** 初审记录保留原结论与历史摘要，本报告记录修订后的关闭状态。该通过仅是有限终态导航与边界的编辑验收，不改变 `draft / source_checked`，不代表 NVIDIA / Ascend / AMD 任一环境已安装、兼容、实测或恢复成功。

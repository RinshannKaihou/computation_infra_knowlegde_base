# Batch 31 · T02-12 第三轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色 / 范围 | 原独立审阅者；第三轮定向复核，仅核对 R08–R12 及其直接修订；不编写或修订正文 |
| 实际模型 / 档位 | `gpt-6.1-sol / xhigh`；符合本轮要求，计为正式复核 |
| 核验方法 | 开始时读取包含本轮请求的当前 rollout 最新 `turn_context`，核对顶层与 `collaboration_mode.settings`；不沿用前轮档位 |
| 核验结果 | 顶层 `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；`collaboration_mode.mode=default`、`settings.model=gpt-6.1-sol`、`settings.reasoning_effort=xhigh`、`settings.developer_instructions=null` |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T00-32-09-01a15f4e-4bcb-7a12-be50-b0ed78c23a91.jsonl` L381，ordinal 380，时间戳 `2026-10-21T17:00:09.768Z` |
| 会话 ID / turn ID | `01a15f4e-4bcb-7a12-be50-b0ed78c23a91` / `01a15f67-d9e7-7800-8932-13ffe084439c` |
| 身份边界 | 当前本地 Codex CLI 会话直接复核；未另启模型或子代理，未发现模型回退 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai；上述时间为 UTC |
| 正文基准 | `knowledge/02-software-stack/environment-installation-and-upgrade.md`；221 行（开始时 `wc -l`） |
| 正文 SHA-256 | `ae21a335b14bc9423e58041d770a3740c38eda760db9587ca9ef345d13c68a16`（开始时 `shasum -a 256`） |
| 上轮正文基准 | 219 行，SHA-256 `c1ce65a42dc0d0df1710766fda2abb4364ec342fd846a5dd9818e0f9bc3d852a`；历史报告不改写 |
| 写入范围 | 仅新增 `docs/research/batch-31-t02-12-codex-recheck-3.md` |

**结论：暂不通过。R09、R10、R11 CLOSED；R08、R12 OPEN。剩余部分续记为 R13（P2）和 R14（P3），P1 0 项。** 主要修正已落实，仍需纠正驱动证据范围的过度否定，并补齐固定版本 bandwidthTest 的登记核读范围。

## 范围与方法

逐项对照[第二轮报告](batch-31-t02-12-codex-recheck-2.md)的 R08–R12 关闭条件，核对[正文](../../knowledge/02-software-stack/environment-installation-and-upgrade.md)、[取证记录](batch-31-t02-12-sources.md)及对应 registry 条目；未重新全量审阅正文、三平台资料或其他任务。

对 R08 定点重新读取 ROCm 的 Verify your installation，并补开 NVIDIA 驱动指南的 Post-installation Actions；对 R10 重读 ROCm 的仓库/缓存清理部分；对 R12 经 GitHub 连接器确认 v12.8 bandwidthTest README 可读。没有运行其中任何设备查询、安装、卸载或样例命令。CANN 原句及既有字段只与前轮已读取材料和登记范围比对，本轮未增加远程 CANN 核验结论。

## R08–R12 逐项判定

正文行号均指本轮 221 行版本。

| 上轮事项 | 判定 | 核对结果 |
|---|---|---|
| R08 · L2 身份及缺证状态 | **OPEN** | NVIDIA L120 已区分包/节点/加载状态，明确 unknown 时 L2 未完成；Ascend L135 补已加载证据与两包分别登记；AMD L149 记录安装身份及官方 rocminfo 的加载确认。允许同一原始记录支持多个层，不能为机械分层编造命令。但 NVIDIA 新增“本文档线未提供独立查询命令”与当前指南直接冲突；AMD 的固件信息字段/缺证状态也未落实。余项 R13 |
| R09 · 旧版方法引用限制 | **CLOSED** | L111 明列 CANN 8.2.RC1.alpha001、HIP 6.3.42134/docs-6.3.3 与本篇文档线差异，并要求目标接口/样例/适用条件另核，未核即对应环节未完成；L109 的契约冻结门槛保留 |
| R10 · ROCm notes 的 unknown 范围 | **CLOSED** | registry L2673 末句已将 unknown 收窄为完整版本回退与依赖恢复，并补仓库/缓存清理定位；与正文 L202、取证 L12/L41 的当前结论一致。既有历史误记未被改写成本库实测 |
| R11 · 两类 NVIDIA 仓库 | **CLOSED** | 取证 L10 已分 local 的 repo 包/复制 keyring 与 network 的 cuda-keyring；与正文 L120 和 registry L7249 一致，不再以修订记录代替主张表更新 |
| R12 · 固定样例与历史记录 | **OPEN** | 正文 L105/L123 已使用 v12.8 bandwidthTest，实际步骤不再含 master URL；取证 L9 已标旧 ID 废止并给稳定替代，L24 区分当前 tag 与历史 master。仍未在对应来源登记中记录 v12.8 bandwidthTest 的核读范围：master 条目仍为原 master 观察，v12.8 条目仍只记录 vectorAdd。余项 R14；不重新要求已完成的 ID 废止标记或链接替换 |

## R13–R14：剩余关闭条件

### R13 · P2 · R08 剩余：未取得证据被写成文档线没有方法，固件缺项未落状态

- **位置**：正文 L120、L149；通用要求 L84。
- **直接证据**：NVIDIA [Post-installation Actions · Verify the Driver Version](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/post-installation-actions.html#verify-the-driver-version)明确说明核验正确版本已加载，并给出 `cat /proc/driver/nvidia/version`（本轮页面转换坐标 L48–52）。因此“本文档线未提供独立的驱动加载状态查询命令”不能成立。原 registry 只记录 Ubuntu/version-locking 两节的核读范围，未读到另一节不等于整条文档线没有该方法。本轮看到的是 latest 当前页，不据此倒推作者先前读取时的页面状态。
- **已认可的边界**：NVIDIA 缺证时停止、不以 deviceQuery 倒填已正确；AMD 官方[安装验证](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html)确实将 rocminfo 用于 runtime/driver 已加载确认（本轮转换坐标 L2392–2405）。本轮接受该命令共享为有限加载证据，**不要求另造一个独立命令或强拆官方步骤**。
- **尚缺**：AMD L149 只列安装及加载身份，没有单列固件信息的来源/版本或 unknown/不适用状态；rocminfo 的 runtime/driver 加载确认不能自动补成固件版本证据。通用 L2 明列固件要求，不能静默省略。
- **关闭条件**：将 NVIDIA 表述改为准确的核读范围限制，或依据可定位官方方法补充核读登记；保留缺证时本层未完成的规则。AMD 明确固件字段的来源及范围，未取得则记录 unknown/未完成且不以共享查询结果补齐。无需实际执行任何查询，不要求补猜测命令。

### R14 · P3 · R12 剩余：v12.8 bandwidthTest 的版本与核读范围尚未登记

- **位置**：registry L1398–1408、L2516–2529；正文 L105/L123；取证 L24。
- **证据**：`src.nvidia.cuda-samples-bandwidthtest-2026-10-08` 的 URL/revision/notes 仍是 master 观察；`src.nvidia.cuda-samples-v12.8` 的 URL/title/notes 均只指 vectorAdd，且明确与 master bandwidthTest 的基准不同。正文当前选择的却是 [v12.8 bandwidthTest](https://github.com/NVIDIA/cuda-samples/tree/v12.8/Samples/1_Utilities/bandwidthTest)。本轮连接器可读取该版本 README，证明入口有效，但不能代作者补成 registry 已核读该对象。
- **关闭条件**：在合适的稳定来源身份下补记 v12.8 bandwidthTest 的具体路径、tag/commit 和实际核读范围，并让取证 L24 对应当前来源。可扩展既有 v12.8 条目的范围；历史 master 记录可以保留，不需改写为曾经核读固定 tag，也无需新增重复身份。第二轮修订栏仍为占位，后续可在同次补记时交代这次范围调整，不要求改动历史审阅报告。

## 一致性与检查

- **已闭合的一致性**：版本范围注、ROCm 清理说明和 NVIDIA local/network 主张表，均与其对应 notes/正文一致；旧 CUDA ID 已明确废止并保留替代映射。此前已关闭事项不重开。
- **仍需补齐**：R13 限定驱动/固件证据边界；R14 限定所选固定样例的登记范围。它们均来自上一轮关闭条件，不是新的全量审阅清单。
- **结构检查**：577 条来源无重复 ID；正文 17 个 source_refs 均存在，schema/日期通过，21 处本地链接目标存在。`PYTHONDONTWRITEBYTECODE=1 make check` 通过：127 content entries / 577 sources；该检查不验证技术语义、远程页面或硬件适用性。
- **写入核对**：开始时记录 683 个 Git 已登记及未忽略文件的摘要；交付时原文件未改变，唯一新增为本报告。正文仍为 221 行及表中 SHA-256。未运行会写入 `build/` 的 `make build`，未修改 `src/kb/`，未运行 `make test`。

**T02-12 仍待 R13–R14 修订后的定向复核。** 当前没有实际安装、升级、卸载、设备查询或恢复成功证据；正文继续保留 `draft / source_checked` 与独立验证轨道边界。本报告的关闭结论仅覆盖上述文档修正，模型复核不替代真实环境验证。

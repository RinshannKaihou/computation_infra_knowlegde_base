# Batch 31 · T02-12 第四轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色 / 范围 | 原独立审阅者；第四轮定向复核，仅对照 R13/R14 关闭条件及其直接修订；不承担正文编写或修订 |
| 实际模型 / 档位 | `gpt-6.1-sol / xhigh`；本轮核验符合要求，计为正式复核 |
| 核验方法 | 开始时读取包含本轮请求的当前 rollout 最新 `turn_context`，核对顶层与 `collaboration_mode.settings` |
| 核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；`collaboration_mode.mode=default`、`settings.model=gpt-6.1-sol`、`settings.reasoning_effort=xhigh`、`settings.developer_instructions=null` |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T00-32-09-01a15f4e-4bcb-7a12-be50-b0ed78c23a91.jsonl` L464，ordinal 463；时间戳 `2026-10-21T17:05:19.252Z` |
| 会话 ID / turn ID | `01a15f4e-4bcb-7a12-be50-b0ed78c23a91` / `01a15f6c-91b2-7cb1-af15-6caab40a5d5f` |
| 身份边界 | 当前本地 Codex CLI 会话直接复核；未另启模型或子代理，未发现模型回退 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai；上述时间为 UTC |
| 正文基准 | `knowledge/02-software-stack/environment-installation-and-upgrade.md`；221 行（开始时 `wc -l`） |
| 正文 SHA-256 | `5d8e69e522fe056c5e0d59d9fd0f44fe35d03c4caf3dd4521609086d90e6dc9d`（开始时 `shasum -a 256`） |
| 上轮正文摘要 | `ae21a335b14bc9423e58041d770a3740c38eda760db9587ca9ef345d13c68a16`；历史报告不改写 |
| 写入范围 | 仅新增 `docs/research/batch-31-t02-12-codex-recheck-4.md` |

**结论：R13 CLOSED；R14 OPEN，仅余新增 notes 的一处来源范围误述，续记 R15（P3）。暂不宣布 T02-12 全部闭环。** 固定 tag 身份、样例路径及核读记录已经补齐；不再要求重复处理这些部分。

## 范围与方法

采用[第三轮报告](batch-31-t02-12-codex-recheck-3.md)的 R13/R14 关闭条件，核对[正文](../../knowledge/02-software-stack/environment-installation-and-upgrade.md) L105/L120/L123/L149、registry L2529/L7249，以及[取证记录](batch-31-t02-12-sources.md) L24/L65–71。没有重新全量审阅或重开其他已关闭发现。

重新打开 NVIDIA 驱动指南的 Verify the Driver Version；用 GitHub 连接器读取 v12.8 bandwidthTest 的完整 README，核对新登记描述。未执行任何来源命令或样例；本轮没有增加 CANN/AMD 远程核验范围。

## R13/R14 逐项判断

| 事项 | 判定 | 证据与关闭条件核对 |
|---|---|---|
| R13 · 驱动方法范围与固件缺项 | **CLOSED** | 正文 L120 已采用官方 `cat /proc/driver/nvidia/version` 方法并保留缺证则本层未完成、不以 deviceQuery 倒填的规则；registry L7249 补记该节，取证 L67 记录首登仅核读两节及本轮补读。正文 L149 明确 AMD 固件字段 unknown/未完成，不以 rocminfo 补齐。符合原关闭条件 |
| R14 · 固定样例登记范围 | **OPEN（仅 R15）** | registry L2529 已在稳定既有 ID 下追加同 tag 的 `Samples/1_Utilities/bandwidthTest`，继承该条目的 v12.8 / commit `db3eea23946bca2e90a75eca2b5b3e07158a9e11` 身份；正文 L105/L123 使用固定入口，取证 L71 明确对应此来源，旧 master 历史记录没有改写为固定 tag。核读范围已落盘，但新 notes 的“CUDA Toolkit 12.5+”超出 README 的文字，需按 R15 修正后关闭 |

### 已核实的直接依据

- [NVIDIA Verify the Driver Version](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/post-installation-actions.html#verify-the-driver-version)说明检查正确版本已加载，并列出正文采用的查询方法（本轮页面转换坐标 L48–52）。这里只核对文档方法存在及引用准确性，不证明本机加载状态，也不据当前 latest 页面证明历史响应逐字相同。
- [bandwidthTest README @ v12.8](https://github.com/NVIDIA/cuda-samples/blob/v12.8/Samples/1_Utilities/bandwidthTest/README.md)描述设备间及主机/设备双向拷贝带宽，列 pageable/page-locked 路径、SM 架构列表和 Prerequisites；README 没有给显式数值通过阈值。该有限描述与新增 notes 主干一致。
- 取证 L65–71 已补第三～四轮修订说明；L24 保留历史 master 来源，L71 将当前固定 tag 核读映射到扩展的既有 v12.8 来源，现行与历史身份可追踪。

## R15 · P3 · R14 剩余：README 的版本文字被扩成兼容范围

- **位置**：`sources/registry.yaml` L2529，Batch 31 扩展核读段。
- **问题**：登记写“要求 CUDA Toolkit 12.5+”；原 README 的 Prerequisites 写“Download and install the CUDA Toolkit 12.5”，没有 `+`、最低版本或向后续版本开放的范围声明。固定 tag 为 v12.8 和 README 中出现 12.5 是两种记录，应分别保存，不能自行合成为最低版本要求。
- **证据**：上述固定 tag README 的 Prerequisites 段，本轮连接器完整读取；本报告没有由此推导任何实际安装可用性。
- **关闭条件**：将 notes 改为准确的“README 前置条件段写 CUDA Toolkit 12.5”等有限描述；tag/commit 身份独立保留，不推导未声明的版本范围。如需作范围判断，须另有明确依据。无需修改正文方法、历史 master 记录、上游文件或执行测试；修正后只需复核此处及相关摘要的一致性。

## 检查与写入核对

正文 schema/日期检查通过，17 个 source_refs 均存在，577 条来源无重复 ID，21 处本地链接目标存在。`PYTHONDONTWRITEBYTECODE=1 make check` 通过：127 content entries / 577 sources；这些检查不验证技术语义或硬件兼容性。

开始时记录 684 个 Git 已登记及未忽略文件的摘要；结束时原文件未改变，唯一新增为本报告。正文仍为 221 行及表中 SHA-256。未运行会写入 `build/` 的 `make build`，未修改 `src/kb/`，未运行 `make test`。

**后续仅需处理 R15 并定向复核。** 已关闭项维持关闭，本轮未发现需要重开它们的直接回归；文档仍为 `draft / source_checked`，没有执行安装、升级、卸载、设备查询或计算样例，真实验证继续由独立轨道承接。

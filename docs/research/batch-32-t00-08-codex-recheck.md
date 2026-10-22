# Batch 32 · T00-08 定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色 / 轮次 | 独立批次审阅者；初审修订后的定向复核；本会话不承担正文编写或问题修订 |
| 指定 / 实际模型与档位 | 指定 `gpt-6.1-sol / xhigh`；当前 rollout 的实际记录为 `gpt-6.1-sol / xhigh`，一致 |
| rollout 文件 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T10-26-52-01a1616e-c73c-7dc1-b1e3-68073a38c93d.jsonl` |
| 会话 ID 互核 | 环境 `CODEX_SESSION_ID`、`CODEX_THREAD_ID` 与 rollout L1 的 `session_meta.id` 均为 `01a1616e-c73c-7dc1-b1e3-68073a38c93d`；文件名中的 ID 亦一致 |
| 最新 turn_context | rollout **L8**，时间戳 `2026-10-22T02:26:57.571Z`；`model=gpt-6.1-sol`、`effort=xhigh`；当前文件只有 1 条 `turn_context` |
| 档位交叉核验 | 同条记录的 `collaboration_mode.mode=default`，`settings.model=gpt-6.1-sol`、`reasoning_effort=xhigh`、`developer_instructions=null`；与顶层实际模型、档位一致 |
| turn / 工作目录 | `turn_id=root_turn_id=01a1616e-c81a-7551-9a01-8951b95b2d56`；`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 执行方式 / 日期 | 本地 Codex CLI 当前会话直接审阅；`originator=codex_exec`、`source=exec`、CLI `0.163.0`；2026-10-22 / Asia/Shanghai；未另启模型或子代理 |
| 核验方法与结果 | 解析当前会话 JSONL 的 `session_meta` 与最新 `turn_context`，对照进程环境及两处档位字段；开始与落盘前复读均一致。模型与档位核验 **PASS**，不以历史报告或默认配置代替实际记录 |
| 比较基准 | HEAD `90c38f7592137eeb2b1862983822fe415cf471c5`；五页在该 commit 中的行数与 SHA-256 均与初审报告输入快照一致，因此本轮以该基准的差异界定修订增量 |
| 写入范围 | 仅新增本报告；保留工作区既有修改。角色页仅审 C03 所涉 L89 的三平台枚举，不扩大至该页其他修订 |

| 发现 | 初审优先级 | 定向复核判定 | 关闭条件核验 |
|---|---|---|---|
| C01 | P2 | **CLOSED** | AMD 入口已就地区分含 AMD 取证的正文、通用方法伴读及尚未核对的 AMD 实现能力 |
| C02 | P2 | **CLOSED** | 五页均有进入条件、知识目标及可检查的阅读产出，实际执行与硬件验证仍独立 |
| C03 | P3 | **CLOSED** | 三平台均可直接进入两个排障页，平台切换及角色页枚举一致，本地链接与 ID 有效 |

**复核结论：C01–C03 共 3 项全部 CLOSED，剩余 OPEN 0 项；该项任务在本审阅范围内通过。** 此结论不代改任务或主题账本，不替代其他任务的审阅，也不建立硬件验证结果。

### 开始复核时的输入快照

在读取修订内容作语义判断前，已对下列文件实际执行 `wc -l` 与 `shasum -a 256`。落盘前重新对照字节摘要，均未变化；行数为命令输出的换行计数。

| 文件 | 行数 | SHA-256 |
|---|---:|---|
| [AMD 平台页](../../paths/platforms/amd.md) | 133 | `4783edb523bfd8002e1f317e6d9daf15620ecee0aeab11c9c675ee8dfb5e99e3` |
| [NVIDIA 平台页](../../paths/platforms/nvidia.md) | 216 | `ffe2a16d415ede544323ffd83d783ce28d588e888ef12d6c1c8b9cbf60550ae8` |
| [昇腾平台页](../../paths/platforms/ascend.md) | 240 | `42dfbbcf4d90075dff614e4b66da6dc30bc5bf108d32a5259d54061f1abeca15` |
| [训练排障页](../../paths/tasks/training-triage.md) | 177 | `8d5872c13dc9fcd7c681bb567904e1a82dddfebffce7c995570a05f4605789ed` |
| [推理排障页](../../paths/tasks/inference-triage.md) | 151 | `ea59b6fffe36f2daf960170bf821f459b26cf75cfe62219dc9ef44af378915be` |
| [角色页](../../paths/roles/reading-by-role.md)（语义范围仅 L89 平台枚举） | 113 | `3dc6a7165bfa721c72f1382e0b9288450343b909601c124f881eb480d0b8356f` |
| [编写者修订记录](batch-32-t00-08-sources.md) | 31 | `355a77d923251dc7babc186f13270755fec7a250aa9d74516c8ab7d8af25852b` |
| [初审报告](batch-32-t00-08-codex-review.md) | 177 | `39a96e392c8c0b63ef7bdf685232f2c96445c497c806000857754ccd97709aa2` |

## 逐项关闭条件核验

判据取自[初审报告](batch-32-t00-08-codex-review.md) C01–C03（L105–145），以当前文件为证据；作者[修订记录](batch-32-t00-08-sources.md) L27–31 仅用于定位，不作为关闭证明。以下行号均为修订后文件实际行号。

### C01 · P2 · CLOSED

关闭条件：入口应能区分含 AMD 取证的诊断目标、通用方法伴读和 AMD 实现能力未核对；具体检查可追到正文条件，不能从 generic、接口相似或其他平台插件推导适用。

| 子条件 | 修订后原文与位置 | 独立核验 |
|---|---|---|
| 设备资源链与 AMD 实现分开 | [AMD 页](../../paths/platforms/amd.md) **L88**：“通用责任链（实现例为 MindCluster/NVIDIA 设备插件与 Slurm，**AMD 插件接入未取证**）”；同一行新增“AMD 侧设备/容器访问的具体取证（`/dev/kfd`、render node、权限与 ROCm 容器文档）”正文链接 | [设备资源链](../../knowledge/05-cluster-platform/device-resource-chain.md) L43–58 确为责任模型，L73 起及 L91 起分别为 MindCluster、NVIDIA 实现；[OS/进程资源正文](../../knowledge/02-software-stack/host-resource-pressure-and-device-access.md) **L164–167** 确有 AMD 节点权限组、`/dev/kfd`、render node 与容器分支。没有把通用资源链当成已取得 AMD 插件证据 |
| 性能正文与慢 rank 伴读分开 | AMD **L103**：“从……性能分解……开始（含 AMD 取证）”；慢 rank 改为“通用阶段分析方法伴读”，并明示“**RCCL/ROCm 侧对应检查能力未核对**，不能由接口相似推定适用” | [性能正文](../../knowledge/06-training/performance-analysis.md) **L72** 有 ROCprofiler-SDK 独立证据及版本限制；[慢 rank 指南](../../knowledge/06-training/slow-rank-triage.md) **L46、L54–58** 的实际样板确为 PyTorch 2.8、NCCL 2.27.5、NCCL RAS/desync/flight recorder 与 DCGM。修订没有新增 RCCL 对等能力断言 |
| 三类边界可识别，取证记录同步 | AMD **L77** 明列“含 AMD 取证 / 通用方法伴读 / AMD 实现能力未核对”；作者取证记录 **L14、L29** 亦明确将慢 rank、设备资源链作为通用伴读 | 三类区分已落实到 L88/L103 的具体入口，不再仅依赖页首总声明；取证记录与实际修订一致 |

**判定：CLOSED。** AMD 访问和性能目标有实际正文承接，通用伴读的实现缺口在入口处可见；不要求本轮补写兄弟篇或运行硬件试验。

### C02 · P2 · CLOSED

关闭条件：五页均有可定位的先修/进入条件、知识目标和完成检查，能区分阅读完成、仍需补证据及超出路径范围；执行与硬件验证保持独立。

| 页面 | 进入条件 / 知识目标证据 | 完成检查原文与判定 |
|---|---|---|
| [AMD](../../paths/platforms/amd.md) | **L75**：“已读……00 导读……记录目标环境身份”，初学者先读软件栈分层；**L77** 要求定位 AMD 取证正文并说明三类证据边界 | **L79** 检查版本/制品身份与无证据组合、术语/工具的取证及 unknown、下一项验证缺口；“**三者任一答不出即未完成，回到对应入口补读**” |
| [NVIDIA](../../paths/platforms/nvidia.md) | **L106** 明确导读、环境身份及软件栈先修；**L108** 要求定位平台正文/档案并说明边界 | **L110** 检查版本/制品身份、无证据或来源冲突、任务首要入口与验证缺口、通用机制和平台取证区分；“**任一答不出即回到对应入口补读**” |
| [昇腾](../../paths/platforms/ascend.md) | **L120** 明确导读、环境身份及软件栈先修；**L122** 要求定位昇腾正文/档案及证据边界 | **L124** 检查制品身份、无证据组合、任务入口/缺口和通用机制边界；保留“**TorchNPU 档案不与 MindCluster/Atlas 资料自动组成已验证环境**”，任一答不出即补读 |
| [训练排障](../../paths/tasks/training-triage.md) | **L96** 要求先整理环境、异常时间、基线、变更、rank 与证据；**L98** 要求形成候选原因、可检验假设及下一项检查 | **L100** 要求写出“现象与影响范围”“首要领域入口与至少两个候选原因”“缺失证据与下一项检查”“停止/升级条件”；证据不足、权限不足、无回退均须有对应动作；不能定位时记录排除范围与缺口后升级 |
| [推理排障](../../paths/tasks/inference-triage.md) | **L80** 要求环境、引擎、请求分布、副本、指标窗口，并分开请求失败/性能/输出质量；**L82** 要求按请求路径与证据形成假设及下一项检查 | **L84** 给出同样四项知识定位产出，特指“**客户端与服务端观测分开**”；“任一写不出即未完成”，无法定位时记录缺口后升级 |

五页的目标均为知识定位与证据产出，没有要求以命令执行成功作为阅读完成。AMD L63/L112、NVIDIA L94/L202、昇腾 L106/L193、训练 L84/L151、推理 L68/L128 仍明示草稿、未实测或须匹配环境；新完成检查也要求列出尚缺证据。两排障页明确了未完成与升级分支，三平台页明确了无证据组合及验证缺口，满足本项条件。

**判定：CLOSED。** 先修、目标与完成检查五页齐全；本轮不据此更新 00.6 主题状态或真实验证状态。

### C03 · P3 · CLOSED

关闭条件：任一平台页可直接找到两个排障首要入口，三平台切换一致，角色页平台枚举符合现状，本地链接与稳定 ID 继续有效。

| 起点 | 平台切换证据 | 排障首要入口证据 |
|---|---|---|
| [AMD](../../paths/platforms/amd.md) | **L116**：“与昇腾路径、NVIDIA 路径使用相同的领域归属”，两条直接链接存在 | **L120**：“排障首要入口：训练排障 · 推理排障”，均直接链接任务页 |
| [NVIDIA](../../paths/platforms/nvidia.md) | **L126** 直接链接昇腾、AMD | **L206** 新增“**排障首要入口：训练排障 · 推理排障**”，均为正确相对路径 |
| [昇腾](../../paths/platforms/ascend.md) | **L126–128** 新增跨平台比较小节，直接链接 NVIDIA、AMD，并要求“错误码、环境变量、诊断工具与支持边界分别查证” | **L197** 新增“**排障首要入口：训练排障 · 推理排障**”，均为正确相对路径 |

[角色页](../../paths/roles/reading-by-role.md) **L89** 的平台枚举实际为“**平台分支见昇腾/NVIDIA/AMD 专题**”，三个词分别链接对应平台页；本项仅核对该行的枚举及目标。训练页 L132–134、推理页 L110–112 仍直接链接三平台。三平台现在各有本组其他两平台及两排障页共四个直接邻接目标；无需任务页彼此互链。

五页 frontmatter 与初审基准逐项相同，五个稳定 ID 未改；新增链接目标的 ID、类型及平台字段符合导航意图，未以元数据平台标记推定技术适用性。

**判定：CLOSED。** 平台切换、两排障入口及角色枚举均满足关闭条件，链接/ID 检查通过。

## 增量语义核对

本轮对五页与初审同字节基准的全部修订差异逐段核对，并抽查所链正文；不重审任务全范围或兄弟篇全部上游主张。未重新抓取外部网页，以下判断是新增导航描述与仓库正文的一致性核验，不是远程文档更新认证。

| 增量 | 抽查落点与结果 |
|---|---|
| AMD 新增设备访问链接 | [OS/进程资源正文](../../knowledge/02-software-stack/host-resource-pressure-and-device-access.md) L166–167 明列权限组与容器设备访问，来源为 **docs-7.2.4**；AMD 页 L88 仅指引这些取证内容，没有把它与页首 ROCm 10.1.0 样板拼成整栈已验证组合，也没有把 render node 访问证明当作 AMD 插件实现证明 |
| AMD 性能入口重新排序 | [性能正文](../../knowledge/06-training/performance-analysis.md) L72 明确 **ROCprofiler-SDK 1.3.2 / docs-7.14.0** 与 ROCm 10.1.0 组件表的 **1.4.1** 分属不同版本线；“含 AMD 取证”符合该段，未变成全篇检查都适用 AMD 的承诺。慢 rank 仍只借用阶段分析，并在同一入口声明 RCCL/ROCm 检查能力未核对 |
| 三平台新增档案完成检查 | [AMD 档案](../../knowledge/02-software-stack/amd-rocm-documented-profile.md) L212–229 分列 documented/conflict/unknown 与 not_run；[NVIDIA 档案](../../knowledge/02-software-stack/nvidia-documented-profile.md) L163–172 保留 R545、Python/制品版本冲突与未知组合；[昇腾档案](../../knowledge/02-software-stack/ascend-documented-profile.md) L109–128 保留精确 HDK 交集缺口、MindCluster 未纳入及“未纳入≠不兼容”。五页新增文字没有抹去这些限制 |
| 新增先修链接与两排障页产出 | 导读及软件栈分层均为现有正文。两排障页的新增产出是导航的阅读要求；与已链[证据与假设](../../knowledge/08-reliability/evidence-and-hypotheses.md) L97–112 的检查收益/代价/影响及授权前提、L138–150 的证据/未知/排除条件一致，没有新增诊断根因、已执行结果或操作授权 |
| 新增平台/任务回链 | 链接文字与目标的稳定 ID、类型、平台字段一致；昇腾新增比较文字仍要求按具体机制及平台分别查证，未引入术语、工具或支持矩阵等价断言 |

差异检查确认：五页元数据均未改；两排障表的原有行逐字保留。新增内联本地链接共 **16 处**（AMD 4、NVIDIA 5、昇腾 7；两任务页无新增链接），全部目标存在。当前五页的内链处数/不同目标依次为 **59/47、87/84、105/95、97/71、82/59**，合计 **430 处 / 118 个不同目标**；无失效目标。角色页 L89 的三条平台链接另行核对，不并入五页计数。

**增量结论：未发现需要保留 OPEN 或另立必修发现的新增语义问题。** 样板与实际环境、通用方法与具体实现、阅读完成与硬件验证的边界均保持。

## 结构校验与写入范围复核

报告落盘后实际执行 `PYTHONDONTWRITEBYTECODE=1 make check`，**退出码 0**：

```text
PASS: 135 content entries; 577 sources.
Checked structure and local file links; not technical correctness or remote links.
```

该结果只确认结构和本地文件链接；语义、平台边界与关闭条件由上述独立核对承担。另行解析本报告的 **30 处内联本地链接**，全部目标存在。八份输入的最终行数与 SHA-256 均与头表一致。

工作区原有其他 Batch 32 的修改与报告。本会话在只读核对阶段对 **714 个 Git 跟踪及非忽略未跟踪文件**建立 SHA-256 快照；落盘前快照无变化。写入报告并运行校验后为 **715 个文件**，714 个既存文件无变化、无删除，唯一新增为 `docs/research/batch-32-t00-08-codex-recheck.md`。未修改正文、作者记录、角色页、计划、registry 或构建产物。

按本轮指令未执行 `make build`；未改 `src/kb/`，未新增测试或运行 `make test`。没有执行知识正文中的安装、诊断、调试采样、恢复或故障注入命令，未操作真实集群。

## 结论

**C01、C02、C03 全部 CLOSED；该项任务在本审阅范围内通过。** 本报告仅关闭上述初审发现及本轮修订增量的审阅问题；不自动关闭 00.6 整体主题、不修改计划或内容编辑状态，也不将来源核对、结构通过或导航可达视为硬件验证。

# Batch 31 · T02-12 第二轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色 / 范围 | 原独立审阅者；第二轮定向复核，仅核对上一轮 R01–R07 关闭条件及其直接修订，不承担正文编写或修订 |
| 实际模型 / 档位 | `gpt-6.1-sol / xhigh`；本轮核验符合要求，计为正式复核 |
| 核验方法 | 开始时定位包含本轮用户请求的当前 rollout，读取最新 `turn_context` 顶层与 `collaboration_mode.settings`；不沿用上一轮记录 |
| 核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；`collaboration_mode.mode=default`，`settings.model=gpt-6.1-sol`、`settings.reasoning_effort=xhigh`、`settings.developer_instructions=null` |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T00-32-09-01a15f4e-4bcb-7a12-be50-b0ed78c23a91.jsonl` L300，ordinal 299；时间戳 `2026-10-21T16:54:04.429Z` |
| 会话 ID / turn ID | `01a15f4e-4bcb-7a12-be50-b0ed78c23a91` / `01a15f62-470f-7ab2-99ab-36a10d4b9621` |
| 身份结论 | 当前本地 Codex CLI 会话直接复核；未另启模型或子代理，未发现模型回退；工具引用中的规则文字不作为回退证据 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai；上述时间为 UTC |
| 正文基准 | `knowledge/02-software-stack/environment-installation-and-upgrade.md`；219 行（开始时 `wc -l`） |
| 正文 SHA-256 | `c1ce65a42dc0d0df1710766fda2abb4364ec342fd846a5dd9818e0f9bc3d852a`（开始时 `shasum -a 256`） |
| 上一轮基准 | 210 行，SHA-256 `9ca061b0673932def8b90bf55837c6edff541f4b54651d82f4319557739b2b6c`；历史审阅报告不改写 |
| 写入范围 | 仅新增 `docs/research/batch-31-t02-12-codex-recheck-2.md` |

**结论：暂不通过。R01–R07 中 2 项 CLOSED（R03、R05）、5 项 OPEN（R01、R02、R04、R06、R07）。剩余部分续记为 R08–R12：P1 0、P2 2、P3 3。** R02 的方法入口和最终验收门槛已补齐，余下仅为跨版本引用限定，按 P3 续记；不再将整个方法小节视为缺失。

## 方法与证据边界

以[上一轮报告](batch-31-t02-12-codex-recheck.md)的七项关闭条件为唯一问题清单，核对[正文](../../knowledge/02-software-stack/environment-installation-and-upgrade.md)、[取证记录](batch-31-t02-12-sources.md)和 `sources/registry.yaml`。没有重做完整三平台审阅，也没有重开已关闭的初审项。

定向重读上游 ROCm 安装页的内核驱动与卸载/仓库清理部分、CUDA 12.8 §10.3.3，以及 NVIDIA Ubuntu 的仓库部分。GitHub 连接器重新检查 v12.8 的 vectorAdd/bandwidthTest README 和残留 master 链接。运行时篇只核对被新增方法表调用的章节、版本声明和方法内容。

CANN 路径、触发条件和 0094 内容沿用前轮已读取的辅助材料比对，本轮复核缓存摘要未变：`cann-0030.html` 为 `39d8c94980ba3a665a7323dbe12d1cc8106686c0cb65b373d6b7e11d32f3d3b0`，`cann-0032.html` 为 `81290adefa2fda0c7178a738a49c4f9977c893bb8babd8afa45d20c4706a338e`，`cann-0033.html` 为 `258fc1a3d7c302e6750affe5079d4da4aac56032659366abb502d181048af378`，`cann-0094.html` 为 `2a3f6534364d604a05c1cf0b831e1b424f88f03d951d7b0a816c79732303eb2e`。未重新下载，不增加“当前远程原件已核验”的结论。

## R01–R07 逐项判定

正文坐标均为本轮 219 行版本。判断依据是文件实际内容，不以修订概要替代核对。

| 上轮事项 | 判定 | 已落实部分与剩余 |
|---|---|---|
| R01 · 驱动与用户态分层 | **OPEN** | AMD L147–150 已分开安装路径、inbox/独立驱动/runfile，并禁止 L5 倒填 L2，错误“一并安装”通则已删除。NVIDIA L118 仍只将包版本登记与设备节点作为本层证据；AMD L147 的加载证据括注也只有安装来源/版本，尚未将已安装与已加载身份闭合或将缺失部分明确记未完成。余项 R08 |
| R02 · 最小方法与结果契约 | **OPEN（剩余降为 P3）** | L101–109 已给三平台方法/同步入口及待冻结字段，明确最终安装/升级不能在未冻结契约时通过；不要求现在填写数值或实跑。尚未落实上一轮关闭条件中的跨版本引用限定：链接方法篇的 CANN/HIP 样板版本与本篇目标文档线不同。余项 R09 |
| R03 · alternatives 适用范围 | **CLOSED** | L192 限定旧 toolkit 完整保留、应用依赖软链接，要求重启进程并按 L4 核实实载；显式路径、容器/框架 runtime、驱动和缺失制品走各自路径。registry L2963 同步 §10.3.3 的软链接条件 |
| R04 · ROCm 仓库清理误记 | **OPEN** | 正文 L200 与取证 L12/L41 已正确列仓库/缓存清理，旧行也已标“已被取代”。但 registry L2673 末句仍写“完整版本回退、依赖恢复与仓库清理未见专门说明，保持 unknown”，与前两者冲突。余项 R10 |
| R05 · CANN 路径与 Kernels 前提 | **CLOSED** | registry L7238 已改完整固件路径，区分 NNAE 与其他包路径，并明确自动卸载的跟随安装前提；与正文 L165/L199 和取证 L11 的现行口径一致。0094 的环境/依赖/样例内容也已补入 notes。关闭仅覆盖已知文本修正与一致性，不升级远程核读或回退能力 |
| R06 · NVIDIA 仓库摘要同步 | **OPEN** | registry L7249 已区分 local 包/复制 keyring 与 network cuda-keyring，正文 L118 一致；取证当前主张表 L10 仍写“cuda-keyring 两种 repo”，未标废止。余项 R11 |
| R07 · 样例定位与现行/历史记录 | **OPEN** | L105 有可读的 v12.8 vectorAdd/bandwidthTest 入口；CUDA notes 已补 §10.3.3、CANN notes 已补 0094，正文 L163–164/L199 已补相应页号。L121 仍保留 404 的 master 链接，取证 L9/L24 仍按现行表呈现旧来源 ID/master，第二轮修订栏仍为占位。余项 R12 |

## R08–R12：剩余关闭条件

### R08 · P2 · R01 剩余：包版本及节点仍不能代替已加载驱动身份

- **位置**：正文 L84、L118、L147。
- **证据**：通用 L2 要求驱动已加载及驱动/固件身份。L118 的包登记只证明安装身份，必要设备节点不能补足加载身份；L147 写“加载证据……（安装来源与版本）”也未说明如何获得已加载状态。官方安装步骤与安装制品登记不构成两种状态相等的保证。这是上一轮 R01 的剩余，不新增硬件实测要求。
- **关闭条件**：明确安装身份、已加载身份及固件信息各自的可定位方法/证据字段；缺少相应来源或采集能力时，将对应 L2 检查记 unknown/未完成且不放行。可以引用已有正确方法，不要求新造命令，也不能用 L5 成功反向填满 L2。

### R09 · P3 · R02 剩余：方法表未保留跨版本引用限制

- **位置**：正文 L105–107；被引用的运行时篇 L65、L142、L195、L310–325。
- **证据**：本篇文档线为 CANN 8.3.RCX / ROCm 10.1.0，而[运行时篇](../../knowledge/02-software-stack/runtime-execution-and-library-loading.md)明确固定为 CANN 8.2.RC1.alpha001 与 HIP 6.3.42134（docs-6.3.3）。新表只写“CANN 侧/HIP 侧样板”，未提示这些版本差异。该篇确有四步方法及同步/错误语义，故不再把方法存在性判为 P2 缺失，也不要求填具体容差。
- **关闭条件**：方法表明确这些入口只提供相应旧版方法样板；目标文档线上的接口、样例及适用条件须另核，未核时相应验证环节保持未完成。给对应章节位置即可，不要求为关闭本项重写相邻篇或执行安装。

### R10 · P2 · R04 剩余：ROCm registry 的 unknown 范围没有收窄

- **位置**：registry L2673 末句；对照正文 L200、取证 L12/L41。
- **证据**：[ROCm 安装页 Uninstalling](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html#uninstalling)包含仓库移除与缓存清理（本轮网页转换坐标 L2670–2678 等）。正文和取证已据此更正，notes 仍把仓库清理列为无说明。取证 L52 的上一轮修订叙述还保存旧错误，但该处属于历史记录，应与现行结论区分。
- **关闭条件**：notes 当前有效结论与正文/取证一致：卸载、仓库/缓存清理说明已存在；unknown 只覆盖仍无依据的完整回退与依赖恢复。历史误记可保留，但须标清已取代，不能留作有效核读结论。无需再复制或执行清理命令。

### R11 · P3 · R06 剩余：取证主张表仍合并两种仓库

- **位置**：取证 L10；对照正文 L118、registry L7249。
- **证据**：[NVIDIA Ubuntu 指南](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/ubuntu.html)区分 local repo 包与 network cuda-keyring；正文和 registry 已改，当前主张表仍写“两种 cuda-keyring”。L54 的修订记录不能代替主张表更新。
- **关闭条件**：同步主张表，或将原表行明确标为已废止历史并指向当前口径；local/network 各自对应的包与公钥处理不再混淆。

### R12 · P3 · R07 剩余：新固定入口未替换旧有效入口，历史表尚未分清

- **位置**：正文 L121；取证 L9/L24/L59/L61–63；正文 source_refs 的 master 样例登记。
- **证据**：L105 新增的固定 tag 入口可读，但平台步骤表 L121 仍链接 master/bandwidthTest，本轮连接器仍返回 404。取证 L9 继续把已删除的 `src.nvidia.cuda-128-install-guide-linux` 标为“本轮新增”，L24 仍指 master；L59 虽可追踪旧→新 ID 映射，当前表与历史表仍未标清，第二轮修订记录也没有实际回填。这些是上一轮 R07 指定余项，并非新增全量来源审阅要求。
- **关闭条件**：实际步骤表采用已确认可定位的样例入口，并在对应登记中记录固定版本/核读范围；取证表呈现当前稳定 ID，或明确标为废止历史并指向替代记录；补齐本轮修订的可追踪说明。历史报告保持原样，不要求改写旧报告中的原始 ID。

## 一致性、结构与写入核对

- **已一致**：alternatives 条件、CANN 卸载路径与跟随安装前提、0094 内容、CUDA §10.3.3 的 notes 已与正文相应主张对应；不因其他余项而重复打开这些修正。
- **仍不一致**：ROCm 清理 unknown（registry）、NVIDIA 两种仓库（取证表）、旧样例链接与旧 ID 的现行/历史呈现，分别由 R10–R12 跟踪。
- **结构**：577 条来源无重复 ID；正文 17 个 source_refs 均存在，schema/日期通过，21 处本地链接目标存在。`PYTHONDONTWRITEBYTECODE=1 make check` 通过：127 content entries / 577 sources。结构检查不证明技术正确性或实际安装可用。
- **写入**：开始时记录 682 个 Git 已登记及未忽略文件的摘要；结束时核对原文件未变，唯一新增为本报告。正文仍为 219 行及表中 SHA-256。未运行写入 `build/` 的 `make build`，未改 `src/kb/`，未运行 `make test`。

**T02-12 仍待处理 R08–R12 后再次定向复核。** 本轮没有发现需重开此前已关闭项的直接回归；没有执行安装、升级、卸载、设备查询或计算样例，也没有新增实际恢复成功证据。正文继续保留 `draft / source_checked` 与独立验证轨道边界。

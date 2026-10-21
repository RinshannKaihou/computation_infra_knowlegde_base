# Batch 31 · T02-12 定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色 / 轮次 | 原独立审阅者；初审 C01–C13 修订后的第一次定向复核；不承担正文编写或修订 |
| 实际模型 / 档位 | `gpt-6.1-sol / xhigh`；符合本轮要求，本报告计为正式定向复核 |
| 核验方法 | 开始时定位包含本次复核请求的当前 rollout，读取最新 `turn_context`，核对顶层与 `collaboration_mode.settings`，不沿用初审轮次的档位记录 |
| 核验结果 | 顶层 `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base`；嵌套 `mode=default`、`settings.model=gpt-6.1-sol`、`settings.reasoning_effort=xhigh`、`settings.developer_instructions=null` |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T00-32-09-01a15f4e-4bcb-7a12-be50-b0ed78c23a91.jsonl` L201，ordinal 200，时间戳 `2026-10-21T16:46:13.698Z` |
| 会话 ID / 当前 turn ID | `01a15f4e-4bcb-7a12-be50-b0ed78c23a91` / `01a15f5b-184f-74f0-a469-719648bb5806` |
| 身份边界 | 同一会话的后续轮次；未另启模型或子代理，未发现元数据模型回退；工具引用中的规则文字不作为回退证据 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai；上述时间为 UTC |
| 复核正文 | `knowledge/02-software-stack/environment-installation-and-upgrade.md`，210 行（开始时 `wc -l`） |
| 修订版 SHA-256 | `9ca061b0673932def8b90bf55837c6edff541f4b54651d82f4319557739b2b6c`（开始时 `shasum -a 256`） |
| 初审基准 | 156 行，SHA-256 `86c2961953fc4c36280745a05166d0f1834a40d677756fb9dcdf61e69f7e13a8`；初审报告保持原样 |
| 写入范围 | 仅新增本报告 `docs/research/batch-31-t02-12-codex-recheck.md` |

**复核结论：暂不通过。C01–C13 中 6 项 CLOSED、7 项 OPEN；本轮归并为 R01–R07 七项待处理事项（P1 0、P2 5、P3 2）。** C05 的原保全/全量卸载问题已关闭，但修订另引入 R03 的回退机制过度概括，不能据此宣布整篇闭环。

## 范围与方法

逐条采用[初审报告](batch-31-t02-12-codex-review.md)既定关闭条件，核对修订[正文](../../knowledge/02-software-stack/environment-installation-and-upgrade.md)、[取证记录](batch-31-t02-12-sources.md)、`sources/registry.yaml` 和 02 首页相关行。只检查这些修订及其直接回归，没有重新全量审阅三平台资料或 06/07 的已闭环任务。

定向重新打开 ROCm 安装页的内核驱动安装、Uninstalling/仓库清理部分，CUDA 12.8 §3.12.3.7/§10.3.3，以及 NVIDIA 驱动 Ubuntu 的 local/network 仓库部分。通过 GitHub 连接器确认 ROCm 指定 commit 存在，并复查 CUDA master/bandwidthTest 入口及固定 12.8 样例。没有执行来源中的安装、卸载、查询设备或样例命令。

CANN 0030/0032/0033 精确静态页本轮仍不可读；重新读取初审已使用的本机辅助缓存，三份摘要均与初审一致：0030 为 `39d8c94980ba3a665a7323dbe12d1cc8106686c0cb65b373d6b7e11d32f3d3b0`，0032 为 `81290adefa2fda0c7178a738a49c4f9977c893bb8babd8afa45d20c4706a338e`，0033 为 `258fc1a3d7c302e6750affe5079d4da4aac56032659366abb502d181048af378`。缓存没有重新下载；不据此宣称当前远程原件已独立核实。

## C01–C13 逐项关闭判断

下表正文行号均指本轮 210 行版本。CLOSED 只关闭原发现；另外识别出的回归仍单列，不以修订概要或修订记录中的“已处理”代替实际文件核对。

| 初审项 | 判定 | 核对结果与证据坐标 |
|---|---|---|
| C01 · 分层证据 | **OPEN** | L81–91/L112/L127/L140 已正确区分环境配置、权限与实载，无法采集实载记未完成；但 NVIDIA L2（L110）仍无驱动/固件身份核查闭合，AMD L139 仍合并 L2/L3、由 L5 回填 L2，并新增“一并安装”的无条件概括。余项 R01 |
| C02 · 运算/同步/结果 | **OPEN** | L93–101 已区分传输、枚举、形态和数值契约，并保留未冻结无法判断；仍无三平台各自可定位的最小运算与完成同步/错误检查方法，“若验收需要”使契约成为可选。余项 R02 |
| C03 · 11 类变化与 B0/N/R | **CLOSED** | L148–175 包含所需 11 类身份、独立变/不变登记要求及检查层；model/config/input 虽共用一行，L160 明确各自独立登记。B0/N/R 均记录环境/输入/判据/输出，使用同负载同判据，首次安装不虚构基线。关闭不要求机械拆成 11 个表行，也不代表任何实际 B0 已存在 |
| C04 · 前置停止与不可逆/恢复 | **CLOSED** | L65–75 三类缺项停止实际变更；L184 扩至数据/模型/状态格式；L175/L199 明确首次安装目标及按受影响层、B0 同判据恢复。方法门槛齐备，不构成现场授权或回退已成功 |
| C05 · 制品保全与全量卸载 | **CLOSED（原问题）** | L183 保全版本/变体/摘要/依赖/仓库/配置/数据；L189 区分通配全量卸载并标明命中旧版属于语义推断；L190 删除 CANN 旧目录保留保证。L183 新增的无条件 alternatives 回退说法另见 R03 |
| C06 · ROCm 卸载误记 | **OPEN** | L191 与 registry L2673 已承认 Uninstalling；但同时误记仓库清理无说明，取证 L12/L41 仍保留未标废的“无专门卸载章节”。余项 R04 |
| C07 · CANN 路径 | **OPEN** | 正文 L190 的固件完整路径及 NNAE/NNAL 等分列已修正；registry L7238 仍为错误绝对路径 `/firmware/script/uninstall.sh`，且仍将 NNAE 概括进架构目录。余项 R05；原页读取缺口未消除 |
| C08 · CUDA 模板与仓库说明 | **OPEN** | 正文 L110–111 与 CUDA registry L2963 已记录具体坐标及模板冲突、区分两类仓库；NVIDIA 驱动 registry L7249 和取证 L10 仍写两种 cuda-keyring。余项 R06 |
| C09 · Kernels 安装关系前提 | **OPEN** | 正文 L156 与取证修订记录 L55 已补“跟随宿主包安装”前提；registry L7238 及取证主张表 L11 未同步此条件。余项 R05 |
| C10 · unknown 与不支持 | **CLOSED** | L75/L83/L124/L152 分开证据状态和操作门槛，保留查询未取得的 unknown，只在明确否定或封闭全集规则下记不支持 |
| C11 · 导航过早闭环 | **CLOSED** | 02 首页 L60 改为“draft，审阅修订中，未实测”；related ID（L37）及 02.7 登记仍在，未宣称本轮已通过 |
| C12 · 就近定位与登记范围 | **OPEN** | 新增的两个 source_refs、CANN revision 纳入 0094、AMD commit 树 URL、06/07 恢复链接均已落实；CUDA master 链仍 404，vectorAdd 元数据不能代替 bandwidthTest 定位；0094 内容与 §10.3.3 未纳入相应 notes，部分升级/回退定位仍只有泛指节名。余项 R07 |
| C13 · CUDA 双身份与 EULA | **CLOSED（身份与许可问题）** | 577 条来源中旧重复 ID 为 0、稳定既有 ID 为 1，相同 CUDA 安装页 URL 仅余该条；正文 L9/L44 已替换，既有条目的 EULA URL 是 12.8.0 归档。取证 L59 给出旧→新身份映射，因此历史引用仍可追踪；首轮表仍标“本轮新增”的呈现不清并入 R07，不认定为 registry 再次出现双身份 |

## R01–R07：未闭合部分与修订回归

### R01 · P2 · C01 剩余，AMD 的修订又把驱动安装与用户态安装等同

- **位置**：正文 L84、L110、L125、L139–141。
- **证据与影响**：L2 通用表要求设备及驱动/固件版本，NVIDIA 平台行仍只给安装与节点语义。AMD 仍依赖装完用户态后的 rocminfo 回填早一层证据，且 L139 明说驱动和用户态“一并安装”。[ROCm 安装页](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html)的 Install the kernel driver 与 Install ROCm 是分开的步骤；Instinct/Radeon 的包管理器路径指向独立驱动安装，Ryzen 有 inbox 驱动条件，runfile 也有单独 amdgpu 目标。此来源不支持所有安装方式都一并安装驱动。
- **关闭条件**：按选择的安装方式分别定位内核驱动/固件身份、加载证据和用户态身份；缺证保持未完成，不让 L5 成功倒填各层全部条件。删除“一并安装”通则，区分独立安装、已有/inbox 驱动与安装器可包含驱动的场景。不要求补猜测命令或实际执行。

### R02 · P2 · C02 剩余：边界声明不能替代最小运算/同步方法

- **位置**：正文 L87–101、L113–114、L128、L141–142、L171–175。
- **证据与影响**：新增小节解释了样例不证明什么，却没有定义每个平台何时确认设备完成、检查哪些同步/异步错误、如何进行结果比对。正文“若验收需要计算正确性契约”使 acceptance 1 的结果检查可选；B0/N/R 又允许沿用该梯子给出通过。添加 vectorAdd 的 source_ref 也尚未把其方法接入该流程。
- **关闭条件**：无需在本篇填实际容差或实跑，但须给三平台各自可定位的方法入口及同步/错误/结果契约字段；明确尚未冻结契约时，L6/L7 或最终验收不能记通过。若由运行时篇承接，给对应章节并保留其版本差异，不能只写“独立验证轨道另行完成”。

### R03 · P2 · C05 修订回归：把所有 NVIDIA 回退写成 alternatives 切换

- **位置**：正文 L183；对照 L112/L189。
- **证据与影响**：L183 写“NVIDIA……回退是 update-alternatives 切换，不是重装”。[CUDA 12.8 §10.3.3](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-installation-guide-linux/index.html#select-the-active-version-of-cuda)只说明依赖 `/usr/local/cuda` 等软链接的应用可选择已安装版本；不覆盖显式版本路径、容器/框架所带 runtime、驱动与依赖恢复，也不保证替换了运行进程的实载库。这会削弱刚补上的按身份恢复要求。
- **关闭条件**：将切换限定为旧 toolkit 完整保留、依赖这些软链接的具体场景，并要求重建/重启相关进程及实载复核；驱动、其他安装方式和缺失制品按各自恢复路径处理。不能把 alternatives 当成整个 NVIDIA 栈的回退定义。

### R04 · P2 · C06 剩余且新增误读：仓库清理并非 unknown

- **位置**：正文 L191；registry L2673；取证 L12/L41/L52。
- **证据与影响**：[ROCm Uninstalling](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html#uninstalling)明确包含 Remove ROCm repositories 和清理缓存步骤，本轮网页转换坐标 L2670–2678、L2772–2796 即可定位；也有 venv/tarball/runfile 等分支。因此“完整版本回退、依赖恢复与仓库清理未见专门说明”把已知清理步骤与未知整套恢复合并。取证首轮表和 unknown 清单仍直接说无卸载章节，未明确标为被修订结论取代。
- **关闭条件**：三份材料一致区分已有卸载/仓库清理说明、旧流版本条件与仍未知的完整恢复能力；取证主张表和 unknown 清单同步更正，或明确标为废止历史记录并指向当前结论。无需复制或执行清理命令。

### R05 · P2 · C07/C09 剩余：正文已改，CANN 登记仍承载原错误

- **位置**：registry L7238；正文 L156/L190；取证 L11/L53/L55。
- **证据与影响**：registry 仍保留 `/firmware/script/uninstall.sh`、统一的 `ascend-toolkit/nnae/nnrt/<arch>-linux/script` 以及无安装关系限定的 Kernels 自动卸载。正文完整路径、NNAE 目录和条件句已经不同。初审与本轮读取的 0030/0032/0033 缓存支持正文这些修正，但不能替 registry 中仍然有效的错误作辩护。
- **关闭条件**：在取得可定位原页或可追溯原件的前提下逐包核对完整路径、安装方式和 Kernels 触发条件，同步当前 notes 与取证主张表；旧文字如需保留须标明已废止。远程不可读时如实保留证据限制，不能宣称已重新核实远端。

### R06 · P3 · C08 剩余：NVIDIA 仓库更正只落到正文

- **位置**：registry L7249；取证 L10/L54；正文 L110–111。
- **证据与影响**：正文已区分 `nvidia-driver-local-repo-...` 与 `cuda-keyring`，但 notes 和主张表仍写“local/network repo 两种 cuda-keyring”。[驱动 Ubuntu 页](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/ubuntu.html)的两种仓库路径不同；修订记录说已处理不能消除有效登记中的误述。
- **关闭条件**：当前 notes、主张表与正文分别描述 local/network，保留 CUDA 双模板冲突的准确记录；不为修复摘要而拼造新的完整命令。

### R07 · P3 · C12 剩余：补了来源身份，尚未补齐实际定位与有效记录

- **位置**：正文 L113、L154–159、L189–190/L210；registry L2963/L7233/L7238；取证 L9/L30/L58–59。
- **证据与影响**：master/bandwidthTest 本轮经连接器仍 404；另一个 vectorAdd 来源只在元数据出现，正文没有给可用的对应 bandwidthTest 固定位置。固定 12.8 的[bandwidthTest README](https://github.com/NVIDIA/cuda-samples/blob/db3eea23946bca2e90a75eca2b5b3e07158a9e11/Samples/1_Utilities/bandwidthTest/README.md)实际可读，但不能据此算作正文已完成定位。CANN revision 加了 0094，notes 却没有该页配置/依赖/样例的核读内容；CUDA notes 仍没有正文引用的 §10.3.3。升级/回退处若只写“升级 CANN 节”或“升级前必读”，还需明确对应登记及页号。取证 L9 继续以“本轮新增”登记已删除的 ID，虽然 L59 可追踪更正，但现行表与历史表未分清。
- **关闭条件**：为所选样例提供实际可定位的版本入口，记录相应来源范围；notes 与宣称核读内容一致；升级/卸载主张就近明确来源和具体章节/页号；取证表明确当前身份与历史更正。06/07 恢复链接和 AMD commit 钉扎已经完成，无需为本项改写兄弟正文。

## 来源修改抽查与检查结果

- **删除与合并**：registry 共 577 项，无重复 ID；同一 CUDA 安装指南 URL 仅一项；17 个正文 source_refs、9 个 related ID 及 verification 引用存在，删除没有制造正文/路径页的悬空来源 ID。初审报告中的旧 ID 属历史事实，本轮不要求改写初审报告。
- **URL 钉扎**：ROCm 带宽工具的正文和 registry 均为 `tree/d7f5efe854b82baa21f34a978841e341de354b97`；GitHub Git commit 接口确认 SHA 相同，tree 为 `d345ecce701dc2c38b0790e4b0f8a2d82b4cd35c`。本项已实现，未扩展复审其整套工具。
- **许可**：本轮合并后的 CUDA 来源保持归档 EULA URL 与保守使用边界；没有因删除重复登记而新增许可声明。本轮不重新审查未变的所有许可证。
- **结构检查**：正文 schema/日期通过，20 处本地链接均存在；`PYTHONDONTWRITEBYTECODE=1 make check` 通过：127 content entries / 577 sources。结构检查不能发现上述有效 notes 的语义冲突。
- **写入核对**：本轮开始时为 681 个 Git 已登记及未忽略文件记录摘要；交付时核对原文件未改变，仅新增本报告。正文仍为 210 行及表中 SHA-256。未运行会写 `build/` 的 `make build`，未修改 `src/kb/`，未运行 `make test`。

**T02-12 仍待修订与再次定向复核。** 后续仅需按 R01–R07 及相应未关闭 C 项补齐；不重开已关闭的原问题，除非后续修订引入直接回归。正文继续为 `draft / source_checked`；本次没有真实安装、升级、卸载或恢复证据，模型复核不替代独立验证轨道。

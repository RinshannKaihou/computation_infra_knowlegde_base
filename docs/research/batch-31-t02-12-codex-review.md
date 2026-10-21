# Batch 31 · T02-12 初审报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 审阅角色 / 轮次 | 独立批次审阅者；第一轮初审；本会话只审阅、只写报告，不承担正文编写或问题修订 |
| 实际执行模型 / 档位 | `gpt-6.1-sol / xhigh` |
| 核验方法 | 定位包含本次完整审阅请求、开始时间与工作目录相符的当前 rollout，读取最新 `turn_context`；交付前再次读取；不以模型配置默认值、工具引文或其他会话代替 |
| 核验结果 | `model=gpt-6.1-sol`、`effort=xhigh`、`cwd=/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 嵌套设置 | `collaboration_mode.mode=default`；`settings.model=gpt-6.1-sol`、`settings.reasoning_effort=xhigh`、`settings.developer_instructions=null`；与顶层一致 |
| 核验坐标 | `/Users/ywang2397/.codex/sessions/2026/10/22/rollout-2026-10-22T00-32-09-01a15f4e-4bcb-7a12-be50-b0ed78c23a91.jsonl` L8，ordinal 7，时间戳 `2026-10-21T16:32:16.475Z`；会话 ID 另见该文件 L1 |
| 会话 ID / turn ID | `01a15f4e-4bcb-7a12-be50-b0ed78c23a91` / `01a15f4e-4cc4-7723-81a0-f7a1d405ba50` |
| 身份结论 | 本地 Codex CLI 当前会话直接审阅；未另启审阅模型或子代理；本轮元数据未显示回退。写作指南 §7 引文中的 `[frontier_llm]` 是被引用的规则文字，不作为回退证据 |
| 日期 / 时区 | 2026-10-22 / Asia/Shanghai；上述 UTC 时间对应本地 00:32 |
| 审阅正文 / 基准 | `knowledge/02-software-stack/environment-installation-and-upgrade.md`；开始前执行 `wc -l`，156 行 |
| 正文 SHA-256 | `86c2961953fc4c36280745a05166d0f1834a40d677756fb9dcdf61e69f7e13a8`（开始前 `shasum -a 256`；交付前复核一致） |
| 写入范围 | 仅新增 `docs/research/batch-31-t02-12-codex-review.md`；不修改正文、取证记录、来源、导航、计划或构建产物 |

**初审结论：需修订并定向复核，暂不通过。共 13 项开放发现：P1 0 项、P2 10 项（C01–C07、C09–C11）、P3 3 项（C08、C12–C13）。** 主要缺口为七层方法与平台步骤未逐项闭合、迁移缺少完整改变项和三状态对照、回退前置门槛与制品保全不足，以及来源误读和导航提前宣告闭环。未执行真实安装的声明本身正确；本报告不要求以实测关闭文档问题。

优先级：P1＝足以严重误导处置的关键错误；P2＝影响技术准确性、证据边界或验收判据的必修事项；P3＝局部措辞、定位与可追溯性问题。正文行号均以上述摘要为准，其他文件另行指明。

## 范围与方法

先读 `README.md`、`AGENTS.md`、[写作指南](../authoring-guide.md)（元数据、操作条目、来源和 §7）、`schemas/content.schema.json`、`content-outline.md` 的 02 域。完整重读[正文](../../knowledge/02-software-stack/environment-installation-and-upgrade.md)及[取证记录](batch-31-t02-12-sources.md)，以 [T02-12](../../plans/full-coverage-backlog.yaml) L7215–7269 的 objective 和四条 acceptance 为基准。报告结构参照 [Batch 30 T08-05](batch-30-t08-05-codex-review.md)。

检查 15 个 `source_refs` 的 URL、revision、license、notes，三条新增登记和 ROCm 既有条目的本批补读；逐项核对正文中的命令、包名、路径、回显及条件。核对 02 首页的 related ID、阅读顺序 14、02.7 入口；相邻正文只读取本篇调用的方法边界。06/07 首页及 T06-09/T07-12 闭环不在范围内，未重审其报告或作出评价。

### 上游读取与证据强度

| 对象 | 本轮核查范围与限制 |
|---|---|
| CUDA 12.8 安装指南 | 直接读取[登记归档页](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-installation-guide-linux/index.html)：§2、§2.6、§3.12.2/3.12.3.7、§5.4、§10.2.2、§10.3.3、§11。章号主干正确；包名模板存在页内冲突，见 C08 |
| NVIDIA 驱动指南 | 直接读取[登记目录](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/index.html)、[Ubuntu](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/ubuntu.html)、[version-locking](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/version-locking.html) 及 Notices。当前目录自述 branch 615；575/580 是锁定章节示例，不能解释为整份指南的版本 |
| CUDA 样例及容器 | 正文 master/bandwidthTest URL 经网页和 GitHub 连接器均返回 404；另用连接器读取 `v12.8` 的 deviceQuery.cpp、bandwidthTest.cu。tag 解析为 `db3eea23946bca2e90a75eca2b5b3e07158a9e11`，源码行号按原文计数。直接读取[容器指南](https://docs.nvidia.com/deeplearning/frameworks/user-guide/index.html) §4、§10，确认宿主驱动/容器边界 |
| NVIDIA 兼容及 README | 直接读取 forward/minor compatibility 可变页；固定 580.105.08 README 本轮远程不可读，设备文件语义仅与登记 notes 比对，未冒称重新核实该 README 全文 |
| CANN 安装/升级/卸载 | 精确尝试静态 `instg_0027`–`0033`、`0094`、`0098`、场景页，以及 document/detail 的 quick、0028、PyTorch 720 insg_0001/0002。静态页不可访问，动态页超时或仅返回站点导航；本机 urllib 亦 DNS 失败。随后读取本机既有 `cann-*.html` 辅助比对，摘要见下表。未重新下载，未证明缓存与当前服务器逐字相同，也未由缓存证明页头版本 |
| ROCm 10.1 | 直接读取[安装页](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html)的方式对比、权限、安装、验证和卸载；读取 release notes 与许可页。兼容矩阵本轮不可读，MI300X 条件块只与登记 notes 比对，不据此重新确认具体硬件/OS 支持 |
| ROCm 带宽工具 | 连接器读取登记 commit `d7f5efe854b82baa21f34a978841e341de354b97` 的 README；这是 RBT-NG 插件式传输工具，正文没有选择插件、测试输入或结果契约。读取 7.2.4 prerequisites，未将其整个版本的安装规则套用到 10.1 |

CANN 缓存仅为辅助材料，未复制到仓库。本轮实际读取文件的 SHA-256 如下；`0027`、`0031` 为章节导航，`0098` 为安装指南目录，不能单独证明命令语义。

| `/private/tmp/` 下文件 | SHA-256 |
|---|---|
| `cann-0027.html` | `726022c9785ec5b74d1e195f363ef736c617c22d695dea615e0532a3a093a40b` |
| `cann-0028.html` | `7b3509b601d1b0030b185c6341e548f0f3c869a057d2431baf3ce8bfd6feef2b` |
| `cann-0029.html` | `edf3f4eed2c3eab9644c3b1794aba8c3662e3c872cb02780eb286a6e267c193c` |
| `cann-0030.html` | `39d8c94980ba3a665a7323dbe12d1cc8106686c0cb65b373d6b7e11d32f3d3b0` |
| `cann-0031.html` | `6033095e3bbc4a55ad9ea84d876e65e78d0d12d19d972177ef3f78901842d29d` |
| `cann-0032.html` | `81290adefa2fda0c7178a738a49c4f9977c893bb8babd8afa45d20c4706a338e` |
| `cann-0033.html` | `258fc1a3d7c302e6750affe5079d4da4aac56032659366abb502d181048af378` |
| `cann-0094.html` | `2a3f6534364d604a05c1cf0b831e1b424f88f03d951d7b0a816c79732303eb2e` |
| `cann-0098.html` | `d62a41a83bd5061d0d6771c601d97881a9f27c42374df3c91c0ae35322030021` |
| `cann-quick.html` | `e1c43780f720bbd40d9124a803bba3386ea74b4bedb1f37f42241e880bce0128` |
| `cann-toc.html` | `a057d7326d1baa57186018b1caf7d3585999b6b92bdcad3c162d210a5e13f495` |

## 已核实的主链与边界

| 对象 | 核对结论 |
|---|---|
| 任务与所有权 | 主归属 02.7 正确；框架执行与引擎验证可由 06/07 正文承接，但本篇仍须记录它们的变更身份、检查层和停止门槛 |
| 元数据 | `procedure` 必填的 applicability/verification 齐备；Draft 2020-12 schema 与日期格式通过；15 个来源、9 个 related ID、4 个 evidence ID 均存在；16 处本地链接目标均存在 |
| 文档/实测分离 | `draft / source_checked`、空 environment_refs、未实跑声明和 V00 独立轨道一致。V00 当前 planned、资源/授权/实例未填、executed_at 为空；没有实际安装成功证据 |
| 平台差异 | L53 明确 `generic` 只表示方法结构；NVIDIA latest 与固定 README 分立，CANN 8.3.RCX/83RC1 标识差异保留，AMD 选择器视图与观察日期没有被写成不可变环境 |
| NVIDIA 有依据的命令 | `cuda-toolkit-12-8`、`apt install nvidia-open`、`apt dist-upgrade`、版本锁包、`update-alternatives`、`cuda-uninstaller`、§11 清理命令均有上游位置；存在不等于可无条件执行，具体包名模板/仓库描述见 C08，保全边界见 C05 |
| NVIDIA 验证与降级 | §10.2.2 确实使用 deviceQuery/bandwidthTest，提设备节点和 SELinux；正文没有把 `nvidia-smi`/`nvcc -V` 伪造成该节验收命令。锁包降级及 Debian 580.103→570.199、57 包示例可核；Ubuntu 跨分支限制也存在，不能由 Debian 示例外推 |
| CANN 可比对主干 | notes 与缓存均有高→低须卸载重装、固件→驱动→CANN、业务中断、升级后配套复查、磁盘条件、`.run --upgrade`、reboot 和 `npu-smi info`。远程重新核读仍有缺口；路径与 Kernels 限定有差异，见 C07/C09 |
| CANN 安装片段 | Conda 包坐标、Yum 示例包名、`.run --install`、set_env.sh、g++、protobuf/numpy 约束及 top1–top5 示例与所读缓存相符；省略号与 `.run` 片段不是完整可复制命令，也不能证明特定实际安装目录已存在 |
| ROCm 安装片段 | `amdrocm10.1`/`amdrocm10.1-gfx942`、video/render、udev 文件、`gpu-access=user/all`、`rocminfo`、`amd-smi version`、pip 验证有直接来源；7.2.4 及更旧须先卸载的条件也存在。否认卸载章节的新增记录错误，见 C06 |
| 许可边界 | 新 CANN/NVIDIA 驱动条目没有宣称取得再分发授权；驱动指南 Notices 与保守使用口径相容。CUDA 归档 EULA 可定位，但新条目链接仍指当前 EULA；ROCm 文档许可页顶部 MIT 可核，未推广到所有组件。来源身份细节见 C13 |

### 七层与 acceptance 1 的对应

| 层 | 当前对应情况 | 尚缺内容 |
|---|---|---|
| L1 硬件/OS | 三平台均有支持入口，Ascend 具体组合保留 unknown | 将查不到直接定为不支持不准确（C10）；缺失交集时停止须显式执行（C04） |
| L2 固件/驱动 | Ascend 有 npu-smi 前置；NVIDIA 有安装/节点语义；AMD 将 L2/L3 合并 | NVIDIA/AMD 缺少独立、先于用户态安装的版本/加载核查闭合，不能只靠后面的 runtime 结果反推（C01） |
| L3 用户态库 | 有包名和配套要求 | 通用“包管理器登记”不能覆盖 runfile/tarball 等方式；须记录对应制品身份（C01/C05） |
| L4 实载路径 | NVIDIA/Ascend 配环境；AMD 配权限 | 三者均未给运行进程实载库身份判据；AMD 本行属于设备访问（C01） |
| L5 后端初始化 | CUDA 样例、CANN 推理样例、HSA 枚举均可提供各自层级信息 | 应标清 runtime/框架覆盖范围，不能由驱动可见反推框架可用（C01/C02） |
| L6 最小算子/同步 | 有推理或传输样例入口 | 未形成三平台明确的最小运算、完成同步/错误检查方法；CUDA 带宽样例存在同步，不等于有数值校验（C02） |
| L7 结果 | CUDA PASS、Ascend top5 形态、AMD 规格/文档对照 | 缺选定输入/预期值或逻辑结果契约及无法判断分支（C02） |

## 逐项发现

### C01 · P2 · 七层的通过判据不能证明所命名的层已完成

- **位置**：正文 L65–77、L86–89、L101–104、L115–117。
- **问题**：L4 以环境脚本/变量指向某版本作为进程“实际加载”正确的判据；AMD L4 甚至只有组与设备权限。搜索配置和设备访问都不能证明进程实载库。L2 NVIDIA 只有安装/设备文件语义，AMD 与用户态安装合并，未分别核对固件/驱动身份与加载状态；L3 的包管理器判据也覆盖不了本文列出的其他安装方式。后续 runtime 样例不能倒填“依次逐层通过”。
- **证据**：本文已链接的[运行时与库装载](../../knowledge/02-software-stack/runtime-execution-and-library-loading.md)“动态链接失败”表（L289 起）明确区分解析与实载；安装指南的环境配置没有提供这种等价保证。设备文件存在也不等于全部驱动条件已满足。
- **关闭条件**：三平台逐层列清所需证据、可证明的状态与缺口；L4 关联实际运行进程及其库文件/版本身份，无法采集则未完成；各安装方式采用适合的制品/安装身份记录。可引用已有方法，无需添加猜测命令或实跑。

### C02 · P2 · 样例运行/输出形态代替了最小运算、同步与结果契约

- **位置**：正文 L74–75、L89–90、L104、L118。
- **问题**：NVIDIA 只选枚举与传输带宽样例；Ascend 只要求 top1–top5 形态；AMD 只有工具名和“与规格核对”。没有逐平台定义最小运算、何时确认设备完成、检查哪些返回/异步错误，以及固定输入对应的预期数值或逻辑结果。形态正确或出现带宽数值，仍可能未验证所需计算结果。
- **证据**：[CUDA v12.8 bandwidthTest.cu](https://github.com/NVIDIA/cuda-samples/blob/db3eea23946bca2e90a75eca2b5b3e07158a9e11/Samples/1_Utilities/bandwidthTest/bandwidthTest.cu#L129-L153) L138–153 的 PASS 由 runTest 返回决定；L384 正常路径返回 0，传输函数有同步（如 L634/L834），但没有逐元素数值比较。CANN 0094 缓存仅展示示例输出；[RBT-NG 固定 README](https://github.com/ROCm/rocm_bandwidth_test/blob/d7f5efe854b82baa21f34a978841e341de354b97/README.md) 的插件式传输入口不能自行给出本文未定义的计算正确性判据。相邻运行时篇已将“运算→同步→结果比对”分开。
- **关闭条件**：三平台各有可定位的最小运算/同步/结果检查方法及覆盖边界；区分样例自带校验、单纯打印/性能测量和需另行定义的比较环节；样例/输入/预期结果未冻结时保持未完成或无法判断，不强行给出安装通过。

### C03 · P2 · 变化矩阵缺 hardware、独立 framework/library 身份和 baseline/变化/恢复对照

- **位置**：正文 L122–135。
- **问题**：矩阵没有硬件改变行；framework 与 backend 混成一行，library 仅被压成“随 toolkit”或“随 ROCm 包”，没有独立库版本/构建身份。engine/model/config/input 虽被提到，只有一句上层矩阵提示。全表没有记录变更前 baseline、目标变化和恢复状态，更无三者使用相同负载/判据进行对照的方法。它目前是升级提示表，未实现 acceptance 2 的变化审计。
- **证据**：T02-12 acceptance 2 明列 11 类改变项及三状态对照；objective 要求按制品/环境身份构造矩阵。已有[兼容证据方法](../../knowledge/02-software-stack/compatibility-evidence.md)要求同一制品、构建变体与目标负载，不能只沿用平台总版本。
- **关闭条件**：hardware/OS/driver/runtime/library/framework/backend/engine/model/config/input 均可独立登记改变或明确不变，记录约束来源与重检层；定义 B0/N/R（名称不限）的身份、固定输入、判据、证据及比较方式。可交付待填写方法表，不要求伪造实际 baseline。

### C04 · P2 · “无交集/无基线/无回退即停止”及数据不可逆边界未落成门槛

- **位置**：正文 L65、L69、L120、L139–145、L149。
- **问题**：现有停止句主要针对命令失败；没有在执行任何变更前明确拦截完整依赖交集缺失、有效 baseline 缺失、恢复路径未落实。ROCm 要“自行落定”、固件要“向支持确认”，仍未说明确认失败必须停止。不可逆小节只谈固件，遗漏数据/格式/状态变化；恢复“至少 L2/L5/L6/L7”也没有要求按实际改变重查 L1/L3/L4 并与原 baseline 对比。
- **证据**：acceptance 3 对这些门槛有明确要求；V00/V01 也将制品、输入、判据、恢复与有效版本交集分开，不能仅以指向相邻概念篇的链接代替本 procedure 的决策分支。
- **关闭条件**：变更前给出可判定的准入/停止分支及所需记录，三类缺项均停止实际变更；明确固件与数据/模型转换/状态格式的可逆性、备份或不适用依据；恢复按全部受影响层及冻结的 baseline 判据验收。首次安装应界定安装前状态和清理恢复目标，不虚构已运行基线。

### C05 · P2 · 制品保全与全量卸载混在同一回退路径

- **位置**：正文 L141–142。
- **问题**：保留一个版本化元包/安装目录不等于保留可恢复的完整制品与依赖。紧接着列 CUDA 全通配 purge，会同时匹配并列旧版；它不能未经区分就作为保留旧 baseline 的回退操作。CANN“旧版本目录仍在”的确定性承诺也不能从“默认升级 latest 指向版本”推出；所列升级 notes 没有给出旧目录不被改写的保证。
- **证据**：[CUDA §11](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-installation-guide-linux/index.html#removing-cuda-toolkit) 的清理模式不限定单一版本；§2.6 另有按包名卸载入口。CANN 0028 缓存及 registry L7238 只说明升级目标，不支持“旧版完整保留”的推论。此处关于通配删除范围的判断为命令语义推断，未实际执行。
- **关闭条件**：保全对象包含准确版本/变体/摘要、依赖、仓库或镜像及配置/数据；区分全量卸载和保留旧版的恢复路径，说明卸载影响集与外置保全条件；删除或补证 CANN 旧目录保证。无需实际下载或安装制品。

### C06 · P2 · ROCm“无专门卸载章节”与原页及既有登记冲突

- **位置**：正文 L120；取证记录 L12/L41；registry `src.amd.rocm-install-docs-10.1.0` L2673 的 Batch 31 追加段。
- **问题**：新增记录否认卸载章节，而相同条目的既有 notes 已记录 apt 卸载命令。本轮原页目录及正文均有独立 Uninstalling，涵盖多种安装方式。缺少完整版本回退保证不能被写成没有卸载说明。
- **证据**：[安装页 Uninstalling](https://rocm.docs.amd.com/en/docs-10.1.0/install/rocm.html#uninstalling)（本轮页面转换坐标 L2623 起）明确列包管理器移除和仓库清理，并另列 venv/tarball 等方式。既有 notes 的记录构成仓库内独立冲突；本轮未据当前页面反推新增章节出现时间。
- **关闭条件**：正文、取证与 notes 一致区分已有卸载步骤、旧流升级前卸载条件和仍未知的完整降级/依赖恢复能力；按所选安装方式定位，保留真正未知项，不因有卸载步骤宣称回退成功。

### C07 · P2 · CANN 固件卸载绝对路径被截短，脚本路径概括也不精确

- **位置**：正文 L143；registry L7238；取证记录 L11。
- **问题**：正文写 `/firmware/script/uninstall.sh`，这是从根目录开始的另一路径；缓存中为 `/usr/local/Ascend/firmware/script/uninstall.sh`。路径不能用这种缩写表达共同前缀。把所有 CANN 脚本统一说成安装目录 `script/` 也隐去了 Toolkit/NNRT 的版本及架构目录、NNAE 的不同结构、NNAL 的 `scripts/`。
- **证据**：本轮读取的 `cann-0033.html` 原文件 L12 与 `cann-0032.html`“脚本卸载”段。对应[0033 原页](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0033.html)本轮不可读；本项确认的是正文/登记与所留存材料的具体不一致，未声称已重新核实远端原件。
- **关闭条件**：取得可定位的对应版本原页或可追溯原件，逐包核对完整路径并修正正文/notes；若不提供完整路径则只给精确章节入口，不能保留貌似可执行的错误绝对路径。配置文件 Install_Path 与当前安装身份也须对应。

### C08 · P3 · CUDA 包名模板的上游冲突未记录，驱动仓库说明混淆

- **位置**：正文 L86–87、L130/L141；取证记录 L9–10；registry L7252/L7263。
- **问题**：反复将 `cuda-toolkit-X.Y` 当作元包通用名称；该点号形式确实出现在上游并列安装句中，因此不能指为本库凭空编造，但同节锁定句使用 `cuda-toolkit-X-Y`，具体表列 `cuda-toolkit-12-8`。需显式区分上游模板矛盾与可用包坐标。local/network“两种 cuda-keyring”概括亦不准确。
- **证据**：[CUDA §3.12.3.7](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-installation-guide-linux/index.html#other-package-notes)存在两种模板；[驱动 Ubuntu 页](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/latest/ubuntu.html)的 Local Repository Enablement 安装 `nvidia-driver-local-repo-...` 并复制 keyring，Network 才安装 `cuda-keyring` 包。
- **关闭条件**：优先使用已明确的具体包坐标或区分版本号/包名模板；记录上游不一致，不能把点号模板当实测可安装包。local/network 的包及公钥处理分别描述；不补造完整安装命令。

### C09 · P2 · CANN Kernels 自动卸载的前提被删去

- **位置**：正文 L131；取证记录 L11；registry L7238。
- **问题**：加粗句把 Kernels 随 Toolkit/NNAE/NNRT 升级自动卸载写成无条件规则。留存文档分别限定“跟随对应软件包安装后”；同段又承认独立升级，不能据此对所有 Kernels 安装布局作同一结论。
- **证据**：[instg_0030](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/83RC1/softwareinst/instg/instg_0030.html)对应缓存原文件 L34–36 的三条提示有此安装关系前提。远程读取限制同 C07，不能将缓存比对称为当前服务器全量核验。
- **关闭条件**：保留对应安装关系、方式/版本和“按需重装”的条件；独立安装/升级场景按来源与实际制品依赖另判，未知时不外推。正文、取证和 notes 同步。

### C10 · P2 · 查不到支持证据被记成“不支持”

- **位置**：正文 L69、L100、L149。
- **问题**：L1“查不到按不支持处理”将证据缺失与官方否定合并；Ascend 又承认具体组合结果未取得，容易把抓取失败记录成平台不支持。保守停止是正确动作，但官方状态仍应保留 unknown。
- **证据**：本文所引[兼容性证据方法](../../knowledge/02-software-stack/compatibility-evidence.md) L141–142 明确：只有来源说明表格是封闭全集，缺席才可按其规则解释为不支持；否则为 unknown。
- **关闭条件**：把操作门槛与证据状态分开：unknown/conflict 均不放行，但仅有明确否定或封闭表规则时才标 unsupported；各平台停止记录保留缺失字段及待补来源。

### C11 · P2 · 02 首页在第一轮初审前已宣告本任务审阅闭环

- **位置**：`knowledge/02-software-stack/index.md` L60（阅读顺序 14）。
- **问题**：写为“gpt-6.1-sol/xhigh 审阅已闭环的 draft”，与本次明确的第一轮初审及开放发现矛盾。这虽未冒称实测，却会使读者跳过修订与定向复核。
- **证据**：开始审阅时该句已经存在；本轮任务定义与取证记录末尾均尚待初审。写作指南 §7 要求修订后定向复核，才能关闭发现。
- **关闭条件**：导航如实记录初审/待修订状态；日后只有可定位的同一审阅者复核结论才能改成闭环。related ID、阅读入口与 02.7 登记保留；本报告不修改导航。

### C12 · P3 · 升级/回退缺少就近来源，0094 的登记核读范围未对应

- **位置**：正文 L128–145/L152；取证记录 L30；registry L7233/L7238；正文 L16–23/L116。
- **问题**：安装表有来源列，升级矩阵和回退各条却没有直接来源页/章号；“全部已随表格定位”的 L156 不成立。取证称 0094 随新增 CANN 条目登记，但该条目 revision/notes 没有 0094；正文引用的 7.2.4 prerequisites ID 也不在 source_refs。NVIDIA 样例入口目前 404，AMD 的“固定 commit”只链可变根页；06/07 恢复入口仅写域名与概称。
- **证据**：逐段链接及登记核对；CANN 新条目仅列 0027–0033，CUDA 新条目也未记录正文使用的 §10.3.3。原页不可访问不证明技术结论错误，但不应继续宣称所有定位均完整。
- **关闭条件**：升级/卸载/回退主张就近指向相应已登记来源的具体章节；notes 与实际核读范围一致，补齐真实依赖；样例固定版本可定位，跨域验证/恢复给具体正文入口。未读页面继续注明缺口。

### C13 · P3 · 同一 CUDA 安装来源再次分配 ID，许可链接未固定到归档

- **位置**：registry L2950–2963 与 L7239–7252；正文 L9/L42；取证记录 L9。
- **问题**：`src.nvidia.cuda-12-8-installation-guide-linux` 已登记相同 CUDA 12.8 URL，本批再建 `src.nvidia.cuda-128-install-guide-linux`，只是核读范围不同，未说明两个身份的必要性。全表没有字面重复 ID，但形成同一版本来源的双身份。新增条目称归档文档条款，license.url 却指当前 EULA。
- **证据**：两个来源 URL 完全相同；[12.8 归档 EULA](https://docs.nvidia.com/cuda/archive/12.8.0/eula/index.html)可直接读取，标日期 2025-01-07。公开可读与具体制品再分发权限仍须分开，不由本报告新增授权解释。
- **关闭条件**：复用稳定既有身份补充核读 notes，或给出明确的版本/作用域差异与对应关系，避免继续制造平行来源身份；许可入口定位所用归档或明确当前/历史差异，保留保守使用边界及历史引用可追踪性。

## 四条 acceptance 的逐条判断

| 条款 | 覆盖与边界 | 初审判断 |
|---|---|---|
| 1 · 硬件/OS→固件/驱动→用户态→实载→后端→最小算子/同步→结果；平台来源分别定位，无猜测命令 | 七层标题齐，主要命令名有来源；真正实载、分层先后及最小计算结果方法尚未闭合；固件路径与包名/样例定位有差异 | **部分满足**；C01/C02/C07/C08/C09/C10/C12 必须处理 |
| 2 · 11 类改变项、约束、baseline/变化/恢复及检查层 | 有三平台约束提示和检查层列；缺 hardware 等独立身份与三状态对照 | **未满足**；C03，配套 C12 |
| 3 · 制品保留、依赖一致性、固件/数据不可逆、恢复门槛与授权；无交集/基线/回退即停止 | 有授权声明、高→低卸载重装、固件 unknown 和恢复提示；无统一准入拦截，数据边界缺失，保全与全量清理冲突，ROCm 来源误读 | **部分满足**；C04/C05/C06/C07/C09/C10 |
| 4 · 三平台所选样板方法、未宣称实装成功、实际记录由独立轨道承接 | 三平台均有入口；元数据与 V00 分离正确，无本库实跑成功声明；方法覆盖仍受前述问题限制 | **文档/实测分离满足，三平台完整方法尚不满足**；C01/C02/C12；导航审阅状态另见 C11 |

## 校验、写入与结论

已执行 `PYTHONDONTWRITEBYTECODE=1 make check`：**PASS，127 content entries / 578 sources**；另独立核对 schema、ID、日期与本地链接。检查只证明结构，不证明远程页面、技术正确性或平台适用性。未运行 `make build`：它会写入 `build/`，与本轮“只新增报告”的明确写入范围冲突；未改 `src/kb/`，无需 `make test`。

初始工作区已有 02/06/07 首页、backlog、registry 修改及本批正文/来源与两项其他审阅文件；本会话未修改它们。唯一仓库写入为本报告。正文保持 156 行及同一 SHA-256；本轮没有运行任何安装、升级、卸载、驱动查询、固件操作或 GPU/NPU 样例，也未产生恢复成功记录。

**T02-12 暂不通过，交回编写者修订。** C01–C13 按各自关闭条件修订后，由同一审阅者定向复核；当前不能以导航的“已闭环”声明代替复核。CANN 原页、NVIDIA 固定 README、MI300X 条件块的本轮读取缺口继续如实保留；缓存/notes 比对不升级为独立远程核验。来源核对、编辑审阅与真实环境验证分别记账，实际记录继续由独立验证轨道承接。

---
id: software-stack.compatibility-evidence
title: 如何判断版本配套是否有依据
type: reference
domain: software-stack
status: draft
platforms: [generic]
source_refs:
  - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
  - src.nvidia.pytorch-container-25.01-release-notes-2026-09-30
  - src.nvidia.frameworks-support-matrix-2026-10-09
  - src.huawei.cann-83rcx-version-compatibility-2026-10-09
  - src.pypi.torch-npu-2.6.0.post3-2026-10-09
updated_at: "2026-10-09"
summary: 用两条独立证据轴判断软件栈版本配套，区分官方发行声明、源码分支范围、项目测试声明和限定环境中的本地验证，并给出平台档案的读取与变化审计规则。
related_ids: [software-stack.layers-and-boundaries, software-stack.ascend-documented-profile, software-stack.nvidia-documented-profile, software-stack.runtime-execution-and-library-loading]
verification:
  status: source_checked
  evidence_refs:
    - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
    - src.nvidia.pytorch-container-25.01-release-notes-2026-09-30
    - src.nvidia.frameworks-support-matrix-2026-10-09
    - src.huawei.cann-83rcx-version-compatibility-2026-10-09
    - src.pypi.torch-npu-2.6.0.post3-2026-10-09
  notes: "已核对 TorchNPU 官方 annotated tag 解引用 commit 中的英文版 README.md 与 version.txt 的文件存在性和版本含义，并确认该快照没有 COMPATIBILITY.md/COMPATIBILITY.en.md；2026-10-09 补充平台档案读取与变化审计规则（制品四层区分、页面审计三件套、documented/unknown/未实测规则），规则实例取自第十五批取证记录；未在 GPU/NPU 环境安装或运行，source_checked 不表示任何组合已在本仓库复现。"
---

# 如何判断版本配套是否有依据

## 范围与结论形式

本文回答的是：当有人声称一组驱动、运行时、框架、插件或上层项目“兼容”时，怎样判断这句话的依据覆盖了哪些对象和条件。组件边界见[主机到模型执行的软件栈分层](layers-and-boundaries.md)；具体昇腾版本档案见[昇腾软件栈的文档配套档案](ascend-documented-profile.md)。

兼容性结论必须同时保留两条轴，不能压缩成一个从弱到强的证据等级：

1. **官方声明轴**：`supported`、`unsupported`、`unknown` 或 `conflict`。它回答供应方或项目是否在特定范围内明确声明支持。
2. **本地验证轴**：`passed`、`failed`、`not_run` 或 `inconclusive`。它回答指定制品、环境和负载在一次可追溯验证中表现如何。

例如，官方声明为 `supported` 而本地验证为 `failed`，需要调查环境、制品或测试覆盖，不能把失败直接改写成“官方不支持”。反过来，官方声明为 `unsupported` 或 `unknown` 而一次本地验证通过，也不能把结果提升为官方支持。推荐用二元结果表达：

> 官方声明：`unknown`；本地验证：`passed`（仅限所记录环境、制品和负载）。

## 四类常见依据回答什么问题

| 依据 | 可以支持的判断 | 不能据此推出 | 必须保存的定位信息 |
|---|---|---|---|
| 发行包的官方兼容矩阵或发行说明 | 指定产品版本、包版本与所列依赖版本之间存在官方声明的配套关系 | 同一源码仓库的任意分支、未列出的硬件/OS/特性、其他上层项目也受支持 | 发布产品与包的完整版本、包名和构建标记，矩阵的版本或固定修订、发布日期和适用说明 |
| 源码分支说明、`version.txt` 或构建配置 | 某个固定 commit 的源码预期适配哪些上游版本，或构建系统接受哪些依赖 | 已发布 wheel 与当前分支等价；源码能够在任意 CANN/CUDA、驱动和硬件上构建并运行 | 仓库、分支名、完整 commit、子模块 commit、构建选项、对应上游源码或包身份 |
| 单个项目的测试声明或 CI 结果 | 该项目在声明的测试范围和时间点检查过某些组合或功能 | 依赖链上的所有组件均获得厂商支持；未执行的模型、算子、精度、拓扑也通过 | 测试项目和 revision、测试配置、环境矩阵、用例范围、制品、日期、结果和已知跳过项 |
| 本地运行验证 | 记录的制品在记录环境中，对记录负载产生了记录结果 | 供应方作出支持声明；相邻版本、其他机器或更大规模负载同样成立 | 环境快照、制品摘要、测试输入和判据、时间、结果、日志或实验记录引用 |

依赖包元数据、安装器允许安装、进程成功启动、单个算子通过，都可以是辅助证据，但各自只覆盖相应阶段。它们不能单独证明整栈支持或目标训练/推理负载正确。

### 源码分支与发行 wheel：TorchNPU 固定快照示例

以下例子只解释证据对象，不构成本仓库的部署推荐或本地验证。TorchNPU 官方 annotated tag `v7.2.0-pytorch2.6.0` 解引用到 commit [`bc51ab84cc6f35c77aab1c59886e0ea43681a317`](https://github.com/Ascend/pytorch/tree/bc51ab84cc6f35c77aab1c59886e0ea43681a317)。该快照的英文 [`README.md`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md) 在不同位置记录了二进制安装包、源码分支和配套表：

| 对象 | 固定快照中的声明 | 能支持的判断 |
|---|---|---|
| 二进制安装包 | `torch-npu==2.6.0.post3`，配套表中对应 PyTorch `2.6.0`、CANN `8.3.RC1` | 这是该固定 README 对发行包配套的声明；仍需按实际 wheel 文件、架构和 Python ABI 固定制品 |
| 源码入口 | 源码构建段指向分支 `v2.6.0-7.2.0` | 这是获取和构建源码的分支身份，不能用分支名代替 wheel 身份 |
| 源码内版本 | 固定 [`version.txt`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/version.txt) 为 `2.6.0.post3` | 该 commit 声明的扩展版本与同一快照的二进制版本一致；它本身不证明某个本地构建等同官方 wheel |
| Python 范围 | 同一 README 的 PyTorch/Python 表为 PyTorch `2.6.0` 列出 Python `3.9.x`、`3.10.x`、`3.11.x` | 这是文档范围，不是本仓库对三个 Python 环境的实测结果 |

该历史快照不存在 `COMPATIBILITY.md` 或 `COMPATIBILITY.en.md`；因此这里以固定英文 README 的安装段和表格为主证据，不能用当前 `master` 中后来出现的兼容文件替代历史证据。即使同一快照中的版本相互一致，实际判定仍要记录下载到的 wheel 完整文件名、构建标记、摘要，以及硬件、固件、驱动和 CANN 补丁条件。

## 为什么依赖交集不能证明整栈支持

假设资料分别声称：

- 组件 A 支持 B 的某些版本；
- 组件 B 支持 C 的某些版本；
- 项目 D 测试过 C 的某些版本。

即使三个版本集合存在交集，也不能直接推出 A、B、C、D 的联合组合受支持。原因包括：

- 每份资料可能针对不同发行渠道、构建变体、硬件系列、OS、Python ABI 或日期；
- “支持 B”可能只覆盖某个 API 或功能子集，并不传递 B 对 C 的全部约束；
- B 的不同构建可能分别满足 A 和 C，集合交集却不存在同一个可安装制品；
- 上层项目的测试可能跳过某些算子、dtype、执行模式、拓扑或规模；
- 同一版本号可能对应不同 wheel 构建标记、容器摘要、补丁集或源码 commit。

因此，每条边只能证明它直接连接的对象与条件。整栈结论需要一份直接覆盖整组制品的官方声明，或一条逐边无冲突且由限定环境验证补强的证据链；后者仍应标为工程验证结果，而不是厂商整栈支持声明。

## 最小环境与制品身份

下表是判定前应填写的最小字段。字段不适用时写 `not_applicable`；未采集或来源没有说明时写 `unknown`，不能留给读者猜测。

| 类别 | 最小字段 | 为什么需要 |
|---|---|---|
| 判定对象 | 目标任务，训练/推理阶段，模型或最小负载，所需特性，dtype，执行模式，单机/多机和规模 | “能初始化”与“目标负载可用”不是同一结论 |
| 硬件 | 厂商、产品系列、准确型号、设备数量；涉及互联时记录拓扑 | 官方表可能只覆盖部分产品系列或规模 |
| 主机环境 | CPU 架构、OS 发行版和版本、内核、容器运行环境；ABI 相关时记录 libc | wheel、驱动和运行时可能受架构或 ABI 限制 |
| 设备底层 | 固件版本、驱动完整版本和构建、设备运行模式 | 仅记录“已装驱动”无法与支持表对齐 |
| 平台软件 | CUDA/ROCm/CANN 等准确版本、补丁级别、安装来源和组件清单 | 平台套件内部也可能存在独立组件版本 |
| 框架与适配层 | 框架、设备后端/插件、通信库、编译器或关键扩展的包名与完整版本 | 只写“PyTorch 环境”会丢失关键依赖边 |
| 二进制制品 | wheel/容器/安装包的准确名称、版本、构建标记、来源、摘要；容器记录不可变 digest | 同名版本可能来自不同构建或渠道 |
| 源码制品 | 仓库 URL、分支、完整 commit、子模块 commit、补丁/dirty 状态、构建选项 | 分支名会移动，源码构建不能由 wheel 版本代替 |
| Python 环境 | Python 实现与版本、ABI、直接相关包的完整版本和来源 | Python 与 wheel ABI 常是兼容矩阵的一部分 |
| 时间与证据 | 环境采集时间、测试时间、来源发布日期或 revision、来源访问日期 | 文档和 `latest`/`master` 会变化 |

## 平台档案的读取与变化审计规则

平台配套档案（[NVIDIA 软件栈的文档配套档案](nvidia-documented-profile.md)、[昇腾软件栈的文档配套档案](ascend-documented-profile.md)；AMD 档案另行建立，适用同一规则）在读取与更新时遵守以下规则。规则实例与冲突原文见[第十五批取证记录](../../docs/research/batch-15-profile-intersection-sources.md)。

### 制品身份的四层区分

「版本相同」在四个层次是不同断言，档案必须分别记录各层身份：

| 层 | 身份形式 | 示例 | 边界 |
|---|---|---|---|
| 构建源码 | 仓库 URL + 完整 commit（分支/tag 只作指针） | TorchNPU tag `v7.2.0-pytorch2.6.0` 固定到 commit `bc51ab84cc6f35c77aab1c59886e0ea43681a317`；release 页称 25.01 容器内含该版 PyTorch 完整源码于 `/opt/pytorch` | tag 可被重指；源码快照不证明发行 wheel 由其原样构建 |
| wheel / 安装包 | 完整文件名 + 摘要（sha256）+ 来源索引与取得日期 | PyPI `torch_npu-2.6.0.post3` 六个 wheel 及索引声明 sha256（2026-10-09 取得） | 索引声明值未下载比对即不代表内容核验；abi0/abi1 等文件名无标记的变体需要独立身份 |
| 容器层 | tag 只作指针；不可变身份是 manifest digest + 签名验证结果 | `nvcr.io/nvidia/pytorch:25.01-py3` 的 manifest digest 未取得，档案中标注 unknown，不以 tag 或 catalog 页 layer SHA 冒充 digest | tag 可被服务端重新关联 |
| 实载库 | 进程运行期实际映射进地址空间的库文件 | `/proc/<pid>/maps` 的 pathname 列核对实载身份；`ldd` 是解析时视图，`dlopen` 装载的库只出现在 maps | 「磁盘已安装」「链接解析到」「进程实载」「调用成功」是四个不同问题，方法与边界见[驱动初始化、运行时执行同步与库装载](runtime-execution-and-library-loading.md) |

### 页面变化审计

厂商文档页会回写日期或演进内容。每次引用可变页面，记录三件套：**页脚/元数据日期 + 观察日期 + 关键字段抽查结果**。已观察到的实例：

- NVIDIA release 25.01 页的页脚与 `nv-pub-date` 在 2026-09-30 登记时记录为「last updated 2026-09-08」，2026-10-09 复核时变为 2026-09-29；Support Matrix 与 Frameworks Containers User Guide 同为 2026-09-29。抽查的容器 Contents、驱动两段原文、`/usr/local/lib/python3.10/dist-packages/torch` 路径未变。
- CUDA minor-version compatibility 页（页脚 2026-09-09）在 2026-10-09 观察时已含 CUDA 13.x 行（2026-09-30 登记时未记录），CUDA 12.x 最低驱动 >=525 行未变。
- hiascend 文档树的页头版本口径可与 URL 路径段不一致（URL 含 `83RC1` 而表头为 `8.3.RCX`）；交互式「兼容性查询助手」与 JS 渲染页面静态抓取不可取结果，只能记录页面外壳与取得方式，查询结果不得代填。

页面变化只触发重核，不自动使旧结论失效：旧登记按当时的观察保留，新旧差异写进取证记录。

### 读取顺序与结论规则

1. **先固定制品身份，再读约束链。** 依次记录源码 commit、wheel 文件名与摘要、容器 digest 状态，然后读官方矩阵或 release 页的约束链，最后读可变补充页；每一步记录出处、定位与观察日期。
2. **交集有证据才 documented。** 只有同一官方来源（或同一发布主体同一版本列）明确给出的组合记为 documented；跨来源拼接、跨粒度（产品家族口径 vs 固定制品口径）的宽口径不能写进固定制品的组合。
3. **未覆盖列保持 unknown。** 硬件 SKU、精确驱动/固件版本、OS×机型组合、容器运行层精确版本等未覆盖列不补齐、不推测。当前实例：Ascend 档案的 CANN 8.3.RC1 精确驱动/固件交集处于**阻塞**状态——CANN 版本兼容性页只有 HDK 系列级通配（25.3.X/25.2.X/25.0.X/24.1.X/24.1.RC3），不得以系列通配冒充精确配套；该补齐子项在取得精确来源前不得标为已覆盖。
4. **冲突不拼成兼容。** 同一页或跨页的互斥声明（如 R545 驱动两段、Python 3.12 与 `python3.10` 路径、TensorRT Model Optimizer 0.21 与 0.17.1）双方位置同时保留，维持 `conflict`，等待同一发布主体的勘误或更高位证据；收窄性证据（如兼容包支持分支表）按其适用范围记录，不越界裁断。
5. **满足文档条件仍标未实测。** 档案即使在文档层面凑齐完整交集，本地验证轴仍为 `not_run`，verification 状态保持 `source_checked`，不转为 `reproduced`；`reproduced` 需要另行记录环境快照、制品摘要与验证证据。

## 人与 Agent 共用的判定步骤

1. **写出精确问题。** 用“制品 X 是否在环境 Y 中、为负载 Z 获得官方支持或本地验证”替代“这些版本兼容吗”。将“官方支持”和“本地能运行”拆成两个待回答问题。
2. **固定所有身份。** 先填写上表。任何会移动的名字，如 `latest`、`master`、未带 digest 的容器标签或只有主版本号的运行时，都不足以形成可复查结论。
3. **寻找直接声明。** 优先定位到供应方或项目的具体兼容表、发行说明、分支文件或测试说明。Git 来源保存固定 revision；版本化文档保存文档版本或发布日期；动态页面至少保存访问日期、精确章节及足以复核结论的合规摘要。搜索摘要、下载页标题或二手文章只用于发现来源。
4. **把声明拆成边。** 每一行只记录两个或少数几个明确对象之间的关系，同时抄录它的硬件、OS、特性和生命周期限制。不要先合成整栈结论。
5. **对齐同一制品。** 检查各条边是否引用相同包版本、构建变体、硬件系列、平台补丁和时间范围。仅有版本集合交集时，整栈仍为 `unknown`。
6. **检查否定和冲突。** 区分“来源明确说不支持”和“来源没有列出”。只有来源说明表格是封闭全集，缺席才可按其规则解释为不支持；否则缺席记为 `unknown`。
7. **分别给两轴结论。** 官方轴依据直接声明；本地轴依据实验或案例记录。没有授权或匹配环境时不运行测试，将本地轴写为 `not_run`。
8. **记录适用边界。** 结论必须带制品、环境、负载、日期和证据位置。任一关键字段变化都触发重新判断，而不是沿用旧结论。

## 决策表：已填的文档研究示例

下表演示人或 Agent 应怎样填写关系记录。它只整理固定 TorchNPU 文档，没有选择或下载实际 wheel，也没有目标硬件环境或本地运行结果。`官方判定` 使用 `supported / unsupported / unknown / conflict`，`本地判定` 使用 `passed / failed / not_run / inconclusive`。

| 关系或主张 | 左侧对象 | 右侧对象 | 直接来源与定位 | 附加条件/缺失项 | 官方判定 | 本地证据 | 本地判定 | 解释 |
|---|---|---|---|---|---|---|---|---|
| 发行包与框架配套 | 文档中的包坐标 `torch-npu==2.6.0.post3` | PyTorch `2.6.0` | 固定英文 README 的二进制安装段与配套表；commit `bc51ab84cc6f35c77aab1c59886e0ea43681a317` | 六个 wheel 的索引层身份（文件名/平台标签/sha256）已取得；未选择具体部署 wheel，下载字节、`METADATA` 与构建 commit/ABI 为 `unknown` | `supported` | `none` | `not_run` | `supported` 只表示该直接关系有官方文档声明，不表示某个本地 wheel 已确认 |
| 发行包与平台套件配套 | 文档中的包坐标 `torch-npu==2.6.0.post3` | CANN `8.3.RC1` | 同一固定 README 的配套表 | CANN 补丁、固件、驱动和硬件为 `unknown` | `supported` | `none` | `not_run` | 精确已列关系保留为 `supported`；缺失的下游条件另记 `unknown` |
| 框架与 Python 范围 | PyTorch `2.6.0` | Python `3.9.x`、`3.10.x`、`3.11.x` | 同一固定 README 的 PyTorch/Python 表 | 实际 Python、OS 和 ABI 为 `unknown` | `supported` | `none` | `not_run` | 文档列出的范围不等于三个环境均已在本仓库运行 |
| 完整运行栈适用性 | 上述文档对象 | 某个实际硬件、固件、驱动、CANN 补丁、wheel 与目标负载 | 没有直接覆盖完整对象的来源 | 实际制品与环境均未提供 | `unknown` | `none` | `not_run` | 直接关系有支持声明，不足以推出整栈结论 |

源码身份单独记录：本例固定 commit 的 `version.txt` 为 `2.6.0.post3`，README 的源码入口为 `v2.6.0-7.2.0`。这只是对象身份事实，不参与 `supported / unsupported` 判定；本地构建选项、子模块与产物摘要仍为 `unknown`。

将这个表用于新判定时，应复制字段结构到具体兼容档案、案例或实验并填写实际值；知识正文不保存未绑定对象的空白结论。

**整栈结论字段**

| 字段 | 填写要求 |
|---|---|
| 官方声明轴 | 给出状态；列出直接覆盖的边和仍为 `unknown` 的边 |
| 本地验证轴 | 给出状态；引用具体实验/案例及其制品、环境、负载和日期 |
| 冲突 | 逐条列出互相矛盾的主张，不静默选择一个来源 |
| 适用边界 | 写明硬件、软件、功能、规模和时间范围 |
| 下一步证据 | 指定需要补齐的固定文档、制品身份或验证，不写成未经授权的执行命令 |

## `unknown` 与 `conflict` 的处理

出现以下任一情况时，相关关系保持 `unknown`：

- 结论依赖过去的动态页面、`master`/`latest` 内容，却没有可定位的当时版本、发布日期/访问日期、精确章节或可复核摘要；
- 只知道项目产品版本，不知道实际安装包版本、构建标记或来源；
- 两份矩阵各自支持相邻依赖，却没有资料覆盖其联合制品；
- 硬件型号、固件/驱动、OS/ABI、执行模式或关键特性缺失；
- 测试声明没有环境、用例范围、跳过项或可定位结果；
- “未列出”但来源没有说明未列出项即不支持。

当两个可定位来源对同一制品、条件和时间范围给出互斥声明时，标记 `conflict`。处理顺序如下：

1. 先检查是否其实是产品版本与包版本、源码与二进制、不同硬件或不同发布日期造成的对象错位。
2. 保留每条声明的原文位置、revision、日期、适用范围和发布主体；不要只保留最后看到的一条。
3. 查找同一发布主体对该版本的勘误、发行说明或生命周期说明。若新资料明确取代旧资料，记录取代关系，旧证据仍保留用于历史判断。
4. 无法消解时维持 `conflict`，并把受影响的整栈结论保持为 `conflict` 或 `unknown`。一次本地通过或失败只能增加本地轴证据，不能自动裁决官方声明冲突。

## 使用与解释注意事项

- “兼容”“支持”“推荐”“可安装”“已测试”和“已复现”不是同义词。记录来源实际使用的术语，并在结论中说明本页采用的解释。
- 版本范围如 `X.Y.x`、最低版本或“及以上”只有在原始来源明确给出时才能展开；不要用语义版本直觉补齐厂商规则。
- 测试覆盖是多维集合。模型通过不代表全部算子通过，单卡通过不代表分布式通过，功能通过也不代表性能或数值结果满足目标。
- 本页 `verification.status: source_checked` 仅表示核对了引用来源怎样区分分支与发行包；不表示本仓库完成了硬件安装、最小运行验证或整栈复现。

## 来源与更新范围

- [TorchNPU tag `v7.2.0-pytorch2.6.0` 的固定 commit](https://github.com/Ascend/pytorch/tree/bc51ab84cc6f35c77aab1c59886e0ea43681a317)：本例统一使用的历史快照；tag 是发布标识，正文链接固定到其解引用 commit。
- [固定英文 `README.md`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md)：二进制安装、源码构建入口、PyTorch/Python 表及 CANN/PyTorch/扩展/分支配套表。
- [固定 `version.txt`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/version.txt)：该 commit 的扩展版本声明。
- [第十五批取证记录](../../docs/research/batch-15-profile-intersection-sources.md)：两平台约束链状态表、冲突原文、候选登记与缺口；「平台档案的读取与变化审计规则」一节的页面变化实例（nv-pub-date 回写、minor-version 页新增 CUDA 13.x 行）与 Ascend 精确 HDK 缺口出自该记录。
- 平台档案实例：[昇腾软件栈的文档配套档案](ascend-documented-profile.md)、[NVIDIA 软件栈的文档配套档案](nvidia-documented-profile.md)；实载库层次的区分方法见[驱动初始化、运行时执行同步与库装载](runtime-execution-and-library-loading.md)。
- 制品证据分层（与[昇腾软件栈的文档配套档案](ascend-documented-profile.md)的清单状态一致）：**已取得（索引声明层面）**——`torch-npu` 2.6.0.post3 六个 wheel 的完整文件名、平台标签（cp39/cp310/cp311 × manylinux x86_64/aarch64）与索引 sha256（2026-10-09 经 PyPI JSON API，见[第十五批取证记录](../../docs/research/batch-15-profile-intersection-sources.md)制品身份表）。**未取得**——下载字节的摘要比对（索引值未经下载核验）、wheel `METADATA` 与包元数据、构建 commit/ABI 身份（abi1 变体无独立清单）、CANN 8.3.RC1 精确驱动/固件配套页，以及任何本地整栈实测证据。这些未取得项不能从 README 的版本交集推导。

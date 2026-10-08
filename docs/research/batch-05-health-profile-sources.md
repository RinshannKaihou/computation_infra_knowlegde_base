# 第五批 F04 / E02 来源准备

> 调研记录，不是知识库正式正文，也不是部署、支持或采购建议。

- 调研范围：F04 `hardware.health-evidence` 与 E02 `software-stack.nvidia-documented-profile`。
- 核对日期：2026-09-30；2026-09-29 已实际读取的 MindX DL 页面沿用原读取日期。
- 执行边界：未安装、构建或运行上游代码；未拉取容器或大型制品；未访问本地主机 GPU/NPU 状态；未执行主动诊断或硬件测试。
- 版本边界：固定源码只说明该 commit 的接口和实现；标记为 `latest` 的网页按观察日期登记，不能当作不可变发行快照。

## 可写判定

当前证据已经足以写两篇边界明确的条目，无需为追求“全覆盖”继续无限搜集：

- F04 可以写成“如何解释健康证据”的方法页，分别给出 GPU 与 NPU 的状态摘要、错误事件、累计计数器、采样失败和未覆盖项；主动测试只写资源影响、隔离要求及型号/版本约束。现有来源不支持编造统一阈值，也不支持把一次 `PASS`/“健康”扩张为整机无故障。
- E02 可以采用 `nvcr.io/nvidia/pytorch:25.01-py3` 作为**文档研究基线**，逐层登记宿主驱动、容器运行层、容器内 CUDA/库、框架、集合通信和诊断组件。R545 条款冲突、Python 路径冲突、镜像 manifest digest、精确 Container Toolkit 版本和宿主 OS 仍应保留为未知。

## F04：设备健康证据与检测边界

### 先固定证据类型，而不是先定义“健康”

正文可统一使用下面五类记录；每条记录都应带设备身份、采集工具及版本、采集时间/窗口和采集结果。GPU 与 NPU 共用这个记录框架，但字段、状态值和支持范围不能互相映射。

| 证据类型 | 应记录的事实 | 不能推出的结论 |
| --- | --- | --- |
| 状态摘要 | 工具在一次查询中返回的健康码或 PASS/WARN/FAIL 类结论，以及查询本身是否成功 | “所有子系统已覆盖”“未来仍健康”“等同于硬件厂商支持结论” |
| 错误事件/错误码 | 事件码、出现时间、来源组件、设备及必要上下文 | 任意非零码都等于器件永久损坏；不同厂商错误码可直接对照 |
| 计数器 | 字段名、单位、累计/窗口语义、起止样本、重置边界 | 没有采集窗口或基线时，单个裸值可以直接套阈值 |
| 采样失败 | API/工具返回错误、超时、权限不足、设备丢失、字段空值或无数据 | 把“读不到”记成零，或把采样失败记成健康 |
| 未覆盖/不支持 | 未启用的 watch、型号不支持、版本缺少插件、容器/权限限制或明确 `SKIP` | 未覆盖项已经通过，或未见错误就是通过 |

### GPU：DCGM 的被动健康与主动诊断

#### 固定来源与字段语义

固定基线选用 NVIDIA DCGM tag `v3.3.9`，解引用到 commit `b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52`。该快照适合固定字段标识和计数器类型，不应用来替代当前产品支持表。

- [`dcgmlib/dcgm_fields.h` 第 604–607 行](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L604-L607)定义 PCIe replay counter。
- [第 640–643 行](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L640-L643)说明 XID 字段的值是具体 XID，而不是可任意求和的“错误严重度”。
- [第 758–778 行](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L758-L778)区分 volatile ECC 总数与跨驱动持续的 aggregate ECC 总数，并注明 aggregate SBE/DBE 单调增加。
- [第 915–930 行](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L915-L930)给出 SBE/DBE retired pages 与 pending retirement 字段；已退休页计数为单调增加。
- [第 982–985 行](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/dcgmlib/dcgm_fields.h#L982-L985)给出 NVLink CRC FLIT error total 字段。

这些定义足以说明“累计计数器需要重置边界和差分窗口”，但不足以给出跨 DCGM 版本、跨 GPU 型号的统一告警阈值。固定实现内部存在规则和常量；F04 不应把实现常量抄成运维通用阈值。

#### 被动证据与主动测试的边界

[DCGM 当前 Health Monitoring 文档](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html)明确区分：`dcgmi health` 基于后台 field watches 和保留样本，被动解释 PCIe、内存、InfoROM、驱动、温度/功耗、NVLink/NVSwitch 等已启用检查；`dcgmi diag` 执行主动测试。“Healthy”只表示已启用规则未在所看窗口内发现 incident，不表示每个子系统都被监视，也不表示主动压力测试已通过。

[DCGM 当前 Diagnostics 文档](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)给出正文必须保留的限制：

- 主动诊断会消耗 GPU 计算、显存、PCIe/NVLink、CPU、功耗和散热资源；较长套件可能复位设备或与业务冲突。
- 应显式选择实体并与调度器协调，把设备从普通服务中隔离后再执行。
- 失败原因可能来自宿主环境、权限、库、拓扑、散热、供电或同时运行的工作负载，不应直接写成 GPU 器件损坏。
- 它不负责维修，不替代离线现场诊断，也不单独决定 RMA。
- 套件和测试可用性取决于 DCGM 发行版、插件、实体类型、硬件、动态库/可执行文件和权限；非数据中心 GPU 的可运行级别另有限制。

[DCGM Exporter Metrics 当前文档](https://docs.nvidia.com/datacenter/dcgm/latest/reference/dcgm-exporter-metrics.html)区分四族：XID/clock-event 的 `COUNT` 是窗口样本数；XID `TOTAL` 是 collector 启动后观察到的非零记录数，clock-event `TOTAL` 是 inactive→active 转换数、初始 active 不计。COUNT 缺有效样本可输出无事件分类标签的零；TOTAL 首次观察前可能无序列，重启或 hot reload 重建 collector 后重置。零值、无序列与无事件不可互换；这些当前网页语义不倒推到 DCGM v3.3.9。

#### GPU 仍应标成未知的事项

- `latest` 页面在 2026-09-30 的内容与 DCGM `v3.3.9` 不是同一个冻结版本；二者只能分别承担“当前概念说明”和“固定字段快照”的角色。
- 未取得一个冻结的 `v3.3.9` 产品/插件支持矩阵。具体 GPU 型号、MIG/NVSwitch/ConnectX/CPU 实体及诊断级别需在实际环境另核。
- 未取得本地采样数据，因此没有验证字段是否可读、采样频率、计数器是否发生重置或任何 PASS/WARN/FAIL 结果。
- `blank`、`no data`、`not watched`、`not supported` 与采集 API 失败需在实现或实际采集层分别保存；正文不把它们归并成零值。

### NPU：固定 DCMI 接口与 MindX 主动诊断

#### 固定接口能证明什么

复用已登记的 MindCluster `v26.1.1` 固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`：

- [`dcmi_interface_api.h` 第 72 行起](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi_interface_api.h#L72-L91)的 `dcmi_ecc_info` 同时包含使能标志、SBE/DBE、total SBE/DBE 和隔离页信息；这些字段不可压成一个笼统“ECC 正常”。
- [第 404 行起](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi_interface_api.h#L404-L420)定义故障事件结构；[第 674 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi_interface_api.h#L674-L674)提供故障事件订阅入口。
- [第 606–615 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi_interface_api.h#L606-L615)分别暴露设备健康、错误码和 ECC 查询；[第 642 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi_interface_api.h#L642-L642)另有网络健康查询。
- Go 封装的[错误码查询第 1504–1524 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi.go#L1504-L1524)把 DCMI 调用失败与返回的错误码数量/内容分开；[健康查询第 1567–1582 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi.go#L1567-L1582)也先检查调用返回值，再处理健康码。
- [网络健康查询第 1780–1813 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi.go#L1780-L1813)单独处理调用返回、健康码和超时；注释说明掉卡后调用可能阻塞。该证据支持把“超时/采样失败”与“不健康状态”分开。
- [错误码与掉卡处理第 1955–2023 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi.go#L1955-L2023)含封装层的超时、重试和 `DeviceNotReady` 映射逻辑；[ECC 封装第 2266–2290 行](https://github.com/Ascend/mind-cluster/blob/44385c13d7b1d87def35f1604e8be4d16de6ca4e/component/ascend-common/devmanager/dcmi/dcmi.go#L2266-L2290)保留使能、当前/累计 SBE/DBE 和隔离页计数。

这组源码证明接口与封装层的分层方式，不证明所有昇腾机型都实现相同字段，也没有给出可跨版本使用的健康阈值或完整健康码语义表。

#### MindX `ascend-dmi` 主动检查的资源和支持边界

2026-09-29 已实际读取 [MindX DL 6.0.RC2 `ascend-dmi` 故障诊断页](https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html)。该页可用于记录以下限制：

- AICore 诊断/压测的条件是 Atlas A2 配套 HDK 23.0.0+（MCU、驱动、固件）、CANN 7.0.0+ toolkit 与配套 kernels；root/产品/执行环境按表 3 核对，两者均影响业务并有后续重启说明。约 20–40 GB HOST 内存只对应 AICore 压测。
- PRBS 单列工具 6.0.RC2.1+、三种产品、root、物理机/特权容器及不能与其他诊断并行的条件；不继承 AICore 的 HDK/CANN 条款。
- network 的 Host root 与 RoCE IP/子网掩码、检测对象 IP 是该测试的前提；普通 HBM 诊断与 HBM 压测/高危地址压测的业务影响须分开。
- 带宽/AI FLOPS 检查会影响业务；DCMI 监控可影响带宽测量。各项覆盖不同，SKIP 和读取失败不能扩张成通过或器件损坏。

该页末端 PRBS 结果表的中英文描述出现相互冲突：`FAIL` 行的中文写“检测通过/误码率小于…”，`PASS` 行反而写“检测失败/误码率大于…”。正文必须把这一点登记为**未解决的文档内部冲突**，不得据此抄写阈值或定义 PASS/FAIL。

#### NPU 仍应标成未知的事项

- 固定 MindCluster 源码没有提供所有健康码到自然语言含义的完整、产品化映射。
- MindX 6.0.RC2 网页与 MindCluster v26.1.1 不是一个已验证配套环境；两者不能组合成“已支持版本矩阵”。
- 页面列出的主动测试影响和型号限制只适用于该文档所述条件；没有本地硬件、驱动、固件、CANN、MindX 或容器环境验证。
- 厂商网页许可范围未确认；只能链接并作原创归纳，不能把仓库 Apache/CC 许可扩张到该网页或软件包。

## E02：NVIDIA 文档配套档案

### 研究基线

选择镜像标签 `nvcr.io/nvidia/pytorch:25.01-py3` 作为明确的**文档研究基线**。基线证据由 [PyTorch Release 25.01](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel-25-01.html) 与 [NGC `25.01-py3` catalog layer 页](https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/pytorch/25.01-py3/layers)共同组成。

这个选择只表示“围绕一个明确 release/tag 建档”。没有拉取镜像、验签、读取 manifest digest、启动容器或测试 GPU；因此它不是本地支持承诺，也不是生产部署推荐。

### 分层档案

| 层 | 文档中可固定的事实 | 必须保留的边界或冲突 |
| --- | --- | --- |
| 宿主驱动 | release 页首先写 570+；同段列出数据中心 GPU 可用的旧分支例外，其中包括 R545 545.23+ | 下一段又把 R545 与若干分支列为对 CUDA 12.8 不 forward-compatible、应升级的驱动。当前 CUDA compatibility 页只给 CUDA 12.x 的大类最低驱动/区间，不能消解 25.01 页面内部的 R545 冲突。宿主 OS 也未知 |
| 容器引擎与 NVIDIA Container Toolkit | 当前 Frameworks User Guide 说明宿主驱动、Docker 与 NVIDIA Container Toolkit 的职责：运行层把设备及宿主驱动能力提供给容器；驱动不应被装入镜像 | 25.01 release 页没有给出与该镜像绑定的 Docker/Container Toolkit 精确版本。不能从“当前用户指南”倒推 2025-01 的唯一版本 |
| 容器制品身份 | NGC catalog 明确 tag `25.01-py3`、签名标记、build id `134983853` 和 build ref `3857cfd7a27acea1d4e19243329fcd1dae3b222e` | catalog 展示的 layer SHA 不是已核验的 image manifest digest；本轮没有取得 digest，也没有执行签名验证 |
| 容器内 OS/Python | release 页 Contents 写 Ubuntu 24.04（含 Python 3.12）；NGC layer 环境字段写 `PYVER=3.12`、`PYVER_MAJMIN=312` | release 页另一处仍写预构建 PyTorch 位于 `/usr/local/lib/python3.10/dist-packages/torch`。layer 元数据增强“3.12”证据，但不能证明文档中的 3.10 路径在所有层/变体中为何出现；正文需保留差异 |
| CUDA 与基础库 | CUDA `12.8.0.038`、cuBLAS `12.8.3.14`、cuDNN `9.7.0.66`、TensorRT `10.8.0.40` | 这些是容器内容，不是宿主驱动兼容性或宿主已安装包声明。CUDA 许可可复用现有 `src.nvidia.cuda-toolkit-12-8`，但具体容器组件和第三方 notice 仍另计 |
| 框架 | PyTorch `2.6.0a0+ecf3bae40a`；NGC layer 字段给出截短形式 `2.6.0a0+ecf3bae` | 这是 NVIDIA 容器构建，不等同于上游 PyTorch v2.6.0 tag，也不应与仓库中的其他 PyTorch 样板合并 |
| 集合通信与网络库 | NCCL `2.25.1`、HPC-X `2.21`、SHARP `3.9.0`、UCC `1.4.0`、OpenUCX `1.18.0`、OpenMPI `4.1.7`、rdma-core `50.0` | 只证明 release 页列入容器内容；没有在本地网络拓扑、驱动、固件、交换机或多机环境验证 |
| 诊断组件 | F04 选择 DCGM `v3.3.9` 作为接近该时期的固定源码样板，可说明诊断证据结构 | 25.01 release 页没有把该 DCGM 版本声明为镜像配套组件。本档案只能列为“研究配套参考”，不能写进已验证依赖链 |
| 设备代际 | release 页写 25.01 为 Blackwell 优化，并从 25.01 起停止 Volta 支持 | 这不是对所有数据中心 GPU、MIG 模式或具体 SKU 的完整支持矩阵；未取得本地设备验证 |

### R545 冲突的处理

不要任选一段消除冲突。E02 可原样记录：

1. 25.01 Driver Requirements 第一段把 R545 545.23+ 列为数据中心 GPU 的旧分支例外。
2. 紧接段落又把 R545 列入不具备 CUDA 12.8 forward compatibility、应升级的分支。
3. [当前 CUDA Minor Version Compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html)说明 CUDA 12.x 的大类最低驱动为 525，且 minor compatibility 有功能限制；它没有回答 25.01 镜像对 R545 的具体例外是否有效。
4. 因此 `R545 + 25.01` 的结论保持 `unresolved`。只有取得当期、同一产品范围的驱动表或实测证据后才能缩小范围。

### Python 路径差异的处理

NGC layer 元数据中的 `PYVER=3.12` 与 release 页 Contents 的 Ubuntu 24.04/Python 3.12 相互一致，可以把容器默认 Python 主版本的文档证据提升为“3.12，有两个相互独立页面字段支持”。但 release 页仍保留 `python3.10/dist-packages` 路径。正式档案应同时展示这三项，不应擅自把路径改成 `python3.12`，也不应凭路径反推默认 Python 是 3.10。

### E02 仍应标成未知的事项

- 镜像 manifest digest、实际签名验证结果和拉取后的层清单。
- 与 25.01 明确绑定的 Docker、containerd、NVIDIA Container Toolkit / runtime 版本。
- 宿主 OS、内核、GPU 型号、固件、Fabric Manager、NIC/交换机与拓扑组合。
- R545 条款冲突的权威勘误或同版支持表。
- 容器内实际 Python 可执行文件、PyTorch wheel 身份、动态链接库和运行时加载结果。
- DCGM 或其他诊断组件是否随镜像提供、应在宿主还是容器运行，以及与该栈的精确兼容版本。

## 正文写作护栏

- F04 的核心句式应是“证据在何种采集条件下支持何种有限结论”，而不是列一张万能健康阈值表。
- `PASS`、健康码、零计数、`SKIP`、无数据、超时、权限不足和工具调用失败必须是不同状态。
- 被动 watch 与主动测试分开；主动测试必须附资源影响、服务隔离、停止/恢复条件、型号与版本适用性。
- GPU 和 NPU 分节，不建立错误码或健康状态的一一对应表。
- E02 每层单独写版本与证据来源；容器内 OS/CUDA 不代表宿主 OS/驱动，catalog tag 不代表已固定 digest。
- 配套档案中的“未知”和“冲突”是结果的一部分，不为填满矩阵而推断。

## 可复用的现有登记

- `src.ascend.mind-cluster-v26.1.1`：固定 commit `44385c13d7b1d87def35f1604e8be4d16de6ca4e`，用于 NPU DCMI 接口与封装。
- `src.nvidia.cuda-toolkit-12-8`：CUDA 12.8 归档与 EULA 入口；只支撑 CUDA 组件/许可边界，不消解 25.01 驱动冲突。

## 待合并来源 YAML

下面是符合 `schemas/sources.schema.json` 的完整独立 YAML。正式合并时应先检查 ID 是否已被其他批次登记；本文件不修改 `sources/registry.yaml`。

```yaml
schema_version: 1
sources:
  - id: src.nvidia.dcgm-v3.3.9
    title: NVIDIA DCGM v3.3.9 固定源码快照
    url: https://github.com/NVIDIA/DCGM/tree/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52
    kind: repository
    registered_at: '2026-09-30'
    revision: v3.3.9; commit b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52
    license:
      status: partial
      scopes:
        - scope: 固定 commit 的仓库自有源码；二进制包、容器、文档和第三方内容另计
          identifier: Apache-2.0
          url: https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/LICENSE
      notes: 仓库 README 将源码许可证与 NVIDIA DCGM 二进制 SLA 分开；本登记不把 Apache-2.0 扩张到二进制发行包、产品文档或第三方依赖。
    notes: 用于固定字段标识、计数器类型及健康实现边界；未构建或运行，不代表当前 DCGM 文档、任一 GPU 型号或诊断插件的支持范围。
  - id: src.nvidia.dcgm-health-monitoring-latest-2026-09-30
    title: NVIDIA DCGM Health Monitoring（latest，2026-09-30 观察）
    url: https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html
    kind: documentation
    registered_at: '2026-09-30'
    revision: latest page observed 2026-09-30
    license:
      status: unknown
      scopes: []
      notes: 公开可读不等于允许全文再分发；本库只链接并作原创归纳，未把 DCGM 源码许可证扩张到网页内容。
    notes: 用于区分被动 health watches、policy 与主动 diagnostics，并限定 Healthy 只覆盖已启用规则及保留样本；latest 页面可变，不作为冻结发行快照。
  - id: src.nvidia.dcgm-diagnostics-latest-2026-09-30
    title: NVIDIA DCGM Diagnostics（latest，2026-09-30 观察）
    url: https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html
    kind: documentation
    registered_at: '2026-09-30'
    revision: latest page observed 2026-09-30
    license:
      status: unknown
      scopes: []
      notes: 公开可读不等于允许全文再分发；本库只链接并作原创归纳，软件、插件和随附第三方内容另计。
    notes: 用于主动诊断的资源占用、隔离、失败归因和型号/插件/权限边界；未执行任何诊断，latest 页面可变。
  - id: src.nvidia.dcgm-exporter-metrics-latest-2026-09-30
    title: NVIDIA DCGM Exporter Metrics（latest，2026-09-30 观察）
    url: https://docs.nvidia.com/datacenter/dcgm/latest/reference/dcgm-exporter-metrics.html
    kind: documentation
    registered_at: '2026-09-30'
    revision: latest page observed 2026-09-30
    license:
      status: unknown
      scopes: []
      notes: 公开可读不等于允许全文再分发；本库只链接并作原创归纳，exporter 软件及镜像许可另行核验。
    notes: 用于 XID/clock event 的时间窗语义、累计量重置边界和健康状态标签；未部署 exporter，latest 页面可变。
  - id: src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29
    title: MindX DL 6.0.RC2 ascend-dmi 故障诊断
    url: https://www.hiascend.com/doc_center/source/zh/mindx-dl/60rc2/toolbox/ascenddmi/toolboxug_0020.html
    kind: documentation
    registered_at: '2026-09-29'
    revision: MindX DL 6.0.RC2 page observed 2026-09-29
    license:
      status: unknown
      scopes: []
      notes: 厂商网页许可与 MindX/CANN/HDK 软件包条款未核验；公开可读不等于允许全文再分发，本库只链接并作原创归纳。
    notes: 用于 ascend-dmi 主动诊断/压测的资源影响、产品与版本限制、SKIP/读取失败边界；页面 PRBS PASS/FAIL 描述存在内部冲突，未执行任何测试，也不与 MindCluster v26.1.1 拼成配套矩阵。
  - id: src.nvidia.pytorch-container-25.01-release-notes-2026-09-30
    title: NVIDIA PyTorch Container Release 25.01 Notes
    url: https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel-25-01.html
    kind: documentation
    registered_at: '2026-09-30'
    revision: Release 25.01; page last updated 2026-09-08; observed 2026-09-30
    license:
      status: unknown
      scopes: []
      notes: 公开可读不等于允许全文再分发；本库只链接并作原创归纳。容器、框架、CUDA 组件及第三方软件的许可和 notices 分别核验。
    notes: E02 文档研究基线；用于容器内容、框架、CUDA/NCCL 和 driver 文本。页面同时存在 R545 前后冲突及 Python 3.10 路径与 Python 3.12 Contents 差异，不能当成已验证支持矩阵。
  - id: src.nvidia.ngc-pytorch-25.01-py3-catalog-2026-09-30
    title: NGC PyTorch 25.01-py3 Catalog Layer Metadata
    url: https://catalog.ngc.nvidia.com/orgs/nvidia/-/containers/pytorch/25.01-py3/layers
    kind: documentation
    registered_at: '2026-09-30'
    revision: tag 25.01-py3; build id 134983853; build ref 3857cfd7a27acea1d4e19243329fcd1dae3b222e; observed 2026-09-30
    license:
      status: unknown
      scopes: []
      notes: NGC 页面、容器制品、软件 EULA 和第三方 notices 的许可范围未核验；本库只链接并记录可见元数据。
    notes: 用于确认 tag、签名标记、build 元数据以及 PYVER=3.12/PYVER_MAJMIN=312。页面中的 layer SHA 未登记为 image manifest digest；未拉取、验签或运行镜像。
  - id: src.nvidia.cuda-compatibility-latest-2026-09-30
    title: NVIDIA CUDA Minor Version Compatibility（latest，2026-09-30 观察）
    url: https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html
    kind: documentation
    registered_at: '2026-09-30'
    revision: latest page observed 2026-09-30
    license:
      status: unknown
      scopes: []
      notes: 公开可读不等于允许全文再分发；本库只链接并作原创归纳。CUDA Toolkit 12.8 的归档和 EULA 已由另一来源登记。
    notes: 用于 CUDA 12.x 的大类最低驱动与 minor compatibility 限制；当前可变页面不能消解 PyTorch 25.01 release notes 内部的 R545 冲突。
  - id: src.nvidia.framework-containers-user-guide-2026-09-30
    title: NVIDIA Deep Learning Frameworks Containers User Guide（2026-09-30 观察）
    url: https://docs.nvidia.com/deeplearning/frameworks/user-guide/index.html
    kind: documentation
    registered_at: '2026-09-30'
    revision: current page observed 2026-09-30
    license:
      status: unknown
      scopes: []
      notes: 公开可读不等于允许全文再分发；本库只链接并作原创归纳。Docker、NVIDIA Container Toolkit、驱动、容器与第三方组件条款分别核验。
    notes: 用于宿主驱动、容器引擎/Toolkit 与镜像的职责边界，以及不把驱动安装进镜像的原则；没有把当前指南倒推为 25.01 的精确 runtime/toolkit 版本。
```

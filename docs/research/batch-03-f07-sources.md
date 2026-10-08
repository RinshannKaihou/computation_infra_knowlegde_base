# 第三批 F07 来源提取记录

本文件记录 `communication.collectives-and-rank-progress` 实际打开的原始资料、可支持的陈述、许可范围和证据缺口。它不是通信库配套矩阵，也不是 GPU/NPU 集群测试结果。

## 选定版本

| 组件 | 本文固定版本 | 选择理由与边界 |
|---|---|---|
| NCCL | 2.27.5 官方归档 | 归档页和 User Guide 均显示 2.27.5；可固定 communicator、collective、CUDA stream、多 communicator 次序和错误类别的语义。未声称它是 PyTorch 2.8 的内置或推荐 NCCL 版本 |
| PyTorch | 2.8 文档 | 版本化 URL 可固定 ProcessGroup、rank、组创建顺序和同步/异步 collective 语义。未核对二进制构建、打包 NCCL 版本或目标环境 |
| HCCL | CANN 8.0.RC1.alpha003《集合通信接口参考》，文档版本 01，发布日期 2024-06-06 | 华为正式 PDF 可直接读取 HCCL 概念、执行流程、C++ API 参数约束与异常说明；资料为 RC/alpha 版本，不外推到其他 CANN/HCCL、TorchNPU、固件或型号组合 |

## 已打开并核对的页面

### NVIDIA NCCL 2.27.5

| 精确页面 | 核对到的内容 | 不支持的推论 |
|---|---|---|
| [归档入口](https://docs.nvidia.com/deeplearning/nccl/archives/index.html) | Release 2.27.5 下列出 User Guide、Release Notes、安装指南、SLA 与 BSD License；确认版本入口真实存在 | 当前最新版本；与任意框架发行包的配套关系 |
| [Creating a Communicator](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/communicators.html) | communicator 中各 CUDA device 使用唯一 `0..n-1` rank；对象关联固定 rank/device；多 communicator 的主机 launch 次序要求；错误类别与异步错误处理 | 相同数量的设备自动属于同一 communicator；所有超时都是网络错误；2.26 后无需全局一致次序 |
| [Collective Operations](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/collectives.html) | 每个 rank 调用 collective，并使用相同 count 与 datatype；root 是 rank 而不是 device number；AllGather/ReduceScatter 布局依赖 rank 次序 | 原生 API 检查 Python tensor shape；所有变长框架 API 都要求同 shape |
| [CUDA Stream Semantics](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/streams.html) | NCCL 调用在操作有效入队到给定 stream 后返回，操作随后在 CUDA 设备异步执行；可用 CUDA stream/event 查询完成；聚合组和 nonblocking 模式另按 Group Calls 限定 | HCCL/NPU 具有同样的返回、stream、event 或环境变量语义；主机返回等于设备完成 |

补充核对 [Group Calls](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/usage/groups.html)：组内 collective 返回可早于入队；nonblocking group 的 `ncclInProgress` 也不代表提交成功。API 聚合组不等于 communicator。

归档页面同时链接 NCCL 软件许可协议与 BSD License，但本轮只链接、原创归纳 User Guide，没有复制代码、图或文档长段。User Guide 页面自身未给出足以确定其全部再分发条件的独立许可声明，因此来源登记把文档许可标为 `partial`，不把软件 BSD 条款自动扩张为所有网页内容的 blanket license。

### PyTorch 2.8

核对页面为 [PyTorch 2.8 `torch.distributed`](https://docs.pytorch.org/docs/2.8/distributed.html)。实际阅读的位置包括：

- `get_rank` / `get_world_size`：rank 是进程组内的唯一连续编号，world size 是组中进程数；
- `new_group` 与 Groups：所有主组进程进入建组、各进程按相同次序创建组；多个 NCCL process group 的 collective 要有全局一致执行次序，多线程发起需要显式同步；
- Synchronous and asynchronous collective operations：CUDA collective 的函数返回、入队、当前 stream 等待和设备完成之间的区别；
- Collective functions：`broadcast`、`all_gather_into_tensor` 等 API 各自的元素数/size 要求。

该页面支持框架 API 契约，不支持把 PyTorch 2.8 与 NCCL 2.27.5 拼成发行配套结论，也不支持 HCCL backend 的实现细节。文档中的 CUDA 语义只用于 NCCL/CUDA 样板，未移植到 NPU。

轮末修订补充：核对同页 `Work.wait`、`init_process_group` 以及 v2.8.0 完整 commit `ba56102387ef21a3b04b357e5b183d48f0afefc7` 的 [ProcessGroupNCCL.cpp](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/csrc/distributed/c10d/ProcessGroupNCCL.cpp)。`isCompleted`（580–585）是异常或结束事件完成；结束事件查询在 649–661；`wait`/stream 依赖与 CPU 等待分支在 775–839；blocking-wait 默认读取在 960。概览措辞不能替代此 backend 实现：普通非 barrier、未指定有效 timeout、未启用 blocking-wait 的等待主要建立 stream 依赖，例外路径会等待 CPU。没有将完成标志单独记为成功证据。

许可定位使用 PyTorch `v2.8.0` 仓库根 [LICENSE](https://github.com/pytorch/pytorch/blob/v2.8.0/LICENSE)。该 BSD-style 条款覆盖仓库随附的代码与文档材料；第三方依赖和独立网站资产仍需按各自声明核对。正文只做原创归纳并链接版本化页面。

### HCCL / CANN 8.0.RC1.alpha003

核对对象为华为正式 PDF：[《集合通信接口参考》](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf)，文档版本 01，发布日期 2024-06-06，共 79 页。

| 页码/章节 | 核对到的内容 | 不支持的推论 |
|---|---|---|
| 集合通信简介与相关概念；执行流程在物理第 8 页，异常在第 9 页，rank 定义在第 10 页 | HCCL 覆盖 PCIe/HCCS/RoCE；初始化、建链、执行三阶段；执行阶段编排 Notify/SDMA 并由 runtime 下发设备；Notify wait/record；ranktable、world/custom group、rank size、world/group/local rank；单卡或链路问题都可能造成集群大量超时 | 用户现场使用了某条链路；任意 timeout 可直接归因于网络；所有版本阶段和默认值都相同 |
| 3.3 C++ 集合通信算子；AllReduce 一致性在物理第 47 页，Broadcast 在第 48 页 | `HcclAllReduce`、`HcclBroadcast`、`HcclAllGather` 等接口、`aclrtStream` 参数及各自 count/dtype/op/root 约束；`HcclBarrier` 阻塞组内各 rank 的 stream，直到各 rank 下发该操作 | 每种 API 的主机返回都等于入队或设备完成；这些约束可替代框架层 shape 检查 |
| 异常处理章节的 HcclGetCommAsyncError | `HcclGetCommAsyncError` 在该版本的返回范围说明 | 更高版本支持范围；TorchNPU watchdog/wait 的具体实现 |
| 样例章节的通信调用与 aclrtSynchronizeStream | 通信调用之后另外调用 `aclrtSynchronizeStream` | 单凭样例可精确定义所有 collective 的 host-return 边界 |

该 PDF 的页脚标示华为版权所有，未发现允许本文库再分发全文或图片的许可。本库仅保存链接和原创摘要，来源登记将许可标为 `unknown`。华为网站[法律声明](https://www.huawei.com/cn/legal)也不应被解释成文档再分发授权。

## 证据关系与保留的 unknown

| 关系 | 状态 | 依据或缺口 |
|---|---|---|
| communicator/process group 决定参与者和组内 rank 解释 | 来源已核对 | NCCL communicator、PyTorch ProcessGroup、HCCL world/custom group 的正式说明相互支持概念层关系 |
| 所有 collective 都要求完全相同 shape | 不成立为通用结论 | NCCL 原生契约使用 count/dtype；框架 API 各自定义 size/shape 或变长参数，必须逐 API 判断 |
| NCCL 主机调用返回 = CUDA 设备完成 | 明确不成立 | NCCL 2.27.5 stream 语义明确区分入队返回与设备异步执行；PyTorch 2.8 也区分函数返回、Work 与 stream 同步 |
| HCCL 所有 collective 的主机返回边界 | `unknown` | 固定 PDF 说明设备任务编排、stream 参数和样例同步，但没有覆盖所有 collective 的统一精确定义；未用 NCCL 语义补齐 |
| timeout = 网络故障 | 明确不成立 | HCCL 文档直接列出单卡和链路均可引发集群大量 timeout；NCCL 文档还列出 CUDA、系统、参数/用法和异步通信错误 |
| 最先打印 timeout 的 rank = 最初故障 rank | 未被来源支持 | 需同一通信域的多 rank 时间线、前序设备/进程异常与时钟信息；正文图是原创概念例，不是事故复盘 |
| PyTorch 2.8 ↔ NCCL 2.27.5 ↔ CANN/HCCL 8.0.RC1.alpha003 | 未建立配套关系 | 三份来源分别用于解释接口边界；没有共同支持矩阵、构建清单或实际制品证据 |

## 来源登记建议

以下条目按 `schemas/sources.schema.json` 编写，供主任务统一合入 `sources/registry.yaml`。F07 不直接修改共享 registry。

```yaml
- id: src.nvidia.nccl-user-guide-2.27.5
  title: NVIDIA NCCL 2.27.5 User Guide
  url: https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/
  kind: documentation
  registered_at: "2026-09-29"
  revision: "2.27.5 archive"
  license:
    status: partial
    scopes:
      - scope: NCCL 2.27.5 软件源码许可入口；User Guide 网页与图的再分发范围未单独确认
        identifier: BSD-3-Clause
        url: https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/pdf/NCCL-BSD.pdf
    notes: 归档页同时列出软件许可协议和 BSD License；本库没有把软件源码条款扩张为全部网页内容，仅链接并原创归纳 User Guide。
  notes: 已核对 communicator 创建、多 communicator 并发次序、collective 参数、CUDA stream、Group Calls 和错误处理页面；未安装或运行 NCCL，也不构成与 PyTorch/CUDA/驱动的配套声明。
```

```yaml
- id: src.pytorch.distributed-2.8
  title: PyTorch 2.8 torch.distributed documentation
  url: https://docs.pytorch.org/docs/2.8/distributed.html
  kind: documentation
  registered_at: "2026-09-29"
  revision: "PyTorch 2.8 documentation"
  license:
    status: partial
    scopes:
      - scope: PyTorch v2.8.0 仓库自有代码与随附文档；第三方依赖和独立网站资产另计
        identifier: BSD-3-Clause
        url: https://github.com/pytorch/pytorch/blob/v2.8.0/LICENSE
    notes: 版本化文档页由项目文档生成；本库仅链接并原创归纳，未复制示例或网站资产。
  notes: 已核对 ProcessGroup、rank、组创建与多 NCCL group 次序、同步/异步 collective 和若干 API 的 size 契约；另核对 v2.8.0 commit ba56102387ef21a3b04b357e5b183d48f0afefc7 的 ProcessGroupNCCL.cpp，区分 Work 完成、异常与 CPU 等待条件；未核对发行二进制及其内置通信库版本。
```

```yaml
- id: src.huawei.hccl-api-cann-8.0-rc1-alpha003
  title: CANN 8.0.RC1.alpha003 集合通信接口参考 01
  url: https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/80RC1alpha003/apiref/hcclapiref/CANN%208.0.RC1.alpha003%20%E9%9B%86%E5%90%88%E9%80%9A%E4%BF%A1%E6%8E%A5%E5%8F%A3%E5%8F%82%E8%80%83%2001.pdf
  kind: documentation
  registered_at: "2026-09-29"
  revision: "CANN 8.0.RC1.alpha003; document 01; 2024-06-06"
  license:
    status: unknown
    scopes: []
    notes: PDF 标示华为版权所有，未发现允许再分发全文或图片的许可；本库仅登记链接并作原创归纳。
  notes: 已核对 HCCL 执行阶段、rank/group 概念、C++ collective 参数约束、异常说明与样例同步位置；RC/alpha 文档不代表其他 HCCL/CANN/TorchNPU/固件/设备版本，且未给出所有 collective 的统一主机返回边界。
```

## 验证与执行边界

本轮只读取公开的官方文档与许可页面，没有安装或运行 PyTorch、NCCL、CANN、HCCL 或 TorchNPU，没有访问 GPU/NPU，没有建立通信域，没有执行 collective、故障注入或超时实验。`source_checked` 只表示正文所列陈述已经与上述固定页面核对；多 rank 时间线是解释证据关系的原创示意，不是本仓库复现的事故。

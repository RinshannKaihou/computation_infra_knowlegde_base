# 第二批 F09 来源核查记录

本记录对应正文 `data-storage.training-data-path`。它保存精确来源定位、可支持的结论、不可外推的范围，以及供主任务合并到 `sources/registry.yaml` 的完整登记建议。它不是本地性能报告或配置指南。

## 核查对象与结论

| 来源 | 固定定位与页面标题 | 本文采用的范围 | 明确不覆盖 |
|---|---|---|---|
| PyTorch 数据加载文档 | [torch.utils.data — PyTorch 2.6 documentation](https://docs.pytorch.org/docs/2.6/data.html) | `DataLoader` 支持 map/iterable 数据集、加载顺序、自动 batching、单/多进程加载与 memory pinning；多进程 worker 承载 dataset access、内部 I/O、transform 和 `collate_fn`；`prefetch_factor` 的含义 | 其他框架或后端的相同实现；最佳 worker 数；目标环境的吞吐；存储、CPU 或设备传输已经成为瓶颈 |
| PyTorch CUDA 文档 | [CUDA semantics — PyTorch 2.6 documentation](https://docs.pytorch.org/docs/2.6/notes/cuda.html#use-pinned-memory-buffers)，章节 “Use pinned memory buffers” | CUDA 条件下 pinned/page-locked 主机内存、`non_blocking=True` 异步 copy 与潜在传输/计算重叠；过度 pinning 和 pinning 成本警告 | TorchNPU/CANN 的实现和性能；调用参数出现即证明已异步或已重叠；任意硬件上的通用加速结论 |
| MLCommons Storage 规则 | [MLPerf Storage Benchmark Submission Guidelines v2.0](https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md) | v2.0 使用模拟加速器和 `sleep()`；AU 的定义；训练数据路径终止于 host DRAM；不包含 online/offline preprocessing；warm-up、数据集/主机内存比例和随机种子用于约束缓存效应 | 主机到 GPU/NPU 传输、真实设备计算或通信；完整训练输入路径；NPU 的模拟参数或性能。该版本规则只列 A100/H100 的 sleep time |

三个精确页面均已直接打开并读取正文，未使用检索摘要代替页面证据。PyTorch 2.6.0 release 页面将 tag 指向 commit `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`；文档 URL 是 2.6 版本化站点。MLCommons release 页面将 `v2.0` release 指向 commit `7e71ca162d8f9e7ae4b5b698d7d79b0883817f25`；主任务补充打开上述完整 commit 的规则正文与 LICENSE.md，最终正文和登记引用完整 commit，保留 tag 作为发布名称。

## 建议新增来源登记

以下片段按 `schemas/sources.schema.json` 的完整字段编写。主任务合并前应再次检查 ID 冲突，并保持 YAML 缩进。

```yaml
  - id: src.pytorch.data-loader-2.6
    title: torch.utils.data — PyTorch 2.6 documentation
    url: https://docs.pytorch.org/docs/2.6/data.html
    kind: documentation
    registered_at: "2026-09-29"
    revision: "PyTorch 2.6 documentation; release tag v2.6.0 resolves to 1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340"
    license:
      status: partial
      scopes:
        - scope: PyTorch v2.6.0 仓库根 LICENSE；生成站点及第三方引用材料的具体范围另计
          identifier: BSD-3-Clause
          url: https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/LICENSE
      notes: 固定 tag 的根许可证已打开核对；本文只做短摘要与链接，未复制文档正文、示例或第三方材料。
    notes: 核对 DataLoader 的数据集、采样、自动组 batch、多进程 worker、预取和 memory pinning 语义；不提供最佳 worker 数或目标环境性能证据。
  - id: src.pytorch.cuda-semantics-2.6
    title: CUDA semantics — PyTorch 2.6 documentation
    url: https://docs.pytorch.org/docs/2.6/notes/cuda.html
    kind: documentation
    registered_at: "2026-09-29"
    revision: "PyTorch 2.6 documentation; release tag v2.6.0 resolves to 1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340"
    license:
      status: partial
      scopes:
        - scope: PyTorch v2.6.0 仓库根 LICENSE；生成站点及第三方引用材料的具体范围另计
          identifier: BSD-3-Clause
          url: https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/LICENSE
      notes: 固定 tag 的根许可证已打开核对；本文只做短摘要与链接，未复制文档正文、示例或第三方材料。
    notes: 仅用于 PyTorch 2.6 的 CUDA pinned memory、non_blocking copy、重叠条件及警告；不能作为 TorchNPU/CANN 行为证据。
  - id: src.mlcommons.storage-rules-v2.0
    title: MLPerf Storage Benchmark Submission Guidelines v2.0
    url: https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/Submission_guidelines.md
    kind: documentation
    registered_at: "2026-09-29"
    revision: "v2.0 release; commit 7e71ca162d8f9e7ae4b5b698d7d79b0883817f25"
    license:
      status: partial
      scopes:
        - scope: mlcommons/storage v2.0 仓库根 LICENSE.md；商标与外部链接材料另计
          identifier: Apache-2.0
          url: https://github.com/mlcommons/storage/blob/7e71ca162d8f9e7ae4b5b698d7d79b0883817f25/LICENSE.md
      notes: 主任务已通过官方 raw 文件补充读取该固定 commit 的根 LICENSE.md，核对为 Apache-2.0；商标、外部材料与发行制品范围仍需分开，登记保留 partial。本文只做原创归纳与链接。
    notes: 核对训练 benchmark 的模拟加速器、AU、缓存控制和 host DRAM 终点；该范围不包含预处理、设备传输或真实 GPU/NPU 计算通信。
```

## 关键证据定位

### PyTorch 2.6 `torch.utils.data`

- 页面开头列出 `DataLoader` 对 dataset 类型、加载顺序、automatic batching、single-/multi-process loading 和 automatic memory pinning 的支持。
- “Loading Batched and Non-Batched Data” 说明 `collate_fn` 如何把样本列表组成 batch。
- “Single- and Multi-process Data Loading” 说明 positive `num_workers` 启用 worker 进程，以及 dataset access、内部 I/O、transform 与 `collate_fn` 在 worker 中执行。
- `DataLoader` 参数表定义 `prefetch_factor` 为每个 worker 预先加载的 batch 数，并说明总预取量与 worker 数的关系。
- “Memory Pinning” 只明确写到 CUDA-enabled GPUs；本文没有把它外推到 TorchNPU。

### PyTorch 2.6 `CUDA semantics`

- “Use pinned memory buffers” 说明 page-locked memory、`pin_memory()`、`non_blocking=True` 和 overlap 的关系。
- 同一节警告 pinning 成本和低 RAM 时过度使用的风险。
- “Asynchronous execution” 还说明异步执行下未经同步的时间测量不准确。正文据此要求使用事件边界或等价时间线，但没有给未经验证的命令。

### MLPerf Storage v2.0

- “Benchmark Overview” 明确不包含 offline/online preprocessing。
- “Training” 说明以 `sleep()` 替代真实加速器计算；benchmark 起点为 shared persistent storage，数据传输终点为 host DRAM，不包含 accelerator memory transfer。
- “Definitions” 与 “Performance Metrics” 给出 AU 为模拟计算时间占总运行时间的比例；如果 I/O 全被计算覆盖，AU 为 100%。
- “Caching” 要求 warm-up、训练数据集至少为各 host node 内存总和的五倍，并在各次运行改变随机种子。这些是 v2.0 benchmark 的规则，不是生产训练的通用缓存配置。
- 规则写明该版本的 sleep time 只包含 NVIDIA A100 和 H100；没有把该模拟结果用于 NPU。

## 本文原创整理与待确认

路径图、阶段观测表、相邻边界证据矩阵和“首个不能按时完成的边界”方法是本知识库的原创归纳，不表述为 PyTorch 或 MLCommons 的标准。它们提供证据收集框架，尚未经过真实环境验证。

仍需真实环境或新来源确认：

- 目标 GPU/NPU 的 profiler 事件、利用率定义、传输队列和同步语义；
- 选定 TorchNPU/CANN 版本对 `pin_memory`、`non_blocking`、主机内存注册与 stream 的官方说明或源码行为；
- 数据格式、访问顺序、压缩/解码、tokenize/增强、batch 形状和缓存层；
- CPU/NUMA/设备拓扑与容器资源限制；
- 队列采集点的实际实现及 batch/step/rank 的关联方法；
- 同一工作负载冷/热阶段、稳定窗口、长尾和各 rank 正常基线。

## 未执行事项与主任务交接

本轮没有安装或运行 PyTorch、MLPerf Storage、DLIO、TorchNPU 或 CANN，没有执行上游脚本，没有访问存储集群、GPU 或 NPU，也没有得到任何本地吞吐、利用率、延迟或最佳配置结果。

主任务需统一完成：

1. 将上述三个来源合并到 `sources/registry.yaml`，检查 ID 与其他 agent 的来源登记是否重复；
2. F03 `hardware.resource-topology` 与 F11 `cluster-platform.device-resource-chain` 入库后，在 F09 正文补普通 Markdown 交叉链接，并视全库关系决定是否加入 `related_ids`；
3. 统一更新章节入口、任务路径与批次计划；
4. 运行 `make check` 和 `make build`。这两项只校验结构与引用，不代表技术判断或硬件实验已通过。

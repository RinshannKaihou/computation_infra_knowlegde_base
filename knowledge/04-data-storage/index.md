---
id: data-storage.index
title: 04 数据路径与存储系统
type: index
domain: data-storage
status: draft
platforms: [generic]
source_refs: [src.ascend.mind-cluster, src.stas.ml-engineering, src.infrasys.aiinfra]
updated_at: "2026-10-08"
summary: 组织数据加载、模型和 checkpoint I/O，以及完整性、持久化和存储异常。
related_ids: [data-storage.training-data-path, hardware.resource-topology, cluster-platform.index, training.index, inference.index, reliability.index, data-storage.checkpoint-durability, data-storage.data-starvation-triage, data-storage.checkpoint-slow-io-triage, data-storage.checkpoint-integrity-evidence]
---

# 04 数据路径与存储系统

本页是内容导航草稿。已建设的正文见下方入口，其余二级主题仍待补充；正文均为草稿，未经本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

## 已有正文

- [Checkpoint 写入与持久化边界](checkpoint-durability.md)：区分暂存、后台写入、提交、持久化和恢复验证。

- [训练数据供给路径与等待](training-data-path.md)：连接存储、缓存、加载、主机内存与设备消费，区分数据等待、传输等待和计算或通信等待的证据。

- [训练数据加载饥饿诊断指南](data-starvation-triage.md)：把取 batch 等待定位到存储、CPU 处理、队列、传输或消费的首个边界；以 PyTorch 2.6 DataLoader 与 profiler 为证据样板。

- [Checkpoint 慢写与恢复 I/O 诊断指南](checkpoint-slow-io-triage.md)：把保存/恢复慢定位到状态收集、staging 拷贝、后台写入、内核 writeback/fsync、存储后端或读路径。

- [Checkpoint 完整性与校验证据](checkpoint-integrity-evidence.md)：容器格式、框架元数据、存储层 scrub、应用自检四层校验各自能发现什么；DCP 2.6 无应用层校验和、MindIO checker 校验文件个数、Ceph deep scrub 默认不自动修复。

## 本章范围

覆盖数据从持久存储到工作负载的路径，以及模型和 checkpoint 的读写、传输和完整性。区分存储系统正常与任务实际获得足够数据。

## 二级主题地图

- **04.1 数据集、预处理、加载与缓存** — 已有[训练数据路径草稿](training-data-path.md)，具体配置与验证待补充。
- **04.2 本地、共享、对象与并行存储** — 待建设。
- **04.3 模型与 Checkpoint 的读写、传输和持久化** — 已有[持久化边界](checkpoint-durability.md)与[慢写/恢复 I/O 诊断](checkpoint-slow-io-triage.md)，具体后端与操作验证待补。
- **04.4 数据与文件完整性、版本和一致性** — 已有[Checkpoint 完整性与校验证据](checkpoint-integrity-evidence.md)（四层校验边界）；[持久化边界](checkpoint-durability.md)另有部分完整性说明，版本管理与一致性专题待补。
- **04.5 I/O 性能、数据饥饿与长尾** — 已有[分阶段观测与判断](training-data-path.md)和[饥饿诊断指南](data-starvation-triage.md)；性能基线和案例待补充。
- **04.6 存储异常、恢复与验证** — 待建设。

## 内容边界

- Checkpoint 文件写入、传输与持久性归本章；保存哪些训练状态、恢复到哪一步归 06。
- 模型文件分发和读取归本章；模型加载后的引擎执行及显存/设备内存管理归 07。
- 通用完整性判定和恢复目标引用 08；具体文件与数据证据归本章。

## NPU 内容位置

NPU 工作负载沿用本章的数据路径问题组织方式；涉及平台相关缓存、checkpoint 组件及框架适配时，显式记录环境和验证条件。

完整路径见[昇腾专题](../../paths/platforms/ascend.md)。其他平台入口见 [NVIDIA 专题](../../paths/platforms/nvidia.md)。

## 关联章节

- [05 集群平台与资源管理](../05-cluster-platform/index.md)
- [06 训练与后训练系统](../06-training/index.md)
- [07 推理与服务系统](../07-inference/index.md)
- [08 可靠性与计算正确性方法](../08-reliability/index.md)

## 已收集的原始资料入口

以下链接指向厂商或项目自己的资料；引用或改编前仍需核对对应版本、来源许可和适用范围。

- [MindCluster 官方仓库](https://github.com/Ascend/mind-cluster)：其中 MindIO 的 checkpoint 相关资料可用于识别 I/O 与训练恢复的内容边界。
- [ML Engineering 项目仓库](https://github.com/stas00/ml-engineering)：数据与存储工程资料入口。
- [AIInfra 项目仓库](https://github.com/Infrasys-AI/AIInfra)：集群存储和数据路径的背景资料。

## 首轮成果与后续

已有数据供给、checkpoint 持久化边界、慢写诊断与完整性校验分层；训练状态恢复由 06 的专题承接。后续补选定存储实现的实测与受控验证。

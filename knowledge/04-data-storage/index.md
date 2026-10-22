---
id: data-storage.index
title: 04 数据路径与存储系统
type: index
domain: data-storage
status: draft
platforms: [generic]
source_refs: [src.ascend.mind-cluster, src.stas.ml-engineering, src.infrasys.aiinfra]
updated_at: '2026-10-22'
summary: 组织数据加载、模型和 checkpoint I/O，以及完整性、持久化和存储异常。
related_ids: [data-storage.training-data-path, hardware.resource-topology, cluster-platform.index, training.index, inference.index, reliability.index, data-storage.checkpoint-durability, data-storage.data-starvation-triage, data-storage.checkpoint-slow-io-triage, data-storage.checkpoint-integrity-evidence, data-storage.local-and-shared-storage, data-storage.object-and-parallel-storage, data-storage.storage-workload-baselines, data-storage.storage-client-backend-recovery]
---

# 04 数据路径与存储系统

本页组织数据供给、四类存储样板、制品发布、完整性、性能与恢复方法。相关交付已完成原审阅范围内的修订和复核；正文仍为草稿，未经本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

## 已有正文

- [Checkpoint 写入与持久化边界](checkpoint-durability.md)：区分暂存、后台写入、提交、持久化和恢复验证。

- [训练数据供给路径与等待](training-data-path.md)：连接存储、缓存、加载、主机内存与设备消费，区分数据等待、传输等待和计算或通信等待的证据；已补数据集身份/游标契约（§A/§B）、NPU 传输分列与对照矩阵（§C）。

- [训练数据加载饥饿诊断指南](data-starvation-triage.md)：把取 batch 等待定位到存储、CPU 处理、队列、传输或消费的首个边界；以 PyTorch 2.6 DataLoader 与 profiler 为证据样板。

- [Checkpoint 慢写与恢复 I/O 诊断指南](checkpoint-slow-io-triage.md)：把保存/恢复慢定位到状态收集、staging 拷贝、后台写入、内核 writeback/fsync、存储后端或读路径。

- [Checkpoint 完整性与校验证据](checkpoint-integrity-evidence.md)：容器格式、框架元数据、存储层 scrub、应用自检四层校验各自能发现什么，外加校验原语对照、选定后端读路径责任、验证链与官方反例（修订已完成原范围审阅与复核，仍未实测）；DCP 2.6 无应用层校验和、MindIO checker 校验文件个数、Ceph deep scrub 默认不自动修复。

- [本地与共享文件存储版本化参考](local-and-shared-storage.md)：Linux v6.16 ext4/NVMe 与 NFSv4.1（RFC 8881＋nfs-utils 手册页）双样板，接口/缓存/一致性/持久性对照与负载选型。

- [对象与并行存储版本化参考](object-and-parallel-storage.md)：Ceph Squid RGW S3 与 Lustre 2.x 双样板，对象语义/分条/锁/一致性对照与最小验证设计。

- [模型制品与 Checkpoint 的传输、发布和读回](artifact-transfer-and-publication.md)：清单身份、暂存、传输、提交与读回，衔接推理加载和结果验证。

- [存储负载、容量与长尾基线口径](storage-workload-baselines.md)：负载身份、计时分层与长尾比较的条件。

- [存储客户端、后端异常与恢复验证](storage-client-backend-recovery.md)：区分客户端、后端和应用恢复边界，保留停止与复验要求。

## 本章范围

覆盖数据从持久存储到工作负载的路径，以及模型和 checkpoint 的读写、传输和完整性。区分存储系统正常与任务实际获得足够数据。

## 二级主题地图

- **04.1 数据集、预处理、加载与缓存** — [训练数据路径](training-data-path.md)包含数据集身份、预处理、缓存与游标契约；现场配置和测量仍需补齐。
- **04.2 本地、共享、对象与并行存储** — [本地与共享文件存储](local-and-shared-storage.md)与[对象与并行存储](object-and-parallel-storage.md)提供四类版本化参考和验证方法，真实后端行为仍须现场核对。
- **04.3 模型与 Checkpoint 的读写、传输和持久化** — [持久化边界](checkpoint-durability.md)、[慢写/恢复 I/O 诊断](checkpoint-slow-io-triage.md)与[制品传输发布读回](artifact-transfer-and-publication.md)串联状态、后端和读回判据；操作验证未执行。
- **04.4 数据与文件完整性、版本和一致性** — [完整性与校验证据](checkpoint-integrity-evidence.md)与[制品传输发布读回](artifact-transfer-and-publication.md)覆盖四层校验、版本身份和结果验证链；签名等未核对机制以各正文 unknown 为准。
- **04.5 I/O 性能、数据饥饿与长尾** — [负载容量长尾基线](storage-workload-baselines.md)连接[饥饿诊断](data-starvation-triage.md)与[Checkpoint I/O 诊断](checkpoint-slow-io-triage.md)；基线和案例材料的范围以所链正文为准。
- **04.6 存储异常、恢复与验证** — [客户端与后端恢复](storage-client-backend-recovery.md)衔接训练侧恢复检查；方法与真实恢复结果分开验收。

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

## 内容范围与后续维护

已有数据供给、checkpoint 持久化边界、慢写诊断与完整性校验分层；训练状态恢复由 06 的专题承接。后续补选定存储实现的实测与受控验证。

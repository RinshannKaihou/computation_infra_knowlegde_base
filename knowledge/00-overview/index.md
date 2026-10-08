---
id: overview.index
title: 00 导读与系统全景
type: index
domain: overview
status: draft
platforms: [generic]
source_refs: [src.infrasys.aiinfra, src.stas.ml-engineering]
updated_at: "2026-09-30"
summary: 建立系统全景、统一术语，并按任务与平台定位知识。
related_ids: [hardware.index, software-stack.index, training.index, inference.index, reliability.index, overview.training-lifecycle, overview.inference-lifecycle]
---

# 00 导读与系统全景

本页是内容导航草稿。训练与推理全流程已有正文，其余二级主题待补充；内容未经本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

## 已有正文

- [一次训练任务的端到端路径](training-lifecycle.md)：沿资源、数据、训练状态和进展选择下一层知识。
- [一次推理请求的端到端路径](inference-lifecycle.md)：连接请求、调度、缓存、输出与服务指标。

## 本章范围

说明知识库的范围、系统边界和阅读方式。从训练任务与推理请求的完整路径理解各组件的作用，再进入具体领域。GPU 与 NPU 均在覆盖范围内。

## 二级主题地图

- **00.1 范围、核心术语与系统边界** — 待建设。
- **00.2 一次训练任务的端到端路径** — 已有[全流程导航](training-lifecycle.md)。
- **00.3 一次推理请求的端到端路径** — 已有[全流程导航](inference-lifecycle.md)。
- **00.4 单机、集群与超节点的参考架构** — 待建设。
- **00.5 设计目标与约束：可靠性、性能、容量、成本、能耗** — 待建设。
- **00.6 按角色、任务与平台组织的阅读路径** — 待建设。

## 内容边界

- 本章组织全景和入口；硬件、软件栈及工作负载的具体机制在对应章节维护。
- 平台专题引用各章内容，不复制正文；术语解释需区分通用概念与厂商特定名称。

## NPU 内容位置

昇腾沿硬件、CANN 与框架、HCCL、集群管理、训练和推理逐层展开。平台差异和版本条件保留在相应条目中。

完整路径见[昇腾专题](../../paths/platforms/ascend.md)。其他平台入口见 [NVIDIA 专题](../../paths/platforms/nvidia.md)。

## 关联章节

- [01 物理设施与计算节点](../01-hardware/index.md)
- [02 系统软件与加速器执行栈](../02-software-stack/index.md)
- [06 训练与后训练系统](../06-training/index.md)
- [07 推理与服务系统](../07-inference/index.md)
- [08 可靠性与计算正确性方法](../08-reliability/index.md)

## 已收集的原始资料入口

以下链接指向厂商或项目自己的资料；引用或改编前仍需核对对应版本、来源许可和适用范围。

- [AIInfra 项目仓库](https://github.com/Infrasys-AI/AIInfra)：全栈主题组织与中文资料入口。
- [ML Engineering 项目仓库](https://github.com/stas00/ml-engineering)：从工程问题进入硬件、训练与推理等主题。

## 首轮成果与后续

已建立训练与推理端到端路径；后续补充术语、参考架构和不同角色的阅读顺序。

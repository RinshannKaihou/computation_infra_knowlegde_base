---
id: overview.index
title: 00 导读与系统全景
type: index
domain: overview
status: draft
platforms: [generic]
source_refs: [src.infrasys.aiinfra, src.stas.ml-engineering]
updated_at: '2026-10-22'
summary: 建立系统全景、统一术语，并按任务与平台定位知识。
related_ids: [hardware.index, software-stack.index, training.index, inference.index, reliability.index, overview.training-lifecycle, overview.inference-lifecycle, overview.terms-and-system-boundaries, overview.reference-architectures, overview.design-targets-and-tradeoffs]
---

# 00 导读与系统全景

本页组织六个导读主题：系统边界、训练与推理路径、参考架构、设计权衡和阅读路径。内容均为草稿，未经本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

## 已有正文

- [一次训练任务的端到端路径](training-lifecycle.md)：沿资源、数据、训练状态和进展选择下一层知识。
- [一次推理请求的端到端路径](inference-lifecycle.md)：连接请求、调度、缓存、输出与服务指标。
- [统一术语、先修关系与系统责任边界](terms-and-system-boundaries.md)：九领域共用术语、同名异义与按症状定位责任领域的方法。
- [单机、集群与超节点的参考架构及选择](reference-architectures.md)：三类组织的控制/数据/管理路径、GB200 NVL72 与 Atlas 900 A3 SuperPoD 超节点样板、DGX SuperPOD 集群样板、约束比较与部署核对清单。
- [设计目标与约束的权衡](design-targets-and-tradeoffs.md)：可靠性、性能、容量、成本、能耗五类目标的统一口径、有效产出定义、能耗测量边界、两个假设计算示例与三窗口验收表。
- [按角色组织的阅读路径](../../paths/roles/reading-by-role.md)：学习者/架构设计者/运维可靠性人员三条路径的进入条件、阅读顺序、可回答问题与完成检查。
- 任务路径（准备阶段）：[选型与容量](../../paths/tasks/selection-and-capacity.md) · [节点验收](../../paths/tasks/node-acceptance.md) · [环境安装](../../paths/tasks/environment-installation.md)；（运行阶段）[性能优化](../../paths/tasks/performance-optimization.md) · [迁移与升级](../../paths/tasks/migration-and-upgrade.md) · [故障恢复](../../paths/tasks/fault-recovery.md)；排障首要入口另见[训练排障](../../paths/tasks/training-triage.md)与[推理排障](../../paths/tasks/inference-triage.md)。

## 本章范围

说明知识库的范围、系统边界和阅读方式。从训练任务与推理请求的完整路径理解各组件的作用，再进入具体领域。GPU 与 NPU 均在覆盖范围内。

## 二级主题地图

- **00.1 范围、核心术语与系统边界** — 已有[统一术语、先修关系与系统责任边界](terms-and-system-boundaries.md)。
- **00.2 一次训练任务的端到端路径** — 已有[全流程导航](training-lifecycle.md)。
- **00.3 一次推理请求的端到端路径** — 已有[全流程导航](inference-lifecycle.md)。
- **00.4 单机、集群与超节点的参考架构** — 已有[参考架构及选择](reference-architectures.md)（三类概念架构＋两个官方超节点样板＋集群样板＋核对清单）。
- **00.5 设计目标与约束：可靠性、性能、容量、成本、能耗** — 已有[设计目标与权衡](design-targets-and-tradeoffs.md)（口径表＋假设计算示例＋验收表模板）。
- **00.6 按角色、任务与平台组织的阅读路径** — 已有[三角色阅读路径](../../paths/roles/reading-by-role.md)（2026-10-21 交付）、六条任务路径（选型/验收/安装、性能/迁移/恢复，2026-10-22 交付）与三平台入口收口（[昇腾](../../paths/platforms/ascend.md) · [NVIDIA](../../paths/platforms/nvidia.md) · [AMD](../../paths/platforms/amd.md)，AMD 入口 2026-10-22 新增）；排障入口[训练](../../paths/tasks/training-triage.md)/[推理](../../paths/tasks/inference-triage.md)。

## 内容边界

- 本章组织全景和入口；硬件、软件栈及工作负载的具体机制在对应章节维护。
- 平台专题引用各章内容，不复制正文；术语解释需区分通用概念与厂商特定名称。

## NPU 内容位置

昇腾沿硬件、CANN 与框架、HCCL、集群管理、训练和推理逐层展开。平台差异和版本条件保留在相应条目中。

完整路径见[昇腾专题](../../paths/platforms/ascend.md)。其他平台入口见 [NVIDIA 专题](../../paths/platforms/nvidia.md)与 [AMD 专题](../../paths/platforms/amd.md)。

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

## 内容范围与后续维护

已建立训练与推理端到端路径、统一术语与系统责任边界、参考架构与设计目标权衡、三角色阅读路径、六条任务路径与三平台入口（角色路径 2026-10-21，任务路径与 AMD 入口 2026-10-22，T00-05/06/07/08）。00.6 已随 Batch 32 审阅闭环（16 项发现全部 CLOSED）升为已覆盖（基础）；导航页均 draft、未实测。

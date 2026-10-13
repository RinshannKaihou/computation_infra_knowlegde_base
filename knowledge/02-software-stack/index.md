---
id: software-stack.index
title: 02 系统软件与加速器执行栈
type: index
domain: software-stack
status: draft
platforms:
- generic
source_refs:
- src.ascend.torch-npu
- src.ascend.agent-skills
- src.infrasys.aiinfra
updated_at: '2026-10-09'
summary: 组织驱动、运行时、编译器、算子与框架适配，并记录环境配套条件。
related_ids:
- software-stack.layers-and-boundaries
- software-stack.compatibility-evidence
- software-stack.ascend-documented-profile
- hardware.index
- cluster-platform.index
- training.index
- inference.index
- software-stack.nvidia-documented-profile
- software-stack.ascend-version-mismatch-triage
- software-stack.ascend-version-mismatch-source-case
- software-stack.ascend-version-mismatch-experiment
- software-stack.ascend-memory-oom-evidence
- software-stack.ascend-op-graph-failure-triage
- software-stack.host-resource-pressure-and-device-access
- software-stack.runtime-execution-and-library-loading
- software-stack.amd-rocm-documented-profile
- software-stack.operators-compilers-and-graphs
- software-stack.gpu-op-graph-failure-triage
- software-stack.framework-backend-adaptation
- software-stack.gpu-memory-oom-evidence
- software-stack.dtype-layout-and-precision-semantics
---

# 02 系统软件与加速器执行栈

本页是内容导航草稿。首批正文见下方阅读顺序，二级主题仍有待补充；所有文章均为草稿，尚未开展本地环境实测。`generic` 表示跨平台导航，不表示所有环境兼容。

## 首批正文与阅读顺序

1. [主机到模型执行的软件栈分层](layers-and-boundaries.md)：先辨认组件职责、调用关系与故障归属。
2. [如何判断版本配套是否有依据](compatibility-evidence.md)：区分官方配套声明、源码状态与本地验证。
3. [昇腾软件栈的文档配套档案](ascend-documented-profile.md)：用固定版本的来源展示已知约束和未知条件。

4. [NVIDIA 软件栈的文档配套档案](nvidia-documented-profile.md)：固定容器标签与各层来源，保留官方文本冲突及未知条件。
5. [昇腾 NPU 内存与 OOM 证据](ascend-memory-oom-evidence.md)：区分物理设备内存、框架分配/保留、workspace 与碎片，固定 TorchNPU/CANN 来源版本。
6. [驱动初始化、运行时执行同步与库装载](runtime-execution-and-library-loading.md)：CUDA / CANN / HIP 的初始化、stream/event 同步、错误发现时机与实载库身份记录。
7. [OS/进程资源压力与设备访问诊断](host-resource-pressure-and-device-access.md)：cgroup/内存压力/限额/命名空间与三平台设备节点的分层取证和隔离对照方法。
8. [AMD ROCm 软件栈的文档配套档案](amd-rocm-documented-profile.md)：ROCm 10.1.0 × MI300X × Ubuntu 24.04.5 样板的组件版本、兼容矩阵、PyTorch 构建关系与验证入口。
9. [算子分发、编译与计算图执行机制](operators-compilers-and-graphs.md)：四种「图」的区分、Dynamo/Inductor、TorchAir/aclgraph、HIP graphs 的固定样板对照与缓存身份方法。
10. [GPU 算子、编译和图执行失败的定向诊断](gpu-op-graph-failure-triage.md)：NVIDIA/AMD 路径的四分支取证、诊断工具与 eager/compile/cache 对照。
11. [框架到设备后端的适配与能力核对](framework-backend-adaptation.md)：PrivateUse1 责任清单、三路径核对表、opcheck/gradcheck 与编译缓存身份测试。
12. [GPU 分配器、保留内存与 OOM 证据](gpu-memory-oom-evidence.md)：allocated/reserved、碎片键、workspace 独立账户、记录表与三对照。
13. [dtype、layout、格式转换与有限精度语义](dtype-layout-and-precision-semantics.md)：五层语义区分、三平台精度开关条件句与最小检查四步。

两份平台档案都是文档研究基线；实际部署和诊断仍需补齐目标环境信息。

## 本章范围

覆盖主机操作系统到加速器执行的依赖链、平台运行时、框架后端和数值语义。重点说明组件边界、版本条件以及环境变更如何影响执行。

## 场景指南、案例与实验

以下均为来源整理草稿；公开案例不代表本库复现，实验仅为设计。

| 主题 | 诊断指南 | 来源案例 | 实验设计 |
|---|---|---|---|
| 昇腾版本配套 | [指南](ascend-version-mismatch-triage.md) | [案例](ascend-version-mismatch-source-case.md) | [实验设计](ascend-version-mismatch-experiment.md) |
| 昇腾算子不支持与图编译失败 | [指南](ascend-op-graph-failure-triage.md) | 待补充 | 待补充 |


## 二级主题地图

- **02.1 OS、进程、主机资源与设备访问** — 已有[OS/进程资源压力与设备访问诊断](host-resource-pressure-and-device-access.md)。
- **02.2 驱动、运行时与基础库** — 已有[分层概念草稿](layers-and-boundaries.md)与[驱动初始化、运行时执行同步与库装载](runtime-execution-and-library-loading.md)。
- **02.3 CUDA、ROCm、CANN 等平台软件栈** — 已有[跨平台分层入口](layers-and-boundaries.md)（三栈职责对照）、[昇腾档案](ascend-documented-profile.md)、[NVIDIA 档案](nvidia-documented-profile.md)与[AMD ROCm 档案](amd-rocm-documented-profile.md)。
- **02.4 算子、编译器、计算图与执行模式** — 已有[算子分发、编译与计算图执行机制](operators-compilers-and-graphs.md)（四层区分+三平台固定样板）、[昇腾算子不支持与图编译失败诊断](ascend-op-graph-failure-triage.md)与[GPU 算子、编译和图执行失败的定向诊断](gpu-op-graph-failure-triage.md)。
- **02.5 框架与设备后端适配** — 已有[职责边界草稿](layers-and-boundaries.md)与[框架到设备后端的适配与能力核对](framework-backend-adaptation.md)（PrivateUse1 责任清单 + 三路径核对 + MindSpore/vLLM 对照）。
- **02.6 内存管理、数据格式与精度语义** — 已有[昇腾 NPU 内存与 OOM 证据](ascend-memory-oom-evidence.md)（固定 TorchNPU/CANN 版本，2026-10-09 补齐主机传输/stream 同步/non_blocking 原生语义）、[GPU 分配器、保留内存与 OOM 证据](gpu-memory-oom-evidence.md)与[dtype、layout、格式转换与有限精度语义](dtype-layout-and-precision-semantics.md)。
- **02.7 环境配套、安装验证、迁移与升级** — 已有[配套证据方法](compatibility-evidence.md)、[昇腾档案](ascend-documented-profile.md)和[NVIDIA 档案](nvidia-documented-profile.md)；已有[版本配套诊断](ascend-version-mismatch-triage.md)、案例与实验设计，真实安装/升级验证待补。

## 内容边界

- 底层设备访问和驱动初始化归本章；容器设备暴露、调度分配和任务运行环境归 05。
- 算子和数据类型的精度语义归本章；loss、梯度、优化器与收敛行为归 06。
- 兼容档案记录环境字段、已知约束和未知条件；具体训练或推理文章引用它，避免重复维护版本表。字段齐全不代表组合已获支持或实测。

## NPU 内容位置

CANN、驱动、框架与 torch_npu、算子包和执行模式均在本章定位。官方声明支持、团队实测和未知组合要分别记录，不能用单一版本号代替配套关系。

完整路径见[昇腾专题](../../paths/platforms/ascend.md)。其他平台入口见 [NVIDIA 专题](../../paths/platforms/nvidia.md)。

## 关联章节

- [01 物理设施与计算节点](../01-hardware/index.md)
- [05 集群平台与资源管理](../05-cluster-platform/index.md)
- [06 训练与后训练系统](../06-training/index.md)
- [07 推理与服务系统](../07-inference/index.md)

## 已收集的原始资料入口

以下链接指向厂商或项目自己的资料；引用或改编前仍需核对对应版本、来源许可和适用范围。

- [TorchNPU 官方仓库](https://github.com/Ascend/pytorch)：安装、框架适配与环境兼容资料入口。
- [Ascend Agent Skills](https://github.com/Ascend/agent-skills)：环境配置与适配任务的结构参考；本库尚未执行这些技能。
- [AIInfra 项目仓库](https://github.com/Infrasys-AI/AIInfra)：软件栈在基础设施体系中的上下文。

## 首轮成果与后续

已有分层（含三栈职责对照）、配套证据、三平台文档档案（NVIDIA/昇腾/AMD ROCm）、运行时初始化/同步/库装载参考、主机资源与设备访问诊断、算子/编译/图执行机制与 GPU 侧排障指南、框架后端适配核对、GPU 内存与 OOM 证据、精度语义基础，以及昇腾配套失败指南、案例和实验设计；后续补安装和升级验证。

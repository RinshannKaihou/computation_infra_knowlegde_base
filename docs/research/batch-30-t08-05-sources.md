# 第三十批 T08-05 来源记录

任务：T08-05（统一测试选择、压力/注入与统计方法；**new** `knowledge/08-reliability/test-design-and-coverage.md`，主题 08.7/08.1/08.3/08.4/08.6）。取证轮次：主会话作者角色首轮（2026-10-21；依赖 T08-01 已于 Batch 29 交付）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| "通过不证明可靠、失败一般证明不可靠"；零 MTTR；传统测试层级（unit/integration/system：smoke/performance/regression）；生产测试＝configuration test＋stress test；rollouts entangle tests；canary＝结构化用户 acceptance＋指数放量 0.1%→100%；break-glass；production probes 新旧组合 | src.google.sre-testing-reliability（**本轮新增**） | [SRE Book Ch.17](https://sre.google/sre-book/testing-reliability/)（2026-10-21 全文核读；CC BY-NC-ND 4.0；正确 URL 经目录页定位，`testing-for-reliability` 404） | Web 服务运维语境；不含 GPU/NPU |
| 统计显著性批评与效应量置信区间（ratio of means）；重复层级与随机效应；warm-up 计为成本 c1；最优重复数公式 Eq.13–14（只依赖相邻层方差比/成本比）；bootstrap CI（§7.2.1/§7.3.1）；CI 非重叠视觉检验的语义局限与正态性假设常被省略 | src.paper.kalibera-jones-effectsize-2020（**本轮新增**） | [arXiv:2007.10899](https://arxiv.org/abs/2007.10899)（2026-10-21 全文核读：§1–§2.3、§5–§7、§8.3.1） | 软件系统性能量化方法；集群迁移需重估方差/成本结构，公式数值不照搬；本库不给通用最小样本量 |

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| checkpoint 负载计次取平均、`drop_caches` 条件、强制 fsync（缓存与校验状态入规则的样板） | src.mlcommons.storage-rules-v2.0 | v2.0 规则（第二批/第十批已核） | 基准定义，非本库执行 |
| `-w` 预热、`-c` 校验不进计时 | src.nvidia.nccl-tests-b4d5beeb | README/实现（第九批已核） | 固定快照口径 |
| HCCL 性能测试参数与结果字段 | src.huawei.hccl-perf-test-guide-cann-9.1.x | 指南 0001/0004–0007（第九批已核） | CANN 9.1.X |
| 判据前置样板（CDF 相似度 α=0.95、单向距离、两阶段执行、MTBI 22.61× 为仿真） | src.usenix.superbench-atc24 | ATC 2024（第九/十二批已核） | Azure GPU |
| 注入只评估检测方法的边界（合成注入≠真实 SDC 证据） | src.ocp.sdc-in-ai-2025 / src.acl.sdc-llm-training-2502 | OCP §6.2.4；ACL §2.1（Batch 30 已核） | 机制性陈述 |
| 主动测试副作用与证据保全 | src.google.sre-effective-troubleshooting | 章节（2026-09-29 已核） | 方法论 |

## 本文原创部分

四类测试选择矩阵（七行维度×四类）、统计纪律八条（含预注册判据/无结果/停止记录）、注入六字段表与压力四声明、七份方案准备矩阵（内容取自库内七份实验正文的既有定义，汇总为本批原创）、"测试通过"四条边界汇总。

## unknown 清单

1. 各方案执行前均缺环境档案（`environment_refs` 空）；0/7 执行状态以 plans/validation-backlog.yaml 为准。
2. 昇腾侧可控注入工具链未登记（FaultDiag 为诊断侧；ChaosBlade 类工具未在 NPU 环境取证）。
3. Kalibera-Jones 公式在 GPU/NPU 集群上的方差/成本参数无本地估计（需初始实验）。
4. SRE 章节未提供"验收层级"对应物；节点四层验收口径来自库内 01 域既有登记而非该章。

## 复核轮修订记录（初审后）

- C01：第二节第 5 条拆为均值类与尾分位类两段——Kalibera-Jones Eq.13–14 明确标注"优化均值区间精度"，尾分位估计另行声明对象/抽样单位/依赖/失败口径，区间方法来源未登记保持待定。
- C02：SuperBench 从"判据完全前置"改写为"离线学习判据、校准后固定、用于后续验证"（§3.4/Algorithm 2 学习自 build-out 全集、§3.1 周期更新），预注册与本库要求区分。
- C03：选择矩阵资源/风险两行改为按层级分列（只读层 vs 主动诊断 run level vs 通信/存储基准独占），不再按类别统一"分钟级/低"。
- C04：准备矩阵改为六列（环境档案/脚本与输入/预先判据/执行采集恢复/结果复核），状态按设计→冻结→执行→复核四层标注；结果复核按 V00 实例要求与编辑审阅区分。
- C05：精度方案改"已定义必须预注册的字段与判读规则，具体值待冻结"；NCCL/HCCL 时间窗口同理。
- C06：三倍缓存条件删除，改为按固定规则 L167–180 记录并照录正文（S<3M）与示例（3S vs M）的不一致，待上游澄清。
- C07：MLPerf 内联链接改指固定 commit 规则文件（registry 登记入口逐字对齐）。
- C08：Kalibera-Jones registry 修订 v1 日期（2020-07-21）与许可（CC BY 4.0，abs 页原页核对），正文来源核对节同步。
- C09："第七节"改为 docs/authoring-guide.md §7 批次审阅约定（相对链接）；指标篇分工条目改为"统计记账（事件损失、可用性与有效产出的合成计算例）"，不再承诺"效应量计算例"。

## 第二轮修订记录（复核后）

- C03：矩阵"风险与恢复"基准格改为独占资源/防污染/结束核对＋影响随占用升级（整机基准高影响口径），不再预设"低"。
- C07：MLPerf 内联链接改登记入口逐字一致（L167–180 移入文字）；DCGM Run Levels 两处链接均对齐登记入口（src.nvidia.dcgm-diag-user-guide-latest-2026-10-08 已加入 source_refs，节名入文字，不再带 fragment）。
- N01 补录：DCGM 取证行——src.nvidia.dcgm-diag-user-guide-latest-2026-10-08 为 latest 可变页（历史观察 2026-10-08 已登记 Run Levels and Tests 四级表/各插件前提/Exit Codes）；本轮（2026-10-21）作者按登记入口引用其 Run Levels and Tests 节定位分级语义，复核轮审阅方独立重读该节（日期与角色如实分开记录）；与固定 v3.3.9 源码快照分别登记、不作同一冻结版本。
- N01：随 C07 一并关闭（DCGM 依赖已登记）。

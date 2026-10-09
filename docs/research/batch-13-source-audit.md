# 第十三批来源与交付记录

**最新审阅状态（2026-10-09）：补充审阅及定向修订范围内通过。** 原 `gpt-6.1-sol / xhigh` 会话完成两轮只读复核：第一轮关闭 R01/R02/R04/R05；修订新增 R06 的 thermal 时间窗缺口后，第二轮关闭 R03/R06，无新增 R07。六个跟踪条目均 CLOSED，无剩余 OPEN/BLOCKED；R03/R06 对应同一处剩余缺口，不重复计数。过程、精确输入与证据边界见[复核汇总](batch-13-codex-rerecheck.md)、[第一轮](batch-13-codex-rerecheck-round-1.md)、[第二轮](batch-13-codex-rerecheck-round-2.md)和[修订记录](batch-13-rereview-revisions.md)。正文仍为 draft/source_checked，未执行硬件实验。

**此前审阅闭环（历史）：** 用户约定的 `gpt-6.1-sol / xhigh` 审阅、修订与两轮定向复核已完成；初审 15 项（2 P1、11 P2、2 P3）+ 复核新增 3 项（2 P2、1 P3）累计 18 项全部关闭，在当时原审阅范围内通过，见[初审记录](batch-13-codex-review.md)与[定向复核](batch-13-codex-recheck.md)。历史 B13-C01–C18 的编号、实际模型和 CLOSED 记录保留。0x80E20207/0x80E21007 的 xlsx 附件由编写者下载解析、独立审阅者未取得，该来源链已在复核记录中如实标注，本次仍未独立取得。

2026-10-08 补充审阅阶段新增 3 项来源登记（119→122）：HDK 26.1.x A2 DCMI LP 页面、Linux v6.16 proc/cpuset 固定源码与 PyTorch 2.6 activation checkpointing 文档。2026-10-09 修订复核另补登原审阅者取得的 numactl 固定 man 源码（122→123），与原 man7 镜像 revision 分开。下文集成数量与此前修订重点保留为历史口径；当前关闭依据以两轮原报告为准。

集成日期：2026-10-08。本批为 full-coverage 路线图第一个执行批次（Batch 13，full-coverage-backlog 的 T00-01/T01-01/T01-02/T01-03/T01-04），由 Kimi 编写，五路探索子代理完成取证、两路完成审阅修订定点复核。全部保持 draft；四篇新正文与一篇修订均为限定来源范围的 source_checked，无 reproduced。

## 本批正文

| 任务 | 正文 | 类型 | 备注 |
|---|---|---|---|
| T00-01 | [统一术语、先修关系与系统责任边界](../../knowledge/00-overview/terms-and-system-boundaries.md) | reference | 新增 |
| T01-01 | [机柜供电、散热预算与共享依赖](../../knowledge/01-hardware/rack-power-cooling-and-failure-domains.md) | concept | 新增 |
| T01-02 | [供电、散热与性能退化证据](../../knowledge/01-hardware/power-thermal-evidence.md) | reference | 修订（训练 NPU 补齐） |
| T01-03 | [NUMA、主机内存与 I/O 局部性的成对验证](../../knowledge/01-hardware/numa-memory-and-io-locality.md) | procedure | 新增 |
| T01-04 | [加速器执行单元、内存层次与数据移动机制](../../knowledge/01-hardware/accelerator-execution-and-data-movement.md) | concept | 新增 |

来源记录：[术语](batch-13-terms-sources.md)、[机柜供电散热](batch-13-rack-power-sources.md)、[训练 NPU](batch-13-training-npu-power-sources.md)、[NUMA](batch-13-numa-locality-sources.md)、[加速器执行](batch-13-accelerator-execution-sources.md)。任务清单：[plans/full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml)。

## 来源变化

新增 35 项登记（总计 84→119）：术语 3 项（k8s 架构/CRI/Volcano PodGroup）+ 机柜 5 项（Redfish schemas 2026.2、SuperPOD DC 设计、GB200 UG、HPE QuickSpecs、Supermicro 数据表）+ 训练 NPU 4 项（HDK 26.1.x A2/A3 npu-smi、A2/A3 故障定义）+ NUMA 10 项（v6.16 内核文档×3、cgroup v2、numactl man、hwloc×2、AMD 58012、CACM×2）+ 加速器 10 项（H100 白皮书镜像/博客/cuda-samples、CDNA2 白皮书/MI200 ISA/HC34/HIP 6.3.3、CANN 8.2 架构与 memcpy、Atlas UG 26）+ 复核补登 3 项（MIG 设备名、H100 产品页、rocm_bandwidth_test d7f5efe）。

扩充/修订既有登记：src.stas.ml-engineering 与 src.infrasys.aiinfra 回填固定 commit（fb75494c、b97c0385；AIInfra 许可由 unknown 更新为 partial：正文 Apache-2.0 / LICENSE-CODE MIT 主体为 Microsoft）；审阅修订更新 9 项（superpod-dc-design、hpe-quickspecs、supermicro-datasheet、hdk-26.1x-a2-npu-smi、atlas-800t-a2-user-guide-26、cann-82rc1alpha001-ascendc-aicore-arch、cann-82rc1alpha001-acl-memcpy、docs-sysctl-kernel-v6.16、numactl-man-pages）；顺带修复 src.pytorch.cuda-semantics-2.6 notes 的 ` #` 未加引号静默截断（既有问题，本批发现并修正）。

## 修订后的重点边界（2026-10-08）

- 术语：主归属规则明确「尚无专题正文的术语其当前定义即本页条目」；设备/逻辑视图不一一对应（MIG 反例）；worker/runtime/checkpoint 同名异义各有官方页面锚点；SRE 排障章归属 SRE Book 第 12 章（非 workbook）。
- 机柜：配电公式按接法分开（Wye 行可复现、Delta 行按表列值并标注不可复现）；容量定额（≥50%）与负载分配（≤50%）为两方向条件；HPE「1.5x TDP ≈192 kW」算术出入保留原文；Supermicro「total power 132kW」与 8×33=264 歧义照录；单路失效=冗余降级而非必然降性能；Redfish schema≠设备实现，Thermal 已废弃。
- 训练 NPU：HDK 26.1.x 训练线 npu-smi 字段/单位/支持矩阵（含 Atlas 800T A2、900 A2 PoD）已补齐；Aicore Freq 无「标称」语义，curFreq 差异可由空闲/策略产生；负面确认限定为「已核对页面中无 reason 位图类公开接口」，pwm 类型在 help 清单但机型支持未核；降P启动 HCCS 款两查询途径、PCIe 款仅设备侧；事件级降频机制（0x80E20207 高温温控、0x80E21007 ACG/POWERBRAKE 快速降频）为编写者解析 xlsx 的限定归纳；设施/BMC/设备/应用四层关联表给出，时钟偏差未知时不做跨层最早异常排序。
- NUMA：first-touch 为分配起点倾向非落点保证；numa_balancing 为位掩码（0/1/2/3）；成对测量证据链区分 允许集（/proc/status）/执行位置采样（task stat）/进程驻留分布（numastat -p，MB；numa_maps，页）/应用指标，系统级 numastat 仅背景；「未支持该候选」而非「排除 NUMA」；Gaud 反例（局部率更高不必然更快）保留。
- 加速器：三平台代际（H100 SXM5、MI200、Atlas A2）真实术语不映射；H100 白皮书为第三方镜像+官方博客交叉（原链失效），显存带宽 3000 GB/s preliminary vs 产品页 3.35 TB/s（SXM）/3.9 TB/s（NVL）分列；220 CU/880 Matrix Core 出自 AMD 署名 HC34 deck；Ascend buffer 容量无官方数值（0010 表 1 六行描述已补）；HCCS 为每路 7 链路合计 392GB/s；路径分四层（H2D/D2H、D2D、设备内 global↔片上、互联），同步分两层（host↔stream、kernel 内/流水）；异步拷贝前提（pinned/对齐/aclrtMallocHost）齐备。
- 全部正文未执行真实环境验证；procedure 的 environment_refs 为空并注明缺失条件。

## 集成时检查

`make check` / `make build` 通过：73 content entries / 119 sources（新增 4 篇正文、35 项来源，修订 1 篇正文与 2 项来源登记，另修 1 处既有 YAML 截断）。catalog 中四篇新条目标题与摘要已核对。结构检查只证明结构与引用，不代表技术正确性或远程内容有效性。

## 2026-10-09 修订复核收尾

本轮修改四篇正文及相关研究/来源记录，新增三份复核报告与修订记录；第五篇加速器正文未修改。健康定义 xlsx 未独立取得、npu-smi 全量扫描为编写者记录、本地版本和权限、机房实测、A3 事件等限制继续保留。模型审阅不建立硬件验证。

最终集成后，主执行者实际运行 `make check`、`make build`，两项退出码均为 0，PASS: 73 content entries / 123 sources；构建生成 build/catalog.json 与 build/catalog.md。正文及研究记录技术输入指纹保留，未执行硬件验证。

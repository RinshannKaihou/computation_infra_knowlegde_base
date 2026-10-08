# 第十批审阅记录（gpt-6.1-sol / xhigh）

**修订后最终状态（2026-10-08）：** 2 项 P2 已逐项修订并定向复核关闭，本批在初审范围内通过，见[定向复核](batch-10-11-12-codex-recheck.md)。下文初审发现、原输入位置与当时结论保留为历史。

审阅日期：2026-10-08。审阅者：本会话 Codex 主助手，运行上下文确认模型为 `gpt-6.1-sol / xhigh`；正文编写者为 Opus。按用户更新的模型约定重新读取正文与上游证据，未派发子代理。此前[替代复查](batch-10-substitute-review.md)作为历史记录保留。

**初审结论（历史）：审阅完成，暂不通过；2 项 P2 开放，无 P1/P3。** 本次交付审阅发现与关闭条件，正文保持审阅输入版本。对象 SHA-256、三批统计、结构检查和执行边界见[汇总](batch-10-11-12-codex-review-summary.md)。

## 范围与实际证据核对

完整读取[慢 rank 诊断](../../knowledge/06-training/slow-rank-triage.md)、[供电散热证据](../../knowledge/01-hardware/power-thermal-evidence.md)、[Checkpoint I/O 诊断](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md)，对应三份来源研究记录、来源审计、既有登记与任务/导航。

| 主题 | 本次重新取得并核对的上游证据 | 覆盖与限制 |
|---|---|---|
| 慢 rank | PyTorch `ba561023…` 的 ProcessGroupNCCL.cpp、TraceUtils.h、FlightRecorder.hpp；[NCCL 2.27.5 RAS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html) | 核对 desync、强制开启错误处理、心跳 480s、CPU 发现时间与 RAS 计数/离群展开条件；进度报告仍是诊断线索 |
| 供电散热 | DCGM `b0ec3c62…` 的 dcgm_fields.h、DcgmHealthWatch.cpp；[health monitoring](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html)、[exporter metrics](https://docs.nvidia.com/datacenter/dcgm/latest/reference/dcgm-exporter-metrics.html)、[diagnostics](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/dcgm-diagnostics.html)、[DGX 规格](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)；MindCluster `44385c13…` 的 collector_for_npu.go | usec 注释、热 watch 的默认一分钟窗口和 30s 最小采样、可选导出字段、PSU 降额与 NPU gauge 均有证据；未重读边缘线 PDF 或 Atlas 产品页，不新增其命令/单位保证 |
| Checkpoint I/O | PyTorch `1eba9b3…` 的 state_dict_saver.py、staging.py、filesystem.py；Linux `038d61fd…` 的 vm.rst；MindCluster `44385c13…` 的 save/flush 接口 | 核对默认 staging 阻塞、保存集合点、文件分桶、fsync 与串行读取；存储传输、MindIO 内部性能仍未知；未复验 MLPerf 工作负载 |

既有来源登记分别为 `src.pytorch.processgroupnccl-env-2.8`、`src.pytorch.distributed-2.8`、`src.nvidia.nccl-user-guide-2.27.5`、`src.nvidia.dcgm-v3.3.9`、DCGM 三项文档登记、`src.nvidia.dgx-h100-h200-user-guide-2026-01-26`、`src.ascend.mind-cluster-v26.1.1`、`src.pytorch.dcp-2.6`、`src.kernel.docs-sysctl-vm-v6.16`、`src.ascend.mindio-acp-v26.1.1`。latest 页面只证明本次取得的内容。

## 初审发现（历史，已关闭）

### B10-C01 / P2：RAS 未显示离群组不能证明全体变慢

- 位置：[慢 rank 诊断](../../knowledge/06-training/slow-rank-triage.md)第 65 行，步骤 1 的解释及下一步。
- 问题：正文把有/无离群组直接映射为个别/全体变慢。RAS 比较的是 communicator 上报的 collective 计数或状态，并按组大小决定是否展开成员；瞬态不平衡也会显示 MISMATCH。个别 rank 在计算或数据阶段变慢时，各 rank 可以仍有相同的最后 collective 计数，未展开成员也不能排除个别慢。
- 证据：[RAS 的 Sample Output](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output)说明查询窗口内计数差异、展开阈值及重复查询的限制，没有给出正文的二分判据。
- 影响：将缺乏进度差异的查询结果误当全体性退化，跳过 rank 级阶段证据。
- 关闭条件：改为“持续计数差异提供候选 rank；无差异/未展开时保持未定”，结合 verbose、完整性/响应状态和各 rank 阶段时间线再决定分支；同步来源研究记录中的推断边界。

### B10-C02 / P2：writeback 等待被误写成排除存储后端

- 位置：[Checkpoint I/O 诊断](../../knowledge/04-data-storage/checkpoint-slow-io-triage.md)第 65 行，步骤 4。
- 问题：“慢在内核而不是存储”把观察到的等待层当成互斥根因。脏页积累及写者节流也可以是后端消化速度不足的结果；仅有 dirty 阈值命中不能排除后端。该行“超过后台阈值后才开始刷出”也遗漏其他写回触发条件。
- 证据：[固定 vm.rst L165–242](https://github.com/torvalds/linux/blob/038d61fd642278bab63ee8ef722c50d10ab01e8f/Documentation/admin-guide/sysctl/vm.rst#L165-L242)分别说明后台阈值、写者阈值、脏页老化和周期写回；它不支持将后端排除的结论。
- 影响：慢后端造成的节流可能被归为独立内核问题，诱导错误的参数处置方向。
- 关闭条件：保留“等待发生在 writeback/写者节流”的定位，根因继续与同窗口后端吞吐/延迟/错误对照；去掉“才”和排除后端的表述，区分观察层与候选原因。

## 初审结束状态（历史）

B10-C01、B10-C02 均开放，等待正文与研究记录修订及定向复核。供电散热篇本次抽查范围未新增发现，不等于所有外部材料已经重新完整核对。三篇继续 `draft / source_checked`，没有设备或存储执行结果。

## 修订后最终状态

B10-C01–C02 全部 CLOSED。具体改动、与上游证据的定向对照及修订后文件身份见[复核记录](batch-10-11-12-codex-recheck.md)。本批在原审阅范围内通过；三篇仍为 `draft / source_checked`，没有真实环境执行结果。

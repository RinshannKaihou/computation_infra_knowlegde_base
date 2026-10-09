# Batch 13 补充审阅修订记录

日期：2026-10-09。主执行者依据用户“直接进行修订”的授权落实 [B13-R01–R05](batch-13-codex-rereview.md)。当前状态：**R01–R06 均 CLOSED，补充审阅及定向修订范围内通过。** 第一轮和第二轮的中间状态、指纹与关闭前提保留为历史。

历史 B13-C01–C18 的编号、实际模型与 CLOSED 记录保留。此次修改不提升硬件验证状态：四篇修改正文仍为 `draft` / `source_checked`，未改稳定 ID，未查询设备、设置绑定、运行负载或操作供电散热。

| 发现 | 修订与同步范围 | 证据与关闭前提 |
|---|---|---|
| B13-R01（P2） | 供电散热正文、训练 NPU 来源记录及 npu-smi/DCMI 登记；限定 npu-smi 负面扫描范围，加入独立 DCMI 当前原因、100ms 更新、无历史查询、IDLE 与故障区别及表 3 支持边界 | 主执行者重新取得 [HDK 26.1.x A2 dcmi_077](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_077.html)，已核对子命令、表 1–3；需原审阅者确认正文不再泄漏平台“无接口”结论 |
| B13-R02（P2） | NUMA 正文的表、步骤、判断分支、停止/完成条件，NUMA 来源记录及三个相关来源 notes；分开允许集、任务/VMA 策略、最近 CPU 样本、驻留和应用指标；覆盖关键 TID/子进程 | 重取 Linux v6.16 固定 proc/cpuset 源码、NUMA 策略文档 L15–69/L429–481、proc.rst L683–715；需确认允许集未被用作策略证明、主线程未代表全部任务 |
| B13-R03（P2） | 供电散热正文、batch 10 GPU 来源记录及固定 DCGM 登记；GPU thermal 分支限定范围，GPU power 保留 ret=OK / blank / 非 NOT_SUPPORTED 条件和 POWER_UNREADABLE 告警 | 重取固定 [MonitorPower L1612–1687](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1612-L1687)；需确认被动与 violation-only 未混同，WARN 按实体及具体错误码解释 |
| B13-R04（P3） | 机柜正文、机柜来源记录及 DMTF 登记；采用 FanSpeedsPercent 数组，单数 FanSpeedPercent 自 v1.1.0 废弃，仅作兼容，缺失/null 不当作 0% | 重取 [PowerSupplyMetrics v1.3.0 JSON](https://redfish.dmtf.org/schemas/v1/PowerSupplyMetrics.v1_3_0.json) 的两属性及版本标记；仍不证明设备实现 |
| B13-R05（P3） | 术语正文与元数据、术语来源记录、AIInfra/PyTorch 登记；改用 PyTorch 2.6 activation checkpointing 机制页，撤下 AIInfra 占位章节的技术引用 | 重取 [PyTorch 2.6 checkpoint](https://docs.pytorch.org/docs/2.6/checkpoint.html#torch.utils.checkpoint.checkpoint)；需确认引用支持“以计算换内存”，机制本身不提供持久化训练状态 |

来源限制保留：健康管理故障定义 xlsx 由编写者取得，独立审阅者未重新取得；A3 事件、现场版本配套、DCMI 实际可用性、设备到 NUMA 实测及机房条件仍未验证。历史数量与结论按各自日期理解。

## 定向复核安排

已继续原审阅会话 `01a11c1a-4fb4-7f73-a0a3-d97e5f379dff`，模型/effort 沿用 `gpt-6.1-sol / xhigh`，两次完整复核均显式设置 `read-only`。范围是上述五项修订、相关研究记录及登记表，包含修订引入的直接回归；不以结构检查或主执行者自查代替审阅关闭结论。

## 修订后输入指纹与初步结构检查

以下 SHA-256 固定本轮定向复核输入；不表示工作区干净。

| 文件 | SHA-256 |
|---|---|
| `knowledge/00-overview/terms-and-system-boundaries.md` | `055bd82e176f9534cc719fe448dcfed73c712dbbddfd588a959ebfed89a43b91` |
| `knowledge/01-hardware/rack-power-cooling-and-failure-domains.md` | `11ea7e42e1454635659b6a44490055b563817d43c7aaaa8ec6af7e3059cfd7b0` |
| `knowledge/01-hardware/power-thermal-evidence.md` | `6bbea31bb15ee3373437d5943700f01776b8dddfd7c603d0b622b7e26eda5346` |
| `knowledge/01-hardware/numa-memory-and-io-locality.md` | `b815f35bf4b20eb5065f90eb68c9508fa60b24566b8223852c07c79771ab5f40` |
| `knowledge/01-hardware/accelerator-execution-and-data-movement.md` | `242bdbaf8d0d3d9eaa929b45ea7ef0f309a5ac08a61420307f1584902a80bf14` |
| `docs/research/batch-13-training-npu-power-sources.md` | `4f777a78cefd0d55ab024b99eba6d8b91bc24b5a736e0db6b97501ec2f7e7357` |
| `docs/research/batch-13-numa-locality-sources.md` | `36a5feecd367b92d00e2f537566efb296c55ef72ffc26749020c05b83985cf4b` |
| `docs/research/batch-13-terms-sources.md` | `6712529b7af7aaedb5c234667e4b283a7faaa9ab5fba38728bed601646a9f07b` |
| `docs/research/batch-13-rack-power-sources.md` | `36d6664cc39131162fc9e7f80905c2c10da2c36c394c6b740ddaea3dae58137b` |
| `docs/research/batch-10-power-thermal-sources.md` | `9e97af42e98285cf02663e85bda2ef0b2ec2c1a01f14337058079a5d05d68eca` |
| `sources/registry.yaml` | `8056554995bfa8b4a95f5c2e42d71b0e22a1f2c83cdbb4b7ae47de1b4c1430f4` |

主执行者已运行 `make check`、`make build`：均返回 0，73 content entries / 122 sources；`git diff --check` 通过。仅确认结构、本地引用与构建，不关闭技术发现。

## 第一轮复核与 R06 补修

第一轮正常退出、返回码 0，11/11 输入指纹匹配；见[原报告](batch-13-codex-rerecheck-round-1.md)。R01/R02/R04/R05 CLOSED；R03 的不可读告警及实体范围修复成立，但新增 B13-R06（P3）指出 thermal 末端是 GetLatestSample，不受 endTime 截断，不能概括成严格历史窗口首末。R03 与 R06 是同一个剩余缺口，不重复计数。

主执行者已重取固定 MonitorThermal L1550–1609 与 MonitorPower L1612–1687；补修正文、batch 10 来源记录及 DCGM 登记，分开范围内起始值与该实体最新值、power 的范围内双端值，要求按实际样本时间归属历史事件。仍待原会话第二轮复核。

补登原审阅者第一轮取得的 numactl 固定源码 `src.numactl.man-sources-09fc1874`，不冒称为原 man7 镜像 revision；登记共 123 项。此前 11 个指纹为第一轮历史输入，第二轮使用下方新的输入指纹。

| 第二轮输入 | SHA-256 |
|---|---|
| `knowledge/01-hardware/power-thermal-evidence.md` | `f3e0361138959f5da8767fc3b2d639ff0662c25a3cb585cf5f7b1d89b670d1a4` |
| `docs/research/batch-10-power-thermal-sources.md` | `a8b67ec91e06d7c0c749383b70e6d8598cbd04c0356ac05bdca3189baa134c88` |
| `sources/registry.yaml` | `e2bba66f07cdefa0d138aae9bc7b77facfae56f64ff06b2835a173f62e98ccd3` |

## 第二轮关闭与最终集成

原审阅者第二轮正常退出、返回码 0；3/3 第二轮输入匹配，重新取得固定 thermal/power 函数，判定 R03/R06 CLOSED，无新增 R07，累计 R01–R06 全部关闭。报告见[第二轮原文](batch-13-codex-rerecheck-round-2.md)，最终逐项状态见[复核汇总](batch-13-codex-rerecheck.md)。

主执行者集成前复核第二轮输入仍为 3/3 MATCH，第一轮其他 8 份文件保持原指纹。保存结论后仅将 DCGM 登记中的 pending 改为 CLOSED，更新记录及导航；正文和研究记录技术内容未再修改。以上不建立硬件复现或现场验证，内容仍为 draft/source_checked。

最终集成后，主执行者实际运行 `make check`、`make build`，两项退出码均为 0，PASS: 73 content entries / 123 sources；构建生成 build/catalog.json 与 build/catalog.md。正文及研究记录技术输入指纹保留，未执行硬件验证。

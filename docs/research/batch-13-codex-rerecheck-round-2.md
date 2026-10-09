主执行者集成说明（2026-10-09，Asia/Shanghai）：以下保留原会话第二轮报告全文。实际配置为 `gpt-6.1-sol / xhigh / read-only`，会话 ID `01a11c1a-4fb4-7f73-a0a3-d97e5f379dff`；进程正常结束，退出码 0。主执行者在集成前再次核对第二轮 3/3 输入指纹匹配。累计状态见[复核汇总](batch-13-codex-rerecheck.md)。

# Batch 13 第二轮只读定向复核报告

## 1. 日期、配置与审阅边界

- **取证日期：2026-10-08（UTC）／2026-10-09（Asia/Shanghai）**，按同一次执行的两种日期口径记录，不作为日期冲突。
- **会话配置：`gpt-6.1-sol / xhigh`，显式 `read-only`。** 按用户指定配置记录；现有工具不能独立认证底层模型身份，不臆测或另行改写模型名称。
- **角色：原独立审阅者。** 本轮只核查 B13-R03／B13-R06 的同一个 thermal 时间窗缺口及修订引入的直接回归。
- **R01、R02、R04、R05 沿用第一轮 CLOSED；本轮没有重新逐项技术审阅这四项。**
- 未编辑文件、提交、生成子代理或另派模型；未读取凭据；未运行硬件、设备查询、绑定、负载或供电散热操作；未执行 `make build`。
- 主执行者的重取及自查记录仅作为修订说明，**不作为本轮关闭证据**。历史报告原文及状态保持不变。

## 2. 第二轮输入与指纹

### 实际读取范围

- `docs/research/batch-13-rereview-revisions.md:41`：第二轮修订说明及第 49–53 行新输入表。
- `docs/research/batch-13-codex-rerecheck-round-1.md:130`：R03 剩余缺口；第 191 行起 R06 的证据、建议和关闭条件。
- `docs/research/batch-13-codex-rerecheck.md:1`：累计状态及日期口径。
- `knowledge/01-hardware/power-thermal-evidence.md:89`、第 91 行：两条取样路径；同时核对元数据和第 153 行直接关联总结。
- `docs/research/batch-10-power-thermal-sources.md:22`：同步后的取样与归属边界。
- `sources/registry.yaml:584`：DCGM 登记，重点为第 597 行 notes。
- `sources/registry.yaml:1551`：numactl 固定源码补登；与第 1288 行 man7 镜像登记对照，仅检查登记一致性。

### SHA-256 核对结果

仅使用“第二轮输入”表的三个指纹，**未将较早的 11 项历史指纹用于本轮输入判定**。开始和结束前均独立计算，结果为 **3/3 MATCH**。

| 第二轮输入 | 实际 SHA-256 | 结果 |
|---|---|---|
| `knowledge/01-hardware/power-thermal-evidence.md` | `f3e0361138959f5da8767fc3b2d639ff0662c25a3cb585cf5f7b1d89b670d1a4` | MATCH |
| `docs/research/batch-10-power-thermal-sources.md` | `a8b67ec91e06d7c0c749383b70e6d8598cbd04c0356ac05bdca3189baa134c88` | MATCH |
| `sources/registry.yaml` | `e2bba66f07cdefa0d138aae9bc7b77facfae56f64ff06b2835a173f62e98ccd3` | MATCH |

以上固定本次输入，不证明工作区干净，也不替代技术审阅。

## 3. 独立上游证据

本轮通过 GitHub connector **重新取得** NVIDIA/DCGM 固定 commit：

`b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52`

实际完整读取两个目标函数：

1. [MonitorThermal，L1550–1609](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1550-L1609)
2. [MonitorPower，L1612–1687](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1612-L1687)

两次读取返回同一文件 blob SHA：

`1ff23bb905f1276a0f846551a44cd803a0c1034c`

浏览工具的 raw 入口获取返回 cache miss；**未将该失败视为取得原文，也未反复重试**。上述两段代码由 GitHub connector 成功独立取得，因此本轮不是仅依赖主执行者摘录或沿用前轮取样代码结论。

## 4. 逐项关闭判定

### B13-R06 — P3／CLOSED

**修订位置**

- `knowledge/01-hardware/power-thermal-evidence.md:89`
- `knowledge/01-hardware/power-thermal-evidence.md:91`
- `docs/research/batch-10-power-thermal-sources.md:22`
- `sources/registry.yaml:597`

**固定实现核对**

[MonitorThermal L1563–1607](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1563-L1607) 的实际语义为：

- `startTime` 为零时设为 `now − 60000000` 微秒。
- 起始样本通过带 `startTime`、`endTime` 的升序 `GetSamples` 取得。
- 第二样本通过该实体、该字段的 `GetLatestSample` 取得，调用没有传入 `endTime`。
- 比较两计数器值的非零差值，不能据此保证第二样本受指定历史查询上界约束。

[MonitorPower L1649–1687](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1649-L1687) 则分别通过同一 `startTime/endTime` 范围内的升序、降序 `GetSamples` 取得 violation 两端样本。

**关闭依据**

当前正文、研究记录及登记说明一致区分两条路径，并明确：

- 默认起点为当前时间减一分钟，**不等于实际两个样本严格相隔一分钟**。
- thermal 的最新样本不保证落在指定历史上界内。
- 历史归属须核对实际样本时间，时间未知时不按请求窗口归属 WARN。
- GPU power violation 的范围内双端取样与当前功耗不可读分支分开。

原“严格历史窗口首末”的未限定表述已消除。修订及本轮固定源码定向复核均已完成，**R06 关闭条件满足**。

### B13-R03 — P2／CLOSED

**修订位置**

- `knowledge/01-hardware/power-thermal-evidence.md:89`、第 91 行
- `docs/research/batch-10-power-thermal-sources.md:22`
- `sources/registry.yaml:597`

**本轮重新确认**

[MonitorPower L1629–1639](https://github.com/NVIDIA/DCGM/blob/b0ec3c624ea21e688b0d93cf9b214ae0eeb6fe52/modules/health/DcgmHealthWatch.cpp#L1629-L1639) 的功耗不可读分支要求同时满足：

- 取样返回 `DCGM_ST_OK`；
- 功耗值为 blank；
- 值不等于 `DCGM_FP64_NOT_SUPPORTED`。

该分支产生 `DCGM_FR_POWER_UNREADABLE` WARN，与 violation 差值分支分开。当前正文保留了完整条件，没有重新将 WARN 一律解释为功率节流，也没有扩张为任意查询失败都会产生该 WARN。

**关闭依据**

第一轮已独立确认的 passive／violation-only 区分、GPU／CPU 实体范围等修复继续保留；本轮未重新技术审阅 CPU thermal 路径。此前阻止 R03 关闭的唯一剩余问题是 R06 所述时间窗缺口，现已由修订和重新取得的两段固定实现确认消除。

因此，**R03 的剩余关闭条件满足，状态由 OPEN 转为 CLOSED**。R03 与 R06 始终作为同一个剩余技术缺口跟踪，不重复计数。

## 5. numactl 来源补登一致性

`sources/registry.yaml:1551` 的 `src.numactl.man-sources-09fc1874`：

- 指向固定 commit `09fc1874fdeb3836d7ea08c57299e9763a49028c`；
- notes 明确归属原审阅者**第一轮**实际取得的 man 源码；
- 与 man7 镜像的 revision 分开；
- 许可状态为 `unknown`，没有将镜像许可扩张为整仓库许可；
- 没有宣称运行工具或完成现场验证。

以上与第一轮实际取得范围一致。**本轮只确认补登一致性，未重新取得 numactl 上游、核验其许可或重新审阅 R02。**

## 6. 直接回归与来源边界

**本轮新增可行动直接回归：0 项；不新增 B13-R07。**

来源范围区分如下：

| 类别 | 本轮处理 |
|---|---|
| 本轮重新取得 | 固定 `MonitorThermal` L1550–1609、`MonitorPower` L1612–1687 |
| 沿用连续会话独立证据 | 第一轮已确认的 CPU thermal／实体分派、采样间隔及 numactl 固定源码取得记录 |
| 未重新取得、未扩大核验 | R01／R02／R04／R05 的其他上游来源及未修改技术内容 |
| 仍未独立取得 | 健康故障定义 XLSX；本轮不声称重新核验其事件定义 |

现场样本时间、设备版本及硬件行为没有被本轮实测。它们不构成本次文档取样语义关闭的阻塞条件，也不因关闭而变为已验证。

## 7. 结构检查及验证状态

本轮实际执行：

```text
PYTHONDONTWRITEBYTECODE=1 make check
退出码：0
PASS: 73 content entries; 123 sources.
```

只读环境产生不能创建 `/tmp/xcrun_db-*` 缓存的警告／错误信息；知识库检查仍实际运行并返回 PASS。登记数由 122 增至 123，与 numactl 来源补登一致。

该检查只确认结构及本地文件链接，不证明远程内容、技术正确性或硬件兼容性。未执行 `make build` 或任何硬件／负载实验。

`power-thermal-evidence.md` 仍为 **`draft` / `source_checked`**，没有提升验证等级。

## 8. 最终结论

**当前 Batch 13 补充审阅通过。**

- **本轮实际关闭：B13-R03、B13-R06。**
- **沿用第一轮关闭、未在本轮重新技术审阅：B13-R01、R02、R04、R05。**
- 累计六个跟踪条目均为 **CLOSED**；本轮新增问题 **0**，剩余 OPEN／BLOCKED **0**。
- 此结论仅覆盖既定补充审阅及此次定向修订，不代表重新完成全批无限范围审阅，也不建立硬件复现或现场验证保证。

本报告未修改仓库或历史报告；历史 OPEN 记录保留为当时状态，本报告提供第二轮关闭结论。
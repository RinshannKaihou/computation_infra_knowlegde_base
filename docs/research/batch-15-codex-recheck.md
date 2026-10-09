# 第十五批定向复核记录（gpt-6.1-sol / xhigh）

复核日期：2026-10-09。复核者：Codex 会话（resume），模型 gpt-6.1-sol / xhigh。复核对象为[初审记录](batch-15-codex-review.md)的 7 项发现及[修订记录](batch-15-review-fixes.md)。复核输出全文照录如下。

---
# Batch 15 定向复核报告

**最终结论：暂不通过。** 初审 7 项中，**6 项 CLOSED、1 项 OPEN**；修订另引入 **B15-C08（P2）**。B15-C06 的 OPEN 是本轮独立图像取证未完成，不是已确认正文仍有技术错误。

## 复核记录
- **复核日期：**2026-10-09，Asia/Shanghai。
- **模型 / effort：**用户约定为 `gpt-6.1-sol / xhigh`；本会话未暴露可核验的实际模型及 effort 运行元数据，因此记录为约定配置，不声称已独立确认执行配置。
- **范围：**核对四份修订正文、四份相关研究记录、修订摘要及相关来源登记；重新读取关键上游，未仅凭修订摘要关闭发现。
- **结构检查：**独立运行 `PYTHONDONTWRITEBYTECODE=1 make check`，**PASS：80 个内容条目、277 条来源**，计数为当前工作树整体结果，包含其他批次内容。四份正文仍为 `draft`，验证状态未提升为硬件复现。
- **操作边界：**未修改仓库，未运行 `make build`，未执行设备诊断、压测、安装或限额变更。

## 逐项判定

| 编号 | 判定 | 位置与复核结果 |
|---|---|---|
| **B15-C01／P2** | **CLOSED** | `knowledge/02-software-stack/host-resource-pressure-and-device-access.md:85`、`knowledge/02-software-stack/host-resource-pressure-and-device-access.md:189`：已分开时间窗差分与层级范围，保留非目标子组反例，并明确 `oom_kill` 不单独证明 `memory.max` OOM。固定 commit `038d61fd…` 的 `cgroup-v2.rst` L1443–L1491 与 L196–L203 支持这些修订，包括 `.local` 和 `memory_localevents` 例外；研究记录及登记 notes 已同步。citeturn885370view0 |
| **B15-C02／P2** | **CLOSED** | `knowledge/02-software-stack/host-resource-pressure-and-device-access.md:108`、`knowledge/02-software-stack/host-resource-pressure-and-device-access.md:175`：`FDSize` 已改为描述符表槽位容量，实际占用改查 `/proc/<pid>/fd`，并注明权限及采样竞争。固定 `proc.rst` Table 1-2 L265、§3.13 L2267 起，以及 `getrlimit(2)` 的 FD 编号上界定义，与修订一致。citeturn885370view1turn640100view0 |
| **B15-C03／P2** | **CLOSED** | `knowledge/02-software-stack/host-resource-pressure-and-device-access.md:102`：原有把系统级 `file-max` 混入 `EMFILE` 分支的问题已消除；`EMFILE`、`ENFILE` 和限额调整调用已分列，并要求记录失败的具体调用。符合初审关闭条件。**但替代表述另引入了 B15-C08，见下文。** `open(2)` ERRORS 确实将两种打开文件错误分列。citeturn748811search1 |
| **B15-C04／P2** | **CLOSED** | `knowledge/02-software-stack/host-resource-pressure-and-device-access.md:133`、`knowledge/02-software-stack/host-resource-pressure-and-device-access.md:192`：errno 已改作候选提示，联合核对设备身份、DAC/组权限、设备控制、seccomp 和安全审计；cpu-manager 历史案例已移入访问许可分支并保留版本限制。OCI v1.3.0 固定 commit `92249139…` 的 Seccomp 节及 `seccomp(2)` 支持默认 `EPERM`、不执行调用即返回 errno 的解释；新增来源登记与正文引用一致。citeturn885370view2turn469738search1 |
| **B15-C05／P2** | **CLOSED** | `knowledge/02-software-stack/runtime-execution-and-library-loading.md:214`、`knowledge/02-software-stack/runtime-execution-and-library-loading.md:227`：已删除“命令随队列删除”的推断，保留两种可能的销毁时机，并明确不建立任务取消或缓冲区可安全释放的保证。重新读取 HIP `docs-6.3.3`、页头 6.3.42134 的 `hipStreamDestroy` 段，修订与原文一致；研究记录也已同步。citeturn132292view0 |
| **B15-C06／P2** | **OPEN：取证阻塞** | `knowledge/01-hardware/node-acceptance-triage.md:105`、`knowledge/01-hardware/node-acceptance-triage.md:150`：正文已分列组件泛述与示例机型限制，保留当前 NIC 支持、`DURATION` 单位和 `--force` 语义的 unknown。但本轮只独立取得 Release 25.03、署期 2026-07-13 的 PDF 文本；第 76 页截图调用未返回本会话可判读的图像，故不能完成新增图像引文及结果表的独立复核。citeturn543456view0turn516605view0 |
| **B15-C07／P3** | **CLOSED** | `knowledge/02-software-stack/compatibility-evidence.md:152`、`knowledge/02-software-stack/compatibility-evidence.md:203`：已区分索引身份已取得与下载字节、`METADATA`、构建 commit/ABI、本地实测未取得。重新读取 PyPI 2.6.0.post3 的 Release files，六个完整文件名、平台标签及六个索引 SHA-256 均与档案清单一致；没有据此补出 abi1 或完整运行栈身份。citeturn535115view0 |

### B15-C06 的剩余关闭条件

提供审阅会话可独立判读、可追溯至同一 Release 25.03 PDF 的**第 76 页／印刷页 70**图像，完成以下核对：

- NIC 机型限定及非支持平台结果说明；
- `--no-prompt` 对该确认提示的作用；
- 示例结果表中的 NIC 状态及正文逐字引文。

随后确认正文、研究记录与图像一致即可关闭。**不要求推测补齐** `DURATION` 单位、`--force` 完整语义或当前全部机型支持矩阵。

## 新发现

### B15-C08 — P2：将调整限额时的 `EPERM` 反推为唯一的 `nr_open` 封顶

**位置：**
- `knowledge/02-software-stack/host-resource-pressure-and-device-access.md:108`
- `knowledge/02-software-stack/host-resource-pressure-and-device-access.md:193`
- `docs/research/batch-15-review-fixes.md:33`

**问题：**修订现在写“EPERM（setrlimit/prlimit）归限额调整被 nr_open 封顶”，步骤 6 更直接写成“setrlimit/prlimit 报 EPERM=硬限被 nr_open 封顶”。这把一个可能原因改写成唯一诊断结果。

**上游证据：**man-pages 6.19，`getrlimit(2)` 的 **ERRORS** 分列三种 `EPERM`：
1. 非特权进程提高硬限，缺少所需 `CAP_SYS_RESOURCE`；
2. 提高硬 `RLIMIT_NOFILE` 超过 `/proc/sys/fs/nr_open`；
3. `prlimit()` 调用者无权设置目标 PID 的限额。citeturn748811search0

因此，即使请求的新硬限远低于 `nr_open`，缺少相应能力的进程提高现有硬限仍可失败。仅记录调用名和 `EPERM` 不足以选择 `nr_open` 分支。来源登记自身已经记录前两种原因，正文的唯一归因也与登记不一致。

**关闭条件：**
- 将反向等号改为候选原因，分列能力不足、`nr_open` 上界和 `prlimit` 目标权限。
- 要求结合 `resource`、原软/硬限、请求值、`nr_open`、调用者能力及目标 PID 权限判断；证据不足保持 unknown。
- 同步修订步骤 6、修订摘要及相关研究说明；定向复核须覆盖“低于 `nr_open` 但无权提高硬限”的反例，不能再次仅凭 errno 定根因。

## 未取得材料与结论边界

- **本轮未独立取得可判读的 NVSM 示例图像。** 已取得其 PDF 文本和版本日期，但不能用编写者的 OCR 记录代替独立图像核验。
- 未下载 wheel、读取包内 `METADATA` 或进行字节摘要比对，也未取得本地整栈实测；这些仍是正文明确保留的缺口，不影响 B15-C07 的索引状态一致性关闭。
- 本轮仅复核七项修订及其引入的问题，**不撤销初审其他未覆盖声明，也不将原有 unknown／conflict／blocked 改为通过**。

**结论：暂不通过。** 需修正并定向复核 B15-C08，同时完成 B15-C06 的独立图像复核，才能宣布本轮定向复核通过。

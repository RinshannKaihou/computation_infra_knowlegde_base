# 第十五批定向复核记录·第二轮（gpt-6.1-sol / xhigh）

复核日期：2026-10-09。复核者：Codex 会话（resume），模型 gpt-6.1-sol / xhigh。复核对象：B15-C06/C08 的第二轮修订。**最终结论：通过，保留限定与证据缺口。** 复核输出全文照录如下。

---
# Batch 15 第二轮定向复核报告

**最终结论：通过——限于已审阅范围，并保留证据边界。**  
B15-C08 已关闭；B15-C06 按“编写者核对记录、未独立核验”的**限定状态关闭**。结合此前复核，B15-C01–C08 均已关闭；本轮未发现需要新增 B15-C09 的问题。

## 复核记录
- **复核日期：**2026-10-09，Asia/Shanghai。
- **模型 / effort：**用户约定为 `gpt-6.1-sol / xhigh`；本会话未暴露可核验的实际运行元数据，不将约定配置表述为已独立确认的执行配置。
- **范围：**两项剩余发现涉及的正文、研究记录、修订摘要与 registry notes；同时核对 Batch 13／B14-C10 的限定关闭先例。
- **结构检查：**独立运行 `PYTHONDONTWRITEBYTECODE=1 make check`，**PASS：80 个内容条目、277 条来源**，为当前工作树整体计数。未修改仓库、未运行 `make build`，未执行现场操作。

## 逐项判定

### B15-C08／P2：CLOSED

核对位置：
- `knowledge/02-software-stack/host-resource-pressure-and-device-access.md:108`
- `knowledge/02-software-stack/host-resource-pressure-and-device-access.md:193`
- `docs/research/batch-15-host-resource-sources.md:25`
- `sources/registry.yaml:2147`
- `docs/research/batch-15-review-fixes.md:33`

**关闭依据：**
- 正文与步骤 6 已删除“EPERM＝nr_open 封顶”的唯一归因，分列能力不足、`nr_open` 上界及 `prlimit()` 目标 PID 权限三种候选。
- 已加入“请求值低于 `nr_open`，但无权提高现有硬限仍可返回 EPERM”的反例。
- 判别输入已包括 `resource`、原软／硬限、请求值、`nr_open` 当前值、调用者能力与目标 PID 权限，并要求证据不足保持 unknown。
- 研究记录、registry notes 和第一轮修订摘要已同步，没有继续保留相反的现行结论。

重新读取 man-pages 6.19 `getrlimit(2)` 的 **ERRORS**：三条 `EPERM` 与上述修订一致；DESCRIPTION 对非特权进程提高硬限的限制也支持该反例。此反例是文档语义核对，不是本地调用实测。citeturn566742search0

### B15-C06／P2：CLOSED——限定为“编写者核对记录、未独立核验”

五处标注均已核对：

| 位置 | 结果 |
|---|---|
| `knowledge/01-hardware/node-acceptance-triage.md:36` | frontmatter 明确区分正文取得与图像的编写者 OCR 记录，注明独立审阅未能判读、未独立核验。 |
| `knowledge/01-hardware/node-acceptance-triage.md:53` | 缺口声明保留图像证据边界及参数、当前机型支持的 unknown。 |
| `knowledge/01-hardware/node-acceptance-triage.md:105` | 统一声明覆盖 NIC 机型限定及非支持平台结果说明、`--no-prompt` 提示作用、示例结果表三项；保留 PDF 链接与页码，不外推当前支持矩阵。 |
| `knowledge/01-hardware/node-acceptance-triage.md:150` | 来源记录明确取得方式、未独立核验状态及后续复核入口。 |
| `knowledge/01-hardware/node-acceptance-triage.md:155` | 独立图像复核继续列为待确认事项，未把限定关闭写成独立核验完成。 |

同步记录也一致：
- `docs/research/batch-15-node-acceptance-sources.md:33`、`docs/research/batch-15-node-acceptance-sources.md:66`、`docs/research/batch-15-node-acceptance-sources.md:80`、`docs/research/batch-15-node-acceptance-sources.md:89`
- `sources/registry.yaml:1925`

该处理符合 `docs/research/batch-14-codex-recheck-round-3.md:29` 的限定关闭先例：**接受完整披露来源取得差异的编写者记录，不将其升级为独立正确性背书。** 未发现实质性标注遗漏或相反声明，故不再要求为关闭此项补取图像；补取图像仍是提升独立核验状态的待补证据任务。

## 保留的证据边界
- NVSM Release 25.03 PDF **第 76 页／印刷页 70**的三项图像内容，仍属于编写者核对记录，**本轮未完成独立图像核验**；官方 PDF URL、版本和页码保持可追溯。
- `DURATION` 单位、`--force` 语义、`--no-prompt` 的完整行为及当前具体机型 NIC 压测支持继续为 unknown；历史示例不得作为当前全部机型支持矩阵或单独的操作依据。
- 初审已声明的其他未覆盖项，不因本轮通过而转为已独立核验；原有 unknown／conflict／blocked 不由本结论消解。
- 两篇本轮涉及的 procedure 仍为 `draft`、`verification.status: not_verified`。审阅通过与结构检查均不构成硬件验证、整栈兼容性认证、现场验收或操作授权。

**Batch 15 最终结论：通过，保留上述限定与证据缺口。**

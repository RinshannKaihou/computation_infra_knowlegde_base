# Batch 26 T07-01 第三轮定向复核

## 复核头部

- 审阅模型／推理档位：`gpt-6.1-sol / xhigh`。已核对本轮本地 Codex CLI 会话的 `turn_context.model` 与 `turn_context.effort`，仅有该模型与档位；已检查的审阅输出无 fallback 标记，未调用其他模型或子代理。
- 日期：2026-10-20（Asia/Shanghai）。
- 范围：仅核对[第二轮复核](batch-26-t07-01-codex-recheck.md)留下的 C08 两处来源记录与 C10 一处首失败分类表，共三处修订及必要邻接语境；其余 9 项沿用第二轮 CLOSED 结论，不重新审阅。
- 证据：重新读取三处本地修订及对应的[初审关闭条件](batch-26-t07-01-codex-review.md)，并于本日重开 MindIE-LLM [快速入门](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/)的“启动容器”“模型推理—启动服务／发送请求”段落。该页仍是 `latest`，未固定文档 commit，原有版本 gate 保留。本报告所列本地行号为本轮读取时位置。
- 执行边界：仅新增本报告；未执行服务启动、加载、请求、探针或共享内存清理，未开展硬件验证。
- 结构校验：在包含本报告的临时工作区副本中执行 `make check`、`make build`，均通过（108 content entries／534 sources）；仅证明结构与本地链接符合检查要求，不作为技术正确性证据，原工作区构建产物未改动。

## C08 — CLOSED

**两处来源记录已满足上轮剩余关闭条件。**

- [来源登记](../../sources/registry.yaml#L6627) L6627，`src.ascend.mindie-llm-doc-latest` 的 notes：已把清理表述限定为“特定容器部署语境”的上游示例，明确它是有状态变更；沿用前必须确认服务停妥、命名空间与归属、无其他消费者和既有授权，仅处理已识别的本实例遗留对象，并明确不得作为未限定环境的通配删除处方。
- [作者来源记录](batch-26-t07-01-sources.md#L62) L62：对应主张同步标明特定容器部署示例、有状态变更、停妥／归属／无他者／授权、仅本实例遗留和非通用通配处方。该表是压缩摘要，结合登记中明确的命名空间条件及[正文“失败清理”](../../knowledge/07-inference/model-loading-and-readiness.md#L153)的容器／IPC 范围限定，未形成另一条不受隔离条件约束的清理要求。

上游[快速入门“启动服务”注意事项](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/)确有切换用户后删除旧用户共享文件的宽泛示例，其前文为具体容器部署流程。修订保留该事实，同时将可执行对象收窄到已确认的本实例遗留；停妥、归属、隔离及授权限制是本库的操作边界，不冒充上游已保证所有现场满足这些条件。两处原有无条件清理要求均已消除，C08 关闭。

## C10 — CLOSED

**首失败分类表的残留逆命题已消除。**

[正文](../../knowledge/07-inference/model-loading-and-readiness.md#L141) L141 的“探针／假就绪”行现写为：“未观察到 `Daemon start success!`——就绪尚未证实（须结合日志完整性与实际请求判断，不能反推无服务）”。它明确区分未采集到成功日志与实际无服务，不再将充分观察标志倒推为必要条件；与同页 L87 的解释一致，满足上轮针对该行的剩余关闭条件。

上游[快速入门“启动服务／发送请求”](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/quick_start/quick_start/)将该日志作为启动成功标志，并另列请求验证示例；未给出“未观察到该日志即无服务”的逆命题。修订要求结合日志完整性与实际请求作判断，与该证据边界相符；这项逻辑判断属于审阅推理。C10 的其他已修部分沿用第二轮结论，不重开。

## 新发现

在上述三处修订及必要邻接语境内，未发现新增技术问题、过度声明或未标注推断。

## 整体结论

**通过。C08、C10 均为 CLOSED。** 结合第二轮已关闭的其余 9 项，T07-01 的 C01–C11 全部关闭，在原审阅范围内通过。本轮仅关闭剩余两项，不扩大平台、版本或实际可用性的证据范围；MindIE `latest` 版本 gate 继续保留，模型审阅不构成硬件验证。

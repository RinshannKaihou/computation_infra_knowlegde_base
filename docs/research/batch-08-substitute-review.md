# 第八批复查记录（替代性复查，非 astra/xhigh）

复查日期：2026-09-30。**重要限制：用户约定每轮由 gpt-6-astra / xhigh 做独立验证审阅；当前环境没有该模型的派发能力，本轮未能完成约定模型的独立审阅。** 本记录是同环境只读子代理做的定向复查，审阅独立性不等同于跨模型外部审阅，不标记为 astra 审阅。高优先级问题未解决不标完成的约定仍然适用；本轮复查没有发现 P1/P2。

## 范围与实际核查

完整复读三篇新增正文（ascend-memory-oom-evidence、data-starvation-triage、idle-resource-job-waiting-triage）、三份第八批来源记录、registry 变更、schema；实际经 raw.githubusercontent.com 固定 commit 原文件核对 20 余处锚点（Ascend/pytorch `bc51ab84`、pytorch/pytorch `1eba9b3a`、kueue `911a822a`），CANN 82RC1alpha001 的 0094/0095 页经原始 HTML 核对；本地核对导航与链接目标存在性；复查者另运行 `make check`（PASS）。

## 发现与关闭

| 发现 | 级别 | 状态 | 关闭依据 |
|---|---|---|---|
| 内存文章把“预留量约为总内存的 1⅛”挂在注释块 L288–362，实际出自代码注释 L380–383（`numSegments(device_total + device_total / 8)`） | P3 | 关闭 | 正文改为引用 L380–383；主任务复查原文件确认注释文本 |
| garbage_collection_threshold 写成“取值 0~1”，源码 TORCH_CHECK 严格排除端点 | P3 | 关闭 | 正文改为 (0,1) 开区间；主任务确认 L963–975 的 `val1 > 0` 与 `val1 < 1.0` |
| 1EB 防御分支写为单数单处，实际有 allocate 与 allocate_with_aligned 两处 | P3 | 关闭 | 正文改为“两处”并补 L3543–3547 |
| 04 index 的 updated_at 未随本轮更新 | P3 | 关闭 | 改为 2026-09-30 |

## 本轮确认保留的边界

- 固定 commit 的内存 API、OOM 文案、选项集、错误码与文档对照表空缺描述与源码一致；master 分支差异只作发现入口；docstring 沿用 CUDA 措辞的问题在正文中如实标注。
- CUDA 语义全部显式标为对照；异步错位标为机制推断。
- Kueue 的 v1beta1 deprecated、UnadmittedWorkloadsObservability 门控（Beta 且默认关闭、默认只见 Pending 回退）、pendingWorkloadsStatus 废弃、troubleshooting_pods.md 原文拼写错误均与固定 commit 一致。
- 「借入被收回」以候选支路与验证路径呈现，未写成已发生结论。
- 三篇 frontmatter 符合 schema；YAML 无静默截断；kubectl/kueuectl 命令均出自固定文档；未发现虚构命令、阈值或版本组合。

## 未覆盖

- 未核对三篇文章的每一个行号锚点（抽查 20 余处关键锚点全部命中）。
- 未复核首轮 54 篇存量内容。
- 未运行 `make build` 之外的验证；未执行任何训练、profiling、调度或 NPU 操作。

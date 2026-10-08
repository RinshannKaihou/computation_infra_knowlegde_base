# 后续 T07 推理长尾场景候选

读取时间：2026-09-30。主任务在第四批审阅期间开展发现与初筛；本文件不是正式案例，也不说明流程已验证。正式写作仍需独立核对。

## 优先候选：vLLM Ascend #17443

已通过精确 URL 阅读 [Issue #17443](https://github.com/vllm-project/vllm-ascend/issues/17443) 正文和可见元数据。页面显示 2026-09-24 提交、当前 Open，没有可见关联修复。它适合整理为“根因未定的长尾调查”，不能写成已解决事故。

报告者描述两台 A3、P/D 分离、GLM-5.3-Flash W8A8，给出框架/后端/CANN/驱动等标识。其测试树与当下 HEAD、pip 元数据有差异，环境不能只保留包版本。固定长度测试在更换代码树时也更换了输入长度；混合长度测试报告 128 次请求中 3 次失败，并有 TTFT 分位数。作者承认跨构建比较尚非同长度对照，计划补做 A/B。

正式案例应只挑必要环境字段、短时间线和一组统计结果，避免复制整个报告。各事实旁链接 Issue，明确全部为报告者提供的信息，不能当本库复现。

本库的独立评估方向：

- 输入、版本和负载同时变化，不能把差异归因到某一 commit 或 patch。
- 客户端 TTFT 包含多个阶段；`input_tokens / TTFT` 不能作为纯 prefill kernel 吞吐。最小 TTFT 也不自动等于零排队时间。
- 平均 TPOT 接近不能排除 decode 长尾；失败请求如何进入/排除分位数要查客户端实现。
- 输出中的版本标识不等于已核验制品，报告涉及的 nightly、补丁及高级 P/D 配置不能套用本库 v0.14.0rc1 样板。
- 同长度、同到达过程、同输出条件和缓存状态的对照，加上完整失败分类，才可进一步区分版本回归和工作负载影响。

访问缺口：网页静态视图未返回可核实的评论内容；随后尝试公开 GitHub API 的 Issue/评论端点，web 工具不可访问，curl 的 Issue 请求返回 HTTP 403，后续评论请求因此没有执行。不能据此声称没有评论或维护者已确认。正式成文可保留根因未知与评论未核实，并再次尝试可访问的公开页面。

## 次要候选

- [#16625](https://github.com/vllm-project/vllm-ascend/issues/16625)：已读正文。报告给出 A3 P/D 服务的无 profiler 基线和带 profiler 测量，另列在线 profiler 的部分失败与停止延迟；页面 Closed，关闭原因未取得。适合后续讨论观测开销，不能把它的关闭当修复或把 profiler 运行建议直接写成安全命令。
- [#2691](https://github.com/vllm-project/vllm-ascend/issues/2691)：已打开页面，尚未完成逐项核查；先不选为正式案例。

## 流程与实验的来源组织

T07-P/T07-X 优先复用本库已固定的 vLLM v0.14.0、vLLM Ascend v0.14.0rc1、F15/F16 与 E01。案例自身的历史环境独立记录，不将 nightly 特性回填样板支持矩阵。第四批审阅已经发现 F16 的服务端计时起止表述问题，正式写作应等待修订，再引用指标字典。

流程按失败/超时分类、计时边界、负载组成、排队、prefill/decode、KV、CPU/frontend、通信与设备证据设置分支。实验只设计同负载重复、一次改一个变量、同时保留失败与质量结果的对照，不填写目标机型的阈值，也不执行 benchmark、profiling、升级或服务变更。

## 转为正文草稿（2026-09-30）

已再次打开 #17443 精确页面核对正文、Open 状态和可见关联信息；评论仍未取得，不表述为“无评论”。现已形成 T07-P/C/X 三篇正文，等待本轮 astra/xhigh 审阅。案例来源已登记 `src.vllm-ascend.issue-17443`；只保留必要事实、有限测量和缺口，本库的证据分析另表列出，不复述为维护者结论。

P/X 复用第四批审阅后固定的 vLLM 指标、benchmark、optimization、prefix caching 和插件功能范围。第四批计时问题已修复：服务端 TTFT/E2E 是 engine request arrival 到 frontend 相关输出接收后的 iteration wall-clock；core phase/ITL 使用 monotonic，不能与客户端原始时间戳拼接。流程特意避免推断客户端减服务端是纯网络时间。

| 产物 | 支持与范围 | 本轮未做 |
|---|---|---|
| `inference.ascend-inference-tail-latency-triage` | 固定负载、失败、计时口径，按候选证据分支；版本和 P/D 边界单列 | 没有执行现场查询或给未验证调参命令 |
| `inference.ascend-inference-tail-latency-source-case` | #17443 未闭环公开报告；版本/长度混杂与缺失失败口径 | 没有复验报告数字、归因或修复 |
| `inference.ascend-inference-tail-latency-experiment` | B0/V1/R0 与按需 O1；预先定义统计、失败与质量标准 | 没有 benchmark、profiling、制品安装、服务变更或结果 |

成文后再读取固定 raw 源码 `stats.py` 233–305/331–377、`serve.py` 404–445/617–712/763–845/1202–1213/1271–1291、`optimization.md` 10–48、`prefix_caching.md` 5–26，确认计时、样本过滤、吞吐窗口、并发与到达、重算和缓存身份。T07-X 的并发约束引文补充 1202–1213，避免只指向 request-rate 定义段。只读副本保存在临时目录，未纳入知识正文附件或运行证据。

补充获取：同日使用 GitHub 连接器 `fetch_issue_comments` 对 `vllm-project/vllm-ascend#17443` 查询全部评论页，成功返回 `comments: []`。这弥补了前述静态页未载入评论的访问缺口；截至该次观察仍无评论内容或维护者结论。此结果不保证未来无新评论。正式案例及 registry 已同步，前述失败尝试保留为历史获取记录。

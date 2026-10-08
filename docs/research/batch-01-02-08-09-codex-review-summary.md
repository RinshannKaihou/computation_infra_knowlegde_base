# batch 01、02、08、09 补审汇总

日期：2026-09-30。用户授权：“由你来替代 astra，帮我审阅这四个尚未完成审阅的 batch”。实际审阅者为本会话 Codex 主助手；没有派发 gpt-6-astra/xhigh，也没有使用子代理。本次独立读取正文与上游证据，不以原来源审计或旧替代复查的通过结论代替核查；它不构成一次实际的 astra/xhigh 模型运行。

**补审、修订和定向复核已完成；9 项唯一发现全部关闭（5 P2、4 P3）。** batch 01 初审无修改项，batch 02、08、09 修订后在原审阅范围内通过。[定向复核](batch-02-08-09-codex-recheck.md)记录逐项关闭依据、复核时补正及最终文件身份。没有执行 GPU/NPU、推理服务、通信、存储或集群实验。后续批次的审阅模型约定未因本次四批授权而自动改变。

## 批次覆盖与结论

| 批次 | 本次完整阅读的正文 | 本批新增发现 | 跨批次影响 | 报告与结论 |
|---|---:|---|---|---|
| 01 | 3 | 0 | 无 | [第一批报告](batch-01-codex-review.md)：限定来源范围内无修改项 |
| 02 | 3，另核对 E01 安装页补充 | 1 P2 | B02-C01 同时影响 batch 08 | [第二批报告](batch-02-codex-review.md)：修订后复核通过 |
| 08 | 3 | 1 P2 + 2 P3 | 继承 B02-C01；B08-C01 同时影响 batch 09 | [第八批报告](batch-08-codex-review.md)：修订后复核通过 |
| 09 | 3 | 3 P2 + 2 P3 | 继承 B08-C01 | [第九批报告](batch-09-codex-review.md)：修订后复核通过 |

“新增发现”按问题的主要归属计数；跨批次复用同一 ID，不再计算第二次。P2 指足以改变诊断分支、漏掉候选故障或错误解释证据的缺陷；P3 指局部语义、触发条件或来源数字范围需要修正。没有发现 P0/P1。

## 已关闭发现清单

| ID | 优先级 | 问题 | 受影响正文 | 状态 |
|---|---|---|---|---|
| B02-C01 | P2 | 未区分中间队列占用与可按序消费 batch，用队列空/满直接判上下游 | training-data-path；data-starvation-triage | 已关闭 |
| B08-C01 | P2 | TorchNPU 进程额度不足也生成同一 OOM 错误码，遗漏 `allowed` 分支 | ascend-memory-oom-evidence；ascend-inference-oom-triage | 已关闭 |
| B08-C02 | P3 | GC 阈值缺少 fraction 生效条件、额度分母和正确时机 | ascend-memory-oom-evidence | 已关闭 |
| B08-C03 | P3 | 从空 conditions 直接反推 StrictFIFO 队首阻塞 | idle-resource-job-waiting-triage | 已关闭 |
| B09-C01 | P2 | EngineDeadError 被误判为启动期失败 | ascend-inference-oom-triage | 已关闭 |
| B09-C02 | P2 | 按 SDC 定义否认主动测试的检测覆盖 | silent-errors-and-integrity | 已关闭 |
| B09-C03 | P2 | 稳定复现、输入依赖和硬件绑定被设为 SDC 嫌疑的必要入口条件 | silent-errors-and-integrity | 已关闭 |
| B09-C04 | P3 | RAS MISMATCH 缺少正常瞬态和连续查询限定 | bandwidth-degradation-triage | 已关闭 |
| B09-C05 | P3 | SuperBench 的冗余链路分母被扩大为全部上行链路 | silent-errors-and-integrity | 已关闭 |

原问题、固定来源、修订建议和关闭条件在各批报告的初审历史中；实际关闭依据见[定向复核](batch-02-08-09-codex-recheck.md)。共享基础 B02-C01/B08-C01 和受影响下游流程已同步修订，研究记录与 registry 已核对。旧 batch 08/09 替代复查的发现保留为另一轮历史，未用它们代替本次关闭证据。

## 核查方法与边界

1. 先读 README、authoring guide、outline、四批来源审计与旧审阅，确定 12 篇正文及 E01 补充的归属。
2. 阅读全部目标正文，对技术主张、推理分支和关联基础条目逐段检查；对关键声明重新读取固定 commit、版本化文档、论文和公开 Issue。
3. GitHub 读取固定源码；动态厂商页面使用浏览器确认目标正文和版本标识；论文相关段落使用网页/PDF 文本提取。完整上游工程、整篇论文、所有配置组合和图表像素均未作为已核对范围。
4. 来源均为现有 registry 中的条目。保留文档/代码/发行包/用户讨论的许可区别，没有引入上游代码、长日志或实时集群状态。
5. 核对元数据、稳定 ID、主领域归属、章节与平台/任务导航，并运行仓库检查和构建。结构通过不能关闭技术发现。

初审及定向复核均没有下载软件发行包、执行安装或设备命令。公开 Issue 的作者归因不等于已确认根因；源码分支分析也不等于实测。没有新的 `reviewed` 或 `reproduced` 正文状态。

## 初审本地检查（历史）

报告及交接入口落盘后，`make check` 与 `make build` 均通过：**60 content entries / 71 sources**；已重新生成 `build/catalog.json` 与 `build/catalog.md`。工具实际提示只检查结构及本地文件链接，不证明技术正确性或远程链接有效。

另完成定向核对：12 篇正文 SHA-256 与本次审阅清单、生成 catalog 完全一致；目标 ID、路径、标题、类型、领域、编辑状态、平台、摘要、source_refs、related_ids、适用条件与 verification 一致，各篇都有所属章节入口。12 篇仍为 `draft / source_checked`。四份报告的发现 ID 与汇总一致，共 9 项唯一发现（5 P2、4 P3）。

没有修改 `src/kb/`；不要求或声称运行 `make test`。以上为初审检查快照，最终文件身份及本地检查另见[定向复核记录](batch-02-08-09-codex-recheck.md)。

## 修订响应（2026-09-30，Opus）

主任务已完成全部 9 项发现的修订（无反驳项），逐项关闭依据、研究记录/registry 同步与修订后文件 SHA-256 见[修订记录](batch-02-08-09-review-fixes.md)。修订后 `make check` / `make build` 通过（60 entries / 71 sources）。原提交状态为“待复核”；随后由原 Codex 审阅者按关闭条件完成[定向复核](batch-02-08-09-codex-recheck.md)，9 项均已正式关闭。

## 初审正文的固定身份（历史）

当前目录未初始化 Git 仓库，因此使用正文文件的 SHA-256 固定初审版本。E01 在 batch 01 与 02 之间共享，不重复计为第 13 篇。下表是初审历史身份，7 篇修订正文的最终身份另存于[定向复核记录](batch-02-08-09-codex-recheck.md)；其余 5 篇未变。

| 正文 | SHA-256 |
|---|---|
| [layers-and-boundaries](../../knowledge/02-software-stack/layers-and-boundaries.md) | `ca1af0bdde0ec7d992beb44ab2ecb63dde8f652993088179b150f7bd6ce183ed` |
| [compatibility-evidence](../../knowledge/02-software-stack/compatibility-evidence.md) | `7dbc08091ca71c1ae1a5f605a22d2cd0d2d191d0315b9ba2fb61f138e8dd7a21` |
| [ascend-documented-profile](../../knowledge/02-software-stack/ascend-documented-profile.md) | `90e2ee190a242a95adf6beed210d0799a0ee2f5dc69de57f2e2d3e0c46284c03` |
| [resource-topology](../../knowledge/01-hardware/resource-topology.md) | `fcf3d510d05a8b73e1785c4a8ac80010fb201f8a8817c1501c4367ee579fdc36` |
| [training-data-path](../../knowledge/04-data-storage/training-data-path.md) | `5d810a872f960ac3a90692cadf53c8675bccf888ddaf43cbc0dff5dd17f275e1` |
| [device-resource-chain](../../knowledge/05-cluster-platform/device-resource-chain.md) | `e2f6a16976b24946f447f88e575a3a008cc3c2ede7618a81e63e8f8fd4d44059` |
| [ascend-memory-oom-evidence](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md) | `4fb4f2f81ae4c019424ae9b65aa1a6598cbefc867653fa0726a9fee62d693e65` |
| [data-starvation-triage](../../knowledge/04-data-storage/data-starvation-triage.md) | `0b6f7f36d1d8849d7038f9397192392613bc778385e1efef9c50d95ba3ebc64f` |
| [idle-resource-job-waiting-triage](../../knowledge/05-cluster-platform/idle-resource-job-waiting-triage.md) | `5130347bcaf4d546eab61f85d3d08c7c0a628f57e0f2a4730e6f2d50cdedf840` |
| [ascend-inference-oom-triage](../../knowledge/07-inference/ascend-inference-oom-triage.md) | `77f57a4ab5a5a78c9ba4c5b0946aff377f8f06cf9d03f287fed6ea470aebbda4` |
| [bandwidth-degradation-triage](../../knowledge/03-communication/bandwidth-degradation-triage.md) | `0c3b6a4699f31bf68d783942e511ae0567db5a6abbeb4b613298d4653c30c384` |
| [silent-errors-and-integrity](../../knowledge/08-reliability/silent-errors-and-integrity.md) | `9b9f48a8ba30ceced604a554dcbd8f9a41af508d315445e2a81617c7da6187c9` |

# Batch 25 T06-07 第三轮定向复核报告

- 日期：2026-10-20（Asia/Shanghai）；上游时间字段按 UTC 记录。
- 依据：[初审报告](batch-25-t06-07-codex-review.md)、[第二轮复核报告](batch-25-t06-07-codex-recheck.md)及 [T06-07 验收条款](../../plans/full-coverage-backlog.yaml)。重点复核 C01、C03、R01，同时检查此前关闭的六项及新增问题。
- 执行方式：当前本地 Codex CLI 会话独立复核，未委托子代理；约定模型/档位为 `gpt-6.1-sol / xhigh`。本轮未取得可独立核验的启动模型元数据，不宣称实际执行模型已核验，也未另行运行其他模型。
- 本轮快照 SHA-256：正文 `8bd432f5e933dc91cf447bba9f9502431e23cdd5629856a376518b5b470ecb2c`；来源记录 `1429e32ed2a96a5606695942d1e4287ae53df7b5a5789d1b821d37129dbfec19`；registry `99b81d2047b01fc2ed7885143d062e6e0d7b44a0415db22dd63d1d9dd474857b`。下文行号针对这些快照。
- 写入范围：仅新增本报告，不修改正文、来源登记、导航、既有报告或原工作树的 `build/`。未执行上游测试命令、训练或 GPU/MPS 性能复跑。

## 1. 三项定向判定

**本轮重点三项：C03 CLOSED，C01 OPEN（仅剩 registry 的数值口径同步），R01 OPEN（仅剩 registry 的时间字段同步）。** 正文第三轮修订的三处内容均已核实，不把登记遗漏误说成正文未修，也不因正文修好就忽略上一轮已经明确要求同步的来源登记。

| 编号 | 判定 | 当前位置 | 理由与剩余关闭条件 |
|---|---|---|---|
| B25-T07-C01（初审 P1；剩余 P2） | **OPEN** | 正文第 61、85、87 行；来源记录第 50–52 行；registry 第 6489 行 | 正文已补齐 MPS 独立负载、输入、精度、机器、compiled/eager 分母和作者归属，且与重新打开的 #192551 正文一致，见 E01；次生因果错误未回归。但是 registry 的现行 `notes` 仍只写“作者报告约 4× 训练步延迟比”，没有 eager 分母、独立负载/精度，也没有指向补齐口径的位置。上一轮明确要求“同时将 registry 的约 4× 说明指向该独立口径”，尚未完成。将该登记的数字补为独立 MPS 条件下的 compiled/eager 比值并定位 #192551 正文，或删除该处无背景的重复数字、改为指向正文第 61 行/来源记录第二轮修订段后可关闭。无需恢复原 P1 或另编新号。 |
| B25-T07-C03（P2） | **CLOSED** | 正文第 50、72–75、94 行；来源记录第 53 行 | 原“若 kernel 慢则改布局后仍应慢”的前提及“被作者数据反驳”的排除结论已删除。kernel 行明确保持候选，指出布局会改变访存、调用或选择，开关对照不能隔离 kernel 因素；工具链仍未排除，质量仍 unknown。把“布局差异占主导”限定为该负载的开关性能现象读取，而非独立 kernel 归因或完整因果排除；固定源码与作者评论支持保留分层，见 E03、E05。满足本项原关闭条件。 |
| B25-T07-R01（P3） | **OPEN** | 正文第 64 行；来源记录第 54 行；registry 第 6495 行 | 正文及最新修订段已正确区分 author `05:31:00Z`、MergeBot committer `05:31:07Z`、PR `closed_at=05:31:12Z`，与 API 相符，见 E02。现行 registry 的 `revision` 却仍为“经 MergeBot 对应落地 commit … 05:31:00”，PR 秒级时间也未标 UTC，继续把 author 时间用于 MergeBot 落地叙述。上一轮的三处统一要求未全部完成。该登记同步写明完整 UTC 字段，或删除不必要的秒级时间、只保留日期后可关闭；committer 时间仍不等于 API 记录的精确 main ref 更新时间。 |

### C01：正文测量背景核对结果

本轮不是只核对作者新增的修订摘要，而是重新打开了 [#192551 正文](https://github.com/pytorch/pytorch/issues/192551)。其 Describe the bug、复现代码、Output 与 Versions 段共同给出：

- 作者自定义的小卷积网络 `Net/Block`，输入 `(256, 3, 32, 32)`，`bf16 autocast`，Apple M5 Pro、macOS 27；不是主案例的 fp16 MobileNet/batch 512。
- 主复现输出的 PyTorch 为 `2.14.0.dev20260807`：eager `25.59 ms/step`，compiled `114.48 ms/step`，输出标明 `4.47x eager`。正文写 nightly 约 4.5× 与之相符；该比值不是“默认布局/关闭布局”的比值。
- 约 9× 对应作者在 issue 开头对 `2.13.0` release wheel 的报告；不能把 nightly 的这组原始时延移植为 release 的原始时延。
- shape sweep 在独立进程和缓存下比较布局开/关；作者报告 `TORCHINDUCTOR_LAYOUT_OPTIMIZATION=0` 后，在其试过的 shape 上 compiled 快于 eager。正文保留了“其试过的 shape”和“数字来自作者机器”的限制，未写成任意 MPS 负载的保证。

因此，**正文与最新来源修订段的 C01 数值背景已经通过核对**。C01 保持 OPEN 仅因为可独立消费、并会进入 catalog 的 registry 数字说明没有同步，不是仍怀疑这些环境或数值。正文第 87 行的“约 4×”作为对已登记 MPS 数值的粗略汇总读取，不另立精度问题；原 P1 因果纠正维持有效。

### R01：字段核对结果

本轮通过已连接的 GitHub 工具重新读取 [commit API](https://api.github.com/repos/pytorch/pytorch/commits/82b424c7f91dc9cb631af7cfe11f5ba12f0ba37d)和 [PR API](https://api.github.com/repos/pytorch/pytorch/pulls/188236)：

| 对象与字段 | 本轮读值 | 可支持的事件 |
|---|---|---|
| `82b424c7…` / `commit.author.date` | `2026-09-23T05:31:00Z` | Git author 时间 |
| 同 SHA / `commit.committer.date`，committer 为 PyTorch MergeBot | `2026-09-23T05:31:07Z` | Git committer 时间 |
| #188236 / `closed_at` | `2026-09-23T05:31:12Z` | PR 关闭时间；API 仍为 `merged=false`、`merged_at=null` |

正文第 64 行没有再把第一行直接称为 MergeBot 时间；registry 第 6495 行仍保留旧说法。来源记录第 43 行属于较早修订记录，已由第 50–54 行的最新段落更正，本轮不把该历史文本当成新断言；但 registry 没有相应更正或作废标识，不能套用这一历史豁免。

## 2. 此前六项 CLOSED 的防回归核对

**C02、C04、C05、C06、C07、C08 均维持 CLOSED，未确认回归。** 本轮重新读取对应正文、来源登记与导航，并对关键上游事实补核；不以作者声称“已修改”替代检查。

| 编号 | 本轮位置与结果 | 核验依据 |
|---|---|---|
| C02 | 正文第 36、59、87、93 行及 registry 第 6489 行维持默认慢、强制启用快，speedup 明确相对 eager | 重新读取 #189239 两组 CSV 及 #191306 的 Benchmark data；本轮按 `178.413744 / 141.905300 ms` 重算，时延下降 `20.462798%`、固定工作量吞吐增加 `25.727329%`，与约 20.5%/25.7% 一致。没有当作落地 SHA 的复测。见 E03。 |
| C04 | 正文第 40–48、66、83–87、106 行保留环境、测量选项、单卡范围、输入 unknown，以及复测与 release tag 的未知边界 | 主 issue 的版本与命令重新取得；PR Results 的 Intel Data Center GPU 与 9 月 2 日评论的 Intel Client GPU/RTX 4080 SUPER 报告仍分开，没有把 CUDA CSV 的完整条件移植给 Intel。作者自报不等于本库复现。见 E03、E04。 |
| C05 | 正文第 58、63、64、79、95 行及 registry 第 6495、6500 行维持 PR 身份、日期顺序、MergeBot 入库语义和最终 diff 区分 | #188236 创建 `2026-06-26T01:58:47Z`，早于 #189239；落地 message 明确关联该 PR。#191306 的关闭理由、forward→lazy backward redesign 及最终四文件清单已重开核对。R01 是登记的秒级字段残留，不重开本项已正确的身份与日期顺序。见 E02、E04。 |
| C06 | 正文第 57、98 行及 registry 第 6484 行仍明确 `140baa4eec85` 仅加注释，真正 guard 引入点未知 | 重新读取该 SHA 的实际 patch，只有四行新增注释；父 SHA `86c24e7e…` 的原文件已经调用 `guard_int_seq` 处理 stride/padding/dilation。未把 message 中的测试清单当作实际修改或本库通过的测试。见 E06。 |
| C07 | 正文第 14 行的完整引号 summary 解析正常 | 本轮实际解析 YAML 并重建 catalog；按稳定 ID 取得的 summary 与 frontmatter 逐字一致，包含 `issue #189239` 及结尾 MPS 平台边界说明，没有井号截断。 |
| C08 | slow-rank 第 82 行、机制页第 263 行、performance-analysis 第 142 行、训练章 index 第 69、78 行的普通 Markdown 案例链接均存在 | 案例第 91、94、97 行也保留返回三篇关联正文的链接；均匀变慢与 rank 偏斜边界、单卡不构成分布式实测的限制未删除。本轮未改动这些页。 |

## 3. 上游证据与读取边界

终端 `gh api` 本轮因无法连接 `api.github.com` 失败；随后用已连接的 GitHub 工具读取官方 API、紧凑 PR 元数据和固定 SHA 原文件。#192551 的环境与数字直接来自重新打开的网页完整正文，不来自搜索摘要；未执行任何源文档内的代码。

- **E01 — MPS 独立问题**：[issue #192551](https://github.com/pytorch/pytorch/issues/192551)的 Describe the bug、复现代码、Output、shape sweep、Versions 及关闭讨论。页面显示 2026-08-07 创建、2026-08-17 关闭，关闭评论指向 #193623，仍早于主案例 2026-09-23 的修复落地。本轮未继续审查 #193623 的实际修复代码，不据此扩大已经确认的复测范围。
- **E02 — 时间字段与落地对象**：[82b424c7 commit API](https://api.github.com/repos/pytorch/pytorch/commits/82b424c7f91dc9cb631af7cfe11f5ba12f0ba37d)、[#188236 PR API](https://api.github.com/repos/pytorch/pytorch/pulls/188236)。commit message 关联 #188236，实际仅改 `torch/_inductor/graph.py`（+29/−15）与 `torch/_inductor/kernel/conv.py`（+15/−0），不含测试文件。时间字段见上表，不凭时间接近推导 PR 身份，也不把 committer 时间当作 main ref 更新时间。
- **E03 — 主报告与对照口径**：[#189239 API](https://api.github.com/repos/pytorch/pytorch/issues/189239)的 Performance regression 命令、两组 CSV、局部 runner、Versions；[#191306 PR 正文](https://github.com/pytorch/pytorch/pull/191306)的 Benchmark data 明示 eager 基线。取得的 `closed_at` 为 `2026-09-23T13:59:15Z`，这仍只证明关闭时点，不证明最终 SHA 在同条件下完成性能或质量复测。
- **E04 — 两个 PR 的结果与不同方案**：[#188236 Results](https://github.com/pytorch/pytorch/pull/188236)、[2026-09-02 作者评论 5508430307](https://api.github.com/repos/pytorch/pytorch/issues/comments/5508430307)、[#191306 PR API](https://api.github.com/repos/pytorch/pytorch/pulls/191306)、[redesign 评论 5440524234](https://api.github.com/repos/pytorch/pytorch/issues/comments/5440524234)、[关闭评论 5457176688](https://api.github.com/repos/pytorch/pytorch/issues/comments/5457176688)。#191306 最终 head 为 `e3612cabaf142656e49584f2e1119e4b8ff7e507`；重新列出的四文件为 `test/inductor/test_layout_optim.py`、`torch/_inductor/compile_fx.py`、`torch/_inductor/cudagraph_utils.py`、`torch/_inductor/output_code.py`；另读取 `compile_fx.py` 的 PR patch，确认 forward 决策传给 lazy backward，不是仅按初始 PR 正文猜测最终实现。该提案内的测试声明不移作 #188236 的验证。
- **E05 — 因果与执行层边界**：[994f78b1 固定 graph.py 第 757–835 行](https://github.com/pytorch/pytorch/blob/994f78b19267fdeb5292595db1fd4d5aa3d9b100/torch/_inductor/graph.py#L757-L835)、[同 SHA conv.py 第 1074–1110 行](https://github.com/pytorch/pytorch/blob/994f78b19267fdeb5292595db1fd4d5aa3d9b100/torch/_inductor/kernel/conv.py#L1074-L1110)，按原文件行范围重新读取。可确认节点计数、强制开关、空计数返回、CUDA 非 HIP 路径的 Triton 候选禁用和 lowering 内的布局转换；不能仅据开关性能恢复排除 kernel/布局/工具链交互。9 月 2 日作者评论亦区分该路径与 cuDNN backward fallback。
- **E06 — message 与实际 diff**：[140baa4eec85 commit API](https://api.github.com/repos/pytorch/pytorch/commits/140baa4eec85ed24f50ad6a32013cfb497cd977a)及[父 SHA 的 conv.py 第 980–995 行](https://github.com/pytorch/pytorch/blob/86c24e7eb95722f737ff5f56f39a4268483344e6/torch/_inductor/kernel/conv.py#L980-L995)。本轮未向前追溯真正行为变更点，保留 unknown。

## 4. 新问题检查

**未确认需要从 B25-T07-R02 起另行编号的新问题。** 本轮检查覆盖新增 MPS 数值及版本归属、kernel 行残留的排除措辞、秒级时间语义、两项 registry、摘要与关联页。C01、R01 的登记遗漏属于上一轮明确列出的未完成关闭条件，沿用原编号，不拆成 R02/R03，也不隐去其 OPEN 状态。

来源记录第 39 行起的修订及第 50 行起的第二轮修订按时间顺序覆盖早期观察中的旧说法；与上一轮相同，不把历史观察中的“次生”“dilation cast”等残留重新作为现行断言。此处理不延伸到没有相应更正的 registry。

## 5. 整体判定与最小闭环

**整体判定：第三轮定向复核尚未通过；T06-07 目前不能声明通过既定审阅范围。** 初审八项中现为 **7 项 CLOSED、C01 仍 OPEN**；上一轮新增的 **R01 仍 OPEN**，本轮新增发现 **0 项**。共剩 **2 项开放问题（1 P2、1 P3），无开放 P1**。

正文的 MPS 测量背景、kernel 候选边界及时间字段修订本身均有效；此前六项也没有回归。剩余阻塞只在来源登记层：

1. `src.pytorch.issue-189239-layout-regression.notes`：为保留的 MPS 倍数补齐独立条件与 eager 分母，或去掉该处无背景的重复数字并指向正文/最新来源修订段。
2. `src.pytorch.layout-opt-fix-chain.revision`：同步 author/committer/PR closed_at 的 UTC 字段，或删去秒级时间只留日期，不再将 `05:31:00` 写作 MergeBot 落地时间。

这两项均是既有关闭条件，无需新增硬件实验、补造测试结果、确定尚未知的 release tag，或重做六项已关闭审阅。同步后只需针对登记与已核对证据再做定向复核；本报告不替作者修改它们。正文继续保持 `draft / source_checked`，来源核对不授予 `reviewed` 或 `reproduced` 状态。

## 6. 结构检查与写入边界

- 在包含原有构建基线的完整临时副本中执行 `make check`、`make build`，均通过：**107 content entries / 525 sources**；原工作树的构建产物未重写。
- 实际核对 YAML 与重建 catalog 的完整 summary；同时读取 catalog 中两项来源登记，确认 C01 的无背景 MPS 数字和 R01 的旧时间叙述也被带入生成物，并非只存在于不再消费的历史记录。
- 本轮未修改 `src/kb/`，未运行其单元测试；结构与链接校验不验证远程事实、性能因果、版本兼容或硬件行为。
- 报告写入后，原工作树 `make check` 通过，含本报告的临时副本 `make check` / `make build` 也通过。写前快照的 535 个既有文件哈希均未变化，包括原工作树的构建产物；核验期间另观察到其他任务新增 T06-05 第三轮复核报告，本轮未创建或修改它，本轮自行新增文件仅为本报告。

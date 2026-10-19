# Batch 25 T06-07 第二轮定向复核报告

- 日期：2026-10-20（Asia/Shanghai）；本报告的上游时间均为 GitHub API 的 UTC。
- 依据：[初审报告](batch-25-t06-07-codex-review.md)的 B25-T07-C01–C08，以及 [T06-07 任务验收条款](../../plans/full-coverage-backlog.yaml)。本轮逐项重新读取修订正文、来源记录、两条 registry 登记与指定关联页，并重新访问初审引用的上游对象，不以作者修订说明替代取证。
- 执行方式：当前本地 Codex CLI 会话独立复核，未委托子代理。约定审阅模型/档位为 `gpt-6.1-sol / xhigh`；本轮未取得可独立核验的启动模型元数据，不宣称已经核验实际执行模型。
- 正文快照 SHA-256：`c12c8450643609f84125551ce4eea47240e01259e9c28619b76ac9050a114c08`；来源记录快照 SHA-256：`1baccb596add1f7bd1521b6b2e9a0a333b1be6aec5a92fbd6f5cd83acbac9325`。下文位置均针对本轮快照。
- 写入范围：仅新增本报告；不修改正文、来源记录、registry、导航或原工作树的构建产物。未执行上游测试、训练、性能复跑或任何 GPU/MPS 硬件验证。

## 1. 逐项判定

**结论：6 项 CLOSED，2 项 OPEN。** C01 的核心 P1 因果错误已经纠正，但其原关闭条件中的 MPS 数值背景尚未补齐，保留同一编号跟踪，剩余问题按 P2 处理；C03 仍有 P2 断言未删除。新增 1 项 P3，见 R01。不把已指出但未修完的内容重新编号为新发现。

| 初审编号 | 判定 | 修订后位置 | 理由与本轮证据 |
|---|---|---|---|
| B25-T07-C01（初审 P1；剩余 P2） | **OPEN** | 正文第 61、85、96 行；registry 第 6484、6489 行；来源记录第 41 行 | “本案修复引入 MPS 次生回归”的核心错误已纠正：正文与 registry 已改为同期独立镜像问题，并给出先存在、先关闭的顺序，API 与关闭评论支持此更正。但是第 61 行只写“独立负载与精度”，没有真正交代该负载、精度和 eager 分母；原关闭条件未全部满足。约 4× 不能只靠“作者报告”四字完成测量边界登记。见下文 C01 剩余项及证据 E02。 |
| B25-T07-C02（P2） | **CLOSED** | 正文第 36、59、87、93 行；registry 第 6489 行；来源记录第 42 行 | 对照方向已改为默认慢、强制启用快；两个 speedup 明确为相对 eager，而非新旧版本。主 issue 的两组原始时延为 178.413744/141.905300ms；本轮算术复核得时延下降 20.462798%、固定工作量吞吐增加 25.727329%，与正文约 20.5%/25.7% 一致，且已标为作者数值的换算而非本库测量。未把该 CSV 当作最终 SHA 的复测。见 E01。 |
| B25-T07-C03（P2） | **OPEN** | 正文第 74 行；对照第 50、72、73、75、94 行及来源记录第 46 行 | 收敛 unknown、工具链未排除、lowering/布局/后端分层等已经改正；但假设表仍保留“若 kernel 慢，强制布局优化后仍应慢”以及“在该负载上被作者数据反驳”。这正是初审指出的无效排除，不能因其他行已变成三态就关闭整项。布局变化可能改变 kernel 的访存、调用或选择，开关后变快不构成排除所有 kernel 因素的实验。固定源码及 issue 局部 runner 还要求区分 NVIDIA 上的 ATen 反向卷积调用与新增 Triton 候选。见 E01、E07。 |
| B25-T07-C04（P2） | **CLOSED** | 正文第 40–48、66、83–87、106 行；来源记录第 45 行 | 已登记主 issue 可取得的 torch/triton 包版本、batch=512、fp16/training、`-n 10`、冷启动选项、禁用 CUDA Graphs、公开命令未配置分布式、输入尺寸 unknown，以及环境采集的 PyTorch/build CUDA 字段 N/A。PR Results 的 Intel Data Center GPU 报告与 9 月 2 日评论中的 Intel Client GPU/RTX 4080 SUPER 报告已分开；与最终落地 SHA 的同条件复测绑定未确认，release tag 继续 unknown。此关闭只认可各证据段已经作出的登记，不将 CUDA 命令/CSV 的完整条件移植给 Intel 报告。见 E01、E03。 |
| B25-T07-C05（P2） | **CLOSED** | 正文第 58、63、64、79、95、104 行；registry 第 6495、6500 行；来源记录第 43 行 | #188236 创建于 2026-06-26，早于 7 月 8 日主 issue；PR API 的 closed/merged=false/merged_at=null 与 MergeBot 对应落地的事实已并列解释。#191306 明确为因已有 PR 关闭的另一提案，且已区分初始计数方案和最终 forward→lazy backward redesign；未再叙述成“两轮失败后另起无关直接提交”。最终文件清单与评论支持这些修订。新增的秒级时间字段归属错误另计 R01，不推翻本项的 PR 身份、日期顺序和入库关联。见 E03–E05。 |
| B25-T07-C06（P2） | **CLOSED** | 正文第 57、98 行；registry 第 6484 行；来源记录第 44 行 | 已将 140baa4eec85 的 message 与实际 diff 分开，明确所核 diff 仅增加 4 行注释、guard 调用此前已存在、真正引入点未确认。本轮重新读取 commit API patch 和父 SHA 的原文件，结果一致；不因 message 中列有测试名就宣称该 SHA 改变行为或本库跑过测试。见 E06。 |
| B25-T07-C07（P3） | **CLOSED** | 正文第 14 行；临时副本生成的 catalog 中 `training.performance-regression-source-case.summary` | summary 已整体加引号。本轮实际解析 frontmatter 并构建 catalog，两个值逐字一致，均包含 `issue #189239` 及末尾的 MPS 平台边界说明，不再在井号处截断。不是仅凭结构检查通过判定关闭。 |
| B25-T07-C08（P3） | **CLOSED** | slow-rank-triage.md 第 82 行；operators-compilers-and-graphs.md 第 263 行；performance-analysis.md 第 122 行；训练章 index.md 第 69、78 行 | 已实际检出新增的两个普通 Markdown 返回链；案例也保留到三篇关联正文的出链，场景表及 06.6 主题入口均存在。slow-rank 链接放在均匀变慢而非 rank 偏斜的边界，案例第 97 行明确单卡案例不构成分布式慢 rank 实测。没有复制案例正文或新增跨平台验证声明。 |

### 本轮重新打开的上游证据

终端 `gh api repos/pytorch/pytorch/issues/189239` 本轮仍因连接 `api.github.com` 失败。随后通过已连接的 GitHub 工具直接读取同一官方 REST API，并对 PR 元数据使用其紧凑读取接口补核，网页只用于定位讨论段落。以下为本轮实际重开对象；状态、秒级时间与 diff 取 API，不取网页缓存或初审结论。

- **E01 — 主报告与关闭事件**：[issue #189239 API](https://api.github.com/repos/pytorch/pytorch/issues/189239)重新取得命令、CSV、Versions 与当前标签；[事件流](https://api.github.com/repos/pytorch/pytorch/issues/189239/events?per_page=100)中的关闭事件 `31681488164` 为 `2026-09-23T13:59:15Z`，操作者 eellison，`commit_id=null`。两组 CSV 是默认/强制布局开关对照；[PR #191306 的 Benchmark data](https://github.com/pytorch/pytorch/pull/191306)明确其 eager 基线。关闭事件仍不构成性能复测证据。
- **E02 — MPS 独立问题**：[issue #192551 API](https://api.github.com/repos/pytorch/pytorch/issues/192551)给出 `created_at=2026-08-07T22:36:36Z`、`closed_at=2026-08-17T09:05:42Z`；[事件流第二页](https://api.github.com/repos/pytorch/pytorch/issues/192551/events?per_page=100&page=2)的关闭事件 `29552983467` 与之对应。[关闭评论 5314010885](https://api.github.com/repos/pytorch/pytorch/issues/comments/5314010885)指向 #193623，早于本案 9 月 23 日落地。本轮只核对这条关闭说明，不宣称已经审完 #193623 的代码或验证链。
- **E03 — #188236 的身份、结果与合入路径**：[PR API](https://api.github.com/repos/pytorch/pytorch/pulls/188236)为 `created_at=2026-06-26T01:58:47Z`、`closed_at=2026-09-23T05:31:12Z`、closed/merged=false/merged_at=null，最终 head 为 `6e9593090530d61bfa40cbaafde80e4267124866`。[最终文件清单](https://api.github.com/repos/pytorch/pytorch/pulls/188236/files?per_page=100)只有 graph.py 与 kernel/conv.py。Results 自报 Intel Data Center GPU 对 nightly 的约 1.3×；[2026-09-02 作者评论 5508430307](https://api.github.com/repos/pytorch/pytorch/issues/comments/5508430307)另报 Intel Client GPU 与 RTX 4080 SUPER 1.3×+，但没有补齐用于绑定最终 SHA 的完整测量条件。[merge 请求](https://api.github.com/repos/pytorch/pytorch/issues/comments/5788157002)、[MergeBot 启动说明](https://api.github.com/repos/pytorch/pytorch/issues/comments/5788173882)和 E05 的 commit message 共同建立落地关联，不能只靠两个时间接近建立关联。
- **E04 — #191306 的另一提案与最终形态**：[PR API](https://api.github.com/repos/pytorch/pytorch/pulls/191306)为 `created_at=2026-07-28T06:21:07Z`、`closed_at=2026-08-28T20:01:20Z`、closed/merged=false/merged_at=null，最终 head 为 `e3612cabaf142656e49584f2e1119e4b8ff7e507`。[2026-08-27 redesign 评论 5440524234](https://api.github.com/repos/pytorch/pytorch/issues/comments/5440524234)明确 forward 决策传播；[关闭评论 5457176688](https://api.github.com/repos/pytorch/pytorch/issues/comments/5457176688)说明已有另一 PR。重新读取的[最终 diff](https://api.github.com/repos/pytorch/pytorch/pulls/191306/files?per_page=100)包含 `test/inductor/test_layout_optim.py`、`torch/_inductor/compile_fx.py`、`torch/_inductor/cudagraph_utils.py`、`torch/_inductor/output_code.py`，不再是 PR 初始正文中的 backward 节点计数改法。其作者自报的测试不能移作 #188236 的落地验证。
- **E05 — 引入与落地 commit**：重新读取 [PR #178945](https://api.github.com/repos/pytorch/pytorch/pulls/178945)、[9c6b1aa07d56 commit](https://api.github.com/repos/pytorch/pytorch/commits/9c6b1aa07d56296da76db2b6c429d7b32efbe2eb)及其父提交对比，确认 2026-05-13 的 MergeBot 提交与 8 文件清单；引入侧含测试不等于修复侧新增本案回归测试。[82b424c7 commit API](https://api.github.com/repos/pytorch/pytorch/commits/82b424c7f91dc9cb631af7cfe11f5ba12f0ba37d)和父提交对比确认落地仅改 graph.py（+29/−15）与 kernel/conv.py（+15/−0），message 关联 #188236；author 时间为 `2026-09-23T05:31:00Z`，committer（PyTorch MergeBot）时间为 `2026-09-23T05:31:07Z`。这一区别引出 R01。
- **E06 — 注释型 SHA**：[140baa4eec85 API](https://api.github.com/repos/pytorch/pytorch/commits/140baa4eec85ed24f50ad6a32013cfb497cd977a)的实际 patch 仅增加 4 行注释；[父 SHA 86c24e7e 的 conv.py 第 980–995 行](https://github.com/pytorch/pytorch/blob/86c24e7eb95722f737ff5f56f39a4268483344e6/torch/_inductor/kernel/conv.py#L980-L995)已经含 stride、padding、dilation 的 guard 调用。本轮未追查更早的真正行为引入点。
- **E07 — 固定源码的支持范围**：重新读取 [994f78b1 的 graph.py 第 757–835 行](https://github.com/pytorch/pytorch/blob/994f78b19267fdeb5292595db1fd4d5aa3d9b100/torch/_inductor/graph.py#L757-L835)与 [conv.py 第 1074–1110 行](https://github.com/pytorch/pytorch/blob/994f78b19267fdeb5292595db1fd4d5aa3d9b100/torch/_inductor/kernel/conv.py#L1074-L1110)：前者可确认前向节点计数、强制开关与空计数返回逻辑；后者将 CUDA 非 HIP 路径的 Triton 反向卷积候选禁用，但布局处理仍在 lowering 内。主 issue 的局部 runner 列有 `torch.ops.aten.convolution_backward.default` 调用。静态快照与局部 runner 不能替代两种配置的完整运行轨迹，也不能建立 C03 所写的 kernel 因素排除实验。

### 两项旧发现的剩余关闭条件

**C01：因果纠正成立，MPS 的定量背景仍缺。** 正文第 61 行的“约 4×训练步延迟比，独立负载与精度”没有告诉读者是什么模型、什么精度、相对哪条基线。上游 E02 实际提供的是作者自定义小卷积网络 `Net/Block`、Apple M5 Pro/macOS 27、`torch 2.14.0.dev20260807`、输入 `(256, 3, 32, 32)`、bf16 autocast；主复现输出 eager 25.59ms/step、compiled 114.48ms/step，即 compiled/eager 为 4.47。它既不是本文 fp16 MobileNet 的负载，也不是“默认布局相对关闭布局”的 4.47 倍。补一条紧凑说明即可，不要求纳入另一个完整案例；同时将 registry 的约 4× 说明指向该独立口径。原 P1 的修复次生因果不再是开放点，剩余为 P2 的测量范围问题。

**C03：第 74 行必须修订，不能宣称三态化已经完成。** 将其改为“独立 kernel 归因未建立；布局开关对照支持布局相关候选，但不能单独隔离 kernel/布局/工具链交互”，或者按实际执行分支分别说明新增 Triton 候选的适用性与未取得的动态证据。不要继续用“kernel 慢则改布局也应慢”作反证；该前提本身没有证据，也不是有效的排除推理。保留第 75 行质量 unknown 和第 73 行工具链未排除即可，无需补造实验或执行 GPU 测试。

来源记录第 39 行起的修订段本轮作为对首轮记录的更正读取，不把其前文第 5、12、13、16、24、26、33 行的旧说法当作重新确立的事实，也不为同一历史残留重复生成发现编号。后续引用该记录应指向修订段，不能再引用旧段落证明“次生回归”或“140baa 行为修复”。

## 2. 新发现

### B25-T07-R01 — P3 / OPEN：新增秒级“落地时间”混用了 author 与 committer 字段

- **位置**：正文第 64 行“经 MergeBot 落地 main（05:31:00）”；registry 第 6495 行的相同时间；来源记录第 43 行。
- **问题**：E05 的 `05:31:00Z` 是 `commit.author.date`，而 PyTorch MergeBot 的 `commit.committer.date` 是 `05:31:07Z`。修订新增的秒级对应把作者时间直接写成了 MergeBot 落地时间，且正文和 registry 没注明 UTC。PR 的 `05:31:12Z` 则是 `closed_at`，不能与 Git author 时间当作同一种事件时间比较。
- **影响范围**：不改变“同日落地、随后关闭”或 #188236 对应该 commit 的结论；该关联有 message、diff 与 bot 评论共同支持。问题仅是来源时间字段的精确归属，不是新的 P1 因果错误。
- **关闭条件**：正文、registry 和来源修订段统一写为“author `2026-09-23T05:31:00Z` / committer（MergeBot）`2026-09-23T05:31:07Z` / PR closed_at `2026-09-23T05:31:12Z`”，或删除不必要的秒级时间，仅保留日期。即使采用 committer 时间，也不将其夸称为 API 已记录的精确 main ref 更新时间。

除 R01 外，本轮未确认需要另行编号的新问题；C01、C03 的残留继续使用原编号，不通过重新编号掩盖未闭环状态。

## 3. 总体判定

**总体判定：本轮定向复核未通过，T06-07 尚不能声明通过既定审阅范围。** 修订已纠正主要时间顺序、PR 语义、开关方向、环境登记、message/diff 混淆、摘要截断和互链问题；但 C01 的剩余测量背景、C03 的无效 kernel 排除以及新增 R01 仍开放。下一轮只需围绕这三处文档证据与表述定向复核，不要求执行硬件实验。

| 验收条款 | 本轮判断 | 依据与剩余项 |
|---|---|---|
| 1. 官方案例；登记版本、模型、精度、并行、输入及实际测量口径 | **部分满足** | 主案例的命令、版本、batch、精度、非分布式公开命令及输入尺寸 unknown 已补齐，C02/C04 可关闭；保留的 MPS 约 4× 数字仍缺独立负载、bf16 和 eager 分母的实际说明，C01 未完全关闭。 |
| 2. 时间线包含现象、最早证据、候选机制、区分检查、修订与可确认复测 | **部分满足** | #188236 早于 issue、MergeBot 落地、#191306 redesign/关闭原因、140baa 注释型 diff、开关对照/PR 作者报告/最终 SHA 未确认复测已分层。C03 的错误排除仍影响“区分检查”的解释，R01 要修正秒级字段归属。 |
| 3. 区分作者报告、源码推断和本库未复现；未知修复版本/条件明确标示 | **部分满足** | 质量 unknown、release tag unknown、未复现与最终 SHA 绑定未确认均可保留。但第 74 行仍将不足以排除候选的开关数据写成“反驳”，与同表的证据纪律不一致，C03 仍开放。 |
| 4. 与性能分析/慢 rank 交叉链接，说明可/不可推广边界 | **满足既定导航与方法范围** | 三篇关联正文的互链及 06.6 入口均已核对；单卡与 rank 偏斜、NVIDIA 与其他后端的边界有说明，C08 关闭。MPS 方法反例的因果位置已改正，其数值背景仍按条款 1 的 C01 跟踪，不重复记缺口。 |

### 结构检查与执行边界

- `make check` 与 `make build`：在临时完整副本中通过，**107 content entries / 525 sources**；未改写原工作树 `build/`。临时副本最初排除了 `build/`，因既有 `docs/first-fill-status.md` 链接到 catalog 而未通过预检查；复制现有构建基线后重新执行两项命令并成功重建。这是临时副本的准备问题，不计作正文缺陷或技术验证。
- 已独立核对 YAML 解析值与重建 catalog 的完整 summary，C07 关闭；结构检查不核验远程事实、kernel 选择、性能因果、版本兼容或硬件行为。
- 报告写入后再次在原工作树执行 `make check`，并将报告纳入临时副本重跑 `make check` / `make build`，均通过。写前快照中的 528 个既有源文件哈希均未变化；核验期间还观察到其他任务的三份新报告，本轮未创建或修改它们，本轮唯一新增文件为本报告。
- 未修改 `src/kb/`，未运行其单元测试；未执行上游评论中的测试命令。正文继续保持 `draft / source_checked`，本轮不授予 `reviewed` 或 `reproduced` 状态。

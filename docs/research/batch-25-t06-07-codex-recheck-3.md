# Batch 25 T06-07 第四轮定向复核报告

- 日期：2026-10-20（本地 Asia/Shanghai）；上游时间字段按 UTC 记录。
- 依据：[初审报告](batch-25-t06-07-codex-review.md)、[第二轮复核报告](batch-25-t06-07-codex-recheck.md)、[第三轮复核报告](batch-25-t06-07-codex-recheck-2.md)、[来源记录](batch-25-t06-07-sources.md)第三轮修订段及 [T06-07 验收条款](../../plans/full-coverage-backlog.yaml)。本轮重点是重新读取两条 registry 登记，核对 C01、R01 的剩余同步条件，并检查已关闭项和修订引入的新问题。
- 执行方式：当前本地 Codex CLI 会话独立复核，未委托子代理；当前约定模型/档位为 `gpt-6.1-sol / xhigh`。本轮未取得可独立核验的启动模型元数据，不宣称实际执行模型已核验，也未另行运行其他模型。
- 写入范围：仅新增本报告，不修改正文、来源登记、来源记录、导航、既有报告或原工作树的 `build/`。未运行上游示例、训练、GPU/MPS 基准或硬件验证。

复核快照 SHA-256：

| 文件 | SHA-256 |
|---|---|
| `knowledge/06-training/performance-regression-source-case.md` | `8bd432f5e933dc91cf447bba9f9502431e23cdd5629856a376518b5b470ecb2c` |
| `docs/research/batch-25-t06-07-sources.md` | `42da448dc489d22d7df23008c3bfb322b6543eab697594f1c47fce6e85beeab1` |
| `sources/registry.yaml` | `6be465aebd3aa52ac672b532eb1d0af8ed4bdc3296c8c4a37dc3282ad55484fe` |

下文行号针对上述快照；正文哈希与第三轮复核完全一致。

## 1. C01、R01 定向判定

**C01 CLOSED；R01 CLOSED。** 上一轮仅余的两项 registry 同步均已完成；本轮不是仅依据作者修订摘要作出关闭判断。

| 编号 | 判定 | 核对位置 | 关闭依据 |
|---|---|---|---|
| B25-T07-C01（初审 P1；上一轮剩余 P2） | **CLOSED** | registry 第 6480–6489 行，重点为 `src.pytorch.issue-189239-layout-regression.notes`；来源记录第 56–59 行；正文第 61、85、87 行 | 重新解析登记确认：保留的 MPS 数字已补齐独立负载、输入、精度、机器/系统、compiled/eager 分母、版本归属和作者机器自测声明，并指向 issue 正文与案例时间线。与重新打开的 #192551 相符，见 E01。登记仍明确这是同期独立的平台镜像问题，先于本案修复存在并关闭，不是修复引入的次生回归；满足上一轮剩余关闭条件。 |
| B25-T07-R01（P3） | **CLOSED** | registry 第 6490–6500 行，重点为 `src.pytorch.layout-opt-fix-chain.revision`；来源记录第 54、59 行；正文第 64 行 | 登记已把 PR `closed_at`、commit author、MergeBot committer 的 UTC 时间字段分列，不再把 `05:31:00` 用作 MergeBot committer 时间。逐字段与重新读取的 commit API、PR 元数据一致，见 E02、E03；正文、最新修订段和来源登记三处同步完成。 |

### E01：重新打开 MPS 原始报告，核对独立测量口径

本轮重新读取 [issue #192551 完整正文](https://github.com/pytorch/pytorch/issues/192551)，定位 Describe the bug、复现代码、Output、shape sweep 和 Versions，而非仅用标题中的“4x”。报告明确限定为小型 conv 网络、batch 256、32×32 输入、bf16 autocast、Apple M5 Pro/macOS 27，数字来自报告者机器。登记中的 nightly 约 4.5×、`2.13.0` 约 9×，均为 **compiled 相对 eager 的训练耗时比**，不是布局开/关比值，也不是本案例 fp16 MobileNet/batch 512 的结果。

nightly 输出为 `2.14.0.dev20260807`，eager `25.59 ms/step`、compiled `114.48 ms/step`，标示 `4.47x eager`；约 9× 来自开头对 `2.13.0` release wheel 的独立陈述，不能借用 nightly 原始时延作为 release 实测值。正文保留“其试过的 shape”和“数字来自作者机器”的限制；registry 未新增跨 shape 或跨后端保证。[同一 issue 的关闭活动](https://github.com/pytorch/pytorch/issues/192551)仍位于 2026-08-17，早于本案 2026-09-23 的落地提交；本轮不扩展核验 #193623 的实现或修复版本。

### E02、E03：重新读取秒级时间字段

| 证据 | 上游实体与字段 | 重新取得的值 | 登记核对结果 |
|---|---|---|---|
| E02 | [commit `82b424c7f91dc9cb631af7cfe11f5ba12f0ba37d` API](https://api.github.com/repos/pytorch/pytorch/commits/82b424c7f91dc9cb631af7cfe11f5ba12f0ba37d)，`commit.author.date` | `2026-09-23T05:31:00Z` | 与 `author 时间 05:31:00Z` 一致 |
| E02 | 同一 commit API，`commit.committer.name` / `commit.committer.date` | `PyTorch MergeBot` / `2026-09-23T05:31:07Z` | 与 `MergeBot committer 时间 05:31:07Z` 一致 |
| E03 | [PR #188236 元数据](https://api.github.com/repos/pytorch/pytorch/pulls/188236)，`closed_at` | `2026-09-23T05:31:12Z` | 与 `closed_at 05:31:12Z` 一致 |

网页读取工具未能打开两项 API 后，本轮改用已连接的 GitHub 工具成功取得 commit API 和 PR 元数据。PR 仍为 `closed`、`merged=false`、`merged_at=null`；[落地 commit 的 message](https://github.com/pytorch/pytorch/commit/82b424c7f91dc9cb631af7cfe11f5ba12f0ba37d)明确关联 #188236，不能以标准 merge 标志否认该对应关系，也不能以这些时间字段代替实际性能复测。committer 时间本身不等于独立核验过的 main ref 精确更新时间；本轮没有新增该类断言。

## 2. 已关闭项防回归

**C02、C03、C04、C05、C06、C07、C08 均维持 CLOSED，未确认回归。** 正文逐字节未变是防回归依据之一；本轮同时检查两项登记的其余字段、最新来源修订段、相关导航及生成清单。除 E01–E03 外，历史上游事实沿用第三轮已核对的证据，不声称本轮重做了初审的全部取证。

| 编号 | 本轮位置与检查结果 |
|---|---|
| C02（P2） | 正文第 36、59、87、93 行及 registry 第 6489 行仍为默认慢、强制启用快；eager speedup 与布局开关对照分开，20%+ 保留作者归属，20.5%/25.7% 保留算术换算而非本库测量的限定。新增 MPS 倍数没有覆盖或混入主案例基线。 |
| C03（P2） | 正文第 50、72–75、94 行仍明确固定源码可确认的节点计数/开关逻辑与完整因果排除不同；工具链和 kernel 因素未排除，收敛/质量 unknown。上一轮已修好的 kernel 行未恢复“改布局后应仍慢”的反证前提，registry 也未新增已排除措辞。 |
| C04（P2） | 正文第 40–48、66、83–87、100、106 行保留软件版本、batch、计量选项、单卡范围、输入尺寸 unknown、作者性能报告与最终 SHA 同条件复测未绑定的边界。MPS 独立环境不充当 NVIDIA/Intel 的缺失条件。 |
| C05（P2） | 正文第 58、63–64、79、95 行及 registry 第 6495、6500 行仍区分 #188236 主线与 #191306 另一提案，未把后者的 redesign/测试移作最终落地验证；本轮重开的 E02、E03 亦支持 #188236 身份与生命周期叙述。R01 字段同步没有重引入 PR 角色错误。 |
| C06（P2） | 正文第 57、98 行及 registry 第 6484 行仍写明 `140baa4eec85` 的已核 diff 仅四行注释、guard 调用此前已存在、真正行为变更点未确认；未恢复以 message 标题充当该 SHA 行为修复的说法。该历史 diff 证据沿用第三轮，不新增行为追溯结论。 |
| C07（P3） | 实际解析 frontmatter 并核对临时重建 catalog：稳定 ID 对应的完整 summary 与源字段逐字一致，包含 `issue #189239` 及末尾 MPS 平台边界说明；未发生 YAML 井号截断。 |
| C08（P3） | slow-rank 第 82 行、机制页第 263 行、performance-analysis 第 144 行、训练章 index 第 69、78 行的普通 Markdown 返回链接均在；案例第 91、94、97 行保留对应出链，未把单卡案例提升为分布式慢 rank 实测。 |

## 3. 新问题检查

**本轮未确认新增问题，不新增 R02 等编号。** 检查重点包括两项登记能否独立理解、数字的分母及版本归属、UTC 时间字段、因果与验证范围、YAML 解析及 catalog 消费结果；没有以“正文已通过”为由跳过 registry。

[来源记录](batch-25-t06-07-sources.md)第 5、12–16、24、26、33、43 行等早期观察仍有“次生”、旧 PR 顺序或未分列时间的历史表述。其后第 39–59 行按修订顺序明确更正这些观察；沿用第三轮的历史记录处理，不把已被后续段落更正的旧文本当作新的现行断言。本轮重点核验的 registry 则已实际同步，不再依赖历史记录豁免。

既有 unknown 继续保留：修复所属 release tag、MPS/#193623 修复链、完整输入/Intel 型号、最终 SHA 的同条件性能与质量复测，以及分布式和其他后端表现。它们不因登记同步而自动补齐，也不作为本轮新发现重复编号。

## 4. 最终整体判定

**T06-07 通过既定审阅范围。** 初审 C01–C08 共 **8 项全部 CLOSED**，后续新增 **R01 CLOSED**；累计 **9 项 CLOSED、0 项 OPEN**，本轮新增问题 **0 项**，无开放 P1/P2/P3。

本轮完成的是第三轮遗留的来源登记闭环及定向防回归：独立 MPS 测量背景和秒级时间字段均与重新取得的精确证据相符；此前已通过的对照方向、证据分层、环境/复测边界、PR 身份、message/diff 区分、摘要与互链没有回归。不要求为通过本次审阅补造缺失实验或确定尚未知的版本归属。

该判定是内容与来源审阅结论，不是模型启动元数据合规认证、硬件验证或跨平台兼容认证。正文继续保持 `draft / source_checked`；本报告不授予 `reviewed` 或 `reproduced` 状态，不宣称本库运行成功、训练质量已验证或最终落地 SHA 已完成性能复测。

## 5. 结构检查与写入边界

- 在包含原有 `build/` 基线的完整临时副本中执行 `make check`、`make build`，均通过：**107 content entries / 525 sources**；未在原工作树运行会重写构建产物的 `make build`。
- 实际解析 YAML，并核对重建 catalog 的两项来源记录与 registry 完全一致；新增 MPS 条件、分母、版本及三个 UTC 时间字段均进入生成物。案例 summary、`draft / source_checked` 也与源字段一致。
- 本轮未修改 `src/kb/`，不新增内容测试、未运行其单元测试。上述校验只覆盖结构、本地文件链接与生成物一致性，不验证远程链接、技术因果或硬件行为。
- 报告写入后，原工作树 `make check` 及含本报告的临时副本 `make check` / `make build` 均通过，计数仍为 107 / 525。
- 写前对 538 个既有项目文件建立哈希快照（不含 Git/虚拟环境/缓存），其中 537 个未变，正文、registry、来源记录及既有报告均未变；新增文件仅为本报告。另观察到原工作树 `build/catalog.json` 在核验窗口内发生变化，内容与临时重建结果相同，写入者未在本轮确定。已检查本轮临时构建导入的模块及默认根目录均位于临时副本；未回写、恢复或覆盖该生成文件，不把原工作树的同期变化冒称为本轮修改或“所有既有文件均未变化”。

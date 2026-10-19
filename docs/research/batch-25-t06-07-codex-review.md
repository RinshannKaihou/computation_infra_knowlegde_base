# Batch 25 T06-07 初审报告（gpt-6.1-sol / xhigh）

- 日期：2026-10-20（Asia/Shanghai）；下表上游时间统一采用 GitHub API 的 UTC，避免与本地日期混用。
- 审阅对象：[训练吞吐回归来源案例](../../knowledge/06-training/performance-regression-source-case.md)，连同[来源记录](batch-25-t06-07-sources.md)、[来源登记](../../sources/registry.yaml)中两个本批条目、[训练章导航](../../knowledge/06-training/index.md)及三个指定关联正文。
- 审阅方式：当前本地 Codex CLI 会话独立初审，未委托其他审阅者；标题按任务指定的模型/档位记录。本轮未取得可独立核验的 CLI 启动模型元数据，不补写“已核验实际模型”的结论。
- 对象快照：正文 SHA-256 `d56a7c7fd2610a4a370c35bb747592aaed28db573c65e184bba1b80c9d39a3fc`；来源记录 SHA-256 `170efb2af81f8bc41122da4819bd9ad26bc7ff5cd7599ba173822895d5ca6a31`。下列正文行号针对该快照。
- 写入范围：仅新增本报告，不修改正文、来源记录、registry、导航及其他已有文件。未执行训练、上游回归测试、性能复跑或硬件验证。

## 核对范围与取证方式

已重新阅读 `README.md`、`docs/authoring-guide.md`、`content-outline.md`、元数据 schema 和 T06-07 四条验收条款；检查正文全文、两个新增来源登记、06.6 场景入口，以及与 `performance-analysis.md`、`slow-rank-triage.md`、`operators-compilers-and-graphs.md` 的链接方向。

本轮终端 `gh api` 请求因网络连接受限失败；随后通过已连接的 GitHub 工具直接读取官方仓库 API 的 issue、事件、PR 元数据、文件清单、commit 元数据与 diff，并用网页定位讨论段落。未把搜索摘要、PR 标题或作者的来源记录当作代码变更的替代证据。网页缓存曾将 #188236 显示为 open；本报告的状态以本轮实时 API 返回为准。

### 日期、状态与文件清单核对

| 上游对象 | 本轮独立核对结果 | 对正文的判断 |
|---|---|---|
| [Issue #189239](https://github.com/pytorch/pytorch/issues/189239)及[事件流](https://api.github.com/repos/pytorch/pytorch/issues/189239/events?per_page=100) | 创建于 `2026-07-08T06:30:30Z`，关闭于 `2026-09-23T13:59:15Z`；关闭事件 ID `31681488164`，操作者 eellison，事件未绑定 commit。当前 labels 确含 high priority、module: regression、module: performance、module: memory format、module: inductor。 | 第 50、54 行日期、当前标签和“同日关闭”成立；关闭本身不证明已在落地 SHA 上完成性能复测。 |
| [PR #178945](https://github.com/pytorch/pytorch/pull/178945) | 创建于 `2026-03-31T23:40:36Z`，关闭于 `2026-05-13T03:54:25Z`；API 为 `state=closed`、`merged=false`、`merged_at=null`。 | 原始 API 状态成立；应与下列 MergeBot 落地事实一起解释，不能等同于代码没有入库。 |
| [Commit 9c6b1aa07d56296da76db2b6c429d7b32efbe2eb](https://github.com/pytorch/pytorch/commit/9c6b1aa07d56296da76db2b6c429d7b32efbe2eb)及[父提交对比](https://github.com/pytorch/pytorch/compare/2fa68666022236704278cfbbdd7b3df65e602893...9c6b1aa07d56296da76db2b6c429d7b32efbe2eb) | author 为 chien-an-chen，committer 为 PyTorch MergeBot，两者日期均为 `2026-05-13T03:54:20Z`；message 标题对应 Triton 反向卷积实现并关联 #178945。共 8 个文件，完整清单见下文。 | 第 48 行日期、引入 lowering 及其布局分支有依据；这不是已通过本库二分验证的性能引入点。 |
| [Commit 140baa4eec85ed24f50ad6a32013cfb497cd977a](https://github.com/pytorch/pytorch/commit/140baa4eec85ed24f50ad6a32013cfb497cd977a) | author 为 Lakshay Garg，committer 为 PyTorch MergeBot，日期均为 `2026-05-21T02:24:40Z`；message 标题描述 dilation guard 并关联 #184255。仅改 `torch/_inductor/kernel/conv.py`，实际 diff 为新增 4 行注释。 | 第 49 行日期、message 对得上，但把该 SHA 的实际效果写成“修正类型问题”不成立，见 C06。 |
| [PR #188236](https://github.com/pytorch/pytorch/pull/188236)及[文件清单](https://api.github.com/repos/pytorch/pytorch/pulls/188236/files?per_page=100) | 创建于 `2026-06-26T01:58:47Z`，关闭于 `2026-09-23T05:31:12Z`；`merged=false`、`merged_at=null`。最终 head 为 `6e9593090530d61bfa40cbaafde80e4267124866`；仅改 `torch/_inductor/graph.py` 和 `torch/_inductor/kernel/conv.py`。 | 第 51 行“2026-07 提交”错误；这是早于主 issue 的公开 PR。须区分 API 的 merge 标志与 MergeBot 落地路径，见 C05。 |
| [PR #191306](https://github.com/pytorch/pytorch/pull/191306)及[文件清单](https://api.github.com/repos/pytorch/pytorch/pulls/191306/files?per_page=100) | 创建于 `2026-07-28T06:21:07Z`，关闭于 `2026-08-28T20:01:20Z`；`merged=false`、`merged_at=null`。最终 head 为 `e3612cabaf142656e49584f2e1119e4b8ff7e507`；文件为 `test/inductor/test_layout_optim.py`、`torch/_inductor/compile_fx.py`、`torch/_inductor/cudagraph_utils.py`、`torch/_inductor/output_code.py`。 | 第 52 行创建日期、closed unmerged 及“携带该测试文件改动”成立；最终方案不同于初始 PR 正文所述的直接计数方案，不宜只凭标题串为同一修复的第二轮。 |
| [Issue #192551](https://github.com/pytorch/pytorch/issues/192551) | 创建于 `2026-08-07T22:36:36Z`，关闭于 `2026-08-17T09:05:42Z`。作者给出的 MPS 示例为 25.59/114.48 ms 每训练步，即延迟比 4.47；正文把 #189239 描述为 CUDA/XPU 的镜像布局问题。 | 第 53 行 UTC 日期、关闭状态及约 4× 现象有依据；“本案修复带出的次生回归”没有依据，见 C01。 |
| [Commit 82b424c7f91dc9cb631af7cfe11f5ba12f0ba37d](https://github.com/pytorch/pytorch/commit/82b424c7f91dc9cb631af7cfe11f5ba12f0ba37d)及[父提交对比](https://github.com/pytorch/pytorch/compare/9186b190a054d20bb060de831eb04008f55c61fd...82b424c7f91dc9cb631af7cfe11f5ba12f0ba37d) | author 为 Yang, Shuxin，时间 `2026-09-23T05:31:00Z`；committer 为 PyTorch MergeBot，时间 `2026-09-23T05:31:07Z`。message 关联 #188236；只改 `torch/_inductor/graph.py` 和 `torch/_inductor/kernel/conv.py`，分别为 +29/−15、+15/−0。 | 第 54 行日期、两文件清单及“不含测试文件改动”成立；“修复 release tag unknown”可保留，未执行逐 tag 包含关系核对。 |

`9c6b1aa07d56` 的 8 文件清单为：`test/inductor/test_torchinductor.py`、`test/inductor/test_torchinductor_codegen_dynamic_shapes.py`、`torch/_inductor/config.py`、`torch/_inductor/kernel/conv.py`、`torch/_inductor/kernel/templates/triton_conv2d_bwd_input.py.jinja`、`torch/_inductor/kernel/templates/triton_conv2d_bwd_weight.py.jinja`、`torch/_inductor/lowering.py`、`torch/_inductor/utils.py`。其中引入侧包含卷积测试，不等同于修复侧新增了本案布局回归测试。

## 发现列表

共 8 项：1 P1、5 P2、2 P3。均为开放发现；本报告不执行修订或替作者关闭问题。

### B25-T07-C01 — P1：把先于修复发生的 MPS 镜像问题写成修复引入的次生回归

- **受影响位置**：正文第 14、34、53、72、82、89、91 行；来源记录第 3、5、16、26、33 行；registry 两项登记中“次生”“修复适用范围风险”的相关表述。
- **问题描述**：正文不只把 #192551 当作平台差异反例，而是宣称本案修复“带出”它，并据此总结完整的“修复→次生风险”周期。#192551 在 2026-08-07 已公开、2026-08-17 已关闭；本文认定的修复落地却在 2026-09-23。现有证据没有把 MPS 问题归因到 #188236 的实验分支或其落地 SHA。把相关问题写成修复造成的问题，构成案例核心因果链错误。
- **证据（上游定位）**：[MPS issue 正文](https://github.com/pytorch/pytorch/issues/192551)将 #189239 作为布局选择方向相反的对照；[2026-08-17 关闭评论](https://github.com/pytorch/pytorch/issues/192551#issuecomment-5314010885)明确指向 #193623，早于 [82b424c7](https://github.com/pytorch/pytorch/commit/82b424c7f91dc9cb631af7cfe11f5ba12f0ba37d)。本轮只核对这条关闭说明，未据此宣称完成 #193623 全链审核或本地验证。
- **建议关闭条件**：将其改为“同期独立的 MPS 镜像问题/平台边界反例”，删除已发生的修复次生因果关系，连同摘要、来源记录及登记同步修正；将“修复须覆盖其他后端”保留为方法建议而非本案已证明的事故事实。约 4× 必须标为该 issue 作者报告的训练步延迟比，并交代其独立负载与精度，不能与本案 fp16 MobileNet 对照混用。

### B25-T07-C02 — P2：现象段把布局对照方向写反，且没有交代 speedup 的基线

- **受影响位置**：正文第 36、50、62、73 行；来源记录第 22 行及 registry 对应数值说明。
- **问题描述**：第 36 行称“相对关闭布局优化的同一工作负载”出现回归，而公开 CSV 的方向恰是默认决策下较慢，强制启用布局优化后较快。两组 speedup 也不是“相对旧版本”的吞吐值，而是各自相对 eager 的比值。若不区分这两个基线，读者会反向理解区分检查，并把约 20% 时延下降、固定工作量下约 25.7% 吞吐提升、作者报告的 20%+ 回归混为同一指标。
- **证据（上游定位）**：[Issue #189239 的 Performance regression 两组命令与 CSV](https://github.com/pytorch/pytorch/issues/189239)：默认 `abs_latency=178.413744`、强制布局后 `141.905300`，对应 speedup `1.448819`、`1.821338`；[PR #191306 的 Benchmark data 段](https://github.com/pytorch/pytorch/pull/191306)明确该 speedup 的 eager 对照口径。按两组原始时延计算，下降比例约 20.46%，反向吞吐提升约 25.73%；这只是对作者数值的算术换算，不是本库测量。
- **建议关闭条件**：明确“默认反向图布局优化未启用”与“强制启用”的方向，分别定义 eager speedup 和布局开关对照；保留作者的 20%+ 原始表述及归属，不把该两组 CSV 当作已冻结旧版/新版的性能二分或落地后复测结果。

### B25-T07-C03 — P2：调查表和现象段仍把缺证据的判断写成确定事实

- **受影响位置**：正文第 36、42、60、62、79 行，尤其“训练正常收敛”“排除了单纯工具链假设”“被反驳”“单看任何一侧都不会出问题”。
- **问题描述**：上游性能基准与生成代码片段不提供训练收敛曲线或质量结论，也没有正文声称的完整工具链排除实验。布局开关对照支持布局相关候选，但不能排除工具链与布局交互，亦不能凭“强制开启后变快”逻辑排除所有 kernel 相关因素。此外，新 lowering 不等于 NVIDIA 实际选择了 Triton 反向卷积 kernel。全页末尾统一声明“作者报告/本库未复现”，不能为这些未在作者记录中出现的事实补证。
- **证据（上游定位）**：[Issue #189239](https://github.com/pytorch/pytorch/issues/189239)给出性能 CSV 与局部 runner，无收敛验证；其反向卷积调用片段是 ATen extern 调用。[固定快照 conv.py](https://github.com/pytorch/pytorch/blob/994f78b19267fdeb5292595db1fd4d5aa3d9b100/torch/_inductor/kernel/conv.py#L1074-L1110)在 CUDA 非 HIP 路径禁用 Triton 反向卷积候选，而布局变换仍位于 lowering 中。[固定快照 graph.py](https://github.com/pytorch/pytorch/blob/994f78b19267fdeb5292595db1fd4d5aa3d9b100/torch/_inductor/graph.py#L757-L835)可以印证节点计数/开关逻辑，不能证明全套因果排除。
- **建议关闭条件**：把收敛与长期质量改为 unknown；调查表分别注明作者报告、固定源码可确认的分支和本库推断，将未测的候选记为“未排除/尚缺对照”。区分 lowering、布局转换、后端选择与实际执行 kernel；将绝对排除改为证据范围内的支持性结论，不要求补造新的实验。

### B25-T07-C04 — P2：已取得的版本、输入和计量条件未登记，可确认的修复方复测范围也被省略

- **受影响位置**：正文第 34、40、50、66–73、91 行；来源记录第 22、24、30–35 行。
- **问题描述**：正文自称给出完整输入和测量口径，实际只写模型及 fp16/training，nightly 让读者另查 issue，未登记 batch=512、禁用 CUDA Graphs、性能/冷启动相关选项，也未交代并行范围和输入空间尺寸的已知/未知。它还仅留下布局开关 CSV，未区分修复 PR 作者自己的性能声明与最终落地 SHA 是否完成同条件复测。因此验收条款 1、2 不能由“见 issue”或关闭日期替代。
- **证据（上游定位）**：[主 issue 的命令、CSV 和 Versions](https://github.com/pytorch/pytorch/issues/189239)可直接取得 batch=512、CUDA 设备参数、`--disable-cudagraphs`、`-n 10`、`--cold-start-latency`，以及软件包记录 `torch==2.14.0.dev20260706+cu130`、`triton==3.8.0+git43422b04`；其环境采集的 PyTorch/build CUDA 字段同时为 N/A，不能忽略这种边界。[PR #188236 Results](https://github.com/pytorch/pytorch/pull/188236)报告 Intel Data Center GPU 上约 1.3×；同页 2026-09-02 作者评论另报告 Intel Client GPU 和 RTX 4080 SUPER 上 1.3×+，但没有给出足以将这些结果绑定到最终落地 SHA 的完整条件。Intel 型号、输入尺寸、分布式设置等不能自行补全。
- **建议关闭条件**：正文增加紧凑的历史环境/测量表：逐项登记可得字段、CSV 指标定义及完整命令链接；并行只能记“公开命令未配置分布式/实际配置待确认”等证据允许的范围，不把两张显卡清单解释为双卡训练。分开列出开关对照、PR 作者性能报告、最终 SHA 的可确认复测范围；缺少固定版本、原始结果、重复性或质量条件时明确 unknown，不把不同 Intel 平台合并成同一组测量。

### B25-T07-C05 — P2：首个修复 PR 的日期错误，PR 生命周期被压成了“两轮未合并后直接提交”

- **受影响位置**：正文第 14、34、51、66、89 行；来源记录第 5、13、24 行；registry 第 6495、6500 行。
- **问题描述**：#188236 于 2026-06-26 创建，早于 2026-07-08 issue，而不是第 51 行的“2026-07 提交”。“两轮修复 PR 后以直接 commit 落地”虽然附有“非标准 merge”的限定，仍掩盖了二者不同的角色：#188236 由 MergeBot 落地，#191306 因已有另一 PR 而关闭，不是两个失败修复之后另起无关直接提交。#191306 的最终改动还已转为 forward 决策向 lazy backward 传播，而非初始正文的 backward 节点计数方案。
- **证据（上游定位）**：[PR #188236 API](https://api.github.com/repos/pytorch/pytorch/pulls/188236)给出上述创建时间；[merge 请求](https://github.com/pytorch/pytorch/pull/188236#issuecomment-5788157002)、[MergeBot 启动说明](https://github.com/pytorch/pytorch/pull/188236#issuecomment-5788173882)及 [82b424c7 message](https://github.com/pytorch/pytorch/commit/82b424c7f91dc9cb631af7cfe11f5ba12f0ba37d)共同建立其入库关联。[#191306 关闭评论](https://github.com/pytorch/pytorch/pull/191306#issuecomment-5457176688)说明已有 PR；[最终 head 的 compile_fx.py](https://github.com/pytorch/pytorch/blob/e3612cabaf142656e49584f2e1119e4b8ff7e507/torch/_inductor/compile_fx.py)和同 PR 2026-08-27 的重新设计说明、最终文件清单表明方案已变化。
- **建议关闭条件**：把 #188236 创建日期改为 2026-06-26，补上其早于 issue 的顺序；保留两 PR 的原始 `closed/merged=false/merged_at=null`，同时明确 #188236 经 MergeBot 对应到落地 commit、#191306 是另一条被关闭的提案。用具名 PR 和固定 head 区分初始方案、最终 diff 与落地方案，避免用“两轮”暗示串行修订或代码均未入库；不得把 #191306 的测试/作者测试声明移作 #188236 的验证。

### B25-T07-C06 — P2：把 commit message 描述的 dilation 修复当成该 SHA 的实际代码修改

- **受影响位置**：正文第 42、49、81 行；来源记录第 12 行；registry 第 6484 行。
- **问题描述**：`140baa4eec85` 的标题确实涉及 dilation guard，但这个 SHA 的实际 diff 只增加解释性注释，未新增或改变 guard。正文直接称其“修正前述 lowering 的类型问题”，并用它作为回归引入与报告之间的修订节点，超出了本轮可见代码证据。
- **证据（上游定位）**：[该 commit 的完整 diff](https://github.com/pytorch/pytorch/commit/140baa4eec85ed24f50ad6a32013cfb497cd977a)仅一文件、+4/−0，全部为注释；[父提交 conv.py](https://github.com/pytorch/pytorch/blob/86c24e7eb95722f737ff5f56f39a4268483344e6/torch/_inductor/kernel/conv.py#L980-L995)已经包含 stride、padding、dilation 的 `guard_int_seq` 调用。故 message 与实际 diff 的语义需要分别记录。
- **建议关闭条件**：将该行改为“message 描述 dilation 问题，所核 SHA 实际仅补充注释；真正行为变更点未确认”，或另行找到并核对真正引入 guard 的提交后再补入时间线。同步修正来源登记，不能仅凭标题宣称实际修复或测试通过。

### B25-T07-C07 — P3：未引用的 summary 被 YAML 的井号注释静默截断

- **受影响位置**：正文 frontmatter 第 14 行。
- **问题描述**：`summary` 为未加引号的 YAML 标量，其中 `issue #189239` 的空格加井号开启注释。实际加载到 Agent 内容清单的摘要只有 `PyTorch 官方仓库的公开训练性能回归链（issue`，后半段不属于字段值。它仍满足非空字符串 schema，所以结构校验不能发现这一内容丢失。
- **证据（定位）**：本轮对该快照执行 YAML 解析，得到上述截断值；[编写指南](../authoring-guide.md#3-元数据约定)已经明确要求含 ` #` 的标题/摘要整体加引号。此项为本地格式问题，无需上游证据。
- **建议关闭条件**：修订事实内容后给完整摘要加 YAML 引号或使用合适的块标量，构建并检查 catalog 中该稳定 ID 的真实摘要值，不只看 `make check` 退出状态。

### B25-T07-C08 — P3：场景导航已接入，但两个指定关联页尚无返回案例的链接

- **受影响位置**：[slow-rank-triage.md](../../knowledge/06-training/slow-rank-triage.md)与[operators-compilers-and-graphs.md](../../knowledge/02-software-stack/operators-compilers-and-graphs.md)的相关入口；案例第 15–18、77–85 行。
- **问题描述**：案例已经出链至三个关联正文；`performance-analysis.md` 第 119 行也已返回案例。06 章场景表及 06.6 地图均已接入，不是缺失项。但 slow-rank 与算子/编译机制页均没有返回案例的普通 Markdown 链接或稳定 ID 引用，未完整达到本任务要求核对的“互链”。
- **证据（定位）**：本地逐页核对与链接搜索结果；[章入口](../../knowledge/06-training/index.md#场景指南案例与实验)有训练吞吐回归行，[性能分解](../../knowledge/06-training/performance-analysis.md)第 119 行有案例链接，另外两页未检出案例路径、ID 或 issue 编号。此项为导航问题，无需上游证据。
- **建议关闭条件**：在 slow-rank 的均匀变慢/非 rank 偏斜边界，以及编译机制页的布局决策示例处分别补一条返回案例的链接。只做导航，不复制案例正文，也不把单机开关结果当作分布式慢 rank 的实测证明。

## 已确认的边界与保留项

- `status: draft`、`verification.status: source_checked`、空环境档案及“本库未复现”声明可保留；稳定 ID、关联 ID 和登记 ID 结构正确。`platforms: [nvidia]` 不应因提到 Intel/MPS 就自动扩成多平台验证声明。
- 两个修复 PR 的实时 API 均为 closed 且 merged=false，此原始字段事实没有被本报告推翻；必须按 C05 补充其不同入库/关闭语义。
- 82b424c7 仅改两个生产文件，因此“该落地 commit 未新增/修改回归测试”成立；#191306 确实改了 `test_layout_optim.py`。不得反向扩张为“整个仓库没有相关测试”“CI 未运行”或“回归永远没有测试覆盖”；本轮未做全仓及后续提交的测试覆盖审计。
- 修复所属 release tag 未核对，保留 unknown 合理。issue 关闭、源码包含修改、上游作者性能报告和硬件复现是不同层次，不能相互替代。
- 20%+、两组 CSV、约 4× 及修复方的 1.3× 均为上游报告；本报告的比例计算也只建立在这些上游数值上。未取得原始运行产物、完整测试条件或本库性能结果。

## 结构检查

- `make check`：通过，107 content entries / 523 sources。
- `make build`：在完整临时源码副本中执行，通过并生成 catalog，避免更改原工作树的 `build/`。从该 catalog 读取本案例的摘要，确认仍为 C07 所列截断值。
- 检查后正文和来源记录的 SHA-256 与本报告开头快照一致。结构/链接检查不核验远程技术事实、PR 状态、因果关系或硬件性能；本轮未更改 `src/kb/`，未运行其单元测试，也未运行任何上游测试。

## 总体判断与验收条款对照

**总体判断：初审不通过，需修订后定向复核。** 案例选题和官方来源有效，结构具备案例骨架，但目前不能称为已核实的完整“回归→修复→次生回归”周期。开放的 C01 必须先纠正；C02–C06 的测量、因果和提交解释亦需闭环，不能因来源可访问或构建成功直接宣告通过。

| 验收条款 | 判断 | 尚需关闭的缺口 |
|---|---|---|
| 1. 官方案例，登记版本、模型、精度、并行、输入及实际测量口径 | 部分满足 | 官方来源、模型、fp16、作者 CSV 已有；版本、batch、测量选项、并行与输入 unknown 未在正文充分登记；对照方向和 speedup 基线需改正（C02、C04）。 |
| 2. 时间线覆盖现象、最早证据、机制、区分检查、修订与可确认复测 | 部分满足 | #188236 的日期和角色错误，MPS 被误串因果，140baa 的 message 与 diff 未区分；开关对照、修复 PR 报告和最终 SHA 复测需分层（C01、C04–C06）。 |
| 3. 区分作者报告、源码推断、本库未复现；未知修复版本/条件显式记录 | 部分满足 | 未复现及 release tag unknown 已明确；收敛、工具链排除、kernel 反证和 MPS 次生归因仍越过证据。统一页末免责声明不能替代逐项归属（C01、C03、C04、C06）。 |
| 4. 与性能分析/慢 rank 交叉链接，说明推广与不推广边界 | 基本满足，互链有小缺口 | 案例出链、性能分解返回链、场景表及推广限制已有；slow-rank 与机制页缺返回链（C08），可迁移经验中须去掉未证实的次生因果和绝对排除（C01、C03）。 |

编辑及机器可读交付还需关闭 C07。修订范围应落在事实、证据等级和链接，不要求为了通过初审虚构 GPU/MPS 实验、补齐未知 release tag，或执行本任务未授权的任何环境修改。

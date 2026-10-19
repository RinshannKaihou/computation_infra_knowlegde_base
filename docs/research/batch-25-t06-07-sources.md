# 第二十五批 T06-07 来源记录

任务：T06-07（训练吞吐回归的公开证据案例；**new** case `knowledge/06-training/performance-regression-source-case.md`，主题 06.6）。取证轮次：主会话作者角色首轮（2026-10-20）。案例固定 **pytorch/pytorch issue #189239（Inductor 布局优化未计入 convolution_backward 致训练性能回归）**，全链经 gh API（issue/PR/commit search）观察；本库未复现任何基准。

案例选择口径：筛选 PyTorch/Megatron 官方仓库中带完整输入与版本信息的训练吞吐/负载回归链。备选淘汰记录：Megatron #678（get_batch 回归，2024 开/2025-12 以 age+不可复现关闭，仅 referenced commit 无修复链）；pytorch #174575（reduce-overhead 7x 回归，场景为推理引擎且关闭无 commit、无修复链）；pytorch #201443/#201120（open 无修复）。最终选择 #189239：训练场景、根因链完整（引入 commit→回归报告→两轮 PR→落地 commit）、带官方基准命令与对照开关、且带次生回归 issue（#192551）——可同时演示"回归引入—检测—修复—次生风险"全周期。

## 本轮观察清单（2026-10-20，gh API）

| 对象 | 状态与时间 | 关键字段 |
|---|---|---|
| issue #189239 | opened 2026-07-08、closed 2026-09-23 | labels: high priority/module: performance/module: regression/module: memory format/module: inductor；基准命令与两组 CSV 数字；TORCHINDUCTOR_FORCE_LAYOUT_OPT=1 对照 |
| 引入侧 PR #178945（Triton backward convolution kernel） | PR closed unmerged；commit 9c6b1aa07d56（2026-05-13）落地 main | issue 正文指认为回归引入源；后续 guard 修复 140baa4eec85（2026-05-21，dilation cast） |
| 修复 PR #188236 | closed unmerged（2026-07） | decide_layout_opt 计入 convolution_backward |
| 修复 PR #191306 | opened 2026-07-28、closed unmerged | 标题含 "20% training regression"；**携带 test/inductor/test_layout_optim.py 改动** |
| 落地 commit 82b424c7f91d | 2026-09-23（Yang Shuxin） | 标题 "[inductor]: Include convolution_backward in decide_layout_opt conv node detection (#188236)"；文件仅 torch/_inductor/graph.py＋kernel/conv.py（**无测试**） |
| 次生 issue #192551 | opened 2026-08-07、closed | MPS 上布局优化强制 channels_last 使 compiled training 比 eager 慢 4× |

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 回归现象与测量口径 | NEW src.pytorch.issue-189239-layout-regression | issue 正文：基准 `benchmarks/dynamo/timm_models.py --float16 --training --only mobilenetv3_large_100`；speedup 1.448819→1.821338、abs_latency 178.41→141.91ms（TORCHINDUCTOR_FORCE_LAYOUT_OPT=1）；平台 RTX4080 SUPER＋Intel Data Center GPU | 作者自测数字；20%+ 回归结论、对照开关的区分力 |
| 根因机制（作者定位） | NEW src.pytorch.issue-189239-layout-regression | issue 正文：decide_layout_opt() 仅统计 aten.convolution.default；AOTAutograd 拆图后 backward 图只含 convolution_backward→conv_nodes 空→layout_opt 静默关闭→PR 178945 的 lowering 检查 V.graph.layout_opt 决定 NHWC，关闭时保持 NCHW | 报告者自述根因与修复方实现一致；本库未复现、不宣称确定根因 |
| 引入与修复时间线 | NEW src.pytorch.layout-opt-fix-chain | 引入 9c6b1aa07d56（2026-05-13）→报告 2026-07-08→修复尝试 PR 188236/191306（均 closed unmerged）→落地 82b424c7（2026-09-23）→issue 同日关闭 | 两轮 PR 未按标准 merge 路径合并、由直接 commit 落地（"Pull Request resolved"标注）；时间线可核对 |
| 回归测试缺口 | NEW src.pytorch.layout-opt-fix-chain | 落地 commit 文件清单仅 graph.py/conv.py；PR 191306 携带的 test_layout_optim.py 未随落地 | "修复落地但回归测试未上"的事实边界——正文不得写成"已带回归测试闭环" |
| 次生风险 | NEW src.pytorch.issue-189239-layout-regression（notes） | #192551：MPS 布局强制 channels_last 4× 慢于 eager | 修复扩大适用面引入的新风险形态；其自身修复链未核对 |
| profiler/性能分解入口 | 复用 src.pytorch.profiler-2.6、src.pytorch.inductor-profiling-2.6 | （既有） | 回归定位的工具背景 |
| 慢 rank 区分方法 | 复用 training.slow-rank-triage 正文 | （既有） | 受害慢节点 vs 最早瓶颈的区分框架互链 |

## unknown 清单

1. 修复 commit 82b424c7 进入哪个 release tag 未逐 tag 核对（issue 关闭时点为 main 线）。
2. 次生 issue #192551 的关闭原因与修复链未核对（仅作风险形态记录）。
3. Intel Data Center GPU 侧 20% 数字为作者报告，具体型号未在正文给出。
4. 基准数字（178.41/141.91ms）为作者环境自测，本库未复现；正文全部标注"作者报告"。
5. PR #178945 引入变更时的评审记录（是否讨论过 layout 交互）未核对。
6. Megatron/MindSpeed 侧未找到同时满足完整输入与修复闭环的训练吞吐回归链（Megatron #678 无修复闭环）——本批以 PyTorch 案例交付，跨框架推广边界在正文声明。

## 修订轮补充（2026-10-20，初审 B25-T07-C01–C08 后，关键事实经作者 gh API 复核）

- **C01（P1，因果链更正）**：#192551（MPS）创建于 2026-08-07、关闭于 2026-08-17（关闭链指向 #193623），**早于本案修复落地（2026-09-23）**——它是同期独立的平台镜像问题（布局方向相反），不是本案修复引入的次生回归。正文、registry 标题与 notes 均已更正。
- **C02（对照方向与基线）**：默认配置慢（178.41ms/eager speedup 1.448819）、强制启用快（141.91ms/1.821338）；speedup 为相对 eager 的比值而非版本对比；20%+ 为作者表述，约 20.5%/25.7% 为作者数值的算术换算（已标注）。
- **C05（PR 生命周期）**：#188236 创建 **2026-06-26**（早于 issue 2026-07-08；作者 gh API 复核 created_at 一致）、经 MergeBot 对应落地 commit 82b424c7（05:31:00）并同刻关闭（05:31:12）；#191306 于 2026-08-28 因维护者"already a pr out for this"关闭，其 redesign（forward 决策向 lazy backward 传播，最终 head 含 compile_fx.py）与测试改动均未落地。
- **C06（commit message≠diff）**：140baa4eec85 所核 diff 仅 +4 行注释（guard_int_seq 调用此前已存在）；registry revision 已注明。
- **C04（环境/口径补登）**：torch==2.14.0.dev20260706+cu130、triton==3.8.0+git43422b04、batch=512、-n 10、--cold-start-latency、--disable-cudagraphs、公开命令未配置分布式、输入尺寸未给出、Versions 的 CUDA 字段 N/A；PR #188236 Results 的 Intel DC GPU ~1.3× 与 2026-09-02 评论 RTX 4080 SUPER 1.3×+（PR 作者自报，与落地 SHA 绑定未确认）。
- **C03（推断分层）**：删除"训练正常收敛""排除工具链""单看任何一侧都不会出问题"等超出证据的断言；假设表改为支持/未排除/unknown 三态；lowering/布局转换/后端选择分层表述。
- **C07（summary 截断）**：frontmatter summary 加引号（原未引用值在 `issue #189239` 处被 YAML 注释截断）。
- **C08（回链）**：slow-rank-triage.md（完成判据节）与 operators-compilers-and-graphs.md（适用边界前）已补案例回链。

## 第二轮修订（2026-10-20，复核轮一 C01 剩余/C03 剩余/R01 后）

- **C01 剩余**：MPS 反例补测量背景——小型 conv 网络、batch 256@32×32、bf16 autocast、Apple M5 Pro/macOS 27；compiled 相对 eager 的训练耗时 nightly 约 4.5×、2.13.0 约 9×、关布局后转为优势；数字来自作者机器。
- **C03 剩余**：假设表 kernel 行改为不排除表述（开关对照说明布局差异占主导，不构成对 kernel 因素的排除实验；布局变化可能改变 kernel 访存/调用/选择）。
- **R01**：时间线 commit 行的时间字段分列——author 时间 05:31:00Z、MergeBot committer 时间 05:31:07Z、PR 关闭 05:31:12Z，不混用。

## 第三轮修订（2026-10-20，复核轮二 C01/R01 registry 同步后）

- **C01 registry 同步**：src.pytorch.issue-189239-layout-regression notes 的 #192551 数字补独立口径（小型 conv 网络/batch 256@32×32/bf16 autocast/M5 Pro；compiled 相对 eager nightly 约 4.5×、2.13.0 约 9×，作者机器自测）。
- **R01 registry 同步**：src.pytorch.layout-opt-fix-chain revision 的时间字段分列（PR closed_at 05:31:12Z；commit author 05:31:00Z、MergeBot committer 05:31:07Z）。

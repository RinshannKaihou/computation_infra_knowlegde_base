# 后续 T05/T06 训练场景来源准备

读取日期：2026-09-30。主任务只读核查；未运行源码、训练、保存/加载或诊断工具。本记录供下一批 `gpt-5.6-sol/high` 写作使用，仍须在成文后接受 astra/xhigh 审阅。

## T05：GPU → NPU 数值差异

### 固定 msprobe 官方指南

通过 `git ls-remote --symref` 确认 msprobe master/HEAD 为 `7783f6b2d0cbae0e2f6200b05e604a09d7820c50`。检索结果中的旧 `docs/en/wiki/train_debug_guide.md` 已不在该快照；沿固定 README 找到并下载实际文档，只读选读以下范围：

| 精确来源 | 已读范围与用途 |
|---|---|
| [训练精度定位指南](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/best_practices/train_debug_guide.md) | 1、2.1、2.2、2.3.1、2.3.2、2.4、3.1 和 3.2.1：前置对齐、固定输入/随机性、复现缩小、首差异与观测干扰；真实案例章节缺型号/版本/日期，不能直接伪装完整事故 |
| [精度比对](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md) | 结构、API 匹配、指标/Result、阈值解释的定位；正式写具体公式或工具命令前再读完整相应段落 |
| [安装指南](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/install_guide/msprobe_install_guide.md) | 前 100 行：工具分发形态与功能不同；未安装，也不沿外链构建环境 |
| [许可说明](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/legal/license_notice.md) | 明确 docs 文档许可与产品许可分开，实际读取所链两个 LICENSE |
| [docs/LICENSE](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/LICENSE) | CC-BY-4.0；外链图、匿名日志及第三方内容不自动覆盖 |
| [产品 LICENSE](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/legal/LICENSE) | MulanPSL-2.0 文本；未核查全部文件头/依赖/wheel，安装指南另有 EULA 声明，不把所有分发形态混为一种许可 |

临时只读文件：`/tmp/kb-t05-msprobe-{readme,guide,compare,install,license}.md`、`/tmp/kb-t05-msprobe-docs-license.txt`、`/tmp/kb-t05-msprobe-product-license.txt`。不是知识正文附件或运行证据。

正式流程的处理原则：

- 复用 F13/F18、E01/E02 与 `src.pytorch.numerical-verification-2.6`；两份平台档案不是匹配实验的现成环境。
- 对齐同一输入字节、权重、模型语义、dtype/layout、数据/训练进度及并行策略；不能把相同 seed 当跨设备同一随机张量。
- 区分有限精度差异、非有限值、训练过程偏离与下游质量。先在各自平台重复，再跨平台比较；容差由任务和参考实现确定。
- 工具文档的 1%、0.99 或其他标红规则不是本库通用验收阈值。CPU/FP64 可作为条件明确的参考，不写成无条件绝对真值。
- 加 dump、同步或换融合实现后故障消失，支持时序/实现依赖假设，不独立证明内存踩踏或唯一根因。观测本身改变时序、内存与 I/O，实验需要保留未插桩对照。
- 原指南的升级/改代码/更换库等建议不自动成为第一步。先固定证据，在独立环境设计单变量验证；不执行这些动作。

### 真实案例候选 #17

已打开 [Ascend/pytorch #17](https://github.com/Ascend/pytorch/issues/17) 正文与元数据：2023-12-19 提交，目前 Open。报告比较 V100 与 910B 上的 SFT 收敛，列出 NPU 侧 Ubuntu 20.04、CANN 7.0.RC1、Python 3.9、torch 2.1.0、torch_npu 2.1.0rc1.post20231013；涉及 PEFT/TRL/Accelerate，但这些库版本与 GPU 软件栈未给全。

报告把 DDP bucket stride 警告及两段 reducer 代码差异列为怀疑对象，没有给出因果对照或修复复验。适合记录“已有环境线索但根因未定”的来源案例；不得把性能警告直接解释为数值错误，更不能把注释中的性能影响当梯度算错证据。静态页面未取得评论，不声称无评论。若正式写作认为环境缺口不足以满足任务验收，应保留 T05-C 待办，而不是补写未给出的模型、数据或版本。

其他初筛：msprobe 指南 3.1/3.2 有来源作者的简要案例，但缺历史环境和日期；Gitee 检索返回的个别页带贡献者访问提示，不继续获取其隐藏内容，也不纳入本批案例。无需绕过限制，已有公开 GitHub 候选。

## T06：Checkpoint 恢复状态异常

优先采用既有 PyTorch 2.6 DCP 与 F14 来源作为流程样板，保持默认 planner 去重/Rank-local 边界的第四批修订。真实案例可用另一明确历史版本，不混写为同一软件环境。

已读 [PyTorch #164257](https://github.com/pytorch/pytorch/issues/164257) 正文和 [PR #165228](https://github.com/pytorch/pytorch/pull/165228) 讨论/合并记录，以及实际 [commit edd8d356b6d9a00cfa34fa323578e5cf1c7e0463](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463) 的单文件 diff：

- 2025-09-30 的报告来自 macOS 26/Apple M3、Python 3.13.1、PyTorch 2.8.0、无 CUDA，单进程 DCP。不是 GPU/NPU 事故，也不能冒充 NPU 恢复验证。
- 未参与 loss 的参数没有对应 optimizer state，示例在装载/应用状态时触发 `KeyError: bias`；原文的示例新建 model2/optimizer2 后调用仍传原对象，需要按原文记录，不能悄悄修好后宣称已复现。
- PR 页面顶端显示 Closed，但底部 bot 记录于 2025-11-05 以 `edd8d35` 落库并标 Merged。固定 commit 明确引用该 Issue/PR，diff 给缺失 FQN 增加存在性和 strict 分支。
- 这支持“上游有特定修订”而非“任意恢复均正确”；首个包含修订的发行版、回移植与实际复验未知。本轮没有运行报告中的删除目录或保存/加载脚本。

备选 [#140900](https://github.com/pytorch/pytorch/issues/140900) 也已读：2024-11-17、PyTorch 2.5.0/CUDA/H100，报告 flattened optimizer 恢复后 `initial_lr` 缺失；页面 Closed，未取得评论/修复链，优先级低于有明确 commit 的 #164257。

## 拟登记来源

写作方可据实际使用补齐 schema YAML 后交主任务登记，建议稳定 ID：

- `src.ascend.msprobe-training-guide-2026-09-30`：固定仓库文档，revision 完整 SHA；许可 partial，docs CC-BY-4.0、声明的产品范围 MulanPSL-2.0，制品与第三方未知。
- `src.ascend.pytorch-issue-17`：Issue 类型按 schema 所允许枚举选择，网页许可 unknown，仅原创摘要与短必要字段。
- `src.pytorch.dcp-issue-164257`：报告、PR/commit 分别明确范围；Issue 评论许可不因 PyTorch 源码许可而自动已知。需要时为固定修订单独登记 repository 类型。

正式来源表尚未合并这三项。P/C 的 source_checked 只指来源整理，X 必须 not_verified 且无测量结果。真实案例保留作者报告、维护者动作、源码推理和本库未知四种证据身份。

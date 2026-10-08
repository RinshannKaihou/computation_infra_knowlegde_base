# 第七批独立审阅记录

审阅日期：2026-09-30。审阅角色：独立 `gpt-6-astra / xhigh`。本记录保留初审发现；所列正文行号对应首次读取的修订前版本，后续修改可能移动行号。

初审结论：发现 **2 项 P2**，均在 T06 的 DCP 调用边界或实验分组；没有发现 P1。T05、T07 及本批新增来源、导航/计划在本次核查范围内没有新增阻断问题。两项 P2 修订后需要定向复核，再由主任务更新交付状态。本记录不把未提供硬件、未知发行版或公开案例未闭环本身列为缺陷。

## 范围与实际核查

先读取 [AGENTS.md](../../AGENTS.md)、[README](../../README.md)、[写作指南](../authoring-guide.md)及[内容归属](../../content-outline.md)。完整审阅 T05、T06、T07 的 P/C/X 九篇，及对应 [T05 来源记录](batch-07-training-sources.md)、[T06 来源记录](batch-07-checkpoint-sources.md)、[T07 来源记录](batch-07-inference-source-candidates.md)、[本批来源审计](batch-07-source-audit.md)。抽查五项新增来源登记、训练/推理章节与平台/任务路径，以及 backlog 和填充计划的范围与状态。

实际取得的原始证据包括：

- msprobe 固定 `7783f6b2d0cbae0e2f6200b05e604a09d7820c50` 的[训练指南随机张量段](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/best_practices/train_debug_guide.md#L305-L330)、[比对文档](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)、[许可说明](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/legal/license_notice.md)、[docs LICENSE](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/LICENSE)和[产品许可文件](https://github.com/Ascend/msprobe/blob/7783f6b2d0cbae0e2f6200b05e604a09d7820c50/docs/zh/legal/LICENSE)；PyTorch 2.6 [Numerical accuracy](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html)。
- GitHub 连接器重新取得 [Ascend/pytorch #17](https://github.com/Ascend/pytorch/issues/17)正文、Open 状态和 [2029286848 评论](https://github.com/Ascend/pytorch/issues/17#issuecomment-2029286848)。评论结果未提供时间或 author association，不据此提升为维护者结论。
- PyTorch 2.6 [DCP 文档](https://docs.pytorch.org/docs/2.6/distributed.checkpoint.html)、固定 v2.6.0 `load`、非 tensor 写入项和去重源码；[Issue #164257](https://github.com/pytorch/pytorch/issues/164257)正文、关闭元数据和四条评论；[PR #165228](https://github.com/pytorch/pytorch/pull/165228)审阅/讨论时间线；固定 [edd8d356 修订](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463)、其 `state_dict.py`/`default_planner.py` 和 [LICENSE](https://github.com/pytorch/pytorch/blob/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463/LICENSE)，并对照 v2.8.0 的 optimizer 初始化路径。连接器返回的 PR `merged: false` 没有单独用作未合入判断；网页时间线的 Merged 标签、bot 指向 `edd8d35` 的关闭事件与固定提交相互印证。
- 固定 vLLM `b17039bccc17b94a2ea107272ad7bc93508708df` 的 [stats.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/v1/metrics/stats.py#L233-L377)和 [serve.py](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/benchmarks/serve.py)，Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696` 的 [conf.py](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/conf.py#L62-L80)；连接器重新取得 [#17443](https://github.com/vllm-project/vllm-ascend/issues/17443)正文、Open 状态及空评论列表。

外部网页、源码和评论只作为证据读取。没有运行 `make`、上游脚本、PyTorch、msprobe、benchmark 或 profiling；没有安装、创建训练环境、读取集群/设备状态、保存/加载 checkpoint 或进行硬件验证。54 entries / 63 sources 是主任务提供的既有结构检查结果，本审阅没有独立重跑。审阅者只新增本报告。

## P2-01：fresh-object 分组不能直接验证 missing-FQN 修订分支

**定位：** [T06-X](../../knowledge/06-training/checkpoint-state-recovery-experiment.md)初审第 59–64 行（U0/F0/S0），第 113 行的 H1 判据；[T06 来源记录](batch-07-checkpoint-sources.md)的 N0/F0/S0 对应表。

**问题与影响：** 原矩阵把 fresh-object 的 F0 指定为验证缺失 state 被跳过、S0 指定为验证新增 strict RuntimeError，却没有控制 `AppState.state_dict()` 生成的目标 state。按 Issue 的包装器和本设计指定的 AdamW，fresh optimizer 会在 DCP 的目标状态获取阶段生成 bias 的占位 state。宽松读取可能把它保留到 `set_state_dict`，使 `_split_optim_state_dict` 看见 bias FQN 已存在，因而没有检验修订的缺失分支。F0 不报错会形成错误的修订验证；U0 也不能预设与旧对象 Q0 命中同一错误。

该结论来自代码静态核对，不是本地测量：

1. [Issue 包装器](https://github.com/pytorch/pytorch/issues/164257)在 `state_dict()` 中调用 `get_state_dict`。固定修订的 [`_get_optim_state_dict` 第 896–899 行](https://github.com/pytorch/pytorch/blob/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463/torch/distributed/checkpoint/state_dict.py#L896-L899)先调用 `_init_optim_state`；[第 615–654 行](https://github.com/pytorch/pytorch/blob/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463/torch/distributed/checkpoint/state_dict.py#L615-L654)在 optimizer state 为空且没有梯度时，对所有 `requires_grad` 参数建立零梯度、以零学习率 step 初始化 state。v2.8.0 也有[同一路径](https://github.com/pytorch/pytorch/blob/v2.8.0/torch/distributed/checkpoint/state_dict.py#L605-L654)。
2. [`create_default_local_load_plan` 第 470–476 行](https://github.com/pytorch/pytorch/blob/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463/torch/distributed/checkpoint/default_planner.py#L470-L476)在 partial load 下跳过 metadata 中缺失的目标 key，不会因此删除目标里的初始化 state。因此必须检查读取后的实际 FQN 和值的来源，不能把目标占位值当已恢复历史。
3. [修订分支第 1009–1017 行](https://github.com/pytorch/pytorch/blob/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463/torch/distributed/checkpoint/state_dict.py#L1009-L1017)判断的是传入 optimizer state 中是否仍缺 FQN。输入已被占位值补齐时，strict false/true 都无法按预期区分该分支。
4. S0 的装载选项还只写 strict true，未保留 F0 的 partial-load。如果采用默认 planner 的 `allow_partial_load=False`，fresh target 的 bias key 在 checkpoint 中缺失会先触发 planner 的 missing-key 错误；它不是本实验要验证的 `_split_optim_state_dict` RuntimeError。仅把 partial-load 补回去又会遇到上述占位状态问题。

**修复建议：** 将“修订分支的最小回归”与“fresh-object 端到端装载”分开。前者确保进入 `set_state_dict` 的输入真实缺少 bias FQN，保留旧对象 Q0 对照，或使用已定义的直接 state-dict fixture；对 strict false/true 只改变对应选项，明确异常调用层和消息。后者保留 fresh-object，但记录 get 前、get 后、DCP read 后、set 前后的 key/FQN、state 来源与参数组，按实际路径解释结果，不预设一定命中缺失分支。宽松装载留下或生成的 bias state 应有独立应用契约；继续训练需与预先定义的参考轨迹比较。若跨 2.8.0 和较晚 main 的整体差异要归到单一提交，还需单独控制其余版本变化。

## P2-02：DCP `load` 的成功返回并非一律只覆盖读取

**定位：** [T06-P](../../knowledge/06-training/checkpoint-state-recovery-triage.md)初审第 57 行“因此返回只属于读取 API 边界”，以及第 70、80 行的装载分层；[T06 来源记录](batch-07-checkpoint-sources.md)“复用的已审机制”第 2 项。主任务追踪到 [F14](../../knowledge/06-training/checkpoint-state-consistency.md)初审第 80–85 行有同类表述，属于本问题的直接传播点，仅需定向修正该处。

**问题与影响：** 文本没有区分普通 state dict 和 `Stateful` 输入。PyTorch 2.6 `dcp.load` 接收 `Stateful` 对象时，在返回前会先取得其 state dict、完成内部读取，再同步调用该对象的 `load_state_dict`。因此对象回调中的 optimizer 错误可能就是外层 `dcp.load` 的失败；不能要求先存在“load 成功返回”才进入对象后处理排查，也不能因返回值为 `None` 就断言回调尚未执行。T06-C 的实际堆栈正是这种嵌套调用。

**原始证据：** 固定 v2.6.0 [`state_dict_loader.py` 的 Stateful 契约](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_loader.py#L67-L72)与[实际调用顺序](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_loader.py#L158-L191)；[#164257 的 load→AppState.load_state_dict→set_state_dict 堆栈](https://github.com/pytorch/pytorch/issues/164257)。

**修复建议：** 保留“API 成功不证明训练正确”的主结论，但条件化 API 边界：普通字典路径需应用后续调用对象装载；`Stateful` 路径在外层返回前已完成配置的回调，回调是否正确传播模型/optimizer 状态仍须审计。按调用堆栈区分 planner/read/callback/set 的最早失败，在流程中明确内部阶段与外层返回不是同一件事。同步修改研究记录及 F14 的直接传播语句。

## 本轮确认保留的边界

| 范围 | 核对结论 |
|---|---|
| T05 数值与工具 | 相同 seed 不保证跨 GPU/NPU 同随机张量；条件 FP64 参考、任务容差与 msprobe 筛选规则分开；首差异及插桩扰动有明确限制。没有把工具阈值或跨平台差异提升为硬件结论。 |
| T05 公开案例 | #17 的症状、NPU 部分环境、GPU 栈缺口与 Open 状态相符；DDP stride warning 没有被写成收敛根因，评论者身份和缺失复验没有升级。 |
| T06 案例与 rank-local | 2.8.0/macOS CPU 案例与 2.6 planner 样板分开；旧对象 quirk、四条评论与固定 diff 描述相符。默认非 tensor 同 FQN 去重没有内容相等检查；未把选定写入者固定为 coordinator。首个发行版与 GPU/NPU 复测继续未知。 |
| T07 指标与版本 | TTFT/E2E 的 frontend wall-clock 与 core phase/ITL 的 monotonic 分开；没有把客户端减服务端当网络时间。vLLM 0.14.0 与插件 conf 的 0.14.1 未拼成兼容组合。成功样本过滤、TPOT 单 token 排除、并发与到达速率、吞吐窗口的引用与固定实现相符。 |
| T07 案例与实验 | #17443 的 Open、125/128 成功、TTFT p99 172.47 秒与源报告相符，评论查询为空；版本与长度混杂、均值不足以证明 decode 健康、input/TTFT 非 kernel 吞吐、min TTFT 非零排队均保留。实验的负载/缓存、失败、质量、观测扰动与恢复条件有区分。 |
| 登记、导航与许可 | 九篇主归属与稳定 ID 清楚，P/C 为限定范围 source_checked、X 为 not_verified，正文仍 draft；路径以链接聚合并标出 CPU 案例边界。msprobe 文档/产品许可与分发包范围分开，Issue/PR 未继承代码许可；本批没有镜像外部全文。 |

## 修订后的定向复核要求

主任务修订后，只复核以上两项的变更及直接传播位置：T06-P/X、T06 研究记录、F14 的调用边界语句；确认新设计没有把静态推演写成实际结果，且未新造发行、环境或运行证据。结构检查与构建仍由主任务执行，不以其通过代替本次技术复核。

## 定向复核与最终状态（2026-09-30）

**最终结论：两项 P2 均已关闭；复核中发现的源码锚点 P3 也已修正并关闭。本批在本次审阅范围内没有剩余 P1/P2 或未关闭发现。** 关闭表示正文、实验设计与所核对源码的语义一致，不表示实验已执行或 GPU/NPU 恢复已验证。

本次只复读 T06-P/X、T06 来源记录、F14 的 Stateful 表格与说明，以及 registry 中 `src.pytorch.dcp-2.6` 和 `src.pytorch.dcp-fix-edd8d35` 的扩充范围，没有重审其余基础内容。

| 发现 | 状态 | 定向复核结果 |
|---|---|---|
| P2-01：fresh-object 遮蔽缺失分支 | **关闭** | T06-X 第 69–93 行改为先核对 source-native/source-get 的真实缺 bias 输入，再直接执行 parent/fixed 的 `set_state_dict` 对照；第 95–118 行将端到端占位观测与受控缺键夹具分开。P0/F0/S0、EP/EF、BP/BF/BS、D0 的判定层次不再混用。 |
| P2-02：Stateful 返回边界 | **关闭** | T06-P 第 57、70、80 行以及 F14 第 80–87 行明确区分普通映射、内部读取、Stateful 回调和公共 `load` 返回；研究记录同步。回调失败不再被表述为外层已正常返回。 |
| P3-01：复核新增的 v2.8.0 原文件锚点偏移 | **关闭** | T06-X 第 51 行和研究记录第 90–91 行原用了网页转换后的 562–598、717–774、863–878，未对应 GitHub 文件行号。主任务已改用固定 commit 和真实的 605–644、774–835、932–952；planner 的 315–352、453–492 原本正确。 |

### P2-01 的关闭依据

[固定修订的 GitHub commit API](https://api.github.com/repos/pytorch/pytorch/commits/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463)返回唯一 parent `658c5f879c37142b1df51c7eb6c5a5bb06318597`，只修改 `state_dict.py`，8 行增加、1 行删除。新版 P/F 对照固定这个父子关系、相同构建参数与依赖；2.8.0 只承担历史症状对照，不再承担单补丁因果判断。

A 的前提现在有可核对的代码链：源对象先完成仅 weight 的一次更新，使 optimizer state 非空但无 bias；[parent `_init_optim_state`](https://github.com/pytorch/pytorch/blob/658c5f879c37142b1df51c7eb6c5a5bb06318597/torch/distributed/checkpoint/state_dict.py#L615-L654)会因非空 state 早退，随后必须再次检查 source-get 的 FQN。目标端 set 前不调用 get。`set_state_dict` 内部虽会初始化目标 optimizer，但[装载函数](https://github.com/pytorch/pytorch/blob/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463/torch/distributed/checkpoint/state_dict.py#L1059-L1079)仍将独立传入的 source state dict 交给 `_split_optim_state_dict`，没有在这条路径上把 target 新建 bias state 合并进入参。因此新设计允许 P0/F0/S0 真正覆盖[缺失 FQN 的旧/新分支](https://github.com/pytorch/pytorch/commit/edd8d356b6d9a00cfa34fa323578e5cf1c7e0463)，同时要求观察调用后的目标 state，避免把分支允许缺失等同历史恢复正确。以上是静态源码判断；运行结果仍待验证。

B 的 EP/EF 保留 fresh target 的完整 skeleton，目的改为观察初始化/partial skip，而不声称覆盖补丁；BP/BF 只裁剪来源已确认缺失的 bias optimizer FQN，BS 只改变 strict，均保留 `allow_partial_load=True`。D0 将普通字典读取返回与显式 set 分开。四个观测点记录 target-native、target-get、DCP 读取后/回调入口、set 前后，能识别占位 state 的来源。夹具裁剪被明确限定为测试用途；误删其他 state 使该组无效，异常对象销毁，不转化为生产恢复处方。原问题的遮蔽和提前 planner 失败已被设计区分。

### P2-02 的关闭依据

[固定 v2.6.0 loader](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/checkpoint/state_dict_loader.py#L53-L189)显示：对映射中的 Stateful 值先取 state dict，内部读取完成后调用 load 回调，再离开公共函数。T06-P、F14 和研究记录现均表达这一顺序，并继续保留“回调返回不能证明回调语义、跨对象状态或续训正确”的限制。registry 的 `src.pytorch.dcp-2.6` 只扩充到已经使用的去重与 loader 源码，没有新增平台兼容或运行保证。

### P3-01 的核对方法与修正

重新读取 [v2.8.0 tag 引用](https://api.github.com/repos/pytorch/pytorch/git/ref/tags/v2.8.0)，得到 commit `ba56102387ef21a3b04b357e5b183d48f0afefc7`。GitHub 连接器分别按 tag 和固定 commit 取原文件，`state_dict.py` 对应 blob `a430a64fad819dae2b2c99ab42f17342efbe5c1f`；按原文件换行核对了以下位置，而没有使用 web 工具重排后的展示行号：

- [`_init_optim_state` 605–644](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/state_dict.py#L605-L644)：非空 state/现存 gradient 的早退、零 LR 初始化和清梯度。
- [`_get_optim_state_dict` 774–835](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/state_dict.py#L774-L835)、[`_load_optim_state_dict` 932–952](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/state_dict.py#L932-L952)：各自的初始化调用及装载分派。
- [`default_planner.py` 315–352](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/default_planner.py#L315-L352)、[453–492](https://github.com/pytorch/pytorch/blob/ba56102387ef21a3b04b357e5b183d48f0afefc7/torch/distributed/checkpoint/default_planner.py#L453-L492)：partial 选项转为计划 strict 值，以及缺 key 时跳过读请求。

已复读主任务修正后的正文、研究记录与 registry；固定 SHA、锚点及登记范围一致。复核期间一次普通 shell 只读 HTTPS 获取因 DNS 不可用失败，随后通过已连接的 GitHub 读取完成核对，没有以失败请求冒充已读证据，也没有运行下载到的源码。

本次仍未运行 `make`、上游程序、安装/构建、保存/加载、训练、集群或硬件操作。实验保持 `not_verified` 且没有测量结果，正文保持 `draft`；本报告的关闭结论不替代主任务的结构检查和构建。

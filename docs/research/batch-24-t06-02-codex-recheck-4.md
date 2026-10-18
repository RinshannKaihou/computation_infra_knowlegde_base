# Batch 24 · T06-02 Codex 定向复核第四轮报告

- 复核日期：2026-10-19（Asia/Shanghai）。
- 结论：**通过（本轮定向技术审阅范围）**。
- 第三轮遗留四项：**CLOSED 4 项、OPEN 0 项**；C07、S3-01、S3-02、S3-03 均满足原关闭条件。
- 本轮新增：**P1 0 项、P2 0 项、P3 0 项**，没有需要分配 `B24-T062-S4-xx` 的新问题。
- 只新增本报告，不修改正文、作者取证、来源登记、导航、任务计划或工作树构建产物；未执行任何训练、编译示例或上游测试。
- 执行者为本会话 Codex CLI，未派发子代理、未另启模型审阅。实际后端模型、推理档位及路由元数据没有可独立核验的记录，记为 `unknown`；不将约定模型名称写成已核实的执行事实。

## 1. 范围与输入基线

按用户要求，**只复核第三轮仍 OPEN 的四项，第三轮已 CLOSED 的九项不重查、不作关联回归审阅**。验收表中的其他条目沿用第三轮结果，本轮仅重新核对任务要求及正文落点，不重新开展这些条目的技术取证。

复核依据为[第三轮报告](batch-24-t06-02-codex-recheck-3.md)的四项关闭条件、[修订后正文](../../knowledge/06-training/framework-execution.md)的对应位置，以及[作者取证](batch-24-t06-02-sources.md)末尾“修订轮四补充”（L146–148）。用户提示中的第三轮历史路径为 `docs/research/batch-24/t06-02-codex-recheck-3.md`，仓库实际文件位于上述扁平路径；本轮读取现有报告，没有创建路径副本。

第三轮将三项新增发现原样编号为 `B24-B24-T062-S3-01/02/03`。本报告以 S3-01/02/03 简称指代它们，保留原号对应关系，不修改历史记录。新发现若存在，才使用本轮要求的 `B24-T062-S4-xx`。

已读取仓库说明、编写指南、内容归属和元数据 schema。验收依据为 `plans/full-coverage-backlog.yaml` L5880–5900 的 T06-02 objective 与五条 acceptance。以下正文及取证行号来自本轮实际文件，正文 141 行、作者取证 148 行。

| 输入 | 本轮 SHA-256 |
|---|---|
| `knowledge/06-training/framework-execution.md` | `751a922a96d36a3c61dce0d29d29012041d436c011bcc8d59c194446759bfe8d` |
| `docs/research/batch-24-t06-02-sources.md` | `e9828876162886133dc8ece5de79b4364992817458a98200b86fab936c1f9ba4` |
| `docs/research/batch-24-t06-02-codex-recheck-3.md` | `d6fea648f8c99539eaf35e54beb3cbddb306ddc154dad5bb38baf686ad3b7d06` |
| `sources/registry.yaml` | `3ea07202e7e0573c8ff8089bc5fcdd142b5a51269dc1f646a9d4a08d065215a2` |
| `plans/full-coverage-backlog.yaml` | `53bfc8fe47d56ab322e546c853858cbaa90cf5a5d0305b33a80bab0f39275d54` |

## 2. 只读重开精确上游证据

网页读取工具对四个精确地址均返回不可访问或 cache miss；随后通过只读 HTTPS GET 成功取得同一精确文件/版本化页面，检查实际内容，而不是以搜索摘要或作者“已修订”声明替代证据。源码沿用第三轮已经定位的固定 commit；本轮不额外声称重新验证 tag 指向。未 import、安装或执行上游代码。

| 证据 | 精确位置与用途 |
|---|---|
| E01 | MindSpeed-LLM [arguments.py](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/training/arguments.py#L242)：原文件 L242–282、L301–314。只核对 C07 的辅助检查、CP/Mcore 前提、算法调用范围与两级 GQA 谓词。 |
| E02 | PyTorch [test/dynamo/test_compile.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/dynamo/test_compile.py#L24)：原文件 L14–32、L149–173。只核对 S3-02 的测试类归属、单次调用的计数断言及公共 API 签名检查。 |
| E03 | PyTorch 2.6 [Troubleshooting](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html)：[Guards](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#guards)、[Recompilation](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#recompilation)、[Dynamic Shapes](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#dynamic-shapes)，本次原 HTML L738–797；[Where to apply torch.compile](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#where-to-apply-torch-compile) L901–940；[Wrapping constants with tensors](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#wrapping-constants-with-tensors) L1212–1274。用于 S3-01/S3-03。 |
| E04 | PyTorch 2.6 [torch.compile API](https://docs.pytorch.org/docs/2.6/generated/torch.compile.html#torch.compile)：本次原 HTML L588–614 的 frame 缓存、guard failure 与动态形状行为。用于 S3-01；不再将此页三角函数示例当作 S3-03 所需训练示例。 |

| 取回对象 | 本轮 SHA-256 |
|---|---|
| E01 `arguments.py` | `fd64204269ad1749159d9b98f47c91f92cb17de5075cb92670f8ab1d5df42a38` |
| E02 `test_compile.py` | `36745171714b59a3ac313ac9b8a80e5423fd95f7abb538933e6731cdbd074d3d` |
| E03 Troubleshooting HTML | `906e4b838df7c1bf0f607d7a1194da37006311e5ac440f36cbcadcb6d4865669` |
| E04 torch.compile API HTML | `a68b803c844532f2fafcf63ee3c903db88ff5cc830915315d8eb759cf8ead84b` |

两份源码摘要与第三轮引用的快照一致。HTML 行号仅是本次下载文件的定位辅助，不转换成 GitHub 源码锚点，也不假设网页字节永久不变。下载文件及检查记录保留于临时目录 `/private/tmp/b24-t062-s4.GPvX0z`，不是仓库永久证据附件。

## 3. 第三轮 OPEN 项逐项判定

### B24-T062-C07 · P2 → CLOSED

**复核落点**：作者取证 L37、L121、L146–148；`sources/registry.yaml` L6024；正文 L126 为相应参数校验入口定位。

第三轮唯一剩余关闭条件是：取证 L121 的建议登记 `notes` 副本须补齐 CP 算法调用范围与 Mcore 前提，或明确引用 L37 的完整条件，不能只在补充说明中声称已同步。

本轮 L121 的实际副本已经加入“进入条件与 L37 同：位于 ulysses/mamba/hybrid 各 CP 分支、要求 --use-mcore-models”。这同时完成了明确交叉引用和条件展开，与 L37、registry 的摘要一致，不再把该辅助头数检查写成 `_validate_cp_args` 全部算法的无条件规则。

E01 支持这一限定：L265–271 在 CP 未启用时返回；L276–277 检查 Mcore 前提；L279–282 的 Ulysses/Mamba 分支与 L301–314 的 hybrid 分支才调用 `_check_attention_head`。没有把相邻 `megatron_cp_algo` 分支泛化纳入该头数检查。修订副本还保留了 L247–257 对应的头数整除及正商、GQA 开启且组数至少为 1 的进入条件、先除 TP 再除 Ulysses 的两层正商，以及 kv-repeat 只绕过第二层的边界。

**判定依据**：本轮修复发生在第三轮明确要求的实际副本，而非仅 L148 的修订声明；原剩余关闭条件完成，故 **CLOSED**。这只核实摘要与已读校验分支一致，不证明任意 CP×TP×GQA 配置可运行，也不扩展未读取的 MindSpeed core 协议。

### S3-01 · 原号 B24-B24-T062-S3-01 · P2 → CLOSED

**复核落点**：正文 L75、L82；作者取证 L148。

L82 已删除“样板下无重编译预期，出现即异常”。现在分开记录编译区外 eager hook 的时间线与模型编译区的重编译，先要求核对 guard 原因，并列出形状、dtype、设备特化及动态形状发现的正常可能性；稳定输入和预热基线下的异常频度才作为检查项，而且明确“该基线属验证设计、未建立”。因此没有把观测到一次重编译直接当作训练或 hook 故障，也没有虚构已运行的零重编译基线。

E03 的 Guards 给出类型、设备、dtype、形状等检查；Recompilation 与 Dynamic Shapes 说明形状变化和动态形状发现可以导致重编译。E04 也明确同一 frame 可能产生多个编译结果，默认动态形状发现可在重编译时推进。以上机制不会因 optimizer 留在 eager 就自动消失。

**判定依据**：已按原关闭条件区分 eager hook 与模型编译 frame，并把异常判读改为基于原因和事先限定的稳定条件，故 **CLOSED**。本项只评估第三轮错误判据的修复，不重审此前已关闭的编译作用域问题，也不验证完整分布式编译支持。

### S3-02 · 原号 B24-B24-T062-S3-02 · P3 → CLOSED

**复核落点**：正文 L121；作者取证 L148。

正文已将错误限定名改为 `InPlaceCompilationTests.test_compilation`，仍对应 `ToyModel`、`model.compile(backend=CompileCounter)`、单次调用后 frame 数为 1 的断言。E02 原文件 L24–32 确认类名、方法、调用及断言一致。

同一行另列 `test_dynamo_signatures` L163–173，描述为公共/内部 API 签名一致性；E02 L149–173 确认该方法属于 `PublicTorchCompilerTests`，比较公共 API 与 `torch._dynamo` 的函数签名，并非前述原地编译计数测试。正文保留“不验证完整训练 step、编译数值或 optimizer/scheduler 路径”的限制，没有从一次 frame 计数推出长期零重编译。

**判定依据**：测试归属已纠正，两种断言的职责和不覆盖范围有明确区分，故 **CLOSED**；没有执行该测试。

### S3-03 · 原号 B24-B24-T062-S3-03 · P3 → CLOSED

**复核落点**：正文 L75；作者取证 L148。

含 optimizer 的训练可调用对象与 optimizer frame guard 失配的近邻引用，已改为 E03 的两个精确章节，而非 `generated/torch.compile.html` 的“相关示例”。两个锚点本次均实际存在：

- `#where-to-apply-torch-compile` 的本次原 HTML L903–906 讨论编译放置，L916–930 给出含 optimizer 的训练函数。
- `#wrapping-constants-with-tensors` 的 L1242–1274 给出 optimizer、scheduler 与学习率常量 guard 引发重编译的具体例子，能支持 L75 所指示例。

**判定依据**：近邻链接与所称训练示例逐项对应，原引用错位已消除，故 **CLOSED**。本项不把链接可达性当作示例在本地、目标 GPU/NPU 或任意训练栈上成功运行的证明。

## 4. 新发现与计数

在上述四项的修订落点及必要证据范围内，**未发现新增问题**；不为无问题项创建 `B24-T062-S4-xx` 占位编号。

| 计数范围 | CLOSED | OPEN | 说明 |
|---|---:|---:|---|
| 本轮复核的第三轮遗留项 | **4** | **0** | C07、S3-01 为原 P2；S3-02/S3-03 为原 P3 |
| 第三轮已经 CLOSED 的历史项 | 9 | 0 | 只继承第三轮状态，本轮不重查 |
| 本轮新增 S4 | 0 | 0 | 新发现 P1/P2/P3 均为 0 |
| 全部历史及本轮累计 | **13** | **0** | 累计是状态汇总，不表示本轮重新审阅全部历史项 |

## 5. 任务验收重新核对

以 T06-02 的实际五条 acceptance 为准。本轮仅重新判定受四项修订影响的第 1/5 条；第 2/3/4 条沿用第三轮结果并核对正文位置，**不重新取证或重查其已 CLOSED 问题**。

| 验收条目 | 对应位置及本轮处理 | 判定 |
|---|---|---|
| 1. eager/compiled step 路径、数据/控制流与观测；编译不等于数值正确 | 正文 L75–85。S3-01 修正重编译判据，S3-03 纠正具体示例引用；原数值正确性限制仍明确。 | **满足（文档/方法范围）** |
| 2. PyTorch、NVIDIA、Ascend 三组独立档案，记录模型/框架/依赖/硬件与未知 | 正文 L89–95。沿用第三轮“在所选资料范围内满足”，不重新验证三组依赖或硬件支持。 | **满足（沿用第三轮范围）** |
| 3. AMD 官方后端执行差异与限制，不直接迁移 | 正文 L97。沿用第三轮“在所选资料范围内满足”，本轮未重开 AMD/ROCm 资料或验证迁移。 | **满足（沿用第三轮范围）** |
| 4. 初始化、first step、backward/update、保存等故障分界与小规模验证方法 | 正文 L101–113。沿用第三轮“在验证方法设计范围内满足”，未执行这些方法。 | **满足（设计，不是实测）** |
| 5. 源码/测试到职责定位；调用不补写未读依赖协议 | 正文 L115–130，取证 L37/L121。C07 实际副本条件已同步，S3-02 测试类归属已修正；不把接口接触点扩展为内部协议或完整测试覆盖。 | **满足（所选代表性映射范围）** |

任务 objective 所需的职责图、平台对照及验证设计沿用既有验收范围。全部第三轮 OPEN 项已 CLOSED，且没有本轮新增 OPEN P1/P2，达到用户给定的通过条件。此结论不自动修改任务表中的 `planned`，也不把 `generic`、`source_checked` 或资料档案当作跨平台兼容与硬件验证。

## 6. 本地检查与只新增约束

1. 报告写入后，在工作树执行 `PYTHONDONTWRITEBYTECODE=1 make check`，退出码 0：**103 content entries / 493 sources**。该检查只验证结构和本地文件链接，不验证远程证据、技术正确性或硬件行为。
2. 为同时遵守仓库构建要求和“只新增一个文件”的限制，将 500 个既有文件及本报告复制到 `/private/tmp/b24-t062-s4.GPvX0z/build-snapshot`；包含工作树既有两份 build 清单，未复制 `.git` 或虚拟环境。在快照中使用仓库现有虚拟环境执行 `PYTHONDONTWRITEBYTECODE=1 make check build`（通过 `PYTHON` 指定解释器），两目标均成功，`make` 退出码 0，仍为 **103 content entries / 493 sources**。清单仅在临时快照中重建，没有写回工作树。
3. 对照写报告前记录的 500 个既有文件 SHA-256：**变化 0、删除 0；新增仅本报告**。该基线包含既有未提交修改、未跟踪文件和工作树 build 文件，本轮没有清理、覆盖或回滚它们。新增报告的 no-index diff 未输出空白错误；其退出码 1 表示存在新增文件差异，不是上述结构检查或构建失败。
4. 未修改 `src/kb/`，未运行 `make test`。没有运行 PyTorch/Megatron/MindSpeed 测试、编译示例、GPU/NPU 工作负载或正文中的验证设计。源码与网页读取、结构检查、隔离构建均不得记为训练实验或硬件验证。

## 7. 最终结论与限制

**通过。** 本轮四项遗留 OPEN 已全部 CLOSED；新增 OPEN P1/P2 为 0，新增 P3 也为 0。第三轮已 CLOSED 的九项只继承状态、不重查。

正文仍为 `draft / source_checked`；未核验的版本配套、MindSpeed core 内部协议、Megatron/MindSpeed 的完整 `torch.compile` 支持与端到端恢复仍不由本次复核补足。上游测试只是已读证据，没有被本轮执行。所有网络请求均只读；仅登记精确链接、摘要和原创归纳，没有镜像上游全文到仓库，也未改变第三方或仓库许可口径。

本结论只表示所限定问题和任务文档验收在本轮范围内闭环，**不代表真实 GPU/NPU、生产规模训练、数值正确性或恢复可靠性已经验证**。

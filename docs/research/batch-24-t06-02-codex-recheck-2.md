# Batch 24 · T06-02 Codex 定向复核第二轮报告

- 复核日期：2026-10-18（Asia/Shanghai）。
- 结论：**暂不通过**。
- 本轮指定复核的 C05–C08：**CLOSED 1 项、OPEN 3 项**；C05 关闭，C06/C07/C08 仍开放。
- 初审 C01–C09 累计：**CLOSED 6 项、OPEN 3 项**。第一轮复核另发现的 **B24-T062-R01（P2）仍 OPEN**；合并历史发现为 **CLOSED 6 项、OPEN 4 项**（OPEN：P1 0、P2 3、P3 1）。
- 本轮没有新增独立的 `B24-T062-S2-xx` 发现；未完成的原关闭条件沿用原编号，不重复计数。
- 执行边界：只审阅，只新增本报告；不修改正文、作者取证、registry、导航及任务计划，不执行上游测试、训练、编译或 GPU/NPU 操作。
- 执行者为本会话 Codex；没有派发子代理。实际后端模型、推理档位和路由元数据未在本会话提供可独立核验的记录，记为 `unknown`，不冒称已经验真为约定模型，也不虚构另一次 CLI 执行。

## 1. 范围、基线与判定方法

先读 `README.md`、`docs/authoring-guide.md`、`content-outline.md` 与 `schemas/content.schema.json`，再读取[初审报告](batch-24-t06-02-codex-review.md)、[第一轮复核](batch-24-t06-02-codex-recheck.md)及当前[修订正文](../../knowledge/06-training/framework-execution.md)。逐项核对[作者取证](batch-24-t06-02-sources.md)末尾“修订轮二补充”（L132–137）与实际落点，而不是把补充中的“已同步”当成修改完成的证据。

主要审阅范围是第一轮仍 OPEN 的 C05/C06/C07/C08。C01–C04/C09 仅检查本轮关联改动是否引起回归，不重做全量初审。R01 虽不在用户列出的四个 C 编号中，但它在第一轮明确为 OPEN，且直接阻断训练 step 验收第 1 条，因此另列复核，不能因本轮补充未提它而漏计。

本次位置均对应下列实际读取的文件快照；正文现为 141 行，初审/第一轮报告的旧行号不能直接沿用。例如原重点 L66/L119，当前对应正文 L67/L120。

| 输入 | SHA-256 |
|---|---|
| `knowledge/06-training/framework-execution.md` | `2335398a596eb00766c7b8041db2137e0a89fb426f966347ffbc9e5898862736` |
| `docs/research/batch-24-t06-02-sources.md` | `18c6777962918c297c32a89ce02d5a403e1e12476081aa66c3fbcde59298519b` |
| `docs/research/batch-24-t06-02-codex-recheck.md` | `a906ffe09f01cd101d7eb1bd9923dc57b1efef3375867f3fd129667838f94d43` |
| `sources/registry.yaml` | `656c2f814bb2b0a28bd60de2c3a113f133550ae0ddd12eb1c6e4305646354d15` |

同时重核 `plans/full-coverage-backlog.yaml` L5880–5927 的 objective、五条 acceptance 与 source_discovery。这里的“通过”仅指本任务的内容审阅范围；不会将源码可读、测试存在、结构校验通过或 `source_checked` 升级成真实环境验证。

## 2. 本轮独立重开证据

通过只读 HTTP 取回实际源码与版本化文档，读取函数、断言和上下文；没有 import 或执行这些上游文件。另以只读 `git ls-remote` 核定三个 tag 当前指向，并再次下载相应 commit 的八个源码文件，逐个确认与 tag 取回字节一致：

- PyTorch `v2.6.0` → `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340`。
- Megatron-LM `core_v0.19.2` → `4b4acac9a1d28ea6829c8d4f566d75698a21249d`。
- MindSpeed-LLM `v2.2.0` → `53f3639c3da9c000a187c44cc0c08d55026ddded`。

下表 E 编号仅为本报告证据索引，不是新 registry ID。源码链接使用本轮实际核定的 commit，L 坐标来自原始文件，不是网页阅读器的重排行号。

| 证据 | 精确上游位置 | 本轮核对用途 |
|---|---|---|
| E01 | PyTorch [test/test_optim.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/test_optim.py#L1349)：L1349–1439、L1646–1717、L1734–1758 | 确认作者所列四个具名测试真实存在；核对参数/optimizer 状态对照、CUDA 限定及 hook 断言。 |
| E02 | PyTorch [test/test_autograd.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/test_autograd.py#L902)：L902–942、L1608–1611、L2263–2280 | 区分解析梯度/高阶梯度、无梯度输入错误等断言；没有把这些测试称为完整训练恢复测试。 |
| E03 | PyTorch [test/dynamo/test_compile.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/test/dynamo/test_compile.py#L24)：L24–39、L55–67、L149–173 | 核对两个类及其具体测试；编译计数、保存加载路径和公共 API 签名检查各有不同覆盖范围。 |
| E04 | Megatron [test_schedules.py](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/tests/unit_tests/pipeline_parallel/test_schedules.py#L47) L47–76；[test_utilities.py](https://github.com/NVIDIA/Megatron-LM/blob/4b4acac9a1d28ea6829c8d4f566d75698a21249d/tests/unit_tests/test_utilities.py#L43) L43–82、L122–141 | 确认四组 TP/PP/VP 配置、函数身份断言，以及 CUDA 设备、NCCL 和真实进程组初始化。 |
| E05 | MindSpeed-LLM [arguments.py](https://github.com/Ascend/MindSpeed-LLM/blob/53f3639c3da9c000a187c44cc0c08d55026ddded/mindspeed_llm/training/arguments.py#L242) L242–282、L301–314 | 核对 GQA 进入条件、两次串联 `divmod`、每次商的下界、kv-repeat 开关，以及调用该头数检查的 CP 算法分支。 |
| E06 | PyTorch [torch/autograd/__init__.py](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/autograd/__init__.py#L294) L294–299、L339–350；[saved_variable.cpp](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/csrc/autograd/saved_variable.cpp#L110) L110–131、L280–285；[Autograd mechanics](https://docs.pytorch.org/docs/2.6/notes/autograd.html#saved-tensors) 的 Saved tensors/Graph retaining 小节 | 区分“某次反向保留后续需要的中间量”与“已释放后再调用选项”；保图不是每个新 forward 的常规要求。 |
| E07 | PyTorch 2.6 [Where to apply torch.compile](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#where-to-apply-torch-compile) 原 HTML L901–940；[Wrapping constants with tensors](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#wrapping-constants-with-tensors) L1242–1275 | 再确认训练可调用对象可包含 optimizer，scheduler/LR 状态可参与 guard 失配和重编译；用于 R01。 |

字节核对记录如下；前三项完整匹配作者新增 registry `revision`，MindSpeed 参数文件与 Megatron 测试文件也完整匹配既有作者记录。

| 文件 | 本轮 SHA-256 |
|---|---|
| E01 `test_optim.py` | `76cf0c7a0a79eb070bbd3fea508b083156dcbaefa68d38914e332c34a4177593` |
| E02 `test_autograd.py` | `a8daf1cb687dad29cc1633c222465a9faecdf2073e137195a32d6d795db033c1` |
| E03 `test_compile.py` | `36745171714b59a3ac313ac9b8a80e5423fd95f7abb538933e6731cdbd074d3d` |
| E04 `test_schedules.py` | `5854bac1a671281796bc1bf4329f1bcbf3331d327380132d9f66e4299bae660f` |
| E04 `test_utilities.py` | `db5281ae70ae9f6f0f3df043ae048fe6809fa090fce012809bf25c9249615fee` |
| E05 `arguments.py` | `fd64204269ad1749159d9b98f47c91f92cb17de5075cb92670f8ab1d5df42a38` |
| E06 `torch/autograd/__init__.py` | `98f86d295e386f647ad234ec63e36cb4b5d6acc3df696546c03bd62bf67a7503` |
| E06 `saved_variable.cpp` | `58c67f6b05a3ebe04dcf24318ed700401aeb7efbf7ba12589eb848603212eb84` |
| E07 Troubleshooting 原 HTML | `51cdeae20c3c5536b180c5c94469286639498a1a9773461c79ad539329fb8b43` |

访问限制如实记录：网页阅读工具未能打开部分 GitHub 源码页及 Troubleshooting；系统 Python 首次 HTTPS 请求还出现本机证书链错误。随后系统 `curl` 正常证书校验的只读请求均成功，未使用跳过证书校验参数；commit 文件也实际取回并比对。没有将阅读器失败或本机证书错误当成来源不存在的证据。

## 3. C05–C08 逐项判定

### B24-T062-C05 · 原 P2 → CLOSED

**复核位置**：正文 L109–113；作者补充 L134；关联[并行与状态页](../../knowledge/06-training/parallelism-and-state.md) L180–201。

本轮已补齐上一轮明确要求的设计契约：

1. 正文 L112 选定“完整 optimizer step 边界”，列出无飞行 micro-batch、无待提交梯度、scaler 已更新、scheduler/数据提交计数位于同一逻辑点，并具名引用关联页的截取边界和合法跳步两节。不再把“同一已保存状态”当成无需定义的前提。
2. 保存内容明确包含模型、optimizer、scheduler、scaler、各 RNG 的截点状态及随截点恢复的数据游标。恢复分支加载 generator 的保存状态，不是重新设置相同 seed；两分支从同一截点使用同一后继输入。这正面处理了 RNG 序列位置问题。
3. 连通性和恢复一致性继续分开，参考/恢复分支、同位更新比较、更新/跳步计数、参数组成员对照、事先写定的量/容差/步数及不确定时停止均保留。该设计没有要求所有真实场景采用同一个数值阈值。
4. L113 仍把 `core_v0.12.1` 示例限定为 TP=2、PP=1、合成数据、仅模型保存加载、加载后无后继训练步；没有拿它证明完整状态恢复已经执行。

**判定依据**：这是验证方法设计的补齐，不是实验结果。前轮剩余的截取边界及截点 RNG 恢复已落实，因此关闭 C05；仍不证明 mid-step、拓扑变化、跨框架迁移或目标硬件恢复成功。实际 generator/rank 映射及容差需在具体实验前填定，不能把本页设计直接当作可执行处方。

### B24-T062-C06 · 原 P2 / OPEN

**复核位置**：正文 L18、L119–128；作者补充 L135；registry L6122–6135 的 `src.pytorch.official-tests-v2.6.0`。

**接受的修订**：

- 新来源已登记并进入正文 `source_refs`。E01–E03 三个文件、完整 SHA-256、列出的 optimizer/autograd 测试名称和编译测试类均真实；本轮不再维持“尚未提供 PyTorch 官方测试文件”的旧判断。
- 正文 L123 的 Megatron 条目已准确列出 TP=2 下的四组 PP/VP 配置，并说明 CUDA＋NCCL 真实初始化、GPU/多进程前提及“只验证选择，不验证数值/通信完成/完整 step”。E04 支持这些说明，这一子问题关闭。不能因此推定邻近连通性设计中的单卡/2 卡就能运行整项调度测试。

**仍未完成的原关闭条件**：上一轮第 4.2 节要求写出代表性测试的“函数、断言和适用/未覆盖”，当前 PyTorch 三行主要仍是文件、名称/类名和职责标签。其关键断言及适用界限没有落入正文或补充取证。例如：

- E01 `test_state_dict_deterministic` L1403–1439 是克隆参数、加载 optimizer 状态后继续更新，对照参数值、状态及参数组；它不是完整应用 checkpoint/RNG 恢复的证明。`test_state_dict_with_cuda_params` L1646 有 `onlyCUDA` 限定，且 L1697–1717 检查加载未改写输入状态、step 状态设备及后续更新。正文未区分这项 CUDA 条件与通用 state_dict 语义。
- E02 `test_backward` L2270–2280 对照解析梯度；`test_backward_badcalls` L1608–1611 断言不需梯度的输入报错。只列函数名不说明它们各自验证什么，也不能将这些名字直接作为保图时序或恢复一致性的测试映射。
- E03 正文只列 `InPlaceCompilationTests`/`PublicTorchCompilerTests` 两个类。可以选 `test_compilation` L25–32 的 frame 计数或 `test_dynamo_signatures` L163–173 的公共/内部签名一致性作为具名断言，但后者并不验证完整训练 step、编译数值或 optimizer/scheduler 路径。

此外，正文 L128 仍写“本轮只在 NVIDIA 档案定位到调度选择测试”“PyTorch 官方测试……职责映射未完成”，与 L119–121 刚添加的 PyTorch 引用和作者 L135 的完成说明没有同步。这属于 C06 的同一映射/覆盖状态未闭环，不另起 S2 编号。

**关闭条件**：至少选择一组已经列出的 PyTorch 代表性测试，补出具名函数、具体断言、设备/参数化或后端条件、不能覆盖的本页结论，并同步 L128 的覆盖状态；L91 的“未逐项映射”可以继续描述尚未覆盖的测试面，不要求将部分映射夸大成全量覆盖。无需补齐整个 PyTorch 测试面，也不要求执行任何上游测试。仅增加更多文件名或将本报告的独立解读当成作者正文已经交付，均不足以关闭本项。

### B24-T062-C07 · 原 P2 / OPEN

**复核位置**：作者取证 L37/L121/L128/L136；registry L6024；正文 L126 关联的平台参数校验入口。

**接受的修订**：三处实际摘要（取证 L37、取证 L121、registry L6024）都已把 GQA 写成串联除法，即先对 TP 分组，再检查该商能否被 Ulysses 规模整除。不再保留“G 分别被 T、U 整除”的弱条件；上一轮 `G=4、T=2、U=4` 的算术反例所针对的问题已经修复。本轮不将该错误继续计为未修。

**剩余差距**：前轮明确要求保留适用分支及每次商为正，取证摘要副本和 registry 尚未完整同步。L37 已写两次商 ≥1，但 L121 与 registry L6024 仍只写整除及乘积，没有商的下界；三个摘要均没有完整保留源码 `group_query_attention and num_query_groups >= 1` 的进入条件。E05 中这个检查也不是所有 CP 算法的无条件规则：L282/L314 分别在相应 Ulysses/Mamba、hybrid 分支调用辅助函数。

为避免把“已改成乘积”误当成全部谓词相同，E05 L247–263 实际结构可用本报告的说明符号表示为：

- 设 `H=num_attention_heads`、`G=num_query_groups`、`T=tensor_model_parallel_size`、`U` 为调用方传给辅助检查的 Ulysses 规模。
- 进入该辅助检查时，要求 `H % (T*U) == 0` 且 `H/(T*U) >= 1`。
- 仅在 GQA 开启且 `G >= 1` 的分支，要求 `G % T == 0` 且 `G/T >= 1`。
- 该分支且 kv-repeat 未开启时，再要求 `(G/T) % U == 0` 且 `(G/T)/U >= 1`；在这些正整数前提下才归纳为 `G` 能被 `T*U` 整除。开启开关绕过的是第二层，不是第一层。

以上只归纳已读条件，不据此判断某个完整配置可运行，也不推断未读 CP 内部协议。不能脱离正整数/进入分支前提，把只含取模的摘要当作全部源码校验条件。

**关闭条件**：将取证 L37/L121 与 registry L6024 同步为含进入条件、两次正商和开关边界的摘要；可用对完整谓词的明确引用避免重复。作者 L136 的“同步”声明不能替代实际副本。此项保留原编号和原优先级，剩余问题不是串联除法算术仍然错误。

### B24-T062-C08 · 原 P3 / OPEN

**复核位置**：正文 L67/L120；作者取证 L34/L93/L137。

**接受的修订**：正文 L67 现在明确说明同图后续求导依赖中间量时，应在会释放这些中间量的较早 backward 中保留；已释放后再加选项不能追溯恢复，普通新 forward 不由此要求每步保图。这与 E06 一致。作者取证 L93 的建议登记摘要也已补了时序与新 forward 边界，不能忽略这部分实际修订。

**未闭环位置**：

- 取证主张—来源表 L34 仍原样写“backward 二次调用需 retain_graph=True；线程安全边界”，没有同图、中间量依赖及先前调用中保留的限定。L137 虽称“取证摘要同步”，但没有修改这条被上一轮点名的主张摘要。
- 正文 L120 仍以“对同一张图二次 backward 才需 `retain_graph=True`”作为观测挂点，没有纳入所需中间量条件和保留时机。该简写不再直接声称能复活已释放中间量，但也没有完成上一轮要求 L66/L119 与取证 L34 同步的关闭条件，且容易与 L67 的精确定义脱节。

E06 的 saved-variable 路径针对后续实际需要而已经不可用的数据报错；不能无条件推出所有同图二次反向都要保图。这里不新增或声称执行任何最小复现。

**关闭条件**：把取证 L34 与正文 L120 改为与 L67 一致的条件/时序，或在表格明确指向 L67 的完整定义。保留常规新 forward 不要求保图的限定；不把是否关闭图释放错误误写成数值正确性或训练恢复证明。剩余问题仍属于原 C08，不重复编号。

## 4. 第一轮新增 R01 与已 CLOSED 项回归抽查

### B24-T062-R01 · 原 P2 / OPEN

正文当前 L75 仍只说“被包装的可调用对象”，没有为表格选定“仅 `compile(model)`”的具体模式；L83 仍保留“通常编译区外；这些状态的推进与编译无关”。本轮作者补充没有处理这项第一轮新发现。

E07 再次确认官方明确列出含 optimizer 的训练可调用对象，且 scheduler/LR 示例展示 optimizer frame 的 guard 失配与重编译。因此不能用这张未选定放置方式的通用表排除 optimizer/scheduler 状态对编译观测的影响。本轮没有发现足以关闭 R01 的修订，也没有因 C05 的恢复改进而替它关闭。

**关闭条件沿用第一轮**：为表格明确选择仅编译模型的样板并标出外层驱动，或并列不同编译范围；区分逻辑更新/跳步契约与编译覆盖、guard 和重编译。保留 DDP/FSDP 实际包装条件，不反向承诺完整 step 可一图编译。

### 已 CLOSED 项抽查

| 项目 | 关联位置及本次抽查范围 | 判定 |
|---|---|---|
| C01 / P2 | 正文 L92 仍为 dataclass 继承字段经参数工厂生成 CLI，保留“CLI 实际解析未运行”；本轮恢复/测试修改没有恢复“无 CLI”的否定结论。未重新执行解析。 | **维持 CLOSED** |
| C02 / P2 | L75–85 的五阶段 eager/compiled 对照、观测及“编译不等于数值正确”仍在。结构性缺失未回归；通用边界错误继续由 R01 单列，避免重复计数。 | **维持 CLOSED** |
| C03 / P2 | L89–95 三组独立资料档案及各自模型/框架/依赖/硬件未知仍保留；新增 PyTorch 测试未被拼成 MindSpeed 2.7.1 或 Megatron 的配套证明。测试映射残缺归 C06。 | **维持 CLOSED** |
| C04 / P2 | L97 保留正确的 PyTorch 2.6 distributed URL、HIP 差异和 AMD 7.1.1 独立版本线；未加入可直接迁移 Megatron/MindSpeed 的结论。本轮不对未改部分重新全量联网审计。 | **维持 CLOSED** |
| C09 / P3 | L134 仍为 optimizer state_dict“不能默认互换”、兼容性未验证，而非所有实现绝对不兼容。新增同版 PyTorch state_dict 测试未被外推成跨框架互转。 | **维持 CLOSED** |

## 5. 新发现与计数

本轮未确认新的独立 P1/P2/P3 问题，故未生成 `B24-T062-S2-01` 等空置或重复条目。C06 的断言/条件缺失及覆盖状态冲突、C07 的摘要副本边界缺失、C08 的未同步摘要均属于此前已规定的关闭条件，继续沿用原 ID。R01 也是第一轮遗留项，不伪装成本轮新发现。

| 计数范围 | CLOSED | OPEN | OPEN 组成 |
|---|---:|---:|---|
| 本轮指定 C05–C08 | 1 | 3 | C06、C07：P2；C08：P3 |
| 初审 C01–C09 累计 | 6 | 3 | 同上 |
| 第一轮新增 R01 | 0 | 1 | P2 |
| 本轮新增 S2 | 0 | 0 | 无 |
| 合并全部历史发现 | **6** | **4** | **P1 0、P2 3、P3 1** |

## 6. 任务验收重核

| T06-02 验收条目 | 当前核对结果 | 判定 |
|---|---|---|
| 1. eager/compiled step 路径、数据/控制流与观测；编译不等于数值正确 | 原结构性 C02 保持关闭，但 L83 的通用 optimizer/scheduler 边界仍与 E07 不符，R01 未改。 | **暂不通过** |
| 2. PyTorch、NVIDIA、Ascend 三组独立资料档案及模型/框架/依赖/硬件边界、未知 | 各组范围与版本隔离仍在，新增测试没有被用来推断可运行配套。 | **在所选资料范围内满足** |
| 3. AMD 所选官方后端差异/限制，不直接迁移 | C04 抽查未见关联回归；保留 PyTorch 2.6 与 AMD 7.1.1 两条独立版本线。 | **在所选资料范围内满足** |
| 4. 初始化、first step、backward/update、保存等故障分界及小规模验证方法 | 连通性/恢复分离，完整 step 截取与 RNG 截点状态已补；保留设计未执行及示例限制，C05 关闭。 | **在验证方法设计范围内满足** |
| 5. 源码/测试到职责定位；不补写未读依赖协议 | 新 PyTorch 登记和 Megatron 环境补证有效；PyTorch 断言/适用与覆盖状态尚未交付一致映射，C06 仍开放；C07/C08 的关联证据摘要也未全部闭环。 | **部分满足，暂不通过** |

Objective 所需组件链与平台对照已经具备，但不能替代未完成的第 1/5 条。任务仍保留 draft/source_checked 与未验证条件，不修改计划状态，不宣称本次完成真实硬件验收。

## 7. 元数据、来源与写入边界

- 正文稳定 ID `training.framework-execution`、reference/training 主归属、`status: draft`、`platforms: [generic]`、日期及关联 ID 未见本轮回归。`generic` 没有被升级成 GPU/NPU/ROCm 兼容证明。
- 本页现有 17 个 `source_refs`；新增官方测试条目的三个文件哈希已独立匹配。来源登记存在与摘要准确是两类判断，因此登记检查不抵消 C06/C07/C08。
- 未读取的 MindSpeed core 内部协议、三组真实配套、完整训练 step 编译支持及跨框架 checkpoint 迁移继续为未知，不从接口名或测试名补推。
- 所有联网行为只读；下载文件和核对产物放在仓库外临时目录，不把外部源码包、日志、凭证或运行环境状态加入仓库。报告只给原创归纳及精确链接，不改许可声明。
- 工作树原先已有其他修改与未跟踪稿件；本轮不整理、不回滚、不覆盖它们。结构构建使用独立快照，避免改写工作树已有 `build/`。

## 8. 本地检查与最终结论

1. 工作树只读执行 `PYTHONDONTWRITEBYTECODE=1 make check`，退出码 0：**103 content entries / 493 sources**。它只检查结构和本地文件链接，不检查技术正确性或远程链接。
2. 在 `/private/tmp/b24-t062-s2.sNZPcG/build-snapshot` 建立独立仓库快照，带入既有 build 基线并使用仓库现有虚拟环境，执行 `make check build`，退出码 0；仍为 **103 content entries / 493 sources**，生成的 `build/catalog.json`、`build/catalog.md` 只写入快照。
3. 对照审阅开始时保存的 493 个既有仓库文件的 SHA-256：既有文件变化 0、删除 0，新增文件仅本报告；原有未提交修改与未跟踪文件保留原状。报告补记检查结果后再次执行结构及边界核对。
4. 未改动 `src/kb/`，没有运行 `make test`；没有执行或声称通过任何 PyTorch/Megatron/MindSpeed 上游测试，也没有执行本文验证设计。以上结构检查不作为技术正确性或硬件验证证据。

**最终结论：暂不通过。** 本轮 C05 关闭；C06/C07/C08 尚未完成原关闭条件，第一轮 R01 也仍为 OPEN。合并历史发现 CLOSED 6、OPEN 4；本轮新发现 0。未达到“全部遗留 OPEN 项 CLOSED 且无新 OPEN P1/P2”的通过条件。

后续应只处理 C06 的测试断言/适用与覆盖状态同步、C07 的分支/正商摘要同步、C08 的条件/时序摘要同步，以及 R01 的编译作用域，再逐项定向复核。以上即使以后全部关闭，也仅构成文档审阅范围内通过，不代表上游测试已执行或真实 GPU/NPU 恢复、数值与生产规模可靠性已验证。

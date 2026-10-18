# Batch 24 · T06-02 Codex 定向复核报告

- 复核日期：2026-10-18（Asia/Shanghai）。
- 结论：**暂不通过**。
- 初审发现：**CLOSED 5 项、OPEN 4 项**；仍开放 C05、C06、C07（P2）及 C08（P3）。
- 新发现：**B24-T062-R01，P2 / OPEN**。合计 OPEN 5 项：P1 0、P2 4、P3 1。
- 执行边界：本会话只做技术审阅，只新增本报告；未修改正文、作者取证、registry、导航或任务计划，未派发子代理，未执行上游训练、测试、编译或 GPU/NPU 操作。
- 模型记录：沿用初审的如实记录原则。本会话未获得可独立核验的后端实际模型、推理档位和路由元数据，记为 `unknown`；不虚构另一次 CLI 调用或指定模型路由已验真。

## 1. 范围、输入与判定原则

先读 `README.md`、`docs/authoring-guide.md`、`content-outline.md` 与元数据 schema，再逐项重读[初审发现表](batch-24-t06-02-codex-review.md) L112–126 的编号、原位置和关闭条件。随后通读[修订正文](../../knowledge/06-training/framework-execution.md) L1–139、[作者取证](batch-24-t06-02-sources.md) L1–130，特别核对末尾 L124–130 的补证，而非仅接受作者的“已更正”说明。

重新核对 `plans/full-coverage-backlog.yaml` L5880–5929 的 T06-02 objective、五条 acceptance、source_discovery、依赖与目标；对照 registry 中本页来源、AMD 独立版本线及关联章节。结论仅覆盖本任务本次文件快照，不替其他 Batch 24 任务验收，不把资料档案当成已验证运行环境。

| 输入 | 本次 SHA-256 |
|---|---|
| `knowledge/06-training/framework-execution.md` | `436584fe1cf8e571e511865cc793b6d01aa3718c4e613bdaab89059fad54228f` |
| `docs/research/batch-24-t06-02-sources.md` | `93f75ec6b95ffb97fc60e1caf7e96ad6d1dbbd40d5f39e8466406cf9c74128d3` |
| `docs/research/batch-24-t06-02-codex-review.md` | `4677091969ea51de4dfd442f810bd4db69df888ad9a4514043d37a458bae4017` |
| `sources/registry.yaml` | `cfb95b9746f8405bf2c9f8d0101090fb9086a5a663c31d1d261693d3d700e59a` |

“CLOSED”表示原发现对应的修订条件已满足，不表示同一节的新断言自动正确。C02 原先缺少路径对照、编译区说明和编译观测的结构性问题已补齐；新表格中的新增泛化断言另列 R01，仍阻断验收第 1 条，避免把同一新问题重复记作两个 OPEN。

## 2. 独立重开上游证据

以下 E 编号为本报告内部证据索引，不是新增 registry ID。源码均重新读取固定 tag 的实际文件；文档均使用明确版本路径。只读请求未执行其中代码。表内 L 坐标取自直接下载文件的原始行号，不使用网页阅读器重排行号，也不把 tag 说成已核定的不可变 commit。

| 证据 | 实际重开对象与精确位置 | 结果与用途 |
|---|---|---|
| E01 | Megatron `core_v0.19.2`：[arguments.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/arguments.py) L2195–2291；[argument_utils.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/argument_utils.py) L95–107、L214–229；[model_parallel_config.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/model_parallel_config.py) L45–56；[transformer_config.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/transformer/transformer_config.py) L32、L53–58 | 四文件直接下载均 HTTP 200。核对继承字段、排除规则和参数注册链，没有运行 CLI。 |
| E02 | PyTorch 2.6：[torch.compiler](https://docs.pytorch.org/docs/2.6/torch.compiler.html) 原 HTML L589–600；[torch.compile](https://docs.pytorch.org/docs/2.6/generated/torch.compile.html) L590–607；[Troubleshooting](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html) L683–688、L738–771、L869–876、L902–940、L1242–1272 | 直接下载均 HTTP 200。分别核对 AOT 反向、可调用对象与缓存/guard、graph break、日志、编译放置位置及 optimizer/scheduler 的编译示例。R01 的关键证据是后两组位置。 |
| E03 | PyTorch 2.6：[Autograd mechanics](https://docs.pytorch.org/docs/2.6/notes/autograd.html) 原 HTML L585–605、L901–910；补读同版源码 [torch/autograd/__init__.py](https://raw.githubusercontent.com/pytorch/pytorch/v2.6.0/torch/autograd/__init__.py) L242–297、L339–354；[saved_variable.cpp](https://raw.githubusercontent.com/pytorch/pytorch/v2.6.0/torch/csrc/autograd/saved_variable.cpp) L110–113、L125–131、L280–285 | 三者直接下载均 HTTP 200。图随迭代重建；需要复用的 saved tensors 应在会释放它们的反向执行中保留，而不是已释放后再靠一次选项恢复。该结论来自源码分支，不是本地测试。 |
| E04 | Megatron `core_v0.19.2`：[test_schedules.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/tests/unit_tests/pipeline_parallel/test_schedules.py) L47–76；[test_utilities.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/tests/unit_tests/test_utilities.py) L43–82、L122–141；[schedules.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/pipeline_parallel/schedules.py) L149–163 | 三文件均 HTTP 200。读取选择断言及实际初始化，不把它称为纯 mock 测试，也不将选择断言扩展为调度数值/通信正确性证明。 |
| E05 | MindSpeed-LLM `v2.2.0`：[arguments.py](https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/mindspeed_llm/training/arguments.py) L242–282，重点 L247–263 | HTTP 200。逐个读取 `divmod`、商的下界和 `kv_head_repeat_before_uly_alltoall` 分支；核对 C07 的全部摘要副本。 |
| E06 | MindSpeed-LLM `v2.2.0`：[training.py](https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/mindspeed_llm/training/training.py) L377–415；[README.md](https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/README.md) L57–97；[install_guide.md](https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/docs/pytorch/install_guide.md) L56–74 | 三文件均 HTTP 200。支持入口职责、PyTorch 2.7.1/Python 3.10/在研组件，以及 MindSpeed core 与 Megatron `core_v0.12.1` 的独立配套线；不证明 MindSpeed core 内部实现。 |
| E07 | PyTorch 2.6：[HIP notes](https://docs.pytorch.org/docs/2.6/notes/hip.html#hip-interfaces-reuse-the-cuda-interfaces) 的接口复用、Checking for HIP、TF32、torch.distributed backends 小节，原 HTML L586 起、L641–642、L683–685；[distributed](https://docs.pytorch.org/docs/2.6/distributed.html) 的 Backends；AMD [docs-7.1.1 兼容页](https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html) 原 HTML L863、L878、L888、L933 起 | 三页直接下载均 HTTP 200。HIP 文档仍写该版 TF32 不支持、分布式后端为 nccl/gloo；AMD 页面含多个版本分节，不是 PyTorch 2.6 配套证明。 |
| E08 | Megatron `core_v0.12.1`：[run_simple_mcore_train_loop.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.12.1/examples/run_simple_mcore_train_loop.py) L24–34、L39–52、L73–77、L107–157 | HTTP 200。MockGPTDataset、TP=2/PP=1、只保存/加载模型及加载后没有再训练一步均可直接确认。 |
| E09 | Megatron `core_v0.19.2`：[training.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/training.py) L2407–2420、L2471–2474、L2517–2531；[distrib_optimizer.py](https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/optimizer/distrib_optimizer.py) L113–124、L825–885；PyTorch `v2.6.0` [optimizer.py](https://raw.githubusercontent.com/pytorch/pytorch/v2.6.0/torch/optim/optimizer.py) 的 `state_dict`/`load_state_dict`；[optim 文档](https://docs.pytorch.org/docs/2.6/optim.html) 原 HTML L585–632 | 四者均 HTTP 200。核对更新成功分支、scheduler 推进、具体优化器状态接口；不推导三个框架的所有格式绝对兼容或绝对不兼容。 |

### 2.1 补证字节一致性

| 本次重新下载对象 | SHA-256 | 与作者/初审记录的关系 |
|---|---|---|
| `argument_utils.py`，core_v0.19.2 | `4abf3e5e5571c5aa025dd8f716f483c6984fa7dbcf89931574d79fed728dc130` | 与作者补证 L126 全值一致 |
| `test_schedules.py`，core_v0.19.2 | `5854bac1a671281796bc1bf4329f1bcbf3331d327380132d9f66e4299bae660f` | 与作者补证 L127 全值一致 |
| MindSpeed-LLM `arguments.py`，v2.2.0 | `fd64204269ad1749159d9b98f47c91f92cb17de5075cb92670f8ab1d5df42a38` | 与作者记录及 registry 全值一致 |
| Megatron 最小训练示例，core_v0.12.1 | `5ed11bc7834177718e836da7e61e2b067256528b55821c0b8397b82e75773064` | 与初审/既有登记全值一致 |
| PyTorch `torch/autograd/__init__.py`，v2.6.0 | `98f86d295e386f647ad234ec63e36cb4b5d6acc3df696546c03bd62bf67a7503` | 本次为 C08 时序补读 |
| PyTorch `saved_variable.cpp`，v2.6.0 | `58c67f6b05a3ebe04dcf24318ed700401aeb7efbf7ba12589eb848603212eb84` | 本次为 C08 时序补读 |
| Megatron `test_utilities.py`，core_v0.19.2 | `db5281ae70ae9f6f0f3df043ae048fe6809fa090fce012809bf25c9249615fee` | 本次为 C06 环境前提补读 |

另对 training.py、schedules.py、distrib_optimizer.py、MindSpeed training/README/install_guide 全文件重新计算哈希，均与作者/初审所列值一致。Autograd/optim 两个 HTML 本次分别为 `a3ffc893eb6cf26ff15591aa66ef894265a22d20b4099ec5e0a05088a034ddbd`、`37a35ae6b2dc2e4299c106a653636f74047feda891b09076c56b9f62b8e5eafb`，与作者历史值不同。没有作者历史原始字节，不能判定差异成因；本次按重开页面的相关段落独立核对，不覆盖历史记录，不因整页哈希不同就认定机制变更。

### 2.2 无法重开与替代取证

- 网页阅读器对 compile API、Troubleshooting、若干 raw 文件返回 Internal Error/Cache miss；随后直接只读下载成功，已按实际 HTTP 200 和字节取证，不能把阅读器错误当成页面不存在。
- AMD 兼容页在网页阅读器返回 HTTP 429，但直接下载为 HTTP 200，并实际读取上述分节；不把限流当作不支持某版本的证据。
- 额外尝试 PyTorch 2.6 `generated/torch.autograd.backward.html`，网页阅读器不可用、直接请求 HTTP 403，**该 API 网页未能独立重开**。C08 转用同版 `torch/autograd/__init__.py` 中的 API 定义和 saved-variable 实现，不凭记忆补网页内容。
- MindSpeed core 本体、Megatron/MindSpeed 的完整 torch.compile 支持、未读的 CUDA graph/rerun 内部路径，仍为 `unknown`。不以本轮读取接口替代这些能力取证。

## 3. 初审发现逐项判定

下表保留初审优先级；原始位置以初审报告为准，修订后位置均指第 1 节记录哈希的文件。

| 编号 / 原优先级 | 原关闭条件摘要 | 修订后位置与独立依据 | 判定 |
|---|---|---|---|
| B24-T062-C01 / P2 | 删除“无 CLI”否定结论，补配置继承到参数工厂的固定版本链；不虚构解析结果 | 正文 L91、作者取证 L126 已改为字段生成 CLI，保留“解析未运行”。E01 确认 `TransformerConfig` 继承含 TP 的配置，工厂按排除规则遍历字段、转换名字并注册；不是仅搜索字面量。既有同 tag registry 条目位于 L4697 起、L5972 起，未被用来宣称运行成功。 | **CLOSED** |
| B24-T062-C02 / P2 | 补 eager/compiled step 数据、控制、梯度及观测对照；声明编译作用域、分段/回退；移除无依据数值自检保证 | 正文 L74–84 新增五阶段对照、被包装对象边界、guard/重编译/graph break 观测，保留数值对照与未执行限定；E02 支持这些组件和观测入口。原先“只有职责树和各一句话”的缺失已消除。新增“状态推进与编译无关”等断言另按 R01 审理，**本项关闭不表示新表整体技术验收通过**。 | **CLOSED** |
| B24-T062-C03 / P2 | 三组分别补模型/程序、框架、依赖、硬件边界与未知，不发明可运行配套 | 正文 L88–94 已按字段列三组；PyTorch 为未绑定模型的张量样板，Megatron 为所引用实现且未绑定配置，MindSpeed 为入口/校验范围。硬件代际/型号、版本配套和未读实现被保留为未知，E01/E06 与独立版本说明相符。这里接受的是资料档案字段补齐，不是完整硬件/依赖支持矩阵已核验。 | **CLOSED** |
| B24-T062-C04 / P2 | 修正不可达后端链接，采用明确 ROCm 执行差异和限制；AMD 另一版本线单列，不外推迁移 | 正文 L90、L96 已改用 registry L3575 起实际登记的 `distributed.html`；HIP 接口命名复用及对应限制小节可由 E07 核对。registry L3547 起与 L3461 起分别对应 HIP 2.6、AMD 7.1.1，正文明确后者不拼入 2.6，也未声称 Megatron/MindSpeed 可迁移。 | **CLOSED** |
| B24-T062-C05 / P2 | 区分连通性与恢复；定义保存边界、未中断/恢复分支、同一后继状态/输入、随机控制、比较规则与更新/跳步观测；准确限制示例 | 正文 L108–112 已分开检查，写同状态/同后继输入、预定容差与停止，并正确限制 E08 为 TP=2、PP=1 的合成数据/模型级示例。但 L111 仍未定义本设计的截取时刻及所需完整状态，固定 seed 也没有说明怎样对应保存点的 RNG 状态。详见第 4.1 节。 | **OPEN** |
| B24-T062-C06 / P2 | 固定版本代表性测试的职责/实现/断言/环境/未覆盖映射；满足 PyTorch 必要测试取证，不套用跨平台测试 | 正文 L114–126、作者补证 L127 的 Megatron 文件和哈希均获 E04 确认；但 PyTorch 行仍明确“未逐项映射”，任务所要求的 PyTorch 必要测试没有补入，且所选 Megatron 测试的 TP/进程组/设备前提未交付。详见第 4.2 节。 | **OPEN** |
| B24-T062-C07 / P2 | 所有取证/登记摘要改为无歧义的取模条件，保留商为正、开关及校验适用范围 | 作者取证 L37、L121、L128 与 registry L6024 虽修正头数/组数的“被整除”方向，仍把关闭 kv-repeat 时的商再除 U，写成原始 G 分别能被 T、U 整除。E05 明确检查的是 `G/T` 再除 U，并要求各商至少 1；不是该弱条件。详见第 4.3 节。 | **OPEN** |
| B24-T062-C08 / P3 | 同步正文和取证摘要，将保图要求限定到同图复用及所需中间量，不作为常规每步要求 | 正文 L66、L119 已补同图/新 forward 区分，主要误读有所收紧；但作者取证 L34 仍保留未限定的二次 backward 摘要。正文 L66 的“已释放中间量的图再次 backward 才需要”还未说明在释放前保留的时序。E03 确认该选项不能复活已释放中间量。详见第 4.4 节。 | **OPEN** |
| B24-T062-C09 / P3 | 收回三组所有 optimizer 格式绝对不兼容的结论，改为不默认互换、兼容性未验证 | 正文 L132 已按条件收紧，且明确不反向断言存在互转能力。E09 仅支持所读具体优化器接口/格式，修订没有超出这条证据边界。 | **CLOSED** |

## 4. 仍开放初审项：剩余差距与关闭要求

### 4.1 C05：恢复设计尚未定义状态截取契约

已接受的修订包括：连通性与恢复分开、同一后继输入/预定比较规则/不确定时停止、更新与合法跳步分开，以及 E08 示例的全部范围限制；这些不再重复要求作者证明。

剩余问题在于正文 L111 的“同一已保存状态”没有说明保存发生于哪一个训练逻辑边界。尤其未确定是否无飞行 micro-batch、是否完成 scaler/scheduler/data commit，也未列出为当前恢复目标实际保存并恢复的 optimizer、scheduler、scaler、RNG 和数据进度。L112 正确认定上游示例只保存模型，因而它不能补足这个空白。

这不是要求本页执行实验或提供某一模型的通用容差。现有[并行页](../../knowledge/06-training/parallelism-and-state.md) L178–199 已区分完整 step、mid-step、成功更新与样本推进；[checkpoint 一致性页](../../knowledge/06-training/checkpoint-state-consistency.md) L121–142 已要求固定截取/比较边界并比较逻辑进度、状态与同输入更新。本页虽链接这些主题，却没有选定本次验证设计采用哪个契约。E09 的更新成功分支也表明不能仅由 loss 或“首个成功更新”推定所有计数一致。

**关闭要求**：选定一个设计边界（可以只选完整 optimizer step 边界），显式引用相关章节的精确小节并列出本设计采用的状态/推进条件；说明未中断分支继续运行、恢复分支加载同一截点，如何恢复该截点随机状态而非只写相同 seed；把同位尝试步/成功更新/输入身份、合法跳步及参数更新证据对应起来。保留预定比较规则、停止条件与未执行声明，无须新增未经取证的命令。

### 4.2 C06：测试补证真实，但尚未覆盖原关闭条件

E04 与作者补充的文件哈希全值相同。实际断言配置为 TP=2 下 PP=1、PP=4 无 VP、PP=4/VP=2、PP=2/VP=4。它验证调度函数选择，不验证一次 forward/backward 的数值、通信完成或完整训练 step。

正文 L121 的“三类选择”概括可以用作入口，但不能将 `vp≥2` 单独当成所有配置的选择定理；同文件实现的基本分支还有 `pp_size>1` 等前提。更重要的是，该测试通过 `Utils.initialize_model_parallel` 进入真实 distributed 初始化：E04 的 utilities L62 使用 CUDA 设备，L78–79 初始化 NCCL 进程组，并非无需设备/进程配置的纯函数测试。正文未交付这些环境条件，不能由相邻的“单卡或 2 卡”验证设计推定这个测试可直接运行。

任务 source_discovery 明确要求 PyTorch 官方执行文档及必要测试；正文 L118–119/L126 仅把 PyTorch 映射未完成记作缺口，未实际补齐。诚实标缺口是正确的，但不等于该项验收完成。MindSpeed 测试继续保持未读即可，不需要为了凑齐表格套用 NVIDIA 测试。

**关闭要求**：补至少一组与本页 PyTorch autograd/optimizer/compile 职责直接相关的固定版本官方代表性测试，写出函数、断言和适用/未覆盖；给现有 Megatron 条目补准确配置及 CUDA/NCCL/进程组条件，不把函数选择测试等同于数值或恢复测试。只读测试源码即可，不要求本轮启动上游测试。

### 4.3 C07：整除方向修正后，组合条件仍被弱化

将 `G=num_query_groups`、`T=tensor_model_parallel_size`、`U=ulysses_size` 作为本段说明符号。在 E05 的 GQA 且 `G>=1` 分支：

1. L251–253 要求 `divmod(G, T)` 的余数为 0，商至少 1。
2. 若未启用 `kv_head_repeat_before_uly_alltoall`，L255–263 再要求 `divmod(G/T, U)` 的余数为 0，商至少 1。

因此在该分支及正规模条件下，第二条对应 **G 能被 T×U 整除且商至少 1**，不是“G 分别能被 T 和 U 整除”。纯整数反例：G=4、T=2、U=4 满足作者两个单独整除表述，却使第二次除法得到余数 2。这里只按源码表达式作算术核对，**没有声称运行此配置，也没有判定其他校验会不会更早拒绝它**。

头数约束的方向及首个商的下界在取证 L37 已修正，予以接受；但 GQA 商的下界、串联除法和摘要副本仍不完整。取证 L121 与 registry L6024 连头数商的下界也未保留。L128“已统一”的声明不能替代这些实际内容。

**关闭要求**：同时修正取证 L37/L121 和 registry L6024，保留适用分支、每次商为正及正确乘积条件；明确这是已读校验而非完整配置支持证明。修订后对 E05 同一 ref 的原始表达式再定向核对，不扩写未读 CP 算法协议。

### 4.4 C08：同图限定有所改善，摘要同步与保留时序未完成

正文 L66 已明确图随迭代重建、常规新的 forward 不要求每步保图，这部分予以接受。但作者取证 L34 仍写二次 backward 需要该选项，未保留同图和 saved-tensor 条件，与原关闭要求的“同步收紧取证摘要”不符。

正文“对同一张已释放中间量的图再次 backward 才需要”还可能被理解为：第一次已释放，再在第二次调用加选项即可修复。E03 的 API 定义说明 `retain_graph=False` 会释放用于求导的图；saved-variable 实现会清除数据，并在之后需要这些数据而已不可用时出错。由这些实现可知，应在需要保留该图供后续反向使用的较早调用中保留；已经释放时需要重新 forward/重建相应图，不能追溯恢复。

**关闭要求**：正文 L66/L119 与取证 L34 一起改成条件和时序完整的描述：同图再次求导且依赖需保留的中间量时，在会释放它们的先前反向中保留；普通重新 forward 的下一轮不由此要求保图。不要无条件断言所有同图二次反向都必须保图，也不新增本地执行结果。

## 5. 新发现

### B24-T062-R01 · P2 / OPEN：新增表格把编译放置选择写成 optimizer/scheduler 的通用边界

- **位置**：修订正文 L74–82，重点 L82 的“通常编译区外；这些状态的推进与编译无关”。这是本次新增 eager/compiled 表格的技术断言，不是原来缺少表格本身，故单独编号；C02 的原结构性缺失不重复计为 OPEN。
- **问题**：表格仅声明“被包装的可调用对象”，没有先选定只包装 model 的具体模式，却把 optimizer/scaler/scheduler 归为通常编译区外，并用无条件措辞切断状态推进与编译观测的联系。如此无法指导读者判断自己编译的是模型还是含 optimizer 的 train step，也可能漏看学习率状态变化导致的 guard/recompile。
- **精确证据**：E02 同一 PyTorch 2.6 Troubleshooting 的 [Where to apply torch.compile](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#where-to-apply-torch-compile)（原 HTML L902–940）明确并列包含 optimizer 的 step、顶层/子模块等放置方式，并给出含 `zero_grad`、forward、loss、backward、`opt.step()` 的包装函数。该页 [Wrapping Constants with Tensors](https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html#wrapping-constants-with-tensors)（L1242–1272）的示例还在包装函数内调用 scheduler，展示 LR 变化触发优化器帧 guard 失配和缓存上限。没有为每个调用另加一次包装；外围函数作用域本身就影响追踪边界。
- **影响**：本页核心目的是解释训练 step 和 compiled 专属观测点。把特定编译放置方式泛化，可能将 optimizer/scheduler 相关重编译排除在训练故障定位之外，属于验收第 1 条的技术问题，不是文字风格偏好。这里不声称所有 Python 调用都进入同一完整图；E02 的 graph break/guard 限制仍须随行。
- **关闭条件**：选定“仅 compile(model)”为表格样板，明确其外层驱动另行执行 optimizer/scaler/scheduler；或并列“编译模型”与“编译含 optimizer 的 step”两种范围。把“推进与编译无关”收紧为逻辑更新/跳步契约由训练驱动规定，但编译覆盖、guard 和重编译可能受相关状态影响。保留 DDP/FSDP 的实际包装条件与数值对照，不反向承诺任意完整训练 step 可一图编译。

除 R01 外，本次未确认需要另起编号的新 P1/P2/P3；C05–C08 的未闭环部分沿用原编号，没有重命名成新发现。未读平台内部实现继续列未知，不凭名称补协议。

## 6. 任务验收重核

| 验收条目 | 本次重核结果 | 判定 |
|---|---|---|
| 1. eager/compiled step、数据/控制流、观测；编译不等同数值正确 | 新对照、作用域提示、编译观测和数值不保证均已补，C02 原结构性问题关闭；但 L82 新的通用边界断言与所引官方 step/scheduler 示例不符，R01 仍开放。 | **暂不通过** |
| 2. PyTorch、NVIDIA、Ascend 三组独立资料档案及逐字段边界/未知 | L88–94 已补字段；PyTorch 2.6、Megatron core_v0.19.2、MindSpeed-LLM v2.2.0 的依赖线分离。未指定的模型、硬件/运行配套保持未知，不冒充可运行环境。C01/C03 关闭。 | **在资料对照范围内满足** |
| 3. AMD 官方后端差异/限制，不直接迁移 | 修正后端 URL、采用 HIP 2.6 小节，AMD 7.1.1 兼容内容单列，迁移/设备等价物保持未知。C04 关闭。 | **在所选版本资料范围内满足** |
| 4. 初始化、first step、backward/update、保存与小规模验证方法 | L100–112 的阶段、连通性与示例限制已改善，但恢复设计自身的保存边界/完整状态/随机状态契约未落实。C05 仍开放。 | **部分满足，暂不通过** |
| 5. 源码/测试到职责定位，不补未读第三方协议 | L114–128 增加真实测试引用且保留未知；PyTorch 必要测试映射与所选测试适用条件尚缺，C06 开放；依赖的 CP 取证摘要和 autograd 摘要仍需 C07/C08 同步闭环。 | **部分满足，暂不通过** |

Objective 的组件覆盖与三组资料对照已具备，但不能由此替代上述未完成的验收条件。尤其“如实标注测试缺口”“完整恢复待补”是诚实状态记录，不是缺口已经完成的证据。

## 7. 元数据、关联内容与写入边界

- 正文稳定 ID、reference/training 主归属、`status: draft`、`platforms: [generic]`、日期与 related_ids 保持合法。`generic` 未被当成 GPU/NPU 兼容证明；正文 L38/L139 继续明确未运行、未建立环境档案。
- 正文的 16 个 source_refs 均可在 registry 找到；新增文字引用的 `src.amd.pytorch-compatibility-7.1.1` 亦已登记。存在性不证明当前摘要准确；C07 正是对已有登记 notes 的语义复核，不把 source_checked 当豁免。
- 关联的算子/编译章节 L104–116 仍按实际编译区域、guard、graph break 和缓存说明边界；R01 没有被这些链接自动纠正。checkpoint/并行章节要求的截取和逻辑计数，也不能在本页尚未选定契约时自动视为已交付。
- 不修改任何外部许可或登记状态，不转载外部代码全文；新旧来源均只作短摘要和精确链接，不宣布软件包许可或三平台运行能力已全面核验。

## 8. 本地检查与结论

1. 工作树只读执行 `PYTHONDONTWRITEBYTECODE=1 make check`：退出码 0，**103 content entries / 491 sources**；它仅检查结构与本地文件链接，不验证技术结论或远程页面。
2. 为遵守“只新增这一个文件”，构建在 `/private/tmp/b24-t062-build.W44U8W` 独立仓库快照执行，带入既有 build 基线并使用仓库现有虚拟环境。`make check build` 退出码 0，仍为 **103 content entries / 491 sources**，仅在快照生成 `build/catalog.json`、`build/catalog.md`；未改写工作树 build。
3. 未修改 `src/kb/`，没有运行 `make test`；没有把任何上游测试源码阅读写成测试成功，没有执行正文设计的连通性/恢复/编译对照。
4. 比对检查前保存的 486 个仓库文件的 SHA-256，既有文件变化为 0，新增文件仅本报告；原有未提交修改与未跟踪文件保持原状。报告最后补记检查结果后再次做同样的边界核对。

**最终结论：暂不通过。** 初审 C01/C02/C03/C04/C09 共 5 项 CLOSED，C05/C06/C07/C08 共 4 项 OPEN；另新增 R01（P2 / OPEN）。未达到“全部初审发现 CLOSED 且无新 OPEN P1/P2”的通过条件。

作者下一轮只需围绕 C05 的恢复契约、C06 的必要测试与环境、C07 的串联除法、C08 的条件/时序/摘要同步及 R01 的编译作用域修订，再逐项定向复核。即使这些内容问题以后全部关闭，也只代表本次文档审阅范围内通过，不代表硬件验证、跨框架 checkpoint 迁移、编译数值一致性或生产规模训练已验证。

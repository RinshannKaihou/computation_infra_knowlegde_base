# Batch 24 · T06-02 Codex 技术审阅报告

- 审阅日期：2026-10-18。
- 结论：**暂不通过**。
- 发现：**P1 0 项、P2 7 项、P3 2 项，共 9 项，全部 OPEN**。存在 OPEN P2，不满足本任务的审阅通过条件。
- 执行者：本会话 Codex，技术审阅角色；没有派发子代理，没有修改正文、导航、来源记录、来源登记或任务计划。本轮只新增本报告。
- 模型记录边界：本会话没有向审阅者提供可独立核验的后端实际模型、推理档位及路由元数据，记为 `unknown`。不把导航中的模型名称当作执行证明，不声称另行完成了写作指南第 7 节的指定模型路由验真，也不虚构额外 CLI 审阅轮次。

## 1. 审阅范围与方法

### 1.1 输入与基线

已读取 `README.md`、`docs/authoring-guide.md`（特别是第 5–7 节）、`content-outline.md` 和 `schemas/content.schema.json`。以任务验收条目而不是目录数量、链接可达性或构建成功判定内容是否完成。

| 对象 | 本轮范围 |
|---|---|
| 任务 | `plans/full-coverage-backlog.yaml` L5880–5929 的 T06-02：完整读取 objective、五条 acceptance、source_packages、existing_source_ids、source_discovery、depends_on、context_topic_refs、targets |
| 正文 | `knowledge/06-training/framework-execution.md` L1–126，含全部 front matter、职责图、各节和来源入口 |
| 作者取证 | `docs/research/batch-24-t06-02-sources.md` L1–122，含取回摘要、逐条主张、unknown 和建议登记项 |
| 导航 | `knowledge/06-training/index.md` L1–104；重点核对 L23、L43、L66 的 ID、正文链接及完成状态表述 |
| 来源 | 正文的 16 个 source_refs 对应登记项；另读取证记录所提 `src.amd.pytorch-compatibility-7.1.1`，核对是否被混入 PyTorch 2.6 样板 |
| 关联内容 | 核对三个 related_ids 的存在与正文链接目标；读取关联编译主题中有关执行边界的内容，不把关联页的详细机制自动视为本页已交付的训练 step 对照 |

正文基线 SHA-256：`6f84b9965a98c6fc86625de16e59263a1c7c581f64c0e728a602d98ee11280b7`。

作者取证记录基线 SHA-256：`b6de7fc63e67813e82f69c8bf2243757d91c72fa05b96064b5c792b7c583b2d0`。

任务要求的 A10/A13/A18/S21/S25、四个 existing_source_ids、02.3–02.7 上下文和前置任务均已与任务定义核对。本轮不修改任务仍为 `planned`、`needs_source_preparation` 及 `source_revision: null` 的状态，也不替其他任务或整个 Batch 24 作验收。

### 1.2 独立核对方式与执行边界

1. 先通读正文与作者记录，再通过只读 HTTP 请求重新取回正文/登记项对应的版本化网页、GitHub raw 文件；以实际字节计算 SHA-256，以原文件行号定位。未使用网页阅读工具重排后的行号替代原始行号。
2. 初始网页阅读器对 compile API、troubleshooting、错误的 distributed backend URL 返回内部错误；随后逐个改用 curl 核对。前两页实际返回 HTTP 200，不能据网页阅读器错误判定其不可达；backend 原链接实际返回 HTTP 404，见 U14。
3. 为核实 CLI 否定性主张，额外只读打开同 tag 的参数工厂，并取回 `core_v0.19.2` codeload 源码包，读取配置继承链及一个调度选择测试。GitHub 匿名目录 API 曾因限流返回错误，后续使用该源码包完成相关文件核对；未将限流当作仓库无文件的证据。
4. 没有执行任何上游训练、编译、分布式测试或 checkpoint 示例，没有安装 Megatron/MindSpeed/TorchNPU，也没有操作 GPU/NPU。读取测试源码不等于测试通过。
5. 作者已明确未读的 MindSpeed core 本体、rerun 状态机细节、完整 CUDA graph 路径、Megatron/MindSpeed 的 torch.compile 支持及在研组件配套，继续保留 `unknown`；本报告不补写这些协议或支持组合。

## 2. 关键上游证据重开记录

以下 U 编号供后文引用。链接为实际取回地址；行号为本次返回文件的原始坐标。所有成功的文件均经独立读取相关段落，而非仅检查 HTTP 状态。未把固定 tag 误称为已核定的不可变 commit。

### 2.1 主证据

| 编号 | 精确地址与核对位置 | 结果及支持边界 |
|---|---|---|
| U01 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/training.py`；L2017、L2336、L2400–2425、L2471–2474、L2517–2531、L3342 | HTTP 200。支持 setup/step/train 入口、schedule 调用、optimizer update 与按成功标志推进 scheduler 的控制流；不证明实际运行成功。 |
| U02 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/pipeline_parallel/schedules.py`；L48、L146–163、L397、L532–574、L992、L2120 | HTTP 200。支持无流水线、非交错和交错调度选择及 backward 的梯度接触点；本轮不验证调度数值公式。 |
| U03 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/optimizer/distrib_optimizer.py`；L113–124、L825–885 | HTTP 200。支持 DP 组内优化器状态分片，以及所选 DistributedOptimizer 的非参数状态与参数相关状态分开保存；不是三类框架所有优化器的互操作性结论。 |
| U04 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/mindspeed_llm/training/training.py`；L188–208、L291–307、L377–415、L515、L586 | HTTP 200。入口、wrapper 和四步职责描述与作者定位相符；只说明本文件的调用/包装关系。 |
| U05 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/mindspeed_llm/training/arguments.py`；L35、L242–270、L1015–1027 | HTTP 200。参数校验入口存在；CP×TP×GQA 的整除方向应按取模表达式解释，作者摘要有反向措辞，见 C07。 |
| U06 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/README.md`；L57–97 | HTTP 200。依赖表确实记录 Python 3.10、PyTorch 2.7.1 及多项“在研版本”；不是完整可复现环境。未采用其性能表作为通用结论。 |
| U07 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/v2.2.0/docs/pytorch/install_guide.md`；L56–74 | HTTP 200。支持 MindSpeed `2.2.0_core_r0.12.1` 和 Megatron-LM `core_v0.12.1` 的上游取用指示；未执行其中命令，也未借此核定外链仓库内部协议。 |
| U08 | `https://docs.pytorch.org/docs/2.6/notes/autograd.html`；L585–605、L659–663、L901–910；How autograd encodes the history / Graph retaining | HTTP 200。支持反向 AD、图按迭代重建、局部禁梯度；二次 backward 的引用上下文是共享/复用同一计算图，见 C08。 |
| U09 | `https://docs.pytorch.org/docs/2.6/optim.html`；L585–632；How to use an optimizer / Constructing it / Per-parameter options | HTTP 200。参数或 named parameters、当前状态及参数组职责有来源支持。 |
| U10 | `https://docs.pytorch.org/docs/2.6/torch.compiler.html`；L589–600 | HTTP 200。分别说明 Dynamo、默认 Inductor 以及 AOT Autograd 的职责；不能据此宣称整个训练 step 一定进入编译区。 |
| U11 | `https://docs.pytorch.org/docs/2.6/generated/torch.compile.html`；L590–607 | HTTP 200。对象是可调用函数/模块；默认 `fullgraph=False`、guard/cache 和回退均是执行边界，不是数值自检证明。 |
| U12 | `https://docs.pytorch.org/docs/2.6/torch.compiler_troubleshooting.html`；L670 起、L683–688，Logging tools / Backend ablation / Accuracy 相关内容 | HTTP 200。支持 JIT、graph break 后分段处理及按组件定位；“运行成功”不能替代编译覆盖证据或数值对照。 |
| U13 | `https://docs.pytorch.org/docs/2.6/notes/hip.html`；HIP Interfaces Reuse the CUDA Interfaces、Checking for HIP、TF32、torch.distributed backends；L641–642、L683–685 | HTTP 200。提供实际可摘录的 ROCm 差异：复用 CUDA 命名接口、HIP 构建判别、该版本文档的 TF32 和分布式后端限制。正文未把这些落实为对照内容。 |
| U14 | `https://docs.pytorch.org/docs/2.6/distributed.backend.html` | **未能独立重开有效文档（curl 最终 HTTP 404，返回错误页）**。该 URL 不是已核实的后端证据，不能凭记忆补全内容。 |
| U15 | `https://docs.pytorch.org/docs/2.6/distributed.html`；Backends / Backend.register_backend / init_process_group | HTTP 200。这才是 `src.pytorch.distributed-backend-2.6` 实际登记 URL；正文 L83 与登记不一致。 |
| U16 | `https://docs.pytorch.org/docs/2.6/notes/cuda.html`；Asynchronous execution / CUDA streams / Memory management | HTTP 200。CUDA 执行与观测边界有原文；不自动延伸为 NPU 或任意 ROCm 版本的验证。 |
| U17 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.12.1/examples/run_simple_mcore_train_loop.py`；L24–34、L39–52、L73–77、L107–115、L118–157 | HTTP 200。是使用 MockGPTDataset 的官方**合成数据示例**；硬编码 TP=2、PP=1；保存/加载函数只处理模型 state，循环在加载前结束。没有完整优化器/RNG/数据游标恢复或加载后的对照 step。 |

### 2.2 为争议主张补查的同版本证据

| 编号 | 精确地址与定位 | 结果及用途 |
|---|---|---|
| U18 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/arguments.py` L2196 起的排除表、L2290–2291；`https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/training/argument_utils.py` L96–107、L214–229 | 两文件 HTTP 200。dataclass 字段经过工厂转成 CLI；不能只因未出现字面量 add_argument 就断言无 CLI。 |
| U19 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/model_parallel_config.py` L45–56；`https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/megatron/core/transformer/transformer_config.py` L32、L54–58 | 从 HTTP 200 的同 tag codeload 包读取。TransformerConfig 继承含 `tensor_model_parallel_size` 的 ModelParallelConfig，与 U18 构成参数生成链。没有执行参数解析器。 |
| U20 | `https://raw.githubusercontent.com/NVIDIA/Megatron-LM/core_v0.19.2/tests/unit_tests/pipeline_parallel/test_schedules.py` L47–76 | 从同 tag 包独立读取。`test_get_forward_backward_func` 含三类调度选择断言，说明存在可供作者进一步映射的固定版本测试；**未运行**，不能视为测试成功或任意平台适用。 |
| U21 | `https://raw.githubusercontent.com/pytorch/pytorch/v2.6.0/torch/optim/optimizer.py`；L235–237、L644、L841、L940、L1012 起 | HTTP 200。支持正文定位表里的基类/state_dict/zero_grad/参数组职责；不是本地实验。 |
| U22 | `https://raw.githubusercontent.com/pytorch/pytorch/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/core/dispatch/OperatorEntry.cpp` L537–557 | HTTP 200。只核对所登记 dispatcher 的错误/后端边界，不补写未读算子实现。 |
| U23 | `https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/README.md` 的 PyTorch 安装段；同目录 `version.txt` | 两文件 HTTP 200。源码快照的 PyTorch 2.6 线与 MindSpeed-LLM README 的 2.7.1 线应分开；不证明任何本地配套成功。 |
| U24 | `https://raw.githubusercontent.com/Ascend/MindSpeed-LLM/53f3639c3da9c000a187c44cc0c08d55026ddded/docs/pytorch/features/high_availability.md` | HTTP 200。抽读副本优化器/高可用职责；本页未进一步展开其内部协议，本报告也不升级为恢复能力验证。 |
| U25 | `https://rocm.docs.amd.com/en/docs-7.1.1/compatibility/ml-compatibility/pytorch-compatibility.html`；Key features / Known issues | HTTP 200。页面包含 PyTorch 2.9 + ROCm 7.1.1 和 PyTorch 2.7/2.8 + ROCm 7.0 的分节；不能拿这个不同版本线的“兼容条目”补成 PyTorch 2.6 支持组合。 |

同 tag codeload 实际地址：`https://codeload.github.com/NVIDIA/Megatron-LM/tar.gz/refs/tags/core_v0.19.2`，HTTP 200，SHA-256 为 `4c16ccc2a0d4c1b6c96f59baaab99316ac3b39eca2ef960ddf4436a2962eb69a`。U19/U20 是包内精确路径，不宣称这些 raw URL 被分别再次请求。

### 2.3 字节级复核摘要

| 对象 | 本次 SHA-256 | 与作者记录比较 |
|---|---|---|
| U01 training.py | `d968ef8216f63d6373372190ac895fc905234c116bba3e804d2951876e6ad98c` | 全值一致 |
| U02 schedules.py | `9d3624f4b1bc8e9e4747f339587b3dab2560e0fc5faa9fecd736e4eed2d5f1b7` | 全值一致 |
| U03 distrib_optimizer.py | `40cae307ccb2a3f484ebd5d28ee8549eb572d1b0ba6e91dc5661c137bf560907` | 全值一致 |
| U04 MindSpeed training.py | `341c0792484b7113fb71716eda66c9f4715e106d370b34e80c6a5201f905b2b8` | 全值一致 |
| U05 MindSpeed arguments.py | `fd64204269ad1749159d9b98f47c91f92cb17de5075cb92670f8ab1d5df42a38` | 全值一致 |
| U06 README.md | `7b4893c93e8884d18eb0ff5eee5291bd93eced52dd91572d6a2566c4a7b12f99` | 全值一致 |
| U07 install_guide.md | `8dd60a6cc0983ffcf1e1aaa84da2cba054d1362a7b53a6bffacd665c0bdad423` | 全值一致 |
| U08 autograd.html | `2c9a030d7c870900a74666d0ff2ab926e30a7f173cc143e1066b934c67e486e4` | 不同；作者为 `792703d16102b45ceaebd07ef3d070fd1398af5c32df147085bb4d12bc4f8283` |
| U09 optim.html | `bc25d9bf04809f6725c699f0775f6931f11d4ff662b8c0ac691554b66f2db02e` | 不同；作者为 `53351ea89339ffb9913c675bc5fe946fee1b04f12b042ba8544a12ae6d9a2db9` |
| U17 最小循环示例 | `5ed11bc7834177718e836da7e61e2b067256528b55821c0b8397b82e75773064` | 与现有来源登记的全值一致 |
| U18 arguments.py | `f7fad20bc0e0cd9ba4b9ba7e70fa1a1b77030dfd020a7edb50b1d3b3aa41ebf6` | 本轮补查 |
| U18 argument_utils.py | `4abf3e5e5571c5aa025dd8f716f483c6984fa7dbcf89931574d79fed728dc130` | 本轮补查 |

两个 HTML 的整文件哈希不一致是客观观察；本轮没有作者原始字节，**不能断言差异来自正文修改、站点模板或传输形式中的哪一种原因**。重新核对后的引用段落仍位于相应原始行号范围，相关机制可独立确认。未据哈希差异本身判定作者取证错误，也未悄悄覆盖作者哈希。其他成功重开的网页按本轮段落核对，不声称与作者历史字节完全相同。

## 3. 逐节主张—证据抽查

| 正文小节与位置 | 至少一处抽查 | 判定 |
|---|---|---|
| 导语及“范围与阅读方式”，L43–47 | U06/U07 与 U01 的 ref 不同；U23 的 TorchNPU 2.6 线另列 | 三组资料不拼成一个栈的原则正确；不是三组环境都已具备完整档案，见 C03。 |
| “训练执行循环的职责图”，L49–70 | U08/U09 的 autograd/optimizer，U01/U02 的调度接触点，U04 的 pretrain 链 | 主体职责与函数入口有支持；图是组件目录，不是可替代具体 step 时序的控制流，见 C02；autograd 限定见 C08。 |
| “eager 与 compiled 的 step 路径”，L72–77 | U10/U11/U12 的编译对象、反向捕获、分段和回退 | 不等同数值正确的警示正确；训练 step 对照和编译观测不足，且“通过框架自检”未获支持，见 C02。 |
| “三组资料档案与版本边界”，L79–89 | U06/U07 的依赖、U18/U19 的 CLI 生成链、U13/U15 的后端语义 | MindSpeed 固定依赖转述有据；CLI 否定错误、档案字段不全、AMD 仅转交链接，见 C01/C03/C04。 |
| “各阶段故障分界与小规模验证方法”，L91–101 | U01 的 update_successful 分支、U17 的模型保存/加载范围 | 阶段名称和未执行标记有交付；闭环的对照对象及示例覆盖不足，见 C05。表中症状应作为候选分界，不构成已确诊根因。 |
| “源码—职责定位表”，L103–115 | U01/U02/U03/U04/U05 的函数锚点，补查 U20 的调度选择断言 | 主要源码入口存在；正文没有任何测试定位，见 C06；第三方依赖保留 unknown 的规则正确。 |
| “使用与解释注意事项”，L117–122 | U03 的具体 DistributedOptimizer 格式与 U21 的基类格式 | 不跨版本拼接原则正确；“optimizer state_dict 格式互不兼容”过度绝对，见 C09。 |
| “来源与更新范围”，L124–126 | 本地取证记录存在，正文/verification 均声明未运行 | 草稿和无硬件验证表述一致；不把源码结构核对升级为实验结果。 |

## 4. 发现表

本表只记录可定位的问题及验收缺口。P2 为影响技术判断或任务验收的阻断项；P3 为需收紧的条件/措辞。**所有条目当前均为 OPEN**，本报告没有替作者修订或关闭发现。

| 编号 | 优先级/状态 | 位置 | 发现与证据 | 建议关闭条件 |
|---|---|---|---|---|
| B24-T062-C01 | P2 / OPEN | 正文 L84 | “core tag 无 --tensor-model-parallel-size 等 CLI 定义”不成立。U18 的 `arguments.py` L2290–2291 用 TransformerConfig 构建参数组；U19 的继承链包含 TP 字段；`argument_utils.py` L96–107、L214–229 将字段转换并注册为 CLI。未找到字面量定义不等于没有生成的参数入口。 | 删除该否定性断言，准确区分 Core 配置 API 与同 tag Megatron-LM 参数工厂；补固定版本生成链定位。若保留任何“无 CLI”范围判断，必须具体到已读字段及排除规则，并定向复核。不要虚构 CLI 执行结果。 |
| B24-T062-C02 | P2 / OPEN | 正文 L51–64、L72–77；验收第 1 条 | 职责树和 eager/compiled 各一句描述没有交付训练 step 的数据/控制流：未确定编译的是模型还是整个 step，未映射 backward、梯度同步/累积、update/跳步与编译区外状态推进，也无 compiled 专属观测挂点。U10–U12 明示反向捕获、graph break、guards/回退等边界；L76 又无依据地增加“通过框架自检”的保证。U01/U17 已提供可对照的实际调用顺序。 | 在所选样板及明确作用域下给出 eager/compiled step 对照，标出数据、梯度、控制状态和观测点；按已读证据说明分段/回退，不默认整个 step 被编译。不必复制 02 章机制，但须链接精确小节并把它映射回本页训练路径；删除或限定“框架自检”。保留“编译不等于数值正确”及未执行状态。 |
| B24-T062-C03 | P2 / OPEN | 正文 L81–87；验收第 2 条 | 三个名字/ref 已固定，但并未逐项记录模型、框架、依赖、硬件边界及未知。尤其 NVIDIA 行只有 tag 和泛称 NVIDIA GPU，没有选定模型/配置范围、框架依赖及具体硬件边界或相应 unknown；PyTorch 行没有独立列明 CUDA/ROCm 构建及依赖未知；MindSpeed 行也未限定本页采用何种模型路径。不能把 tag 固定替代资料档案完整性。U06/U07 只补足了 MindSpeed 的部分依赖，不能反向补齐其他两组。 | 三组分别补齐模型或程序范围、框架 ref、关键依赖、硬件/拓扑范围和未知字段。没有证据的项目明确 unknown/未选定，不要求发明可运行环境。必要时链接既有固定档案的精确位置；区分运行时支持、源码可读和本地未验证。 |
| B24-T062-C04 | P2 / OPEN | 正文 L83、L89；取证记录 L42；验收第 3 条 | AMD 部分只说“以资料为准”，没有实际表达选定 PyTorch/ROCm 的执行差异和限制；正文后端 URL U14 实际 HTTP 404，与已登记的 U15 不同。U13 已有可核对的接口命名、HIP 判别及后端/TF32 边界。所提 AMD 兼容条目 U25 又属另一版本线，未在正文给出精确条目和适用边界。 | 用实际可达的版本化后端证据修正链接，补至少能影响本页执行解释的具体差异/限制并逐项定位；若使用 AMD 7.1.1 文档，作为独立版本线登记引用，不拼入 2.6 组合。不迁移 Megatron/MindSpeed 的警示应保留，缺失的设备/算子等价性继续 unknown。 |
| B24-T062-C05 | P2 / OPEN | 正文 L93–101；验收第 4 条 | “首步 loss、梯度范数与重载后首步一致性”没有规定与哪个状态、哪一批输入比较、如何控制随机性或采用何种事先定义的容差，不能可靠区分更新未生效与合法状态推进。引用的 U17 默认 TP=2，且只存模型、不存优化器/RNG/数据游标，加载后也没有再执行一步；不能直接承接正文完整闭环或泛化成单卡/跨平台样板。 | 将连通性检查与恢复一致性分开：定义保存边界、未中断参考分支与恢复分支的同一后继输入/状态、观测项、预先约定的比较规则及不确定时停止条件；把参数更新或合法跳步作为独立观测。明确 U17 仅为 NVIDIA/该 ref 的合成数据、模型保存加载示例及其默认配置，完整状态/再一步是待补的验证设计；不新增未经来源核实的执行命令或结果。 |
| B24-T062-C06 | P2 / OPEN | 正文 L103–115；取证记录 L45–55；验收第 5 条及 source_discovery L5915 | 标为“源码—职责定位表”的内容只有实现或文档，没有任何测试文件、测试函数、断言或测试适用条件。读实现入口不满足任务中“源码/测试到职责”及“必要测试”的要求。U20 同 tag 中有可读的调度选择断言，说明不能把未做测试映射当作测试资料不存在。 | 独立读取所选固定版本的代表性上游测试，补“职责—实现—测试/断言—环境前提—未覆盖”定位；其他平台未取得测试时明确缺口，不套用 NVIDIA 测试。只需审阅测试源码，不要求本轮执行；保持第三方组件内部协议 unknown。 |
| B24-T062-C07 | P2 / OPEN | 取证记录 L37、L121；`sources/registry.yaml` L6024 | 参数约束摘要把数学方向写反或至少造成反向理解：“num_attention_heads 须整除 ulysses_size×TP”“num_query_groups 须整除 TP”。U05 L247–253 的实际检查是头数除以并行规模乘积、GQA 组数除以 TP 的余数为零，同时商至少为 1；L255–263 的后续约束另受 kv_head_repeat 开关控制。正文职责定位依赖这份取证摘要，错误会传给组合边界判断。 | 作者在取证表及登记 notes 统一改为无歧义的被整除/取模条件，保留商为正和开关分支适用条件；只陈述已读校验，不把通过这段校验当作完整配置受支持。定向复核同 ref 原始表达式及所有本任务摘要副本。 |
| B24-T062-C08 | P3 / OPEN | 正文 L66；取证记录 L34、L50 | “重复 backward 需 retain_graph=True”遗漏同一计算图及已释放 saved tensors 的上下文，容易被读成每个训练迭代都要保图。U08 的 Graph retaining 谈共享/复用图；同页也说明图随迭代重建。常规重新 forward 后的下一轮 backward 不由该段推出必须 retain_graph。 | 明确仅在需要再次遍历同一图且仍依赖已释放中间量等条件下讨论保图；不得把 retain_graph 变成所有训练 step 的默认要求。同步收紧取证摘要，保持实际故障上下文。 |
| B24-T062-C09 | P3 / OPEN | 正文 L119 | “optimizer state_dict 格式互不兼容”是跨三组所有实现的绝对结论，没有指定优化器、封装层、格式、版本或迁移条件。U03 支持某个 DistributedOptimizer 的具体分离格式，U21 支持基类接口，二者不能证明所有 PyTorch/Megatron/MindSpeed 优化器之间都绝对不兼容，尤其 MindSpeed 的未读依赖协议仍 unknown。 | 改为“不能默认互换，兼容性未验证”，或仅对已经读取的具体格式/加载接口作有条件比较并提供精确证据。不要从此反过来宣称存在可用互转能力。 |

## 5. 验收条目逐项核对

| 任务验收条目 | 已交付部分 | 缺口与判定 |
|---|---|---|
| 1. eager/compiled 训练 step、数据/控制流、观测点；编译不等同数值正确 | 有职责图，明确不把编译成功当数值正确；有通用 profiler/timers/loss 观测词 | **部分满足，暂不通过**。组件目录未转换为两条可追踪的训练执行路径，compiled 覆盖证据和控制边界不足，另有无依据“自检”表述；C02，及条件精度 C08。 |
| 2. 三组独立固定档案，逐项列模型/框架/依赖/硬件边界与未知 | 三组 ref 分开，MindSpeed 的 2.7.1/在研组件及 core_v0.12.1 已正确分离 | **部分满足，暂不通过**。档案字段不齐，且 NVIDIA CLI 结论错误；C01/C03。不能靠泛称平台和“不同栈”警告替代逐字段边界。 |
| 3. AMD 使用所选官方后端资料表达差异/限制，不宣称直接迁移 | 不直接迁移的警示明确；HIP 来源已登记 | **部分满足，暂不通过**。没有展开实际差异，backend 原链接 404，兼容条目版本线没有落实；C04。未据不可达页判定任何后端能力。 |
| 4. 初始化、first step、backward/update、保存等分界及小规模验证方法 | 阶段表齐备；设计明确未执行，没有伪造硬件结果 | **部分满足，暂不通过**。恢复对照和更新进展判据不明确，官方样例的模型级保存/加载不足以承接完整闭环；C05。 |
| 5. 源码/测试到职责定位；未读第三方协议不补写 | 实现入口的主要行号经独立重开；第三方协议 unknown 明确 | **部分满足，暂不通过**。缺测试定位与断言范围；C06。取证约束摘要还需按原表达式修正，见 C07。 |

Objective 的组件覆盖轮廓已经出现，但“训练框架如何组装执行循环”的核心对照仍缺训练 step 的边界和控制流，不能仅凭几个正确函数入口判定 objective 已完整完成。source_discovery 中 MindSpeed 接口与所指 Megatron 依赖已有证据；Megatron 实现已固定；PyTorch 必要测试等缺口未闭环。

## 6. 元数据、来源与导航核对

- `id: training.framework-execution` 与任务 target 一致，标题与 H1 一致；`type: reference`、`domain: training`、`status: draft` 符合内容类型/主归属。没有要求改成 procedure，也没有把 `generic` 当作平台兼容证明。
- `updated_at: "2026-10-18"` 是合法日期字符串，未在本次审阅日期之后。三个 related_ids 均存在；正文指向并行页和编译页的本地链接有效。checkpoint 相关 ID 存在，但验证设计仍需落实自己的比较边界。
- 16 个 source_refs 均已登记；四个 verification.evidence_refs 均存在。登记“存在”不代表其支持所有主张，尤其 U14 与登记 URL 不同，来源摘要存在 C07。
- `verification.status: source_checked` 及 notes 明确未运行，未冒充 reproduced；这与 draft 不冲突。但应在修订时重新核定 source_checked 的实际覆盖，不能借该状态豁免 C01–C07。
- `training.index` 的 related_ids、L43 正文入口和 L66 主题入口一致；导航仍写草稿、未实测及具体工作负载/执行验证待补，没有宣布该任务 review passed。本轮未发现稳定 ID 损坏、重复正文主归属或本地死链。
- 取证记录只提源码结构/未运行，厂商性能表明确未采用；正文没有把厂商数字升级成通用性能结论。U17 是上游合成数据示例，应在正文也明确写“合成”，不能把 mock 演示当成本地实测；该项随 C05 关闭。
- 外部许可状态保留了 unknown/partial 的范围；本报告没有重发外部代码、图片或完整网页，也没有增添统一再分发许可。登记状态本身不作为软件包许可或逐文件许可已全面核验的证明。

## 7. 本地检查与写入边界

1. 在工作树执行 `PYTHONDONTWRITEBYTECODE=1 make check`：退出码 0，结果为 **103 content entries / 489 sources**，结构与本地文件链接通过。
2. 为遵守“只新增报告”，**未在工作树运行会改写 build 的构建**。将当时仓库复制到 `/private/tmp` 独立快照，在快照执行 `make check build`（使用现有虚拟环境 Python）：最终退出码 0，检查通过并生成快照内的 `build/catalog.json`、`build/catalog.md`。
3. 首次临时快照排除了既有 build，检查因此报告 `docs/first-fill-status.md` 指向两个缺失清单；补入工作树既有生成文件作为快照基线后重新检查/构建通过。这是临时复制范围造成的错误，不记为正文发现，也不隐瞒为一次即过。
4. 未更改 `src/kb/`，未运行 `make test`；没有声称运行上游测试。结构/构建结果不证明本文技术正确、平台支持或硬件验证成功。
5. 工作树原有其他未提交内容保持原状；本报告针对上述正文哈希，不覆盖后续作者可能并发进行的修订。

## 8. 结论与定向复核要求

**暂不通过：T06-02 本轮范围内共 9 项 OPEN，P1 0、P2 7、P3 2。** P2 的 C01–C07 是阻断项；本轮只完成审阅及报告交付，没有实施正文修订，没有关闭任何发现。

作者修订后，应由同一审阅者重新读取受影响的正文、取证摘要和来源条目，并至少重开参数工厂/继承链、编译边界、HIP/后端、最小示例保存范围及实际新增测试。逐项检查关闭条件，重新填写五条验收结果；OPEN P1/P2 清零之前不声明通过。P3 应收紧或明确记录处置理由。

即使后续内容审阅通过，也仍不代表任何 GPU/NPU 环境、跨框架 checkpoint、编译数值一致性或生产规模执行已经验证；当前未知项和未执行状态必须保留。

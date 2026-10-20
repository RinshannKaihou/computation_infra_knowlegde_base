# Batch 27 · T07-06 新建交付初审

## 会话元数据

- 审阅角色：AI 可靠性知识库批次审阅者；正文作者与本轮审阅角色分立。
- 实际执行模型：`gpt-6.1-sol`；实际推理档位：`xhigh`。
- 核验依据：当前 `CODEX_THREAD_ID=01a15aeb-1946-7dc0-b7a8-b52e1f4adac1` 对应 CLI rollout 的 `session_meta.originator=codex_exec`、`source=exec`、`cli_version=0.163.0`；`turn_context.model` 与 `effort` 分别为上述值，所查运行记录只有这一组模型/档位。本轮未调用其他审阅模型。
- 工作目录：`/Users/ywang2397/work/AI_reliability_knowledge_base`。
- 日期：2026-10-21（Asia/Shanghai）。
- 任务：`T07-06`，operation 为 `new`，内容类型为 `concept`；本轮为未提交工作区版本初审。
- 审阅正文 SHA-256：`d51a94a290465b5299209e2fa7da3a4bf9a8df63744c09ebd70c4dcc091551a8`。
- 写入范围：只新增本报告；不修正文、来源表、计划或导航，不改变审核/验证状态。

## 审阅范围与方法

先读取 [README](../../README.md)、[写作指南](../authoring-guide.md)、[内容总目录](../../content-outline.md)、仓库 `AGENTS.md` 与元数据 schema，再逐条读取 [T07-06 正文](../../knowledge/07-inference/distributed-inference-layouts.md)、[任务 acceptance](../../plans/full-coverage-backlog.yaml)、[作者取证记录](batch-27-t07-06-sources.md)及[来源登记表](../../sources/registry.yaml)。下文“正文 L…”均指本轮 111 行原文件坐标。

证据固定为 vLLM `b17039bccc17b94a2ea107272ad7bc93508708df`、vLLM Ascend `52d4acfa51fb868823d1070b81cbd2d97e9e4696`、MindIE-LLM `69e5a5dd4b533eaffc7e198320435350825a36f7`。重新打开 `/tmp/b27-fetch/` 原文件，以原文件行号核对，未把作者摘要当成上游结论。网络重取曾遇网页工具 cache miss 与本地 DNS 失败；随后使用已存在的完整快照补查实际断言及 MindIE 配置页，未用其他版本替代。

来源结论、作者归纳和待核实分别判定。表格或命令名称存在，不等于验收项完成；文档字段注释也不等于执行分支。未安装、启动引擎，未运行 GPU/NPU、通信测试或故障注入。结构校验不作为技术正确性或硬件兼容性的证据。

### 文件身份复核

作者记录列出的 16 个缓存文件，其 SHA-256 前 16 位全部匹配。完整摘要如下；文件名均相对 `/tmp/b27-fetch/`。其中 MindIE EPLB、moe、micro_batch 三页仅复核文件身份，正文已将其未展开内容列为 unknown，本轮不将其提升为已核能力。

| 缓存文件 | SHA-256 |
|---|---|
| vl-parallelism_scaling.md | `ee64a18691d16f463c4603bf89121284a4bd531b21d700a63cff2763b61288f9` |
| vl-cp_deployment.md | `7f0559ad25f3648373f25bb61571208ebf3eb09284226d0fb17196a5ebe02458` |
| vl-dp_deployment.md | `24eecb8e13d89f13e9b2a233b88163f9f5878647abf859acd676ff7258a7efec` |
| vl-ep_deployment.md | `0d21023710921910d521ae8088a9e0ac25c81a5fa126ae44ac10620ae735947f` |
| vl-dist_troubleshooting.md | `e925dff3c9a19a5510e11a980a092b408565f90feb469a6201b9f864187129d3` |
| vl-config-parallel.py | `0673811d4f37058d0f9be143ce113b31ad47e90bd74c1aedad51cfa7cc44d6cd` |
| mi-f-tensor_parallel.md | `d121df6eca46276bbb69aa0d419a2b639f29a8c97187e7da01e385455cc20147` |
| mi-f-data_parallel.md | `86bfa6f496129adcfc662f460c49047d64d21cd8d4dd1cb8b09757485bc8ce35` |
| mi-f-context_parallel.md | `81079974f242e90abbb8b320c5cf31e5578786ce9e28b39c4d81ad0a2a92cbd0` |
| mi-f-sequence_parallel.md | `a444200c23cc49b8547933eb1c9c31f9698510f5f10e0f5528ca84186598b8a9` |
| mi-f-expert_parallel.md | `34e11a572286c43f1ed568d6de720c54aeb156150281af4f80dbafff26c11529` |
| mi-f-expert_parallelism_load_balancer.md | `b020d1ec5e0d37d7e249f4d2a94809ddc78735da910a45dfb81ed0b99c7fce56` |
| mi-f-moe.md | `512331151682669eeaa4e60526095aeded4a994aaad48923ecd2189b19f16070` |
| mi-f-micro_batch.md | `e5af759ca7e6d0c2e77a021221c81fc2348ebdeec422cc170ddb6d19689cb4e4` |
| mi-optimization_and_tuning.md | `0c348668366760a0fa2b39d48cdd7d605b0b3ae305a74f224a09252e92b0c72a` |
| va-supported_features.md | `9c576fc4063ad9718aa76e91aeb602ed7d835ee4a121afc7df9ccc215801ae42` |

补充打开的完整快照分别位于 `/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/`、`/tmp/MindIE-LLM-master/`。前者 `config/parallel.py` 与本轮缓存摘要完全一致，`config/model.py` 与本轮既有 `vl-config-model.py` 一致；后者 CP 页与本轮缓存一致，下列两个服务文档摘要也与 [T07-03 取证记录](batch-26-t07-03-sources.md)一致。目录名没有被单独用作版本证明。

| 补充文件（相对各快照根目录） | SHA-256 |
|---|---|
| vllm/engine/arg_utils.py | `a07546cd72a3906bfa0f5e123e1cec7d7102e0396bde8198a1f9137d1ed3265d` |
| vllm/config/vllm.py | `937bfd346f262a34b2e2e3c60ef8c0ce04907c7bb6c46e60a67fff15a9131e50` |
| vllm/config/model.py | `bb8a629254b756f030ccb1808f72df0a9e537e22ae364521044993448d960c9c` |
| docs/zh/user_guide/user_manual/service_parameter_configuration.md | `59f1dd120399191f251ff9cdc338669f32728a042a1acd254be16bfa76a7b613` |
| docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md | `75bd1da15eb171f244206c5a3c7ab7adf0ca9b34d6d15eb7b5a10c25257d3ad0` |

## 发现清单

以下 C01–C11 均为 **OPEN**。P1 表示严重错误或危险误导，P2 表示实质技术/验收缺口，P3 表示定位、登记和导航问题。本轮没有 P1。

### C01 · P2 · DP 所有权行未包含 MoE 权重跨 DP 分片，缺少 group/rank 图示

- **位置**：正文 L48–56，尤其 L50 的权重所有者列。
- **陈述**：将每个 DP rank 写成持完整模型或仅在本 DP 单元内 TP/PP 分片，不能描述紧接着讨论的 DP attention＋TP/EP MoE。专家权重跨 `DP×TP` 组分片，不能仅给同步列加 MoE 例外而保持权重列不变。正文也没有画出组合下的请求入口、attention 组、expert 组及 rank 责任；概念名称表不足以展示这些组如何重叠。
- **证据**：[vLLM DP L7–17](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/data_parallel_deployment.md#L7-L17)说明专家层默认 TP 组为 `DP×TP`；[EP L35–67](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/expert_parallel_deployment.md#L35-L67)明确专家跨所有 EP ranks 分片、attention 在 DP 间复制或在各 DP 单元内 TP 分片，并给出 TP=2、DP=4 的示例。
- **关闭条件**：把纯独立副本与 MoE DP attention 分开写清权重/KV/请求/同步；补一幅有来源约束的组合示意，标出逻辑 group、rank 责任与 dispatch/combine 路径。若自行编号，标为本库示意，不声称实际运行时 rank 编号或 placement 已验证。

### C02 · P2 · 合并 CP/SP 行把 CP 的 ring 通信扩张成 SP 的共同语义

- **位置**：正文 L54、L58、L82、L102。
- **陈述**：CP/SP 共用“ring 传 KV＋分块结果修正”的同步列，会使读者认为 MindIE SP 单独开启也已取得 ring 实现证据；来源只对 CP 作此声明。行内“与 TP 配合”的权重所有者也没有解释权重究竟复制还是分片。训练 SP 与这里的 MindIE KV SP 还应明确区分。
- **证据**：[MindIE CP L3–6](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/context_parallel.md#L3-L6)声明 ring、FA2 分块与结果修正；[SP L3–21](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/sequence_parallel.md#L3-L21)只说明 KV 分片、组合条件及限制，没有给出该 ring 同步结论。既有[训练并行正文](../../knowledge/06-training/parallelism-and-state.md) L70–82 的 SP 是激活/部分 buffer 分布，不能套用其实现来填补这里的证据。
- **关闭条件**：拆开并注明平台及 prefill/decode 语境；CP 的 ring 保留为 MindIE CP 来源结论，SP 未核的同步/权重细节标 unknown。分别写明 CP、SP 均不支持 BF16，并链接训练 SP 的不同语义；vLLM dcp 单列或保持独立说明。

### C03 · P2 · world_size 无条件公式只采字段注释，遗漏同文件实际赋值分支

- **位置**：正文 L56；作者取证表 world_size 行与 registry 对应 notes。
- **陈述**：`world_size=TP×PP`、跨 DP 为 `TP×PP×DP` 符合 L238–239/L351–354 的注释口径，但并非该快照所有配置下的实现公式。文中将其称为组合语义，没有限定 PCP=1 及普通执行后端。
- **证据**：[parallel.py L539–547](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L539-L547)实际赋值乘入 `prefill_context_parallel_size`；`external_launcher` 分支进一步乘入 DP。[L351–354](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L351-L354)的属性返回 `self.world_size×DP`。字段注释与这些分支存在范围差异。
- **关闭条件**：把简化公式限定为本文普通布局假设，补实际赋值的精确定位并记录特殊分支；不能以此宣告尚在开发的 PCP 可部署，也不要擅自替上游裁定特殊分支的预期行为。同步纠正取证记录及 notes 中无条件的“实现”口径。

### C04 · P2 · dcp 的“实现校验”定位不成立，GQA 组合限制未写出

- **位置**：正文 L58，作者取证表 L46、unknown L76，frontmatter L32 的“校验逻辑”范围。
- **陈述**：`parallel.py L252–273` 是字段说明与 docstring，不是执行整除检查的分支。两个约束本身有实际代码支持，但当前证据级别及位置错误；此外，把 `dcp≤TP/H` 和 `TP%dcp=0` 作为选型约束仍不足以覆盖该快照的 GQA 检查。
- **证据**：TP 整除的实际断言在 [arg_utils.py L1387–1395](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/engine/arg_utils.py#L1387-L1395)；block 条件在 [config/vllm.py L830–854](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/vllm.py#L830-L854)，限定 DCP>1，并要求 block size 不小于且能被 interleave size 整除。[config/model.py L1076–1098](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/model.py#L1076-L1098)对非 MLA 还检查 TP>KV heads、DCP 上界及每 KV head 的 query-head 数能被 DCP 整除。
- **关闭条件**：改引实际调用位置，区分字段契约与执行断言，补 GQA/非 MLA 条件或明确当前清单不完备并给出检查入口；更新 source_checked 的核对范围。保留正确的三组案例数字，不能把文档范围当作完整模型支持矩阵。

### C05 · P2 · MindIE 配置层级把 EP、MoE 字段错误归入 parallel_options

- **位置**：正文 L82 开头。
- **陈述**：把 `ep_level/moe_tp/moe_ep/lm_head_local_tp/o_proj_local_tp` 全部放在 `models.deepseekv2.parallel_options`，与所引服务配置示例不符，会直接给读者错误的字段位置。
- **证据**：[optimization_and_tuning.md L169–191](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/optimization_and_tuning.md#L169-L191)把 `moe_tp/moe_ep` 放在 ModelConfig 模型项，将 `ep_level` 放在 `models.deepseekv2`；同页还给出 `moe_ep×moe_tp=worldSize` 及 ep_level=2 时 moe_tp=1。[expert_parallel.md L34–59](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/expert_parallel.md#L34-L59)同样把 ep_level 置于 deepseekv2 内。
- **关闭条件**：逐字段分开列配置层级并补 MoE 乘积等式。local tp 的参数表写有 parallel_options 层，而 [tensor_parallel.md L75–80 示例](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/tensor_parallel.md#L75-L80)直接放在 deepseekv2 下；这部分应保留文档层级差异或核对解析代码，不能把参数表的层级扩张给其他字段。

### C06 · P2 · “多机默认 Ray”没有区分指南口径与实际后端选择条件

- **位置**：正文 L78，相关取证及 registry notes。
- **陈述**：该句是上游部署指南的原意，但正文同时给出 `--nnodes` 的多机 mp 路径，却未说明这一路径会影响默认选择；读者不能据“多机”二字确定实际用了 Ray。
- **证据**：[parallelism_scaling.md L31–33](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/parallelism_scaling.md#L31-L33)作默认 Ray/mp 的概述；同快照 [parallel.py L590–631](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L590-L631)在未显式指定后端、world_size>1 时先置 mp，CUDA 且 nnodes>1 分支也选 mp；DP Ray、placement group 等另有分支。CUDA 本节点卡数不足但 nnodes 未正确设置时还可能直接报错。
- **关闭条件**：将“指南称…”与实现条件分开记录；说明 nnodes、多机进程启动方式、显式配置及 Ray placement 的作用，要求记录最终生效后端。不能把一条指南概述当成所有 NVIDIA/ROCm 环境的运行期默认值。

### C07 · P2 · VLLM_HOST_IP 的“各节点统一”遗漏每节点值必须不同

- **位置**：正文 L89，作者取证 L50，registry 对应 notes。
- **陈述**：当前措辞容易被执行为所有节点设同一个 IP。应对齐的是每个节点内部 vLLM 与 Ray 所用的地址，各节点并不共用一个 VLLM_HOST_IP。
- **证据**：[distributed_troubleshooting.md L11](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/distributed_troubleshooting.md#L11)明确要求每节点取不同值；[parallelism_scaling.md L77–104](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/parallelism_scaling.md#L77-L104)分别给 head/worker 的本机 IP，并要求用 ray status/list nodes 核对。
- **关闭条件**：写成“每节点设为其自身、且与该节点 Ray 一致的可达地址，各节点值不同”，保留命令用于核对已选地址/资源；同步修正取证与 notes 的歧义。

### C08 · P2 · 选型表缺少验收要求的扩展效率/尾延迟比较，容量条件有歧义

- **位置**：正文 L62–74。
- **陈述**：L67“单机多卡放不下→TP”按字面与下一行“多机才放得下”重叠；来源实际条件是单卡放不下、单机多卡放得下。表格覆盖模型容量、长上下文、MoE 和互联，但代价列没有按布局比较扩展效率、内存分配和尾延迟，转链指标定义不能替代这种比较。L71“先 TP 到 H，再 dcp”也应说明 DCP>1 需要 TP>H，不能将 TP=H 当作可开启有效 DCP 的通用终点。
- **证据**：[parallelism_scaling.md L5–23](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/parallelism_scaling.md#L5-L23)给出明确容量区间；[context_parallel_deployment.md L27–41](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/context_parallel_deployment.md#L27-L41)说明复制、DCP 通信代价及先调整 TP 性能再用 DCP 减复制。任务 acceptance 第 2 项明确要求上述比较。
- **关闭条件**：纠正容量区间和 DCP 条件；在模型/序列/并发/硬件/互联条件下补定性比较或比较模板，至少解释影响扩展效率与长尾的同步、stage 不均、专家负载等条件及其待测范围。归纳性机制判断继续标为本库归纳，数值未知保留 unknown；不要求编造效率或时延结果。

### C09 · P2 · ROCm 明示 unknown 合规，但仍未交付 acceptance 要求的布局限制

- **位置**：正文 L7、L44、L78、L111；acceptance 第 3 项。
- **陈述**：正文诚实说明没有 ROCm 专属取证，这避免了误用 NVIDIA 判据；但三平台验收明确包含 vLLM NVIDIA/ROCm。当前只有上游通用描述，没有固定 ROCm 的所选布局、硬件/后端和通信限制，不能把这项算作已完成。
- **证据**：作者 unknown 第 5 项与正文直接承认此缺口。已读 [parallel.py L325–338](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L325-L338)至少明确 EPLB 的 CUDA/ROCm 平台门控，但这一个判断不能证明所有 TP/PP/DP/EP 或 all2all 后端在 ROCm 的组合支持。
- **关闭条件**：补固定版本的 ROCm 官方布局/实现证据，限定实际能证明的布局与通信后端；继续把未覆盖组合和 RCCL 对应观测口径列 unknown。若客观无法补齐，保留此验收项未通过并明确后续证据任务，不能用平台名或 NCCL 日志替代。

### C10 · P2 · 单副本失败证据未定义，地址检查没有覆盖布局 mapping 与通信等待

- **位置**：正文 L86–95，尤其 L92；acceptance 第 4 项。
- **陈述**：L92 把单 rank 失败表现留为 unknown，随后转给 PD 分离及未指明的恢复正文；既有 PD 页讨论 connector/请求失败和外部路由职责，不建立 DP attention＋共享专家组的失败边界。可观察表的 mapping 也只有地址检查，没有说明怎样对应请求、DP/TP/PP/EP 组、rank 与设备/节点；NCCL 传输路径命中不是通信等待进展。三项验证已有框架，但无法据当前表判断故障是否只影响一个副本。
- **证据**：[vLLM DP L9–17](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/data_parallel_deployment.md#L9-L17)明确共享专家组需跨 DP 同步，不能假定单 DP rank 是故障隔离单元。[PD 正文](../../knowledge/07-inference/pd-disaggregation.md) L42–49、L74 没有给 DP 单 rank 故障的证据；[collectives 正文](../../knowledge/03-communication/collectives-and-rank-progress.md) L194–207 已提供 group、成员、操作、进度及时间线字段，可引用并与本布局关联。
- **关闭条件**：补一份未执行的最小证据/验证记录设计，关联请求失败或停滞、目标 rank/进程状态、组成员与节点设备、其他副本/共享专家组进度、collective 进入与完成及前序错误；区分独立服务副本和 MoE 共享同步域。给出要检验的影响范围及通过/失败判据，运行期表现没有源码/文档证据时仍标 unknown。三项验证应共用固定模型/权重、输入输出长度、采样、负载与资源口径，并记录错误/超时；本次不要求实际制造故障。

### C11 · P3 · 精确来源定位、登记记录与普通链接尚未对齐

- **位置**：正文 L54、L78、L80、L82、L109；related_ids L25；作者取证 L57、L67/L69、L86。
- **陈述与证据**：vLLM Ascend 的五行状态实际在 supported_features.md **L23–26、L31**，正文及取证的 L20–25 漏掉 DP/CP；async EPLB 默认 policy 的断言在 parallel.py **L85–88**，不在正文 L308–341 链接范围。MindIE L82 多项硬约束/两处冲突主要靠末尾 feature 目录导航，缺少邻近的具体文件定位。所有权表中的 PP 按层持 KV、邻段传激活等内容含机制推导，parallelism_scaling L23/L31 并未逐列陈述全部 KV/同步细节，应与来源原文区分。取证 L86 声称 Ascend notes 已补并行五行，本轮 registry 该条实际未见这次补记。`communication.bandwidth-baselines` 虽已登记为 related_id，正文仍缺[集合通信带宽基线](../../knowledge/03-communication/bandwidth-baselines.md)的普通 Markdown 导航。
- **关闭条件**：修正上述原文件坐标；在 MindIE 约束和冲突处直接链接对应特性页与 optimization_and_tuning 的相关行；标出所有权表中来源未直接陈述的机制归纳，或补足精确证据；使取证的集成声明与 registry 实际内容一致；补带宽基线普通链接。这里只要求定位和记录准确，不把已有来源登记或本地文件链接判为不存在。

### 已核对且本轮无新增问题的部分

| 维度 | 判定依据及边界 |
|---|---|
| MoE 同步与 dummy forward | 正文 L50、L99 与 DP 原文件 L9–17 一致：专家层每 forward 跨 rank 同步，空 rank 做 dummy forward，Coordinator 每 N 步 collective 判全体 idle；每 DP engine 独立 KV。此项通过不抵消 C01 的权重所有权错误。 |
| TP 的 KV 复制与 DCP 数字 | 正文 L51/L58 的 TP>H 时复制 TP/H、DCP 不增加 GPU 数及交织分片符合 context_parallel_deployment L23–31。R1 tp8→dcp8，Kimi-K2 tp16→dcp16 或 dcp8（剩 2x，来源案例为节点内通信），Qwen3-235B-A22B 的 H=4、tp8→dcp2，均与 L35–39 一致；案例不推广为任意 placement 的性能保证。 |
| 选型的可溯源性 | 逐行核对：单卡、单机 TP、多机 TP×PP、无 NVLink/不均分割分别见 parallelism_scaling L7–9/L23；MoE 见 DP L7；KV 侧并行见 CP L23–29 与 MindIE SP；吞吐 DP 见 DP L3/L17、MindIE DP L7。正文 L62 已将未标注处声明为本库归纳，未把整表伪装成官方通用推荐；覆盖完整性仍见 C08。 |
| vLLM EP/EPLB | allgather_reducescatter 默认、flashinfer_all2allv 的 MNNVL 语境与所列可选后端符合 EP L19–26；enable_expert_parallel 及 TP×DP>1 符合 parallel.py L331–338，async 默认 policy 符合 L85–88。并非所有后端/平台组合的支持证明，精确定位见 C11。 |
| Ascend 状态边界 | supported_features L23–26/L31 五项均为 Functional；正文明确 Next Step 不能证明当前能力，保留 TP>4×graph、dynamic EPLB 的实现 unknown。DP 行的 Qwen3 MoE 文字也在 Next Step 列，不能独立当模型组合支持证据。非对称 PD TP 转链既有 PD 页，未推广为普通服务能力。 |
| MindIE 数值及组合约束 | data_parallel L23–29 支持 attention 的 dp×tp、启 CP 时 dp×tp×cp、dp=1、sp=tp 和默认 tp/moe_tp；CP L12–32 支持须同时 SP、仅切 2、不支持 BF16、PD 分离仅 P；SP L10–21 同样要求 sp=tp、PD 分离仅 P 且不支持 BF16。EP L14/L25 支持 >32 的指定 DeepSeek 模型融合算子和双机 ep_level=2 交换机前提；optimization L172 支持 ep_level=2 时 moe_tp=1。字段层级和分行表达仍需 C02/C05 修订。 |
| 跨页冲突① | 正文保留 optimization L62/L67–68 的“D 未分布式推荐、仅 tp=1 可开”，以及 tensor_parallel L9–11 的“D 分布式场景支持、tp>1 对 o_proj 排斥/对 lm_head 不建议”。两维差异均保留，没有裁定谁更新或补成共同支持条件。 |
| 跨页冲突② | CP L11、SP L8 的 R1-W8A8/R1-W4A8/V3-W4A8/V3.1-W4A8，与 optimization L114/L139 的 V3/R1/V3.1-W8A8，确实互缺；正文 L82 明说不合成并集、相应组合 unknown。通过的是冲突记录，不是这些组合获得兼容性认证。 |
| 日志与 MindIE timeout | NCCL TRACE 的 NET/IB/GDRDMA 与 NET/Socket 判读符合 parallelism_scaling L207–213，正文 L78 明限 NVIDIA 语境；两条 KV 容量/并发估计日志及 max_model_len 口径符合 L13–20。MindIE 服务参数原文件 L133–134 确认 kv_link_timeout 为 PD KV 通信域建域超时、失败重试至成功/超时，kv_trans_timeout 为 D 拉 KV 超时，两者用途不同；正文的既有服务参数链接能追到该页，没有据此证明一般 TP/EP 通信域已建立。 |
| 领域边界与本地链接 | 推理无梯度更新的定位及 KV/执行转链清楚；PD 的 connector/非对称布局留在 PD 主文，未复制底层网络或 collective 实现。训练 SP 的语义提醒见 C02。正文 9 个 related_ids、5 个 source_refs 均存在；id/type/domain/title/date/draft 合规，source_checked 与未硬件验证分开。量化页 L111→本页、本页 L82→量化页均为有效本地链接，07 首页已列新条目；related_ids 无须强制双向。 |

## acceptance 逐条判定

以下逐项对应 [backlog T07-06 L6466–6471](../../plans/full-coverage-backlog.yaml) 的五项原要求，判定针对本轮正文，不扩张为整批其他任务的结论。

| 项 | 原验收要求 | 判定 | 依据与关闭依赖 |
|---|---|---|---|
| 1 | 画出请求分配、权重与 KV 的所有者、同步路径及各 group/rank 责任，解释独立副本 DP 与模型内 TP/PP/EP 的区别。 | **部分满足，未通过** | 有四列所有权表及 MoE 同步例外，但 MoE 权重所有权错误、CP/SP 混写，尚无组合 group/rank 示意；world_size 只给无条件简式。依赖 C01–C03。 |
| 2 | 按模型/序列/并发/硬件/互联给出选型表，比较跨机通信代价、扩展效率、内存和尾延迟。 | **部分满足，未通过** | 已有可溯源规则且标明作者归纳；容量区间有歧义，缺布局间扩展效率/尾延迟的实质比较。依赖 C08；DCP 可用条件同时受 C04 约束。 |
| 3 | 至少固定 vLLM NVIDIA/ROCm、vLLM Ascend 与 MindIE 的所选布局限制；MoE/非对称/混合组合不从名字推断支持。 | **部分满足，未通过** | 三条版本线、Ascend 状态边界与两处 MindIE 冲突保留正确；ROCm 所选限制缺证，MindIE 配置层级错误，DCP/后端条件及来源定位需修订。依赖 C04–C06、C09、C11。 |
| 4 | 定义跨机初始化、mapping、通信等待与单副本失败的可观察证据和最小 correctness/throughput/latency 验证。 | **部分满足，未通过** | 初始化、NCCL 路径、容量日志及三项验证已有雏形；IP 设置缺关键限定，单副本失败仍仅 unknown，地址 mapping 未连到 group/rank 与等待进度。依赖 C07、C10。 |
| 5 | 链接网络/RDMA/collective 基线；不重复底层通信实现正文。 | **通过（导航需小修）** | L74 已链互联/RDMA，L95 链 collectives 与 rank 进度；related_ids 有带宽基线，正文没有重复底层实现。C11 补普通带宽链接便于直接阅读，不改变本项边界判定。 |

## 整体结论

**T07-06 本次新建交付初审未通过，需修订后定向复核。** 已有可信的固定版本取证、正确的 DCP 案例和诚实的冲突/unknown 记录；但 MoE 权重所有权、CP/SP 语义、MindIE 字段层级、vLLM 实现条件和 IP 表述存在实质问题，选型比较、ROCm 限制及失败证据尚未完成验收。不得据本报告把正文改标为 reviewed，或将 source_checked 等同于硬件验证。

后续按 C01–C11 逐项提交修订与证据，由同一审阅角色定向复核；跨页冲突继续保留，未核组合继续 unknown。报告交付、问题关闭和真实环境验证分别记录，本报告没有关闭任何发现。

结构检查记录：基线及报告落盘后均执行 `PYTHONDONTWRITEBYTECODE=1 make check`，通过（111 content entries / 542 sources）。为遵守只新增报告的范围，使用完整输入副本 `/tmp/b27-review/validation-copy/` 执行同一 Makefile 的 `make build`（指定原工作区虚拟环境 Python），通过并生成临时 catalog；其中目标正文摘要与本轮受审 SHA-256 一致。未修改工作区 `build/`，未修改 `src/kb/`，未运行硬件测试。对审阅前 565 个既有文件逐一比较摘要，均未改变；本轮工具仅写指定报告，原有未提交正文及两处导航/量化修改保留。最终目录清点另见 `docs/research/batch-27-t07-04-codex-review.md` 新出现，本轮未创建或修改该文件，不将其计作本任务产出。

统计：发现 11 项（P1=0，P2=10，P3=1）；OPEN=11，CLOSED=0；acceptance 通过=1，部分满足未通过=4；整体=需修订后定向复核；真实硬件验证=0。

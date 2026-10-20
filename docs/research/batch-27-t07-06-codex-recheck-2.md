# Batch 27 · T07-06 第二轮定向复核

## 会话元数据

- 角色：AI 可靠性知识库批次审阅者；仅复核[第一轮报告](batch-27-t07-06-codex-recheck.md)尚开放的 C02、C03、C05、C06、C07、C09、C11、N01，以及本轮修订引入的问题。
- 实际执行模型：`gpt-6.1-sol`；实际推理档位：`xhigh`。
- 核验依据：`CODEX_THREAD_ID=01a15aff-2f93-78c3-9e24-282930a658de` 对应本地 CLI rollout；`session_meta.originator=codex_exec`、`source=exec`、`cli_version=0.163.0`；所查 `turn_context.model/effort` 只有上述一组值。本轮未调用其他审阅模型。
- cwd：`/Users/ywang2397/work/AI_reliability_knowledge_base`。
- 日期：2026-10-21（Asia/Shanghai）。
- 写入范围：只新增本报告；正文、registry、取证记录和历史报告均不修改。

| 受审输入 | SHA-256 |
|---|---|
| [当前正文](../../knowledge/07-inference/distributed-inference-layouts.md) | `ea1bcf1b8cfabefe9d903e0c1721b8a5729b494c193b0a8e6e087fab4697a3fc` |
| [当前来源登记表](../../sources/registry.yaml) | `19bf6fd6fbb59a319b9f604a4d50e53ff8a103b13e63b6d1506f9c3f3eb405f3` |
| [当前取证记录](batch-27-t07-06-sources.md) | `f71dfe2a9201f63e9cbba529dd941eea70a347c4cbd3b592d91c79411c5e0838` |
| [第一轮复核](batch-27-t07-06-codex-recheck.md) | `19ea25be0925f2f1378d2bafe28a0a260c73a538f2356b33746b08b7139fd59d` |

已从 README、写作指南开始读取仓库规范，并核对 content-outline 的归属边界。下文“正文 L…”指当前 156 行正文，“取证 L…”指当前 110 行取证记录。C01、C04、C08、C10 沿用第一轮 CLOSED，不重新展开；初审已通过维度及 acceptance 第 5 项同样沿用。

取证使用 `/tmp/b27-fetch/`、固定 vLLM 快照 `/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/` 及 MindIE 快照。初审记录的 16 个缓存文件完整摘要全部匹配。新补四文件的完整摘要如下，均与用户给出的前 16 位及 vLLM 快照逐字节相符：

| vLLM@b17039bc 文件 | SHA-256 |
|---|---|
| `vllm/platforms/rocm.py` | `b7fcec9a5263d8f9abeddba3b880fa2fe9e844a9ed5911d48942e35a4c9cf400` |
| `vllm/distributed/device_communicators/cuda_communicator.py` | `531b9f74e55f7f29437dfe8716b34ce83f4c2f5163d7f9575a87164428a47433` |
| `vllm/utils/nccl.py` | `574c956318442918b6852581a8affb39a170bd547f440241350f9adf08020d70` |
| `docs/getting_started/installation/gpu.rocm.inc.md` | `3f0c7129c7e0834745751f161feda79dada7851a2cd6b91b41f4794645c0db95` |

另为核对 C09 的调用桥接，读取同快照 `pynccl.py`（`2194624b032558afb24b97301813ebee49f83afe17495840eb56953f9820a71b`）、`pynccl_wrapper.py`（`bbbedf8b182a50bae44e43e26c9c029733c910126fcaeab739f11e76203e024d`）。尝试重取四个固定 raw URL：网页工具成功打开 cuda_communicator.py，其余三个返回 cache miss；本地网络重取均因 DNS 解析失败而未取得新副本。因此摘要结论来自已有原文件与固定快照比对，不声称四文件已全部在线重取。行号取原文件；registry 同时核对物理文本与 `yaml.safe_load` 后的有效值。未启动引擎或执行通信、故障注入及硬件验证。

## 逐项判定

### C02 · CLOSED

正文 L147 已增加到[训练并行与状态](../../knowledge/06-training/parallelism-and-state.md)的普通 Markdown 链接，目标存在，其中序列维并行说明的是激活/部分 buffer 的分布。结合已经通过的 MindIE KV SP、CP ring 与 vLLM DCP 分述，满足第一轮只剩导航的关闭条件。

### C03 · CLOSED

registry L536 的 `src.vllm.inference-v0-14.notes` 解析值现已明确区分字段说明和实际赋值：乘入 PCP，external_launcher 再乘 DP；简式仅适用 PCP=1 且非 external launcher。与正文 L75、取证 L106 一致，符合 [parallel.py L539–547](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L539-L547)；[L351–354](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L351-L354)的属性仍为实际 world_size 乘 DP。PCP 开发中和特殊分支完整语义 unknown 均保留，没有新增部署能力声明。

### C05 · CLOSED（配置层级及差异归属；行级链接残项归 C11）

正文 L120 已撤回“同页不一致”，如实记为两页差异：[tensor_parallel.md L17–34](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/tensor_parallel.md#L17-L34)参数表和 [L75–80](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/tensor_parallel.md#L75-L80)示例都有 parallel_options；[optimization_and_tuning.md L70–85](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/optimization_and_tuning.md#L70-L85)示例将两项直挂 deepseekv2。取证 L107 明确更正初审修订轮旧记录，未追改历史报告；L156 继续保留解析实现 unknown。其他字段层级及 MoE 乘积等式沿用已通过部分。正文的 tensor_parallel 链接尚无行级目标，仅在 C11 计数。

### C06 · CLOSED

registry L536 的有效 notes 已同步“指南概述”与 [parallel.py L590–631](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/config/parallel.py#L590-L631)实现条件：未指定且 world_size>1 时从 mp 起步，CUDA nnodes>1、卡数不足报错及后续 DP Ray/placement group 分支均有记录，并要求记录最终生效后端。与正文 L105/L130/L146、取证 L106 一致。分支先后以固定实现为准，不能将后列 Ray 条件视作覆盖前面已经命中的分支。

### C07 · CLOSED

registry L536 的有效 notes 已改为每节点设自身可达地址、各节点值不同，并与该节点 Ray 一致；保留 ray status/list nodes 复核。与正文 L131、取证 L106 及 [distributed_troubleshooting.md L11](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/serving/distributed_troubleshooting.md#L11)一致，原歧义已消除。

### C09 · 仍开放（补证方向正确，所选路径的条件尚未闭环）

正文 L112、取证 L108 和 registry L536 新增入口均真实存在：[rocm.py L161–169](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/platforms/rocm.py#L161-L169)固定平台字段，[L508–512](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/platforms/rocm.py#L508-L512)选择 CudaCommunicator；[all_reduce L126–174](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/cuda_communicator.py#L126-L174)的分支顺序也与正文一致。不能再将本项描述成完全没有 ROCm 布局证据。

但第一轮明确要求列出硬件/依赖及实现分支条件、继续追清至少一条通信路径。本轮仍只列候选路径，以“各层仍以条件分支为准”概括，缺少以下有限范围的落实：

1. **库名选择不等于实际加载及命中。** [utils/nccl.py L17–35](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/utils/nccl.py#L17-L35)只返回库名；无覆盖项时才按 torch 构建选默认值。实际桥接是 [CudaCommunicator L56–63](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/cuda_communicator.py#L56-L63)构造 PyNcclCommunicator、[pynccl.py L90–105](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/pynccl.py#L90-L105)检查禁用项/加载失败，再由 [pynccl_wrapper.py L311–318](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/pynccl_wrapper.py#L311-L318)调用 find_nccl_library 和 ctypes.CDLL。现正文及 notes 把库名辅助函数直接称为“实际加载”，没有落实这些启用/失败边界。
2. **ROCm 不会无条件走完整候选串。** 同文件 [L65–90](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/cuda_communicator.py#L65-L90)中，SymmMemCommunicator 初始化还要求 is_cuda()；custom/quick 的初始化受 use_custom_allreduce、world_size 和平台分支约束。正文只转述 MI3* 注释及 all_reduce 顺序，没有给所选基线路径的前提，也不能由此认定实际 collective 一律经 RCCL。
3. **所选布局的硬件与依赖边界未列出。** 同 commit 安装页已有 [L3–14](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L3-L14)的 GPU 架构、ROCm/torch 文档要求及不同架构例外；当前段没有把其中适用范围与所选单节点 Dense TP 联系起来。该安装声明本身也不能升级为本库实测配套。

最小修订仍可只选 pynccl/RCCL 一条条件路径：补上述桥接，说明 HIP 构建、库覆盖项、pynccl 未禁用且初始化成功、前序优化路径是否命中，以及所选硬件/依赖的文档边界；把“默认库名选择”“满足条件可走的实现路径”“现场实际命中”分开。其他分支不必全部展开。同步正文、取证与 notes 后再定向复核；多机、EP/all2all、DCP 和 RCCL 传输判据继续 unknown，不要求执行硬件实验。

### C11 · 仍开放（主要修复成立，仅余 local TP 行级目标）

已满足：正文 L116 的 CP 实际 URL 已另指 [supported_features.md L31](https://github.com/vllm-project/vllm-ascend/blob/52d4acfa51fb868823d1070b81cbd2d97e9e4696/docs/source/user_guide/support_matrix/supported_features.md#L31)；L122 另补 expert_parallel.md L25 和 context_parallel.md L32，分别准确覆盖双机交换机与切分仅 2。registry L553–556 已用块标量，解析后的 `src.ascend.vllm-ascend-v0-14-0rc1.notes` 含完整 issue #1608、T07-06 及 Tensor/Pipeline/Expert/Data/Context Parallel 五项，不再被注释截断。Batch 21 的 `src.ceph.test-scrub-repair-v19.2.7.notes` 解析值也完整保留“tracker #8914 未打开”；此处只确认序列化修复，不扩展为该批技术复审。

残项：正文 L120 的 tensor_parallel.md 仍为整页 URL，没有第一轮要求的参数表及示例行级目标；“L77 起”只是正文文字。optimization_and_tuning.md 已有 L70–85 目标。最小修订是将前者补为本报告 C05 所列 `#L17-L34`、`#L75-L80`，不需重写已经纠正的两页差异。取证 L110 的“互链”成立，但尚不能据此确认行级定位全部完成。本项不再保留 YAML 截断或那两处已修约束作为反对理由。

### N01 · CLOSED

正文 L112 与取证 L109 已把 AITER 的选择自行构建指定 branch/commit，与 MORI 的 EP/PD 用途分开；AITER 的布局依赖和可省略条件明确 unknown。与 [gpu.rocm.inc.md L87–100](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L87-L100)及 [L103–115](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L103-L115)一致；registry 的有效 notes 也分开陈述。这里的“可选自建”限于自行构建这项选择，不建立 AITER 在所有布局均可省略的结论。MORI 安装命令中的 gfx942;gfx950 仅为该步骤口径，不视为完整支持矩阵。

## 新问题

### N02 · P3 · 新增安装行级链接未覆盖同句前三项安装主张

- **位置**：正文 L112 的“安装口径（同 commit 文档 gpu.rocm.inc.md L87–115）”及其后无预编译 wheel、docker 推荐、ROCm Triton 固定 commit 三项。
- **问题与依据**：新 URL 的实际目标 L87–115 只覆盖 AITER/MORI。前三项主张本身有同文件支持，但位置分别是 [L3–6](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L3-L6)（docker 推荐）、[L22–24](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L22-L24)（无预编译 ROCm wheel）、[L47–64](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L47-L64)（Triton 安装及固定提交）。不能用同文件后段的精确链接代替这些位置。
- **关闭条件**：在相应主张旁分别补上述准确目标，保留 L87–115 用于 AITER/MORI。无需新增来源 ID 或改变安装结论。本项只计定位问题，与 C09 所选布局路径的证据缺口分开。

本轮没有其他独立、已证实的新问题。C09 的调用桥接和条件缺口计入原 ID，未重复新增编号；历史取证段的旧表述由 L103–110 明示更正，不将历史记录要求改写为当前结论。

## 整体结论

**本轮关闭 C02、C03、C05、C06、C07 与 N01；C09、C11 仍开放，新增 N02（P3）。T07-06 尚不能声明审阅通过。** C09 还需把所选 ROCm 路径的实现条件和硬件/依赖边界落实；C11 和 N02 均为有限的行级定位修订。C01、C04、C08、C10 继续 CLOSED，初审其他已通过部分沿用，不重新扩大验收范围。

ROCm 新文件和 registry 修复已提供有效进展；其余组合 unknown 及正文 draft/source_checked 状态继续成立。来源核对与结构检查不建立实际后端命中、平台兼容性或硬件验证。

结构校验：`PYTHONDONTWRITEBYTECODE=1 make check` 通过（111 content entries / 542 sources）。为遵守只新增报告的范围，在 `/tmp/b27-recheck-2/validation-copy/` 的完整输入副本中使用原工作区虚拟环境 Python 执行 `make build`，通过并生成临时 catalog；原工作区 build 文件未改。未修改 src/kb/，未新增或运行代码测试。以上检查不验证远程链接或技术结论。

写入范围核对：开工记录的 574 个既有文件摘要均未改变，三份受审输入与第一轮报告仍为头部摘要。本轮工具只新增本报告；收尾另观察到 `docs/research/batch-27-t07-04-codex-recheck-2.md` 新出现，本轮未创建或修改该文件，不计为本任务产出。

统计：原 C01–C11 共 11 项，CLOSED=9（沿用4＋本轮5），仍开放=2（C09/C11）；上一轮 N01=CLOSED；本轮新增=1（N02，P1=0，P2=0，P3=1，OPEN=1）；累计已编号=13，CLOSED=10，OPEN=3；本轮复核8项中关闭6项、仍开放2项；整体=未通过，需修订后定向复核；真实硬件验证=0。

# Batch 27 · T07-06 第三轮定向复核

## 会话元数据

- 角色：AI 可靠性知识库批次审阅者；仅核对[第二轮复核](batch-27-t07-06-codex-recheck-2.md)尚开放的 C09、C11、N02，以及本轮修订是否引入新问题。其余 CLOSED 项沿用。
- 实际执行模型：`gpt-6.1-sol`；实际推理档位：`xhigh`。
- 核验依据：`CODEX_THREAD_ID=01a15b04-7cd9-71c0-8832-1b74cefa2675` 对应本地 CLI rollout；`session_meta.originator=codex_exec`、`source=exec`、`cli_version=0.163.0`；所查 `turn_context.model/effort` 只有上述一组值。本轮未调用其他审阅模型。
- cwd：`/Users/ywang2397/work/AI_reliability_knowledge_base`。
- 日期：2026-10-21（Asia/Shanghai）。
- 写入范围：只新增本报告；正文、registry、取证记录和历史报告均不修改。

| 受审输入 | SHA-256 |
|---|---|
| [当前正文](../../knowledge/07-inference/distributed-inference-layouts.md) | `64babd5f6de874b7f7cadb37a02fade38e65e16e492bee3bef3e98ae05bac77b` |
| [当前来源登记表](../../sources/registry.yaml) | `5b5dd30a8fe1747a68115588f6e27a7a90b39aa1f0defcb925817c04bddf1715` |
| [当前取证记录](batch-27-t07-06-sources.md) | `444d386770384c4478b47851edd414732c4d070ec7451b5cb855c7b20a353b36` |
| [第二轮复核](batch-27-t07-06-codex-recheck-2.md) | `79b57b116870c0c0171070953a3cd42230b804e95c46d27c1d5dab78a9a02b2f` |

已读取 README、写作指南和 content-outline。下文“正文 L…”指当前 156 行正文，“取证 L…”指当前 116 行取证记录。与第二轮校验副本比对，正文变动限 L112、L120；取证新增 L112–116；registry 解析后的条目差异限 `src.vllm.inference-v0-14.notes`。不重新展开其他 CLOSED 项或已通过验收维度。

方法为原文件核对：读取 `/tmp/b27-fetch/` 原文件，并与固定 vLLM 快照 `/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/` 比对。以下六个文件逐字节一致；新增两文件的摘要前 16 位与用户给定值相符。

| vLLM@b17039bc 文件 | SHA-256 |
|---|---|
| `vllm/platforms/rocm.py` | `b7fcec9a5263d8f9abeddba3b880fa2fe9e844a9ed5911d48942e35a4c9cf400` |
| `vllm/distributed/device_communicators/cuda_communicator.py` | `531b9f74e55f7f29437dfe8716b34ce83f4c2f5163d7f9575a87164428a47433` |
| `vllm/utils/nccl.py` | `574c956318442918b6852581a8affb39a170bd547f440241350f9adf08020d70` |
| `vllm/distributed/device_communicators/pynccl.py` | `2194624b032558afb24b97301813ebee49f83afe17495840eb56953f9820a71b` |
| `vllm/distributed/device_communicators/pynccl_wrapper.py` | `bbbedf8b182a50bae44e43e26c9c029733c910126fcaeab739f11e76203e024d` |
| `docs/getting_started/installation/gpu.rocm.inc.md` | `3f0c7129c7e0834745751f161feda79dada7851a2cd6b91b41f4794645c0db95` |

MindIE 的 `tensor_parallel.md`（`d121df6eca46276bbb69aa0d419a2b639f29a8c97187e7da01e385455cc20147`）及 `optimization_and_tuning.md`（`0c348668366760a0fa2b39d48cdd7d605b0b3ae305a74f224a09252e92b0c72a`）也与本地原快照逐字节一致。尝试在线打开固定 commit 的 pynccl、wrapper、ROCm 安装页和 tensor_parallel 原文件，网页工具均返回 cache miss；本地重取 pynccl 又遇 DNS 解析失败，未取得新副本。因此本轮不声称在线重取成功。所有行号取原文件坐标；registry 同时核对物理文本与 `yaml.safe_load` 后的有效 notes。未启动引擎、执行通信或开展硬件验证。

## 逐项判定

### C09 · 仍开放（P2；桥接和主要边界已补，当前结论仍需收紧）

本轮实质补证成立，不再沿用“缺少调用桥接、初始化门控和安装硬件边界”的整组反对理由：

- **调用桥接真实存在**：正文 L112、取证 L114 与 registry L536 的有效 notes 均已补 [CudaCommunicator L56–63](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/cuda_communicator.py#L56-L63) → [pynccl.py L90–105](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/pynccl.py#L90-L105) → [pynccl_wrapper.py L311–318](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/pynccl_wrapper.py#L311-L318)。world_size>1 时构造 PyNcclCommunicator，禁用项及加载异常会令其 disabled，wrapper 按路径缓存或用 ctypes.CDLL 加载。
- **主要门控与三层区分已补**：[cuda_communicator.py L65–90](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/cuda_communicator.py#L65-L90)支持 SymmMemCommunicator 还要求 is_cuda()，ROCm 不构造该对象；custom/quick 构造受 use_custom_allreduce 与 world_size>1 门控。MI300 系列被如实标成 ROCm 分支注释，没有升级为实测支持。新增“默认库名选择／满足条件可走的实现路径／现场实际命中须日志确认”也已进入正文及有效 notes。
- **硬件/依赖来源已补**：[gpu.rocm.inc.md L3–14](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L3-L14)支持 ROCm 6.3+、torch 2.8.0+ 以及列出的 GPU 架构和例外要求；其中 Ryzen AI 原文范围为 MAX / AI 300 Series（gfx1151/1150）。正文把这组资料作为所选单节点 Dense TP 基线的文档边界，并保留“非本库实测配套”。多机、EP/all2all、DCP 与 RCCL 传输判据仍 unknown，未据安装页认定这些组合可用。

**尚未关闭的有限残项是：新增限定没有消除当前正文与 notes 中已有的无条件结论，且“库加载成功”仍被写成路径可用的充分条件。**

1. 正文 L112 前半仍称“torch 为 HIP 构建时实际加载 librccl.so.1”“即 ROCm 上……实际通信库是 RCCL”；registry L536 的当前有效 notes 仍称 find_nccl_library 在 HIP 时“加载”该库、“HIP 下实际库为 RCCL”。这些不是只供追溯的历史报告，而是当前正文及当前来源摘要。[utils/nccl.py L17–35](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/utils/nccl.py#L17-L35)实际只返回库名，且覆盖项优先；[pynccl.py L90–102](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/pynccl.py#L90-L102)允许在真正加载前就禁用或因加载失败返回。后半虽已正确区分三层，前面的强断言仍与该限定冲突。
2. 正文新增“上述链路在 world_size>1、未禁用、库加载成功时可用”。[pynccl.py L104–147](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/pynccl.py#L104-L147)显示 available/disabled 赋值之后，还要取得 unique ID、同步、执行 ncclCommInitRank 及 warmup all_reduce/stream synchronize；库加载成功本身不保证构造成功。进入普通 pynccl all_reduce 还以[前序优化分支未返回](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/cuda_communicator.py#L126-L174)为前提。这里不能将早期加载检查写成完整可用条件。

**最小关闭条件**：将正文与有效 notes 中旧的“实际加载／实际库”断言统一改成“无覆盖项时，HIP 构建默认返回 librccl.so.1”；描述实际加载时指向 wrapper，并以 PyNcclCommunicator 初始化成功为前提；所选普通 pynccl/RCCL all-reduce 路径还需前序优化路径未返回。保留现场实际命中须证据确认，更新最新取证结论即可，不要求重写历史修订日志或开展硬件实验。这些仍属于第二轮 C09 已要求的默认选择、初始化成功与分支命中边界，不新增发现编号。

### C11 · CLOSED

正文 L120 的两个实际 URL 现分别带 `#L17-L34` 与 `#L75-L80`。原文件核对确认：[参数表 L17–34](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/tensor_parallel.md#L17-L34)同时覆盖两项 local TP 的 deepseekv2/parallel_options 层级；[服务化示例 L75–80](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/feature/tensor_parallel.md#L75-L80)包含相同层级及两个字段。与已正确保留的 optimization_and_tuning 两页差异一致，取证 L116 也如实记录。第二轮仅剩的行级定位残项关闭；其余 CLOSED 部分沿用。

### N02 · CLOSED

正文 L112 后半已把三项安装主张分别与正确 URL 配对：[docker 推荐 L3–6](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L3-L6)、[无预编译 ROCm wheel L22–24](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L22-L24)、[ROCm Triton 安装 L47–64](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/docs/getting_started/installation/gpu.rocm.inc.md#L47-L64)。最后一处的 L57 确为固定提交 f9e5bf54。取证 L115 与 registry 有效 notes 同步；L87–115 继续支持 AITER/MORI。前三项虽在该长段中重复出现，现已有各自准确的行级支持，不再保留第二轮“只有 L87–115 目标”的反对理由。本项只判断定位，安装步骤未执行。

## 新问题

本轮未发现独立、已证实的新问题。C09 的残留强断言及初始化条件不完整沿用原 ID，不重复计入 N03。C11、N02 的定位修订未改变已通过的技术主张；未扩大复审其他 CLOSED 项。

## 整体结论

**本轮关闭 C11、N02；C09 仍开放，T07-06 尚不能声明审阅通过。** C09 的证据桥接、主要门控和文档边界已有有效进展，剩余修订限于统一当前结论的条件：默认库名、成功初始化、所选分支命中分别表述。其余 C01–C08、C10、N01 沿用 CLOSED，不要求重新补证。

正文保持 draft/source_checked；来源核对和结构校验不建立实际通信路径命中、平台兼容性或真实硬件验证。

结构校验：`PYTHONDONTWRITEBYTECODE=1 make check` 通过（111 content entries / 542 sources）。为遵守只新增报告的范围，在 `/tmp/b27-recheck-3/validation-copy/` 输入副本中使用原工作区虚拟环境 Python 执行 `make build`，通过并生成临时 catalog；原工作区 build 未修改。临时副本首次未复制既有 build，因 first-fill-status 对 catalog 的本地链接缺失而失败，补齐该输入后通过。未修改 src/kb/，未新增或运行代码测试。

写入范围核对：开工记录的 576 个既有文件摘要均未改变，三份受审输入与第二轮报告仍为头部摘要。本轮工具只新增本报告；收尾另观察到 `docs/research/batch-27-t07-04-codex-recheck-3.md` 新出现，本轮未创建或修改该文件，不计为本任务产出。

统计：原 C01–C11 共11项，CLOSED=10（沿用9＋本轮1），OPEN=1（C09，P2）；既有新增项 N01/N02 均CLOSED（N01沿用，N02本轮关闭）；本轮复核3项，关闭2项、仍开放1项；本轮新增=0（P1=0，P2=0，P3=0）；累计已编号=13，CLOSED=12，OPEN=1；整体=未通过，需修订后定向复核；真实硬件验证=0。

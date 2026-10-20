# Batch 27 · T07-06 第四轮定向复核

## 会话元数据

- 角色：AI 可靠性知识库批次审阅者；仅核对[第三轮复核](batch-27-t07-06-codex-recheck-3.md)仍开放的 C09 是否关闭，以及本轮修订是否引入新问题。其余 CLOSED 项沿用。
- 实际执行模型：`gpt-6.1-sol`；实际推理档位：`xhigh`。
- 核验依据：`CODEX_THREAD_ID=01a15b08-406f-75b0-a69c-ca00b1eec3c1` 对应本地 CLI rollout；`session_meta.originator=codex_exec`、`source=exec`、`cli_version=0.163.0`；所查 `turn_context.model/effort` 只有上述一组值。本轮未调用其他审阅模型。
- cwd：`/Users/ywang2397/work/AI_reliability_knowledge_base`。
- 日期：2026-10-21（Asia/Shanghai）。
- 写入范围：只新增本报告。

| 受审输入 | SHA-256 |
|---|---|
| [当前正文](../../knowledge/07-inference/distributed-inference-layouts.md) | `4fd0c0e0b6a70c2d1970e1bfdf361f6073d55cb1a1d2e23d70ca633235810198` |
| [当前来源登记表](../../sources/registry.yaml) | `7337d2fcc8f4aaf1bd272e0c0a0b8c881f3e4459e8b95b0ebf9961af6041e73a` |
| [当前取证记录](batch-27-t07-06-sources.md) | `6cd9f8ce8a409ec023a735292370007595318b5ab122b01465e670ce949ef86d` |
| [第三轮复核](batch-27-t07-06-codex-recheck-3.md) | `249c3172940586ea0a9b1d4f8e853a09a24f4760fd1927b90fb2422333dc799c` |

已读取 README、写作指南和 content-outline。下文“正文 L…”指当前 156 行正文，“取证 L…”指当前 120 行取证记录。第三轮校验副本的三份输入摘要均与第三轮报告头部一致；与该副本比对，当前正文只改 L112，取证只新增 L117–120，registry 解析后的条目差异仅为 `src.vllm.inference-v0-14.notes`。本轮不重新展开其他 CLOSED 项。

方法为原文件核对：读取 `/tmp/b27-fetch/` 原文件，并与固定快照 `/tmp/vllm-b17039bccc17b94a2ea107272ad7bc93508708df/` 逐字节比对。下列四份文件均一致，摘要也与第三轮记录一致；平台文件与安装页的原文件摘要及逐字节一致性另已核对，既有判定沿用。

| vLLM@b17039bc 文件 | SHA-256 |
|---|---|
| `vllm/utils/nccl.py` | `574c956318442918b6852581a8affb39a170bd547f440241350f9adf08020d70` |
| `vllm/distributed/device_communicators/pynccl.py` | `2194624b032558afb24b97301813ebee49f83afe17495840eb56953f9820a71b` |
| `vllm/distributed/device_communicators/pynccl_wrapper.py` | `bbbedf8b182a50bae44e43e26c9c029733c910126fcaeab739f11e76203e024d` |
| `vllm/distributed/device_communicators/cuda_communicator.py` | `531b9f74e55f7f29437dfe8716b34ce83f4c2f5163d7f9575a87164428a47433` |

尝试在线打开固定 commit 的 utils/nccl.py 与 pynccl.py，网页工具均返回 cache miss，未取得新副本；本轮结论依据上述本地原文件，不声称在线重取成功。所有源码行号均取原文件坐标；registry 同时核对物理文本与 `yaml.safe_load` 后的有效 notes。未启动引擎、执行通信或开展硬件验证。

## C09 判定

**C09 · CLOSED（原 P2）。第三轮保留的两项残留理由均已消除，正文、有效 notes 与最新修订记录一致。**

1. **库名选择与实际加载已区分。** 正文 L112 已将“库加载层”改为“库名选择层”，明确覆盖项优先、无覆盖项时 HIP 构建默认返回 `librccl.so.1`，并限定为库名选择。原文件 [utils/nccl.py L17–35](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/utils/nccl.py#L17-L35)确实先检查覆盖项，再按 torch 后端选择库名并返回；该函数不执行加载。实际加载仍准确指向 [pynccl_wrapper.py L311–318](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/pynccl_wrapper.py#L311-L318)：按路径复用缓存，未缓存时经 `ctypes.CDLL` 加载。当前正文及 registry L536 的有效 notes 已消除第三轮指出的“HIP 时实际加载／实际库为 RCCL”无条件断言。
2. **完整初始化已成为实现路径的前提。** 正文 L112 现在明确“库加载成功本身不充分”，以 PyNcclCommunicator 初始化成功为前提。[pynccl.py L90–105](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/pynccl.py#L90-L105)保留单 rank、显式禁用及加载异常的提前返回；[L104–147](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/pynccl.py#L104-L147)显示 available/disabled 赋值后仍需 unique ID 的取得与广播同步、设备绑定、ncclCommInitRank、warmup all_reduce 及 stream synchronize。修订覆盖了第三轮要求的后续初始化阶段，不再把加载成功或早期标志赋值当作完整初始化成功。
3. **普通 pynccl all_reduce 的分支条件已补齐。** 正文 L112 明确须前序优化分支未返回，且继续区分“默认库名选择／满足条件可走的实现路径／现场实际命中”。[cuda_communicator.py L126–174](https://github.com/vllm-project/vllm/blob/b17039bccc17b94a2ea107272ad7bc93508708df/vllm/distributed/device_communicators/cuda_communicator.py#L126-L174)确认顺序：symmetric-mem NCCL、quick、custom、symm-mem 均可能提前返回；之后才检查 pynccl 对象及 disabled 状态并调用普通 pynccl all_reduce，禁用或返回空结果时有 PyTorch 兜底。因此当前表述只说明有条件的实现路径，没有将初始化成功直接等同于某次请求的实际命中。
4. **当前有效摘要与修订记录已同步。** registry L536 解析后的 `src.vllm.inference-v0-14.notes` 同时保留覆盖优先、仅库名选择、初始化成功、available 后仍有初始化工作、普通 pynccl 前序分支未返回和现场命中须日志确认等限定，内容未被 YAML 注释截断。取证 L118–120 新增“第三轮复核修订”节，记录相同边界。此前修订节按历史记录保留，不作为当前结论中的无条件加载断言。

以上满足第三轮 C09 的最小关闭条件。既有的单节点 Dense TP 基线范围及其他 ROCm 组合 unknown 沿用；本轮关闭的是来源与表述问题，不增加平台兼容或现场通信路径已验证的结论。

## 新问题

本轮未发现独立、已证实的新问题。已核对的修订只收紧 C09 的库名、初始化与分支条件，没有改变其他 CLOSED 项的技术主张或引用定位；不新增 N03。C01–C08、C10、C11、N01、N02 均沿用第三轮 CLOSED。

## 整体结论

**本轮关闭 C09；累计 13 项已编号发现全部 CLOSED，T07-06 在原审阅范围内通过。** 正文仍为 `draft / source_checked`；本结论不建立实际路径命中、部署组合兼容性或真实硬件验证。

结构校验：`PYTHONDONTWRITEBYTECODE=1 make check` 通过（111 content entries / 542 sources）。为遵守只新增报告的范围，在 `/tmp/b27-recheck-4/validation-copy/` 复制当前输入及既有 build 后，使用工作区虚拟环境 Python 执行 `make build`，通过并生成临时 catalog；原工作区 build 未修改。这些检查仅验证结构与本地文件链接，不验证技术正确性或远程内容。未修改 src/kb/，未新增或运行代码测试。

写入范围核对：开工快照记录的 573 个既有文件（排除 .git、.venv 与运行缓存）摘要均未改变，没有删除文件；唯一新增文件为本报告。三份受审输入与第三轮报告仍为头部摘要，历史判定记录未修改。

统计：原 C01–C11 共11项，CLOSED=11（沿用10＋本轮1），OPEN=0；既有新增项 N01/N02 均CLOSED（沿用）；本轮复核1项，关闭1项、仍开放0项；本轮新增=0（P1=0，P2=0，P3=0）；累计已编号=13，CLOSED=13，OPEN=0；整体=原审阅范围内通过；真实硬件验证=0。

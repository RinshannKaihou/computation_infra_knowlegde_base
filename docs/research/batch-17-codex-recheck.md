# 第十七批第一次定向复核记录

**最新进展（2026-10-09）：[第六次定向复核](batch-17-codex-sixth-recheck.md)已完成，第五次三项修订均通过，无新增修改项；累加精度与固定实现关联仍缺证，累计 12 项 CLOSED、1 项 P2 OPEN（C08）。** 已通过项不重开，各阶段输入、判定保留；以下为第一次复核记录，Batch 17 仍暂不通过。

复核日期：2026-10-09（Asia/Shanghai）。**结论：暂不通过。B17-C01–C13 中 8 项 CLOSED，5 项 OPEN（均为 P2）：C01、C03、C08、C10、C11。** 修订已推进多数技术主张，但“提交修订”与“满足关闭条件”分别判定；不以表格行数或结构检查代替验收。

依据：[初审与关闭条件](batch-17-codex-review.md)、[作者修订记录](batch-17-review-fixes.md)、[路线图](../full-coverage-roadmap.md)、[T02-08–T02-11 验收清单](../../plans/full-coverage-backlog.yaml)、[写作指南第 7 节](../authoring-guide.md#7-批次审阅约定)。

执行者：初审同一 Codex 主助手，与本批正文编写者分开；未派发子代理，未改写知识正文或四份作者研究记录。用户约定配置为 `gpt-6.1-sol / xhigh`；沿用初审披露：本会话没有可独立核验的实际模型/effort 运行标识，不将约定写成已经确认的执行元数据。

## 本轮范围与证据

重新读取四篇修订正文、四份研究记录及末尾修订附录、修订记录、来源登记与本批验收条件。对照初审关闭条件检查相关代码段和官方页面；未扩展为全部软件栈或旧 Ascend allocator/workspace 的重新验收。

- 固定源码：重读初审同日取得的 PyTorch `1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340` 中 allocator、配置解析、cuBLAS workspace、memory API、Storage 方法生成、gradcheck 和 ScalarType 的相关原文件段落；TorchNPU `bc51ab84cc6f35c77aab1c59886e0ea43681a317` 中 CopyKernel、CachingHostAllocator、设备注册和 autocast 分支。沿用固定 raw 文件，不把本轮段落核对写成所有文件重新下载或运行。
- 新增文件：通过原登记精确 raw URL 取得并完整读取 `torch_npu/npu/_format.py`（38 行、15 个 Format 成员）；验证其枚举与包装逻辑，不据此证明格式转换或算子精度支持。
- 本轮实开 CUDA 12.8 Memory Management / Stream Ordered Allocator、PyTorch 2.6 Reproducibility / Numerical accuracy / torch.library / Tensor Attributes。CANN 1807 实开静态页；AOL 静态页本轮网页工具失败，重读初审同日从相同精确地址取得的正文，保留此取证方式限制。
- 未重新执行或下载 Batch 16 的 `test_cache_guard`；其既有证据只能支持该上游测试的已审阅范围，不能证明 TorchNPU 编译缓存全部能力。

修订复核输入 SHA-256（本轮写报告前固定）：

| 输入 | SHA-256 |
|---|---|
| [框架后端正文](../../knowledge/02-software-stack/framework-backend-adaptation.md) | `c706b2a1862033a544b4730c435d467648100ec4668e4cfcfcc8cdd5c007b6ec` |
| [GPU 内存正文](../../knowledge/02-software-stack/gpu-memory-oom-evidence.md) | `3ef38db50c69c66346e68ccbdb2ccd0af9ab97b94cb8d83a624a8fc5bea39051` |
| [精度语义正文](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md) | `bff24297f3d02a38ff2828205aa9c8ef9046b90675ee4d9c68b170374db34f5b` |
| [Ascend 内存正文](../../knowledge/02-software-stack/ascend-memory-oom-evidence.md) | `b1c3e6cfceb9625d109a93629ce13d2ffa8205d58f17e5f2efae58155b6c2869` |
| [框架研究记录](batch-17-framework-backend-sources.md) | `69a919bfaa80f47b489cdeadb4658c8a6bd41e4e8d28615d533f8ae44e03b546` |
| [GPU 研究记录](batch-17-gpu-memory-sources.md) | `10b2fa42fd4bc83a4fe51eaf72efc64f9b1ac67e9654038446ed6b78715c5e0b` |
| [精度研究记录](batch-17-dtype-precision-sources.md) | `856a24894ef6666e6723be7ed14dd96f450c35078ab155c25ee30483b10323f1` |
| [Ascend 研究记录](batch-17-ascend-transfer-sources.md) | `6e99c3a6a6e4c9e6e3e9e4d07556d90db0ff41a554bbab1d7e03859ebd2bb002` |
| [修订记录](batch-17-review-fixes.md) | `bfd1e68fe5288f3e88653246d7c83fba56442785b1458cf9f58b306a1182ae6e` |
| [来源登记](../../sources/registry.yaml)（332 项） | `d3eecbe4ea3f6bcee16153b45a94d3fae1518e1c18305f1e8037aaf078e4509d` |

领域索引未变化，SHA-256 `7e0cb816f3d1575f24b246eeee6a345baffe65812ae8f5fb483c0efa1eac6be0`。研究记录前段保留修订前取证，末尾附录是对应发现的修订说明；最新是否关闭以本报告为准，不将旧表中的错误表述重新采信为通过结论。

## 逐项判定

位置均为本轮输入的源文件行号，初审位置保留在原报告。

| 发现 | 优先级 | 状态 | 复核位置与依据 |
|---|---|---|---|
| B17-C01 | P2 | OPEN，部分修复 | GPU L50、L72–74、L120 已去重复求和；L27 摘要仍称独立账户，L117 把 graph reserved 说成 allocated 的子集，见下文 |
| B17-C02 | P2 | CLOSED | Ascend L139–145 已分管理/非管理、方向与条件接口，区分下发、阻塞、可读与复用；[CopyKernel L97–102](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/CopyKernel.cpp#L97-L102) 与 [host allocator L181–207](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/core/npu/CachingHostAllocator.cpp#L181-L207) 相符。关闭范围是原遗漏的显式 stream 等待分支；未验收完整调用链或实机阻塞时长 |
| B17-C03 | P2 | OPEN，部分修复 | GPU L66、L115 已补选项与真实 getter；来源登记却将该 getter 等同请求配置，见下文 |
| B17-C04 | P2 | CLOSED | GPU L82 按分配来源保留 CUDA 的可能同步及 async 例外，与 [CUDA 12.8 cudaFree Description](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__MEMORY.html) 相符，不再推成 CUDA 无同步保证 |
| B17-C05 | P2 | CLOSED | GPU L78 补 API 返回、新提交访问、已提交工作流序及实际释放的边界，并明确跨流依赖；符合 [CUDA 12.8 cudaFreeAsync / cudaMallocAsync](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-runtime-api/group__CUDART__MEMORY__POOLS.html) |
| B17-C06 | P2 | CLOSED | 精度 L99、L121–124 扩充控制项，两次不同先记观察，定位首差要求字节一致和可重复超差；符合 [Reproducibility 2.6](https://docs.pytorch.org/docs/2.6/notes/randomness.html)，不再直接判正常 |
| B17-C07 | P2 | CLOSED | 精度 L128 分拒绝输入、进一步验证、已证错误，预设残差/参考/阈值且明确待执行；[Numerical accuracy → Linear algebra](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html#linear-algebra-torch-linalg) 的风险声明未被改成已发生错误 |
| B17-C08 | P2 | OPEN，部分补证 | 精度 L86–93 新有限样板属实；转换与逐算子计算/累加精度仍未验收，元数据/登记也未同步，见下文 |
| B17-C09 | P2 | CLOSED | 框架 L67、L107 与精度 L91 将列表限定为 Storage 方法，AMP/tensor/算子支持独立取证；符合 [backend_registration.py L318–340](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/backend_registration.py#L318-L340) 和 [TorchNPU 调用 L203–205](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/__init__.py#L203-L205)。测试表中的失败类型另归 C10 |
| B17-C10 | P2 | OPEN，部分修复 | 框架 L59、L82、L96 已限定梯度测试义务并说明前提；L84–94 的九行表仍有方法/判据缺口与失败类型错误，见下文 |
| B17-C11 | P2 | OPEN，部分修复 | GPU L62、L96 的统计限制正确；L124 的 F2 重置/采样顺序和对象恢复仍不足，见下文 |
| B17-C12 | P3 | CLOSED | Ascend L127 改为八项，研究附录与登记更正一致；对照 [1807 静态原文](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_1807.html) 不补出第九项 |
| B17-C13 | P3 | CLOSED | 精度 L54 将十二种限定为页列摘要，明确实现枚举不同及存在/支持/覆盖分离；符合 [Tensor Attributes 2.6](https://docs.pytorch.org/docs/2.6/tensor_attributes.html#torch-dtype) 和 [ScalarType.h L60–91](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/core/ScalarType.h#L60-L91) |

关闭项表示对应文档错误或设计缺口在本轮限定范围内关闭，不代表运行环境兼容或实验通过。所有开放项沿用原 ID 和优先级，不另计为新增发现。

## 剩余发现与关闭条件

### B17-C01 — P2，OPEN：账户关系尚未贯穿元数据和记录表

已修复：用途分类不相加、workspace 经 caching allocator、graph pool 进入 aggregate、删除错误余量公式，并保留未知量。

残留位置：GPU L27 的 metadata summary 仍写“workspace 与外部库独立账户”，生成 catalog 与 Agent 摘要会继续传播旧口径；L117 将 `graph_pool_reserved` 写成“reserved/allocated 的子集”。graph pool 的保留量可以包含非活跃块，不能把整个保留池说成当前 allocated 的子集；其活跃块计入 allocated、其 runtime segment 计入 reserved 是两种统计关系。

证据：[CublasHandlePool.cpp L166–167](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/aten/src/ATen/cuda/CublasHandlePool.cpp#L166-L167)、[allocator L1443–1448](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L1443-L1448) 与 [L2775–2784](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L2775-L2784) 分别增加活跃和保留统计，不能合并成同一个子集关系。

关闭条件：摘要改为用途/allocator 可见性口径；记录表区分 graph 活跃量与保留量及采样/高水位窗口，只对相同统计类型声明子集关系。同步修订附录并构建后检查 catalog 实际 summary；维持并列不相加。

### B17-C03 — P2，OPEN：登记把 active backend 又写成请求配置

已修复：选项表含十项与两个选项名别名，移除不存在的 `_get_allocator_settings`；正文已区分 backend 查询与 env 请求快照。

残留位置：`sources/registry.yaml:3704` 的 `src.pytorch.torch-cuda-memory-source-v2.6.0` notes 将 `get_allocator_backend` 描述为返回 ALLOC_CONF 设定的 backend 字符串“即请求配置”。固定 [memory.py L925–934](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/cuda/memory.py#L925-L934) 明确描述 active allocator backend，并调用 C++ getter；它不是读取当前 env 快照的 Python 函数。正文 L115 与登记因此相互矛盾。

关闭条件：登记明确 getter 查询 active backend 的限定范围，env 单列请求配置；两者都不代表已取得全部选项的生效值。保持选项名别名与环境变量名区分，同步修订记录。无需为了关闭此项新增全配置 getter。

### B17-C08 — P2，OPEN：有限格式样板已核实，强制精度/转换子项未交齐

已补证：[固定 _format.py](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/_format.py) 的 L7–23 确为 15 成员，L29–38 包装 `get_npu_format`；autocast 的 bf16 分支也属固定实现事实。AOL 的未明示支持场景边界句可从取得的正文确认。这些证据不提供转换 API 的语义或具体算子的计算/累加精度。

残留位置：精度 L88、L93、L137 保留转换 API 与逐算子精度 unknown，作者正确保留其强制门；但 L37/L45 仍将 CANN 描述为未抽取正文/只返回壳，登记 `src.ascend.cann-82rc1alpha001-aol-index`（`sources/registry.yaml:3944`）的 revision/notes 也未记录已取得简介静态正文。正文“静态正文已取得”与元数据不一致，新增 _format.py 尚未在 verification notes 中说明本次有限核对范围。

证据：[T02-10 acceptance/source_discovery](../../plans/full-coverage-backlog.yaml)、[路线图材料门槛](../full-coverage-roadmap.md#批次执行与来源入口)、[AOL 接口简介](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/operatorlist_00001.html) 与固定格式文件。

关闭条件：补一个范围有限、版本明确的 Ascend 格式转换与算子计算精度样板，来源定位到官方正文及固定实现，单独列未取得的累加精度和算子/硬件限定；不能取得的必交子项继续 OPEN。同步 source_checked 的范围说明、AOL 登记与研究附录，区分已取得简介和仍未取得的支持表。未经用户明确调整，不撤销路线图必交范围。

### B17-C10 — P2，OPEN：逐能力表仍未提供足够的可判读对照

已修复：训练/推理与自定义/标准算子的梯度测试义务有所区分；double 默认精度、非可微点、重叠内存前提与 [gradcheck.py L1987–2004](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/autograd/gradcheck.py#L1987-L2004) 一致。

残留位置：框架 L82、L87–94、L96。

1. dtype 行 L89 的失败类型写成 Storage 未覆盖组合的 `NotImplementedError`；该固定实现对于 `unsupported_dtype` 的 TypedStorage 转移在 [backend_registration.py L281–289](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/utils/backend_registration.py#L281-L289) 抛 `RuntimeError`，不能与 dispatcher 未注册算子的 NotImplementedError 合并。其“有覆盖证据 = 通过”也将文档支持性与组合实际结果测试混为一个通过状态。
2. stream 行仅写“多 stream + event”，缺生产/消费先后、参考结果和有依赖/缺依赖对照；集合通信仅写“双设备最小集合通信”，缺 collective、rank 次序、输入/预期输出及无法判断条件。可以给待执行设计，不需要现场运行，但要能按定义实施和解释。
3. 表中未定义验收要求的性能对照（基线、相同负载与同步计时边界、比较指标），也未给标准算子训练分支的 forward/backward 数值对照；“覆盖证据”不能替代任务结果。L96 将非可微点/重叠输入一律改用同输入数值对照，则只检查 forward，不能验证本来需要的梯度，应先调整 gradcheck 输入或明确替代梯度方法与剩余 unknown。

证据：[T02-08 acceptance 第三项](../../plans/full-coverage-backlog.yaml) 要求最小测试、观察点、预期失败和完整性/性能对照；[torch.library Testing custom ops / Warning](https://docs.pytorch.org/docs/2.6/library.html#testing-custom-ops) 区分注册检查与梯度数学正确性，不能用 forward 接近替代后者。

关闭条件：修正 Storage 失败类型，分别标记文档支持性、方法适用性和实际结果；为尚为空泛的能力行提供一个固定最小输入及可定位方法、正反/无法判断条件，补性能对照的待执行定义。明确自定义有梯度算子、标准训练算子、无梯度推理与方法不适用时的替代验证，不把 forward 比较作为梯度验证通过。仍不虚构 TorchNPU 测试用例名或实验结果。

### B17-C11 — P2，OPEN：恢复窗口可在记录前被重置，存活状态未形成对照

已修复：F1 backend 使用独立进程、记录 OOM 对象与干净进程对照、分指标限制和四类解释；inactive_split 已改为提示，async/expandable 边界与固定实现相符。

残留位置：GPU L124 写“复跑前后分别重置 peak/accumulated 并对比 reserved.peak 与 num_ooms 增量”，没有规定在后一次 reset 之前保存终点读数。按此顺序直接 reset 后读取，会丢失本窗口的 OOM 计数和峰值；记录存活张量/失败引用后只执行 empty_cache，也没有定义哪些对象保留作为基线、哪些释放，以及何时同步和采样。“复跑后 allocated 不回落”缺比较阶段和对象基线，不能可靠地区分正常保留对象、warmup 缓存与泄漏候选。

证据：[memory.py L334–370](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/cuda/memory.py#L334-L370) 定义两种 reset；[allocator L1637–1679](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/cuda/CUDACachingAllocator.cpp#L1637-L1679) 将 num_ooms 等历史计数归零并重置峰值。reset 不替代释放业务对象或完成设备工作。

关闭条件：把 F0/F2 写成有序窗口：保存失败现场与对象基线 → 明确对象清理/保留与同步完成 → 窗口开始重置并保存起点 → 固定负载 → 同步并在再次 reset 前保存终点/峰值 → 比较同阶段基线，最后才为下一窗口重置。也可不重置累计值而比较明确的前后增量，须选定一种口径。区分初始化/warmup/steady/recovery 窗口，保留干净进程对照；同步研究附录，保持待执行。

## 任务与批次状态

| 任务 | 本轮判定 | 未完成范围 |
|---|---|---|
| T02-08 | 未通过 | C10 的测试输入、失败类型、梯度及性能对照 |
| T02-09 | 未通过 | C01/C03 的一致性、C11 的有序统计/恢复设计 |
| T02-10 | 未通过 | C08 的 Ascend 强制样板与元数据同步 |
| T02-11 | 原 C02/C12 关闭；整任务不作完成声明 | 原来源/接口未知边界仍保留；尤其 0088/0089 作者正文尚只记页名，旧 allocator/workspace 非本轮全量重核 |

T02-11 的 acceptance 第三项要求待执行验证设计；本轮未执行硬件本身不是该设计项的失败依据。接口证据是否齐全与实机是否执行仍分别记录。C08 未关闭，不解锁要求 T02-10 完成的后续依赖；本轮不把任何 backlog 任务改为 done，不调整主题覆盖状态。

## 检查与限制

本轮独立执行 `make check` 与 `make build`：均 PASS，83 content entries / 332 sources，生成 `build/catalog.json` 与 `build/catalog.md`。只验证结构和本地引用，不证明上述技术问题已解决、远程内容有效或硬件通过。修订记录末尾“待运行”是作者提交时状态，最新结构结果以本报告为准。

未修改 `src/kb/`，未新增代码测试；未安装 wheel、执行 GPU/NPU/集群代码、复现 OOM、测量流等待、跑数值或性能实验。没有把未知配套、发行包、TorchNPU 条件接口存在性、所有 dtype/format 组合或历史来源的许可提升为已验证。五项开放问题修订后仍需同一审阅者定向复核；`draft / source_checked` 保持限定范围，不提升到硬件复现状态。

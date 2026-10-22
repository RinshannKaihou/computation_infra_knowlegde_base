---
id: software-stack.dtype-layout-and-precision-semantics
title: dtype、layout、格式转换与有限精度语义
type: concept
domain: software-stack
status: draft
platforms: [generic, nvidia, amd, ascend]
source_refs:
  - src.pytorch.tensor-attributes-2.6
  - src.pytorch.amp-2.6
  - src.pytorch.amp-examples-2.6
  - src.pytorch.cuda-semantics-2.6
  - src.pytorch.set-float32-matmul-precision-2.6
  - src.pytorch.testing-assert-close-2.6
  - src.pytorch.numerical-verification-2.6
  - src.pytorch.channels-last-tutorial
  - src.nvidia.cublas-12.8-math-repro
  - src.nvidia.cuda-math-api-fp8-12.8
  - src.nvidia.cudnn-890-mathtype
  - src.amd.rocm-precision-7.14.0
  - src.amd.rocblas-precision-7.14.0
  - src.amd.miopen-precision-7.14.0
  - src.ascend.cann-82rc1alpha001-aol-index
  - src.huawei.cann-82rc1alpha001-aclnn-add
  - src.huawei.cann-82rc1alpha001-aclnn-matmul
  - src.huawei.cann-82rc1alpha001-acl-datatype
  - src.huawei.cann-82rc1alpha001-acl-promotion
  - src.ascend.torchnpu-npu-format-7.2.0
  - src.ascend.torchnpu-format-cast-7.2.0
  - src.ascend.torchnpu-format-helper-7.2.0
  - src.ascend.torchnpu-autocast-ops-7.2.0
  - src.ascend.torch-npu-v7.2.0-pytorch2.6.0
  - src.ascend.msprobe-training-guide-2026-09-30
  - src.pytorch.scalar-type-v2.6.0
updated_at: '2026-10-22'
summary: "区分 tensor dtype、布局与内存格式、内部格式、算子计算与累加精度、类型转换与特殊值五层语义，给出三平台精度开关的条件句（PyTorch 2.6、CUDA 12.8 库侧、ROCm docs-7.14.0、CANN 8.2.RC1.alpha001 入口级），只讲 autocast/累加/loss scaling 的基础责任，并给出同字节输入、固定权重、同平台重复与第一稳定差异的最小检查方法；训练收敛判据归 06.5、推理量化质量归 07.4。"
related_ids:
  - software-stack.layers-and-boundaries
  - software-stack.operators-compilers-and-graphs
  - software-stack.framework-backend-adaptation
  - software-stack.ascend-memory-oom-evidence
applicability:
  environment_refs: []
  notes: "尚无环境档案：PyTorch 侧固定 2.6 文档与 v2.6.0 源码（commit 1eba9b3）；CUDA 库侧固定 12.8.0 归档（cuDNN 例外为 8.9.0 归档，与 12.8 配套未经验证）；AMD 侧固定 docs-7.14.0；CANN 侧固定 8.2.RC1.alpha001（简介、aclDataType 枚举、互推导规则、aclnnAdd/aclnnMatmul 逐算子页静态正文已取得；累加精度未陈述）。目标环境的 dtype/精度组合需另行固定。"
verification:
  status: source_checked
  evidence_refs:
    - src.pytorch.tensor-attributes-2.6
    - src.pytorch.amp-2.6
    - src.pytorch.testing-assert-close-2.6
    - src.amd.rocm-precision-7.14.0
    - src.ascend.cann-82rc1alpha001-aol-index
    - src.huawei.cann-82rc1alpha001-aclnn-add
    - src.huawei.cann-82rc1alpha001-aclnn-matmul
    - src.huawei.cann-82rc1alpha001-acl-datatype
    - src.huawei.cann-82rc1alpha001-acl-promotion
    - src.ascend.torchnpu-npu-format-7.2.0
    - src.ascend.torchnpu-format-cast-7.2.0
    - src.ascend.torchnpu-format-helper-7.2.0
    - src.ascend.torchnpu-autocast-ops-7.2.0
  notes: "对照第十七批取证记录（docs/research/batch-17-dtype-precision-sources.md）所列固定版本来源核对；有限核对范围说明——Ascend 侧 source_checked 仅覆盖：aclDataType 19 行简写表（完整类型见 AscendCL 文档，未取得）、互推导规则、aclnnAdd/aclnnMatmul 两算子正文（含逐项 dtype 表与 cubeMathType 计算选项及产品/一维排除条件）、_format.py 存储格式枚举、FormatCast 候选门控分支返回值契约与入口体有限路径（候选函数未被已核验入口体调用）、FormatHelper base 判定、算子级 autocast 归属策略、autocast dtype 分支、AOL 简介支持规则；其余逐算子正文、逐算子累加精度、dtype-format 映射表逐项、枚举成员适用条件、TorchNPU 侧 cubeMathType 透传实现均未覆盖。cuDNN 8.9.0 与 CUDA 12.8 配套未经验证；未运行任何数值实验。条件验收例外见 docs/research/batch-17-t02-10-exception.md（C08 长期 open）。"
---

# dtype、layout、格式转换与有限精度语义

## 定义与要解决的问题

数值问题调查第一步是把五个易混概念分开，再谈“误差是否正常”：

1. **tensor dtype**：元素存储类型（如 fp32/fp16/bf16/int8）。2.6 [Tensor Attributes](https://docs.pytorch.org/docs/2.6/tensor_attributes.html) 页列 12 种常见类型；但固定 v2.6.0 [`ScalarType.h` L60–91](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/core/ScalarType.h#L60-L91) 还包含 Float8（e5m2/e4m3fn/fnuz 变体）、ComplexHalf、亚字节量化、UInt16/32/64 等——**页列 12 种是常见类型摘要，不是固定实现的完整集合**；类型存在、算子支持、autocast 覆盖是三个不同问题，不互相推出。fp16 = 1-5-10、bf16 = 1-8-7，bf16 与 fp32 同指数位宽故保范围。
2. **布局（layout）**：内存寻址方式（`torch.layout`：strided/sparse）。
3. **内存格式（memory format）**：分配与访问格式（`torch.memory_format`：contiguous/channels_last/channels_last_3d/preserve）。layout 与 memory_format 是两个正交概念。
4. **内部格式**：硬件/库侧的实际计算排布（如 Tensor Core 要求的对齐、block scaling），用户 dtype 不直接等于计算格式。
5. **计算与累加精度**：算子内部以何精度计算、以何精度累加（如 fp16 输入 + fp32 累加），以及转换、舍入、特殊值（NaN/inf、subnormal）的处理。

本文只到基础语义 + 检查方法。混合精度只讲 autocast/累加/loss scaling 的基础责任；训练收敛与任务质量判据见 06 章的[混合精度、算子适配与收敛验证](../06-training/mixed-precision-and-convergence.md)，推理量化方法与质量验证归 07.4，不在本文展开。

## 机制与关键关系

### 类型提升与内存格式

算术 type promotion 三规则（scalar 高类别 / 0-dim 高类别 / 同类别 dimensioned）与输出 tensor 三禁（int 不收 float、bool 不收非 bool、非复不收复）（[Tensor Attributes](https://docs.pytorch.org/docs/2.6/tensor_attributes.html)）。注意 `notes/type_promotion.html`、`notes/memory_format.html`、`notes/amp.html` 在 2.6 下实测 404，以 tensor_attributes 页正文为准，避免误引。

channels_last 用 stride 表达 NHWC（如 `(3072,1,96,3)`）；`to` 与 `contiguous` 在 `C==1` 等歧义形状下行为不同，推荐用 `to`；`clone`/like/逐点算子保持格式，conv 以 channels_last 为主导（[Channels Last 教程](https://docs.pytorch.org/tutorials/intermediate/memory_format_tutorial.html)，浮动版本、Last Verified 2024-11-05；性能数字只作方向证据）。

### 混合精度基础责任（只到机制）

autocast 只包 forward（含 loss），backward 不推荐包、沿用 forward dtype；CUDA 可 cast fp16 表 / 强制 fp32 表 / 按最宽输入提升表；未列出 op 不走 autocast（[torch.amp](https://docs.pytorch.org/docs/2.6/amp.html)）。`torch.cuda.amp.*` 已 deprecated，以 `torch.autocast(device_type=…)` 为准。

GradScaler 三步责任：scale 防 fp16 underflow → `unscale_` 后再检查/裁剪 → `step` 遇 inf/NaN 跳过 → `update`；梯度累加期间保持 scaled 且 `update` 只在有效 batch 步调；每 loss 独立 scale（[torch.amp](https://docs.pytorch.org/docs/2.6/amp.html) + [AMP Examples](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html)）。bf16 预训练模型用 fp16 scaler 可能反向 overflow（amp 页 Note 原文）。

### NVIDIA 侧精度开关（条件句）

- PyTorch 侧：`matmul.allow_tf32`（1.12+，默认 False）、`cudnn.allow_tf32`（默认 True），关断需两开关同关；`allow_fp16/bf16_reduced_precision_reduction`（BF16 默认开）；A100 示例 TF32 相对误差约大两量级（仅方向证据，不作阈值）（[CUDA semantics TF32 节](https://docs.pytorch.org/docs/2.6/notes/cuda.html)）。
- [`set_float32_matmul_precision`](https://docs.pytorch.org/docs/2.6/generated/torch.set_float32_matmul_precision.html)：highest/high/medium 三档只改内部计算精度、不改输出 dtype、不改卷积精度；**当前只影响 CUDA**（NVIDIA-only，正文保留该限定）。
- 库侧：cuBLAS 单 stream + 同架构同 SM 数 bitwise 保证，多 stream 非确定（四种规避）；GEMM K 切分在 compute 精度高于 output 时可中间溢出（`CUBLAS_MATH_DISALLOW_REDUCED_PRECISION_REDUCTION` 可控）；Tensor Core 使用与对齐条件；FP8/block-scaling 在 Lt §3.1.4（[cuBLAS 12.8](https://docs.nvidia.com/cuda/archive/12.8.0/cublas/index.html)）。cuDNN：`cudnnMathType_t`（DEFAULT/FMA/TENSOR_OP/ALLOW_CONVERSION）、`NVIDIA_TF32_OVERRIDE=0`（[cuDNN 8.9.0 归档 API](https://docs.nvidia.com/deeplearning/cudnn/archives/cudnn-890/api/index.html)，与 CUDA 12.8 配套未经验证）。CUDA FP8 格式（e4m3/e5m2、e8m0 scale）见 [Math API](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-math-api/cuda_math_api/group__CUDA__MATH__INTRINSIC__FP8.html)；PyTorch 2.6 amp 页未列 FP8，不推断框架覆盖。

### AMD 侧精度开关（条件句）

[ROCm 精度总表（docs-7.14.0）](https://rocm.docs.amd.com/en/docs-7.14.0/reference/precision-support.html)：HIP 类型与硬件架构支持矩阵（FP8 FNUZ 仅 CDNA3、OCP 仅 CDNA4/RDNA4）、matrix-core 支持表、各库输入/输出支持表；库页声明“所列为库支持、硬件支持另计”，正文保留该条件句。[rocBLAS 精度页](https://rocm.docs.amd.com/projects/rocBLAS/en/docs-7.14.0/reference/data-type-support.html)：Level 1–3 逐函数 dtype 矩阵（fp16/bf16 多为受限或不支持，GEMV fp16/bf16 仅 batched/strided-batched 脚注）。[MIOpen 精度页](https://rocm.docs.amd.com/projects/MIOpen/en/docs-7.14.0/reference/data_type_support.html)：`miopenDataType_t` 仅 Float/Half 全支持，卷积要求输入/输出 dtype 与 layout 一致；MI200 MFMA flush denormal，训练 backward 默认 alt-impl（forward 原实现），覆盖开关 `MIOPEN_DEBUG_CONVOLUTION_ATTRIB_FP16_ALT_IMPL`。

### Ascend 侧有限样板（数据类型枚举 + 互推导 + 逐算子表 + 计算精度选项）

- **aclDataType 简写表（官方正文，有限范围）**：[数据类型表](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/common/%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B.md)（静态正文已取得）说明：完整类型见 AscendCL `aclDataType` 文档（该页 L3 外链，本轮未取得）；该页 L7–27 为原始名/简写名两列简写表，共 19 行（含 ACL_STRING），**无 torch 对应列**。引用时按 19 行核对，不补推完整枚举或 torch 映射。
- **互推导规则（官方正文）**：[互推导关系](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/common/%E4%BA%92%E6%8E%A8%E5%AF%BC%E5%85%B3%E7%B3%BB.md)（静态正文已取得）——输入 dtype 不一致时 API 内部推导出一类型并转换后计算，原理类似 PyTorch Type Promotion。规则存在性证据；逐算子例外以各算子页约束为准。
- **aclnnAdd 样板（官方算子正文）**：[aclnnAdd/aclnnInplaceAdd](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/aclnnAdd&aclnnInplaceAdd.md)（静态正文已取得）——支持产品（Atlas 训练系列；Atlas A2 训练系列/800I A2 推理/A200I A2 异构组件）；self/other/alpha/out 逐项 dtype 表（A2 比训练系列多 BFLOAT16）；ND 数据格式；broadcast；`ACLNN_ERR_PARAM_INVALID` 错误条件。逐参数 dtype 存在性样板；Add 为逐元素算子，不含累加语义。
- **aclnnMatmul 计算精度样板（官方算子正文 + 框架实现侧）**：[aclnnMatmul](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/aclnnMatmul.md)（静态正文已取得）——self/mat2/out 逐项 dtype 表（训练/推理系列 FLOAT16/FLOAT32；A2 系列加 BFLOAT16）；ND 格式；1–6 维与 broadcast；**cubeMathType（INT8，Host 侧）指定 Cube 单元计算逻辑**：有互推导关系时选项处理的是推导后的类型，out 须与推导后类型一致（降计算精度不等于输出存储 dtype 降低）；0 `KEEP_DTYPE`（保持输入类型计算，**训练/推理系列 FLOAT32 输入不支持该选项**）；1 `ALLOW_FP32_DOWN_PRECISION`（训练/推理 F32→F16，A2 F32→HF32，其他输入不处理）；2 `USE_FP16`（输入降精度至 FLOAT16 计算，**A2 上 BFLOAT16 输入不支持该选项**）；3 `USE_HF32`（限 A2 且仅 F32 输入）；A2 不支持 BFLOAT16 与 FLOAT16/FLOAT32 的互推导；**self 与 mat2 均为一维时 cubeMathType 不生效**（尽管维度支持 1–6 维）。框架实现侧（分别记录，非同一证据链）：TorchNPU 快照为 matmul 家族（matmul/mm/bmm/addmm 等）注册 `lower_precision_fp` autocast 归属（见下条），属输入 autocast 注册策略，不建立到 cubeMathType 的实现关系。**累加精度未在官方页陈述**，继续单列 unknown。
- **算子级 autocast 归属策略（固定实现，非计算精度证据）**：

以下是有官方正文与固定实现的有限样板；**累加精度仍 unknown**（见本节末）。

- **存储格式枚举（固定实现）**：TorchNPU 快照 [`torch_npu/npu/_format.py`](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/_format.py)（38 行）定义 NPU 存储格式 `Format`：UNDEFINED/NCHW/NHWC/ND/NC1HWC0/FRACTAL_Z/NC1HWC0_C04/HWCN/NDHWC/FRACTAL_NZ/NCDHW/NDC1HWC0/FRACTAL_Z_3D/NC/NCL，并经 `_apply_npu_format_patch` 把 `torch_npu.get_npu_format` 返回值包成该枚举。这是与 `torch.memory_format` 不同的另一套存储格式面（分形/NHWC 变体等硬件排布），引用时带 NPU 前缀，不得与 PyTorch 通用格式混读。
- **格式转换（固定实现）**：快照 [`FormatCastHelper.h`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/FormatCastHelper.h)（29 行）定义转换接口面（base-format cast、between-group cast、`ApplyBaseFormatTensorBy`）；[`FormatCastKernelNpu.cpp`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/FormatCastKernelNpu.cpp)（287 行）中 `MaybeUseAclnnNpuFormatCast`（L39–83，文件注释明示为未来功能保留）区分：aclnn-only 且接口缺失 → 报 `NOT_SUPPORT`（L50–52）；jit-disable + 接口存在但尺寸 API 失败且无 `customize_dtype` → 返回 `false`（L54–62）；接口缺失且无 `customize_dtype` → 返回 `false`（L70–75）；jit 未禁用且无 `customize_dtype` → 返回 `false`（L78–83）；带 `customize_dtype` 的若干分支另有报错条件。**该候选函数的返回值只说明其自身返回契约**：已核验的 `NPUNativeFunctions` 入口体（L155–284：同格式短路、目标格式重载中的双边 base 快径、通用转换调用）**未调用**该候选函数，不得据此声称当前入口按这个布尔值切换路径（不推断仓库别处无调用）。已核验范围限所查入口体重载分支，不扩大为全部公开绑定/运行时链已验收。内核注释原文：format cast 只改变物理排布，view 元数据不变。函数与入口定义存在不证明 aclnn 内核可用性或版本交集已验收。base 定义见 [`FormatHelper.cpp` L96–126](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/framework/FormatHelper.cpp#L96-L126)（`GetBaseFormat` 查 info 映射表，`IsBaseFormatType` 即等于自身 base；未知格式 `AT_ERROR("unknown format type")`）。调用点含 dtype 到 aclDataType 的转换（`convert_to_acl_data_type`/`GetAclDataType`），映射表内容未核对，不引用具体映射。
- **dtype 分支（固定实现）**：[`autocast_utils.py`](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/autocast_utils.py) 的 `get_amp_supported_dtype`（bf16 支持则 `[float16, bfloat16]` 否则 `[float16]`）；`__init__.py` 的 `unsupported_dtype` 五项仅约束自动生成的 Storage 转移方法（见 T02-08 修订，不作后端否定清单）。
- **算子级 autocast 归属策略（固定实现，非计算精度证据）**：快照 [`AutoCastOps.cpp`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/AutoCastOps.cpp)（159 行）为 NPU 后端逐算子注册 autocast 归属：普通 `KERNEL_PRIVATEUSEONE` 宏四族（`lower_precision_fp` 如 matmul/conv 线性族、`fp32` 如 exp/log/norm/loss 族、`fp32_set_opt_dtype` 如 softmax/reduction 族、`promote` 族）+ `KERNEL_DIFFERENT_REDISPATCH_SIGNATURE_PRIVATEUSEONE` 宏的第五种策略（`fp32_append_dtype`，norm 三个重载，L128–142）+ `binary_cross_entropy` 的显式禁用（banned，引导改用 with_logits 版）。这是算子级精度**归属策略**样板（上游 autocast 语义以 PyTorch 2.6 amp 页为准），**不是逐算子计算/累加精度证据**，不关闭 C08 必交子项。
- **官方边界（官方正文）**：[AOL 接口简介](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/operatorlist_00001.html)（静态正文已取得）明示 AOL 结构（公共 Meta 接口、aclnn NN 算子、融合与 DVPP 算子）与支持规则——对于各类算子接口或规格清单中未审明支持的场景（如产品型号、数据类型、数据格式、数据维度等），不推荐使用，当前版本不保证调用效果。即：某 dtype/format 组合的支持性以**该算子文档的列表**为准，不在列表即未知，不得用 TorchNPU 快照或 CUDA 语义补写。
- **仍 unknown**：逐算子累加精度（aclnnMatmul 官方页未陈述累加数据类型；其余算子页同理待查）；info 映射表逐项内容；上述 Format 枚举成员各自的适用算子/硬件条件；TorchNPU 侧 cubeMathType 透传实现未在快照内定位。autocast 归属策略不代替计算精度证据。必交子项未齐部分在主题验收时保持 open。

### 比较方法：assert_close 与重复性

数值比较用 [`assert_close`](https://docs.pytorch.org/docs/2.6/testing.html)：`|actual−expected| ≤ atol + rtol·|expected|`，按 dtype 默认容差表（fp16 1e-3/1e-5、bf16 1.6e-2/1e-5、fp32 1.3e-6/1e-5），`check_dtype/layout/device/stride` 默认前三开，NaN 默认不等。**默认容差表只作比较起点，任务验收阈值须按任务预设**（msprobe 的 1%/0.99 为工具内规则，同样不作通用阈值）。

同平台重复控制（[Reproducibility](https://docs.pytorch.org/docs/2.6/notes/randomness.html)）：`manual_seed` 全设备只是随机性控制之一；另须分别处理算法自身非确定（`use_deterministic_algorithms` 与可抛错语义）、其他 RNG 源、未初始化内存填充、cuDNN `benchmark=False`（选算法确定）vs `deterministic=True`（算法自身确定）分工、`CUBLAS_WORKSPACE_CONFIG`；首段“跨 release/commit/平台不保证复现，CPU↔GPU 可不同”是跨平台比较的上限声明。

浮点非结合、CPU↔GPU 同字节输入也可不同、batch/slice 与逐元素结果可不同、linalg 非有限输入无保证与病态矩阵可静默错（`svdvals`/`cond` 排查）见既有数值验证登记（`src.pytorch.numerical-verification-2.6`，本轮复核）。

## 适用边界

- 三平台开关不互推：TF32、`set_float32_matmul_precision`、alt-impl、aclnn 精度各自只在其来源支持范围成立。
- `assert_close` 默认容差、msprobe 工具内规则、TF32 示例误差均为方向证据；任何通用数值验收阈值都不存在，阈值必须按任务预设。
- cuDNN 8.9.0 与 CUDA 12.8 的配套组合未经验证，不得拼成已验证环境。
- 本文不含任何“某模型收敛/不收敛”“某量化方法质量好坏”结论；不含实测数值。

## 常见误解

- **“输出 dtype 相同即计算精度相同”**：错。计算精度（TF32/reduced reduction/alt-impl）与累加精度独立于输出 dtype，须查开关当时值。
- **“开了 autocast 误差就可接受”**：错。可接受与否由任务预设容差判定；autocast 只决定算子归属表，不给出正确性保证。
- **“跨平台同输入应同输出”**：错。跨平台/跨版本不保证复现是官方上限声明；比较前先做同平台重复性，再谈差异。
- **“assert_close 通过即任务正确”**：错。它只证明在给定容差下数值接近；dtype 未对齐（默认 `check_dtype=True` 直接失败）与病态/非有限输入的数值风险是两类反例（见下节三档处理）。

## 最小检查方法

顺序不可换：

1. **同字节输入**：固定输入字节（含 dtype、shape、stride/memory_format、NaN/inf 分布），记录 `dtype/strides/is_contiguous(memory_format=…)` 快照。
2. **已固定权重**：同一 checkpoint 同一加载路径；先 assert shape + dtype + layout 一致，再谈数值（`check_dtype/check_layout` 默认开做门禁）。
3. **同平台重复性**：同机同卡同版本跑两次并记录全部随机性/算法/同步控制（上节清单）。两次不同**先记为观察**，再按任务预设规则判定——即使存在已知非确定性，也不能自动认定该差异满足任务阈值；可复现的差异仍须按任务容差验收，不自动判正常。
4. **第一稳定差异**：先确认输入/权重字节一致、重复比较、差异位置可定位；再逐层/逐算子二分，每次只改一个变量（TF32 / reduction / autocast / alt-impl 开关），用 `assert_close` 以任务预设 `rtol/atol` 判定；首个**可重复**超差点才是第一稳定差异，向上追溯到开关 + 算子 + 输入分布。单次超差不等于稳定差异，证据不足时保留 unknown。

**正常误差例**：开 TF32 的 fp32 matmul vs 关 TF32（或 fp64 参考），相对误差大 1–2 量级但随开关可解释、可复现；MI200 fp16 卷积 forward 原实现 vs alt-impl 小幅差异。属有限精度语义内（仍须过任务容差门）。

**数值风险分支（非“须判错”）**：① `assert_close(fp16_tensor, fp32_tensor)` 在默认 `check_dtype=True` 下直接失败——错在比较前提，不是数值错误，先统一 dtype 再设容差；② linalg 在病态/非有限输入下**可能**静默返回错误结果（上游：[Numerical accuracy → Linear algebra](https://docs.pytorch.org/docs/2.6/notes/numerical_accuracy.html#linear-algebra-torch-linalg)，非有限输入无行为保证）——处理分三档：**拒绝输入**（检出 NaN/inf 即停止并排查上游，不进入归因）、**进一步验证**（高 `cond` 时换参考解/算残差，阈值按任务预设）、**已证错误**（残差超阈且可重复，才记错误结论并写清参考与阈值）。检出高 condition number 或换设备结果不同本身不证明已观察输出必然错误，更不直接归因平台缺陷；以上均为待执行设计，不编造错误结果。

## 来源与待确认问题

- PyTorch 2.6：[Tensor Attributes](https://docs.pytorch.org/docs/2.6/tensor_attributes.html)、[torch.amp](https://docs.pytorch.org/docs/2.6/amp.html)、[AMP Examples](https://docs.pytorch.org/docs/2.6/notes/amp_examples.html)、[CUDA semantics](https://docs.pytorch.org/docs/2.6/notes/cuda.html)（TF32/reduction 节）、[set_float32_matmul_precision](https://docs.pytorch.org/docs/2.6/generated/torch.set_float32_matmul_precision.html)、[torch.testing](https://docs.pytorch.org/docs/2.6/testing.html)、[Reproducibility](https://docs.pytorch.org/docs/2.6/notes/randomness.html)、[Channels Last 教程](https://docs.pytorch.org/tutorials/intermediate/memory_format_tutorial.html)。
- NVIDIA（12.8.0 归档，cuDNN 例外 8.9.0）：[cuBLAS](https://docs.nvidia.com/cuda/archive/12.8.0/cublas/index.html)、[CUDA Math FP8](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-math-api/cuda_math_api/group__CUDA__MATH__INTRINSIC__FP8.html)、[cuDNN 8.9.0 API](https://docs.nvidia.com/deeplearning/cudnn/archives/cudnn-890/api/index.html)。
- AMD（docs-7.14.0）：[精度总表](https://rocm.docs.amd.com/en/docs-7.14.0/reference/precision-support.html)、[rocBLAS 精度](https://rocm.docs.amd.com/projects/rocBLAS/en/docs-7.14.0/reference/data-type-support.html)、[MIOpen 精度](https://rocm.docs.amd.com/projects/MIOpen/en/docs-7.14.0/reference/data_type_support.html)。
- Ascend：[CANN AOL 入口与接口简介](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/operatorlist_00001.html)（AOL 结构与支持规则）、[aclDataType 枚举](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/common/%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B.md)、[互推导关系](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/common/%E4%BA%92%E6%8E%A8%E5%AF%BC%E5%85%B3%E7%B3%BB.md)、[aclnnAdd](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/aclnnAdd&aclnnInplaceAdd.md)、[aclnnMatmul 含 cubeMathType 计算选项](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/aclnnMatmul.md)（以上静态正文均已取得）；TorchNPU [`_format.py`](https://raw.githubusercontent.com/Ascend/pytorch/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/npu/_format.py)（存储格式枚举）、[`FormatCastHelper.h`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/FormatCastHelper.h) + [`FormatCastKernelNpu.cpp`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/common/FormatCastKernelNpu.cpp)（转换路径）、[`FormatHelper.cpp` L96–126](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/framework/FormatHelper.cpp#L96-L126)（base 判定）、[`AutoCastOps.cpp`](https://github.com/Ascend/pytorch/blob/bc51ab84cc6f35c77aab1c59886e0ea43681a317/torch_npu/csrc/aten/AutoCastOps.cpp)（算子级归属策略）与 [`ScalarType.h`](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/c10/core/ScalarType.h#L60-L91)（页列 12 种 vs 实现枚举差异）。
- 逐条主张与证据定位见[第十七批精度语义来源记录](../../docs/research/batch-17-dtype-precision-sources.md)。
- 待确认：逐算子累加精度（aclnnMatmul 官方页未陈述；其余算子页同理待查）；info 映射表逐项内容与 Format 枚举成员适用条件；TorchNPU 侧 cubeMathType 透传实现定位；PyTorch 2.6 autocast 对 FP8 覆盖；ROCm 各页许可；任何通用数值验收阈值。
- 修订记录：2026-10-09 按初审 B17-C06/C07/C08/C13 修订，后续复核补格式转换样板、门控分支限定、autocast 第五策略、本轮补 aclDataType/互推导/aclnnAdd/aclnnMatmul 计算精度样板（见 [batch-17-review-fixes.md](../../docs/research/batch-17-review-fixes.md)），已完成[第六次定向复核](../../docs/research/batch-17-codex-sixth-recheck.md)；B17-C08 继续 OPEN，并受[用户批准的条件验收](../../docs/research/batch-17-t02-10-exception.md)约束，不表示精度契约或硬件验证通过。

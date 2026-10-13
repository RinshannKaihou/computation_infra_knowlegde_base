# 第十七批 T02-10 精度语义来源记录

任务：T02-10 dtype、layout、格式转换与有限精度语义（`dtype-layout-and-precision-semantics.md`，concept）。取证日期 2026-10-09。域边界：训练收敛判据归 06.5、推理量化质量归 07.4，本文只到基础语义 + 检查方法。

## 候选来源（11 项新登记 + 3 复用）

| proposed-id | 精确 URL | 核对要点 |
|---|---|---|
| src.pytorch.tensor-attributes-2.6 | docs/2.6/tensor_attributes.html | 12 种 dtype、fp16/bf16 位宽、promotion 三规则 + 输出三禁、layout vs memory_format 正交；type_promotion/memory_format/amp notes 页 404 |
| src.pytorch.amp-2.6 | docs/2.6/amp.html | autocast 包 forward、op 三类表、GradScaler 三步；cuda.amp deprecated |
| src.pytorch.amp-examples-2.6 | docs/2.6/notes/amp_examples.html | clip/累加/多模型多优化器模式；只讲机制 |
| （复用）src.pytorch.cuda-semantics-2.6 | docs/2.6/notes/cuda.html TF32/reduction 节 | allow_tf32 双开关、reduced precision reduction、A100 误差量级方向 |
| src.pytorch.set-float32-matmul-precision-2.6 | docs/2.6/generated/torch.set_float32_matmul_precision.html | 三档只改内部计算、只影响 CUDA |
| src.pytorch.testing-assert-close-2.6 | docs/2.6/testing.html | 公式、dtype 默认容差表、四开关、equal_nan；与 numerical-verification 复核一致；只作比较起点 |
| （复用）src.pytorch.numerical-verification-2.6 | numerical_accuracy 全文 | 非结合、跨设备差异、linalg 病态、MI200 env 表；本轮复核通过 |
| （复用）src.ascend.msprobe-training-guide-2026-09-30 | commit 7783f6b | 1%/0.99 为工具内规则，非通用阈值 |
| src.pytorch.channels-last-tutorial | tutorials memory_format_tutorial.html | NHWC stride 实例、to vs contiguous、格式保持；浮动版本；性能数字不作阈值 |
| src.nvidia.cublas-12.8-math-repro | 12.8 cublas/index.html | §2.1.4 bitwise 保证/四种规避、§2.1.10 K 切分溢出、§2.1.11 Tensor Core、§2.2.10 math、§3.1.4 FP8 |
| src.nvidia.cuda-math-api-fp8-12.8 | 12.8 …/group__CUDA__MATH__INTRINSIC__FP8.html | e4m3/e5m2、e8m0 scale；只证明入口存在；2.6 amp 未列 FP8 |
| src.nvidia.cudnn-890-mathtype | cudnn-890/api/index.html | math type/data type/tensor format 枚举；与 12.8 配套未经验证 |
| src.ascend.cann-82rc1alpha001-aol-index | aolapi/operatorlist_00001.html | 入口已定位；正文未抽取（站点外壳）；逐算子表待二次核对 |
| src.amd.rocm-precision-7.14.0 | docs-7.14.0/reference/precision-support.html + HIP low_fp_types 伴页 | 架构支持矩阵、matrix-core 表、库表；FNUZ vs OCP；库支持≠硬件支持 |
| src.amd.rocblas-precision-7.14.0 | docs-7.14.0 rocBLAS data-type-support | Level 1–3 矩阵；GEMV 脚注 |
| src.amd.miopen-precision-7.14.0 | docs-7.14.0 MIOpen data_type_support + alt-impl + env | 枚举与矩阵；MI200 alt-impl 默认；确定性开关 |

备选已实开未单独立 ID：hipBLAS 精度页、MIOpen NHWC batchnorm 页、cuBLAS Lt FP8（归入 #9 节锚）。

## 主张—来源定位表（16 行）

dtype 12 种与位宽（#1 dtype 节）；promotion 三规则 + 三禁（#1）；layout vs memory_format 正交（#1）；channels_last stride 与 to/contiguous 差异（#8）；autocast 包 forward 与 op 三表（#2）；GradScaler 三步与累加模式（#2/#3）；TF32 双开关与误差量级（#4 + numerical-verification）；reduction 开关与 SDPA upcast（#4 + 同）；三档精度只改内部、只影响 CUDA（#5）；非结合/跨设备差异/linalg 病态（numerical-verification）；MI200 alt-impl（同 + #15）；assert_close 公式与容差表（#6）；重复三件套与跨平台上限（#7）；cuBLAS 保证/规避/K 切分/FP8（#9）；cuDNN math type（#11）；MIOpen/ROCm 矩阵与 FNUZ/OCP（#13–#15）。平台边界见正文条件句。

## 最小检查方法草案

同字节输入 → 固定权重 → 同平台重复性 → 第一稳定差异（每次只改一个开关，assert_close 以任务预设判定）。容差规则：任务预设为准。正常误差例：TF32 开关可解释差异、MI200 alt-impl 小幅差异。错误反例：dtype 未对齐的 assert_close 失败（比较前提错）、病态 linalg 静默错（isfinite + cond/svdvals 前置）。

## 跨域不重复清单

06.5 留收敛判据/优化器策略/质量评估；07.4 留 PTQ/QAT 与引擎量化配置；本文只到开关语义 + op 归属表 + GradScaler 责任 + 比较方法。

## unknown 清单

CANN 逐算子表（blocked）；TorchNPU dtype/format 文件级定位；2.6 autocast 对 FP8 覆盖；cuDNN/12.8 配套；ROCm 各页许可；channels-last 版本钉死；hipBLASLt 细节；MIOpen 确定性保证强度；任何通用数值验收阈值；Ascend 侧官方原文（一律 unknown，不互推）。

## 修订记录（2026-10-09，按初审 B17-C06/C07/C08/C13）

- C06：重复性控制扩展为清单（seed/算法/其他 RNG/未初始化内存/benchmark vs deterministic/CUBLAS_WORKSPACE_CONFIG）；两次不同先记观察再按任务规则判；第一稳定差异须输入字节一致、重复比较、可重复超差。
- C07：病态/非有限输入改三档处理（拒绝输入/进一步验证/已证错误），残差与阈值按任务预设；不编造错误结果。
- C08：补 Ascend 有限样板——TorchNPU _format.py 存储格式枚举 15 成员（修订轮 raw 全文 38 行实测）+ autocast dtype 分支 + AOL 简介官方边界句（未审明支持不推荐/不保证效果，静态正文已取得）；转换 API 与逐算子计算/累加精度仍 unknown 并逐项列出。新增登记 src.ascend.torchnpu-npu-format-7.2.0。
- C13：12 种改为页列常见类型摘要；固定 ScalarType.h L60–91 另含 Float8/ComplexHalf/亚字节量化/UInt16-64 等；存在≠支持。定向复核待执行。

## 第二轮复核修订（2026-10-09，按 B17-C08 剩余条件）

- 新增格式转换有限样板：FormatCastHelper.h（29 行接口面）+ FormatCastKernelNpu.cpp（287 行：aclnn 门控路径与非 aclnn 路径、物理排布语义注释）+ FormatHelper.cpp L96–126（base 判定、未知格式 AT_ERROR）；调用点 dtype→aclDataType 转换存在性（映射表内容未核对）。
- 新增登记 2 项（format-cast、format-helper）；AOL 登记 revision/notes 记录简介静态正文已取得；正文 verification notes 说明有限核对范围；逐算子计算/累加精度、映射表逐项、枚举成员适用条件仍 unknown 并保持 open。

## 第三轮修订（2026-10-09，按第二次复核 C08 剩余条件）

- 转换门控改写为分支条件：aclnn-only 缺接口报 NOT_SUPPORT；其余三类（jit-disable 缺接口无 customize_dtype、取尺寸失败无 customize_dtype、jit 未禁用无 customize_dtype）返回 false 走候选非 aclnn 路径；带 customize_dtype 分支另有报错条件。公开入口 npu_format_cast[_] 到 impl 调用链已核验（同格式短路/双边 base 快径/通用路径）。
- 新增算子级 autocast 归属样板：AutoCastOps.cpp 全文 159 行（四族 + binary_cross_entropy 禁用），明确标注非计算精度证据、不关闭必交子项；新增登记 src.ascend.torchnpu-autocast-ops-7.2.0。逐算子计算/累加精度仍 unknown 并保持 open。

## 第四轮修订（2026-10-09，按第三次复核 C08 剩余条件）

- 候选门控与入口关系纠正：MaybeUseAclnnNpuFormatCast（L39–85，未来功能保留）分支坐标更正（NOT_SUPPORT 完整为 L50–52；L54–62 系接口存在尺寸失败分支；接口缺失无 customize_dtype 的 false 在 L70–75）；返回值只说明候选函数自身契约，已核验入口体（L155–284）未调用它；核验范围限所查重载分支。
- autocast 样板补第五种策略：fp32_append_dtype 经不同宏注册（norm 三重载，L128–142）；“四族”限定为普通注册宏。计算/累加精度仍 unknown 并保持 open。

## 第五轮修订（2026-10-09，C08 计算精度样板）

- 经 doc_center 静态 markdown 通道取得：aclDataType 全量枚举表、互推导关系规则、aclnnAdd 逐参数 dtype 表（含 A2 BFLOAT16 差异与错误码）、aclnnMatmul 逐项 dtype 表与 cubeMathType 四选项计算逻辑（KEEP/ALLOW_FP32_DOWN/USE_FP16/USE_HF32，逐产品条件与互推导排除项）；新增登记 4 项。
- TorchNPU 侧 cubeMathType 透传实现未在快照内定位；累加精度官方未陈述，继续单列 unknown 并保持 open。

## 第六轮修订（2026-10-09，按第五次复核三项要求）

- 数据类型页更正为 19 行简写表（含 ACL_STRING，无 torch 列；完整类型见 AscendCL 文档未取得）；正文“21 项全量枚举”断言撤销，登记 title/notes 同步。
- Matmul 摘要补全：KEEP_DTYPE 训练/推理 F32 不支持；USE_FP16 的 A2 BFLOAT16 排除；互推导存在时处理推导后类型、out 与推导后类型一致（降计算精度≠降输出存储 dtype）；双一维输入 cubeMathType 不生效；SDK 契约与 TorchNPU 实现分别记录。登记 notes 同步。
- verification notes 同步“两算子正文已取得”范围，其余逐算子正文与累加精度/实现关联仍 unknown。累加精度继续 OPEN。

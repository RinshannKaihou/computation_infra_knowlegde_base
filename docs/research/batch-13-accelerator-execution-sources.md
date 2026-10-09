# 第十三批来源记录：三平台执行单元、内存层次与数据移动机制（T01-04）

研究日期：2026-10-08。研究者：探索子代理（非 gpt-6.1-sol）。目标正文：`knowledge/01-hardware/accelerator-execution-and-data-movement.md`（concept，planned，验收标准见 plans/full-coverage-backlog.yaml T01-04）。代际选择：NVIDIA H100 SXM5（Hopper，CC 9.0）、AMD CDNA2/MI200（MI250X）、Ascend CANN 8.2.RC1.alpha001 文档树所描述的 Atlas A2（910B 代）。Ascend 此前「执行单元/内存层次只有产品页」的受阻已解除（官方 Ascend C 架构页可取）。未执行任何设备测试；除本文件外未改动仓库其他文件。

## 主张—证据表（NVIDIA）

| 主张 | 来源与定位 | 版本 | 性质 | 反例/未知 |
|---|---|---|---|---|
| H100 SXM5：132 SM、每 SM 128 FP32 核 + 4 个第四代 Tensor Core、80GB HBM3、50MB L2；SM 内 256KB L1+shared 合体（shared 可配至 228KB）；GH100 满配 144 SM/6 HBM 堆栈/60MB L2 | [H100 白皮书 V1.01](https://www.advancedclustering.com/wp-content/uploads/2022/03/gtc22-whitepaper-hopper.pdf)（第三方镜像）与[官方博客 Hopper In-Depth 表 3](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/) 交叉核对 | V1.01 / 博客 2022-03-22 | C+B（镜像+官方网页） | 原始 resources.nvidia.com 链接 2026-10-08 实测 302 跳转失效；白皮书法律声明未逐字提取 |
| SIMT：warp=32 线程；Volta 起 Independent Thread Scheduling；每 SM 64 warps/2048 线程、64K 寄存器 | [CUDA C++ Programming Guide 12.8](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-c-programming-guide/index.html) §4.1/§4.2（已登记 src.nvidia.cuda-toolkit-12-8） | 12.8 | A | — |
| 内存层次与数据移动：§2.3 Memory Hierarchy；§3.2.6 Page-Locked Host Memory；§3.2.8.3 Overlap（asyncEngineCount）；§3.2.8.9 Synchronous Calls；§2.5 cuda::memcpy_async；§7.29 TMA（12.8 新增 TMA Swizzle） | 同上对应章节 | 12.8 | A | TMA 需 CC 9.0 |
| NVLink 第四代 18 链路 900GB/s（7×PCIe Gen5）；NVSwitch 第三代 64 端口 13.6 Tbit/s；PCIe Gen5 128GB/s 双向 | 白皮书/官方博客对应节 | 2022 | C+B | — |
| 显存带宽口径冲突：白皮书/博客 Table 3 记 3000 GB/s（标注 preliminary）；NVIDIA H100 产品页（2026-10-08 复核）Product Specifications 表为 3.35 TB/s（H100 SXM）与 3.9 TB/s（H100 NVL），页面不再单列 PCIe（非 NVL）列 | 上述两来源 vs [产品页](https://www.nvidia.com/en-us/data-center/h100/) | 2022 vs 2026-10-08 | C+B vs B | 正文注明口径与时间，不混写（B13-C14 修订：补产品页精确口径与登记） |
| 计算强度（arithmetic intensity）与延迟隐藏/占用率 | CUDA 指南 §5.2 | 12.8 | A | — |
| 官方传输验证示例：cuda-samples bandwidthTest（D2D、H2D/D2H pageable 与 page-locked 四路带宽，event 计时，支持 SM 9.0） | [cuda-samples](https://github.com/NVIDIA/cuda-samples/tree/master/Samples/1_Utilities/bandwidthTest) | master 观察 2026-10-08（README 提 Toolkit 12.4） | B | 仓库 LICENSE 未核 |

## 主张—证据表（AMD CDNA2/MI200）

| 主张 | 来源与定位 | 版本 | 性质 | 反例/未知 |
|---|---|---|---|---|
| MI200=2×GCD（OAM，MI250/MI250X）；每 GCD 64GB HBM2e（整卡 128GB）、聚合 3.2TB/s；L2 每 GCD 8MB；封装内 Infinity Fabric 400GB/s 双向；8 条外部 IF 链路合计 800GB/s；一致性主机接口（16-lane IF，配特定 EPYC 时缓存一致，否则回退 PCIe）；FP64 峰值 47.9 TFLOPS（向量） | [AMD CDNA 2 Architecture 白皮书](https://www.amd.com/content/dam/amd/en/documents/instinct-business-docs/white-papers/amd-cdna2-white-paper.pdf) | ©2021 AMD | A | 提取至约 p.10；MI210 为 3 链路 300GB/s 且单 GCD，勿混 |
| wavefront=64 work-items；SALU+VALU；LDS 64kB/CU（32 bank）；EXEC mask；矩阵指令 V_MFMA_F64_16x16x4/4x4x4、V_MFMA_..._BF16_1K；packed FP32 | [MI200 ISA Reference Guide](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instruction-set-architectures/instinct-mi200-cdna2-instruction-set-architecture.pdf) ch.1–3/7/11 | 2022-02-04，267 页 | A | 许可为 AMD Specification Agreement：仅许对接设计参考、禁止复制；只可归纳 |
| 220 CU/880 Matrix Core（MI250X） | [Hot Chips 34 AMD deck](https://hc34.hotchips.org/assets/program/conference/day1/GPU%20HPC/HC2022.AMD.AlanSmith.v13.Final.20220818.pdf)（AMD 研究员署名）与 amd.com NAMD tech brief | 2022-08 | B（A 级衍生） | 不在白皮书已提取部分；正文注明出处层级 |
| HIP：warp 典型 64（"though sometimes 32"）；host/device 异构、stream/event 异步；pinned memory 小批量可走 DMA 不涉 CPU | [HIP programming manual docs-6.3.3](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/user_guide/programming_manual.html) | HIP 6.3.42134 | A（MIT 已核） | CDNA2 以 ISA 的 64 为准 |
| hipMemcpy：kind 与指针不匹配=未定义行为；P2P 需 hipDeviceEnablePeerAccess 否则经 host staging；hipMemcpyAsync 对非 pinned 内存退化为同步；"on HCC hipMemcpyAsync does not support overlapped H2D and D2H copies" | [HIP 6.3.3 memory_management 模块](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/reference/hip_runtime_api/modules/memory_management.html) 与 [how-to](https://rocm.docs.amd.com/projects/HIP/en/docs-6.3.3/how-to/hip_runtime_api/memory_management.html) | docs-6.3.3 | A（MIT） | "on HCC" 为运行时实现注记，正文限定为 ROCm 文档注记的实现边界 |
| AMD 侧验证工具：ROCm/rocm_bandwidth_test（默认分支 develop HEAD d7f5efe，2026-07-08；根 LICENSE.md 为 MIT，GitHub license API 确认；该 revision 的 README 已描述重写后的 RBT-NG 实现（基于 TransferBench 插件架构），该 commit 另新增 RBT 弃用/迁移声明（迁移至 TransferBench/RVS）——已存在实现与弃用声明分开，不写成「正在重写」） | [GitHub](https://github.com/ROCm/rocm_bandwidth_test) | 固定 commit d7f5efe | B | 弃用声明版本，行为/输出格式按版本限定（B13-C14 补登记 src.amd.rocm-bandwidth-test-d7f5efe；B13-C18 修订措辞） |

## 主张—证据表（Ascend / CANN 8.2.RC1.alpha001 文档树）

| 主张 | 来源与定位 | 版本 | 性质 | 反例/未知 |
|---|---|---|---|---|
| AI Core = Cube（矩阵）/Vector（向量）/Scalar（标量）三计算单元 + 存储单元 + 搬运单元（MTE1/2/3、FixPipe）；耦合架构 vs 分离架构（AIC/AIV）；Atlas A2 训练/推理系列为分离架构（AIC：MTE1/MTE2/Cube/Scalar + GM/L1/L0A/L0B/L0C/BT/FP Buffer；AIV：MTE2/MTE3/Vector/Scalar + GM/UB） | [atlas_ascendc_10_0008.html](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/opdevg/Ascendcopdevg/atlas_ascendc_10_0008.html) | URL 82RC1alpha001；页头版本未直核；2026-10-08 观察 | A | CANN 9.0 树英文同页术语一致（coupled/separated mode），可作对照 |
| Cube 一次完成 A(M×K)×B(K×N)；Vector 源/目的必须在 UB、通常 32B 对齐；Scalar≈小 CPU（iCache/dCache）；核外 L2 Cache | [0009 计算单元](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/opdevg/Ascendcopdevg/atlas_ascendc_10_0009.html) | 同上 | A | — |
| 内存层次 GM/L1/L0A/L0B/L0C/UB 多级内部存储；MTE=Memory Transfer Engine，搬运可随路格式/类型转换；经搬运单元读写 GM 默认经 L2 Cache；各存储大小随处理器型号、由 GetCoreMemSize 获取。**表 1（存储单元介绍）经原始 HTML 内嵌数据补得六行**：L1 Buffer（通用中转区，暂存 Cube 反复使用的数据）；L0A/L0B（Cube 指令输入）；L0C（Cube 输出，累加时也是输入）；Unified Buffer（向量和标量计算的输入输出）；BT Buffer（BiasTable）；FP Buffer（Fixpipe，量化/Relu 参数等） | [0010 存储单元](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/opdevg/Ascendcopdevg/atlas_ascendc_10_0010.html) | 同上 | A | 表 1 在阅读器式提取中为空（JS 渲染），须取原始 HTML 解析内嵌 JSON（B13 复核补齐）；容量数值表仍无官方来源 |
| 数据流：GM→L1→L0A/L0B→Cube→L0C→FixPipe→GM/L1；GM→UB→Vector→UB→GM；Scalar 分发到 Vector/Cube/MTE 独立队列、队列间并行；PipeBarrier（队列内）、SetFlag/WaitFlag（队列间）同步原语；Ascend C = SPMD（GetBlockIdx 区分分片） | [0011 控制单元](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/opdevg/Ascendcopdevg/atlas_ascendc_10_0011.html)、[0012 编程模型](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/opdevg/Ascendcopdevg/atlas_ascendc_10_0012.html) | 同上 | A | — |
| aclrtMemcpy：「实现内存复制」；「本接口会立刻进行内存复制，函数内部不会进行隐式的device同步或流同步」；kind：「预留参数，配置枚举值中的值无效，系统内部会根据源内存地址指针、目的内存地址指针判断…」（页内**无**「同步接口」的直述整句，同步语义由上述两句体现，引用时不得改写为「同步接口」）；Device 间复制须先 aclrtDeviceCanAccessPeer + aclrtDeviceEnablePeerAccess | [aclcppdevg_03_0105.html](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0105.html)（FetchURL 主文本 + curl 原始 HTML 双重核对） | 同上 | A | — |
| aclrtMemcpyAsync：「本接口是异步接口，调用接口成功仅表示任务下发成功，不表示任务执行成功…需调用同步等待接口（例如，aclrtSynchronizeStream）」；源/目的 64 字节对齐为各型号通用约束；kind 四枚举名（HOST_TO_HOST/HOST_TO_DEVICE/DEVICE_TO_HOST/DEVICE_TO_DEVICE）**并非该页参数表列出，而是约束条款中散见**（枚举定义需另查 aclrtMemcpyKind 页）；EP 形态不支持异步 H2H（返回 ACL_ERROR_RT_FEATURE_NOT_SUPPORT）；RC 形态 H2D/D2H/H2H 系统内部默认按 D2D 执行；Host 内存非 aclrtMallocHost 申请时行为不可预知 | [aclcppdevg_03_0106.html](https://www.hiascend.com/document/detail/zh/CANNCommunityEdition/82RC1alpha001/API/appdevgapi/aclcppdevg_03_0106.html)（同上双重核对） | 同上 | A | 同步版 kind 预留 vs 异步版 kind 有效为版本相关行为，引用必须带 8.2.RC1.alpha001 限定（B13-C13 修订：0105/0106 逐字精度） |
| Atlas 800T A2 用户指南 26·技术规格（表 3-1/3-2 逐字）：「支持8路华为自研昇腾910 AI处理器，芯片支持直出200G RoCE网络接口。**每一路AI处理器提供7条HCCS互连链路，最大理论带宽为392GB/s。** 每个NPU载板由8路AI处理器组成，通过HCCS组成一个8P Full mesh互联」；表 3-1：「容量为64GB。带宽为1600GB/s」（单个 AI 处理器片上内存口径）；「每个NPU通过PCIe 4.0 x16与CPU互联」；「支持4路鲲鹏920处理器」 | [support.huawei.com EDOC1100317202](https://support.huawei.com/enterprise/zh/doc/EDOC1100317202/f3dba488) | 文档 26；页面约 2026-09-18 更新；2026-10-08 复核（FetchURL 直取正文成功） | A（可变网页） | 392GB/s 是**每路 AI 处理器 7 链路的合计**口径，不是每链路、也不是整机；原文未标注单向/双向，每链路数值未单独给出（B13-C12 修订：正文曾误写 7×392GB/s）；老 910（Atlas 800/9000）为 3 链路 90GB/s，代际不混；第三方「单链路 200GB/s/2.4TB/s」禁用 |

## 候选新来源登记

`src.nvidia.h100-whitepaper-v1.01-mirror`、`src.nvidia.hopper-in-depth-blog-2022-03-22`、`src.nvidia.cuda-samples-bandwidthtest-2026-10-08`、`src.nvidia.h100-product-page-2026-10-08`（B13-C14 补登记）、`src.amd.cdna2-white-paper-2021`、`src.amd.mi200-isa-2022-02-04`、`src.amd.mi200-hotchips-hc34-2022`、`src.amd.hip-docs-6.3.3`、`src.amd.rocm-bandwidth-test-d7f5efe`（B13-C14 补登记，MIT，弃用声明版本）、`src.huawei.cann-82rc1alpha001-ascendc-aicore-arch-2026-10-08`、`src.huawei.cann-82rc1alpha001-acl-memcpy-2026-10-08`、`src.huawei.atlas-800t-a2-user-guide-26-2026-10-08`。复用已登记：src.nvidia.cuda-toolkit-12-8、src.huawei.cann-82rc1alpha001-acl-runtime-memory、src.pytorch.cuda-semantics-2.6、src.huawei.mindx-dl-60rc2-ascend-dmi-2026-09-29、src.huawei.atlas-800t-a2-product-2026-09-29。

## 缺口与冲突

- NVIDIA H100 白皮书无官方可驻留 URL（resources.nvidia.com 302 失效）：依赖第三方镜像+官方博客交叉，正文注明；显存带宽 3000 GB/s（preliminary）vs 产品页 3.35 TB/s 口径分列。
- AMD 白皮书提取截断：220 CU/880 Matrix Core 现由 Hot Chips deck（AMD 署名）支撑，正文注明出处层级；CDNA3/MI300 未取证（任务择一）。
- Ascend「架构规格」数值表未取到：0010 表 1 已经原始 HTML 内嵌数据补得六行存储单元描述（B13 复核），但各 buffer 容量、910B AI Core 数量仍只有二手资料，正文写「随型号、以 GetCoreMemSize/架构规格页为准」，禁止写具体数值；910B HBM 代际/容量按芯片级同样无官方版本化来源。
- Ascend 页头版本号未直核（JS 渲染），URL 路径版本=8.2.RC1.alpha001，沿用已登记同树页的版本核对结论。
- cuda-samples 的 LICENSE 未核；rocm_bandwidth_test 已核为 MIT（LICENSE.md，B13-C14 修订）。
- Ascend 侧 H2D/D2H/D2D/P2P 带宽测量工具为已登记 ascend-dmi（MindX DL 6.0.RC2），三平台验证方法统一引用。

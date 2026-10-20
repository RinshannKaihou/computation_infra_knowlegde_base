---
id: inference.mindie-execution-profile
title: MindIE 推理执行与配置样板
type: reference
domain: inference
status: draft
platforms: [ascend]
source_refs:
- src.ascend.mindie-llm-repo-69e5a5dd
- src.ascend.mindie-llm-docs-69e5a5dd
- src.ascend.mindie-llm-src-69e5a5dd
- src.ascend.mindie-llm-doc-latest
updated_at: "2026-10-20"
applicability:
  environment_refs: []
  notes: "未建立环境档案。证据锚定 MindIE-LLM 开源仓 master@69e5a5dd（release_notes 自述 MindIE LLM 3.1.0 正式版；推荐配套 CANN 9.0.1、MindCluster 26.0.0、Ascend Extension for PyTorch 26.0.0）。产品包（闭源部分）范围 unknown；目标部署组合须现场核验，本文不构成部署建议。"
verification:
  status: source_checked
  evidence_refs:
  - src.ascend.mindie-llm-docs-69e5a5dd
  - src.ascend.mindie-llm-src-69e5a5dd
  notes: "仅核对固定快照内文档与源码语义（锚点与 SHA-256 见 docs/research/batch-26-t07-03-sources.md）；未安装、构建或运行 MindIE，未执行量化脚本，无本库实测。"
summary: MindIE（LLM 3.1.0 文档线）的执行架构、config.json 配置语义档案、PD 混部/分离部署、日志与健康检查观测、首失败边界与最小验证设计，附 Qwen 可追溯样板。
related_ids:
- inference.engine-backend-boundaries
- inference.model-loading-and-readiness
- inference.execution-and-kv-cache
- inference.pd-disaggregation
- inference.quantization-and-quality
---

# MindIE 推理执行与配置样板

本页给出 MindIE 的实质执行与配置档案：架构分层、服务化 `config.json` 的逐段语义、PD 部署模式、观测手段与启动失败的第一证据。组件结构与三引擎对照见[引擎组件与平台功能交集档案](engine-backend-boundaries.md)，装载与启动序列见[权重加载、引擎 ready 与启动失败诊断](model-loading-and-readiness.md)——本页与两页互补，不重复其内容。

## 版本线与范围

- **版本锚点**：开源仓 master@`69e5a5dd` 快照；仓内 `release_notes.md` 自述 **MindIE LLM 3.1.0（正式版本，维护周期三个月）**，推荐配套 CANN 9.0.1、MindCluster 26.0.0、Ascend Extension for PyTorch 26.0.0、CCAE V100R026C10SPC100；兼容矩阵 3.1.0×CANN 9.0.0/9.0.1/9.1.0（Y，8.5.x 为"/"）。官方声明"各组件需要配套使用，请勿跨版本混用"。
- **同快照数值差异记录**：README 的版本说明表写 MindIE 软件 2.3.0↔CANN 8.5.0，与 release_notes 的 3.1.0 线数值不同——何者"过期"是本文推断（来源未作冲突裁定），本页仅声明**采信 release_notes 作为本文档线**；源码实现与产品包的实际版本映射保持 unknown。
- **文档站对应（有限证据）**：仓内有 Read the Docs/MkDocs 构建配置（`.readthedocs.yaml`＋`mkdocs.yml`，`docs_dir: docs/zh`，未锁定部署 commit）；`model_support_list` 仓内版与 latest 站点渲染经 Qwen2-7B-Instruct 行核对一致——这是**抽查页级一致**，不构成"整站对应本快照"的全局映射；latest 引用继续按页＋取回日期记录。
- **开源仓 vs 产品包**：本文档口径为开源仓（Python 框架 `mindie_llm`＋C++ 核心 `src/`）；服务化入口二进制与错误码参考属产品包/产品文档线，其归属为未确认推断（unknown）。

## 执行架构与运行模式

四层架构（[architecture_overview.md](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/developer_guide/architecture_design/architecture_overview.md)）：

| 层 | 职责 | 关键点 |
|---|---|---|
| Server | 服务化：OpenAI/vLLM/Triton 等协议经 Endpoint 封装转换，对外 RESTful | 业务面/内部面/指标面三接口分离（见 ServerConfig） |
| LLM Manager | 调度层：interface（模型实例管理、C++/Python 接口）＋engine（编排 scheduler/executor/worker）＋block manager（KV cache 内存分配）＋kv connector（跨卡/跨设备 KV 链路，支持多种池化后端） | 请求状态管理与任务调度 |
| Text Generator | 执行层：preprocess/generate/postprocess 工作流 | SpecDecoding、ChunkPrefill 特性 |
| Modeling | 后端：CustomLayer 算子编排＋Compilation 图引擎 | **ACLGraph 与 ATBGraph 两种图模式后端** |

运行模式由配置决定：`backendType`（**atb**＝加速库后端，默认；**torch**＝兼容 torch 框架）；`inferMode`（**standard**＝PD 混部；**dmi**＝PD 分离）；服务化（**run 包入口** `mindieservice_daemon`／**whl 包入口** `mindie_llm_server`，见 PD 节；二进制制品归属未确认）与离线推理（ATB Models 纯模型）两种使用形态。C++ 侧调度组件（策略族、块管理、pre/post 调度器）的结构与有限语义见[引擎组件档案](engine-backend-boundaries.md)。

## config.json 配置语义档案

结构：`Version`（1.0.0，不支持修改）/`ServerConfig`/`BackendConfig`/`LogConfig`/`EnableDynamicAdjustTimeoutConfig`；**读取时先校验文件大小∈(0MB,10MB]，否则读取失败**（[配置参数说明](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/service_parameter_configuration.md)）。

### ServerConfig（服务面）

- **接口三分离**：`ipAddress`（业务面，默认 127.0.0.1）/`managementIpAddress`＋`managementPort`（内部面，默认 1026）/`metricsPort`（指标面，默认 1027，**Prometheus 格式**）。绑定 0.0.0.0 默认禁止（三面隔离安全要求），需 `allowAllZeroIpListening=true` 显式打开并自担全零监管风险。
- **并发模型**：`maxLinkNum`（默认 1000、**推荐 300**）——maxLinkNum 个请求并发处理＋2×maxLinkNum 个排队，**第 3×maxLinkNum+1 个请求被拒绝**；1000 并发仅小模型/低序列长度受限支持。
- **安全**：`httpsEnabled`（默认 true）及业务/内部/指标三组 TLS 证书族；集群实例间通信 TLS（`interCommTLSEnabled`，inferMode=standard 时忽略后续参数）。
- **协议兼容**：`openAiSupport`（默认 "vllm"＝`/v1/chat/completions` 用 vLLM 兼容版本；其他值＝原生 OpenAI 版本；**支持热更新**）。
- **超时**：`tokenTimeout`（默认 600s）/`e2eTimeout`（默认 600s）——**PD 分离场景两者无效**；客户端 timeout 参数与之任一达到即超时并终止该请求推理。

### ModelConfig（模型面）

- `modelWeightPath`：路径下 `config.json` 须用户组/用户名与当前用户一致、**非软链接、权限不高于 750**，否则 **Server 启动失败**。
- `npuMemSize`（单 NPU 可申请 KV Cache 上限，GB）：**-1**＝自动分配，官方公式＝单卡总内存×分配比例（默认 0.8，`NPU_MEMORY_FRACTION` 可调）−单卡权重占用−运行时变量−系统占用；权重加载 OOM 时可调高比例或加卡；**>0**＝固定分配。**设置超过系统可分配最大显存会出现启动失败或启动卡死**；多模态不支持 -1（另给计算公式）；PD 分离场景仅 `backendType=atb` 可 -1。
- `worldSize`：单机场景须与使用 NPU 数相等；**PD 分离的 D 侧须与下发身份设置的卡数一致**（配置表 worldSize 行）；**多机场景 npuDeviceIds/worldSize 失效，实际卡号与总 Rank 数由 ranktable 确定**（混部页多机节）。
- `trustRemoteCode` 默认 false。
- PD 分离专用：`kv_trans_timeout`（D 节点拉 KV 超时，默认 10s，仅 PD 生效）、`kv_link_timeout`（KV 传输通信域建立超时，默认/建议 1080s，**重试直至成功或超时退出**）。

### ScheduleConfig（调度面）

| 参数 | 默认 | 语义要点 |
|---|---|---|
| templateType | Standard | **Standard＝PD 混部（P/D 各自组 batch）**；Mix＝SplitFuse 特性；**PD 分离场景该项无效**（配置表逐项声明） |
| cacheBlockSize | 128 | [1,128]，非 128 须为 16 的整数倍 |
| maxPrefillBatchSize / maxPrefillTokens | 50 / 8192 | **谁先达到各自上限即完成本次组 batch**；maxPrefillTokens 须≥maxInputTokenLen |
| prefillPolicyType / decodePolicyType | 0 | **只能配置为 0（FCFS）**——与源码工厂注释（当前 Prefill/Decode 只支持 FCFS）互证 |
| prefillTimeMsPerReq / decodeTimeMsPerReq | 150 / 50 | supportSelectBatch 时参与选择本轮 Prefill 或 Decode；**PD 分离场景无效** |
| maxBatchSize | 200 | 最大 decode batch（Atlas 300I Duo 上限 2000）；按 block 数计算约束 |
| maxPreemptCount | 0 | 配置表声明：>0 时限制一轮调度最多抢占数，且此时 cpuMemSize 不可为 0（源码配置校验确有该交叉条件）。**源码已核路径显示该计数门控的是 SWAP 模式选择**：FCFS 抢占先默认 RECOMPUTE，仅 swapNum<maxPreemptCount 且可换出时改 SWAP；块分配失败/首 token 场景的 Preempt 调用未见 ">0 总开关"——"0＝关闭全部抢占"不成立（文档声明与已核源码局部路径分立记录，不合并） |
| maxQueueDelayMicroseconds | 5000 | 排队到时即使未达 batch 上限也出队 |
| maxFirstTokenWaitTime | 2500ms | 达到后允许本轮抢占以缩首 token 延迟；**PD 分离不生效** |
| maxIterTimes / maxN | 512 / 128 | 全局最大输出长度 / 束宽与并行采样上限 |

### HealthCheckConfig（健康面）

`npuUsageThreshold`（0＝关闭；[1,100]＝开启并作阈值）。**健康检查方案**：每个 Server 实例周期性同步执行**虚拟推理（单 Token）＋NPU 利用率检测**，据结果在实例内更新三态——**健康**（虚拟推理正常）/ **繁忙**（虚拟推理失败且利用率≥阈值）/ **异常**（失败且＜阈值）。

## PD 部署（混部与分离）

- **模式**：`inferMode: standard`（混部，同实例服务 P 与 D）与 `dmi`（分离）。调度侧 P/D 角色对应 PDDSPolicy、KV 迁移对应 KVTransferSchedulePolicy（源码已核存在，见[组件档案](engine-backend-boundaries.md)）；dmi 的部署示例在配置表中指向**外部 MindIE Motor 开发指南**（含 HCCL 重传相关变量提示）——该指南未取证（unknown），分离部署依赖范围不建立结论。
- **单机混部前提**：NPU 驱动固件/CANN/PyTorch/ATB Models/MindIE 已装；容器场景共享内存≥1GB；Server 侧 Python3.11.x。可通过 `MIES_CONFIG_JSON_PATH` 环境变量提供配置文件。
- **多机混部（混部页多机节声明）**：单机显存容不下模型时多节点部署；**仅支持 Atlas 800I A2、最多 4 机 32 卡、不支持 Atlas 300I Duo**；多机时 npuDeviceIds/worldSize 失效（ranktable 决定）；**各节点默认采样参数不一致可能导致卡死**；节点间 TLS 证书族（interNodeTls\*）与 KMC 密钥配置。
- **3.1.0 特性叠加约束（release_notes）**：**PD 混部不能同时开启 Prefix Cache、SplitFuse 与 DP>1；PD 分离不受该限制**。
- **拉起（两入口分立）**：建议先用 MindStudio `msprechecker` 预检工具校验配置合法性；**run 包分支**的工作目录为 **`{MindIE安装目录}/latest/mindie-service`**（在该目录执行 `nohup ./bin/mindieservice_daemon > output.log 2>&1 &` 后台启动；**不能在 bin 目录启动**——bin 目录只读；前台命令原页另列）；**whl 包分支**入口为 `mindie_llm_server`，从安装目录开始、启动目录须可写。证书文件 chmod 400。二进制制品归属未确认（见版本线节）。
- **边界**：connector 实现与 KV 传输路径未从源码核（unknown）；与 vLLM PD（connector 注册表/ Mooncake 线）互不推断，见[PD 分离](pd-disaggregation.md)的既有边界。

## 观测：日志、指标与健康检查

- **日志格式**：`[date time] [pid] [tid] [组件名称] [大写日志级别] [file:line] : [error code] log message`；组件枚举 **motor/server/llm/llmmodels/sd**；分**安全审计日志**与**运行调试日志**两类；Critical/部分 Error 带错误码（错误码参考在 hiascend 产品文档线，未登记）。排障时以 `file:line` 与组件名定位层。
- **动态日志**：`dynamicLogLevel` 及生效时长/起始时间配置，运行期调整级别。
- **指标**：`metricsPort`（Prometheus 格式）暴露服务管控指标（指标清单未取证）。
- **健康检查**：见上节三态语义——这是**主动探测设计**（虚拟推理＋利用率），与 vLLM `/health` 的"死活标志"是不同证据类型，不可互相套用结论（见[加载页](model-loading-and-readiness.md)的 health/ready 区分）。

## 首失败边界与最小验证设计

| 类别 | 第一证据（文档口径） |
|---|---|
| 配置文件 | 大小∉(0MB,10MB] 读取失败；权限非 640；字段取值越界 |
| 权重/权限 | modelWeightPath 下 config.json 属组不一致/软链接/权限>750 → **Server 启动失败** |
| 内存 | npuMemSize 超过系统可分配最大显存 → **启动失败或启动卡死**；运行期 KV 不足的表现未在配置页给出（unknown） |
| 初始化 | 离线（ATB Models）模型初始化失败（用户自定义修改导致）需**手动结束进程** |
| 调度/执行 | 超时（tokenTimeout/e2eTimeout，PD 分离无效）→ Server 返回超时报错并终止该请求；抢占模式选择见 ScheduleConfig 节（文档与源码口径分立）；定向验证可观察日志字段：requestId/seqId/preempt mode/maxPreemptCount config/swapNum（观察项设计，非已观察结果） |

**最小验证设计**（绑定后文"可追溯样板：Qwen"节的候选样板记录；沿用[加载页](model-loading-and-readiness.md)骨架，MindIE 特有项替换）：身份五元组（含 config.json 关键字段值）→ 按样板走完整启动（可先 msprechecker 预检；whl 入口）→ ready 判据＝`Daemon start success!` 类启动成功日志（充分标志，未观察到须结合日志完整性与实际请求判断）＋确定输入请求成功 → 质量锚定任务/参考与阈值（见[量化与质量](quantization-and-quality.md)）→ **健康检查三态观察**（npuUsageThreshold>0 时记录一次周期检测结果与状态）→ 日志锚点采集（组件名＋file:line＋错误码有无；抢占场景加采 requestId/seqId/preempt mode/swapNum）→ 失败清理（进程终止＋设备/共享内存回收，含前述 /dev/shm 限定）→ 同环境重试一次。验证通过仅覆盖该样板记录的组合；样板未达可执行条件前（依赖版本/权重身份缺），本设计保持为计划。

## 可追溯样板：Qwen

[examples/atb_models/examples/models/qwen/](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen)（qwen/ 本身为文件目录；其父目录 models/ 共 36 个条目＝34 个模型目录＋2 个 Python 工具文件）：

- README 逐模型特性矩阵：800I A2 与 300I Duo 的 TP world size、FP16/BF16/PagedAttention/W8A8/W8A16/KV cache 量化/稀疏量化（仅 300I Duo）/MOE 量化/MindIE Service/长序列/prefix_cache/FA3/functioncall/MultiLoRA。同目录 `convert_quant_weight.sh`/`convert_quant_weights_72b.py` 与校准 prompt（`calib_prompt_14b/72b.json`、`anti_prompt_pdmix.json`）构成量化样板入口（脚本未运行）。
- **与模型支持列表的逐项对照（Qwen2-7B-Instruct）**：共同证据——两表 W8A8 均标支持。**卡数差异未消解**——README 行为 A2 TP 1/2/4/8、300I Duo TP 2/4/8（且 README 注明其为"对话测试可跑通配置，需考虑输入长度内存占用"）；[模型支持列表](https://mindie-llm-doc.readthedocs.io/zh-cn/latest/user_guide/model_support_list/)为 A2 1/2/4、300I Duo 1/2、A3 1/2。两表口径不同（测试配置 vs 支持分级），**不取并集、不判某表过期**；prefix_cache/MindIE Service 列仅 README 有，不能用支持列表互证。
- **候选验证样板（文档级绑定，未达可执行条件）**：模型 Qwen2-7B-Instruct（权重/tokenizer revision 待现场固定）；硬件 Atlas 800I A2，**选定 worldSize=2（支持列表推荐卡数；README 差异如上记录）**；并行 **TP**（TP 依据 Qwen README 的 A2 Tensor Parallelism 列；支持列表该列为"硬件规格"卡数、未明示并行语义）、**不做量化（BF16 原生；W8A8 为后续变体）**；dtype **BF16**（README：7B 建议 BF16；300I Duo 仅 FP16 故该硬件不适用）；backendType=atb、inferMode=standard、单机、whl 安装形态；依赖以"已装 CANN/PyTorch/Torch-NPU/ATB Models"为前提（各版本未定，逐项 unknown），另 README 要求 Qwen2 需 transformers≥4.40.1。**仍缺**：权重身份、阈值/资源基线、依赖版本映射——明确未达可执行条件，不宣称任何组合可运行。

上述最小验证设计（见前节）绑定本候选样板执行；样板未达可执行条件前，该设计保持为计划。

## 与 vLLM 的有证据对照（有限项）

- **健康语义**：MindIE＝周期性虚拟推理＋利用率三态（主动探测）；vLLM `/health`＝错误标志死活探针＋标准入口启动后可见。两者证据类型不同。
- **调度策略**：MindIE 配置层 prefill/decode 仅 FCFS（文档与工厂互证）；vLLM 有 FCFS/Priority 队列实现。不可推断 MindIE 无优先级需求场景的替代方案。
- **抢占**：MindIE 已核局部路径——RECOMPUTE 为默认模式，SWAP 受 swapNum<maxPreemptCount 门控（该计数限制 SWAP 选择，非总开关）；vLLM 已核局部链（分配失败→释放→回 waiting）。触发条件两侧均未全面核对。
- 其余组件/参数对照边界见[引擎组件档案](engine-backend-boundaries.md)（参数不同名不直译）。

## 来源与验证记录

- 固定快照 master@69e5a5dd：[架构总览](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/developer_guide/architecture_design/architecture_overview.md)、[配置参数说明（服务化）](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/service_parameter_configuration.md)、[PD 混合部署](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md)、[版本说明书](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/release_notes.md)、[日志简介](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/log/log_overview.md)、[离线推理](https://github.com/Ascend/MindIE-LLM/blob/69e5a5dd4b533eaffc7e198320435350825a36f7/docs/zh/user_guide/user_manual/offline_inference.md)、[Qwen 样板](https://github.com/Ascend/MindIE-LLM/tree/69e5a5dd4b533eaffc7e198320435350825a36f7/examples/atb_models/examples/models/qwen)。
- 当前验证范围：仅快照内文档/源码语义核对（SHA-256 见 [batch-26-t07-03-sources](../../docs/research/batch-26-t07-03-sources.md)）；未安装、构建或运行 MindIE，未执行量化脚本。
- 待确认：PD 分离 connector 实现；mindieservice_daemon 与错误码的产品包范围；motor/sd 组件归属；metricsPort 指标清单；多机 ranktable 细节；model_parameter_configuration 嵌套表；健康检查周期数值。

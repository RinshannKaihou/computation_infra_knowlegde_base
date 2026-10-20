# 第二十六批 T07-03 来源记录

任务：T07-03（MindIE 推理执行与配置样板；**new** reference `knowledge/07-inference/mindie-execution-profile.md`，主题 07.1/07.2/07.3/07.5）。取证轮次：主会话作者角色首轮（2026-10-20；前置 T07-02 已通过审阅闭环）。

版本选择口径（含版本 gate 收窄）：证据锚定 MindIE-LLM 开源仓 **master@`69e5a5dd`**（T07-01 轮钉扎的同一快照；codeload 整包 `1b67d0215ffc8dd0`）。本轮关键收窄：仓内 `docs/zh/release_notes.md` 自述 **MindIE LLM 3.1.0（正式版本，维护周期三个月）**，推荐配套 CANN 9.0.1、MindCluster 26.0.0、Ascend Extension for PyTorch 26.0.0、CCAE V100R026C10SPC100；兼容矩阵 3.1.0×CANN 9.0.0/9.0.1/9.1.0（Y）、×MindCluster 26.0.0/26.1.0/7.3.0（Y）。**同一快照内 README 的版本说明表（MindIE 软件 2.3.0↔CANN 8.5.0）与 release_notes（3.1.0 线）数值不同——何者"过期"为本文推断（来源未作冲突裁定），本轮采信 release_notes 为本文档线**（T07-01 轮登记的"2.3.0↔8.5.0"即该表）；源码实现与产品包的版本映射保持 unknown。文档站对应（审阅修订 T07-03-C01 收窄）：仓内有 Read the Docs/MkDocs 构建配置（`.readthedocs.yaml`＋`mkdocs.yml`，docs_dir 指向 docs/zh，未锁定部署 commit）；model_support_list 仓内 Markdown 与 latest 站点渲染经 Qwen2-7B-Instruct 行核对一致——**抽查页级一致，不构成整站对应快照的全局映射**；latest 引用继续按页＋取回日期记录。本轮未运行任何引擎。

## 本轮取回清单（2026-10-20，均为 master@69e5a5dd 快照内文件）

| 对象 | SHA-256（前 16 位） |
|---|---|
| docs/zh/developer_guide/architecture_design/architecture_overview.md | 069f3c6ad68d8c22 |
| docs/zh/user_guide/user_manual/service_parameter_configuration.md | 59f1dd120399191f |
| docs/zh/user_guide/user_manual/prefill_decode_mixed_deployment.md | 75bd1da15eb171f2 |
| docs/zh/release_notes.md | f4dddd5a096b4f68 |
| docs/zh/user_guide/log/log_overview.md | 578c37d87d0c84ae |
| docs/zh/user_guide/user_manual/offline_inference.md | c8c3b80637ac4b7b |
| docs/zh/user_guide/model_support_list.md（仓内版） | cebe1df8005841c3 |
| docs/zh/user_guide/user_manual/model_parameter_configuration.md | 7795bd4b958b90ab |
| examples/atb_models/examples/models/qwen/README.md | 09941aede58df7cc |

## 主张—来源定位表

| 主张 | 登记 ID | 精确位置 | 支持范围 / 未覆盖 |
|---|---|---|---|
| 四层架构与目录：Server（服务化，OpenAI/vLLM/Triton 协议经 Endpoint 转 RESTful）；LLM Manager（interface＋engine 编排 scheduler/executor/worker＋block manager＋kv connector 跨卡/跨设备 KV 链路）；Text Generator（preprocess/generate/postprocess，SpecDecoding、ChunkPrefill）；Modeling（CustomLayer＋Compilation，ACLGraph/ATBGraph 两图模式后端）。Python 核 mindie\_llm（text\_generator 插件：prefix\_cache/splitfuse/memory\_decoding/la；modeling/atb）与 C++ 核 src/ 双层 | NEW src.ascend.mindie-llm-docs-69e5a5dd | architecture\_overview.md（概述/架构介绍/目录结构节） | 架构与目录口径；各组件实现细节见复用条 |
| config.json 结构与读取：Version（1.0.0 不支持修改）/ServerConfig/BackendConfig/LogConfig/EnableDynamicAdjustTimeoutConfig；读取先校验文件大小∈(0MB,10MB] 否则失败；whl 与 run 包两种获取路径 | NEW src.ascend.mindie-llm-docs-69e5a5dd | service\_parameter\_configuration.md 头部 | 结构语义 |
| ServerConfig 关键项：ipAddress/managementIpAddress/metricsPort（默认 1027，Prometheus 格式指标）；allowAllZeroIpListening（默认 false，全零监管安全门）；maxLinkNum 并发模型（默认 1000、推荐 300：maxLinkNum 个并发＋2×maxLinkNum 排队，第 3×maxLinkNum+1 个请求被拒）；httpsEnabled＋TLS/内部接口/指标接口证书族；**inferMode：standard＝PD 混部、dmi＝PD 分离**；interCommTLSEnabled（集群实例间通信 TLS，inferMode=standard 时忽略后续参数）；openAiSupport（"vllm"＝/v1/chat/completions 用 vLLM 兼容版本，热更新）；tokenTimeout/e2eTimeout（PD 分离场景无效）；maxRequestLength；distDPServerEnabled（仅大规模专家并行生效）；HealthCheckConfig | NEW src.ascend.mindie-llm-docs-69e5a5dd | service\_parameter\_configuration.md ServerConfig 表 | 配置语义；运行行为未实测 |
| ModelConfig 关键项：modelInstanceType/modelName/modelWeightPath/worldSize/cpuMemSize/**npuMemSize**（-1＝按可用显存自动分配 KV Cache：单卡总内存×0.8（NPU\_MEMORY\_FRACTION 可调）−权重−运行时变量−系统占用；>0＝固定分配；**超限会出现启动失败或启动卡死**；多模态不支持 -1（另有公式）；PD 分离仅 backendType=atb 可 -1）/**backendType**（atb＝加速库后端、torch＝兼容 torch 框架）/trustRemoteCode（默认 false）/**kv\_trans\_timeout**（PD 分离 D 节点拉 KV 超时，默认 10s，仅 PD 生效，≤0 自动改 1）/**kv\_link\_timeout**（KV 传输通信域建立超时，默认/建议 1080s，重试直至成功或超时退出） | NEW src.ascend.mindie-llm-docs-69e5a5dd | service\_parameter\_configuration.md ModelConfig 表（npuMemSize/backendType/kv\_\* 行） | 配置语义与官方口径的内存公式 |
| ScheduleConfig 关键项：templateType（Standard＝PD 混部各自组 batch／Mix＝SplitFuse）；templateName（Standard\_LLM）；cacheBlockSize（[1,128]，默认/建议 128，其他值须 16 整数倍）；maxPrefillBatchSize（默认 50）与 maxPrefillTokens（默认 8192，须≥maxInputTokenLen）**谁先达到谁完成本次组 batch**；prefillTimeMsPerReq（150）/decodeTimeMsPerReq（50）在 supportSelectBatch 时参与选择 P 或 D；**prefillPolicyType 与 decodePolicyType 只能配置为 0（FCFS）**——与源码工厂注释互证；maxBatchSize（默认 200，Atlas 300I Duo≤2000；按 block\_num 计算约束）；maxIterTimes（512）；**maxPreemptCount（配置表声明：>0 时限制一轮调度最多抢占数且 cpuMemSize 不可为 0；源码已核路径显示该计数门控 SWAP 模式选择——FCFS 抢占默认 RECOMPUTE、仅 swapNum<maxPreemptCount 且可换出改 SWAP，未见 >0 总开关，"0＝关闭全部抢占"不成立——审阅修订 T07-03-C02，文档与源码口径分立；定向验证可观察日志字段 requestId/seqId/preempt mode/maxPreemptCount config/swapNum）**；maxQueueDelayMicroseconds（5000us，排队到时即使未达 batch 上限也出队）；maxFirstTokenWaitTime（2500ms，达到后允许本轮抢占以缩首 token 延迟；PD 分离不生效——maxQueueDelayMicroseconds 原表无此声明）；templateType 与 prefill/decodeTimeMsPerReq 在 PD 分离无效（配置表逐项声明，审阅补 T07-03-C03）；worldSize 单机须等于 NPU 数、PD 分离 D 侧须与下发身份设置的卡数一致（ModelConfig 表 L128）、多机由 ranktable 决定且 npuDeviceIds/worldSize 失效；maxN（束宽/并行采样上限） | NEW src.ascend.mindie-llm-docs-69e5a5dd | service\_parameter\_configuration.md ScheduleConfig 表 | 文档版调度语义；与源码已核路径（T07-02）互证 |
| HealthCheckConfig：npuUsageThreshold（0＝关闭；[1,100]＝开启并作 NPU 利用率阈值）。**健康检查方案＝每个 Server 实例周期性同步执行虚拟推理（单 Token）＋NPU 利用率检测**，据结果在实例内更新三态：健康（虚拟推理正常）；繁忙（虚拟推理失败且利用率≥阈值）；异常（失败且＜阈值） | NEW src.ascend.mindie-llm-docs-69e5a5dd | service\_parameter\_configuration.md HealthCheckConfig 节 | 配置与判定语义；检测周期数值未见表 |
| PD 混合部署：单机混部（前提：NPU 驱动固件/CANN/PyTorch/ATB Models/MindIE 已装；容器共享内存≥1GB；Server 侧 Python3.11.x）；MIES\_CONFIG\_JSON\_PATH 环境变量提供配置；modelWeightPath 下 config.json 须用户组/用户名与当前用户一致、非软链接、权限不高于 750，否则 **Server 启动失败**；证书文件 chmod 400；建议 MindStudio msprechecker 预检工具校验配置合法性；权重拷贝到 modelWeightPath；**两入口分立**——run 包工作目录为 `{MindIE安装目录}/latest/mindie-service`（在该目录 `nohup ./bin/mindieservice_daemon > output.log 2>&1 &` 后台启动；**不能在 bin 目录启动**；前台命令原页另列）、whl 包入口 `mindie_llm_server`（从安装目录开始，启动目录须可写；daemon 制品归属未确认推断）；多机混部（**仅 Atlas 800I A2、最多 4 机 32 卡、不支持 300I Duo；各节点默认采样参数不一致可能卡死**；interNodeTls\* 证书族、KMC 密钥；ranktable 决定卡号与总 Rank）；**3.1.0 叠加约束：PD 混部不能同时开 Prefix Cache、SplitFuse 与 DP>1（PD 分离不受限）**；dmi 部署示例指向外部 MindIE Motor 开发指南（未取证） | NEW src.ascend.mindie-llm-docs-69e5a5dd | prefill\_decode\_mixed\_deployment.md（单机混部前提/操作步骤 L117–131 whl、L256–287 run、多机混部节 L305–346）；release\_notes.md L97–99；service\_parameter\_configuration.md L128/L133 | 文档级 PD 支持证据来自混部页＋配置表＋release\_notes（本轮未取证独立的分离部署专页）；connector 实现与 Motor 指南未核（unknown） |
| 日志观测：格式 `[date time] [pid] [tid] [组件名称] [大写日志级别] [file:line] : [error code] log message`；组件枚举 motor/server/llm/llmmodels/sd；安全审计日志与运行调试日志两类；Critical/部分 Error 带错误码，错误码参考在 hiascend 产品文档线（mindie/300，未登记）；LogConfig 支持动态日志（dynamicLogLevel 及生效时长/起始时间） | NEW src.ascend.mindie-llm-docs-69e5a5dd | log\_overview.md（日志分类/记录格式节）；service\_parameter\_configuration.md LogConfig | 格式与分类；各级别字段细则未全摘 |
| 版本线：MindIE LLM 3.1.0 正式版；配套矩阵（CANN 9.0.0/9.0.1/9.1.0；MindCluster 26.0.0/26.1.0/7.3.0；CCAE 三线）；"各组件需要配套使用，请勿跨版本混用"；**README 版本表（2.3.0↔CANN 8.5.0）与 release_notes 数值不同（何者过期为本文推断、来源未裁定）** | NEW src.ascend.mindie-llm-docs-69e5a5dd | release\_notes.md（版本配套说明/兼容性表）；README 版本说明表 | 采信 release_notes 为本文档线；实际安装组合未验证 |
| 离线推理（ATB Models 纯模型）：模型初始化失败时（用户自定义修改导致）需手动结束进程；权重路径及文件须保证其他用户无写权限；README 三类文档体系（推理流程/特性/调测定位） | NEW src.ascend.mindie-llm-docs-69e5a5dd | offline\_inference.md（前提/约束/README 解读节） | 文档口径 |
| Qwen 模型样板（可追溯 example）：examples/atb\_models/examples/models/qwen/README.md 给逐模型特性矩阵（800I A2 与 300I Duo 的 TP world size、FP16/BF16/PagedAttention/W8A8/W8A16/KV cache 量化/稀疏量化/MOE 量化/MindIE Service/长序列/prefix\_cache/FA3/functioncall/MultiLoRA）；**Qwen2-7B-Instruct 与模型支持列表逐项对照（审阅修订 T07-03-C05）：共同证据仅 W8A8 两表均支持；卡数差异未消解**——README 行 A2 TP 1/2/4/8、300I Duo TP 2/4/8（README 注明为对话测试可跑通配置），支持列表为 A2 1/2/4、300I Duo 1/2、A3 1/2，不取并集不判过期；prefix\_cache/MindIE Service 列仅 README 有；README 另注 Qwen2 需 transformers≥4.40.1、7B 建议 BF16、300I Duo 仅 FP16；qwen/ 为文件目录（README＋convert\_quant\_weight 脚本＋校准 prompt anti\_prompt\_pdmix/calib\_prompt\_14b/72b，无子目录），父目录 models/ 36 个条目＝34 目录＋2 个 Python 文件（审阅修订 T07-03-C08） | 扩展 src.ascend.mindie-llm-src-69e5a5dd（notes） | examples/atb\_models/examples/models/qwen/（README＋脚本清单；models/ 共 36 个条目（34 目录＋2 个 Python 文件）） | 样板存在性与矩阵口径；脚本执行未运行 |
| 组件结构背景（scheduler 策略族/block\_manager/engine/pre-post 调度） | 复用 src.ascend.mindie-llm-src-69e5a5dd、src.ascend.mindie-llm-repo-69e5a5dd、src.ascend.mindie-llm-doc-latest | （既有，T07-02 轮） | 本轮未重开 |

## unknown 清单

1. src/ C++ 实现层（llm_engine 执行流细节、模型侧 CacheManager 的 block 数计算实现）未逐行核——T07-02 已覆盖组件结构，本轮以文档语义与配置口径为主。
2. PD 分离（dmi）的 KV connector 实现与传输路径未从源码核（KVTransferSchedulePolicy 存在已核；kv_trans/kv_link 超时语义来自配置文档）。
3. 日志组件枚举中 motor、sd 的组件归属（MindIE Motor/其他产品件？）未取证；错误码参考在 hiascend 产品文档线（mindie/300）未登记。
4. MindIE 产品包（闭源部分）功能范围仍 unknown；服务化二进制 mindieservice_daemon 的实现不在开源仓（仓内为 mindie\_llm 框架与 C++ 核心，daemon 属产品包制品——此为推断，标注待核）。
5. performance\_tuning.md 与日志内容配置细则页未逐项摘录；观测指标（metricsPort 的指标清单）未取证。
6. 多机混部的 ranktable/组网细节未逐项核对。
7. model\_parameter\_configuration.md 的嵌套参数表未逐项摘录（仅登记哈希）。
8. 未运行任何引擎、服务或量化脚本；全部为文档/源码口径，无本库实测结果。

## 集成轮结果（2026-10-20 已执行）

- 新登记 1 项：src.ascend.mindie-llm-docs-69e5a5dd（仓内 docs 树固定快照；许可按 README 声明的 CC BY-SA 4.0 登记，声明范围解释保留）。
- 扩展 1 项：src.ascend.mindie-llm-src-69e5a5dd 的 notes 补 Qwen example 样板（examples 源码属木兰 PSL-2 scope）。
- registry 537→538；T07-03 正文进入撰写轮。readthedocs latest gate 的记录口径（抽查页级一致，不构成整站对应快照的全局映射——首轮"站点＝仓内 docs 构建、取回对应 69e5a5dd"的判断已在审阅修订中撤回收窄）同步记入 MindIE 文档条目 notes。

# 第九批来源记录：通信带宽退化证据（R2-05）

研究日期：2026-09-30。目标正文：`knowledge/03-communication/bandwidth-degradation-triage.md`（procedure）。行号按固定 commit 原文件核对（raw URL + codeload tarball 交叉）；主任务抽查确认 nccl-tests common.cu 的 deltaSec 计算（L795–801）、NCCL_TESTS_MIN_BW（L1931）与 util.cu 页脚输出（L897–908）。未构建或运行任何测试工具。

## 主张—证据表（nccl-tests 固定 commit b4d5beeb）

| 主张 | 证据位置 | 类型 | 反证/未知 |
|---|---|---|---|
| algbw = S/t；busbw 由 algbw 乘集合类型修正因子，用于与硬件峰值比较；因子表：AllReduce 2(n-1)/n、ReduceScatter/AllGather/AlltoAll (n-1)/n、Broadcast/Reduce 1 | doc/PERFORMANCE.md L18–20、L24–29、L136–143；实现 src/all_reduce.cu L59–65 | 文档+源码 | busbw "reflect the speed of the hardware bottleneck" 是设计意图而非测量保证 |
| 主计时是 host 端墙钟（std::chrono::steady_clock），计时区间为整个 iters 循环除以 iters*agg_iters；CUDA events 仅用于 -I 逐迭代统计；CUDA Graph 模式 deltaSec 另除以 graph launch 次数 | src/timer.cc L8–21；src/common.cu L756–771、L795–801、L666–695（主任务抽查确认） | 源码 | 与旧版每迭代 event 计时行为不同；只对该 commit 成立 |
| 每个 size 同时跑 out-of-place 与 in-place 两列；迭代内偏移轮转避免缓存效应 | src/common.cu L958–959、L557–560；表头 src/util.cu L867–880 | 源码 | — |
| -c 的正确性校验在计时循环之外单独执行，不进报告的 time/algbw/busbw；-c 0 时跳过 initData、#wrong 列输出 N/A | src/common.cu L757–771、L800、L811、L823–824、L831–884、L722–725；src/util.cu L604–608 | 源码 | README 只说 "quite slow"，"不影响带宽" 为源码级结论 |
| "Out of bounds values: N FAILED/OK" = 出现数据校验错误的测量行数；N>0 → FAILED 且退出码非 0；名称易误读为"数组越界" | src/util.cu L901（主任务抽查确认）、src/common.cu L492、L1955–1956 | 源码 | README/PERFORMANCE.md 未解释该字段；语义为源码推断 |
| 页脚 "Avg bus bandwidth" 与环境变量 NCCL_TESTS_MIN_BW 比较，低于其 90% 判 FAILED；该变量无 README 文档 | src/common.cu L1931–1932、src/util.cu L902（主任务抽查确认） | 源码 | — |
| 其他口径开关：-I 与 -G 不兼容；-C 报 CPU time；-z blocking 0/1/2/3；-T 超时；多组并行报告的是每组带宽；内存不足自动下调 maxBytes（"Reducing maxBytes … due to memory limitation"） | README.md L82–96、L103、L106、L126；src/common.cu L1636 | 文档+源码 | maxBytes 自动下调是基线对比易忽略的口径漂移 |

## 主张—证据表（NCCL 2.27.5 归档 User Guide）

| 主张 | 证据位置 | 类型 | 反证/未知 |
|---|---|---|---|
| NCCL_DEBUG=VERSION/WARN/INFO/TRACE；NCCL_DEBUG_SUBSYS 默认 INIT,BOOTSTRAP,ENV，子系统含 GRAPH（拓扑检测与图搜索）、TUNING（算法/协议调优）、P2P、SHM、NET、NVLS、RAS、ALL | env.html §NCCL_DEBUG、§NCCL_DEBUG_SUBSYS | 版本化文档 | 文档不给日志行样例 |
| NCCL_ALGO（Ring/Tree/Collnet*/NVLS*/PAT 等，版本门限各异；^ 排除；2.24+ func:algo 语法；默认自动选）；NCCL_PROTO（LL/LL128/Simple；官方劝阻设置；不支持 LL128 的平台强行开启可致 data corruption） | env.html §NCCL_ALGO、§NCCL_PROTO | 版本化文档 | — |
| 传输选择：P2P（NVLink/PCI）由 NCCL_P2P_DISABLE/NCCL_P2P_LEVEL 控制；SHM 为 P2P 不可用时经 host memory，NCCL_SHM_DISABLE 后跨 socket 走网络；NET 由 NCCL_NET/NCCL_IB_DISABLE 控制 | env.html 各小节 | 版本化文档 | — |
| IB 相关：NCCL_IB_TIMEOUT（默认 20 since 2.23）、NCCL_IB_RETRY_CNT（默认 7）、NCCL_IB_RETURN_ASYNC_EVENTS（since 2.23，IB 事件以 warning 报出）、NCCL_IB_ADAPTIVE_ROUTING、NCCL_IB_ECE_ENABLE、NCCL_CROSS_NIC 等 | env.html 各小节 | 版本化文档 | 配置语义证据；降速/重传计数器不在 NCCL 文档 |
| 带宽低于预期的官方排查（散落 troubleshooting.html）：GPU Direct 段建议 p2pBandwidthLatencyTest/nvbandwidth；ACS/IOMMU 重定向可致显著性能下降或 hang（lspci -vvv \| grep ACSCtl）；拓扑检测段：VM/容器虚拟 PCI 拓扑会 sub-optimal；跑 NCCL 前先跑 ib_write_bw；memlock 限制；RoCE GID（2.21+ 动态）；网卡 UP 不可达会 init 失败或 hang | troubleshooting.html §GPU Direct、§PCI Access Control Services、§Topology detection、§Networking issues | 版本化文档 | 无独立"性能排查"章节；NUMA 仅以 NCCL_P2P_LEVEL 语义间接出现 |
| RAS 章节实际路径 troubleshooting/ras.html（顶层 ras.html 404）：since 2.24 默认启用；ncclras 客户端 localhost:28028，STATUS/VERBOSE STATUS/TIMEOUT；输出含 Communicators 表（Status RUNNING/INIT/FINALIZE，Errors OK/MISMATCH/INCOMPLETE/DEAD/TIMEOUT）；MISMATCH 例为各 rank collective 计数不同——可提示慢 rank/进度分叉，**但官方示例说明活跃通信期间的计数差异可能是正常瞬态，初始化/销毁过渡也可能暂时出现；对同一 communicator、相同阶段连续查询，并与该负载正常基线比较；计数持续不推进才值得调查**；进程 60 秒不可达判 DEAD（Codex 代审 B09-C04 修订点） | troubleshooting/ras.html §Principle of Operation/§RAS Queries/§Sample Output；env.html §NCCL_RAS_* | 版本化文档 | 无链路级硬件计数器，只覆盖 hang/crash/进度不一致 |

## 主张—证据表（HCCL 侧）

| 主张 | 证据位置 | 类型 | 反证/未知 |
|---|---|---|---|
| cann-hccl 2d685b08 仓库内没有 HCCL Test 结果解释/带宽参数文档：docs/ 只有九个算法页，test/README.md 仅 2 行占位；docs/README.md 把结果解释指向外部《HCCL性能测试工具用户指南》 | gitee git/trees API（truncated: False）；docs/README.md；test/README.md | 源码仓取证 | — |
| 算法页定性表述：NHR 页称大流量场景 RHD 每阶段链路变化可能引起交换机流量冲突导致带宽下降；AHC 页给含收敛比 C 的 α/β/γ 公式；Mesh 页称利用双工链路双向带宽 | docs/NHR.md L5；docs/AHC.md L5/L10/L32；docs/Mesh.md L9 | 源码仓文档 | 定性描述，无测量方法 |
| CANN 9.1.X《HCCL性能测试工具》：仅支持基于 HCCL 单算子 API 的网络性能测试；"集合通信带宽指的是算法带宽，即执行某集合通信操作时的数据量/耗时"；影响因素：链路物理带宽+算法编排 | HCCLpertest_16_0001.html §工具介绍/§背景知识 | 版本化文档（新登记 src.huawei.hccl-perf-test-guide-cann-9.1.x） | 与 nccl-tests busbw 口径不同，无 bus 带宽列 |
| 参数口径：-b/-e 默认 64M；-i 步长（默认 (max−min)/10），-f 乘法因子，-i 0 固定 -b 持续测；工具对 -b/-e/-i 输入做地址对齐或 rank size 倍数微调；-n iters 默认 20；-w warmup 默认 10 不参与统计（首轮 socket 建链等）；-t onlydevicetime 仅统计 Device 侧耗时（约束 AIV/CCU 模式、HCCL_BUFFSIZE>100MB、-w/-n≤100）；-c 0/1/2 默认 1（大规模集群开启校验增加耗时） | HCCLpertest_16_0005.html §命令格式/表3 | 版本化文档 | avg_time 计时实现（Host/Device、跨 rank 归约）无源码证据，标未知 |
| 结果字段：data_size（单个 NPU 上参与通信的数据量，Bytes）、avg_time(us)、alg_bandwidth(GB/s)、check_result（success/failed/NULL；-c 0 → NULL；溢出或超出可精确表达范围 → NULL，附各 op×dtype 最大可校验卡数表）；校验原理=固定输入校验输出 | HCCLpertest_16_0006.html §结果说明 | 版本化文档 | — |
| -p x 从 Device ID 0 连续启动 x 个 Device；各产品取值范围（950: 1-8；A3: 1-16；A2: 1-8；Atlas 训练: 1/2/4/8 等）；执行前提：关闭防火墙、调 somaxconn/tcp_max_syn_backlog、ulimit -n 65535、950 需 hccl_rootInfo.json | HCCLpertest_16_0007.html §规格约束；HCCLpertest_16_0004.html §前提条件 | 版本化文档 | — |

## 口径对照（本库归纳）

nccl-tests：host 墙钟 + -a 跨 rank 归约（默认 avg），有 busbw 修正因子，-c 校验不进计时。HCCL Test：avg_time + alg_bandwidth（无 busbw），warmup 默认 10 不计入，-t 可切 Device-only 计时，-c 进结果字段。两边数字不可直接互比；且 HCCL Test 会对输入数据量做对齐微调，nccl-tests 会在内存不足时下调 maxBytes——基线对比前必须固定这些口径。

## 未解决与抓取失败

- HCCL Test 计时实现未知（源码随 CANN 安装包分发，未获取）。
- 链路退化的直接计数器（IB perf counters、交换机遥测、光模块/HCCS 计数）无已核对来源，procedure 的"真实链路退化"支路证据链有缺口，正文如实标注。
- NCCL_DEBUG=INFO 日志行格式无官方样例。
- hiascend 为 SPA + cookie 反爬，正文经 cookie jar + __NUXT_DATA__ 解码提取，无行号；引用定位用页面 ID + 小节/表名。
- 0008 页 301 跳 0009；0009–0012 为 FAQ 与环境类条目，与带宽解释无关。

# 第十一批来源记录：弹性训练与成员变更（R2-11）

**2026-10-08 修订注记：** Codex `gpt-6.1-sol / xhigh` 按 B11-C03 修正本记录并完成[定向复核](batch-10-11-12-codex-recheck.md)。下述原研究者、首次获取方式与当时任务状态为历史；修订补读和保留的未知条件见本记录及复核报告。

研究日期：2026-09-30（子代理完成）。目标正文：`knowledge/06-training/elastic-training-and-membership.md`（concept）。PyTorch 侧为 2.6 版本化文档（锚点经原始 HTML id 核验）；MindSpeed-LLM 侧为 v2.2.0 固定 commit `53f3639c3da9c000a187c44cc0c08d55026ddded`。两者版本体系不同（该 tag README 指向 PyTorch 2.7.1），只能机制对照，不拼配套。

## 主张—证据表（PyTorch 2.6 elastic）

| 主张 | 证据位置 | 反证/未知 |
|---|---|---|
| rendezvous = 同步原语 + 对等发现，五项功能：Barrier（min 节点加入才放行、max 立即完成、min 未达有整体超时且 non-retryable）、Exclusivity（同一 job 任意时刻只允许一个节点组）、Consistency（成员就 membership 与 rank 达成一致，rank 不稳定）、Fault-tolerance（rendezvous 中节点失败自动 re-rendezvous）、共享 KV store（仅本次成员共享） | docs/2.6/elastic/rendezvous.html 顶部叙述区与 #dynamic-rendezvous | 状态图图片未文本化读取 |
| 内置后端：c10d（推荐，基于 TCPStore）、etcd-v2、etcd legacy（将移除）；etcd 需服务端 v2 API | rendezvous.html 各小节；run.html #note-on-rendezvous-backend | — |
| RendezvousTimeout 默认：join 600s、last_call 30s、close 30s | rendezvous.html 参数表 | heartbeat 默认值该表未给 |
| 失败模式：worker 失败后全组停止并按实际 max_restarts 预算重启；agent 失败=本地 worker 组失败，由 job manager 决定整作业失败或换节点；node departure/arrival 时 agent 停全部 worker、组建新 WorkerGroup、以新 RANK/WORLD_SIZE 重启。默认预算依入口：torchrun CLI 为 0，WorkerSpec API 为 3 | run.html #failure-modes、#membership-changes；[固定 run.py L490–497](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/run.py#L490-L497)、[api.py L78–86](https://github.com/pytorch/pytorch/blob/1eba9b3aa3c43f86f4a2c807ac8e12c4a7767340/torch/distributed/elastic/agent/server/api.py#L78-L86) | B11-C03 修正：示例 max-restarts=3 非 CLI 默认；实际命令行/环境覆盖需记录；“谁通知 agent”未展开 |
| 语义边界：失败或成员变更时幸存 worker 全部被立即杀死；训练进度恢复完全依赖应用自己的 checkpoint，频率取决于容忍度；RANK 不稳定、禁止硬编码 RANK/LOCAL_RANK 对应；elastic（min≠max）时禁止硬编码 WORLD_SIZE；仅支持同质 LOCAL_WORLD_SIZE | run.html #important-notices | — |
| 训练脚本要求自带 load_checkpoint/save_checkpoint；任意 worker 失败时以相同参数重启全部 worker，丢失最近 checkpoint 之后的进度 | elastic/train_script.html | torchelastic 不保存/恢复训练状态是多条原文的合成结论，写作时并列引用 |
| 错误三分类：User Error（Input Error / Worker Failure=worker 子进程失败）、Platform Error（agent 自身）、Infra Error（agent/worker 域之外如宿主机）；@record 写 TORCHELASTIC_ERROR_FILE，agent 聚合上报时间戳最小者（"Root Cause" 启发式）；**2.6 的失败记录类名是 ProcessFailure，页面无 WorkerFailure 旧名** | elastic/errors.html；run.html #important-notices | — |
| LocalElasticAgent 的 exit_barrier_timeout（默认 300s）防止把先正常退出的 worker 误判为 scale-down | elastic/agent.html #implementations | — |
| WorkerState：worker 组作为整体变状态；单 worker 失败即整组 failed；UNKNOWN 态不可恢复 | elastic/agent.html #concepts | — |

## 主张—证据表（MindSpeed-LLM v2.2.0 high_availability.md，86 行全文核对）

| 主张 | 行号 | 反证/未知 |
|---|---|---|
| 副本机制底座：DP 组切成两个副本 DP 组，优化器状态均有备份；内存占用增加（bf16 grads 4+32/d vs 分布式优化器 4+16/d）；推荐千卡及以上集群 | L5、L26、L30–35 | “千卡及以上”是推荐语非硬约束 |
| TTP 临终遗言：故障后校验优化器中间状态完整性/一致性，生成临终 checkpoint，恢复可回到故障前一刻 | L7–9 | “故障前一刻”的精确 step 语义未定义 |
| UCE Step 级重计算：NPU 卡内存 UCE 故障实时检测，检测到后基于副本在线修复故障卡并继续训练；开关 --enable-hbmfault-repair（要求全局至少存在一个故障卡的副本卡） | L11–13、L51 | “实时检测”的实现层级（芯片/驱动/框架）未指明 |
| 弹性训练：故障且无空闲资源时基于副本缩掉部分节点继续训练；有空闲资源时再扩容回原规模；**仅支持 DP 粒度缩扩**；开关 --enable-elastic-training（剔除故障卡所在 DP 域对应节点；要求未故障节点中至少一份完整优化器数据；需配合 MindCluster 组件） | L15–18、L57 | 缩扩由谁驱动、通信组如何重建，文档未述，属未知 |
| 依赖 mindio_ttp 与 taskd 两个 whl（附外链）；HIGH_AVAILABILITY=dump/retry/recover/elastic-training 环境变量优先级高于命令行 | L41–45、L61–69 | 外链未核对 |
| 弹性专属四条约束：① 须开 enable-high-availability、use-distributed-optimizer；② 不支持 use-custom-fsdp、reuse-fp32-param；③ 仅支持 DP/TP/PP 并行；④ 缩容后不可再次缩容，扩容仅支持回到原有规模 | L75–84 | — |
| 通用约束：ptd 切分 DP size>1；MoE 稠密/稀疏层 DP size 均>1；长序列 dp_cp_size>1 | L71–73 | — |
| 实现入口确认：features_manager/high_availability/high_availability.py 注册五开关（L10–21）；validate_args 在代码层强制 mindio_ttp/taskd 导入、HA 先于弹性、use_distributed_optimizer、拒绝 use_custom_fsdp/reuse_fp32_param/EP>1/CP>1，另有文档未列的断言：HA 与 use_dist_ckpt 冲突（L37–38）、与 swap_optimizer 冲突（L39–40）；patches patch torch.distributed 集合通信与 Megatron 初始化入口 | high_availability.py L1–120 | L120 之后未读；L86 外链《MindIO TTP 约束限制》未读 |
| tests/ut 与 tests/st 无 HA 专项目录 | 目录列举 | tests/0day、poc、pipeline、coverage、test_tools 未枚举，不能断言全仓库无 HA 测试 |

## 未解决与抓取失败

- GitHub 未认证 API 一度 rate limit，改 gh api 完成；无其他抓取失败。
- TTP 临终 checkpoint 的时间语义、UCE 检测实现层级、弹性缩扩的内部驱动方均未定义。
- elastic/run.html 的 #launcher-api 全参数表、quickstart、metrics 页未逐字读。

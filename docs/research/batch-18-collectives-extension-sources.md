# 第十八批 T03-04 集合通信扩展来源记录

任务：T03-04（修订 `collectives-and-rank-progress.md`，只做加法）。取证日期 2026-10-09。版本各自为样板，不拼同一环境。

## 候选来源（4 项新登记 + 复用）

新登记：thakur-collective-mpich-2005（α–β 模型，历史 cutoff 不移植）、patarasuk-allreduce-2009（环带宽最优边界）、mpi-man-4.1（等长/变长行为样板）、megatron-core-dev-guide（latest 未冻结，drafting 前固定 tag；DP/TP/PP/EP 映射样板）。复用 nccl-user-guide-2.27.5（collectives/p2p/env 行级）、distributed-2.8（变长规则、DDP/FSDP）、hccl-api（原语约束、执行流程）。

## 主张—来源定位表

六原语数据流（NCCL collectives/p2p + torch + MPI 对照）；NCCL 等长契约与框架叠加约束；α–β 模型与假设；无固定最优算法；NCCL ALGO/PROTO 名单与自动选择；HCCL 原语约束与执行层；选定实现映射（DDP/FSDP/Megatron/DeepSeek MoE 组网表）；错序/超时边界维持。

## unknown 清单

HCCL 主机返回边界；HCCL 算法选择机制；NCCL 实际算法未取证；三源不拼环境；Megatron latest 未冻结；框架外推禁止；S26 推理侧不挪用；数值语义未取证；MPI 规范固定；RCCL 留 T03-05/06。

## 2026-10-10 修订（B18-C13–C15）

- C13：ring all-reduce 精确式 `2(p−1)α + 2((p−1)/p)nβ + ((p−1)/p)nγ`（大 p 近似另列；p=2 差一倍警示）；记号 p/n/lg-ceil/二次幂分支/单端口无竞争前提逐行补齐；Patarasuk 环轮次接入模型注明为推导；Rabenseifner 行维持（论文相应条件有依据）。
- C14：补六类 ASCII 图（all-reduce/reduce/broadcast/all-gather/reduce-scatter/all-to-all 转置）+ send/recv 五模式说明；实现冻结 Megatron-LM tag core_v0.19.2（mappings.py 类函数、p2p_communication.py P2PCommunicator、parallel_state.py 四组 getter 均复核 raw 200）；表改逐调用 shape×dtype/组/条件；DeepSpeed 引用移除；EP 消息字节/路由继续 OPEN；in-place 按 2.8 签名区分 + NCCL 未转录记 unknown。
- C15：`## 四种"进度"不能互相代替` H2 与说明段落分开。

## 2026-10-11 第二轮修订（B18-C13、C14）

- C13：ceil 限二项树文本支持，不跨算法迁移；recursive-doubling 非二次幂额外步骤另行推导；ring/ring all-reduce 等分条件（不等分 unknown）；Rabenseifner ceil 限本算法结构。
- C14：PP 修正（is_single_shape 仅 Python 检查 L131–137；真实 shape 通信限 variable_seq_lengths/mtp_standalone L322–328）；表改逐调用核算（DDP 桶/广播、FSDP chunk/完整输出、TP 各原语输入输出口径与 splits、PP tensor_shape 条件、EP OPEN）；六图全画（all-reduce/reduce-scatter 四 rank；send/recv 基本对+融合）；变长逐对匹配；in-place 未交付，标题不再承诺。

## 2026-10-12 第三轮修订（B18-C13、C14；一次源核对）

- C13：一次源 PDF（/tmp 外部抓取，未入库）文本核对：§4.5 Rabenseifner 原式 `2 lg p α + 2((p−1)/p)nβ + ((p−1)/p)nγ` 无 ceil；二项树 reduce 旧式 `Ttree = ⌈lg p⌉(α+nβ+nγ)` 为 ceil 的出处（不迁移）；§5.1 递归要求二次幂，非二次幂缩 p0 + 额外开销。正文行改原式 + 二次幂条件 + 非二次幂程序/unknown。
- C14：mappings.py 一次源核对（同 tag raw）：六函数阶段语义 L201–297（copy fwd 无通信/bwd 约简等）；sp2hp/hp2sp 文档 shape L566–621；FSDP Notes payload 公式/unit 定义/buffer 三节（padding 未转录 unknown）；token_dispatcher.py（同 tag，SHA 7af27461…，不新增登记 ID）：MoEAlltoAllTokenDispatcher 工作流 L372–383、ep_group 归属、A2A 调用 L690–720；EP 字节随路由可变（公式结构冻结，具体值调用方定）。

## 2026-10-13 第四轮修订（B18-C14）

- EP 有限分支一次源核对（同 tag raw）：moe_utils.py L423–467（non-fused argsort permute：tokens `index_select` 得 [m,H]，probs 一维 [m]；drop_and_pad/capacity 变体另计）；dispatcher combine 前 RS(TP)（L817–826，tp_size>1）与 combine A2A split 交换（L855–863，注释 [SEQL,H]→[SEQL,H/TP]）。正文 EP 行改 tokens `m_ij·H·b_t` / probs `m_ij·b_p` 各自表达式、dispatch×2 与 combine 反向、TP=1 基线 + TP>1 AG/RS 条件、metadata 边界；fused/padded/具体路由值继续 unknown。

## 2026-10-14 第五轮修订（B18-C14）

- AG/排序条件一次源核对（同 tag raw）：dispatch_postprocess L734–744（`tp_size>1` 时对 tokens 和 probs 各做一次 AG，含 output_split_sizes 分支）；排序 L746 起（`num_local_experts>1` 才进入）。正文 EP 行改 AG 条件为 `tp_size>1`（tokens+probs），排序条件为 `num_local_experts>1`；combine 前 RS（`tp_size>1`）不变。

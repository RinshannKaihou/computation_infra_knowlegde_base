# 第十八批审阅修订映射（B18-C01–C15）

修订日期 2026-10-10。初审输入 SHA 见审阅报告；本记录逐项映射关闭动作与证据，待定向复核（CLOSED/OPEN 由复核者判定）。

## C01（P2，适用表）→ 修正转录 + 分歧注记

- `interconnect-paths.md` 样板 A：适用表逐行转录（canonical 与 `:6066` 2026-10-10 抓取字节一致 12307 B）；Note（RC 形态例外）照录。
- **分歧**：初审记训练行 `/`；本轮两次抓取为训练/推理合并行 `√`。以可复现抓取为准，不补造矩阵；合并行不能区分训练单列，所选训练形态可调用性待目标形态确认。
- 计划 A 改为接口条件分支（不可调用/语义不明→该分支记证据不足、不能执行）。
- 登记 `src.ascend.cann-aclrt-devices-topo-2026-10-09` notes 同步。

## C02（P2，CX 故障域）→ 联合身份重写

- Table 5 全量 8×OSFP + Slot 行；Table 6 联合身份（模块/CPU+CX+BDF+mlx5）+ CX 局部编号正反例（模块 1 CX0=GPU7 vs 模块 0 CX0=GPU3）。
- 故障域：模块/转接板/DensiLink 对/OSFP P1+P2 对/PSU/超配；删除"单 CX 卡双端口"断言。

## C03（P2，图/表/计划）→ 已补

- 图 N-1、图 A-1（原创 ASCII，有证边/逻辑/unknown 区分）；核对行表（两组 OSFP + 发现命令）；计划 N/A（固定输入/比较/观察点/通过-失败-无法判断）。

## C04（P2，版本绑定）→ 对齐 + 收窄

- OFED：24.10-5.1.6.1 LTS；RoCE canonical 已确认，其余四页注明未逐页确认。
- man7 降为可读入口；语义准绳为 v65.0 固定 man 源（逐条行号）；九页完整差分未做如实保留。
- 内核改引 v6.16 tag 固定文件（复核 200）；`source_checked` 收窄至标注行号。
- perftest 行号按 a31f9ea 固定并分拆登记；rdma-core tag 待定保留；Megatron 改冻结 tag（新登记）。

## C05（P2，IMM）→ 四分 + 分阶段

- DOCA §4.1.4/§4.3.2 转录；SEND/WRITE/WRITE_WITH_IMM/READ 四分表；注册/提交/完成/异步四阶段映射；RNR vs ACCESS_ERR 下一检查分开。

## C06（P2，CQE/byte_len）→ 前提 + 边界

- signaled/sq_sig_all 前提（固定 man L140–150）；mlx5 L164–182 字节字段边界；字节验收用请求长度+接收/端口证据。

## C07（P2，PFC 条件）→ 条件表

- Cumulus 双模式/ASIC/trunk 转录；传输/重试/PFC/ECN/目标五分；诊断规则不作部署处方。

## C08（P2，图/比较/链接）→ 已补

- 图 M-1/M-2；工作负载/设计比较表；隔离样板（UFM 分区计数器）+ 反例（Secure Host 范围）；正文内链诊断文。

## C09（P2，IB/RoCE 分开）→ 分列

- 路径工具 IB 专用；RoCE 快照三要素；计数器三层；SM 主备；G4 双快照。

## C10（P2，计数器/门槛）→ 逐项 + 三列

- UFM 全表转录；零增量仅错误列；tick 不换算；恢复=新窗零新增；停止≠根因。

## C11（P2，NUMA/计时）→ 精确互斥 + 优先级

- 互斥仅两对；显式>外部>自动；计时取时间戳层面。

## C12（P2，覆盖率）→ 分轮 + 覆盖声明

- 扫描/校验分轮；skips/stale 覆盖；errors=0 限已检查部分；校验吞吐差不归因网络。

## C13（P2，公式）→ 精确式 + 前提

- 精确式与近似式分开；p/n/lg-ceil/分支/假设逐行；推导属性注明。

## C14（P2，图/冻结/EP）→ 已补 + OPEN

- 六类 ASCII 图 + all-to-all 转置；core_v0.19.2 精确路径（raw 200）；逐调用核算；DeepSpeed 移除；EP 字节/路由继续 OPEN；in-place 已核对部分 + NCCL unknown。

## C15（P3，链接/标题）→ 已修

- NCCL URL 去 `usage/`；H2 与段落分开。审计注记：`make check` 只验本地链接，远端可用性由本轮逐条复核承担（404 已修一处）。

## 文件清单

正文 4 篇（3 重写 + 1 修订）；登记 375（+1 冻结 Megatron；8 项审阅者登记沿用）；研究记录 4 份追加修订节；本映射 1 份。

## 2026-10-11 第二轮修订（定向复核 7 CLOSED / 9 OPEN → 本轮处理全部 9 项）

- C01 CLOSED（复核确认审阅者误读，撤销反证）：正文注记改纠错确认口径；RC Note 与形态确认保留。
- C02/C07/C08/C09/C11/C15 CLOSED：本轮未改动其关闭依据（仅 C08/C09 关联行随 C05/C10 多因口径同步文字）。
- C03：图例统一 + A-1/A-2 独立片段 + 三入口发现表 + 计划 N 对应。
- C04：D-IB/D-RoCE 文档级样板选型；NIC/交换机逐项语义仍 unknown（诚实保留，非降级关闭）。
- C05：INLINE 发送侧限定 + RNR 范围限定 + 图表同步。
- C06：SQ/RQ 分离 + READ 限定 + bullets 补回。
- C10：Packets 单位 + Constraint 多因 + 样板指标/delta/回绕 + UFM 口径限定。
- C12：G1 设计值 + host/device 依赖 + 隔离规则 + 覆盖判据。
- C13：ceil/等分/非二次幂逐行条件。
- C14：PP 分支修正 + 逐调用核算 + 全图 + 逐对匹配 + in-place 摘帽（EP 仍 OPEN）。
- C16（新增）：Slot3 推定删除 + 摘要口径修正。

## 2026-10-12 第三轮修订（第二次复核 11 CLOSED / 5 OPEN → 本轮处理 C04/C10/C12/C13/C14）

- C04：正文 verification 待补项改"完整九页差分"（tag 本体已选 v65.0）；研究记录加状态说明，历史"待定"句标为当时状态。
- C10：ECN/流控 canonical 页只读转录（只读取得，不新增登记）；参数/计数/率三类分开，ECN/PFC 归 RoCE 分支；重试计数 unknown（validator retries 不互换）；回绕 unknown 分支；缺字段门禁无法判断。
- C12：迭代/统计/聚合/覆盖门禁全部可计算化（BW 5000、bw_avg median、(skips+stale)/iters 带内）；H1 硬件样板（文档级，型号固件待定）。
- C13：一次源 PDF 核对（未入库）；Rabenseifner 原式无 ceil + 二次幂/非二次幂条件。
- C14：TP 六函数阶段纠正 + sp2hp/hp2sp 真实现 + FSDP 公式/buffer + EP 冻结 dispatcher（同 tag，不新增 ID）。

## 2026-10-13 第四轮修订（第三次复核 13 CLOSED / 3 OPEN → 本轮处理 C10/C12/C14）

- C10：ECN 双入口纠正 + PFC 型号声明限定；缺字段 unknown 保持（不关闭必交项，由复核判定）。
- C12：同粒度覆盖门禁（后端/字段/换算/失败分支/G0 同门禁）；device 轮字段未映射前记 unknown。
- C14：EP 各自表达式 + combine/TP 条件 + metadata 边界；未核定部分继续 unknown。

## 2026-10-14 第五轮修订（第四次复核 13 CLOSED / 3 OPEN → 本轮处理 C10/C12/C14）

- C12（P3）：研究记录倒置修正（==0）；正文门禁不动（已接受）。
- C14：AG（tp_size>1，tokens+probs）与排序（num_local_experts>1）分开绑定一次源行号；其余已接受部分不动。
- C10：补取证尝试记录（ECN/流控/IB 索引/UFM 已查范围与缺失结论）；缺字段 unknown 保持，是否关闭由复核判定。

## 2026-10-14 第六轮修订（第五次复核 15 CLOSED / 1 OPEN → 本轮处理 C10）

- C10：纠正开关/计数归类——正文测量表新增 `dropless_rq`（配置开关）与 `out_of_buffer`（NIC 硬件丢包计数，局部语义已取得、采集信息 unknown）两行；研究记录 L45 同步拆分（前者非计数）。补 OFED 树 pagetree（无独立计数器/统计页）与 QoS 页（仅配置）核查结论。缺字段 unknown 保持，是否关闭由复核判定。

## 2026-10-14 第七轮修订（第六次复核 15 CLOSED / 1 OPEN → 本轮交付 C10 字段）

- C10：交付三类版本化字段（mlx5 双驱动 v6.16 字段表 + netdev 统计 ABI，共 3 新登记）；正文测量表、停止门禁、适用范围、验证注记同步；FW 细则/位宽/型号固件/ASIC 内部分支 unknown 保留。

## 2026-10-14 第八轮修订（第七次复核 15 CLOSED / 1 OPEN → 本轮修正 C10 四项）

- out_of_buffer 双入口拆分（IB sysfs vport_ 前缀 vs mlx5e ethtool qcounter）；per-QP 与 ib_counters API 区分（per-QP 待核定）；本机标记占比口径与停止表同步；Cumulus 双页引用链 + 更新边界 + ABI 语义约束；pause_duration 微秒纠正。新增 3 登记（378→381）。

## 2026-10-14 第八次复核后收尾（16 CLOSED / 0 OPEN，Batch 18 有限文档范围通过）

- 非阻断提示已处理：per-QP 行表名括注拆分为三表各自归属（basic_op_cnts / rdmarx_cnp_op_cnts / rdmatx_cnp_op_cnts，L131–141）；不改变 per-QP 待核定状态。
- 保留条件：NIC 型号固件/FW 细则/累计位宽/ASIC 内部 unknown；per-QP 用户态入口待核定；rdma-core 九页差分未完成；正文 draft、基线 not_verified；无实机验证。

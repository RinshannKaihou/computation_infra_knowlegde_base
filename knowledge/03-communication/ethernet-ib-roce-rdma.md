---
id: communication.ethernet-ib-roce-rdma
title: Ethernet、IB、RoCE 与 RDMA 机制
type: concept
domain: communication
status: draft
platforms: [generic]
source_refs:
  - src.linux.rdma-core-v65.0
  - src.linux.rdma-verbs-man-pages-2026-08-04
  - src.linux.rdma-core-verbs-man-v65.0-fixed
  - src.linux.rdma-core-mlx5-cq-v65.0
  - src.kernel.infiniband-user-verbs-v6.16-fixed
  - src.kernel.infiniband-sysfs-abi-v6.16-fixed
  - src.nvidia.mlnx-ofed-586042lts-roce
  - src.nvidia.mlnx-ofed-586042lts-ib
  - src.nvidia.mlnx-ofed-586042lts-ecn
  - src.nvidia.mlnx-ofed-586042lts-flow-control
  - src.nvidia.mlnx-ofed-586042lts-secure-host
  - src.nvidia.rdma-aware-networks-guide-3.5.0
  - src.nvidia.gpudirect-rdma-13.4
  - src.ibta.specification-2.1
updated_at: "2026-10-10"
summary: "以 rdma-core v65.0 固定 man 源文件为准绳解释链路与网络协议、传输与 verbs 接口、注册内存、QP/CQ、完成和错误语义：Ethernet 与 IB 为不同协议栈，RoCE 是 IB 传输 over 以太网（v1 L2 封装 ethertype 0x8915，v2 L3 可路由 UDP dport 4791）；SEND/WRITE/WRITE_WITH_IMM/READ 四分、MR/PD/QP/CQ 分工、应用完成与远端持久化的区别、signaled 通知前提与 mlx5 字节字段边界；无损/有损按模式条件给出；加速器直连逐产品另核对，命令留待工具版本固定。"
related_ids:
  - communication.interconnect-paths
  - communication.rdma-baseline-and-congestion-triage
  - communication.collectives-and-rank-progress
  - hardware.resource-topology
applicability:
  environment_refs: []
  notes: "尚无环境档案：verbs 语义以 rdma-core v65.0 固定 commit 58e4080 man 源文件为准（man7 2026-08-04 快照仅作可读入口，未做九页完整逐字差分）；内核侧以 v6.16 tag 固定文件（user_verbs.rst、sysfs-class-infiniband，不用 docs.kernel.org 浮动入口作版本证据）；OFED 侧为 24.10-5.1.6.1 LTS（2024 LTS U5；586042lts 入口，RoCE 页 canonical 已确认）；GDR 文档 v13.4；DOCA 3.5.0 归档仅作 IMM/RNR/SM 局部机制反证。目标 NIC/固件/驱动组合需另行固定。"
verification:
  status: source_checked
  evidence_refs:
    - src.linux.rdma-core-verbs-man-v65.0-fixed
    - src.linux.rdma-core-mlx5-cq-v65.0
    - src.nvidia.mlnx-ofed-586042lts-roce
  notes: "对照第十八批取证记录所列固定版本来源核对；2026-10-11 第二轮：SQ/RQ 通知归属分离（create_qp L28–33、post_send L140–150/L164–168、post_recv L51–54），RNR 限 RC/connected，INLINE 例外仅发送侧，远端接收 CQE 不受发起侧 signaled 约束；man7 快照与固定 commit 的完整差分、IBTA 规范全文未验收，source_checked 仅覆盖逐条标注的固定小节/行号；未在任何 RDMA 硬件上执行验证。"
---

# Ethernet、IB、RoCE 与 RDMA 机制

## 定义与要解决的问题

RDMA 排障先分清三层：**链路与网络协议**（走什么线、谁寻址）、**传输与 verbs 接口**（谁发起、谁完成）、**内存与完成语义**（谁能碰哪块内存、完成意味着什么）。Ethernet 与 InfiniBand 是不同的协议栈；RoCE 是"IB 传输 over 以太网"（标准归属 IB 架构规范，2010 首版；规范本身会员门控未获取，只引用存在性与版本名）。

## 机制与关键关系

### 图 M-1：协议承载三柱（原创示意）

```text
IB 线缆                  RoCEv1（L2）                 RoCEv2（L3 可路由）
[IB 传输层]              [IB 传输层]                   [IB 传输层]
[LRH + GRH]              [ETH ethertype 0x8915]       [ETH / IP / UDP dport 4791]
[需 SM][LID]             [无 SM][LID=0 正常]           [无 SM][UDP 源端口作 ECMP 流标识]
[APM 可选]               [APM 不支持]                  [IP 头替代 GRH 穿 L3]
```

IB 传输层（含 QP/verbs 语义）横跨三种承载。RoCE 建连要点：无需 SM；RC QP 无 alternate path 故 **APM 不支持**；查 path 不可能，建连前自填 path record，**建议用 RDMA-CM**；QP 的 GID index 决定 RoCE 模式；SL→PCP 映射。（[MLNX_OFED RoCE 章](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/rdma-over-converged-ethernet-roce)，24.10-5.1.6.1 LTS）

GID 表由网卡以太网 IP 配置生成，每值占 v1+v2 双条目；IPv4 GID 为 IPv4-mapped IPv6；sysfs `gids/<i>`、`gid_attrs/types/<i>`（[v6.16 sysfs ABI 固定文件](https://github.com/torvalds/linux/blob/v6.16/Documentation/ABI/stable/sysfs-class-infiniband)佐证路径存在性，不推导计数器语义）。

### 图 M-2：verbs 数据路径与参与者（原创示意）

```text
发起方应用 --ibv_post_send--> [SQ] --线缆--> [远端 RQ/CQ]
   |  (lkey 本地 MR)                opcode 决定远端行为：
   |                          SEND -> 需远端预投 RR -> 远端 recv_cq 产生 CQE（数据进接收 buffer）
   +--ibv_reg_mr--> [MR/lkey/rkey] WRITE -> 直写 remote_addr+rkey -> 远端无通知、无远端 CQE
                                   WRITE_WITH_IMM -> 直写 + 消耗远端 RR -> 远端 CQE（数据进 remote_addr，imm 进通知）
                                   READ <- 从 remote_addr+rkey 取回 -> 仅发起方 send_cq CQE
通知归属：发起侧 SQ 逐条通知受 signaled/sq_sig_all 约束；远端 RQ 成功接收 CQE 按 recv_cq
关联产生，不受发起侧 signaled 条件约束。发起方完成 ≠ 远端持久 ≠ GPU 可见。
```

### verbs：SEND、WRITE、WRITE_WITH_IMM、READ 四分（C05 修正）

opcode×QP-type 容许表（[固定 post_send man 源](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/libibverbs/man/ibv_post_send.3)，表头列为 UD/UC/RC/XRC_SEND/RAW_PACKET）：READ/原子仅 RC/XRC 列有值；WRITE 系列无 UD 列；SEND_WITH_IMM 在 UD/UC/RC/XRC 均有值。

| 原语 | 远端资源 | 数据落点 | 远端通知与完成 |
|---|---|---|---|
| SEND[WITH_IMM] | RC/connected 语义下必须消耗远端预投 RR（`ibv_post_recv`）；RNR 判据限 RC/connected，UD/UC 不套用（按 DOCA 传输表为不可靠/单包语义，其无 RR 行为另查，本样板不下结论） | 接收 buffer（UD QP 收包 GRH 占 scatter 首 40B） | 远端 recv_cq 产生 CQE（不受发起侧 signaled 约束）；接收 buffer 必须取回 CQE 后方可复用（`post_recv` NOTES 无 INLINE 例外） |
| RDMA WRITE | 无（远端 CPU 不参与） | `remote_addr`（`+rkey` 授权） | 远端无通知、无远端 CQE |
| RDMA WRITE_WITH_IMM | **RC/connected 语义下必须消耗远端 RR**；无 RR 时回 RNR 错误（范围同 SEND 行） | 数据进 `remote_addr`（不是接收 buffer），imm 值进接收通知 | 远端 CQE（含 `IBV_WC_WITH_IMM`）；"notify 远端的是 immediate 值，不是数据搬运"（[DOCA 3.5.0 §4.1.4](https://networking-docs.nvidia.com/doca/archive/3-5-0/rdma-aware-networks-programming-guide)）；RC 下无 RR 判 RNR，不判链路/内存故障（[同 §4.3.2](https://networking-docs.nvidia.com/doca/archive/3-5-0/rdma-aware-networks-programming-guide)：RR 缺失 + send/WRITE_WITH_IMM → RNR） |
| RDMA READ | 无（远端 CPU 不参与） | 取回发起方 | 仅发起方 send_cq 产生 CQE（受本 QP signaled/sq_sig_all 约束） |

- **MR**：`ibv_reg_mr(pd,addr,len,access)`；`REMOTE_WRITE`/`REMOTE_ATOMIC` 须连带 `LOCAL_WRITE`；local read 恒开；`lkey` 供本地、`rkey` 供远端；变体与 `FLUSH_GLOBAL/PERSISTENT` 均标 if supported。
- **PD**：`ibv_alloc_pd(ctx)`；dealloc 在仍有资源关联时可失败——PD 是 MR/QP 关联分组，**不可写成"PD=网络租户隔离/加密"**（DOCA 局部术语佐证分组定义：components can interact with only each other）。
- **QP 与 CQ 归属**：`create_qp` 的 `send_cq` 关联 SQ、`recv_cq` 关联 RQ（固定 create_qp man 源 L28–33）；`sq_sig_all` 定义为"each WR submitted to the SQ generates a completion entry"——**仅 SQ 范围**，不控制远端 RQ 的成功接收 CQE。
- **通知前提**：成功的 unsignaled SQ WR 本来就不要求逐条 CQE。`IBV_SEND_SIGNALED` 仅在 QP 创建未置 `sq_sig_all` 时有意义（固定 post_send man 源 L140–150）；判"发送侧 CQE 缺失"前必须先核对通知策略（signaled/sq_sig_all）、CQ 消费进度与采样时间窗，再进入故障分支。远端成功接收是否产生 CQE 与发起侧 signaled 无关，不得混用。
- **buffer 生命周期（发送/接收分开）**：发送 buffer 在 WR 完全执行且取回 CQE 后可复用，**例外仅发送侧**：置 `IBV_SEND_INLINE` 时 `post_send` 返回后即可复用（固定 post_send man 源 L164–168）。接收 buffer 无此例外：`post_recv` NOTES 只允许 CQE 取回后复用（固定 post_recv man 源 L51–54）。
- **QP 状态机**：`create_qp`（cap、类型 RC/UC/UD/RAW_PACKET/DRIVER，实际 cap≥请求）与 `modify_qp` 状态机 **Reset→Init→RTR→RTS**（RC 需 AV/path_mtu/dest_qpn/PSN/重试参数；RoCE 时 GID index 进 AV）。
- **CQ/完成**：`poll_cq→wc{wr_id,status,opcode,vendor_err,byte_len,qp_num,…}`；**非 SUCCESS 时仅 wr_id/status/qp_num/vendor_err 有效**（[固定 poll_cq man 源](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/libibverbs/man/ibv_poll_cq.3) L67–71）；CQ overrun → `IBV_EVENT_CQ_ERR` 且 CQ 不可用；错误定位另看异步事件（QP_FATAL/REQ_ERR/ACCESS_ERR、PORT 事件）与 ack 义务。
- **字节字段边界（C06）**：固定 mlx5 `cq.c` `handle_good_req`（L164–182）WRITE/WRITE_IMM 与 SEND 成功分支只设 opcode、不填 `byte_len`，仅 READ 分支填入（原子填 8）。因此字节数验收一律用**请求长度**（sge/MR 登记值）及有明确语义的接收侧/端口证据，不得把该 provider 的 READ 赋值扩为通用 WRITE 保证。
- 用户态接入：慢路径经 `/dev/infiniband/uverbsN` write + ABI 头，快路径 mmap 寄存器直写；内核 idr 句柄隔离；`get_user_pages` pin + `pinned_vm`/`RLIMIT_MEMLOCK`（[v6.16 user_verbs 固定文件](https://github.com/torvalds/linux/blob/v6.16/Documentation/infiniband/user_verbs.rst)，v6.16；与 T02-01 主机资源模型衔接）。

### 分阶段错误映射（C05：注册、提交、完成、异步四阶段分开）

| 阶段 | 证据 | 候选与下一检查 |
|---|---|---|
| 本地注册 | `ibv_reg_mr` 返回值/errno | 权限/长度/内存不足；只查本地，不推导远端 |
| 提交 | `post_send/post_recv` 返回 errno；`modify_qp` errno | 参数/QP 状态/AV-GID；`QP_REQ_ERR` 查建连 |
| 完成（WC） | `poll_cq` status/opcode（失败时四字段；发起侧 SQ 条目受 signaled 约束） | RC 下 RNR（对端 RR 不足，查接收投递）vs 可重试传输错误 vs 远端内存/权限；UD/UC 不用 RNR 判据 |
| 异步事件 | `QP_ACCESS_ERR` / PORT 事件 | 远端不可读写（rkey/权限/地址）；`get_async_event` 另查 |

本地注册失败不得直接推导远端 `ACCESS_ERR`；RNR 与权限不足是不同候选、下一检查不同。

### 完成 ≠ 持久 ≠ 对端可见

RELAXED_ORDERING 页明示 completion 仍保证数据可见但 write-after-write 次序不再保证；持久化需 FLUSH 放置类型（if supported）。GPUDirect RDMA 侧：并发运行的 GPU kernel 观察到的 RDMA 写可为 stale/乱序（数据竞争），须经 CPU 侧 CUDA 提交/同步定序（[GDR v13.4](https://docs.nvidia.com/cuda/gpudirect-rdma/)）。禁语："RDMA 完成即远端落盘/即 GPU 可见"。

### RDMA ≠ 零成本/零拷贝/天然可靠（C07 条件化）

pin 代价（内核 pin + `RLIMIT_MEMLOCK`；GDR pin 毫秒级 + BAR 有限 → lazy unpin/registration cache）；注册/建连/重传/拥塞控制皆成本；可靠性按 QP 类型与网络条件分档（DOCA 传输表：RC 可靠有序、UC 不可靠需高层协议、UD 单包）。

无损/拥塞按模式条件给出，不写通用处方：

| 条件 | 要求 | 出处 |
|---|---|---|
| RoCE lossless 模式（Cumulus 4.3，Spectrum ASIC） | PFC + ECN（`net add roce lossless`） | [Cumulus 4.3 RoCE](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-43/Network-Solutions/RDMA-over-Converged-Ethernet-RoCE/) |
| RoCE lossy 模式（同页） | ECN（无 PFC） | 同上；性能另议，不保证等同无损 |
| RoCEv1 | 需 trunk 口（802.1p 分类依赖） | 同上 |
| ECN（OFED 24.10-5.1.6.1） | 限 RoCEv2、路径全节点支持 | [ECN 页](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/explicit-congestion-notification-ecn) |
| 无损以太网一般 | PFC 按优先级 pause（[流控页](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/flow-control)） | 交换机侧配置另查，不当证据 |

RC 等传输保证、丢包重试、PFC 流控、ECN 拥塞响应、工作负载目标五者分开陈述；其他 NIC/交换机/模式组合保留未知。诊断侧停止/恢复规则见[RDMA 基线与拥塞诊断](rdma-baseline-and-congestion-triage.md)，不写成通用部署处方。

### 工作负载、依赖、设计与安全比较（C08）

| 维度 | 选项与取舍 | 条件 |
|---|---|---|
| 小消息/时延敏感 | UD send/recv 或 RC 短 WRITE； tended RR 预投充足 | QP 类型 + 通知策略 + 接收资源 |
| 大消息/带宽 | RC READ/WRITE 单边，零远端 CPU 参与（IMM 除外） | MR 注册/pin 代价 + MTU/GID 前提 |
| 需要远端通知 | SEND 或 WRITE_WITH_IMM（RC 下仍需 RR） | RNR 风险与接收投递预算（RC 范围） |
| 网络设计 | IB 子网（SM/分区）vs RoCE lossless vs RoCE lossy | 按选定 NIC/交换机/模式，不互推 |
| 隔离机制样板（版本化） | UFM 4.18.15 记录 FilterRaw/PartitionEnforcement（PKey/分区）/IP version 出向/入向检查（失败计入 Xmit/Rcv Constraint Error；多因，需结合分区配置快照定位，不单独证明 PKey 错） | 仅该版本该指标语义；租户/加密通用机制仍 unknown |
| 隔离反例（版本化） | Secure Host 页仅 ConnectX-3/3 Pro（SMP 防火墙/M_Key/GUID0），不可泛化 | [Secure Host](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/secure-host) |

RC QP 的 timeout/retry/rnr 参数为逐 QP 可配；PFC 按优先级、ECN 按设备/端口/优先级；观测点 `ibv_devinfo`/`link_layer`、`ibdev2netdev`、GID、`traffic_class/TTL` 只列存在性——**命令留到工具版本固定后写**。

加速器直连逐产品另核对：PeerDirect/GDR 是"IB CORE↔peer-memory 客户端"API（`nvidia-peermem`，CX-3+，IB/RoCE 皆可），不是"装了 verbs 就有 GDR"；同 root complex、PCIe 拓扑、BAR、同步注册均为前提；**NPU 直连零证据**。

## 适用边界

- verbs 语义以 v65.0 固定 man 源文件为准（man7 快照仅可读入口，未做九页完整逐字差分）；OFED 行为以 24.10-5.1.6.1 LTS 为准；IBTA 规范细节不转述。
- fabric 级通用隔离（分区/租户/加密）官方证据未取得；上表两行分别为版本化样板与反例，不可泛化。
- 计数器单位/方向语义留 T03-03；`ibv_*` 等命令一律不写。

## 常见误解

- **"RDMA 就是零拷贝不要钱"**：pin、注册、建连、重传都是成本，GDR pin 还是毫秒级。
- **"收到完成就是对端落盘了"**：完成≠持久≠GPU 可见，三者各需证据。
- **"PD 就是租户隔离"**：PD 只是关联分组；隔离另需 fabric 证据（仅 UFM 分区计数器样板）。
- **"RoCE 下 LID=0 是故障"**：正常现象，勿报故障；SM 缺失在 IB 侧才是故障（active/standby 区分见诊断文）。
- **"WRITE_WITH_IMM 不需要远端准备"**：RC 下需要 RR；无 RR 报 RNR，不是链路故障（UD/UC 另议）。
- **"无 CQE 就是丢包"**：先查发起侧 signaled 策略与 CQ 消费；unsignaled SQ 成功本无逐条通知；远端接收 CQE 与该条件无关。
- **"RoCE 必须开 PFC"**：只在 lossless 模式；lossy 模式只用 ECN（Cumulus 4.3）。

## 原语到观测和故障的映射

| 原语 | 观测（先核通知前提） | 故障信号 |
|---|---|---|
| `reg_mr` | 返回值/errno（本地阶段） | 本地失败只查本地；不对推远端 |
| `create/modify_qp` | `modify_qp` errno；`QP_REQ_ERR` | 建连卡住；RoCE GID/AV 填错 |
| `post_send(SEND)` | 发起侧 send_cq CQE（signaled 约束）+ 远端 recv_cq CQE（无此约束） | RC 下无 RR→RNR；UD GRH 偏移误读 |
| `post_send(WRITE)` | 发起侧 send_cq CQE（signaled 约束）；字节数用请求长度 | 全零/陈旧数据（RO 后写乱序另查） |
| `post_send(WRITE_IMM)` | 发起侧 send_cq CQE（signaled 约束）+ 远端 CQE（含 imm） | RC 下 RNR（接收资源不足）；权限问题查异步事件 |
| `post_send(READ)` | 发起侧 CQE（`byte_len` 仅部分 provider 填） | 超时/重试耗尽 |
| CQ 消费 | `IBV_EVENT_CQ_ERR` | 雪崩式完成丢失；恢复=重建 |
| 链路/端口 | `state/phys_state/link_layer/lid/rate` | RoCE LID=0 正常；IB 侧 SM 缺失为故障 |
| 拥塞/无损 | PFC prio 计数器、`port_xmit_wait`、ECN 参数 | 按模式条件判读（阈值留 T03-03） |

独立验证引用口径：固定 rdma-core v65.0 + 内核版本后，用最小 verbs 程序复现；可判读的独立对照流程见[RDMA 网络基线、路由与拥塞诊断](rdma-baseline-and-congestion-triage.md)（G0–G5 对照组与完成判据）。

## 来源与待确认问题

- [rdma-core v65.0](https://github.com/linux-rdma/rdma-core)（仓库锚点）；[固定 man 源文件组](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/libibverbs/man/ibv_post_send.3)（语义准绳；man7 快照待完整差分）；[mlx5 CQ 固定实现](https://github.com/linux-rdma/rdma-core/blob/58e40801bfed5a8befc0881594820fa0a0baa4a1/providers/mlx5/cq.c)（单 provider 字段边界）。
- [v6.16 user_verbs 固定文件](https://github.com/torvalds/linux/blob/v6.16/Documentation/infiniband/user_verbs.rst)与[sysfs ABI 固定文件](https://github.com/torvalds/linux/blob/v6.16/Documentation/ABI/stable/sysfs-class-infiniband)（接入模型与路径存在性）。
- MLNX_OFED 24.10-5.1.6.1 LTS：[RoCE](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/rdma-over-converged-ethernet-roce)（canonical 已确认）、[IB 索引](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/infiniband-network)、[ECN](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/explicit-congestion-notification-ecn)、[流控](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/flow-control)、[Secure Host 反例](https://networking-docs.nvidia.com/mlnxofedswum/586042lts/secure-host)（后四页 canonical 未逐页确认，按同入口默认版本引用）。
- [DOCA 3.5.0 RDMA-aware Guide](https://networking-docs.nvidia.com/doca/archive/3-5-0/rdma-aware-networks-programming-guide)（§4.1.4 IMM 通知、§4.3.2 RR/RNR、Glossary SM；局部机制反证，不作 v65.0 支持矩阵）。
- [GPUDirect RDMA v13.4](https://docs.nvidia.com/cuda/gpudirect-rdma/)（通用边界；具体型号另核对）；[IBTA 规范页](https://infinibandta.org/ibta-specification/)（存在性引用，未获取全文）。
- 逐条主张与证据定位见[第十八批 RDMA 机制来源记录](../../docs/research/batch-18-rdma-mechanism-sources.md)。
- 待确认：man 快照完整差分；IBTA 全文；计数器语义（归 T03-03）；通用隔离机制；加速器直连（尤其 NPU）；命令（待工具版本固定）。

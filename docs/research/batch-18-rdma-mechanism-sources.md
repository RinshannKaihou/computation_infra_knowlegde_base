# 第十八批 T03-02 RDMA 机制来源记录

任务：T03-02（`ethernet-ib-roce-rdma.md`，concept）。取证日期 2026-10-09。固定：rdma-core v65.0、man 页 2026-08-04 快照（待与 v65.0 对版）、内核 v6.16、MLNX_OFED 586042lts、GDR v13.4、IBTA R2.1（存在性）。

## 候选来源（10 项新登记）

rdma-core-v65.0（仓库锚点）、rdma-verbs-man-pages（9 页语义准绳）、infiniband-docs-v6.16（接入模型与稳定 ABI）、mlnx-ofed RoCE/IB/ECN/流控/Secure Host（后者为 CX-3 反例）、gpudirect-rdma-13.4（通用边界）、ibta-specification-2.1（存在性引用）。

## 主张—来源定位表

三柱图与 RoCE 边界（OFED RoCE 章）；GID 表（同上 + 内核 ABI）；send/recv、read/write、MR/PD/QP/CQ、完成与异步事件（man 页组）；接入模型与 pin 代价（内核 user_verbs）；完成≠持久（man RELAXED_ORDERING + GDR）；非零成本与可靠性分档；逐 QP 参数与观测点存在性；GDR 产品边界与 NPU 零证据。

## unknown 清单

内核二选一已定 v6.16（与 T02-01 对齐）；man 页对版待起草；IBTA 全文未取；计数器语义归 T03-03；安全/隔离通用机制未取；加速器直连（NPU 零证据）；命令待工具版本固定。

## 2026-10-10 修订（B18-C04–C08）

- C04：OFED 版本统一为 24.10-5.1.6.1 LTS（RoCE 页 canonical 含 24.10-5.1.6.1lts 已确认；其余四页按同入口默认版本引用并注明未逐页确认）；man7 快照（2026-08-04）降为可读入口，正文语义以 v65.0 固定 commit 58e4080 man 源文件为准（post_send 表头列 UD/UC/RC/XRC_SEND/RAW_PACKET；L140–150 signaled/solicited/inline；poll_cq L67–71 失败四字段）；内核改引 v6.16 tag 固定文件（user_verbs.rst、sysfs-class-infiniband 均复核 200）；DOCA 3.5.0 仅 §4.1.4/§4.3.2/Glossary 局部反证。source_checked 收窄至逐条标注的固定小节/行号。
- C05：§4.1.4（WRITE_WITH_IMM 通知远端的是 immediate 值）+ §4.3.2（无 RR + send/WRITE_WITH_IMM → RNR）转录；正文改四分表 + 四阶段错误映射。
- C06：mlx5 cq.c L164–182（WRITE/SEND 不填 byte_len，READ 填， atomic 填 8）转录；正文加 signaled 前提与字节字段边界。
- C07：Cumulus 4.3 页 lossless（PFC+ECN）/lossy（ECN）双模式、RoCEv1 trunk、Spectrum 限定转录；正文改条件表。
- C08：补图 M-1/M-2（原创 ASCII）；工作负载/设计比较表；隔离样板=UFM 4.18.15 PartitionEnforcement 计数器 + Secure Host 反例范围；正文内链诊断文 G0–G5。

## 2026-10-11 第二轮修订（B18-C05、C06）

- C05：INLINE 例外限定发送侧（post_send L164–168；post_recv L51–54 无例外）；RNR 限 RC/connected（DOCA §4.3.2 + 传输表；UD/UC 无 RR 行为另查，本样板不下结论）；图 M-2 与四分表同步。
- C06：create_qp L28–33（send_cq↔SQ、recv_cq↔RQ、sq_sig_all 仅 SQ）；发起侧 SQ 通知与远端 RQ 接收 CQE 分离；READ 完成限定发起侧 send_cq + signaled 约束；QP 状态机与 CQ bullets 补回。

# 第十八批 T03-01 互联路径来源记录

任务：T03-01（`interconnect-paths.md`，reference）。取证日期 2026-10-09。样板：DGX H100（NVLink 4 代/NVSwitch）+ 800T A2 节点 + A3 SuperPoD。

## 候选来源（9 项新登记 + 复用）

新登记：nvlink-nvswitch-page、hopper-architecture-page、h100-product-page（以上营销页仅作代次/形态锚定）、dgx-superpod-h100-ra-arch、dgx-superpod-h100-ra-fabrics（rail/超配口径）、nvidia-smi-manual（发现视图）、cann-aclrt-devices-topo（Ascend 发现视图）、mindcluster-affinity-principles-730（910 代环 + A2 不支持否定句，集成者实开复核）、hccl-intro-link-types（四链路分层）。复用：dgx-h100-h200-user-guide、atlas-800t-a2-product、nccl-user-guide-2.27.5、mind-cluster-v26.1.1、A3 SuperPoD 用户指南组、lingqu 指南。

## 主张—来源定位表

DGX 机型与互联代次（指南组件表，代次归属照录）；NVLink 代次锚定（产品页）；SHARP/GH200 范围（Hopper 页，厂商宣称）；SXM/NVL 形态差（H100 页）；端口映射（Table 5/6）；fabric 与超节点范围（RA 两页）；nvidia-smi 发现视图（手册）；NCCL 拓扑陷阱（2.27.5 troubleshooting）；800T A2 机型锚点与互联 unknown（产品页）；aclrtGetDevicesTopo 七值枚举（CANN 900）；HCCL 四链路（简介）；910 代环对照 + A2 否定句（730 页）；A3 组成与 L2 端口（T01-05 登记复用）。

## unknown 清单

800T A2 NPU 数量/内存/互联边；HCCS 交换有无；A3 分档指标；DGX 矢量边清单；NVL72/GB200 隔离；作业可用带宽（归 T03-03）；nvidia-smi 页无版本号；H100 NVL 与 DGX 样板隔离。

## 2026-10-10 修订（B18-C01–C04、C15）

- C01：CANN 900 aclrt 页 canonical 与 `:6066` 抓取字节一致（12307 B），适用表逐行转录入正文样板 A；分歧注记：初审记训练行 `/`，本轮两次抓取为合并行 `√`，以可复现抓取为准；训练/推理合并行不能区分训练单列，所选训练形态可调用性待目标形态确认；计划 A 改为接口条件分支。
- C02：DGX Table 5 全量 8×OSFP 行 + Slot 行转录；Table 6 按模块/CPU+CX+BDF+mlx5 联合身份展开（模块 1 CX0=GPU7/dc:00.0/mlx5_11 vs 模块 0 CX0=GPU3/5e:00.0/mlx5_5）；故障域按原文共用关系重写（模块/转接板/DensiLink 对/OSFP P1+P2 对/PSU/超配）。
- C03：补图 N-1、图 A-1（原创 ASCII；有证边/逻辑关联/unknown 区分）；核对行表（两组 OSFP 联合身份 + 发现命令映射）；计划 N/A 含固定输入、比较对象、观察点、通过/失败/无法判断条件。
- C15：来源节 NCCL troubleshooting URL 去掉多余 `usage/`（与 L70 一致）。

## 2026-10-11 第二轮修订（B18-C03、C16；C01 复核结论同步）

- C01：定向复核确认初审系误读产品列斜杠，CLOSED。两页 SHA（e0fbe171…）与原抓取一致；正文注记改为纠错确认口径。
- C03：图 N-1 图例统一（实线=有证边，虚线=Table 6 GPU 列逻辑归属；GPU—CX 无直连证据）；A-1 拆分为 A-1（A2 片段）/A-2（A3 片段），类型候选集不与柜/板连边；发现表按手册三入口重写（topo -m 矩阵+亲和非 BDF 表；--status 本端状态+Active 带宽；-p/-R 取远端；手册无版本号，目标工具版本未固定）；计划 N 观察点与上表对应。
- C16：Slot3 BlueField/DPU 推定删除，改为原表字段摘要（卡型号无精确 BOM 证据不推定）；Table 5 标题改为"计算网 8 端口全量 + Slot/板载摘要"。

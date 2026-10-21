# 第三十批 T08-04 来源记录

任务：T08-04（补齐 SDC 检测、训练传播与平台证据；**revise** `knowledge/08-reliability/silent-errors-and-integrity.md`，主题 08.6）。取证轮次：主会话作者角色首轮（2026-10-21；无前置依赖，批内为首任务）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 硅测试漏斗；四类触发因素（数据随机化/电气 f,V,I/环境温湿度热点/生命周期含 6 个月后失败实验）；Fleetscanner 搭维护窗口、Ripple 共置毫秒级 always-on＋shadow/footprint tax；表 1 与 §6 量化（68M/40 亿 fleet 秒 vs 25 亿/1 亿 fleet 秒每月；93%/23%/7%；15 天 vs 5–6 个月；Ripple 总 77%）；`(1.1)^53=0` 应用侧后果 | src.arxiv.sdc-detection-wild-2203（**本轮新增**） | [arXiv:2203.08989v1](https://arxiv.org/abs/2203.08989)（2026-10-21 arXiv HTML 全文逐节核读：§1、§3、§4、§5.1–5.2、表 1、§6.1–6.3；CC BY-NC-ND 4.0） | Meta 数据中心 CPU、所研究 CPU 缺陷族、3+ 年生产；不含 GPU/NPU，不外推发生率 |
| 真实不健康节点三层级影响（mismatch freq/severity 逐节点表值、WCNTS≤5.1%、loss 重合但参数漂移、微调尖峰 Node 6 精度 0、同步降低 SDC 发生率）；fleet 管理筛选手法（collective 压力＋计算单元压力＋golden truth 小训练）；ABFT float32 仅 Node 14 被标出＋三条失败解释＋bf16 假阳性 | src.acl.sdc-llm-training-2502（**本轮新增**） | [ACL 2025 长文](https://aclanthology.org/2025.acl-long.996/)（=arXiv:2502.12340v1；2026-10-21 全文核读含附录 D.1–D.4、§9 局限） | 其 15 台临时持有节点、单节点 TP、XLA 确定性设置；数字不外推 |
| 检测/恢复分类法正文：§5.2.1 端到端完整性校验、§5.2.2 复制与一致性、§5.2.3 整数剩余校验、§5.3.1 checkpoint 代价与 goodput 引用、§5.3.2 ABFT 前向恢复、§5.4 开销/非确定性/分层法、§6 开放问题 | src.ocp.sdc-in-ai-2025（既有登记，**本轮扩展 notes 至文末**） | [OCP 白皮书](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf)（Batch 30 补读 p.20–30；pdfinfo 重核 30 页） | 分类与机制性讨论；无发生率数据 |
| 昇腾算子级精度比对三步与全部判据（RE/Cosine>0.99/MaxAbsErr<0.001/千分位仅趋势、error/warning 标记、占位与冗余 API 豁免、NPU 与 CPU/GPU 差异累积） | src.ascend.msprobe-26.2.0.b110（**本轮新增**） | [固定 tag 比对文档](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)＋README（2026-10-21 逐条核读；tag 根无 LICENSE 文件） | 离线比对工具的官方判定规则；不是 SDC 检出或发生率证据 |
| npu-smi ECC 计数字段全集（当前/生命周期累计/隔离页/待隔离 0–64 与刷新方式、计数上限 4294967295、支持矩阵） | src.huawei.hdk-26.1x-a2-npu-smi-2026-10-08（既有登记，**本轮扩展 notes**） | [npusmi_0034](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2npu/npusmi_0034.html)（doc_center/source 静态页，2026-10-21 逐字段核读） | signaled（ECC 计数）错误的观测面；HDK 26.1.x A2 树 |
| DCMI ECC 接口（仅 HBM 类型、enable_flag、重启清零、生命周期累计、"查到多比特须定位处理"） | src.huawei.hdk-26.1x-a2-dcmi-ecc（**本轮新增**） | [dcmi_047](https://www.hiascend.com/doc_center/source/zh/HDK/2610/A2/A2DCMI/dcmi_047.html)（doc_center/source 静态页，2026-10-21 逐字段核读） | 同上 |
| FaultDiag 诊断输出结构（根因节点/首错节点/传播链/故障事件/建议方案；-p 性能劣化；16 条终端上限） | src.ascend.faultdiag-v26.1.1（**本轮新增**） | 固定 commit 44385c1 的概述/03_log_parsing/04_fault_diagnosis/04_appendix 四页（文件树重新定位后核读） | 规则匹配=候选假设；示例报告非真实事故 |

## 复用来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| SDC 定义、2x3=5、干净日志盲区、ECC 覆盖不完整 | src.arxiv.sdc-at-scale-v1 | §1/§5/§7（第九批已核） | 数据中心 CPU |
| 数值噪声扣除边界（非结合律、CPU↔GPU 不逐位一致、assert_close 容差） | src.pytorch.numerical-verification-2.6 | 三页文档（第九批已核） | PyTorch 2.6 文档口径 |
| 灰色退化与冗余掩盖（ToR 冗余链路、HBM 重映射 77.8%） | src.usenix.superbench-atc24 | 印刷页 837–838（第九批已核） | Azure GPU 场景 |

## 本文原创部分

Fleetscanner/Ripple 对比表的组织方式、三层级证据表的中文归纳框架、"检测方法分层"表（含把 ACL 2025 ABFT 实测反例并入 OCP 分类行的组合）、NPU 平台证据清单表的"边界"列、NPU SDC 资料可得性边界的检索范围表述（检索面：hiascend HDK 树/CANN 入口/msprobe 仓库/mind-cluster FaultDiag）。

## unknown 清单

1. NPU 侧 SDC 发生率、fleet 级扫描实践、算力校验保障：检索范围内无公开一手材料，正文保持 unknown，未以 CPU/GPU 研究代填。
2. 2203.08989 是否有后续版本：abs 页当前仅 v1。
3. ACL 2025 研究不健康节点维修归队后的复测结果：论文未含。
4. hiascend `document/detail` 形态页（如搜索命中到的 latest ECC 页）需 JS 渲染不可直读；本批以同版本 `doc_center/source` 静态页取证，latest 路径未核对。
5. Table 5 类绝对计数与百分比的 HTML 渲染自洽性（见 T08-06 记录），本文避免引用绝对计数。

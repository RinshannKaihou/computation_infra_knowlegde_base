# 第三十批 T08-08 来源记录

任务：T08-08（诊断评测方法与公开教学题组；**new** `knowledge/08-reliability/diagnostic-evaluation-method.md`＋`knowledge/08-reliability/diagnostic-evaluation-fixtures.md`，主题 08.4/08.8）。取证轮次：主会话作者角色首轮（2026-10-21；同批前置 T08-05/T08-07 已于本轮完成）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 真实事故数据集评测样板：一年期 Microsoft 事故、RCA accuracy 至 0.766、诊断信息采集组件生产使用 4 年以上 | src.arxiv.rcacopilot-2305.15778（**本轮新增**） | [arXiv:2305.15778v4](https://arxiv.org/abs/2305.15778) 摘要页（2026-10-21 核对；全文细节未逐节核读，仅引用摘要级事实） | 云端事故 RCA 评测的公开实践 |
| 评测维度与可复现构造：452 案例/40 故障类型/K8s 全栈；State Snapshot 确定性数字孪生；A@k/TCR/Trajectory Alignment/Relevance/Coverage/MTTI/Steps/IAC/RAR/ZTDR 指标定义；反猜测设计 | src.arxiv.cloud-opsbench-2603.00468（**本轮新增**） | [arXiv:2603.00468v1](https://arxiv.org/abs/2603.00468) §3.2/§4/§5 指标定义（2026-10-21 全文核读；CC BY 4.0） | K8s v1.31 测试床；模型分数未引用；数据/代码仓未读 |

## 复用来源与主张定位（题组 oracle）

| 条目 | 登记 ID | 精确位置 | 边界 |
|---|---|---|---|
| PTF-01 DCP 恢复 KeyError＋修复对照 | src.pytorch.dcp-issue-164257 / src.pytorch.dcp-fix-edd8d35 | Issue 正文＋固定 commit（2026-09-30 已核） | 首个含修复发行版 unknown |
| PTF-02 rank 0 缺席 broadcast 超时 | src.pytorch.issue-118369 | Issue（已核） | stale 关闭≠修复；根因 unknown |
| PTF-03 容器内物理/逻辑 NPU ID | src.vllm-ascend.issue-2557 | Issue＋completed close（已核） | 无同现场复验；不外推其他框架 |
| PTF-04 共同原因双证据 | src.meta.oct-2021-facebook-outage / src.cloudflare.oct-2021-facebook-outage | 两篇（Batch 29 已核） | 事件时刻 vs 发现时刻须分列 |
| PTF-05 应用侧 SDC 症状 | src.arxiv.sdc-detection-wild-2203 | §1（Batch 30 已核） | CPU 场景 |
| PTF-06 ABFT 假阴性 | src.acl.sdc-llm-training-2502 | 附录 D（Batch 30 已核） | 其实验设置 |
| PTF-07/08 Table 5 归因口径与 Unknown 类 | src.arxiv.llama3-infrastructure | §2.2＋Table 5（Batch 30 已核） | 只引用百分比 |
| PTF-09 合成夹具（诊断报告示例） | src.ascend.faultdiag-v26.1.1 | 04_fault_diagnosis.md 示例输出（Batch 30 已核） | 文档示例，显式标合成 |

## 本文原创部分

train/dev/held-out 划分与"入库即 train 侧"规则、按案例家族/版本/时间三维隔离、冻结与外置答案纪律、三角色表、污染披露与换卷策略、答案证据强度四级（A/B/C/U）表、七维 rubric（含各维 0 分反例）、九条题组全部条目结构（输入/oracle/判据含负面清单/rubric 侧重）、检索回归用法与维护规则。

## unknown 清单

1. 独立评测集（V12）未获取：输入/答案外置，授权与脱敏审查未开始；在此之前不宣称任何独立评测结论。
2. 七维权重与评分细则冻结版本：待 V12 评审时一并冻结。
3. 污染的量化检测方法（n-gram 类）未登记原始来源，当前只按披露纪律执行。
4. RCACopilot 正式发表版（若存在于 arXiv v4 之外）未核对；Cloud-OpsBench 代码/数据仓（LLM4Ops/Cloud-OpsBench）未读取。
5. 题组九条覆盖训练/推理/硬件/通信/存储/平台与 U 级样例；昇腾专用公开案例目前仅 PTF-03/09，数量随后续批次补充。

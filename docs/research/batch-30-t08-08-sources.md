# 第三十批 T08-08 来源记录

任务：T08-08（诊断评测方法与公开教学题组；**new** `knowledge/08-reliability/diagnostic-evaluation-method.md`＋`knowledge/08-reliability/diagnostic-evaluation-fixtures.md`，主题 08.4/08.8）。取证轮次：主会话作者角色首轮（2026-10-21；同批前置 T08-05/T08-07 已于本轮完成）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 真实事故数据集评测样板：一年期 Microsoft 事故、RCA accuracy 至 0.766、诊断信息采集组件生产使用 4 年以上 | src.arxiv.rcacopilot-2305.15778（**本轮新增**） | [arXiv:2305.15778v4](https://arxiv.org/abs/2305.15778) 摘要页（2026-10-21 核对；全文细节未逐节核读，仅引用摘要级事实） | 云端事故 RCA 评测的公开实践 |
| 评测维度与可复现构造：452 案例/40 故障类型/K8s 全栈；State Snapshot 确定性数字孪生；A@k/TCR/Trajectory Alignment/Relevance/Coverage/MTTI/Steps/IAC/RAR/ZTDR 指标定义；反猜测设计 | src.arxiv.cloud-opsbench-2603.00468（**本轮新增**） | [arXiv:2603.00468v1 固定入口](https://arxiv.org/abs/2603.00468v1) §3.2/§4.2 指标定义（2026-10-21 全文核读 v1；CC BY 4.0；无版本入口现展示 v2 未读） | K8s v1.31 测试床；模型分数未引用；数据/代码仓未读 |

## 复用来源与主张定位（题组 oracle）

| 条目 | 登记 ID | 精确位置 | 边界 |
|---|---|---|---|
| PTF-01 DCP 恢复 KeyError＋修复对照 | src.pytorch.dcp-issue-164257 / src.pytorch.dcp-fix-edd8d35 | Issue 正文＋固定 commit（2026-09-30 已核） | 首个含修复发行版 unknown |
| PTF-02 rank 0 缺席 broadcast 超时 | src.pytorch.issue-118369 | Issue（已核） | stale 关闭≠修复；根因 unknown |
| PTF-03 容器内物理/逻辑 NPU ID | src.vllm-ascend.issue-2557 | Issue＋completed close（已核） | 无同现场复验；不外推其他框架 |
| PTF-04 共同原因双证据 | src.meta.oct4-2021-postmortem / src.cloudflare.oct-2021-facebook-outage | 两篇（Batch 29 已核） | 事件时刻 vs 发现时刻须分列 |
| PTF-05 应用侧 SDC 症状 | src.arxiv.sdc-detection-wild-2203 | §1（Batch 30 已核） | CPU 场景 |
| PTF-06 ABFT 假阴性 | src.acl.sdc-llm-training-2502（附录定位经 src.arxiv.sdc-llm-training-2502-v1） | arXiv v1 附录 D.1–D.4（Batch 30 已核，版本分列） | 其实验设置 |
| PTF-07/08 Table 5 归因口径与 Unknown 类 | src.arxiv.llama3-infrastructure | §3.3.4＋Table 5（印刷页 13；Batch 30 已核，复核轮更正初稿误写的 §2.2） | 只引用百分比 |
| PTF-09 合成夹具（诊断报告示例） | src.ascend.faultdiag-v26.1.1 | 04_fault_diagnosis.md 示例输出（Batch 30 已核） | 文档示例，显式标合成 |

## 本文原创部分

train/dev/held-out 划分与"入库即 train 侧"规则、按案例家族/版本/时间三维隔离、冻结与外置答案纪律、三角色表、污染披露与换卷策略、答案证据强度四级（A/B/C/U）表、七维 rubric（含各维 0 分反例）、九条题组全部条目结构（输入/oracle/判据含负面清单/rubric 侧重）、检索回归用法与维护规则。

## unknown 清单

1. 独立评测集（V12）未获取：输入/答案外置，授权与脱敏审查未开始；在此之前不宣称任何独立评测结论。
2. 七维权重与评分细则冻结版本：待 V12 评审时一并冻结。
3. 污染的量化检测方法（n-gram 类）未登记原始来源，当前只按披露纪律执行。
4. RCACopilot 正式发表版（若存在于 arXiv v4 之外）未核对；Cloud-OpsBench 代码/数据仓（LLM4Ops/Cloud-OpsBench）未读取。
5. 题组九条覆盖训练/推理/硬件/通信/存储/平台与 U 级样例；昇腾专用公开案例目前仅 PTF-03/09，数量随后续批次补充。

## 复核轮修订记录（初审后）

- C01：ZTDR 与 abstention 脱钩（交互取证过程指标 vs 弃答），两种误判形态写明；引用改 v1 §4.2。
- C02：冻结规则改"测试条件冻结＋候选变量声明"，候选变化＝同协议受控比较、试卷变化才不可比。
- C03：PTF-04 输入改复盘披露范围（容量评估命令/审计阻止失败/全部骨干连接断开），判据分四层（进程运行/公网不可达/内部工具依赖/网络访问失效）；共享控制路径标注为本库归纳；撤销机制 unknown。
- C04：PTF-06 改两组独立观察（bf16 失配 vs float32 ABFT，论文自述不必对应），"持续"收缩，三条解释保持假设语气，拒绝直接配对算漏检率者得高分。
- C05：PTF-07 删"同型集群参照区间"标准答案；合法用法限带条件来源观察/调查假设背景，1.4% 分母写明。
- C06：PTF-08 本地情境显式标注合成（来源事实与构造设定分列）；summary/verification notes 同步为两条合成。
- C07：新增 PTF-10 存储·checkpoint 文件完整性与加载语义（torch.save CRC32 vs torch.load 自研 reader，固定 commit 锚点＋04 域正文）；使用规则补六域题号映射；总数十条。
- C08：Meta URL 对齐 registry 入口；PTF-06 oracle 改 arXiv v1 入口；取证 ID 更正 src.meta.oct4-2021-postmortem；RCACopilot 许可改 CC BY 4.0（v4 页面核对）。
- C09：Cloud-OpsBench 指标定位改 v1 §4.2、入口固定 v1（abs 现展示 v2 未读）；Llama 3 Table 5 定位改 §3.3.4（印刷页 13）。
- C10：PTF-02 证据强度标签改"本事件根因 U＋机制依据"，不再使用未定义的复合等级。

## 第二轮修订记录（复核后）

- C07/N01：PTF-10 现场情境显式标注为构造输入（判据证据仍为公开来源）；summary/verification notes 同步为三处合成（PTF-08 本地情境、PTF-09、PTF-10 现场情境）。
- C08：PTF-06 oracle 补登记入口说明（新登记 src.arxiv.sdc-llm-training-2502-v1 作为附录定位入口）；Llama 3 登记入口固定 v3（registry URL 已改）；PTF-10 的 serialization.py 文件入口登记于 src.pytorch.dcp-2.6 notes；Meta 入口补 curl 双路径 200 证据（registry notes）。
- C09：本记录主张定位表的 Cloud §5→v1 §4.2、Llama §2.2→§3.3.4、PTF-06 附录版本分列已就地更正。

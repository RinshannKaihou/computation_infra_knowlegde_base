# 第三十批 T08-04 来源记录

任务：T08-04（补齐 SDC 检测、训练传播与平台证据；**revise** `knowledge/08-reliability/silent-errors-and-integrity.md`，主题 08.6）。取证轮次：主会话作者角色首轮（2026-10-21；无前置依赖，批内为首任务）。

## 新增来源与主张定位

| 主张 | 登记 ID | 精确位置 | 支持范围 |
|---|---|---|---|
| 硅测试漏斗；四类触发因素（数据随机化/电气 f,V,I/环境温湿度热点/生命周期含 6 个月后失败实验）；Fleetscanner 搭维护窗口、Ripple 共置毫秒级 always-on＋shadow/footprint tax；表 1 与 §6 量化（68M/40 亿 fleet 秒 vs 25 亿/1 亿 fleet 秒每月；分母为实际检出集合：93%/23% 独有、Ripple 共同 70%/15 天、7% 独有/合计 77%；signature 全 fleet 部署≈2 周属发布速度、Fleetscanner 全 fleet 扫描一轮≈5–6 个月——两类时间量分列）；`(1.1)^53=0` 应用侧后果 | src.arxiv.sdc-detection-wild-2203（**本轮新增**） | [arXiv:2203.08989v1](https://arxiv.org/abs/2203.08989)（2026-10-21 arXiv HTML 全文逐节核读：§1、§3、§4、§5.1–5.2、表 1、§6.1–6.3；CC BY-NC-ND 4.0） | Meta 数据中心 CPU、所研究缺陷族的较大子集、3+ 年生产；不含 GPU/NPU，不外推发生率 |
| 真实不健康节点三层级影响（mismatch freq/severity 逐节点表值、WCNTS≤5.1%、loss 重合但参数漂移；微调 DP 仅在多数非灾难性运行与所测六任务上不大于换种子对照，反例 Node 6 CosmosQA 精度 0/DP=100% vs 换 seed 6.70%；同步降低 SDC 发生率——Node 14 超 4000 步观察窗口内仅偶发）；fleet 管理筛选手法（collective 压力＋计算单元压力＋golden truth 小训练）；ABFT float32 仅 Node 14 被标出＋三条失败解释＋bf16 假阳性 | src.acl.sdc-llm-training-2502（**本轮新增**） | 登记主修订 [ACL 2025 长文](https://aclanthology.org/2025.acl-long.996/)（pp. 20372–20394，附录仅 D.1/D.2、实验在正文）＋[arXiv:2502.12340v1](https://arxiv.org/abs/2502.12340)（全文，附录 D.1–D.4；两版附录编号不同，引用按版本定位；2026-10-21 两版分别核读，ACL PDF 已抽查附录结构） | 其 15 台临时持有节点、单节点 TP、XLA 确定性设置；数字不外推 |
| 检测/恢复分类法正文：§5.2.1 端到端完整性校验、§5.2.2 复制与一致性、§5.2.3 整数剩余校验、§5.3.1 checkpoint 代价与 goodput 引用、§5.3.2 ABFT 前向恢复、§5.4 开销/非确定性/分层法、§6 开放问题 | src.ocp.sdc-in-ai-2025（既有登记，**本轮扩展 notes 至文末**） | [OCP 白皮书](https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf)（Batch 30 补读 p.20–30；pdfinfo 重核 30 页） | 分类与机制性讨论；无发生率数据 |
| 昇腾算子级精度比对三步与全部判据（RE/Cosine>0.99/MaxAbsErr<0.001/千分位仅趋势、error/warning 标记、占位与冗余 API 豁免、NPU 与 CPU/GPU 差异累积） | src.ascend.msprobe-26.2.0.b110（**本轮新增**） | [固定 tag 比对文档](https://github.com/Ascend/msprobe/blob/tag_MindStudio_26.2.0.B110_001/docs/zh/user_guide/accuracy_compare/pytorch_accuracy_compare_instruct.md)＋README（2026-10-21 逐条核读；docs 目录许可 CC BY 4.0——docs/LICENSE 与 docs/zh/legal/license_notice.md 复核轮核对，产品/代码许可另计） | 离线比对工具的官方判定规则；不是 SDC 检出或发生率证据 |
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

## 复核轮修订记录（初审后）

- C01："静默"改为三层（硬件原生检测未触发＝定义域；应用间接症状＝候选证据；主动结果校验＝有限检出），NVIDIA 行拆分被动观测与主动诊断。
- C02：量化表两个时间量分列（同等 70% 检出覆盖 15 天 vs 5–6 个月；signature 部署 2 周另列）；比例分母改为"实际检出集合"；"大部分缺陷"改"较大子集"。registry notes 同步。
- C03：检测方法表补元数据/结构校验、差分/不变量与 golden 对照、任务质量检测三行。
- C04：新增 activation→梯度→optimizer 状态→参数→checkpoint 传播链小节（PyTorch 2.6 固定源码 Adam 为方法推导依据）；数据错误候选先核 oracle 身份；链接 06/04 域正文。
- C05：平台清单改为三平台表：NVIDIA 分列 v3.3.9 固定快照与 user-guide 观察页、AMD 引 rccl-tests 固定 tag 的正确性检查、Ascend 保持逐项表。
- C06：补 SuperBench/msprobe/npu-smi（npusmi_0034 支持页与 npusmi_0007 入口关系）/DCMI/FaultDiag 的正文直接锚点；Llama 3 数字补登记来源与精确引用；PyTorch 子页标注"同登记条目"。
- C07：两版修订定位分列（ACL 主修订＋arXiv v1 附录定位），ACL PDF 附录结构已抽查核验；registry revision/notes 同步。
- C08："不大于换种子"加范围与反例（Node 6 vs 6.70%）；registry notes 同步。
- C09："每 4000 步才偶发"改"超 4000 步观察窗口内仅偶发（Node 14）"；初始尖峰利用率解释标注作者推测。
- C10："batched 与逐元素"改"整批执行与逐 batch 样本分别执行同一运算"。
- C11：msprobe docs 许可核实 CC BY 4.0（docs/LICENSE），registry license 由 unknown 升 identified（限 docs 范围）。

## 第二轮修订记录（复核后）

- C02：共同比较基准改为"该缺陷族观察到的失败集合（两方法合并检出并集）"；占比行（93%/77%）与"同一终点（共同 70% 子集）时间"行可比；扫描一轮与 signature 部署移出比较表单列。registry notes 同步。
- C03：成本声明改 unknown 分列（结构属性/指纹/差分/golden/任务质量各行分别声明，不统一排序）；任务质量行补误报边界（正常随机性/分布变化/合法数值差异，OCP §5.4）。
- N01：结构属性检查与内容指纹校验拆为两行——属性检查不查值；指纹在参考可信且无碰撞前提下可发现内容变化（含保持结构的变化），但不证明语义、不容纳合法浮点差异。
- C05：NVIDIA 行补具体字段（dcgm_fields.h L758–778 ECC volatile/aggregate、DCGM_FR_MEMORY_MISMATCH）；AMD 行补 `-c` 校验对象/开关/开销（README L175）与"硬件观测能力未核 unknown"。
- C06：registry 补深页精确入口（npusmi_0034 全 URL、numerical-verification 子页 URL、parallel-training-state 的 adam.py 文件入口、新登记 src.arxiv.sdc-llm-training-2502-v1 作为 ACL 条目的附录定位入口；Llama 3 registry URL 固定 v3）。
- C09：Node 14 显式绑定；利用率-发生率解释标注"论文提示的可能机制，未独立控制"。

## 第三轮修订记录（复核二后）

- N10：ECC 字段名更正为固定源码真实宏名（DCGM_FI_DEV_ECC_CURRENT/_PENDING 300/301、SBE/DBE_VOL_TOTAL 310/311、SBE/DBE_AGG_TOTAL 312/313），行号区间扩为 L751–793；初稿自造的 `SB_ERROR/_DB_ERROR` 名称作废。
- N11：代价行移回 Fleetscanner/Ripple 三列表内（时间行之后），删除两处孤立/重复代价行；任务质量行按四列表头重排（成本入机制列、误报入盲区列）。
- C06：registry 补 dcgm_fields.h 完整文件 URL（含 blob SHA）；正文两处 arXiv 无版本链接固定为 v1。
- C05：显存测试前提（GPU 配置允许性/最小内存分配）已入正文；AMD `-c 0`＝未校验语义已入正文。

## 第四轮修订记录（复核三后）

- N11 终修：任务质量行重排为规范四格（机制｜覆盖与成本｜盲区），成本限定与低敏感/误报边界各归其列；Fleetscanner/Ripple 表的代价行已于第三轮移回表内。

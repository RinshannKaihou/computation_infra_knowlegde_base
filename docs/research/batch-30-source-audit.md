# Batch 30 来源与交付审计

收尾日期：2026-10-21。五任务：T08-04（SDC 检测/训练传播/平台证据，**revise** `knowledge/08-reliability/silent-errors-and-integrity.md`，主题 08.6）、T08-05（统一测试选择/压力注入/统计方法，new `knowledge/08-reliability/test-design-and-coverage.md`，主题 08.7/08.1/08.3/08.4/08.6）、T08-06（可靠性统计/有效产出/恢复损失，new `knowledge/08-reliability/reliability-metrics-and-recovery-loss.md`，主题 08.1/08.8）、T08-07（事故复盘/来源更新/知识维护，new `knowledge/08-reliability/postmortem-and-knowledge-update.md`，主题 08.8/08.3/08.4）、T08-08（诊断评测方法与公开题组，new `knowledge/08-reliability/diagnostic-evaluation-method.md`＋`knowledge/08-reliability/diagnostic-evaluation-fixtures.md`，主题 08.4/08.8）。批内顺序按依赖：T08-04 → T08-05 → T08-06 → T08-07 → T08-08。内容提交 857702c，审阅修订随本收尾提交。

## 来源账面

- registry 559→575：新增 16 项——arXiv:2203.08989（Meta 检测量化，CC BY-NC-ND 4.0，全文）、ACL 2025 LLM 训练 SDC（=arXiv:2502.12340 同研究；全文含附录，两版附录编号不同、引用按版本定位）及其 arXiv v1 附录定位入口（复核轮独立条目）、Llama 3（arXiv:2407.21783v3 固定入口）、Google MPG（arXiv:2502.06982v1 固定入口，CC BY 4.0；v2 已存在未读）、SRE Book Ch.17 Testing for Reliability 与 Ch.14 Managing Incidents、SRE Workbook Ch.10 Postmortem Culture（三章 CC BY-NC-ND 4.0 全文）、Kalibera & Jones arXiv:2007.10899v1（CC BY 4.0，复核轮核正许可与提交日期）、NIST e-Handbook 可靠性章节与 CSRC RTO 术语（复核轮登记）、msprobe 固定 tag（docs 许可 CC BY 4.0 经 docs/LICENSE 复核轮核正）、hiascend DCMI ECC（dcmi_047 逐字段）、Ascend FaultDiag v26.1.1 固定 commit（文件树重新定位后核读）、RCACopilot（CC BY 4.0，复核轮核正）、Cloud-OpsBench v1（固定 v1 入口，CC BY 4.0；无版本入口现展示 v2 未读）。
- 既有条目扩展/核正：src.ocp.sdc-in-ai-2025（补读 §5.2–§7 至文末；pdfinfo 重核 30 页并更正 29 页旧记）；src.huawei.hdk-26.1x-a2-npu-smi-2026-10-08（补核 npusmi_0034 ECC 全字段＋深页 URL）；src.arxiv.llama3-infrastructure 等五条（复核轮：章节定位核正 §3.3.1/§3.3.4、MPG v1 固定、Meta 入口 curl 重定向证据、Adam/dcgm_fields.h/rccl-tests README 精确文件入口入 notes、Kalibera-Jones 与 MPG/RCACopilot 许可核正）。
- 取证方法备注：hiascend `document/detail` 页 JS 挡墙，改用同版本 `doc_center/source` 静态页；ACL PDF 独立抽查附录结构后确立两版版本映射；Meta 登记入口经 curl 捕获 200＋1 次重定向至 networking-traffic、canonical 一致的同文证据；GitHub API 限流不影响 raw 取证。

## 审阅账面（全部 gpt-6.1-sol / xhigh，每轮经 turn_context 核验）

| 任务 | 初审 | 复核轮次 | 终态 |
|---|---|---|---|
| T08-04 | 11 项（P2×8、P3×3）＋复核新增 N01/N10/N11 | 5 轮（第一轮 6/12；第二轮 2/6；第三轮 2/6；第四轮 3/4；第五轮 N11 确认） | 14/14 CLOSED |
| T08-05 | 9 项（P2×7、P3×2）＋复核新增 N01 | 3 轮（第一轮 7/10；第二轮 1/3；第三轮 2/2） | 10/10 CLOSED |
| T08-06 | 12 项（P2×8、P3×4）＋复核新增 N01–N03、N10 | 4 轮（第一轮 5/15；第二轮 5/10；第三轮 1/6；第四轮 5/5） | 16/16 CLOSED |
| T08-07 | 5 项（P2×3、P3×2）＋复核新增 N01 | 3 轮（第一轮 4/6；第二轮 1/2；第三轮 1/1） | 6/6 CLOSED |
| T08-08 | 10 项（P2×7、P3×3）＋复核新增 N01 | 3 轮（第一轮 7/11；第二轮 1/4；第三轮 3/3） | 11/11 CLOSED |

合计 57 项编号发现全部 CLOSED，无 P1、无例外项。会话核验：全部审阅/复核会话（含五轮初审与 18 个后续会话）turn_context 均为单一 `gpt-6.1-sol / xhigh`、工作目录为本仓库；`[frontier_llm]` 命中均为 authoring-guide §7 原文的工具输出引用（抽查确认）。复核主要修订方向：**统计口径**（Fleetscanner/Ripple 共同分母与两类时间终点分列、Llama 3 Table 5 计数/百分比冲突照录不裁定、预算消耗按坏时间直算 83.33%、均值与尾分位规划分列、一般更新过程与 HPP 假设分层、浴盆曲线年龄 hazard 与 ROCOF 分开）；**证据边界**（"静默"三层化、ABFT 假阴性反例并入方法表、NPU SDC 发生率保持 unknown、ACL/arXiv 两版附录编号分列、"换种子上界"加反例范围、合成情境显式标注共三处）；**结构字段**（检测方法表补元数据/指纹/差分/golden/任务质量行并四列对齐、三平台版本化清单、schema 三表＋same_cause/independent_overlap 分组＋goodput 时间分母、六步追溯链补 catalog 重建、真实字段名核正 DCGM_FI_DEV_ECC_SBE/DBE_VOL/AGG_TOTAL）；**入口登记**（arXiv v1/v3 固定、深页 URL 入 notes、多处许可核正、Meta 重定向证据）。未运行任何注入/演练/部署/评测；正文均为 draft、verification source_checked。

## 主题账面

08.6（三缺口关闭：NPU 平台证据清单建立且边界明确、训练侧传播正文、目录级分类升级节级）、08.7（方法两缺口关闭：统一选择矩阵、统计/注入/压力方法；第三缺口"真实环境结果"按验收条款仍由 validation-backlog V 工作包管理，执行 0/7 不变）、08.8（三缺口关闭：有效产出/长期统计方法、复盘与知识更新方法、独立评测集的方法与公开题组——**独立评测集本体仍待 V12 外置获取**）。三主题升已覆盖，覆盖统计 57/6/0→60/3/0（covered 含 6 个 covered_basic）。批次与五任务置 done（completion_record：本文件）。机器可读记录见 plans/topic-coverage.yaml 与 plans/full-coverage-backlog.yaml。

## 写作轮次自记

- 正文均为 draft、verification source_checked（T08-07 为 procedure 且 applicability.environment_refs 空＋notes 说明）；无任何本地环境操作、注入、压力或评测执行。
- T08-04 修订保留稳定 ID 与既有正确章节；T08-08 题组十条（≥8 达标），覆盖训练/推理/硬件/通信/存储/平台＋U 级样例，PTF-08 本地情境/PTF-09 全条/PTF-10 现场情境三处合成显式标注，判据证据均来自固定公开来源。
- 各轮修订记录（含被取代口径的标注）见五份 sources 记录的修订记录小节；08 index 已更新（五条新正文＋08.6/08.7/08.8 地图行）。
- 过程备注：审阅提示词首启因 shell heredoc 截断多字节字符而全败（UTF-8 校验失败），改经 Python 显式 UTF-8 写盘后重试成功；一轮复核报告中指向仓库外技能文件的链接被 make check 拦截，就地改为纯文本（发现内容未动）。
- 下一批 Batch 31：T06-09/T07-12/T02-12/T00-04/T00-05（按依赖图）。

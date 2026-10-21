# Batch 28 · T00-02 第五轮定向复核报告

## 会话元数据与结论

| 项目 | 记录 |
|---|---|
| 角色与范围 | 承接[第四轮定向复核](batch-28-t00-02-codex-recheck-4.md)，仅复核 C05 的四项最小剩余条件，并检查此次修订引入的问题；本会话未编写或修改被审正文、来源记录 |
| 实际执行模型 / 推理档位 | `gpt-6.1-sol / xhigh` |
| 模型核验 | 读取 `CODEX_THREAD_ID` 对应本地会话 JSONL：第 1 行 `session_meta`、第 8 行 `turn_context`（`2026-10-21T08:33:27.530Z`）；记录的模型/档位唯一为 `gpt-6.1-sol / xhigh`，与 `collaboration_mode.settings` 一致；assistant 消息未检出回退标记；未另启模型、审阅 CLI 子进程或子代理 |
| 本轮会话 ID | `01a15d97-d981-7b50-9ab5-9dc2375857a2` |
| 第四轮复核会话 ID | `01a15d92-1332-7de2-b97f-18283b6bceca` |
| 执行方式 | 本地 Codex CLI；`originator=codex_exec`、`source=exec`、`cli_version=0.163.0`；静态定向复核、CommonMark 链接解析与官方登记入口核对 |
| 日期 / 时区 | 2026-10-21 / Asia/Shanghai |
| 工作目录 | `/Users/ywang2397/work/AI_reliability_knowledge_base` |
| 修订正文 | [reference-architectures.md](../../knowledge/00-overview/reference-architectures.md)，157 行 |
| 作者提交的正文 SHA-256 | `4e94e12f5a9b956c5e48e539b219d576eafee423c5b742dc17726697d462ef03` |
| 独立计算的正文 SHA-256 | `4e94e12f5a9b956c5e48e539b219d576eafee423c5b742dc17726697d462ef03`，**匹配**；与第四轮留存副本逐字一致 |
| 现行来源记录 | [batch-28-t00-02-sources.md](batch-28-t00-02-sources.md)，54 行；SHA-256 = `3f6c8a7b4aaec143b5a84b644cc00601d2acb06e7ee277e3a7e58698d6eeb4ca` |
| 第四轮来源记录 SHA-256 | `5f8152dcaec0fa7d50e33407f19c6377a2998ac0c00a6b8832557ade03006c55`，47 行；已独立核验第四轮留存副本 |
| 来源登记版本 | [registry.yaml](../../sources/registry.yaml)，SHA-256 = `a87cd520ba611ef258ab7310359280b192b5d76721265ce4de3876e0950ab605` |
| 来源记录核验 | 主张表 L9–16 的 21 个唯一来源 ID 均存在于 registry；四个产品资料链接的实际目标逐字匹配对应登记 URL；A3 两页匹配既有逐页取证；来源记录 7 处内联本地链接目标均存在；K8s 链接解析结果不满足登记入口定位，详见下文 |
| 写入范围 | 仅新增本报告；不修改正文、来源记录、registry、导航、计划或审核状态；构建在临时源码副本执行 |

**判定：C05 · P3 = OPEN。本轮 CLOSED=0、OPEN=1。**

A3 主张行的两个官方逐页链接及候选共享组限定已落实，四个产品资料 URL 也已准确恢复登记入口。阻止关闭的直接原因是来源 L14：登记 ID 说明被写入 Markdown 链接目标，包含未转义空格，CommonMark 未生成 K8s 链接，不能认定恢复了可点击的登记入口。修订摘要另有原有一致性残留：L43 已加订正，但其指向的 L47 仍称“此前第二轮脚本仅 A3 行实际生效”，与新增 L51 对前两轮均未生效的说明冲突。

K8s 链接破坏是此次修订引入的定位问题，仍属于 C05 原有关闭条件，不另立 N02。未发现此次修订引入的独立技术主张问题。此前已关闭的 C01/C02/C03/C04/C06/N01 沿用原状态；本报告不构成 T00-02 审阅闭环或 Batch 28 整批验收，不改变 `draft / source_checked`，也不建立硬件验证结论。

## 范围与版本证据

已读取 [README](../../README.md)、[写作指南](../authoring-guide.md)、[AGENTS](../../AGENTS.md)、[内容总目录](../../content-outline.md)及[内容元数据 schema](../../schemas/content.schema.json)，以第四轮报告的最小清单为本轮边界。关联的[资源拓扑](../../knowledge/01-hardware/resource-topology.md)及[Batch 14 组成取证](batch-14-supernode-composition-sources.md)仅用于确认 A3 逐页入口及既有样板定位，不重新验收关联正文。

版本比较使用第四轮留存副本 `/private/var/folders/bk/3f4npkcs6l30twg9ph23c2jh0000gn/T/t0002-recheck4-193tbz1b/repo`。先复算正文与来源记录哈希，均符合第四轮报告，再逐行比较：正文完全未变；来源记录仅改 L10/L11/L13/L14/L43，并新增 L49–54。L47 原句未改，unknown 清单 L18–23 及此前有效的 05/04/03 域入口均保留。

以下行号绑定元数据表所列现行文件哈希。临时副本只作版本差异证据，不当作厂商原文缓存；作者回应与修订摘要不代替实际条目核验。

## C05 最后剩余条件逐项判定

| 第四轮条件 / 位置 | 本轮核验 | 判定依据 |
|---|---|---|
| 来源 L10：A3 产品概述/组网拓扑写入主张行 | **满足** | 两个链接实际出现在“精确位置”栏，CommonMark 分别解析为 `EDOC1100401572/bd23f260`、`EDOC1100401572/d975beba`；与正文 L110、资源拓扑及 Batch 14 的既有逐页入口一致。保留 Batch 14 核对说明，支持范围改为“组成/互联（故障域为候选共享组口径）”，未宣称本轮重获原文或验证故障影响。 |
| 来源 L11/L13：四个产品资料 URL 对齐登记 | **满足** | 四个实际链接目标均逐字匹配各自 registry URL，路径差异已全部消除，详见下一节。AMD 主张与 unknown 第 2 条继续限定“本库本轮未取得”和既有取证范围；没有新增 AMD 超节点外推。 |
| 来源 L14：恢复 K8s 登记入口并区分观察口径 | **未满足** | 已去掉 v1.32 域名，但登记 ID 说明位于链接目标的 ASCII 圆括号内，目标含空格；CommonMark 将 K8s 整段保留为文字，仅生成同一栏后续两篇 05 域本地链接。实际可点击目标没有恢复为 `https://kubernetes.io/docs/concepts/architecture/`。 |
| 来源 L43/L47：明确旧完成声明偏差 | **部分满足，仍有残留** | L43 新增“该轮脚本实际未生效于 A3 行”的订正，L51 也明确前两轮未生效；但 L43 指向“复核第三轮修订”，该处 L47 仍保留“此前第二轮脚本仅 A3 行实际生效”，没有就地标明失实或已被订正。第四轮要求处理的 L47 偏差仍在；最新补记不能使两处相反表述一致。 |

来源 L15–16 的四个 04/03 域链接及 L14 的两个 05 域链接均仍可达；主张表 21 个唯一来源 ID 均可解析。正文未改，原有就近引用和未验证边界保留；不再要求改写正文、补新 AMD 样板或重做已关闭发现。

## 链接与上游证据核验

| 位置 / 对应登记 ID | 现行实际入口与本轮读取范围 |
|---|---|
| L10 / `src.huawei.atlas-900-a3-superpod-user-guide-13-2026-06-25` | [产品概述](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/bd23f260)、[组网拓扑](https://support.huawei.com/enterprise/zh/doc/EDOC1100401572/d975beba)均位于登记指南的同一文档树，匹配既有精确定位。本轮分别返回 HTTP 403，未取得厂商正文；只确认定位写入与历史取证对应，不重核指南 13 全文。访问受限本身不阻止本轮补链接条件关闭。 |
| L11 / `src.supermicro.as-8125gs-tnmr2-manual-mnl-2671-r1.0b` | [MNL-2671.pdf](https://www.supermicro.com/manuals/superserver/8U/MNL-2671.pdf)与登记 URL 一致；网页工具返回文件过大（40,902,491 字节）的限制，未读取 PDF 正文。不声称本轮重核 Rev 1.0b 或 §1.1/§1.2；沿用 Batch 14 取证定位。 |
| L11 / `src.amd.instinct-mi300x-platform-datasheet-2023` | [MI300X 平台数据表](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-platform-data-sheet.pdf)与登记 URL 一致；成功读取两页，标题、首面 UBB/8 加速器说明及第二页平台段与节点级样板对应。仅核对文档身份与本行范围。 |
| L13 / `src.nvidia.dgx-h100-h200-user-guide-2026-01-26` | [Introduction 页](https://docs.nvidia.com/dgx/dgxh100-user-guide/introduction-to-dgxh100.html)与登记 URL 一致；成功读取标题、开篇与组件表，支持八 GPU 节点级样板。现行页脚已为 2026-10-17，不能据本轮读取宣称取得 2026-01-26 快照；L13 的旧日期沿用历史登记口径，不追改其观察记录。 |
| L13 / `src.huawei.atlas-800t-a2-product-2026-09-29` | [Atlas 800T A2 产品页](https://e.huawei.com/cn/products/computing/ascend/atlas-800t-a2)与登记 URL 一致；成功读取产品标题与“技术规格”，只支持既有主机、存储、网络、供电等节点组成范围，不由此补写 NPU 数量或节点内互联。 |

K8s 登记条目 `src.kubernetes.cluster-architecture-2026-10-08` 的 URL 是[无版本 Cluster Architecture 页](https://kubernetes.io/docs/concepts/architecture/)，revision 明确为“可变网页，2026-10-08 观察”。本轮单独打开该精确入口成功，控制面、worker nodes、调度器与节点组件段与概念范围对应；此次读取不是历史观察页快照的复现，也不能补救来源 L14 的 Markdown 语法问题。

现行来源 L14 的相关片段为：

```markdown
[K8s 集群架构](https://kubernetes.io/docs/concepts/architecture/（src.kubernetes.cluster-architecture-2026-10-08 登记入口）)
```

使用本地已有 `markdown_it.MarkdownIt('commonmark')` 对现行行执行 `parseInline` 和 `renderInline`：K8s 片段未生成 `link_open` 或 `<a>`；该行只有 `kubernetes-job-lifecycle.md`、`slurm-jobs-and-device-resources.md` 两个本地链接。原因是中文括注连同空格都在 ASCII 链接目标括号内，既不是目标外的说明，也不是合法的带引号链接标题。这是本地可复核的确定性问题，不是远端访问失败。即使某些渲染器宽松处理，也不能把附加说明的目标视作登记 URL。

## 最小剩余修订与新问题检查

1. **来源 L14**：将登记 ID 说明移到 Markdown 链接目标括号之外，例如下列形式；关闭时确认解析出的实际 `href` 恰为登记 URL，而非仅查找 URL 子串：

   ```markdown
   [K8s 集群架构](https://kubernetes.io/docs/concepts/architecture/)（src.kubernetes.cluster-architecture-2026-10-08 登记入口）
   ```

2. **来源 L43/L47**：在 L47 就地订正或标明“此前第二轮脚本仅 A3 行实际生效”为旧误述；L43 的交叉说明应指向实际说明 A3 最终落实的“复核第四轮修订”，避免指向仍含相反陈述的第三轮摘要。保留历史轮次时明确：第二、三轮未实际写入 A3 链接，至第四轮修订才落实。

本轮新增的 K8s 链接失效并入 C05；摘要残留是第四轮已指出的一致性问题延续，不重复编号。A3 候选共享组限定没有新增故障影响定论，四个恢复登记的产品资料 URL 没有扩大技术支持范围，正文也没有新增数字、兼容组合、成本排序、实测或部署声明。DGX 在线页更新属于外部可变资料的观察边界，不是此次修订引入的内容变更，不另立发现。

上述两处完成后，仅需按实际主张表链接解析、登记对应及摘要一致性再次定向核对；无需新增来源或改动正文。模型审阅不替代真实环境验证。

## 校验与写入范围

报告落盘后，工作区执行 `PYTHONDONTWRITEBYTECODE=1 make check`，退出码 0：**PASS: 117 content entries; 553 sources**。`git diff --check` 通过。在包含本报告的临时源码副本 `/private/var/folders/bk/3f4npkcs6l30twg9ph23c2jh0000gn/T/t0002-recheck5-p22li9ko/repo` 执行 `make build`（使用工作区现有虚拟环境的 Python），退出码 0，重新生成两个 catalog；读取 JSON 确认 `documents=117`、`sources=553`。副本预先保留历史文档引用的 build 文件后重建，工作区 `build/` 未写入。

另用 CommonMark 解析正文、来源记录及本报告，分别核对 31、7、11 处内联本地文件链接，目标均存在；无行尾空白，文件末尾换行正常。对来源 L14 的解析另核对实际链接 token 与 HTML 输出，避免将完整 URL 字符串的出现误认成有效链接。结构工具不核验远端内容、历史版本对应、取证语义或技术正确性，结构通过不能关闭 C05。

写入前留存的 618 个既有文件（排除 Git、虚拟环境与缓存）在交付核验时指纹均未改变、无文件删除；新增文件仅本报告。正文、来源记录及 registry 交付前复算仍与元数据 SHA-256 一致。未修改 `src/kb/`，未新增或运行代码回归测试；未访问真实设备/集群，未执行调度作业、性能测试、故障注入或部署验收。

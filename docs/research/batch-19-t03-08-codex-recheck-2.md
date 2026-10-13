# 第十九批 T03-08 第二次定向复核

审阅日期：2026-10-13（Asia/Shanghai，本机日期确认）。正文的 `2026-10-14` 是作者交付标签，不作为本轮实际取证日期；输入身份以下表 SHA-256 为准。

**结论：本轮 C25、C26 CLOSED；C23、C24、C27 OPEN（3 项 P2）。本批累计 24 CLOSED / 3 OPEN（审阅发现），T03-08 未通过。** C01–C22 沿用既有 CLOSED，不重新审阅。BLOCKED-1（HCCL Test × 目标 CANN/HDK/机型官方交集）仍单列 blocked_on_evidence/open，不计入发现数量。T03-06/T03-07 的已交付有限文档/来源范围通过保持；整个 Batch 19 未验收。

约定配置 `gpt-6.1-sol / xhigh` 仅记录为用户约定，不写成已独立确认的执行模型或推理等级。执行者为当前 Codex 主会话，角色为独立审阅者，与作者修订角色分开；无子代理。本轮只写本报告，不代作者修订，不新增发现 ID。四分支判据中本轮发现的逻辑问题追记于 C23。

## 输入与复核范围

| 输入 | SHA-256 |
|---|---|
| [T03-08 正文](../../knowledge/03-communication/bandwidth-degradation-triage.md)（procedure / draft） | `32d762aa4b66b2ff0a3cd5f835371ecf75bf4f5a382349e0478656b1972d4015` |
| [作者来源记录](batch-19-t03-08-sources.md) | `87b4657a9e0ce64fa11e6e83832eb5202b83148538a817b1259fbd793c11a4e4` |
| [修订映射](batch-19-review-fixes.md)（T03-08 L97–104；第二轮 C23–C27 L106–112） | `5ceee47bff7c0583f7310b14905242057fbd52f4a763780191ec7d98f09ad6c9` |
| [前次定向复核](batch-19-t03-08-codex-recheck.md)（C23–C27 剩余关闭条件权威来源） | `1522f120c8ae331cbaa9a8e3aba5fb6f3d6ffa636958a2dadea443847124e916` |
| [加法初审](batch-19-t03-08-codex-review.md)（原发现、格式及边界） | `a037c2be9116bce802617a2de0c3e2169fe16bd9199443d463cbbd36722f9a7f` |
| [任务验收](../../plans/full-coverage-backlog.yaml)（T03-08 acceptance 1–4，L5006–5010） | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

判定逐项对照前次复核 L56–106 的剩余条件，不以修订映射的“已删除”“已重写”“七要素”等自述替代正文/记录。来源记录表仍只有 7 条主张行；本轮逐行检查完整 ID、URL、字段及支持范围。

必要依赖只读核对，不重新审阅其历史发现；来源登记用于 C26 的第三处删除及 C27 的 ID 解析，不修改登记。

| 补充只读输入 | SHA-256 |
|---|---|
| [来源登记](../../sources/registry.yaml) | `277aecb64892438a366c1729fe01210cbeae60845ff6fbefce437a7a7a96901e` |
| [T03-07 基线口径](../../knowledge/03-communication/bandwidth-baselines.md) | `8c2884b63cf7b638c1df2d7de88f5fe9d2923c0d95b025548041aea203574039` |
| [T03-03 RDMA 诊断](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `7f6d59752e7c74628f2c9d706ce2ec00e3031ecd36230554eb8d2680fee67412` |
| [T03-05 RCCL 档案](../../knowledge/03-communication/rccl-runtime-and-verification.md) | `1f95d5b310726d858900e2028ab3b779f1470b03a1ba67187fbed1c6da5b19db` |
| [T03-06 通信库对照](../../knowledge/03-communication/communication-library-profiles.md) | `d4a5fb535ba78d852e070f09ff387b69dc6e1ab7cf86620c7ee08e9a99577646` |

## 一次源取证与方法限制

采用本地只读逐行检查、默认 TLS 校验的只读 curl、允许的 GitHub 连接器及网页阅读器。curl 对 #2409 API、NCCL 2.27.5 env 和 RCCL docs-10.1.0 troubleshooting 的请求均因沙箱 DNS 失败：exit 6、HTTP 000、下载 0 字节。HTTP 000 不是上游状态，不据此判来源失效；未使用 `-k/--insecure`，未修改 DNS、代理或 TLS 配置。

GitHub 连接器取得 #2409 body 与四条评论、#814 body 与六条评论、#209 body 与评论。长结果存在显示截断，故 #2409 深度表和 #209 绑定建议另取精确 comment API；#814 开帖另由网页阅读器取得完整正文，与评论交叉检查。网页阅读器取得 env、ACS、RAS、UFM 的精确页面/锚点。RCCL docs-10.1.0 的 HTML 阅读仍返回 Internal Error；另读取已登记 `therock-10.1` 的官方文档源码，核对工具用途，**不冒充该 HTML 已实开，也不声明两者全文相同**。本轮没有可供计算原始远程 HTTP 字节 SHA 的 curl 响应，不补造远程哈希。

| 一次源 / 已登记 ID | 精确位置与本轮证据 | 支持范围 / 限制 |
|---|---|---|
| `src.nvidia.nccl-issue-2409` | [开帖](https://github.com/NVIDIA/nccl/issues/2409) Environment、§1/§2/§4 | 环境、rail 扫描及开帖的 NCCL 侧限制假说；该假说被最终回复纠正，不是最终根因证明。 |
| `src.nvidia.nccl-issue-2409` | [粒度跟帖 5660150852](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660150852)，message size × 1/8 QP 表 | Ndministrator 的 host-memory、同节点对、mlx5_0、单向对照及 NCCL 内部开销假说；不是修后证据。 |
| `src.nvidia.nccl-issue-2409` | [深度跟帖 5660232470](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5660232470)，两张表；另取精确 API | 128 KiB 的 293.4/392.1/392.0 Gb/s 分属 1 QP/depth 8、8 QP/depth 8、8 QP/depth 64。depth 1 表为 1 QP，128 KiB 117.0 Gb/s 对应约 8.8 us 推算。上下文为 mlx5_0、host memory、单向、每点 3 s；默认 tx depth 128 不覆盖显式 depth 8/64/1。 |
| `src.nvidia.nccl-issue-2409` | [报告者修正 5673453587](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5673453587)，平台/config 两项与修后表 | ACS＋IOMMU 与误设 QP split 的报告者归因、分步修后比较、ADAPTIVE_ROUTING 修后无差；约 97% 相对报告者引用的未核验期望。 |
| `src.nvidia.nccl-issue-2409` | [维护者关闭 5699369631](https://github.com/NVIDIA/nccl/issues/2409#issuecomment-5699369631) | stephenmsachs 按请求关闭；没有独立复现、库发布修复版本或本库实测。 |
| `src.nvidia.nccl-issue-814` | [开帖](https://github.com/NVIDIA/nccl/issues/814)，拓扑 XML、P2P 与 pairwise 表、末尾 ring 调整；[首个维护者回复](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1493802672)、[作者关闭](https://github.com/NVIDIA/nccl/issues/814#issuecomment-1496450442) | 6×RTX 4090/AMD CPU 个案；ring 调整未果，维护者以推断语气解释双向/多流交织，作者未交付替换 CPU 的验证。不支持最慢链路因果证明、tree 流量解释或 `--bind-to none` 归属。 |
| `src.nvidia.nccl-issue-814` | [2.23 评论 2283482549](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2283482549)、[GeForce 澄清 2825666454](https://github.com/NVIDIA/nccl/issues/814#issuecomment-2825666454) | 前者是更多场景避让 P2P、不超出 PHB 设置效果；后者澄清不表示近期 GeForce 支持 P2P。两者不是 RTX 4090 修复/支持证明。 |
| `src.nvidia.nccl-issue-209` | [TCP 开帖](https://github.com/NVIDIA/nccl/issues/209)、[绑定建议 491475792](https://github.com/NVIDIA/nccl/issues/209#issuecomment-491475792)（另取精确 API） | 无 RDMA、NET/Socket；绑定和 socket 驱动线程的一线检查建议，不外推 IB，不作为通用验证修复。 |
| `src.nvidia.nccl-user-guide-2.27.5` | [QP split 参数](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-ib-split-data-on-qps)、[ACS](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#pci-access-control-services-acs)、[RAS sample output](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output) | 所读归档的 split 默认 0；ACS 的 DMA 路径作用；MISMATCH 可为瞬态。配置语义及进度响应不等于物理错误证据。 |
| `src.nvidia.ufm-41815-port-counters` | [InfiniBand Port Counters](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)，Rcv Errors、Symbol Errors、Link Error Downed、Xmit Discards 行 | 接通正文所引用 T03-03 L79–98 的 UFM 4.18.15/IB 口径。Rcv Errors 包含物理错、畸形包及 overrun；Xmit Discards 多因。字段语义不证明目标设备具备该能力，也不能把所有收错都定为硬件根因。 |
| `src.rocm.rocm-systems-therock-10.1`（`src.amd.rccl-docs-10.1.0` HTML 未重取成功） | [官方 troubleshooting 源码](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/docs/how-to/troubleshooting-rccl.rst)，Using the RCCL Replayer / Collect the TransferBench data；Git blob `89779e32d545fcd1f61a7dc728e0abf9113bc186` | Replayer 用 collective 日志和 dummy data 回放；TransferBench 对指定设备间并发拷贝做基准。它们不是仅凭名称就成立的真实端点/rail/transport 替代。未构建或执行。 |

## B19-C23 — P2 / OPEN：分支表述已细化，但门禁仍不完整且配置判据反向

位置：正文 L76（步骤 8），参照 L51/L55–63 的共同输入；来源记录 L10；修订映射 L108。对应 acceptance 2；剩余条件依据前次复核 L64。

| 分支 | 已接受证据 | 仍不足 / 判定 |
|---|---|---|
| 路由/映射/热链路 | 已列 rank→设备→NIC/端口、算法/QP/rail 输入；明确映射缺失 unknown；#814 多流解释已有精确评论及推断限定。 | “实际传输与预期一致且同窗遥测方向一致”本身不能确认错误映射或热点；没有预期负载/历史对照及端口集中度定位。把“映射错误纠正后复测恢复”写在**排除**下，实际支持原配置/映射原因，不能作为排除整个分支。OPEN。 |
| 共享 CPU/网络/存储干扰 | 已分别要求隔离轮与背景轮，并写背景退化/隔离恢复、两轮无差、缺轮或同窗记录不能判争用；#209 TCP 限定正确。 | 此部分在共同同口径前提下接受为分支级比较门禁；具体各轮变更/保持/原生输出仍按 C24 审查，不重复新增问题。 |
| 物理错误 | 已通过 T03-03 接通 UFM 字段语义/IB 作用域/版本；Xmit Discards 多因及未选字段 unknown 的限制成立，ACS/IOMMU/GDR/注册移出硬件错误。 | 仍只列错误类别，没有实际最小输入及支持/排除门禁：所选端口/字段、前后值/增量、窗口/重置边界、路径关系及掩盖/覆盖声明怎样支持或只能排除已观测范围未给出。Rcv Errors 的 overrun 等不能统一当成硬件物理根因；当前“物理错误”标签需要限强度。OPEN。 |
| 调用/消息变化 | 实际 collective、datatype/count/root/rank/次序及消息记录已接回同口径比较；参数差异纠正后恢复支持、参数一致排除该类差异的方向正确。 | 本支已有实际比较规则；仍需补实际记录/消息序列缺失或未能对齐时的 unknown 门禁，不只要求“回链”。OPEN。 |

新增判据问题仍属于 C23 的原关闭条件，不新增 ID。#2409 最终回复的分步平台/配置修正后比较也说明“纠正后恢复”用于支持原配置原因；这里是审阅者对门禁逻辑的判断，不把该个案泛化为操作处方。T03-07 L154–159 已有热点同窗端口定位/对照口径，可精确链接复用，不要求实测。

**剩余关闭条件：**纠正路由/映射的支持/排除方向，并把配置不一致与热点集中分开判读；可链接 T03-07 的实际最小输入和同窗端口定位条件。为物理支给字段/版本/端口/窗口/增量/重置及路径关系、支持/有限排除/unknown 契约，不能仅列错误名或把无错误等同链路健康。补调用记录不足时的 unknown；保留已经成立的三域隔离/背景比较及 TCP 个案边界。所有结论强度继续受 C22 既有时窗限制约束，不重开 C22。

## B19-C24 — P2 / OPEN：工具和风险边界纠正，流程前向入口与逐轮方案仍缺

位置：正文 L75–77/L81–94；来源记录 L11；修订映射 L109。对应 acceptance 4；剩余条件依据前次复核 L74。

已接受：步骤 8→9 明确，步骤 9 已写完成→回 7、未完成→unknown；测量、日志回放、解析候选、真实 rail/NIC/传输替代已有用途区分。TransferBench 明确为设备间拷贝基准，未再当作日志回放；RCCL 档案及 troubleshooting URL 已接入。失败/超时/异步错误/窗口失效单列停止，原值/批准修复配置恢复、同条件正确性/覆盖复测及不新增授权均保留。所读 RCCL 官方源码支持工具用途分开；HTML 通道失败不据此否定已修正的用途描述。

仍不足：

1. **7→8 未明示。**L75 的默认下一步仍为满足完成判据后结束；L77 的补充只说“步骤 7 在步骤 8/9 证据齐全……后汇总”，没有定义什么未完成候选/证据缺口从 7 转入 8。步骤 9 内文返回 7，末列却仍“满足完成判据后结束”；没有统一前向进入、返回及结束的条件。
2. **“每轮列”仍是作者待填要求，不是逐轮交付。**L77 一句列出七类字段，但没有分别给隔离基线、可控背景、单变量及替代端点/rail/路径轮的具体输入、变更项、保持项、原生输出、正确性/完整性和无法判断/判定契约。缺输入记 unknown 的通则不能代替这些具体设计；来源记录 L11 的“基线→单变量→替代路径”也不是设计表。RCCL 档案 L91–99 是特定两节点最小运行/异常支路，并非本页四轮方案；不能以整页链接补齐未给出的每轮内容。
3. NCCL/HCCL 既有版本化资料入口可读，RCCL 新入口已补；但“链接……资料”这一要求句不等于已选择每轮版本/能力。未选工具须继续标未完成候选，不能用末列“每轮输入/判定齐全”预先认定可执行。

**剩余关闭条件：**在新增说明里给清楚的 7→8→9→7 进入/返回/结束条件，协调步骤 9 内文与末列。实际列出上述四类轮次的七要素及判定，变更/保持项分开，CPU/网络/存储背景各自有可重现输入，真正替代的端点/rail/transport 明确；允许不填任何测量值。未选版本/输入/能力的轮次标未完成/unknown，并接通相应 NCCL/HCCL/RCCL 条件。保留已接受的工具归位、失败停止、原值/批准配置恢复与覆盖复测边界。

## B19-C25 — P2 / CLOSED：五阶段、对照列身份与配置修复边界已成立

位置：正文 L98–108；修订映射 L110。对应 acceptance 3；剩余条件依据前次复核 L84。来源记录的表格定位残留另归 C27，不撤销已经成立的正文案例定位。

正文现在分别定位开帖、粒度跟帖、深度跟帖、报告者修正和维护者关闭。L99 交代开帖的 NCCL 侧限制假说及最终纠正；L100 标粒度阶段仍为 handoff 假说；L101 给精确深度评论、mlx5_0/host buffer/单向/3 s，并将 293.4 与 392.1 明确分属 **1 QP/depth 8 与 8 QP/depth 8**，392.0 为 8 QP/depth 64。depth 1 的 128 KiB 约 8.8 us 明确为推算；链接源表进一步固定为 1 QP，而不是默认深度或另一条修后测量。

L102/L104 给完整 `NCCL_IB_SPLIT_DATA_ON_QPS`，默认 0 与所读 2.27.5 参数页一致。最终回复的分步平台修正、配置修正及 ADAPTIVE_ROUTING 无差，与正文列值/角色相符。L103 继续把 perftest 的反证限于覆盖路径/参数/窗口，不保留普遍排除 fabric 规则；L105 的关闭按报告者请求、L106 的约 97% 相对未独立核验期望估算、L104 的配置修复非库发布修复版本，均与一次源吻合。实际环境及不同库/测试快照身份沿用前次已接受内容，未重新审阅既有关闭项。

**剩余关闭条件：无（本项）。**只关闭来源整理的案例阶段/参数/强度问题，不证明双因在本库复现、交换机遥测可用、期望门槛正确或任一环境的修复适用性。

## B19-C26 — P2 / CLOSED：三处撤销成立，#814 的后续评论没有合并外推

位置：正文 L76/L109；来源记录 L14；来源登记 L4851；修订映射 L111。对应 acceptance 2/3；剩余条件依据前次复核 L94。

步骤 8 已无“环受最慢链路限制为 #814 个案解释”；案例索引 L109 和来源登记 L4851 都只保留“无原文支持/已删除归属”的撤销说明，不再断言最慢链路因果。关键词残留是撤销说明，不是三处删除失败。来源记录 L14 及映射与这三处一致。

正文逐条链接维护者解释、作者关闭、2.23 评论及 GeForce 澄清；原 body 的拓扑/矩阵与 ring 顺序调整未果、维护者多流/双向的推断语气、作者未验证替换 CPU 即关闭均分开。2.23 的 P2P 避让不超出 PHB 设置效果，与“近期 GeForce 不支持 P2P”的后续澄清没有被合成 RTX 4090 能力或验证修复。`--bind-to none` 已归 #209 TCP 检查建议，未归给 #814；没有新增 tree 流量解释归属。

**剩余关闭条件：无（本项）。**来源记录尚未逐条写入评论 URL 属 C27 的映射完整性，不能因此把已经撤销的错误因果归属再次算 OPEN。

## B19-C27 — P2 / OPEN：正文状态部分同步，但记录映射和轮次仍未兑现

位置：正文 L34/L60/L74/L76–77/L118–121；来源记录 L3/L9–15/L19；修订映射 L112。对应 acceptance 1–4 的可追溯性；剩余条件依据前次复核 L106。

已接受：L10 的 env/ACS/RAS 有精确锚点，本轮已重新核对；L11 已用完整 RCCL 文档/源码登记 ID。正文 L119 接入本轮作者记录；L76 的 T03-03、L77 的 RCCL 档案及 L118 的 T03-07 入口有效。正文 L60/L34、来源记录 L19 已将旧遥测缺口限定为原批（Batch 09），区分当前文档可复用与现场能力未知；L118 与 verification/来源记录的“已交付字段契约和判据，非实测矩阵”一致，T03-07 L144–161 也只给字段及判断条件。没有预写本轮通过或关闭 BLOCKED-1。

仍不足：

| 定位 | 未满足的原关闭条件 |
|---|---|
| 来源记录 L9–10 | 时间窗行用“—（方法整理）”，只有任务简称/整页链接，未列所依赖完整内容 ID；四分支行未把新采用 UFM 错误字段映射到 `src.nvidia.ufm-41815-port-counters` 及精确字段/范围。已有 env/ACS/RAS 精确 URL 不覆盖这些新增物理字段。 |
| 来源记录 L11 | Replayer/TransferBench 仍只链 RCCL 整页并误定位到“两节点设计节”（工具实际在 RCCL 档案 L69–71，设计在 L91–99）；未给官方具体工具节/URL。FaultDiag 仍只写存在性、版本待定，未形成可核验来源定位；若未选，应只保留未采用候选，不算设计已完成。 |
| 来源记录 L12–15 | #2409/#814/#209 仍只链接 Issue 首页；没有正文已经补出的四条 #2409 评论、所用 #814 评论及 #209 绑定评论逐项 ID—URL—字段—范围。L13 仍以“同上”“同页”替代独立可解析的 ID/URL，不能把正文的准确链接等同作者记录表已重写。 |
| 来源记录 L3/L19；正文 L34 | C1/C2/C3、S4/S5/S6/S7 仍无本记录内定义/映射，unknown 清单保留悬空代号。正文 verification 写作者首轮＋第二轮＋本轮三阶段，记录 L3 仍“首轮＋本轮”，未同步本次第二轮修订的取证阶段/角色；本报告不能替作者证明其此前实际打开记录。 |
| 正文 L74/L121 | L60 已加历史限定，但 L74 仍“本库尚未核对此类来源”，L121 仍把链路级计数器“可用来源”列为待确认，未显式限定该两处为原批范围、区分已核对 UFM/mlx5/Cumulus 文档与目标机型字段能力 unknown。读者需要自行选择全库状态版本。 |
| 正文 L76–77/L118–119 | T03-03/05/07 已接入；T03-06 `communication.communication-library-profiles` 仍无本页直接入口，对照工具/条件仍有“链接……资料”的要求句。矩阵状态同步成立，不代替尚缺的工具/平台条件映射。 |

**剩余关闭条件：**把仍缺的每项主张写成完整来源/内容 ID—精确页面或评论 URL—字段/段落—支持及未覆盖范围，尤其 UFM、新采用工具和案例各阶段；替换“同上/同页”，定义或删除悬空代号，未选工具明确仅候选。修正 RCCL 工具节定位并接入 T03-06 等实际对照条件。同步 L74/L121 的原批遥测缺口/当前文档/现场能力边界；保留已成立的矩阵字段契约而非实测表述。正文与记录按实际作者首轮、第一次修订、第二次修订及独立审阅轮次/角色同步，不能把映射的完成自述或审阅者取证当作者已完成的证据。

## 状态集合与验收影响

| 状态 | ID / 范围 |
|---|---|
| 本轮 CLOSED（2） | C25、C26 |
| 本轮 OPEN（3 P2） | C23、C24、C27 |
| 既有 CLOSED（22；不重开） | C01–C22 |
| 本批累计审阅发现 | **24 CLOSED / 3 OPEN**（共 27 个 ID，未新增） |
| 既有验收子项 OPEN（单列） | BLOCKED-1，blocked_on_evidence；不计入发现数量 |
| T03-08 | **第二次定向复核未通过**；下一轮仅复核 C23/C24/C27 剩余关闭条件 |
| T03-06/T03-07 | 已交付有限文档/来源范围通过保持；不重新验收 T03-06 acceptance 5 |
| Batch 19 | 未完成整批验收，不由本次局部 CLOSED 推导全部完成 |

acceptance 1 的时窗/矩阵字段契约保持既有接受，不重开 C22；acceptance 2 的配置/物理支门禁仍由 C23 阻挡；acceptance 3 的正文案例与 #814 归属本轮满足，但来源记录完整性仍受 C27 限制；acceptance 4 的前向入口/逐轮设计仍由 C24 阻挡。模型审阅和结构校验都不建立硬件验证或版本兼容交集。

## 检查边界与写入范围

- 仅新增本报告；不改正文、作者记录、映射、来源登记、计划、索引或来源审计。工作区既有改动不恢复、不提交、不创建分支。
- 不执行 benchmark、collective/MPI、实机采集、配置修改、故障注入、库升级或报告所引用的上游命令；正文/上游的诊断和实验命令仅作阅读。
- 未取交换机原始计数器/现场时钟/目标机型能力，未核验 nccl-tests#309 期望来源，未验证 HCCL Test × CANN/HDK/机型交集；这些 unknown 不因来源可读而消失。
- 原始远程 curl 未完成；允许的替代只读通道完成本报告所列关键语义核对。RCCL 使用精确已登记 tag 的官方源码核对工具用途，不声称 HTML 实开成功或所有版本相同。
- 为遵守“只写这一份报告”，在包含本报告及既有构建文件的临时仓库快照运行 `make check` / `make build`，均 PASS（88 content entries / 389 sources）；构建产物仅写临时快照，原仓库 `build/` 不重建。结构和本地链接通过不验证技术正确性或远程语义。
- 本报告 11 处本地链接、11 个不同目标均存在。写入前后 SHA 清单核对：原有 307 个受保护文件（含既有构建文件）均不变、无删除，仅新增本报告；六项任务输入与输入 SHA 表一致。未修改 `src/kb/`，不执行 `make test`。

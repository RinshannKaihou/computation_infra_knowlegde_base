# Batch 22 整批收尾独立审阅

审阅日期：2026-10-17（Asia/Shanghai）。审阅者：本地 Codex CLI 的独立审阅角色，与作者角色分离；本轮未委派子代理或其他模型。约定模型为 `gpt-6.1-sol / xhigh`，实际可见运行元数据的核验见文末。

## 1. 结论

**结论：需修订后定向复核，暂不宣告整批收尾无保留通过。** 内容交付、六项内容缺口关闭、任务账面补正和未来主题验收分工成立；发现 **P3 两项、P1/P2 零项，B22X-C01、B22X-C02 均 OPEN**，分别为 T05-04 审阅轮次与模型核验计数未同步、章节导航仍把 T05-02/T05-03 写成待审阅。

这两项是记录一致性问题，不是要求撤销六项缺口关闭，也不重开历史 B22-C01–C44。作者账面 `Batch 22: done` 已存在，本报告不修改它；本轮独立审阅的通过状态须在作者修订、同一审阅者定向复核后另行确认。

| 审阅项 | 本轮判断 |
|---|---|
| 六个缺口是否已有足够的内容层交付 | 成立，限各任务约定的版本化样板与方法层范围 |
| T05-02/03/04/05、Batch 22 与复核报告及审计任务表是否一致 | 交付状态与历史发现闭环一致；轮次/核验记录有 B22X-C01 |
| 主题状态、后续任务、稳定 ID、真实历史、draft/验证边界 | 保持；章节导航状态有 B22X-C02 |
| 结构和本地链接 | `make check`、`make build` 均通过；不证明技术或远程链接正确 |
| 两个收尾提交是否夹带非所述改动 | 未发现；详见第 7 节 |

模型审阅不构成平台、硬件、兼容组合或现场验证。

## 2. 工作区、输入与取证范围

开始执行的首组命令包含 `git log --oneline -5` 与 `git status --short`。HEAD 为 `34d98c9010246c29c5921feba087294abcce0b2a`，工作区干净；其前四项为 `f9d8a15`、`dacf274`、`82647df`、`4b4c077`。报告写入前 HEAD 不变，作者文件无工作区或暂存区差异，目标报告此前不存在。

已读取 [AGENTS.md](../../AGENTS.md)、[README](../../README.md)、[编写指南](../authoring-guide.md)（特别是 §7，L124 起）、[内容总目录](../../content-outline.md)的领域边界，以及本次计划、盘点、正文、来源记录、历史复核报告与提交差异。`docs/`、`plans/`、`knowledge/`、`sources/` 下未找到更深层 AGENTS.md。

### 2.1 输入哈希：开始时与成稿前

以下为整文件原始字节 SHA-256，使用 `shasum -a 256`。开始快照：**2026-10-17T21:59:22+08:00**；成稿前快照：**2026-10-17T22:06:51+08:00**。四项全部一致，无输入漂移。

| 输入 | 开始时 SHA-256 | 成稿前 SHA-256 |
|---|---|---|
| [plans/full-coverage-backlog.yaml](../../plans/full-coverage-backlog.yaml) | `6f44bd8e41c9d7e1c2554f5d4d97beb86a166552d911124c1fbbabdefc6da561` | `6f44bd8e41c9d7e1c2554f5d4d97beb86a166552d911124c1fbbabdefc6da561` |
| [plans/topic-coverage.yaml](../../plans/topic-coverage.yaml) | `988ab0da5d8b903af14f3f960ec6aba318994832f98b5c5a22d7672d37a774dd` | `988ab0da5d8b903af14f3f960ec6aba318994832f98b5c5a22d7672d37a774dd` |
| [docs/topic-coverage-audit.md](../topic-coverage-audit.md) | `54617a0f34c2699c9e04eccdf749850176cc3f4958667873db133d0205ca7c5d` | `54617a0f34c2699c9e04eccdf749850176cc3f4958667873db133d0205ca7c5d` |
| [docs/research/batch-22-source-audit.md](batch-22-source-audit.md) | `bb74ee0de3339a351967269c9430cb93f48403a66ae95719ad9530dd3b79a68f` | `bb74ee0de3339a351967269c9430cb93f48403a66ae95719ad9530dd3b79a68f` |

### 2.2 当前正文是否仍是历史复核的输入

逐文件计算哈希并与所列末次复核的输入表比较，五项均相同。因而本轮未把已经漂移的新稿冒充历史通过稿。

| 正文 | 当前 SHA-256 | 对照报告 |
|---|---|---|
| [镜像运行时基线](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) | `96d8364e63a8197e4c477fa278c99bdf7cbbb42c444e4f077454da06e7caa39f` | [T05-01 第 33 次复核](batch-21-t05-01-codex-recheck-33.md) §2 |
| [Kubernetes 生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md) | `15a1b70e514126d87fc9fa2c4b56f4e290f0acadfd9e0c4791f14be58e75b09b` | [T05-02 第 5 次复核](batch-22-t05-02-claude-recheck-5.md) L18 |
| [Slurm 生命周期与资源](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md) | `0e82205bcf30b082c234f3adcdbc8b9baa3e6efbea285323b020c7a8bc7e66c5` | [T05-03 第 4 次复核](batch-22-t05-03-claude-recheck-4.md) L17 |
| [设备资源链](../../knowledge/05-cluster-platform/device-resource-chain.md) | `f2b933842cca3b6b5f943b25a3261530aaf09404813c7687f8b69fde25c91449` | [T05-04 第 5 次复核](batch-22-t05-04-claude-recheck-5.md) L29 |
| [准入与放置](../../knowledge/05-cluster-platform/admission-and-placement.md) | `1c55afd01f4abfd2d1d8dffec8b0cf27d7ad9b1be6a71cc84a22b1900c883e98` | [T05-05 第 5 次复核](batch-22-t05-05-claude-recheck-5.md) L15 |

### 2.3 精确上游证据抽查

本轮不只依赖任务标成 done 或作者摘要；重新读取关键正文段落，并对与关闭理由直接相关的上游证据作有限抽查：

- Kubernetes v1.32 Job 精确版本页：核对失败退避、deadline、terminal conditions 与保留 Pod 的区分；对应正文 L44–72、L122–133，原始链接见[正文来源节](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md)。
- NVIDIA 固定 commit `487d7a93894b0f3ad08097169593972eb3ca8206` 的 `internal/plugin/server.go`：重新取得原文件，抽查运行时 ID 转换和注入路径；对应[设备链](../../knowledge/05-cluster-platform/device-resource-chain.md) L91–100，而非由 generic 或数量一致推定设备身份一致。
- Volcano 固定 commit `8fc394c11e8db0d0ada5c17816b58bced9d7213d` 的 `pkg/scheduler/actions/allocate/allocate.go` L302–338 与 `pkg/controllers/job/state/restarting.go` L20–52：通过 GitHub 只读连接取得带原文件行范围的内容，核对 JobReady 才提交、余量再入队，以及重试上限/回 Pending 的条件；对应[准入与放置](../../knowledge/05-cluster-platform/admission-and-placement.md) L95–97。
- Slurm `overview.html`、`scancel.html`、`priority_multifactor.html` 的 **24.11.7 精确归档页本轮访问失败**，没有用当前主站替代或声称重开成功。补充读取官方仓库已知 tag `slurm-24-11-7-1` 的 `doc/html/overview.shtml` L1–150、`doc/html/priority_multifactor.shtml` L35–135：核对独立 daemon 职责、gang 为分时以及调度评估顺序。此为同发行标签的文档源码抽查，不是归档网页字节一致性证明。版本与原归档页面映射见[来源记录](batch-22-t05-03-sources.md)和[登记](../../sources/registry.yaml)的 `src.slurm.docs-24.11.7`。
- OCI image-spec `v1.1.1/annotations.md` 精确页面已打开；其支持范围仍按[镜像基线](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) §1 的方法层限定，不把注解当作构建可复现或供应链系统已落地的证明。

上述抽查不等于重新完成历史全部来源审计；未成功重开的归档内容沿用已有来源记录与复核历史，并在结论中保留本轮取证限制。

## 3. 发现

优先级为编辑审阅分级，不是生产事故或漏洞严重性；本轮不代作者修订，不将发现自动置 CLOSED。

### B22X-C01 — P3 / OPEN：最终六轮审阅与“五轮元数据均已核验”记录不一致

- **位置：** [batch-22-source-audit.md](batch-22-source-audit.md) L3、L13；对照 L31、[T05-04 第 5 次复核](batch-22-t05-04-claude-recheck-5.md) L5、L176–184。
- **证据：** 审计 L3 已追加第 5 次定向复核通过，却紧接着保留“五轮审阅（初审＋四次定向复核）的模型元数据均经调用方按 CLI 输出核验”；L13 同一任务行先写“初审＋五次定向复核”，后又写“五轮模型元数据均经调用方核验”。磁盘实际存在 1 份初审和 5 份复核，共 **6 轮**。末次报告把自身有效性明确保留给调用方核验；[topic-coverage.yaml](../../plans/topic-coverage.yaml) L59 又作本批模型核验概括，两处审计计数不能准确承接最终轮次。
- **影响：** 无法从这两句准确判断第 5 次复核是否包含于已核验范围。**这不是已经证明第六轮未核验、发生 fallback 或 C44 没关闭**；问题是最终记录的计数与范围矛盾，整批验收不应自行把“五”推成“六”。
- **关闭条件：** 作者依据真实 CLI 输出确认核验覆盖的轮次，将 L3、L13 同步为正确范围；若确已六轮全核验，可写“六轮（初审＋五次定向复核）”，保留指定模型、单一实际模型和无执行回退标记的限定。若实际只核验前五轮，须另补末次核验；不能仅改数字冒充证据。若发现不合约定的执行回退，依编写指南 §7 弃用该轮并走相应重审流程。修订后定向复核 L3/L13/L31、末次报告前提及机器可读概括的一致性；不追改历史报告的实际模型。

### B22X-C02 — P3 / OPEN：章节导航仍称 T05-02/T05-03 待审阅

- **位置：** [knowledge/05-cluster-platform/index.md](../../knowledge/05-cluster-platform/index.md) L42、L44、L62。
- **证据：** L42 写“T05-02 草稿，待审阅”，L44 写“T05-03 草稿，待审阅”；L62 再称两稿“待审阅”。与 [backlog](../../plans/full-coverage-backlog.yaml) L5431、L5468 的 done 状态、[来源审计](batch-22-source-audit.md) L9–10，以及两份末次复核 L5 的通过结论冲突。`f9d8a15` 更新了同一索引中的 T05-04 审阅状态，但未清除这两稿的过时状态；`34d98c9` 的整批收尾也未同步它们。
- **影响：** 读者从正文入口得到的任务审阅状态与收尾账面不一致。L62 的“完整生命周期待审阅验收”若指 **05.2 主题最终验收**，仍应保留其未来边界，不能连同任务审阅状态一起改成整主题已通过。
- **关闭条件：** 作者同步三处措辞：两稿仍为 draft，但任务审阅已闭环、未做真实环境验证；明确 05.2 主题内容验收仍 planned、属 Batch 24，T05-08/T05-10 等未交付。定向复核三处与末次报告、backlog/审计的一致性，并运行结构和本地链接检查；不改正文稳定 ID、编辑/验证状态或历史模型。

## 4. 六项缺口关闭判定

逐项读取 [backlog](../../plans/full-coverage-backlog.yaml) 的 `gap_text`、`task_refs`、`closure_lane`、`validation_refs` 和状态，再对照正文而非只数已交付任务。六项均是 `closure_lane: content`、`validation_refs: []`，关闭不承接现场验证义务。

| 缺口与计划定位 | 正文落点及实质核对 | 结论与保留边界 |
|---|---|---|
| **05.1-G1**（L1853），镜像构建/制品身份/供应链 → T05-01 | [镜像基线](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) L49–64：digest、构建修订/上下文、参数/锁文件、工具版本、SBOM 扫描配置与身份、签名核验及拉取策略；L114 起的环境记录与 K1/K2/K3 区分提供后续观测入口 | **足以按约定方法层关闭。** T05-01 acceptance 明说只记录方法，不宣称已有供应链系统；不是要求已部署制品平台或实际构建/验签成功 |
| **05.1-G2**（L1861），GPU runtime/CDI 专项 → T05-01＋T05-04 | [镜像基线](../../knowledge/05-cluster-platform/container-image-runtime-baseline.md) §2 的固定 OCI/containerd/runc/Toolkit/CDI 样板、权限/注入与 M-ID 表；[设备链](../../knowledge/05-cluster-platform/device-resource-chain.md) L85–130、L166–170 分离账本 ID/运行时 ID、Allocate、CDI/环境注入、健康/重启和回收观察 | **足以关闭所选 GPU 方法范围。** 不证明多卡枚举、index→宿主 UUID 映射或 NPU 兼容；保持其 K1/K2/K3 和独立实现边界 |
| **05.2-G1**（L1915），Slurm 正文与来源 → T05-03 | [Slurm 参考](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md) L26–145 已有架构/Job-Step/状态/节点/取消重排清理/GRES 等实质正文；[来源记录](batch-22-t05-03-sources.md)给出 24.11.7 归档逐页映射，正文 source_refs 可在登记解析 | **足以关闭。** 非只有目录或泛用 K8s 介绍；NPU 接入和现场参数仍 unknown；归档页本轮不可重开见 §2.3 |
| **05.2-G2**（L1923），双平台生命周期/控制器/退出重试清理 → T05-02＋T05-03 | [Kubernetes 生命周期](../../knowledge/05-cluster-platform/kubernetes-job-lifecycle.md) L44–88、L90–126：Job/Pod/Workload 身份、控制器状态链、backoff/deadline/replacement、TTL/finalizer/GC、三类账本核对；[Slurm 参考](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md) L36–62、L93–114、L155–173：Job/Step、COMPLETING、cancel/requeue/Epilog 与验证设计 | **足以关闭双平台内容缺口。** 不把 Running/Complete 当应用正确；平台重建不保证恢复训练状态，也不替代 T05-08/T05-10 的变更/控制面恢复专题 |
| **05.4-G1**（L2002），gang 成组启动/失败/回退 → T05-05 | [准入与放置](../../knowledge/05-cluster-platform/admission-and-placement.md) L82–102：minMember/minResources 分层、valid/ready/pipelined、Commit/Discard、调度重试与控制器 RetryCount/Restart/Failed/Pending；明确不等于应用 rendezvous | **足以关闭固定实现样板。** handler 事件路径全覆盖仍 unknown；但已有机制和失败回退正文，不因尚未实测就重开内容缺口 |
| **05.4-G3**（L2019），其他平台调度独立来源 → T05-03＋T05-05 | [Slurm 参考](../../knowledge/05-cluster-platform/slurm-jobs-and-device-resources.md) L116–139 与[准入与放置](../../knowledge/05-cluster-platform/admission-and-placement.md) L157–173 分别引用 Slurm 24.11.7 的 partition/QOS/priority/reservation/GRES 页；与 Kueue 样板 A、Volcano gang 分开，来源页不是 K8s 页面转述 | **足以关闭。** 不把 Slurm gang（分时）套成 Volcano 成组放行，也未由 GPU 样板推出 Slurm NPU 支持 |

**没有把尚待 T05-06–T05-10 的缺口误关。** 逐项核对结果如下；这些未交付任务仍为 `planned / needs_source_preparation`。

| 仍 OPEN 的缺口 | 尚未交付的必要任务 |
|---|---|
| 05.1-G3 | T05-06；虽已有 T05-01，仍不足以关闭容器隔离主题缺口 |
| 05.4-G2 | T05-07；已有 T05-05 的有限样板不替代完整策略权衡任务 |
| 05.5-G1 / G2 / G3 | 分别 T05-06 / T05-07 / T05-06＋T05-07 |
| 05.7-G1 / G2 | 分别 T05-10 / T05-10（另有 T05-04 已交付） |
| 额外抽查 05.6-G1 / G2 / G3 | 分别 T05-08 / T05-09 / T05-08＋T05-09；均未误关 |

## 5. 账面一致性与 exit_gate

### 5.1 任务与历史复核

四任务均为 `done / source_preparation_completed`，T05-01 也为该状态，但仍归 Batch 21，不混入 Batch 22 的四个 `task_refs`。审计任务表中的通过结论与下列末次报告逐一一致：

| 任务 | 真实报告链 | 历史发现结果 |
|---|---|---|
| T05-02 | 初审＋5 次复核，共 6 份 | [末次](batch-22-t05-02-claude-recheck-5.md) L5：B22-C01–C11，11 CLOSED / 0 OPEN |
| T05-03 | 初审＋4 次复核，共 5 份 | [末次](batch-22-t05-03-claude-recheck-4.md) L5：B22-C12–C21，10 CLOSED / 0 OPEN |
| T05-05 | 初审＋5 次复核，共 6 份 | [末次](batch-22-t05-05-claude-recheck-5.md) L5：B22-C22–C30，9 CLOSED / 0 OPEN |
| T05-04 | 初审＋5 次复核，共 6 份 | [末次](batch-22-t05-04-claude-recheck-5.md) L5：B22-C31–C44，14 CLOSED / 0 OPEN；模型核验计数见 C01 |
| 前置 T05-01 | 沿用第 33 次复核，不把“33 次”改成当前重审次数 | [末次](batch-21-t05-01-codex-recheck-33.md) §1：C30–C34 闭环，acceptance 4/4 |

本批在库 Claude 报告计 23 份。B22-C01–C44 合计 **44 CLOSED / 0 OPEN** 是这些报告的累计历史状态；本轮新增 B22X 两项另列，不能混作原 44 项未关闭。

### 5.2 Batch 22 exit_gate 逐项落点

[backlog](../../plans/full-coverage-backlog.yaml) L3673 起的批次状态为 done，四个 task_refs 正确；原 exit_gate 文本保留。

| gate 项 | 落点与本轮判断 |
|---|---|
| 目标产物交付 | T05-02/03 两篇新稿、T05-04/05 两篇修订稿均在；ID 与正文哈希见 §2.2。导航可达，但状态措辞有 C02 |
| 来源审计 | 四任务各自 `batch-22-t05-XX-sources.md`、registry 与整批审计在；本轮抽查范围和无法重开的来源如实区分 |
| 指定模型审阅 | gate 字面写 gpt-6.1-sol/xhigh；按 authoring-guide §7 的 2026-10-13 试用补充，历史 claude-opus-5-5 可作为约定路径，不据此追改历史模型。本轮为另行指定的 Codex 整批审阅；历史调用方核验仅按记录引用，C01 待澄清 |
| 发现修订与定向复核 | 末次报告与修订链支持原 44 项全 CLOSED；本轮两项记录发现尚 OPEN |
| make check/build | 本轮实际执行并通过，见 §7；不当作技术正确性或现场执行证据 |
| 对应主题范围复核 | 六个 content 缺口与正文逐一对照成立，其他缺口及未来主题验收保持；不是要求所有关联主题在本批升 covered |

## 6. 主题口径与保留边界

- **无主题升为已覆盖：成立。** 解析两次收尾提交前后的 YAML：`plans/topic-coverage.yaml` 只有 `batch_planning.notes` 改动，topics、documents 和基线快照未改。05.1/05.2/05.4/05.7 仍 partial，05.5/05.6 仍 missing，05.3 仍为原 covered。
- **未来主题验收未提前：成立。** backlog 中 05.1/05.4/05.5（额外检查 05.6）均 Batch 23、planned；05.2/05.3/05.7 均 Batch 24、planned。05.3 的 covered 是基础判断，不是本批最终 v1 达标。
- **Batch 17–21 未回填：如实披露，但不能把盘点当完整最新快照。** Markdown 盘点 L3 明确写了未回填及批次账面待订正；机器可读 notes 只追加实际 B13–16 与 B22 更新，没有执行 B17–21 主题/文档数组的回填。YAML notes 未逐字复述该提醒；结合其保留基线及 Markdown 披露，本轮不据此另判为已声称全量回填。T05-01 作为具体前置闭环被引用，不等于 Batch 21 整批盘点已补全。
- **closure_criteria 保留：成立。** 对 `f9d8a15^` 至 HEAD 的解析结果逐主题比较，63 个主题的 closure_criteria 数组全部未变；稳定 ID、真实模型历史、新稿 draft、方法层交付不等于 reproduced 的条款均保留。
- **正文编辑/验证状态未升级：成立。** 五篇正文均为 `status: draft / verification.status: source_checked`；两次收尾提交没有修改这五篇正文。既有 Ascend 指南/公开案例/方案入口保留，Slurm NPU 和未建立的版本支持交集继续 unknown。
- **已披露的 M-ID 张力不被本轮消失化。** 整批审计 L32 仍保留 T05-01 M-ID② 与 T05-04 账本 ID/运行时 ID 口径的跟进候选。本轮 G2 的关闭判定只针对已选 uuid 单卡方法与专项内容覆盖；不据此认可未选 index 分支的泛化表述，也不把该候选算成已修复。本轮不借整批收尾越界重审或修改 T05-01 已闭环正文；如扩大到该分支，应单独立项。

## 7. 结构校验与波及检查

### 7.1 实际执行的本地检查

运行 `PYTHONDONTWRITEBYTECODE=1 make check` 和 `PYTHONDONTWRITEBYTECODE=1 make build`，均 exit 0：

```text
PASS: 96 content entries; 446 sources.
Checked structure and local file links; not technical correctness or remote links.
Built build/catalog.json and build/catalog.md.
```

`make build` 仅按授权重建生成目录；`git ls-files build` 无跟踪文件，检查后 `git status --short` 仍为空。上述计数是本轮实际值；审计中较早的 444 sources 记录不被追改成当前快照。未运行上游测试、集群/设备命令，也未因本轮仅新增审阅报告而新增测试。

### 7.2 两个收尾提交

实际执行了用户要求的 `git show 34d98c9 --stat` 与 `git show f9d8a15 --stat`，并查看差异、解析 YAML 前后变化：

| 提交 | 实际改动 | 波及判断 |
|---|---|---|
| `f9d8a156a748f47e864000c732a743ad17442f6a` | 4 文件，204 增/9 删：新增 T05-04 第 5 次复核报告 195 行；整批审计同步；章节 index 两处 T05-04 状态说明；backlog 的 T05-04 status/readiness | 符合所述，未夹带正文、来源、实现代码或其他任务改动；本轮发现其记录收尾残留 C01/C02 |
| `34d98c9010246c29c5921feba087294abcce0b2a` | 4 文件，17 增/17 删：整批审计标题/待办、Markdown 盘点头段、YAML 盘点 notes、backlog | 符合所述；backlog 精确为 T05-02/03/05 的 6 个状态/准备度字段、批次 22 的 1 个状态字段、6 个缺口状态字段；没有多关闭缺口 |

除本报告外，不修改作者文件，不提交、不建分支；未变更用户授权、源文件许可或外部 notices。

## 8. 局限与后续判据

1. 本轮是整批收尾独立审阅，不是对所有历史技术细节重新首审。历史全 CLOSED 的事实依据是具体复核报告与当前正文哈希一致；历史会话原始 CLI 元数据未在本轮逐轮重放核验。
2. 上游抽查有明确边界，尤其 Slurm 归档页本轮不可访问；成功取得的同标签官方文档源码不能被写成归档网页成功重开或字节身份证明。
3. 未读取集群/设备现场状态，未安装、构建镜像、生成 SBOM、验签、提交作业、运行容器或执行恢复/隔离实验；方法、unknown、实测证据分别处理。没有新环境档案，不标 reproduced。
4. 仅需作者针对 B22X-C01/C02 修订记录，并由同一审阅者定向复核；复核时同时确认输入未漂移、六个缺口与未来验收边界未被扩大。**本报告不替作者完成修订，也不预先宣布发现关闭。**

## 9. 模型与运行元数据核验

- **指定值与会话自述：** 本轮按用户要求使用 Codex 审阅角色，指定 `gpt-6.1-sol / xhigh`。仅有自述不足以证明执行身份，因此另读本地 CLI 会话记录，而非把提示词中的模型名作为核验结果。
- **实际读取的 CLI 元数据：** 会话 ID `01a14a28-8094-70a2-9362-ae55195c77fe`；文件为 `~/.codex/sessions/2026/10/17/rollout-2026-10-17T21-58-50-01a14a28-8094-70a2-9362-ae55195c77fe.jsonl`。`session_meta` 记 `originator=codex_exec`、`source=exec`、`cli_version=0.157.1`、`model_provider=custom`，创建时间 `2026-10-17T13:58:50.833Z`（本地 21:58:50）。`codex --version` 同时返回 `codex-cli 0.157.1`。
- **模型/档位核验结果：** 成稿前解析所见 1 条 `turn_context`，`model=gpt-6.1-sol`、`effort=xhigh`；其 `collaboration_mode.settings.model` 同为 `gpt-6.1-sol`，`reasoning_effort=xhigh`。所见执行上下文为单一指定模型/档位，**不是仅凭会话自述**。这确认本地 CLI 所记执行上下文，不是独立的服务端路由、实际底层计算模型或供应商证明；`custom` 不被解释成已证明另一个模型，也不被隐去。
- **fallback 检查：** 成稿前对本会话已落盘的 4 段 assistant `output_text` 进行执行回退标记检索，未发现实际回退标记、切换到其他模型的运行输出或认证/路由失败事件。提示词、引用历史报告、工具参数或本节说明性出现的 `[frontier_llm]`/fallback 字样不算发生回退。`codex --version/exec --help` 的 PATH aliases 权限警告不是模型回退；本轮没有另启一个 Codex 子会话，也未因它切换模型。
- **历史模型核验的证据等级：** B22 各 Claude 报告的模型自述与调用方在审计/盘点中所记的 CLI `modelUsage` 核验分开看待；本轮没有读取其 23 轮原始 CLI 输出，不能升级为“本审阅者独立核验每轮实际模型”。T05-01 第 33 次复核自带本地元数据核验说明，按历史记录保留；C01 只要求把 T05-04 最终轮次的核验范围说准确，不伪造任何历史元数据。

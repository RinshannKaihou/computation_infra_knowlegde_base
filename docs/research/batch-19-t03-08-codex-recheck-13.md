# 第十九批 T03-08 第十三次定向复核

审阅日期：2026-10-13（Asia/Shanghai，本机日期确认）。正文 `updated_at: 2026-10-14` 及部分来源登记日期晚于本轮日期，仅视为作者交付标签，不作为取证日期或历史执行证明；输入身份以下表 SHA-256 为准。

**结论：C27 仍 OPEN（1 项 P2）；C01–C26 保持 CLOSED，含 C24，不重开。累计 26 CLOSED / 1 OPEN（共 27 个审阅发现），T03-08 第十三次定向复核未通过。** 第十二次报告第 3 条的三项余项——第四轮具体复用记录、#223 未采用与历史实开 unknown、L19 当前定位纠正——本轮均接受关闭。作者十三轮及输入既有审阅十三份的总述也已同步；但 verification 明确指向的逐轮账本仍仅有首轮至第十二轮十二行，第十二轮还无历史限定地标“本轮”，没有第十三轮与其修订节的账本行。该同步缺口按原 C27 追记，不新增 ID，不撤回已接受条件。

约定配置 `gpt-6.1-sol / xhigh` 仅为用户约定，不写成已独立确认的执行模型或推理等级。执行者为当前 Codex 主会话，角色为独立审阅者，与作者修订角色分开；无子代理。本轮只写本报告，不代作者修订。

## 输入与复核范围

| 输入 | SHA-256 |
|---|---|
| [T03-08 正文](../../knowledge/03-communication/bandwidth-degradation-triage.md)（procedure / draft，verification L27–34） | `8c42b486e7aca25638254f43f7eca1a2b6ab90ddc3367f462a1425159c8c2368` |
| [作者来源记录](batch-19-t03-08-sources.md)（L3 总述；逐轮账本 L5–22；主张表 L24–34；unknown L36–38） | `f5a683b13936a6d5aceaa4c33eae5de596bc24797f65731d0324e2b3ec402481` |
| [修订映射](batch-19-review-fixes.md)（第十三轮 L165–167） | `e05deb03fd5d30b8869a188d567d6b44191a7f6aace34789a56c151458929628` |
| [第十二次定向复核](batch-19-t03-08-codex-recheck-12.md)（剩余关闭条件 L95–100） | `293ff6a82a2010aef5442359276f741e1bce3e2e1d71b2062d51e5c7b27e23eb` |
| [任务验收](../../plans/full-coverage-backlog.yaml)（T03-08 acceptance 1–4，L5006–5010） | `121826a4d499273e7f6a00735e0a53931eef5c097bd66ab6b2425fdbc36ddfe0` |

以第十二次报告 L98–100 为三项剩余关闭条件的权威来源，L97 为已接受条件保持边界，并检查用户本轮明确要求的 verification/记录轮次同步。不重验 C01–C26，不重新判定 #2409/#814/#209 的案例原因、反证或修复结论，不重新验收 T03-06 acceptance 5。

| 补充只读输入 | SHA-256 |
|---|---|
| [来源登记](../../sources/registry.yaml) | `277aecb64892438a366c1729fe01210cbeae60845ff6fbefce437a7a7a96901e` |
| [T03-07 基线口径](../../knowledge/03-communication/bandwidth-baselines.md)（矩阵 L144–161） | `8c2884b63cf7b638c1df2d7de88f5fe9d2923c0d95b025548041aea203574039` |
| [T03-03 RDMA 诊断](../../knowledge/03-communication/rdma-baseline-and-congestion-triage.md) | `7f6d59752e7c74628f2c9d706ce2ec00e3031ecd36230554eb8d2680fee67412` |
| [T03-05 RCCL 档案](../../knowledge/03-communication/rccl-runtime-and-verification.md)（工具 L69–71） | `1f95d5b310726d858900e2028ab3b779f1470b03a1ba67187fbed1c6da5b19db` |
| [T03-06 三库对照](../../knowledge/03-communication/communication-library-profiles.md)（工具 L65；交集限制 L74–76） | `d4a5fb535ba78d852e070f09ff387b69dc6e1ab7cf86620c7ee08e9a99577646` |
| [第四次定向复核](batch-19-t03-08-codex-recheck-4.md)（当时来源定位 L88–95） | `80a9860817beca3ce65cf6b83acadb519350d343d9d2b898d7d3e4988eea29c3` |
| [第五次定向复核](batch-19-t03-08-codex-recheck-5.md)（工具文件 URL 落盘 L88） | `f54bff372b66ec6f9503c0e91d3dba915f9fa11e03cfd18626224f5ba4027a41` |
| [第九次定向复核](batch-19-t03-08-codex-recheck-9.md)（第二轮候选 L93；历史差异 L102） | `9d0027c03fd59529cb8d7f8e6b246d1e998e6752354df4a8c72fd510a9135b10` |
| [第十次定向复核](batch-19-t03-08-codex-recheck-10.md)（#223 状态要求 L75） | `6d52df81f494232d2bcf0e9ca20de234f1b40b8ee9051da2e708ff3f7526c0bb` |

补充登记与四篇依赖正文的 SHA 均与前次报告所列一致。历史报告用于定位当时记录和判定，不将审阅者取证转记为作者取证；本轮对第四轮的接受限于作者已补交的回溯复用关联，不独立认证历史远程执行。

## 一次源取证与方法限制

采用本地只读逐行核对、默认 TLS 校验的只读 curl、允许的网页阅读器（`web.run`）及 GitHub 连接器。curl 对 UFM 精确端口页与 RCCL `therock-10.1` troubleshooting 文件 URL 两次均返回退出码 6 / DNS 解析失败，HTTP `000`，未取得响应正文。网页阅读器读取以下四个 NVIDIA 页面成功；RCCL tag 文件的网页阅读器请求返回 Internal Error，随后 GitHub 连接器返回该精确 tag 文件原行 L129–203。

| 一次源 / 已登记 ID | 本轮精确定位与通道 | 核对范围 / 限制 |
|---|---|---|
| `src.nvidia.nccl-user-guide-2.27.5`：env | 网页阅读器：[SPLIT_DATA_ON_QPS 节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/env.html#nccl-ib-split-data-on-qps)，阅读器 L599–606 | 对应来源 L12/L29/L38 第 9 项的分摊与默认值入口；只核对所指文档，不证明历史实开或现场配置。 |
| 同一 NCCL 归档 ID：ACS | 网页阅读器：[troubleshooting ACS 节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting.html#pci-access-control-services-acs)，阅读器 L50–54 | 重定向语义归 troubleshooting；不混入物理错误计数，不执行页内命令。 |
| 同一 NCCL 归档 ID：RAS | 网页阅读器：[sample-output 节](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2275/user-guide/docs/troubleshooting/ras.html#sample-output)，阅读器 L19–61 | MISMATCH 示例与重复查询解释可定位；不建立链路硬件证据。 |
| `src.nvidia.ufm-41815-port-counters` | 网页阅读器：[InfiniBand Port Counters](https://networking-docs.nvidia.com/ufmsdnappswum/41815/infiniband-port-counters)，阅读器 L121–133；登记 L4520–4530 | 四项字段全名可对应，收错含 overrun、丢弃多因的范围保持。完整版本后缀沿用登记；本轮阅读器未显示 `4.18.15` 字串，不宣称独立实测版本选择器，也不重开既有版本范围。 |
| `src.rocm.rocm-systems-therock-10.1` | GitHub 连接器：[作者所链 tag 文件](https://github.com/ROCm/rocm-systems/blob/therock-10.1/projects/rccl/docs/how-to/troubleshooting-rccl.rst)，原行 L129–203；Git blob `89779e32d545fcd1f61a7dc728e0abf9113bc186` | Using the RCCL Replayer / Collect the TransferBench data 两节可定位，分别为 collective 日志回放与设备间并发拷贝基准。只确认源码用途，不记为 HTML 成功、真实替代路径或历史作者执行。 |

阅读器行号只作本报告定位，不拼为 GitHub 原文件行锚点；Git blob 身份不混作 SHA-256。curl 未取得远程字节，不补造远程 SHA-256。本轮不实开 #223 或其他未采用候选，不重取八条已接受的案例评论，不补 HCCL 官方交集或进行新一轮案例技术验收。替代通道的当前可读性既不倒证作者历史实开，也不因 curl 失败否认其历史自述。

## B19-C27 — P2 / OPEN：三项余项关闭，十三轮账本目标仍不同步

位置：来源记录 L3/L5–22，尤其 L10/L12/L16–17/L20；unknown L36–38；映射 L165–167；正文 verification L34。子条件 CLOSED/OPEN 不产生新 ID。

| 本轮核对项 | 判定 | 位置与证据 |
|---|---|---|
| 1. 第四轮具体复用、未知边界与无新增远程主张 | CLOSED（记录关联接受） | 来源 L12 不再仅写“以复用已核对来源为主”：列 #2409/#814 八条评论（L31–33）、NCCL env/ACS/RAS 三锚点（L29）、UFM 4.18.15 精确页（L29＋登记 L4520–4530）、RCCL `therock-10.1` troubleshooting 两节（L30）、T03-07 跨节点矩阵及 T03-06/RCCL 档案入口（正文步骤 9 L77）。版本/入口有明确指向；L3/L5 保留无法还原通道的 unknown，L22 保留回溯补记解释；L12 明说无新增远程取证主张、不追加远程取证。接受作者复用范围的补记，不扩大为历史逐页实开或未列对象也已核对。 |
| 2. #223 未采用；历史实开 unknown | CLOSED | 来源 L10 明确未在登记/主张表/正文采用、现为未采用候选且不引用；无精确 URL/版本记录，历史是否实开无法还原记 unknown。映射 L167 对应。第九次 L93 / 第十次 L75 的历史名称未被抹去，但没有由名称、当前省略或相邻轮次自行判定其历史采用状态。本轮不选入口、不实开候选。 |
| 3. L19 当前定位与历史坐标 | CLOSED | 来源 L3/L16 改指 `unknown 清单` 的“未采用候选”条目；L3/L17 改指该清单第 9 项“NCCL 三页已用”。实际目标仍为 L36 节、L38 第 9 项；新增账本不再用“本记录 L19”定位当前清单。映射 L147/L151 的 L19 保留为第八/九轮旧记录坐标；L167 明确本轮改稳定节/条目名称，不将旧坐标作为当前位置。历史报告原始坐标不要求追改。 |
| 4. verification、作者十三轮与既有审阅十三份同步 | OPEN（总述计数 CLOSED；所指账本交付未同步） | 正文 L34、来源 L3、映射 L165–167 均正确写作者十三轮及输入既有审阅十三份；初审＋一至十二次复核的十三个文件均存在，未把本报告计入输入。但正文 L34 还称“逐轮明细精确引用来源记录逐轮账本表”，该表 L9–20 仅十二行，缺第十三轮，L20 仍写“第十二轮修订（本轮）”且未限定为当轮历史自指。总述与映射不能替代已指名账本目标中的缺行与当前轮指向。 |

### 已接受条件保持

第十二次报告 L97 所要求的保持边界未撤回：C01–C26 均 CLOSED；映射 L149/L151/L159 的累计、历史对象及输入时点限定保留；第三/五/六轮 unknown、第七轮目标与第八/九轮落盘拆分、L22 回溯补记解释保留；来源主张表 ID—精确 URL—字段—范围、工具用途、原批遥测限定及实测矩阵未交付的范围保持。第四/五次旧报告中工具 URL 的落盘时点只用于限制历史解释；本轮不把补交复用关联改写为第四轮已交付完整映射，也不倒灌审阅者源码取证。

本轮新追记的事实差异只有账本目标仍停在十二轮及“本轮”指向未更新，均属于 C27 的记录同步问题。它不重开前次已接受的十三份输入计数规则，不否认十三轮修订节已存在，更不要求追加远程取证或实验。

## 剩余关闭条件（仅 C27，账本同步）

1. 保持本轮三项 CLOSED 及前次已接受条件。第四轮具体复用、通道 unknown 和无新增远程主张、#223 未采用/历史实开 unknown、稳定清单定位及历史坐标边界均不撤回；C01–C26 不重开。
2. 在 verification 已明确指向的作者逐轮账本中，补第十三轮与 `T03-08 第十三轮修订` 的对应行，记录该轮实际的三项补记及无新增远程取证/仅复用范围。可以精确复用来源 L3、映射第十三轮节等已有记录，不要求补造响应、日志或历史执行。
3. 将账本第十二轮行的“本轮”去除或明确限定为第十二轮当时自指，使当前第十三轮在总述、账本、映射及 verification 中一致。输入既有审阅仍是十三份（初审＋一至十二次复核）；本报告交付后才是十四份审阅记录，不计入本轮输入，也不自行产生作者第十四轮。

## 状态集合与验收影响

| 状态 | ID / 范围 |
|---|---|
| 本轮整项新增 CLOSED | 无；第十二次报告第 3 条三项余项 CLOSED，不另计 ID |
| 既有 CLOSED（26；不重开） | C01–C26，含 C24 |
| 本轮 OPEN（1 P2） | C27，仅上述账本同步余项 |
| 累计审阅发现 | **26 CLOSED / 1 OPEN**（共 27 个 ID，未新增） |
| 既有验收子项 OPEN（单列） | BLOCKED-1，`blocked_on_evidence`；不计入发现数量 |
| T03-08 | **第十三次定向复核未通过**；后续仅复核账本同步及已接受条件保持 |
| T03-06/T03-07 | 有限文档/来源范围通过保持；不重新验收 T03-06 acceptance 5 |
| Batch 19 | 未完成整批验收，不由来源可读、三项子条件关闭或总述计数更新推导全部完成 |

acceptance 1 的时窗/矩阵契约、acceptance 2 的四分支与物理门禁、acceptance 3 的既有案例结论、acceptance 4 的对照/复现输入/风险/停止/恢复与资料入口保持原 CLOSED 范围，不重新技术验收。C27 仍限制作者记录可追溯性的闭环。BLOCKED-1 的 HCCL Test × 目标 CANN/HDK/机型官方交集缺口保持；模型审阅、文档核对与结构校验不建立现场复现或版本兼容交集。正文仍为 draft / source_checked。

## 检查边界与写入范围

- 仅新增本报告，不改作者正文、来源记录、修订映射、登记、计划、索引或来源审计；不恢复既有工作区改动，不提交、不创建分支。
- 不执行 benchmark、collective/MPI、实机采集、配置修改、故障注入或上游诊断命令；引用的命令只阅读，未取得现场遥测、时钟、字段能力或实验结果。
- curl 两次 DNS 失败、RCCL 网页阅读器失败及替代 GitHub 源码通道如实分列；不宣称 HTML/锚点浏览器实测或作者历史远程执行成功。
- 为遵守“只写这一份报告”，结构校验在仓库外临时快照执行，不重建原仓库 `build/`；不改 `src/kb/`，不执行 `make test`。结构校验不验证技术正确性、历史取证或远程语义。
- 含本报告的临时快照执行 `make check` / `make build` 均 PASS（88 content entries / 389 sources）；报告 14 处本地链接、14 个不同目标均存在。账本行计数另行只读核对为十二行，无第十三轮行；构建通过不消除该记录同步缺口。
- 写入前后 SHA-256 / 符号链接清单核对：原有 3487 个常规文件（含 `.git`、既有构建与本地环境文件）及 3 个符号链接均不变，无删除，仅新增本报告；五项任务输入及补充输入与 SHA 表一致。临时快照与清单均在仓库外，不作为现场验证证据。

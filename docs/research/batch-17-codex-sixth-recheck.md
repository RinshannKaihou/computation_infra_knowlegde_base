# 第十七批第六次定向复核记录

复核日期：2026-10-09（Asia/Shanghai）。**第五次报告的三项修订要求均已满足，本轮无新增修改项。B17-C08 仍 OPEN（P2），当前阻止关闭的证据范围为累加精度与固定实现关联；累计 12 项 CLOSED、1 项 OPEN，Batch 17 暂不通过。** 已通过的表述、适用条件与元数据修订不再列为待办，不新增发现 ID，不重开已关闭项。

依据：[第五次定向复核](batch-17-codex-fifth-recheck.md)、[第六轮修订记录](batch-17-review-fixes.md)、[完整覆盖路线图](../full-coverage-roadmap.md)、[T02-10 验收清单](../../plans/full-coverage-backlog.yaml)和[批次审阅约定](../authoring-guide.md#7-批次审阅约定)。执行者为初审及前五次复核的同一 Codex 主助手，与正文编写者分开，未派发子代理。用户约定为 `gpt-6.1-sol / xhigh`；沿用此前披露，本会话没有可独立核验的实际运行标识，不把约定当作已确认的执行元数据。

## 输入与核对范围

| 输入 | 第六次复核 SHA-256 |
|---|---|
| [精度正文](../../knowledge/02-software-stack/dtype-layout-and-precision-semantics.md) | `b1d0f64bf045a6eb77c049e24c13ec20e738f42aff5a2e89e571dbeb3f19cfab` |
| [精度研究记录](batch-17-dtype-precision-sources.md) | `1e4a0908bbb02c3d1f1b65451dfd45484179672ed24851a82d0bd59163a586fc` |
| [修订记录](batch-17-review-fixes.md)（追加本次结果前） | `1c4cc0aaf03ed45c177d82f07665283af50c729aa1edca860562083c50204fb1` |
| [来源登记](../../sources/registry.yaml)（340 项，本轮不改） | `2b100cf829e4db7373f2e5607f958bddcd4e85d51c7e6e723cb1a8fee5f9ea00` |

重读正文 L61、L104、L107、L117、数据类型/Matmul 登记及第六轮研究附录。复用第五次独立取得的版本化静态 Markdown，重新核对相关原文；两个临时响应摘要与第五次报告一致（数据类型 `31024e3939fa672a92af6d35f9fc5d06c6c3b85f311d70790312f72da5558420`，Matmul `c4fa0ef483cade0d51a84ba489d43a8d3bceb469fbaed115ccb12a03b4d7d235`）。没有重新下载或执行样例，也没有新增来源。

其他三篇正文、领域索引、其他三份研究记录与 backlog 的摘要和第五次输入一致，本轮不重新验收已关闭项。

## 三项修订判定

| 第五次待修订项 | 本轮判定 | 当前定位与核对结果 |
|---|---|---|
| 简写表来源范围 | 已满足 | 精度 L104、L61 与 `src.huawei.cann-82rc1alpha001-acl-datatype` title/notes 一致：19 行原始名/简写名两列，含 STRING，无 torch 列；完整类型另指 AscendCL 文档且明确未取得，不补推全量或映射 |
| Matmul 适用条件及 SDK/实现边界 | 已满足 | 精度 L107 与 Matmul 登记补齐 KEEP_DTYPE 的训练/推理 FLOAT32 限制、USE_FP16 的 A2 BFLOAT16 排除、先推导再处理、out 一致性及双一维输入选项不生效；把官方 SDK 契约和 TorchNPU 注册分别记录，不宣称已建立实现关联 |
| verification 取得范围 | 已满足 | 精度 L61 明确 Add/Matmul 两算子正文已取得；其余逐算子正文、累加精度及相关实现仍未覆盖，不再无条件称 CANN 逐算子表未取得 |

数据类型判定对照[登记的简写表](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/common/%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B.md) L3、L7–27；Matmul 判定对照[官方算子页](https://www.hiascend.com/doc_center/source/zh/CANNCommunityEdition/82RC1alpha001/API/aolapi/context/aclnnMatmul.md) L36、L39–49、L78–80。行号为第五次保存的原始响应坐标，不是网页阅读器坐标。第六轮研究附录已纠正第五轮旧概括；历史前段保留，不另计新发现。

## 剩余开放条件与状态

**B17-C08 — P2，OPEN。** 精度 L117 的累加精度与 TorchNPU 侧 cubeMathType 实现关联继续 unknown；当前处理符合原强制证据边界。官方计算逻辑契约及本轮补齐的产品/类型/维度条件已核实，不再概括为未取得。其他既有 unknown（完整类型文档、映射表逐项等）保持原范围，不由本次表述修订补作验收。

关闭条件沿用第五次报告的未验收范围：取得版本与适用条件明确的逐算子累加精度证据，以及可定位到固定版本/修订的相关计算实现依据，记录实际参数选择/调用关系。普通 autocast 注册、输出 dtype 或 Cube 计算选项本身均不能代替累加数据类型及实现关联证据；未取得时继续 OPEN。后续只定向复核新取得的证据和正文/登记/研究记录同步，不重复要求修改本轮及第四次已通过的限定。

累计 CLOSED：C01、C02、C03、C04、C05、C06、C07、C09、C10、C11、C12、C13（12 项）；OPEN：C08（1 项 P2）。T02-10 继续暂不通过，不解锁依赖其完成的任务。条目保持 `draft / source_checked`，backlog 和主题覆盖状态不调整。

独立 `make check` / `make build` 均 PASS：83 content entries / 340 sources。本轮只新增第六次复核报告、更新审阅状态并追加结果，未改知识正文、四份作者研究记录、来源登记或 `src/kb/`；未新增代码测试，未执行设备/集群、数值或性能实验，未重新全量审查许可。结构检查不证明技术正确性或硬件验证。
